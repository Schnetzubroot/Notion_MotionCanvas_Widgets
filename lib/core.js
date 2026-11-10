/* Mechanik-Widgets: kleine Bibliothek für 2D/3D-Zeichnungen, Regler und Animation. */
(function () {
  'use strict';
  const V = {
    add: (a, b) => a.map((x, i) => x + b[i]),
    sub: (a, b) => a.map((x, i) => x - b[i]),
    mul: (a, s) => a.map(x => x * s),
    dot: (a, b) => a.reduce((s, x, i) => s + x * b[i], 0),
    cross: (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]],
    norm: a => Math.sqrt(a.reduce((s, x) => s + x * x, 0)),
  };
  V.unit = a => { const n = V.norm(a); return n < 1e-12 ? a.map(() => 0) : V.mul(a, 1 / n); };

  const fmt = (x, d = 2) => {
    if (!isFinite(x)) return '–';
    const p = Math.pow(10, d), r = Math.round(x * p) / p;
    return (Math.abs(r) < 1e-12 ? 0 : r).toLocaleString('de-CH', { maximumFractionDigits: d });
  };
  const fv = (a, d = 2) => '(' + a.map(x => fmt(x, d)).join(', ') + ')';
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const colors = () => ({ fg: css('--fg'), muted: css('--muted'), grid: css('--grid'), line: css('--line'), bg: css('--bg'),
    c1: css('--c1'), c2: css('--c2'), c3: css('--c3'), c4: css('--c4'), c5: css('--c5'), field: css('--field'),
    acc: css('--acc'), fill: css('--fill'), warn: css('--warn') });
  const FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

  // ---------- controls ----------
  function slider(parent, o) {
    const w = document.createElement('div'); w.className = 'sl';
    w.innerHTML = `<span class="n">${o.label}</span><input type="range" min="${o.min}" max="${o.max}" step="${o.step || 0.01}"><output></output>`;
    const inp = w.querySelector('input'), out = w.querySelector('output');
    const show = () => { out.textContent = o.fmt ? o.fmt(+inp.value) : fmt(+inp.value) + (o.unit || ''); };
    inp.value = o.value; show();
    inp.addEventListener('input', () => { show(); o.onInput && o.onInput(+inp.value); });
    parent.appendChild(w);
    return { get: () => +inp.value, set: v => { inp.value = v; show(); }, el: w };
  }
  function check(parent, label, checked, onChange) {
    const l = document.createElement('label');
    l.innerHTML = `<input type="checkbox" ${checked ? 'checked' : ''}> ${label}`;
    const i = l.querySelector('input'); i.addEventListener('change', () => onChange(i.checked));
    parent.appendChild(l); return { get: () => i.checked, set: v => { i.checked = v; } };
  }
  function select(parent, label, options, onChange) {
    const l = document.createElement('label'); l.textContent = label + ' ';
    const s = document.createElement('select');
    options.forEach(([v, t]) => { const o = document.createElement('option'); o.value = v; o.textContent = t; s.appendChild(o); });
    s.addEventListener('change', () => onChange(s.value)); l.appendChild(s); parent.appendChild(l);
    return { get: () => s.value, set: v => { s.value = v; } };
  }
  function button(parent, text, onClick) {
    const b = document.createElement('button'); b.textContent = text; b.addEventListener('click', onClick); parent.appendChild(b); return b;
  }
  // time control: play button + slider for t in [t0, t1]
  function player(parent, o) {
    const btn = button(parent, '▶ Abspielen', () => (running ? pause() : play()));
    const s = slider(parent, { label: o.label || 't', min: o.t0, max: o.t1, step: (o.t1 - o.t0) / 400, value: o.value ?? o.t0,
      fmt: o.fmt, onInput: v => { pause(); o.onTime(v); } });
    let running = false, last = 0, raf = 0;
    const speed = (o.t1 - o.t0) / (o.duration || 6);
    function frame(ts) {
      if (!running) return;
      const dt = last ? (ts - last) / 1000 : 0; last = ts;
      let t = s.get() + dt * speed;
      if (t > o.t1) { if (o.loop === false) { t = o.t1; s.set(t); o.onTime(t); pause(); return; } t = o.t0 + (t - o.t1); }
      s.set(t); o.onTime(t); raf = requestAnimationFrame(frame);
    }
    function play() { running = true; last = 0; btn.textContent = '❚❚ Pause'; raf = requestAnimationFrame(frame); }
    function pause() { running = false; cancelAnimationFrame(raf); btn.textContent = '▶ Abspielen'; }
    return { get: () => s.get(), set: v => { s.set(v); o.onTime(v); }, play, pause };
  }
  function info(el, head, rows, note, warn) {
    el.innerHTML = (head ? `<div class="head ${warn ? 'warn' : ''}">${head}</div>` : '') +
      rows.map(([k, v]) => `<div><span class="k">${k}:</span> <span class="v">${v}</span></div>`).join('') +
      (note ? `<div class="note">${note}</div>` : '');
  }

  // ---------- common canvas base ----------
  function base(canvas, draw) {
    const ctx = canvas.getContext('2d');
    const st = { canvas, ctx, W: 0, H: 0, draw, raf: 0 };
    st.redraw = () => { cancelAnimationFrame(st.raf); st.raf = requestAnimationFrame(() => { if (st.W) { ctx.clearRect(0, 0, st.W, st.H); st.C = colors(); st.layout && st.layout(); st.draw(st); } }); };
    new ResizeObserver(() => {
      const dpr = window.devicePixelRatio || 1, r = canvas.getBoundingClientRect();
      st.W = r.width; st.H = r.height; canvas.width = Math.round(st.W * dpr); canvas.height = Math.round(st.H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); st.redraw();
    }).observe(canvas);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', st.redraw);
    // screen-space primitives
    st.sLine = (p, q, color, w = 1, dash) => { ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = w; if (dash) ctx.setLineDash(dash);
      ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke(); ctx.restore(); };
    st.sArrow = (p, q, color, w = 2.5, head = 10) => {
      const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy); if (L < 1.5) return;
      const h = Math.min(head, L * 0.45), ux = dx / L, uy = dy / L;
      ctx.save(); ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0] - ux * h * 0.8, q[1] - uy * h * 0.8); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(q[0] - ux * h - uy * h * 0.45, q[1] - uy * h + ux * h * 0.45);
      ctx.lineTo(q[0] - ux * h + uy * h * 0.45, q[1] - uy * h - ux * h * 0.45); ctx.closePath(); ctx.fill(); ctx.restore();
    };
    st.sDot = (p, color, r = 4, hollow) => { ctx.save(); ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, 2 * Math.PI);
      if (hollow) { ctx.lineWidth = 2; ctx.strokeStyle = color; ctx.fillStyle = st.C.bg; ctx.fill(); ctx.stroke(); } else { ctx.fillStyle = color; ctx.fill(); } ctx.restore(); };
    st.sText = (p, t, color, dx = 6, dy = -6, size = 13, bold = true, align = 'left') => { ctx.save(); ctx.fillStyle = color;
      ctx.font = `${bold ? '600 ' : ''}${size}px ${FONT}`; ctx.textAlign = align; ctx.fillText(t, p[0] + dx, p[1] + dy); ctx.restore(); };
    st.sPoly = (pts, color, w = 1.5, dash, closed, fill) => { if (pts.length < 2) return; ctx.save(); ctx.beginPath();
      pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); if (closed) ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (color) { ctx.strokeStyle = color; ctx.lineWidth = w; if (dash) ctx.setLineDash(dash); ctx.stroke(); } ctx.restore(); };
    return st;
  }

  // ---------- 2D view (world coordinates, y up, equal scale) ----------
  function View2D(canvas, o, draw) {
    const st = base(canvas, draw);
    st.layout = () => {
      const sx = st.W / (o.xmax - o.xmin), sy = st.H / (o.ymax - o.ymin);
      st.S = Math.min(sx, sy); st.cx = (o.xmin + o.xmax) / 2; st.cy = (o.ymin + o.ymax) / 2;
    };
    st.toS = p => [st.W / 2 + (p[0] - st.cx) * st.S, st.H / 2 - (p[1] - st.cy) * st.S];
    st.toW = (x, y) => [st.cx + (x - st.W / 2) / st.S, st.cy - (y - st.H / 2) / st.S];
    st.bounds = () => { const a = st.toW(0, st.H), b = st.toW(st.W, 0); return { x0: a[0], y0: a[1], x1: b[0], y1: b[1] }; };
    st.line = (a, b, c, w, d) => st.sLine(st.toS(a), st.toS(b), c, w, d);
    st.arrow = (a, v, c, w, h) => st.sArrow(st.toS(a), st.toS([a[0] + v[0], a[1] + v[1]]), c, w, h);
    st.dot = (p, c, r, hollow) => st.sDot(st.toS(p), c, r, hollow);
    st.text = (p, t, c, dx, dy, size, bold, align) => st.sText(st.toS(p), t, c, dx, dy, size, bold, align);
    st.poly = (pts, c, w, d, closed, fill) => st.sPoly(pts.map(st.toS), c, w, d, closed, fill);
    st.circle = (c, r, color, w = 1.5, dash, fill) => { const s = st.toS(c); st.ctx.save(); st.ctx.beginPath(); st.ctx.arc(s[0], s[1], r * st.S, 0, 2 * Math.PI);
      if (fill) { st.ctx.fillStyle = fill; st.ctx.fill(); } st.ctx.strokeStyle = color; st.ctx.lineWidth = w; if (dash) st.ctx.setLineDash(dash); st.ctx.stroke(); st.ctx.restore(); };
    // arc from angle a0 to a1 (radians, math positive), radius r in world units
    st.arc = (c, r, a0, a1, color, w = 1.5, dash) => { const pts = []; const n = Math.max(8, Math.ceil(Math.abs(a1 - a0) * 30));
      for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; pts.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); } st.poly(pts, color, w, dash); return pts; };
    st.grid = (step = 1, axes = true, labels = true) => { const b = st.bounds(), C = st.C;
      for (let x = Math.ceil(b.x0 / step) * step; x <= b.x1; x += step) st.line([x, b.y0], [x, b.y1], C.grid, 1);
      for (let y = Math.ceil(b.y0 / step) * step; y <= b.y1; y += step) st.line([b.x0, y], [b.x1, y], C.grid, 1);
      if (axes) { st.sArrow(st.toS([b.x0, 0]), st.toS([b.x1, 0]), C.muted, 1.2, 8); st.sArrow(st.toS([0, b.y0]), st.toS([0, b.y1]), C.muted, 1.2, 8);
        if (labels) { st.sText([st.W - 14, st.toS([0, 0])[1]], o.xlabel || 'x', C.muted, -4, -6, 13, false, 'right'); st.sText([st.toS([0, 0])[0], 14], o.ylabel || 'y', C.muted, 8, 6, 13, false); } }
    };
    // draggable handles
    const handles = []; let drag = null;
    st.handle = (getPos, setPos) => { handles.push({ getPos, setPos }); };
    const pos = e => { const r = canvas.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
    canvas.addEventListener('pointerdown', e => { const p = pos(e); let best = null, bd = 20;
      handles.forEach(h => { const s = st.toS(h.getPos()); const d = Math.hypot(s[0] - p[0], s[1] - p[1]); if (d < bd) { bd = d; best = h; } });
      if (best) { drag = best; canvas.setPointerCapture(e.pointerId); } });
    canvas.addEventListener('pointermove', e => { const p = pos(e);
      if (!drag) { canvas.style.cursor = handles.some(h => { const s = st.toS(h.getPos()); return Math.hypot(s[0] - p[0], s[1] - p[1]) < 20; }) ? 'grab' : 'default'; return; }
      drag.setPos(st.toW(p[0], p[1])); st.redraw(); });
    const end = () => { drag = null; }; canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end);
    return st;
  }

  // ---------- 3D view (orthographic, z up, drag to rotate) ----------
  function View3D(canvas, o, draw) {
    const st = base(canvas, draw);
    const DEF = { yaw: (o.yaw ?? 20) * Math.PI / 180, pitch: (o.pitch ?? 22) * Math.PI / 180, zoom: 1 };
    const cam = { ...DEF };
    st.cam = cam; st.extent = o.extent || 4; st.center = o.center || [0, 0, 0];
    st.layout = () => {
      const cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
      st.f = [cp * cy, cp * sy, sp]; st.r = [-sy, cy, 0]; st.u = [-sp * cy, -sp * sy, cp];
      st.S = Math.min(st.W, st.H) / (2.3 * st.extent) * cam.zoom;
    };
    st.toS = p => { const q = V.sub(p, st.center); return [st.W / 2 + st.S * V.dot(q, st.r), st.H / 2 - st.S * V.dot(q, st.u)]; };
    st.depth = p => V.dot(p, st.f);
    st.line = (a, b, c, w, d) => st.sLine(st.toS(a), st.toS(b), c, w, d);
    st.arrow = (a, v, c, w, h) => st.sArrow(st.toS(a), st.toS(V.add(a, v)), c, w, h);
    st.dot = (p, c, r, hollow) => st.sDot(st.toS(p), c, r, hollow);
    st.text = (p, t, c, dx, dy, size, bold, align) => st.sText(st.toS(p), t, c, dx, dy, size, bold, align);
    st.poly = (pts, c, w, d, closed, fill) => st.sPoly(pts.map(st.toS), c, w, d, closed, fill);
    // circle with center c, axis n, radius R; optional angle range (relative to basis e1,e2)
    st.circlePts = (c, n, R, a0 = 0, a1 = 2 * Math.PI, N = 72, e1in) => {
      const nn = V.unit(n); let e1 = e1in || (Math.abs(nn[2]) < 0.9 ? V.unit(V.cross([0, 0, 1], nn)) : V.unit(V.cross([1, 0, 0], nn)));
      const e2 = V.cross(nn, e1); const pts = [];
      for (let i = 0; i <= N; i++) { const a = a0 + (a1 - a0) * i / N; pts.push(V.add(c, V.add(V.mul(e1, R * Math.cos(a)), V.mul(e2, R * Math.sin(a))))); }
      return pts;
    };
    st.axes = (L = 3, names = ['x', 'y', 'z']) => { const C = st.C;
      [[L, 0, 0], [0, L, 0], [0, 0, L]].forEach((e, i) => { st.line([0, 0, 0], V.mul(e, 0.92), C.muted, 1.2); st.arrow(V.mul(e, 0.9), V.mul(e, 0.1), C.muted, 1.2, 7);
        st.text(V.mul(e, 1.04), names[i], C.muted, 3, 4, 13, false); });
      st.text([0, 0, 0], 'O', C.muted, -14, 14, 12, false);
    };
    st.floor = (n = 3, z = 0) => { for (let i = -n; i <= n; i++) { st.line([i, -n, z], [i, n, z], st.C.grid, 1); st.line([-n, i, z], [n, i, z], st.C.grid, 1); } };
    st.resetView = () => { Object.assign(cam, DEF); st.redraw(); };
    // rotate / zoom
    const ptrs = new Map(); let pinch0 = 0, zoom0 = 1;
    canvas.style.cursor = 'grab';
    canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, [e.clientX, e.clientY]);
      if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); zoom0 = cam.zoom; } });
    canvas.addEventListener('pointermove', e => { if (!ptrs.has(e.pointerId)) return; const prev = ptrs.get(e.pointerId); ptrs.set(e.pointerId, [e.clientX, e.clientY]);
      if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; cam.zoom = Math.min(3, Math.max(0.4, zoom0 * Math.hypot(a[0] - b[0], a[1] - b[1]) / pinch0)); st.redraw(); return; }
      cam.yaw -= (e.clientX - prev[0]) * 0.008; cam.pitch = Math.min(1.5, Math.max(-1.5, cam.pitch + (e.clientY - prev[1]) * 0.008)); st.redraw(); });
    const up = e => ptrs.delete(e.pointerId); canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    canvas.addEventListener('wheel', e => { e.preventDefault(); cam.zoom = Math.min(3, Math.max(0.4, cam.zoom * Math.exp(-e.deltaY * 0.0015))); st.redraw(); }, { passive: false });
    return st;
  }

  // ---------- safe expression parser: "sqrt(3)/2", "2pi", "cos(t)", "2^-1", "0,5" ----------
  const FN = { sqrt: Math.sqrt, sin: Math.sin, cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos,
    atan: Math.atan, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan, exp: Math.exp, ln: Math.log, abs: Math.abs };
  const CONST = { pi: Math.PI };
  function compile(src, vars = []) {
    const s = String(src).trim().replace(/π/g, 'pi').replace(/√/g, 'sqrt').replace(/[·×]/g, '*').replace(/[−–]/g, '-').replace(/,/g, '.');
    if (!s) throw new Error('leer');
    const toks = []; let i = 0;
    while (i < s.length) {
      const ch = s[i];
      if (/\s/.test(ch)) { i++; continue; }
      if (/[0-9.]/.test(ch)) { let j = i; while (j < s.length && /[0-9.]/.test(s[j])) j++;
        const v = parseFloat(s.slice(i, j)); if (isNaN(v)) throw new Error('Zahl?'); toks.push({ t: 'n', v }); i = j; continue; }
      if (/[a-zA-Z_]/.test(ch)) { let j = i; while (j < s.length && /[a-zA-Z_0-9]/.test(s[j])) j++; toks.push({ t: 'id', v: s.slice(i, j) }); i = j; continue; }
      if ('+-*/^()'.includes(ch)) { toks.push({ t: ch }); i++; continue; }
      throw new Error('Zeichen „' + ch + '“');
    }
    let p = 0; const peek = () => toks[p]; const eat = t => (toks[p] && toks[p].t === t ? (p++, true) : false);
    const expr = () => { let a = term(); for (;;) { if (eat('+')) { const b = term(), x = a; a = e => x(e) + b(e); } else if (eat('-')) { const b = term(), x = a; a = e => x(e) - b(e); } else return a; } };
    const term = () => { let a = unary(); for (;;) {
      if (eat('*')) { const b = unary(), x = a; a = e => x(e) * b(e); }
      else if (eat('/')) { const b = unary(), x = a; a = e => x(e) / b(e); }
      else if (peek() && ['n', 'id', '('].includes(peek().t)) { const b = power(), x = a; a = e => x(e) * b(e); }
      else return a; } };
    const unary = () => { if (eat('-')) { const a = unary(); return e => -a(e); } if (eat('+')) return unary(); return power(); };
    const power = () => { const a = primary(); if (eat('^')) { const b = unary(); return e => Math.pow(a(e), b(e)); } return a; };
    const primary = () => {
      const k = peek(); if (!k) throw new Error('unvollständig');
      if (k.t === 'n') { p++; const v = k.v; return () => v; }
      if (k.t === '(') { p++; const a = expr(); if (!eat(')')) throw new Error('„)“ fehlt'); return a; }
      if (k.t === 'id') { p++; const n = k.v.toLowerCase();
        if (FN[n]) { if (!eat('(')) throw new Error(n + '(…) braucht Klammern'); const a = expr(); if (!eat(')')) throw new Error('„)“ fehlt'); const f = FN[n]; return e => f(a(e)); }
        if (n in CONST) { const v = CONST[n]; return () => v; }
        if (vars.includes(k.v)) { const nm = k.v; return e => e[nm]; }
        throw new Error('unbekannt: ' + k.v); }
      throw new Error('unerwartet: ' + k.t);
    };
    const f = expr(); if (p < toks.length) throw new Error('unerwartet am Ende');
    return f;
  }
  // number from expression (no variables); returns NaN on error and stores message in .error of out object
  function num(src, out) { try { const v = compile(src)({}); if (!isFinite(v)) throw new Error('keine Zahl'); if (out) out.error = ''; return v; }
    catch (e) { if (out) out.error = e.message; return NaN; } }

  window.MW = { V, fmt, fv, css, colors, slider, check, select, button, player, info, View2D, View3D, deg: Math.PI / 180, compile, num };
})();
