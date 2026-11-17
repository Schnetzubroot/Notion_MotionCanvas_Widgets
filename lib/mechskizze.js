/* MechSkizze – Textsprache für Mechanik-Skizzen -> SVG (Sprachreferenz: mechskizze/REFERENZ.md).
   Aus dem MechSkizze-Editor übernommen. Läuft im Browser (window.MechSkizze) und in Node (module.exports). */
(function (root) {
'use strict';
const DEG = Math.PI / 180;

// ---------------------------------------------------------------- Tokenizer
function splitStatements(line) {
  const out = []; let cur = '', q = false, d = 0;
  for (const ch of line) {
    if (ch === '"') q = !q;
    if (!q && ch === '(') d++;
    if (!q && ch === ')') d--;
    if (!q && d === 0 && ch === '#') break;
    if (!q && d === 0 && ch === ';') { out.push(cur); cur = ''; continue; }
    cur += ch;
  }
  out.push(cur);
  return out.map(s => s.trim()).filter(Boolean);
}
function tokenize(s) {
  const t = []; let i = 0;
  while (i < s.length) {
    const c = s[i];
    if (/\s/.test(c)) { i++; continue; }
    if (c === '"') { let j = s.indexOf('"', i + 1); if (j < 0) j = s.length; t.push({ s: s.slice(i + 1, j), q: true }); i = j + 1; continue; }
    let j = i, d = 0;
    while (j < s.length) {
      const ch = s[j];
      if (ch === '(') d++; else if (ch === ')') d--;
      else if (d === 0 && (/\s/.test(ch) || ch === '"')) break;
      j++;
    }
    t.push({ s: s.slice(i, j), q: false }); i = j;
  }
  return t;
}

// ---------------------------------------------------------------- Ausdrücke
const FN = { sqrt: Math.sqrt, sin: x => Math.sin(x * DEG), cos: x => Math.cos(x * DEG), tan: x => Math.tan(x * DEG),
  asin: x => Math.asin(x) / DEG, acos: x => Math.acos(x) / DEG, atan: x => Math.atan(x) / DEG, abs: Math.abs, pi: Math.PI };
function evalExpr(src, params, warn) {
  let s = String(src).trim().replace(/°/g, '').replace(/π/g, 'pi').replace(/·/g, '*').replace(/−/g, '-');
  s = s.replace(/√\s*\(/g, 'sqrt(').replace(/√\s*([\d.]+|[A-Za-zα-ωΑ-Ω_]\w*)/g, 'sqrt($1)');
  s = s.replace(/(\d|\))\s*(?=[A-Za-zα-ωΑ-Ω_(])/g, '$1*');
  s = s.replace(/[A-Za-zα-ωΑ-Ω_][\w']*/g, id => {
    if (id in FN) return 'F.' + id;
    if (!(id in params)) { if (warn) warn('Parameter ' + id + ' nicht gesetzt, nehme 1'); params[id] = 1; }
    return 'P[' + JSON.stringify(id) + ']';
  });
  if (!/^[\d\s.+\-*/()PF\[\]"'.\wα-ωΑ-Ω,]*$/.test(s)) throw new Error('Ungültiger Ausdruck: ' + src);
  // eslint-disable-next-line no-new-func
  const v = Function('P', 'F', 'return (' + s + ');')(params, FN);
  if (typeof v !== 'number' || !isFinite(v)) throw new Error('Ausdruck ergibt keine Zahl: ' + src);
  return v;
}
function splitPair(s) { let d = 0; for (let i = 1; i < s.length; i++) { const c = s[i]; if (c === '(') d++; else if (c === ')') d--; else if (c === '-' && d === 0 && s[i + 1] !== '>') return [s.slice(0, i), s.slice(i + 1)]; } return [s]; }
function splitTop(s, sep) { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '(') d++; if (ch === ')') d--; if (d === 0 && ch === sep) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; }

// ---------------------------------------------------------------- Vektoren
const add = (a, b) => a.map((v, i) => v + b[i]), sub = (a, b) => a.map((v, i) => v - b[i]), mul = (a, k) => a.map(v => v * k);
const dot = (a, b) => a.reduce((s, v, i) => s + v * b[i], 0), len = a => Math.hypot(...a), unit = a => { const l = len(a) || 1; return a.map(v => v / l); };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const rot2 = (v, deg) => { const c = Math.cos(deg * DEG), s = Math.sin(deg * DEG); return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]; };

// ---------------------------------------------------------------- Parser
function parse(text) {
  const M = { params: {}, sys: { welt: { o: [0, 0, 0], a: 0 } }, pts: {}, ptOrder: [], bodies: {}, ops: [], panels: [{ title: '' }],
    is3d: false, proj: axo(20, 15), title: '', warnings: [], labelOpts: {}, scale: null, noLabel: new Set() };
  const warn = m => M.warnings.push(m);
  let panel = 0, farbe = null;   // farbe: 'farbe …' gilt für alle Elemente einer Anweisung
  const lines = text.split(/\r?\n/);
  lines.forEach((raw, li) => {
    for (const st of splitStatements(raw)) {
      try { statement(st); } catch (e) { warn('Zeile ' + (li + 1) + ': ' + e.message); }
    }
  });
  return M;

  function E(s) { return evalExpr(s, M.params, warn); }
  function is3() { return M.is3d && !M.panels[panel].flat; }
  function sysOf(tk) { const i = tk.findIndex((t, j) => !t.q && t.s === 'in' && tk[j + 1] && M.sys[tk[j + 1].s.replace(/:$/, '')]); if (i >= 0) { const n = tk[i + 1].s.replace(/:$/, ''); tk.splice(i, 2); if (!M.sys[n]) throw new Error('System ' + n + ' unbekannt'); return M.sys[n]; } return M.sys.welt; }
  function toWorld(sys, c) { const r = rot2([c[0], c[1]], sys.a); return [sys.o[0] + r[0], sys.o[1] + r[1], sys.o[2] + (c[2] || 0)]; }
  function vecWorld(sys, c) { const r = rot2([c[0], c[1]], sys.a); return [r[0], r[1], c[2] || 0]; }
  function lastGroup(s) { if (!s.endsWith(')')) return null; let d = 0; for (let i = s.length - 1; i >= 0; i--) { if (s[i] === ')') d++; if (s[i] === '(') { d--; if (d === 0) return [s.slice(0, i), s.slice(i + 1, -1)]; } } return null; }
  function P(s, sys) {
    sys = sys || M.sys.welt; s = s.trim();
    const g = lastGroup(s);
    if (g) {
      const [pre, inner] = g;
      if (pre === '') return toWorld(sys, splitTop(inner, ',').map(E));
      if (pre === 'mitte') {
        const args = splitTop(inner, ',').map(x => x.trim());
        if (args.length === 1 && M.bodies[args[0]]) return M.bodies[args[0]].center;
        const ps = args.map(a => P(a, sys)); return mul(ps.reduce(add), 1 / ps.length);
      }
      if (pre === 'teil') { const [a, b, f] = splitTop(inner, ','); const A = P(a, sys), B = P(b, sys); return add(A, mul(sub(B, A), E(f))); }
      const m = pre.match(/^(.*)([+-])$/);
      if (m && m[1]) { const base = P(m[1], sys); const v = vecWorld(sys, splitTop(inner, ',').map(E)); return m[2] === '+' ? add(base, v) : sub(base, v); }
    }
    if (M.pts[s]) return M.pts[s];
    if (M.bodies[s]) return M.bodies[s].center;
    throw new Error('Punkt ' + s + ' unbekannt');
  }
  function dirTok(s, sys, from) {
    s = s.trim();
    const ax = s.match(/^([+-])([xyz])$/);
    if (ax) { const v = [0, 0, 0]; v['xyz'.indexOf(ax[2])] = ax[1] === '-' ? -1 : 1; return is3() ? v : vecWorld(sys, v); }
    if (s.startsWith('(')) return unit(vecWorld(sys, splitTop(s.slice(1, -1), ',').map(E)));
    if (/->/.test(s)) { const [a, b] = s.split('->'); return unit(sub(P(b, sys), P(a, sys))); }
    if (from && (M.pts[s] || /\(/.test(s))) return unit(sub(P(s, sys), from));
    const a = E(s) + sys.a; return [Math.cos(a * DEG), Math.sin(a * DEG), 0];
  }
  // Schlüsselwort-Optionen herausnehmen
  function take(tk, key, n = 1) { const i = tk.findIndex(t => !t.q && t.s === key); if (i < 0) return null; const v = tk.slice(i + 1, i + 1 + n).map(t => t.s); tk.splice(i, 1 + n); return n === 1 ? v[0] : v; }
  function flag(tk, ...keys) { for (const k of keys) { const i = tk.findIndex(t => !t.q && t.s === k); if (i >= 0) { tk.splice(i, 1); return k; } } return null; }
  function str(tk) { const i = tk.findIndex(t => t.q); if (i < 0) return null; const v = tk[i].s; tk.splice(i, 1); return v; }
  function style(tk) {
    const st = {};
    const s = flag(tk, 'gestrichelt', 'punktiert', 'strichpunkt'); if (s) st.dash = s;
    if (flag(tk, 'dick')) st.w = 3.2; if (flag(tk, 'dünn')) st.w = 0.8; if (flag(tk, 'sehrdick')) st.w = 5;
    const w = take(tk, 'breite'); if (w) st.w = +w;
    if (flag(tk, 'grau')) st.fill = '#9a9a9a'; if (flag(tk, 'hellgrau')) st.fill = '#dcdcdc';
    if (flag(tk, 'schraffiert')) st.hatchFill = true;
    return st;
  }
  function op(o) { o.panel = panel; if (farbe) o.farbe = farbe; M.ops.push(o); return o; }
  function supDir(tk, sys) {
    if (flag(tk, 'an')) {
      const w = tk.shift(); const side = tk[0] && ['links', 'rechts', 'oben', 'unten'].includes(tk[0].s) ? tk.shift().s : null;
      if (w.s === 'decke') return -90; if (w.s === 'boden') return 90;
      if (w.s === 'wand') return side === 'rechts' ? 180 : 0;
    }
    if (flag(tk, 'hängend')) return -90;
    const r = take(tk, 'richtung'); if (r) { const v = dirTok(r, sys); return Math.atan2(v[1], v[0]) / DEG; }
    return 90;
  }

  function statement(st) {
    const tk = tokenize(st); if (!tk.length) return;
    const kw = tk.shift().s.toLowerCase().replace(/:$/, '');
    const sys = sysOf(tk);
    farbe = kw === 'stil' ? null : farbeVon(take(tk, 'farbe'));
    switch (kw) {
      case 'titel': M.title = str(tk) || ''; break;
      case 'stil': {
        const v = tk.length ? tk.shift().s.toLowerCase() : '';
        if (v === 'hand' || v === 'handskizze') { M.stil = 'hand'; M.einfarbig = !!flag(tk, 'einfarbig', 'schwarz'); }
        else if (v === 'sauber' || v === 'normal') M.stil = 'sauber';
        else throw new Error('stil erwartet hand oder sauber');
        break;
      }
      case '3d': M.is3d = true; {
        if (flag(tk, 'schräg', 'kavalier')) { const a = E(take(tk, 'winkel') || '34'), k = E(take(tk, 'faktor') || '0.6'); M.proj = oblique(a, k); }
        else { flag(tk, 'achsen');
          const ach = tk.filter(t => !t.q && t.s.startsWith('('));
          if (ach.length === 3) { const v = ach.map(t => splitTop(t.s.slice(1, -1), ',').map(E)); const ex = [v[0][0], v[1][0], v[2][0]], ey = [v[0][1], v[1][1], v[2][1]]; M.proj = { ex, ey, v: unit(cross(ex, ey)) }; }
          else { const az = take(tk, 'azimut'), el = take(tk, 'elevation'); if (az || el) M.proj = axo(E(az || '20'), E(el || '15')); }
        }
      } break;
      case 'massstab': M.scale = E(tk[0].s); break;
      case 'param': case 'parameter':
        for (const t of tk) { const [k, v] = t.s.split('='); M.params[k.trim()] = E(v); } break;
      case 'system': {
        const name = tk.shift().s; if (tk[0] && tk[0].s === '=') tk.shift();
        const s = { o: [0, 0, 0], a: 0 };
        const g = take(tk, 'gedreht'); if (g) s.a = E(g);
        const u = take(tk, 'ursprung') || take(tk, 'um') || take(tk, 'verschoben'); if (u) s.o = P(u, sys);
        M.sys[name] = s; break;
      }
      case 'punkt': case 'punkte': case 'knoten': {
        const sichtbar = kw === 'knoten' || flag(tk, 'markiert');
        for (const t of tk) {
          const g = lastGroup(t.s); if (!g) throw new Error('Punkt erwartet Name(x,y): ' + t.s);
          let [name, inner] = g; let p;
          const m = name.match(/^([^=]+)=(.*)$/);
          if (m) { name = m[1]; p = P(m[2] + '(' + inner + ')', sys); }
          else p = toWorld(sys, splitTop(inner, ',').map(E));
          if (name.startsWith('_')) M.noLabel.add(name);
          const ex = M.ptOrder.find(e => e.n === name && e.panel === panel);
          if (ex) ex.p = p; else M.ptOrder.push({ n: name, p, panel });
          M.pts[name] = p;
          if (sichtbar) op({ k: 'dot', p });
        }
        break;
      }
      case 'körper': case 'koerper': case 'fläche': case 'flaeche': case 'linie': case 'polygon': {
        let name = null;
        if (kw === 'körper' || kw === 'koerper') { name = tk.shift().s; if (tk[0] && tk[0].s === '=') tk.shift(); }
        const desc = str(tk); const stl = style(tk);
        let typ = 'polygon'; if (tk[0] && ['polygon', 'kreis', 'linie'].includes(tk[0].s)) typ = tk.shift().s;
        if (typ === 'kreis') {
          const c = P(tk.shift().s, sys); const r = E(take(tk, 'radius') || tk.shift().s);
          const nrm = take(tk, 'normale'); const n = nrm ? dirTok(nrm, sys) : [0, 0, 1];
          op({ k: 'circle3', c, r, n, st: Object.assign({ w: 2.2 }, stl) });
          if (name) M.bodies[name] = { center: c, desc };
          break;
        }
        const pts = tk.map(t => P(t.s, sys));
        const closed = kw === 'linie' || typ === 'linie' ? false : true;
        const w = kw === 'körper' || kw === 'koerper' ? 2.2 : (kw === 'fläche' || kw === 'flaeche' ? 1.2 : 1.1);
        op({ k: 'poly', pts, closed, st: Object.assign({ w }, stl), body: !!name });
        if (name) M.bodies[name] = { center: centroid(pts), pts, desc };
        break;
      }
      case 'stab': case 'balken': case 'stäbe': case 'staebe': case 'fachwerk': {
        const stl = style(tk); const num = flag(tk, 'nummeriert'); const dots = kw === 'fachwerk' || flag(tk, 'knoten');
        let pairs = tk.filter(t => !t.q).map(t => splitPair(t.s));
        if (pairs.every(p => p.length === 1)) pairs = pairs.slice(1).map((p, i) => [pairs[i][0], p[0]]);
        const w = kw === 'balken' ? 4.5 : 2.2; let i = 0; const seen = new Set();
        for (const [a, b] of pairs) {
          const A = P(a, sys), B = P(b, sys); i++;
          op({ k: 'poly', pts: [A, B], closed: false, st: Object.assign({ w }, stl), body: true });
          if (num) op({ k: 'text', p: mul(add(A, B), 0.5), s: String(i), small: true, side: true, seg: [A, B] });
          if (dots) for (const [n, X] of [[a, A], [b, B]]) if (!seen.has(n)) { seen.add(n); op({ k: 'dot', p: X }); }
        }
        break;
      }
      case 'gelenk': for (const t of tk) op({ k: 'hinge', p: P(t.s, sys) }); break;
      case 'punktmarke': case 'marke': for (const t of tk) op({ k: 'dot', p: P(t.s, sys) }); break;
      case 'festlager': case 'loslager': case 'einspannung': case 'gelenklager': case 'schiebehülse': case 'kugelgelenk': {
        const p = P(tk.shift().s, sys); const ang = supDir(tk, sys); const stl = style(tk);
        op({ k: 'support', typ: kw, p, ang, st: stl }); break;
      }
      case 'boden': case 'wand': case 'decke': case 'ebene': {
        const stl = style(tk); const side = take(tk, 'schraffur') || take(tk, 'seite');
        const mittig = flag(tk, 'mittig');
        let A, B;
        const r = take(tk, 'richtung'), L = take(tk, 'länge') || take(tk, 'laenge');
        A = P(tk.shift().s, sys);
        if (r || L) {
          const d = r ? dirTok(r, sys) : (kw === 'wand' ? [0, 1, 0] : [1, 0, 0]);
          const l = E(L || '1'); B = add(A, mul(d, l)); if (mittig) { A = sub(A, mul(d, l / 2)); B = sub(B, mul(d, l / 2)); }
        } else { const t = tk.shift(); if (t && t.s === '->') B = P(tk.shift().s, sys); else B = P(t.s, sys); }
        const def = { boden: 'unten', ebene: 'unten', decke: 'oben', wand: 'links' }[kw];
        op({ k: 'ground', a: A, b: B, side: side || def, st: stl }); break;
      }
      case 'seil': case 'feder': case 'dämpfer': {
        const A = P(tk.shift().s, sys); let B;
        const r = take(tk, 'richtung'), L = take(tk, 'länge') || take(tk, 'laenge');
        if (r) B = add(A, mul(dirTok(r, sys), E(L || '1'))); else B = P(tk.shift().s, sys);
        const stl = style(tk); op({ k: kw === 'seil' ? 'rope' : 'spring', a: A, b: B, st: stl }); break;
      }
      case 'rolle': { const c = P(tk.shift().s, sys); const r = E(take(tk, 'radius') || tk.shift().s); op({ k: 'circle3', c, r, n: [0, 0, 1], st: { w: 2 } }); op({ k: 'hinge', p: c }); break; }
      case 'kraft': case 'vektor': case 'pfeil': case 'geschwindigkeit': {
        const name = kw === 'pfeil' ? null : (tk[0] && !tk[0].q ? tk.shift().s : null);
        const lbl = str(tk) || (name && name !== '-' ? name : '');
        const thick = flag(tk, 'dick'); const zu = flag(tk, 'zu', 'auf', 'endet'); const st = style(tk);
        const L = take(tk, 'länge') || take(tk, 'laenge'); const lage = take(tk, 'lage');
        const von = kw === 'pfeil' ? take(tk, 'von') : null;
        if (von) {
          const A = P(von, sys); const B = P(take(tk, 'nach'), sys);
          op({ k: 'arrow', a: A, b: B, label: lbl, thick, st, lage, dbl: flag(tk, 'doppelt') }); break;
        }
        const bei = take(tk, 'bei') || tk.shift().s; const p = P(bei, sys);
        const r = take(tk, 'richtung'); const d = dirTok(r || '-y', sys, p);
        op({ k: 'force', p, d, label: lbl, thick, zu, len: L ? E(L) : null, st, lage, kind: kw }); break;
      }
      case 'moment': case 'drehung': {
        const name = tk[0] && !tk[0].q && tk[1] && tk[1].s === 'bei' ? tk.shift().s : null;
        const lbl = str(tk) || name || ''; const cw = flag(tk, 'uhrzeiger', 'cw'); flag(tk, 'gegen', 'ccw');
        const bei = take(tk, 'bei') || tk.shift().s; const p = P(bei, sys);
        const ax = take(tk, 'achse'); const lage = take(tk, 'lage'); const L = take(tk, 'länge');
        if (ax) op({ k: 'force', p, d: dirTok(ax, sys, p), label: lbl, dbl: true, len: L ? E(L) : null, lage, st: {} });
        else op({ k: 'moment', p, cw: !!cw, label: lbl, lage }); break;
      }
      case 'last': case 'streckenlast': {
        const lbl = str(tk); const seite = take(tk, 'seite') || 'links'; const h = take(tk, 'höhe');
        const qq = take(tk, 'q'); let qs = [1, 1]; if (qq) { qs = splitTop(qq.replace(/^\(|\)$/g, ''), ',').map(E); if (qs.length === 1) qs.push(qs[0]); }
        const rr = take(tk, 'richtung'); const pf = flag(tk, 'ohnepfeile'); const outw = flag(tk, 'nachaussen', 'zug');
        const A = P(take(tk, 'von') || tk.shift().s, sys); const B = P(take(tk, 'nach') || take(tk, 'bis') || tk.shift().s, sys);
        const st = style(tk); op({ k: 'load', a: A, b: B, qs, side: seite, label: lbl, h: h ? E(h) : null, st, dir: rr ? dirTok(rr, sys) : null, noarrows: !!pf, out: !!outw }); break;
      }
      case 'mass': case 'maß': case 'bemassung': {
        const off = take(tk, 'versatz'); const stil = flag(tk, 'strich', 'striche') ? 'tick' : 'arrow'; const lbl = str(tk) || '';
        const [a, b] = splitPair(tk.shift().s); const seite = take(tk, 'seite');
        op({ k: 'dim', a: P(a, sys), b: P(b, sys), label: lbl, off: off ? E(off) : null, stil, seite }); break;
      }
      case 'kante': {
        while (tk.length) {
          const t = tk.shift(); if (t.q) continue; const [a, b] = splitPair(t.s); const lbl = tk[0] && tk[0].q ? tk.shift().s : '';
          const seite = tk[0] && ['innen', 'aussen', 'links', 'rechts', 'oben', 'unten', 'l', 'r', 'o', 'u'].includes(tk[0].s) ? tk.shift().s : 'aussen';
          op({ k: 'edge', a: P(a, sys), b: P(b, sys), label: lbl, seite });
        }
        break;
      }
      case 'winkel': {
        const lbl = str(tk) || ''; const r = take(tk, 'radius'); const bogen2 = flag(tk, 'doppelt');
        const s1 = take(tk, 'zwischen'), s2 = take(tk, 'und'); const v = P(tk.shift().s, sys);
        const VERT = is3() ? [0, 0, 1] : [0, -1, 0];
        const d1 = s1 === 'horizontal' ? [1, 0, 0] : s1 === 'vertikal' ? VERT : dirTok(s1, sys, v);
        const d2 = s2 === 'horizontal' ? [1, 0, 0] : s2 === 'vertikal' ? VERT : dirTok(s2, sys, v);
        op({ k: 'angle', v, d1, d2, label: lbl, r: r ? +r : null, dbl: bogen2 }); break;
      }
      case 'querlager': { const p = P(tk.shift().s, sys); const r = take(tk, 'richtung'); op({ k: 'qlager', p, d: r ? dirTok(r, sys) : [1, 0, 0], lang: !!flag(tk, 'lang') }); break; }
      case 'diagramm': {
        const name = str(tk) || ''; const B0 = P(take(tk, 'basis'), sys); const L = E(take(tk, 'länge') || '1'); const k = E(take(tk, 'skala') || '1');
        flag(tk, 'punkte'); const pts = tk.filter(t => !t.q && t.s.startsWith('(')).map(t => splitTop(t.s.slice(1, -1), ',').map(E));
        const g = pts.map(([x, v]) => [B0[0] + x, B0[1] - v * k, 0]);
        const poly = [[B0[0] + pts[0][0], B0[1], 0], ...g, [B0[0] + pts[pts.length - 1][0], B0[1], 0]];
        op({ k: 'poly', pts: poly, closed: true, st: { w: 0.01, hatchFill: true, stroke: 'none' } });
        op({ k: 'poly', pts: g, closed: false, st: { w: 2 } });
        op({ k: 'arrow', a: B0, b: [B0[0] + L + 0.35, B0[1], 0], label: 'x', st: { w: 0.9 } });
        const vmax = Math.max(0, ...pts.map(p => p[1])) * k;
        op({ k: 'arrow', a: [B0[0], B0[1] - Math.min(0, ...pts.map(p => p[1])) * k + 0.15, 0], b: [B0[0], B0[1] - vmax - 0.35, 0], label: name, st: { w: 0.9 }, lage: 'l' });
        break;
      }
      case 'bruch': { const p = P(tk.shift().s, sys); const r = take(tk, 'richtung'); op({ k: 'brk', p, d: r ? dirTok(r, sys) : [1, 0, 0] }); break; }
      case 'text': { const lbl = str(tk); const grau = flag(tk, 'grau'); const kasten = flag(tk, 'kasten'); const p = P(tk.shift().s, sys); const lage = take(tk, 'lage'); op({ k: 'text', p, s: lbl, lage, upright: !!flag(tk, 'normal'), color: grau ? '#888' : null, box: !!kasten }); break; }
      case 'beschrifte': case 'name': {
        const n = tk.shift().s; const lbl = str(tk); const lage = take(tk, 'lage') || (tk[0] ? tk.shift().s : null);
        M.labelOpts[n] = { s: lbl, lage }; break;
      }
      case 'ohne': case 'versteckt': if (tk[0] && tk[0].s === 'namen') { tk.shift(); tk.forEach(t => M.noLabel.add(t.s)); if (!tk.length) M.noLabels = true; } break;
      case 'schwerpunkt': for (const t of tk) op({ k: 'cog', p: P(t.s, sys) }); break;
      case 'achse': {
        const lbl = str(tk); const p = P(tk.shift().s, sys); const d = dirTok(take(tk, 'richtung') || tk.shift().s, sys, p);
        const L = E(take(tk, 'länge') || '1'); op({ k: 'poly', pts: [sub(p, mul(d, L / 2)), add(p, mul(d, L / 2))], closed: false, st: { w: 0.9, dash: 'strichpunkt' } });
        if (lbl) op({ k: 'text', p: add(p, mul(d, L / 2)), s: lbl, lage: 'r' }); break;
      }
      case 'koordinaten': case 'basis': {
        const p = P(tk.shift().s, sys); const L = take(tk, 'länge'); const names = take(tk, 'namen', is3() ? 3 : 2);
        const basis = kw === 'basis' || flag(tk, 'basis');
        const def = basis ? ['~e_x', '~e_y', '~e_z'] : ['x', 'y', 'z'];
        const axes = is3() ? [[1, 0, 0], [0, 1, 0], [0, 0, 1]] : [vecWorld(sys, [1, 0]), vecWorld(sys, [0, 1])];
        axes.forEach((a, i) => op({ k: 'force', p, d: a, label: (names && names[i]) || def[i], len: L ? E(L) : null, pxlen: L ? null : 38, st: { w: 1.1 }, thin: true }));
        break;
      }
      case 'quader': {
        const A = P(take(tk, 'von'), sys); const B = P(take(tk, 'bis'), sys);
        op({ k: 'box', a: A, b: B, st: style(tk) }); break;
      }
      case 'kegel': {
        const S = P(take(tk, 'spitze'), sys); const C = P(take(tk, 'basis'), sys); const r = E(take(tk, 'radius'));
        op({ k: 'cone', s: S, c: C, r, st: style(tk) }); break;
      }
      case 'zylinder': {
        const C = P(take(tk, 'basis'), sys); const ax = dirTok(take(tk, 'achse') || '+z', sys); const r = E(take(tk, 'radius')); const h = E(take(tk, 'höhe') || take(tk, 'laenge') || take(tk, 'länge'));
        op({ k: 'cyl', c: C, ax, r, h, st: style(tk) }); break;
      }
      case 'kugel': { const c = P(tk.shift().s, sys); const r = E(take(tk, 'radius') || tk.shift().s); op({ k: 'sphere', c, r, st: style(tk) }); break; }
      case 'bogen': {
        const c = P(tk.shift().s, sys); const r = E(take(tk, 'radius')); const a1 = E(take(tk, 'von')), a2 = E(take(tk, 'bis'));
        const st = style(tk); const pts = []; for (let i = 0; i <= 48; i++) { const a = (a1 + (a2 - a1) * i / 48 + sys.a) * DEG; pts.push(add(c, [r * Math.cos(a), r * Math.sin(a), 0])); }
        op({ k: 'poly', pts, closed: false, st: Object.assign({ w: 1.1 }, st) }); break;
      }
      case 'kurve': {
        const st = style(tk); const rp = flag(tk, 'richtungspfeile'); const closedK = flag(tk, 'geschlossen'); let pts = [];
        if (tk[1] && tk[1].s === 'von') {
          const v = tk.shift().s; const a = E(take(tk, 'von')); const b = E(take(tk, 'bis').replace(/:$/, ''));
          if (tk[0] && tk[0].s === ':') tk.shift();
          const g = tk.shift().s.replace(/^:/, ''); const inner = g.trim().replace(/^\(|\)$/g, '');
          const old = M.params[v]; const N = 96;
          for (let i = 0; i <= N; i++) { M.params[v] = a + (b - a) * i / N; pts.push(toWorld(sys, splitTop(inner, ',').map(E))); }
          if (old === undefined) delete M.params[v]; else M.params[v] = old;
        } else {
          const C = tk.filter(t => !t.q).map(t => P(t.s, sys));
          if (C.length < 2) throw new Error('kurve braucht mindestens 2 Punkte');
          const n = C.length, cl = !!closedK, g = i => cl ? C[(i + n) % n] : C[Math.max(0, Math.min(n - 1, i))];
          for (let i = 0; i < (cl ? n : n - 1); i++) {
            const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
            for (let k = 0; k < 16; k++) { const t = k / 16, t2 = t * t, t3 = t2 * t;
              pts.push([0, 1, 2].map(j => 0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3))); }
          }
          pts.push(cl ? C[0] : C[C.length - 1]);
        }
        if (st.fill && !flag(tk, 'gefüllt')) { st.stroke = st.fill; delete st.fill; }
        op({ k: 'poly', pts, closed: false, st: Object.assign({ w: 1.5 }, st), marks: rp ? [0.3, 0.7] : null }); break;
      }
      case 'rechtwinklig': case 'rechterwinkel': {
        const s1 = take(tk, 'zwischen'), s2 = take(tk, 'und'); const v = P(tk.shift().s, sys);
        op({ k: 'rangle', v, d1: dirTok(s1, sys, v), d2: dirTok(s2, sys, v) }); break;
      }
      case 'drehpfeil': {
        const lbl = str(tk); const p = P(tk.shift().s, sys); const ax = take(tk, 'achse'); const r = take(tk, 'radius'); const cw = flag(tk, 'uhrzeiger');
        op({ k: 'spin', p, n: ax ? dirTok(ax, sys, p) : [0, 0, 1], r: r ? E(r) : null, cw: !!cw, label: lbl, lage: take(tk, 'lage') }); break;
      }
      case 'untereinander': M.vertical = true; break;
      case 'nebeneinander': M.vertical = false; break;
      case 'teilbild': panel = M.panels.length; M.panels.push({ title: str(tk) || '', flat: !!flag(tk, '2d', 'eben') }); break;
      case 'aus': case 'ein': { const p = P(tk.shift().s, sys); op({ k: 'outof', p, into: kw === 'ein', label: str(tk) || '', lage: take(tk, 'lage') }); break; }
      default: throw new Error('Unbekannter Befehl: ' + kw);
    }
  }
}
function axo(az, el) { // orthogonale Axonometrie, z bleibt senkrecht
  const a = az * DEG, e = el * DEG;
  return { ex: [-Math.sin(a), Math.cos(a), 0], ey: [-Math.cos(a) * Math.sin(e), -Math.sin(a) * Math.sin(e), Math.cos(e)], v: [Math.cos(a) * Math.cos(e), Math.sin(a) * Math.cos(e), Math.sin(e)] };
}
function oblique(a, k) { const kx = -k * Math.cos(a * DEG), ky = -k * Math.sin(a * DEG); return { ex: [kx, 1, 0], ey: [ky, 0, 1], v: unit([1, -kx, -ky]) }; }
function centroid(pts) {
  if (pts.length < 3) return mul(pts.reduce(add), 1 / pts.length);
  let A = 0, cx = 0, cy = 0; const z = pts.reduce((s, p) => s + p[2], 0) / pts.length;
  for (let i = 0; i < pts.length; i++) { const [x0, y0] = pts[i], [x1, y1] = pts[(i + 1) % pts.length]; const c = x0 * y1 - x1 * y0; A += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c; }
  if (Math.abs(A) < 1e-12) return mul(pts.reduce(add), 1 / pts.length);
  return [cx / (3 * A), cy / (3 * A), z];
}

// Formeltext zerlegen: ~ Vektor, _ Index, ^ Exponent, √ Wurzel, {…} Gruppe
function parseRich(cs, i0 = 0, stop = null) {
  const out = []; let i = i0;
  const group = () => { // Gruppe {…} oder ein Zeichen
    if (cs[i] === '{') { const r = parseRich(cs, i + 1, '}'); i = r.i + 1; return r.nodes; }
    if (cs[i] === '~') { i++; const b = group(); return [{ t: 'vec', b }]; }
    if (i < cs.length) return [{ t: 'c', c: cs[i++] }];
    return [];
  };
  while (i < cs.length && cs[i] !== stop) {
    const ch = cs[i];
    if (ch === '~') { i++; out.push({ t: 'vec', b: group() }); continue; }
    if (ch === '_' || ch === '^') { i++; out.push({ t: ch === '_' ? 'sub' : 'sup', b: group() }); continue; }
    if (ch === '√') {
      i++;
      if (cs[i] === '(') { let d = 1, j = i + 1; while (j < cs.length && d) { if (cs[j] === '(') d++; if (cs[j] === ')') d--; j++; } const r = parseRich(cs.slice(i + 1, j - 1)); out.push({ t: 'sqrt', b: r.nodes }); i = j; continue; }
      if (cs[i] === '{') { out.push({ t: 'sqrt', b: group() }); continue; }
      let j = i; while (j < cs.length && /[\d.]/.test(cs[j])) j++;
      if (j === i && j < cs.length && /[A-Za-zα-ωΑ-Ω]/.test(cs[j])) j++;
      out.push({ t: 'sqrt', b: cs.slice(i, j).map(c => ({ t: 'c', c })) }); i = j; continue;
    }
    if (ch === '{' ) { const r = parseRich(cs, i + 1, '}'); out.push(...r.nodes); i = r.i + 1; continue; }
    out.push({ t: 'c', c: ch }); i++;
  }
  return { nodes: out, i };
}
// Textbreite messen (Browser: Canvas mit derselben Schrift; sonst Schätzung)
const FONTS = "'Latin Modern Roman','CMU Serif','Times New Roman',serif";
const HANDFONTS = "'Zen Kurenaido','Comic Sans MS','Segoe Print',cursive";
let MCTX; const WCACHE = new Map();
function textW(s, px, it, hand) {
  const key = (hand ? 'h' : it ? 'i' : 'n') + px + '|' + s; if (WCACHE.has(key)) return WCACHE.get(key);
  if (MCTX === undefined) { try { MCTX = typeof document !== 'undefined' ? document.createElement('canvas').getContext('2d') : null; } catch (e) { MCTX = null; } }
  let w, keep = true;
  if (MCTX) { MCTX.font = (it && !hand ? 'italic ' : '') + px + 'px ' + (hand ? HANDFONTS : FONTS); w = MCTX.measureText(s).width;
    // Handschrift noch nicht geladen: Breite nicht merken, sonst bleiben die Ersatzschrift-Masse hängen
    if (hand) try { keep = !document.fonts || document.fonts.check(px + "px 'Zen Kurenaido'", s); } catch (e) {} }
  else { w = 0; for (const c of s) w += px * (/[iljtfrI1.,:;!|'′ ]/.test(c) ? 0.3 : /[mwMW]/.test(c) ? 0.85 : /[A-ZΑ-Ω]/.test(c) ? 0.66 : /[(){}\[\]]/.test(c) ? 0.34 : 0.5) * (hand ? 0.92 : 1); }
  if (keep) WCACHE.set(key, w); return w;
}

// ---------------------------------------------------------------- Handskizze (stil hand): Gel-Marker-Look
// Farben je Bedeutung; Linien leicht gewellt und ungleich dick. Der Zufall hängt nur vom Element ab (gleiche Skizze = gleiches Bild).
const PAL = { geo: '#1f2d4d', lager: '#46546b', kraft: '#e03131', moment: '#ae3ec9', kin: '#1971c2', hilf: '#2b8a3e', text: '#1f2d4d' };
const FARBEN = { rot: '#e03131', blau: '#1971c2', grün: '#2b8a3e', gruen: '#2b8a3e', violett: '#ae3ec9', lila: '#ae3ec9', orange: '#f08c00',
  schwarz: '#1f2d4d', braun: '#8f5a2a', türkis: '#0c8599', tuerkis: '#0c8599', pink: '#d6336c', grau: '#868e96' };
function farbeVon(s) { if (!s) return null; const c = FARBEN[s.toLowerCase()]; if (c) return c; if (/^#[0-9a-f]{3}([0-9a-f]{3})?$/i.test(s)) return s; throw new Error('Unbekannte Farbe: ' + s + ' (' + Object.keys(FARBEN).join(', ') + ' oder #rrggbb)'); }
function hashStr(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
// Mittellinie fein abtasten und quer zur Linie wellen. Liefert Punkte mit Bogenlänge s und Normale n.
function handLine(pts, closed, R, amp) {
  const P = closed ? pts.concat([pts[0]]) : pts; const S = []; let tot = 0;
  for (let i = 0; i < P.length - 1; i++) {
    const a = P[i], b = P[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); const m = Math.max(1, Math.ceil(l / 8));
    const bow = (R() - 0.5) * 2 * Math.min(1.8, 0.009 * l) * (amp > 0 ? 1 : 0);   // leichter Bauch auf langen Strecken
    for (let k = 0; k < m; k++) S.push({ p: [a[0] + (b[0] - a[0]) * k / m, a[1] + (b[1] - a[1]) * k / m], s: tot + l * k / m, bow: bow * Math.sin(Math.PI * k / m) });
    tot += l;
  }
  if (!closed) S.push({ p: P[P.length - 1].slice(), s: tot, bow: 0 });
  const N = S.length; if (N < 2) return { S, tot };
  for (let i = 0; i < N; i++) {   // Normale (Gehrung an Ecken, begrenzt)
    const prev = S[closed ? (i - 1 + N) % N : Math.max(0, i - 1)].p, next = S[closed ? (i + 1) % N : Math.min(N - 1, i + 1)].p, c = S[i].p;
    const t1 = [c[0] - prev[0], c[1] - prev[1]], t2 = [next[0] - c[0], next[1] - c[1]]; const l1 = Math.hypot(...t1), l2 = Math.hypot(...t2);
    const u1 = l1 ? [t1[0] / l1, t1[1] / l1] : null, u2 = l2 ? [t2[0] / l2, t2[1] / l2] : null; const ua = u1 || u2, ub = u2 || u1;
    let n = [-(ua[1] + ub[1]), ua[0] + ub[0]]; const ln = Math.hypot(...n);
    if (ln < 1e-6) n = [-ua[1], ua[0]]; else n = [n[0] / ln, n[1] / ln];
    const cs = Math.abs(n[0] * -ua[1] + n[1] * ua[0]); S[i].n = n; S[i].mit = 1 / Math.max(0.5, cs);
  }
  // Welle: bei geschlossenen Linien periodisch, damit Anfang und Ende zusammenpassen
  const k1 = closed ? 2 * Math.PI * Math.max(1, Math.round(tot / 260)) / tot : 1 / 40, k2 = closed ? 2 * Math.PI * Math.max(2, Math.round(tot / 90)) / tot : 1 / 15;
  const f1 = R() * 6.283, f2 = R() * 6.283, e0 = (R() - 0.5) * amp, e1 = (R() - 0.5) * amp;
  for (const q of S) { const t = tot ? q.s / tot : 0;
    const off = amp * (0.75 * Math.sin(q.s * k1 + f1) + 0.25 * Math.sin(q.s * k2 + f2)) + q.bow + (closed ? 0 : e0 * (1 - t) + e1 * t);
    q.p = [q.p[0] + q.n[0] * off, q.p[1] + q.n[1] * off]; }
  return { S, tot };
}
// Strich als gefüllte Kontur mit wechselnder Dicke (Gel-Marker); offene Enden rund
function handStroke(H, closed, w, R, f) {
  const { S, tot } = H; const N = S.length; if (N < 2) return '';
  const g1 = R() * 6.283, g2 = R() * 6.283;
  const hw = q => { let k = 1 + 0.17 * Math.sin(q.s / 17 + g1) + 0.08 * Math.sin(q.s / 5.3 + g2);
    if (!closed) { const d = Math.min(q.s, tot - q.s); if (d < 7) k *= 0.78 + 0.22 * d / 7; } return w / 2 * k; };
  const L = [], Rt = [];
  for (const q of S) { const h = hw(q) * Math.min(q.mit, 2.2); L.push([q.p[0] + q.n[0] * h, q.p[1] + q.n[1] * h]); Rt.push([q.p[0] - q.n[0] * h, q.p[1] - q.n[1] * h]); }
  const P = a => a.map(p => f(p[0]) + ' ' + f(p[1])).join('L');
  if (closed) return 'M' + P(L) + 'ZM' + P(Rt.reverse()) + 'Z';
  const cap = (q, dir, from) => { const h = hw(q), t = dir; const c = []; for (let i = 1; i < 6; i++) { const a = Math.PI * i / 6;
    const v = [from * (q.n[0] * Math.cos(a)) + t[0] * Math.sin(a), from * (q.n[1] * Math.cos(a)) + t[1] * Math.sin(a)]; c.push([q.p[0] + v[0] * h, q.p[1] + v[1] * h]); } return c; };
  // Tangente aus der Normalen: n = (-t_y, t_x) -> t = (n_y, -n_x)
  const te = [S[N - 1].n[1], -S[N - 1].n[0]], tb = [-S[0].n[1], S[0].n[0]];
  return 'M' + P(L) + 'L' + P(cap(S[N - 1], te, 1)) + 'L' + P(Rt.slice().reverse()) + 'L' + P(cap(S[0], tb, -1)) + 'Z';
}

// ---------------------------------------------------------------- Renderer
function render(src, opts = {}) {
  const M = typeof src === 'string' ? parse(src) : src;
  let curPn = 0; const flat3 = () => !M.is3d || (M.panels[curPn] && M.panels[curPn].flat);
  const pj = p => !flat3() ? [dot(p, M.proj.ex), dot(p, M.proj.ey)] : [p[0], p[1]];
  const view = M.proj.v;
  const stil = opts.stil || M.stil || 'sauber', hand = stil === 'hand';
  const mono = hand && (opts.farben === false || !!M.einfarbig);
  const FS = opts.fontSize || (hand ? 22 : 19);

  // Geometrie je Teilbild sammeln für Massstab
  const geo = M.panels.map(() => []);
  const addG = (pn, p) => { curPn = pn; geo[pn].push(pj(p)); };
  for (const o of M.ops) for (const k of ['p', 'a', 'b', 'c', 'v', 's']) if (o[k] && Array.isArray(o[k]) && typeof o[k][0] === 'number') addG(o.panel, o[k]);
  for (const o of M.ops) if (o.pts) o.pts.forEach(p => addG(o.panel, p));
  for (const o of M.ops) if (o.k === 'circle3' || o.k === 'sphere') { addG(o.panel, add(o.c, [o.r, o.r, 0])); addG(o.panel, sub(o.c, [o.r, o.r, 0])); }
  for (const e of M.ptOrder) addG(e.panel, e.p);
  let ext = 0, aw = 0, ah = 0;
  geo.forEach(g => { if (!g.length) return; const xs = g.map(p => p[0]), ys = g.map(p => p[1]); const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys); ext = Math.max(ext, w, h); aw = Math.max(aw, w); ah = Math.max(ah, h); });
  const asp = Math.max(1, Math.min(1.8, Math.sqrt((aw || 1) / (ah || aw || 1))));
  const S = (M.scale || 1) * (opts.size || 300) * asp / (ext || 1);

  const panelsOut = M.panels.map((pn, pi) => renderPanel(pi));
  // Teilbilder nebeneinander
  const gap = 40; const pv = panelsOut.filter(Boolean);
  const vert = M.vertical === true || (M.vertical !== false && pv.reduce((s, P) => s + P.w, 0) > 1000);
  let W = 0, H = 0, body = '';
  if (vert) { let y = 0; W = Math.max(...pv.map(P => P.w)); for (const P of pv) { body += `<g transform="translate(${f((W - P.w) / 2 - P.minx)},${f(y - P.miny)})">${P.svg}</g>\n`; y += P.h + gap; } H = Math.max(0, y - gap); }
  else { let x = 0; H = Math.max(...pv.map(P => P.h)); for (const P of pv) { body += `<g transform="translate(${f(x - P.minx)},${f(-P.miny + (H - P.h) / 2)})">${P.svg}</g>\n`; x += P.w + gap; } W = Math.max(0, x - gap); }
  const titleH = 0;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${f(W)} ${f(H + titleH)}" width="${f(W)}" height="${f(H + titleH)}" font-family="${hand ? HANDFONTS : FONTS}" font-size="${FS}">\n<defs>${hand ? '<pattern id="schh" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><line x1="0" y1="0" x2="0" y2="7" stroke="#5c6b85" stroke-width="1.1" stroke-linecap="round"/></pattern>' : '<pattern id="sch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#000" stroke-width="0.7"/></pattern>'}</defs>\n${body}\n</svg>`;
  return { svg, warnings: M.warnings, model: M };

  function f(v) { return (Math.round(v * 10) / 10).toString(); }

  function renderPanel(pi) {
    curPn = pi;
    const ops = M.ops.filter(o => o.panel === pi);
    const names = M.ptOrder.filter(e => e.panel === pi);
    if (!ops.length && !names.length) return null;
    const T = p => { const q = pj(p); return [q[0] * S, -q[1] * S]; };
    const out = []; let minx = 1e9, miny = 1e9, maxx = -1e9, maxy = -1e9;
    const bb = (x, y) => { minx = Math.min(minx, x); maxx = Math.max(maxx, x); miny = Math.min(miny, y); maxy = Math.max(maxy, y); };
    const segs = []; const blocks = []; // für Namensplatzierung (px)
    const dirs2 = d => { const a = pj(d), b = pj([0, 0, 0]); const v = [a[0] - b[0], -(a[1] - b[1])]; const l = Math.hypot(...v) || 1; return [v[0] / l, v[1] / l]; };
    let cat = 'geo', over = null, R = rng(1);
    const C = () => over || (hand ? PAL[mono ? 'geo' : cat] : '#000');
    const dashOf = d => d === 'gestrichelt' ? '7 4' : d === 'punktiert' ? '1.5 3' : d === 'strichpunkt' ? '10 3 2 3' : null;
    function line(pts, st = {}, closed = false, rec = true) {
      if (pts.length < 2) return;
      pts.forEach(p => bb(...p));
      const d = 'M' + pts.map(p => f(p[0]) + ' ' + f(p[1])).join('L') + (closed ? 'Z' : '');
      const da = dashOf(st.dash);
      let fill = 'none'; if (st.fill) fill = st.fill; if (st.hatchFill) fill = 'url(#sch)';
      if (!closed && st.fill && !st.stroke) { st = Object.assign({}, st, { stroke: st.fill }); fill = 'none'; }
      if (hand) handPath(pts, st, closed, fill);
      else out.push(`<path d="${d}" fill="${fill}" stroke="${st.stroke || C()}" stroke-width="${st.w || 1.1}"${da ? ` stroke-dasharray="${da}"` : ''} stroke-linejoin="round" stroke-linecap="${st.cap || 'round'}"/>`);
      if (rec) for (let i = 0; i < pts.length - 1 + (closed ? 1 : 0); i++) segs.push([pts[i], pts[(i + 1) % pts.length]]);
      if (st.stroke !== 'none' && !(st.w < 0.05)) for (let i = 0; i < pts.length - 1 + (closed ? 1 : 0); i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; ink.push([a[0], a[1], b[0], b[1]]); }
    }
    function circInk(c, r) { for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6, b = a + Math.PI / 6; ink.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a), c[0] + r * Math.cos(b), c[1] + r * Math.sin(b)]); } }
    function circ(c, r, fill, w = 1.2) { bb(c[0] - r, c[1] - r); bb(c[0] + r, c[1] + r); circInk(c, r); if (hand) { handCirc(c, r, fill, w); return; } out.push(`<circle cx="${f(c[0])}" cy="${f(c[1])}" r="${f(r)}" fill="${fill === '#000' ? C() : fill}" stroke="${C()}" stroke-width="${w}"/>`); }
    function head(tip, d, L = 11, W = 4) { const n = [-d[1], d[0]]; const b = [tip[0] - d[0] * L, tip[1] - d[1] * L]; const pts = [tip, [b[0] + n[0] * W, b[1] + n[1] * W], [b[0] - n[0] * W, b[1] - n[1] * W]]; pts.forEach(p => bb(...p)); for (let i = 0; i < 3; i++) ink.push([...pts[i], ...pts[(i + 1) % 3]]);
      if (hand) { const j = () => (R() - 0.5) * 1.4; const q = pts.map((p, i) => i ? [p[0] + j(), p[1] + j()] : p); out.push(`<path d="M${q.map(p => f(p[0]) + ' ' + f(p[1])).join('L')}Z" fill="${C()}" stroke="${C()}" stroke-width="1.3" stroke-linejoin="round"/>`); return; }
      out.push(`<path d="M${pts.map(p => f(p[0]) + ' ' + f(p[1])).join('L')}Z" fill="${C()}"/>`); }
    // --- Handskizze: Linie, Kreis
    function handPath(pts, st, closed, fill) {
      const col = C(), w0 = st.w || 1.1, pathOf = S => 'M' + S.map(q => f(q.p[0]) + ' ' + f(q.p[1])).join('L');
      if (fill && fill !== 'none') {
        const g = fill === '#9a9a9a' ? 0.22 : fill === '#dcdcdc' ? 0.1 : null;
        const fc = fill === 'url(#sch)' ? 'url(#schh)' : g ? (over || (mono ? PAL.geo : PAL[cat])) : fill;
        out.push(`<path d="${pathOf(handLine(pts, true, R, 0.5).S)}Z" fill="${fc}"${g ? ` fill-opacity="${g}"` : ''}/>`);
      }
      if (st.stroke === 'none' || w0 < 0.05) return;
      let sc = col, so = st.stroke === '#9a9a9a' ? 0.5 : st.stroke === '#dcdcdc' ? 0.28 : 1;
      if (so === 1 && st.stroke && st.stroke !== '#000') sc = st.stroke;
      const w = Math.max(1.35, w0 * 1.12), H = handLine(pts, closed, R, Math.min(0.9, 0.3 + w * 0.12)), da = dashOf(st.dash);
      if (da) { out.push(`<path d="${pathOf(H.S)}${closed ? 'Z' : ''}" fill="none" stroke="${sc}"${so < 1 ? ` stroke-opacity="${so}"` : ''} stroke-width="${f(w)}" stroke-dasharray="${da.split(' ').map(v => f(v * 1.3 + (v < 2 ? 0 : 1))).join(' ')}" stroke-linecap="round" stroke-linejoin="round"/>`); return; }
      out.push(`<path d="${handStroke(H, closed, w, R, f)}" fill="${sc}"${so < 1 ? ` fill-opacity="${so}"` : ''}/>`);
    }
    function handCirc(c, r, fill, w) {
      const N = Math.max(14, Math.round(r * 1.5)), a0 = R() * 6.283, pts = [];
      for (let i = 0; i < N; i++) { const a = a0 + 2 * Math.PI * i / N; pts.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
      const fc = fill === '#000' ? C() : fill;
      if (fill === '#000' && r < 4.5) { out.push(`<path d="M${handLine(pts, true, R, r * 0.08).S.map(q => f(q.p[0]) + ' ' + f(q.p[1])).join('L')}Z" fill="${fc}"/>`); return; }
      handPath(pts, { w: w * (r < 8 ? 0.95 : 1) }, true, fc || 'none');
    }
    function hatch(a, b, n, step = 6.5, L = 7) { // n: Seite der Schraffur (px)
      const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); const u = [t[0] / l, t[1] / l];
      const sd = [(n[0] - u[0]) * 0.7071 * L, (n[1] - u[1]) * 0.7071 * L];
      let s = ''; for (let k = step / 2; k <= l; k += step) { const p = [a[0] + u[0] * k, a[1] + u[1] * k]; ink.push([p[0], p[1], p[0] + sd[0], p[1] + sd[1]]); bb(p[0] + sd[0], p[1] + sd[1]);
        if (hand) { const j = () => (R() - 0.5) * 1.2, e = 0.85 + R() * 0.3; s += `M${f(p[0] + j())} ${f(p[1] + j())}l${f(sd[0] * e + j())} ${f(sd[1] * e + j())}`; }
        else s += `M${f(p[0])} ${f(p[1])}l${f(sd[0])} ${f(sd[1])}`; }
      if (hand) out.push(`<path d="${s}" stroke="${C()}" stroke-opacity="0.8" stroke-width="1.15" stroke-linecap="round" fill="none"/>`);
      else out.push(`<path d="${s}" stroke="${C()}" stroke-width="0.8" fill="none"/>`);
    }
    function ground(a, b, n, st = {}) {
      if (st.fill) { const t = 6; const pts = [a, b, [b[0] + n[0] * t, b[1] + n[1] * t], [a[0] + n[0] * t, a[1] + n[1] * t]]; line(pts, { w: 0.01, fill: st.fill, stroke: st.fill }, true, false); line([a, b], { w: 2.4 }, false, false); }
      else { line([a, b], { w: 1.3 }, false, false); hatch(a, b, n); }
    }
    // --- Formelsatz: Indizes, Exponenten, Vektor-Unterstrich, Wurzel mit Überstrich
    // Aufbau als Liste von Teilen (Textläufe, Linien, Pfade) mit gemessenen Breiten, damit nichts ineinanderläuft.
    function isUpright(s, o) { return !!(o && o.upright) || /[A-Za-zÄÖÜäöüß]{4,}/.test(s.replace(/max|min|sqrt|\{[^}]*\}/g, '')); }
    function rich(s, fs, up) {
      const nodes = parseRich([...s]).nodes;
      return lay(nodes, fs, up);
    }
    function lay(nodes, fs, up) {
      let x = 0, asc = fs * 0.7, desc = fs * 0.2; const parts = []; let run = '', runIt = null, prev = null;
      const flush = () => { if (!run) return; parts.push({ k: 't', x, y: 0, s: run, fs, it: runIt }); x += textW(run, fs, runIt, hand); prev = runIt ? 'it' : 'up'; run = ''; };
      const place = (L, dx, dy) => { for (const q of L.parts) parts.push(Object.assign({}, q, q.k === 't' ? { x: q.x + dx, y: q.y + dy } : { pts: q.pts.map(([a, b]) => [a + dx, b + dy]) })); };
      for (const nd of nodes) {
        if (nd.t === 'c') {
          const it = /[A-Za-zα-ωΑ-Ω]/.test(nd.c) && !up && !hand;
          if (run && it !== runIt) flush();
          if (!run && prev === 'it' && !it) x += fs * 0.04; // Kursivkorrektur
          runIt = it; run += nd.c; continue;
        }
        flush();
        if (nd.t === 'vec') {
          const L = lay(nd.b, fs, up); place(L, x, 0);
          const deep = nd.b.some(n => n.t === 'c' && /[gjpqyβγζημξρφχψ]/.test(n.c));
          const uy = fs * (deep ? 0.3 : 0.13), sw = Math.max(0.9, fs * 0.055);
          const it = nd.b.some(n => n.t === 'c' && /[A-Za-zα-ωΑ-Ω]/.test(n.c)) && !up && !hand;
          // Strich nur unter dem Grundzeichen (bei Kursivschrift leicht nach links versetzt)
          parts.push({ k: 'l', pts: [[x + (it ? fs * 0.01 : fs * 0.03), uy], [x + L.w - (it ? fs * 0.06 : fs * 0.02), uy]], sw });
          x += L.w; desc = Math.max(desc, uy + sw); asc = Math.max(asc, L.asc); prev = 'vec';
        } else if (nd.t === 'sub' || nd.t === 'sup') {
          const sfs = Math.max(fs * 0.7, FS * 0.5); const L = lay(nd.b, sfs, up);
          const dy = nd.t === 'sub' ? fs * 0.3 : -fs * 0.42;
          x += prev === 'vec' ? fs * 0.1 : prev === 'it' ? fs * 0.03 : 0;   // Abstand, damit der Index nicht in den Unterstrich läuft
          place(L, x, dy); x += L.w; asc = Math.max(asc, -dy + L.asc); desc = Math.max(desc, dy + L.desc); prev = 'sub';
        } else if (nd.t === 'sqrt') {
          const L = lay(nd.b, fs, up); const sw = Math.max(0.9, fs * 0.055);
          const top = -(L.asc + fs * 0.1), bot = fs * 0.14, w0 = fs * 0.5;
          parts.push({ k: 'l', pts: [[x + fs * 0.03, -fs * 0.26], [x + fs * 0.13, -fs * 0.32], [x + fs * 0.27, bot], [x + w0 - fs * 0.04, top], [x + w0 + L.w + fs * 0.06, top]], sw });
          place(L, x + w0, 0); x += w0 + L.w + fs * 0.1; asc = Math.max(asc, -top + sw); desc = Math.max(desc, bot + sw, L.desc); prev = 'up';
        }
      }
      flush();
      return { w: x, asc, desc, parts };
    }
    function emitRich(L, x, y, anchor, o = {}) {
      const x0 = anchor === 'middle' ? x - L.w / 2 : anchor === 'end' ? x - L.w : x;
      bb(x0, y - L.asc); bb(x0 + L.w, y + L.desc);
      const col = o.color || '#000'; let g = '';
      const esc = c => c.replace(/&/g, '&amp;').replace(/</g, '&lt;');
      for (const q of L.parts) {
        if (q.k === 't') g += `<text xml:space="preserve" x="${f(x0 + q.x)}" y="${f(y + q.y)}" font-size="${f(q.fs)}"${q.it ? ' font-style="italic"' : ''}>${esc(q.s)}</text>`;
        else g += `<path d="M${q.pts.map(([a, b]) => f(x0 + a) + ' ' + f(y + b)).join('L')}" fill="none" stroke="${col}" stroke-width="${f(q.sw)}" stroke-linecap="round" stroke-linejoin="round"/>`;
      }
      const rot = hand ? ` transform="rotate(${f((rng(hashStr(L.parts.map(q => q.s || '').join('')))() - 0.5) * 5)} ${f(x0 + L.w / 2)} ${f(y - L.asc / 3)})"` : '';
      out.push(`<g fill="${col}" stroke-linejoin="round" class="lbl"${rot}><g stroke="#fff" stroke-width="${hand ? 4 : 3.2}" paint-order="stroke">${g.replace(/<path[^>]*\/>/g, '')}</g>${hand ? `<g stroke="${col}" stroke-width="0.55">${g.replace(/<path[^>]*\/>/g, '')}</g>` : ''}${(g.match(/<path[^>]*\/>/g) || []).join('')}</g>`);
    }
    function tex(x, y, s, anchor = 'middle', o = {}) {
      if (s == null || s === '') return;
      const fs = o.small ? FS * 0.75 : FS; emitRich(rich(s, fs, isUpright(s, o)), x, y, anchor, o);
    }
    const LAGE = { r: [1, 0], l: [-1, 0], o: [0, -1], u: [0, 1], or: [0.75, -0.75], ol: [-0.75, -0.75], ur: [0.75, 0.75], ul: [-0.75, 0.75],
      rechts: [1, 0], links: [-1, 0], oben: [0, -1], unten: [0, 1], mitte: [0, 0] };
    const boxes = [];      // bereits gesetzte Beschriftungen (px)
    const ink = [];        // alle gezeichneten Strecken (px) für die Kollisionsprüfung
    const labelQ = [];     // Beschriftungen werden erst gesetzt, wenn alle Linien gezeichnet sind
    const withCol = o => (o && o.color) || (!hand && !over) ? o : Object.assign({}, o, { color: C() });
    function labelAt(p, dir, s, gap = 9, o = {}, own = null) { o = withCol(o); if (s) labelQ.push({ p, dir, s, gap, o, own: own || [[p[0], p[1], p[0], p[1]]], strict: Object.values(LAGE).includes(dir) }); }
    function fixedText(x, y, s, o = {}) { o = withCol(o); if (s) labelQ.unshift({ fixed: [x, y], s, o, own: [[x, y, x, y]] }); }
    function clipLen(sg, b) { // Länge der Strecke innerhalb des Rechtecks (Liang-Barsky)
      let [x1, y1, x2, y2] = sg; const dx = x2 - x1, dy = y2 - y1; let t0 = 0, t1 = 1;
      for (const [pp, qq] of [[-dx, x1 - b[0]], [dx, b[0] + b[2] - x1], [-dy, y1 - b[1]], [dy, b[1] + b[3] - y1]]) {
        if (Math.abs(pp) < 1e-12) { if (qq < 0) return 0; continue; }
        const r = qq / pp; if (pp < 0) { if (r > t1) return 0; if (r > t0) t0 = r; } else { if (r < t0) return 0; if (r < t1) t1 = r; }
      }
      return (t1 - t0) * Math.hypot(dx, dy);
    }
    function boxCost(bx) {
      let c = 0; const sh = [bx[0] + 1, bx[1] + 1, bx[2] - 2, bx[3] - 2];
      for (const q of boxes) { const ox = Math.min(bx[0] + bx[2], q[0] + q[2]) - Math.max(bx[0], q[0]) + 2, oy = Math.min(bx[1] + bx[3], q[1] + q[3]) - Math.max(bx[1], q[1]) + 2; if (ox > 0 && oy > 0) c += 40 + ox * oy; }
      for (const sg of ink) { if (Math.max(sg[0], sg[2]) < sh[0] || Math.min(sg[0], sg[2]) > sh[0] + sh[2] || Math.max(sg[1], sg[3]) < sh[1] || Math.min(sg[1], sg[3]) > sh[1] + sh[3]) continue; const l = clipLen(sg, sh); if (l > 0) c += 6 + 4 * l; }
      return c;
    }
    // Beschriftungen gemeinsam platzieren (Point-Feature Label Placement):
    // Kandidatenpositionen um den Ankerpunkt mit Prioritäten (Imhof 1975), Bewertung von Überlappung mit Linien/Labels,
    // Mehrdeutigkeit (Label näher an fremdem Anker als am eigenen) und Hinweislinien; Optimierung mit Simulated Annealing
    // (Christensen/Marks/Shieber 1995), wie im D3-Labeler. Hinweislinie nur, wenn kein naher Platz frei ist.
    function rectDist(p, b) { const dx = Math.max(b[0] - p[0], 0, p[0] - b[0] - b[2]), dy = Math.max(b[1] - p[1], 0, p[1] - b[1] - b[3]); return Math.hypot(dx, dy); }
    function rectPoint(p, b) { return [Math.max(b[0], Math.min(p[0], b[0] + b[2])), Math.max(b[1], Math.min(p[1], b[1] + b[3]))]; }
    function geoDist(G, b) { let m = Infinity; for (const g of G) for (let k = 0; k <= 8; k++) { const t = k / 8; m = Math.min(m, rectDist([g[0] + (g[2] - g[0]) * t, g[1] + (g[3] - g[1]) * t], b)); if (g[0] === g[2] && g[1] === g[3]) break; } return m; }
    function placeAll() {
      const Q = labelQ.map(q => { const o = q.o || {}; const fs = o.small ? FS * 0.75 : FS; const L = rich(q.s, fs, isUpright(q.s, o)); return Object.assign({}, q, { o, L, hh: L.asc + L.desc }); });
      const anchors = Q.map(q => q.fixed || q.p);
      for (const [qi, q] of Q.entries()) {
        const { L, hh } = q; q.c = [];
        if (q.fixed) { const [x, y] = q.fixed; q.c.push({ bx: [x - L.w / 2, y - hh / 2, L.w, hh], s: 0 }); continue; }
        const { p, dir, gap } = q; const zero = !dir[0] && !dir[1]; const base = Math.atan2(dir[1], dir[0]);
        const devs = zero ? [0] : q.strict ? [0, 20, -20, 40, -40] : [0, 20, -20, 40, -40, 60, -60, 90, -90, 120, -120, 150, -150, 180];  // mit 'lage' bleibt die gewünschte Seite
        const gaps = zero ? [[0, 0, 0]] : q.strict ? [[0, gap, 0], [1, gap + 5, 0], [2, gap + 11, 0]] : [[0, gap, 0], [1, gap + 5, 0], [2, gap + 11, 0], [3, gap + 26, 1], [4, gap + 42, 1]];
        for (const [gi, g, lead] of gaps) for (const dv of devs) {
          const d = zero ? [0, 0] : [Math.cos(base + dv * DEG), Math.sin(base + dv * DEG)];
          const cx = p[0] + d[0] * (g + L.w / 2), cy = p[1] + d[1] * (g + hh / 2);
          const bx = [cx - L.w / 2, cy - hh / 2, L.w, hh];
          let s = boxCost(bx) + Math.abs(dv) / 20 * 3 + gi * 6;
          // Mehrdeutigkeit: liegt ein fremder Anker näher am Label als der eigene?
          const dOwn = geoDist(q.own, bx);
          for (const [aj, r] of Q.entries()) { if (aj === qi) continue; const a = anchors[aj]; if (Math.hypot(a[0] - p[0], a[1] - p[1]) < 3) continue; const da = geoDist(r.own, bx); if (da < dOwn + 6) s += (dOwn + 6 - da) * 4; }
          let ld = null;
          if (lead) { const e = rectPoint(p, bx); const u = [e[0] - p[0], e[1] - p[1]]; const l = Math.hypot(...u) || 1; ld = [p[0] + u[0] / l * 3, p[1] + u[1] / l * 3, e[0] - u[0] / l * 1.5, e[1] - u[1] / l * 1.5];
            s += 30 + l * 0.6; for (const sg of ink) if (segX(ld, sg)) s += 25; }
          q.c.push({ bx, s, ld });
        }
      }
      // Paar-Kosten zweier gewählter Kandidaten
      const pair = (a, b) => { let c = 0; const A = a.bx, B = b.bx; const ox = Math.min(A[0] + A[2], B[0] + B[2]) - Math.max(A[0], B[0]) + 2, oy = Math.min(A[1] + A[3], B[1] + B[3]) - Math.max(A[1], B[1]) + 2;
        if (ox > 0 && oy > 0) c += 40 + ox * oy;
        if (a.ld && clipLen(a.ld, B) > 0) c += 30; if (b.ld && clipLen(b.ld, A) > 0) c += 30; if (a.ld && b.ld && segX(a.ld, b.ld)) c += 30; return c; };
      const n = Q.length; const sel = Q.map(q => { let bi = 0; q.c.forEach((c, i) => { if (c.s < q.c[bi].s) bi = i; }); return bi; });
      const nb = Q.map((q, i) => Q.map((r, j) => j).filter(j => j !== i && Math.abs(Q[j].c[0].bx[0] - q.c[0].bx[0]) < 400 && Math.abs(Q[j].c[0].bx[1] - q.c[0].bx[1]) < 400));
      const local = (i, ci) => { let c = Q[i].c[ci].s; for (const j of nb[i]) c += pair(Q[i].c[ci], Q[j].c[sel[j]]); return c; };
      // Greedy-Durchgänge, dann Simulated Annealing mit festem Zufallsstartwert (reproduzierbar)
      for (let it = 0; it < 3; it++) for (let i = 0; i < n; i++) { let b = sel[i], bc = local(i, b); for (let k = 0; k < Q[i].c.length; k++) { const c = local(i, k); if (c < bc - 1e-6) { bc = c; b = k; } } sel[i] = b; }
      let seed = 12345; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
      if (n > 1) { let T = 40; const steps = Math.min(30000, 300 * n);
        for (let s = 0; s < steps; s++) { const i = Math.floor(rnd() * n); if (Q[i].c.length < 2) continue; const k = Math.floor(rnd() * Q[i].c.length); const d = local(i, k) - local(i, sel[i]);
          if (d < 0 || rnd() < Math.exp(-d / T)) sel[i] = k; T = Math.max(0.5, T * 0.9995); }
        for (let it = 0; it < 2; it++) for (let i = 0; i < n; i++) { let b = sel[i], bc = local(i, b); for (let k = 0; k < Q[i].c.length; k++) { const c = local(i, k); if (c < bc - 1e-6) { bc = c; b = k; } } sel[i] = b; } }
      Q.forEach((q, i) => {
        const c = q.c[sel[i]]; const bx = c.bx; const res = boxCost(bx) + nb[i].reduce((s, j) => s + pair(c, Q[j].c[sel[j]]) / 2, 0);
        if (res > 0) (M.diag || (M.diag = [])).push([q.s, Math.round(res)]);
        if (c.ld) { out.push(`<path d="M${f(c.ld[0])} ${f(c.ld[1])}L${f(c.ld[2])} ${f(c.ld[3])}" stroke="${q.o.color || '#000'}" stroke-width="0.7" fill="none"/>`); (M.leaders || (M.leaders = [])).push(q.s); }
        boxes.push(bx); emitRich(q.L, bx[0] + bx[2] / 2, bx[1] + q.L.asc, 'middle', q.o);
        over = q.o.color || null; if (q.o.box) line([[bx[0] - 5, bx[1] - 3], [bx[0] + bx[2] + 5, bx[1] - 3], [bx[0] + bx[2] + 5, bx[1] + bx[3] + 3], [bx[0] - 5, bx[1] + bx[3] + 3]], { w: 0.8 }, true, false);
      });
    }
    function segX(a, b) { const o = (p, q, r) => Math.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]));
      const A = [a[0], a[1]], B = [a[2], a[3]], C = [b[0], b[1]], D = [b[2], b[3]]; return o(A, B, C) * o(A, B, D) < 0 && o(C, D, A) * o(C, D, B) < 0; }

    // --- Zeichnen
    const later = [];
    const catOf = o => { switch (o.k) {
      case 'force': return o.dbl ? 'moment' : o.thin ? 'hilf' : (o.kind === 'vektor' || o.kind === 'geschwindigkeit') ? 'kin' : 'kraft';
      case 'load': return 'kraft'; case 'moment': return 'moment'; case 'spin': return 'kin';
      case 'support': case 'ground': case 'qlager': return 'lager';
      case 'dim': case 'edge': case 'angle': case 'rangle': case 'arrow': return 'hilf';
      case 'text': return 'text';
      case 'poly': return o.st && o.st.dash ? 'hilf' : 'geo';
      default: return 'geo'; } };
    const seedOf = o => hashStr(JSON.stringify(o, (k, v) => typeof v === 'number' ? Math.round(v * 1000) : v));
    for (const o of ops) {
      const oc = catOf(o), ov = (o.st && o.st.farbe) || o.farbe || null, sd = hand ? seedOf(o) : 0, n0 = later.length;
      cat = oc; over = ov; R = rng(sd);
      switch (o.k) {
        case 'poly': { const q = o.pts.map(T); line(q, o.st, o.closed);
          if (o.marks) { const L = []; let tot = 0; for (let i = 1; i < q.length; i++) { tot += Math.hypot(q[i][0] - q[i - 1][0], q[i][1] - q[i - 1][1]); L.push(tot); }
            for (const m of o.marks) { const t = m * tot; const i = L.findIndex(v => v >= t); if (i < 0) continue; const a = q[i], b = q[i + 1]; const d = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...d) || 1; head(b, [d[0] / l, d[1] / l], 9, 3.5); } }
          break; }
        case 'circle3': case 'sphere': {
          if (flat3() || o.k === 'sphere') { const c = T(o.c); const r = o.r * S; bb(c[0] - r, c[1] - r); bb(c[0] + r, c[1] + r); circInk(c, r); if (hand) handCirc(c, r, o.st.fill || 'none', o.st.w || 2); else out.push(`<circle cx="${f(c[0])}" cy="${f(c[1])}" r="${f(r)}" fill="${o.st.fill || 'none'}" stroke="${C()}" stroke-width="${o.st.w || 2}"/>`); if (o.k === 'sphere' && !flat3()) line(ring(o.c, o.r, [0, 0, 1]).map(T), { w: 0.8, dash: 'gestrichelt' }, true, false); break; }
          line(ring(o.c, o.r, o.n).map(T), o.st, true); break;
        }
        case 'dot': { const p = T(o.p); circ(p, 3.2, '#000', 0.5); break; }
        case 'qlager': { const p = T(o.p); const d = dirs2(o.d); const n = [-d[1], d[0]]; const L = o.lang ? 26 : 4, H = o.lang ? 10 : 14, g = 3;
          for (const sg of [1, -1]) { const c = (u, v) => [p[0] + d[0] * u + n[0] * v * sg, p[1] + d[1] * u + n[1] * v * sg]; line([c(-L, g), c(L, g), c(L, g + H), c(-L, g + H)], { w: 1, hatchFill: true }, true, false); }
          break; }
        case 'brk': { const p = T(o.p); const d = dirs2(o.d); const n = [-d[1], d[0]]; const q = []; for (let i = 0; i <= 12; i++) { const t = (i / 12 - 0.5) * 18; const w = Math.sin(i / 12 * 2 * Math.PI) * 3; q.push([p[0] + n[0] * t + d[0] * w, p[1] + n[1] * t + d[1] * w]); } line(q, { w: 0.9 }, false, false); break; }
        case 'rangle': later.push(() => { const v = T(o.v), a = dirs2(o.d1), b = dirs2(o.d2), k = 9;
          line([[v[0] + a[0] * k, v[1] + a[1] * k], [v[0] + (a[0] + b[0]) * k, v[1] + (a[1] + b[1]) * k], [v[0] + b[0] * k, v[1] + b[1] * k]], { w: 0.9 }, false, false);
          circ([v[0] + (a[0] + b[0]) * k * 0.5, v[1] + (a[1] + b[1]) * k * 0.5], 1.1, '#000', 0.2); }); break;
        case 'spin': later.push(() => {
          const rw = o.r || 9 / S; const R = ring(o.p, rw, o.n, 60).slice(4, 56); let q = R.map(T); if (o.cw) q.reverse();
          line(q, { w: 1.2 }, false, false); const a = q[q.length - 2], b = q[q.length - 1]; const d = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...d) || 1; head([b[0] + d[0] / l * 5, b[1] + d[1] / l * 5], [d[0] / l, d[1] / l], 8, 3.2);
          if (o.label) labelAt(T(o.p), o.lage ? LAGE[o.lage] : [-0.8, -0.6], o.label, rw * S + 3);
        }); break;
        case 'outof': { const p = T(o.p); later.push(() => { circ(p, 6, '#fff', 1.1); if (o.into) { line([[p[0] - 4, p[1] - 4], [p[0] + 4, p[1] + 4]], { w: 1 }, false, false); line([[p[0] - 4, p[1] + 4], [p[0] + 4, p[1] - 4]], { w: 1 }, false, false); } else circ(p, 1.6, '#000', 0.3); labelAt(p, o.lage ? LAGE[o.lage] : [-1, 0], o.label, 8); }); break; }
        case 'hinge': later.push(() => circ(T(o.p), 4, '#fff', 1.6)); break;
        case 'cog': { const p = T(o.p); circ(p, 6, '#fff', 1); out.push(`<path d="M${f(p[0])} ${f(p[1])}v-6a6 6 0 0 1 6 6zM${f(p[0])} ${f(p[1])}v6a6 6 0 0 1 -6 -6z" fill="${C()}"/>`); break; }
        case 'support': {
          const p = T(o.p); const n = [Math.cos(o.ang * DEG), -Math.sin(o.ang * DEG)]; const t = [-n[1], n[0]];
          const at = (k, m) => [p[0] - n[0] * k + t[0] * m, p[1] - n[1] * k + t[1] * m];
          segs.push([p, at(14, 0)]);
          if (o.typ === 'einspannung') { const a = at(0, -16), b = at(0, 16); ground(a, b, [-n[0], -n[1]], o.st); break; }
          if (o.typ === 'kugelgelenk') { circ(p, 6, '#fff', 1.4); ground(at(9, -12), at(9, 12), [-n[0], -n[1]], o.st); later.push(() => circ(p, 2.2, '#000', 0.5)); break; }
          if (o.typ === 'schiebehülse') { line([at(-10, -7), at(10, -7)], { w: 1.4 }, false, false); line([at(-10, 7), at(10, 7)], { w: 1.4 }, false, false); ground(at(-10, -7), at(10, -7), t.map(v => -v), o.st); ground(at(10, 7), at(-10, 7), t, o.st); break; }
          const h = 15, b = 9;
          line([p, at(h, -b), at(h, b)], { w: 1.4 }, true, false);
          if (o.typ === 'loslager') { circ(at(h + 3, -4.5), 2.6, '#fff', 1); circ(at(h + 3, 4.5), 2.6, '#fff', 1); ground(at(h + 6, -13), at(h + 6, 13), [-n[0], -n[1]], o.st); }
          else ground(at(h, -13), at(h, 13), [-n[0], -n[1]], o.st);
          later.push(() => circ(p, 4, '#fff', 1.6)); break;
        }
        case 'ground': {
          const a = T(o.a), b = T(o.b); const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t) || 1; let n = [-t[1] / l, t[0] / l];
          const want = LAGE[o.side] || [0, 1]; if (n[0] * want[0] + n[1] * want[1] < 0) n = [-n[0], -n[1]];
          ground(a, b, n, o.st); segs.push([a, b]); blocks.push({ a, b, n }); break;
        }
        case 'rope': line([T(o.a), T(o.b)], Object.assign({ w: 1.1 }, o.st)); break;
        case 'spring': {
          const a = T(o.a), b = T(o.b); const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); const u = [t[0] / l, t[1] / l], n = [-u[1], u[0]];
          const pts = [a]; const z = 8, s0 = l * 0.15, s1 = l * 0.85;
          pts.push([a[0] + u[0] * s0, a[1] + u[1] * s0]);
          for (let i = 1; i < 2 * z; i++) { const k = s0 + (s1 - s0) * i / (2 * z); const sg = i % 2 ? 6 : -6; pts.push([a[0] + u[0] * k + n[0] * sg, a[1] + u[1] * k + n[1] * sg]); }
          pts.push([a[0] + u[0] * s1, a[1] + u[1] * s1], b); line(pts, { w: 1.1 }); break;
        }
        case 'force': later.push(() => drawForce(o)); break;
        case 'arrow': later.push(() => { const a = T(o.a), b = T(o.b); const d = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...d); const u = [d[0] / l, d[1] / l]; line([a, [b[0] - u[0] * 6, b[1] - u[1] * 6]], Object.assign({ w: 1 }, o.st), false, false); head(b, u, 11, 3.6); if (o.dbl) head(a, [-u[0], -u[1]], 11, 3.6); labelAt(b, o.lage ? LAGE[o.lage] : u, o.label, 4, {}, [[a[0], a[1], b[0], b[1]]]); }); break;
        case 'moment': later.push(() => {
          const p = T(o.p), r = 17; const a0 = 40 * DEG, a1 = 330 * DEG;
          const pts = []; for (let i = 0; i <= 40; i++) { const a = a0 + (a1 - a0) * i / 40; pts.push([p[0] + r * Math.cos(a), p[1] - r * Math.sin(a)]); }
          line(o.cw ? pts.slice().reverse() : pts, { w: 1.6 }, false, false);
          const end = o.cw ? a0 : a1; const tip = [p[0] + r * Math.cos(end), p[1] - r * Math.sin(end)];
          const tg = o.cw ? [Math.sin(end), Math.cos(end)] : [-Math.sin(end), -Math.cos(end)];
          head([tip[0] + tg[0] * 6, tip[1] + tg[1] * 6], tg, 10, 4);
          labelAt([p[0] + r * 0.75, p[1] - r * 0.75], o.lage ? LAGE[o.lage] : [0.7, -0.7], o.label, 4);
        }); break;
        case 'load': {
          const a = T(o.a), b = T(o.b); const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); const u = [t[0] / l, t[1] / l]; let n = [-u[1], u[0]];
          const want = LAGE[o.side] || [0, -1]; if (n[0] * want[0] + n[1] * want[1] < 0) n = [-n[0], -n[1]];
          if (o.dir) { const d = dirs2(o.dir); n = o.out ? d : [-d[0], -d[1]]; }   // Last liegt entgegen der Pfeilrichtung (bzw. in Pfeilrichtung bei nachaussen)
          else if (o.out) n = [-n[0], -n[1]];
          const H = o.h ? o.h * S : 42; const qs = o.qs; const qm = Math.max(...qs.map(Math.abs)) || 1;
          const hq = k => { const m = qs.length - 1; if (m === 1) return qs[0] + (qs[1] - qs[0]) * k; const x = k * m; const i = Math.min(m - 1, Math.floor(x)); const tt = x - i;
            const g = j => qs[Math.max(0, Math.min(m, j))]; const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
            return 0.5 * (2 * p1 + (-p0 + p2) * tt + (2 * p0 - 5 * p1 + 4 * p2 - p3) * tt * tt + (-p0 + 3 * p1 - 3 * p2 + p3) * tt * tt * tt); };
          const top = []; for (let i = 0; i <= 40; i++) { const k = i / 40; const h = H * hq(k) / qm; top.push([a[0] + t[0] * k + n[0] * h, a[1] + t[1] * k + n[1] * h]); }
          line([a, b], Object.assign({ w: 0.9 }, o.st), false, false); line(top, Object.assign({ w: 0.9 }, o.st), false, false);
          if (!o.dir) { line([a, top[0]], { w: 0.9 }, false, false); line([b, top[40]], { w: 0.9 }, false, false); }
          if (o.st.hatchFill) line([a, b, ...top.slice().reverse()], { w: 0.01, hatchFill: true, stroke: 'none' }, true, false);
          const cnt = Math.max(3, Math.round(l / (o.dir ? 24 : 20)));
          if (!o.noarrows) for (let i = 1; i < cnt; i++) { const k = i / cnt; const h = H * hq(k) / qm; if (Math.abs(h) < 7) continue; const base = [a[0] + t[0] * k, a[1] + t[1] * k]; const st = [base[0] + n[0] * h, base[1] + n[1] * h]; const sg = Math.sign(h);
            if (o.out) { line([base, [st[0] - n[0] * 5 * sg, st[1] - n[1] * 5 * sg]], { w: 0.8 }, false, false); head(st, [n[0] * sg, n[1] * sg], 7, 2.6); }
            else { line([st, [base[0] + n[0] * 5 * sg, base[1] + n[1] * 5 * sg]], { w: 0.7 }, false, false); head(base, [-n[0] * sg, -n[1] * sg], 5, 2); } }
          let ki = 0, hm = 0; for (let i = 0; i <= 40; i++) { const h = Math.abs(hq(i / 40)); if (h > hm) { hm = h; ki = i; } }
          labelAt(top[ki], [n[0] * 0.6 + (ki >= 20 ? u[0] : -u[0]) * 0.6, n[1] * 0.6 + (ki >= 20 ? u[1] : -u[1]) * 0.6], o.label, 5);
          break;
        }
        case 'dim': later.push(() => {
          const a = T(o.a), b = T(o.b); const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); const u = [t[0] / l, t[1] / l]; let n = [u[1], -u[0]];
          let off = o.off != null ? o.off * S : 22; if (o.seite) { const want = LAGE[o.seite]; if (want && n[0] * want[0] + n[1] * want[1] < 0) n = [-n[0], -n[1]]; off = Math.abs(off); }
          const A = [a[0] + n[0] * off, a[1] + n[1] * off], B = [b[0] + n[0] * off, b[1] + n[1] * off];
          const ex = 5 * Math.sign(off || 1);
          line([[a[0] + n[0] * Math.sign(off) * 3, a[1] + n[1] * Math.sign(off) * 3], [A[0] + n[0] * ex, A[1] + n[1] * ex]], { w: 0.6 }, false, false);
          line([[b[0] + n[0] * Math.sign(off) * 3, b[1] + n[1] * Math.sign(off) * 3], [B[0] + n[0] * ex, B[1] + n[1] * ex]], { w: 0.6 }, false, false);
          if (o.stil === 'tick') { line([A, B], { w: 0.8 }, false, false); }
          else { line([[A[0] + u[0] * 8, A[1] + u[1] * 8], [B[0] - u[0] * 8, B[1] - u[1] * 8]], { w: 0.8 }, false, false); head(A, [-u[0], -u[1]], 10, 3.4); head(B, u, 10, 3.4); }
          const m = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2]; const sn = Math.sign(off) || 1;
          labelAt(m, [n[0] * sn, n[1] * sn], o.label, 3, {}, [[A[0], A[1], B[0], B[1]]]);
        }); break;
        case 'edge': later.push(() => {
          const a = T(o.a), b = T(o.b); const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); let n = [-t[1] / l, t[0] / l];
          if (o.seite === 'aussen' || o.seite === 'innen') {
            // Seite bestimmen: weg vom Schwerpunkt benachbarter Körper
            let c = null, best = 1e18;
            for (const B of Object.values(M.bodies)) { if (!B.pts) continue; const bc = T(B.center); const d = Math.hypot(bc[0] - m[0], bc[1] - m[1]); if (d < best) { best = d; c = bc; } }
            if (c && ((m[0] - c[0]) * n[0] + (m[1] - c[1]) * n[1] < 0) === (o.seite === 'aussen')) n = [-n[0], -n[1]];
          } else if (LAGE[o.seite]) { const w = LAGE[o.seite]; if (n[0] * w[0] + n[1] * w[1] < 0) n = [-n[0], -n[1]]; }
          labelAt(m, n, o.label, 4, {}, [[a[0], a[1], b[0], b[1]]]);
        }); break;
        case 'angle': later.push(() => {
          if (!flat3()) {
            const d1 = unit(o.d1), d2 = unit(o.d2); const th = Math.acos(Math.max(-1, Math.min(1, dot(d1, d2))));
            let w = sub(d2, mul(d1, dot(d1, d2))); w = len(w) < 1e-9 ? [0, 0, 1] : unit(w);
            const rw = (o.r || 26) / S; const P3 = t => add(o.v, add(mul(d1, rw * Math.cos(t)), mul(w, rw * Math.sin(t))));
            const pts = []; for (let i = 0; i <= 30; i++) pts.push(T(P3(th * i / 30)));
            line(pts, { w: 0.9 }, false, false);
            const vv = T(o.v), m = T(P3(th / 2)); const dd = [m[0] - vv[0], m[1] - vv[1]]; const l = Math.hypot(...dd) || 1;
            labelAt(m, [dd[0] / l, dd[1] / l], o.label, 3); return;
          }
          const v = T(o.v); const d1 = dirs2(o.d1), d2 = dirs2(o.d2);
          let a1 = Math.atan2(d1[1], d1[0]), a2 = Math.atan2(d2[1], d2[0]); let da = a2 - a1; while (da > Math.PI) da -= 2 * Math.PI; while (da < -Math.PI) da += 2 * Math.PI;
          const r = o.r || 26; const pts = []; for (let i = 0; i <= 30; i++) { const a = a1 + da * i / 30; pts.push([v[0] + r * Math.cos(a), v[1] + r * Math.sin(a)]); }
          line(pts, { w: 0.9 }, false, false);
          if (o.dbl) { const p2 = pts.map(p => [v[0] + (p[0] - v[0]) * 0.85, v[1] + (p[1] - v[1]) * 0.85]); line(p2, { w: 0.9 }, false, false); }
          const am = a1 + da / 2; labelAt([v[0] + r * Math.cos(am), v[1] + r * Math.sin(am)], [Math.cos(am), Math.sin(am)], o.label, 3);
        }); break;
        case 'text': later.push(() => {
          const p = T(o.p);
          if (o.seg) { const a = T(o.seg[0]), b = T(o.seg[1]); const t = [b[0] - a[0], b[1] - a[1]]; const l = Math.hypot(...t); labelAt(p, [-t[1] / l, t[0] / l], o.s, 3, o); return; }
          if (o.lage && LAGE[o.lage]) labelAt(p, LAGE[o.lage], o.s, 5, o); else fixedText(p[0], p[1], o.s, o);
        }); break;
        case 'box': {
          const [x0, y0, z0] = o.a, [x1, y1, z1] = o.b; const C = []; for (const x of [x0, x1]) for (const y of [y0, y1]) for (const z of [z0, z1]) C.push([x, y, z]);
          let hid = 0, mn = 1e9; C.forEach((c, i) => { const d = dot(c, view); if (d < mn) { mn = d; hid = i; } });
          for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) { const diff = sub(C[i], C[j]).filter(v => Math.abs(v) > 1e-9).length; if (diff !== 1) continue; const h = i === hid || j === hid; line([T(C[i]), T(C[j])], h ? { w: 0.9, dash: 'gestrichelt' } : Object.assign({ w: 2.2 }, o.st), false, !h); }
          break;
        }
        case 'cone': case 'cyl': {
          let rings, apex = null;
          if (o.k === 'cone') { rings = [ring(o.c, o.r, unit(sub(o.c, o.s)))]; apex = o.s; }
          else { const top = add(o.c, mul(o.ax, o.h)); rings = [ring(o.c, o.r, o.ax), ring(top, o.r, o.ax)]; }
          const all = []; rings.forEach((R, ri) => R.forEach((p, k) => all.push({ p: T(p), ri, k })));
          if (apex) all.push({ p: T(apex), ri: -1 });
          const hull = convexHull(all);
          // Mantellinien: Hull-Kanten zwischen verschiedenen Ringen / Spitze
          for (let i = 0; i < hull.length; i++) { const A = hull[i], B = hull[(i + 1) % hull.length]; if (A.ri !== B.ri) line([A.p, B.p], Object.assign({ w: 2.2 }, o.st)); }
          // Ringe: sichtbar wenn Deckfläche zum Betrachter zeigt; sonst nur Hull-Teile durchgezogen
          const capN = o.k === 'cone' ? [unit(sub(o.c, o.s))] : [mul(o.ax, -1), o.ax];
          rings.forEach((R, ri) => {
            const vis = dot(capN[ri], view) > 0; const onHull = new Set(hull.filter(h => h.ri === ri).map(h => h.k));
            if (vis) { line(R.map(T), Object.assign({ w: 2.2 }, o.st), true); return; }
            // hintere Hälfte gestrichelt: Punkte, die "hinter" liegen
            const ctr = o.k === 'cone' ? o.c : (ri ? add(o.c, mul(o.ax, o.h)) : o.c);
            let run = [], runVis = null; const flush = () => { if (run.length > 1) line(run, runVis ? Object.assign({ w: 2.2 }, o.st) : { w: 0.9, dash: 'gestrichelt' }, false, runVis); run = []; };
            for (let k = 0; k <= R.length; k++) { const p = R[k % R.length]; const front = dot(sub(p, ctr), view) > -1e-9; if (runVis !== null && front !== runVis) { const last = run[run.length - 1]; flush(); run = [last]; } runVis = front; run.push(T(p)); }
            flush();
          });
          break;
        }
      }
      for (let i = n0; i < later.length; i++) { const fn = later[i]; later[i] = () => { cat = oc; over = ov; R = rng(sd + 1); fn(); }; }
    }
    later.forEach(fn => fn());
    cat = 'text'; over = null;

    function drawForce(o) {
      const p = T(o.p); const u = dirs2(o.d);
      const L = o.len ? o.len * S : (o.pxlen || (o.thick ? 62 : 50));
      const th = o.thick ? 5 : (o.st && o.st.w) || 1.5;
      const hl = o.thick ? 20 : 11, hw = o.thick ? 7 : 4;
      let tail, tip;
      if (o.zu) { tip = p; tail = [p[0] - u[0] * L, p[1] - u[1] * L]; } else { tail = p; tip = [p[0] + u[0] * L, p[1] + u[1] * L]; }
      const back = o.dbl ? hl * 1.7 : hl * 0.8;
      line([tail, [tip[0] - u[0] * back, tip[1] - u[1] * back]], { w: th, cap: 'butt' }, false, false);
      head(tip, u, hl, hw); if (o.dbl) head([tip[0] - u[0] * hl * 0.8, tip[1] - u[1] * hl * 0.8], u, hl, hw);
      segs.push([p, o.zu ? tail : tip]);
      // Beschriftung: an der Spitze, seitlich versetzt
      const own = [[tail[0], tail[1], tip[0], tip[1]]];
      if (o.lage && LAGE[o.lage]) { labelAt(o.zu ? tail : tip, LAGE[o.lage], o.label, 4, {}, own); return; }
      const end = o.zu ? tail : tip; let n = [-u[1], u[0]]; if (n[1] > 0.3 || (Math.abs(n[1]) <= 0.3 && n[0] < 0)) n = [-n[0], -n[1]];
      if (o.thin) labelAt(end, u, o.label, 3, {}, own); else labelAt([end[0] - u[0] * 4, end[1] - u[1] * 4], [u[0] * 0.45 + n[0] * 0.9, u[1] * 0.45 + n[1] * 0.9], o.label, 3, {}, own);
    }

    // --- Punktnamen (grösste Winkellücke)
    if (!M.noLabels) for (const ent of names) { const nm = ent.n;
      if (M.noLabel.has(nm) && !(M.labelOpts[nm] && M.labelOpts[nm].s)) continue;
      const lo = M.labelOpts[nm] || {}; const s = lo.s || nm.replace(/'/g, '′');
      const p = T(ent.p); const ang = [];
      for (const [a, b] of segs) {
        for (const [q, r] of [[a, b], [b, a]]) {
          if (Math.hypot(q[0] - p[0], q[1] - p[1]) < 1.5) { ang.push(Math.atan2(r[1] - q[1], r[0] - q[0])); }
          else { // Punkt liegt im Inneren eines Segments
            const t = [r[0] - q[0], r[1] - q[1]]; const L2 = t[0] * t[0] + t[1] * t[1]; if (!L2) continue; const k = ((p[0] - q[0]) * t[0] + (p[1] - q[1]) * t[1]) / L2;
            if (k > 0.02 && k < 0.98 && Math.abs((p[0] - q[0]) * t[1] - (p[1] - q[1]) * t[0]) / Math.sqrt(L2) < 1.5) ang.push(Math.atan2(t[1], t[0]));
          }
        }
      }
      for (const g of blocks) { const t = [g.b[0] - g.a[0], g.b[1] - g.a[1]]; const L2 = t[0] * t[0] + t[1] * t[1]; const k = ((p[0] - g.a[0]) * t[0] + (p[1] - g.a[1]) * t[1]) / L2; if (k > -0.02 && k < 1.02 && Math.abs((p[0] - g.a[0]) * t[1] - (p[1] - g.a[1]) * t[0]) / Math.sqrt(L2) < 2) { const a0 = Math.atan2(g.n[1], g.n[0]); ang.push(a0 - 0.6, a0, a0 + 0.6); } }
      let dir;
      if (lo.lage && LAGE[lo.lage]) dir = LAGE[lo.lage];
      else if (!ang.length) dir = [0.7, -0.7];
      else {
        ang.sort((x, y) => x - y); let best = -1, bi = 0;
        for (let i = 0; i < ang.length; i++) { const g = (i + 1 < ang.length ? ang[i + 1] : ang[0] + 2 * Math.PI) - ang[i]; if (g > best + 1e-6) { best = g; bi = i; } }
        // bevorzugt leicht nach oben/links, wenn Lücke riesig
        const a = ang[bi] + best / 2; dir = [Math.cos(a), Math.sin(a)];
        if (best > 1.6 * Math.PI) { const c = [[-0.7, -0.7], [0.7, -0.7], [-0.7, 0.7], [0.7, 0.7]]; dir = c.reduce((bst, v) => (v[0] * dir[0] + v[1] * dir[1]) > (bst[0] * dir[0] + bst[1] * dir[1]) ? v : bst); }
      }
      labelAt(p, dir, s, 5);
    }
    over = null; placeAll();
    return { svg: out.join('\n'), minx: minx - 6, miny: miny - 6, w: maxx - minx + 12, h: maxy - miny + 12 };
  }
}
function ring(c, r, n, N = 72) {
  n = unit(n); let a = Math.abs(n[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0]; const u = unit(cross(n, a)), v = cross(n, u);
  const pts = []; for (let i = 0; i < N; i++) { const t = 2 * Math.PI * i / N; pts.push(add(c, add(mul(u, r * Math.cos(t)), mul(v, r * Math.sin(t))))); }
  return pts;
}
function convexHull(items) {
  const P = items.slice().sort((a, b) => a.p[0] - b.p[0] || a.p[1] - b.p[1]);
  const cr = (o, a, b) => (a.p[0] - o.p[0]) * (b.p[1] - o.p[1]) - (a.p[1] - o.p[1]) * (b.p[0] - o.p[0]);
  const lo = [], up = [];
  for (const p of P) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
  for (const p of P.slice().reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
  return lo.slice(0, -1).concat(up.slice(0, -1));
}

const api = { parse, render, version: '0.3' };
if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.MechSkizze = api;
})(typeof window !== 'undefined' ? window : globalThis);
