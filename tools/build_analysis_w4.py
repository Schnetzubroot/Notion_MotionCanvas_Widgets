"""Widgets zu Analysis I, Woche 4: Kapitel II.1 Begriff des Differentialquotienten (Rechenregeln, Kettenregel,
Ableitung der Umkehrfunktion) und II.2 Linearisieren (Stammbach, Teil A, Kap. II S. 3-17; Vorlesungsnotizen Kap. II, S. 1-8)."""
from template import build
from build_analysis_w1 import AX, BOX
from build_analysis_w3 import EQ, TALLBOX

# numerische Ableitung (zentraler Differenzenquotient), nur zur Kontrolle in der Anzeige
ND = r'''
  const nd = (f, x, h = 1e-5) => (f(x + h) - f(x - h)) / (2 * h);
'''

W = []

# ---------------------------------------------------------------- 1.1
W.append(dict(file='1-1-sekante-tangente.html', title='Vom Differenzenquotienten zum Differentialquotienten',
  sub='Die Sekante durch P = (x₀, f(x₀)) und Q = (x₀ + Δx, f(x₀ + Δx)) hat die Steigung (f(x₀ + Δx) − f(x₀))/Δx. Für Δx → 0 wird sie zur Tangente, falls der Grenzwert existiert. Dann ist er f′(x₀).',
  hint='Beispiel wählen, Δx gegen 0 schieben (auch negativ).', legend=[('--c2', 'Graph von f'), ('--c1', 'Sekante PQ'), ('--c3', 'Tangente in P')], js=AX + r'''
  const S = {
    sq: { name: 'f(x) = x²', f: x => x * x, df: x => 2 * x, x0: 1, win: [-1.5, 3, -1, 6], move: true, note: 'Skript/Vorlesung: ((x + Δx)² − x²)/Δx = 2x + Δx → 2x.' },
    sin: { name: 'f(x) = sin x', f: Math.sin, df: Math.cos, x0: 1, win: [-1, 4, -1.4, 1.4], move: true, note: 'Skript (S. 6): der Grenzwert ist cos x₀. Dafür braucht man sin(Δx)/Δx → 1.' },
    abs: { name: 'f(x) = |x| bei x₀ = 0', f: Math.abs, df: null, x0: 0, win: [-2, 2, -0.5, 2], move: false, note: 'Von rechts ist die Steigung immer +1, von links immer −1. Die beiden einseitigen Grenzwerte sind verschieden: nicht differenzierbar.' },
    root: { name: 'f(x) = √|x| bei x₀ = 0', f: x => Math.sqrt(Math.abs(x)), df: null, x0: 0, win: [-2, 2, -0.5, 1.6], move: false, note: 'Vorlesung (S. 2): √Δx/Δx = 1/√Δx → +∞ für Δx → 0+. Senkrechte Tangente, nicht differenzierbar.' },
  };
  let key = 'sq', dx = 1.2, x0 = 1;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], [a, b, c, d] = s.win, A = mkAx(a, b, c, d); axes(v, A, 'x', 'y');
    fplot(v, A, s.f, C.c2, 2.5, 800);
    const y0 = s.f(x0), x1 = x0 + dx, y1 = s.f(x1), m = (y1 - y0) / dx;
    const line = (mm, col, w, dash) => fplot(v, A, x => y0 + mm * (x - x0), col, w, 50);
    if (s.df) line(s.df(x0), C.c3, 1.6);
    line(m, C.c1, 2);
    v.line(A.P(x0, y0), A.P(x1, y0), C.muted, 1, [3, 3]); v.line(A.P(x1, y0), A.P(x1, y1), C.muted, 1, [3, 3]);
    v.text(A.P((x0 + x1) / 2, y0), 'Δx', C.muted, -6, dx * (y1 - y0) >= 0 ? 16 : -6, 11, false);
    v.text(A.P(x1, (y0 + y1) / 2), 'Δy', C.muted, 6, 4, 11, false);
    v.dot(A.P(x0, y0), C.fg, 6); v.text(A.P(x0, y0), 'P', C.fg, -16, -6);
    if (A.inY(y1)) { v.dot(A.P(x1, y1), C.c1, 6); v.text(A.P(x1, y1), 'Q', C.c1, 6, -6); }
    const rows = [['Δx', fmt(dx, 4)], ['Differenzenquotient', fmt(m, 5)]];
    if (s.df) rows.push(['f′(x₀)', fmt(s.df(x0), 5)]); else rows.push(['f′(x₀)', 'existiert nicht']);
    MW.info(infoEl, s.name + (s.move ? ', x₀ = ' + fmt(x0) : ''), rows, s.note, !s.df);
  });
  const sx = MW.slider(ctl, { label: 'x₀', min: -1, max: 2.5, step: 0.01, value: x0, onInput: t => { x0 = t; view.redraw(); } });
  MW.slider(ctl, { label: 'Δx', min: -1.5, max: 1.5, step: 0.001, value: dx, fmt: t => fmt(t, 3), onInput: t => { dx = Math.abs(t) < 0.001 ? (t < 0 ? -0.001 : 0.001) : t; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), t => { key = t; x0 = S[key].x0; sx.set(x0);
    sx.el.querySelector('input').disabled = !S[key].move; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 1.2
W.append(dict(file='1-2-ableitungsfunktion.html', title='Die Ableitung als Funktion: Steigung an jeder Stelle',
  sub='Oben f mit der Tangente an der Stelle x, unten die Ableitung f′. Der Punkt unten hat als Höhe genau die Steigung der Tangente oben.',
  hint='Funktion wählen, x verschieben oder abspielen.', tall=True, legend=[('--c2', 'f'), ('--c3', 'Tangente'), ('--c1', 'f′')], js=AX + ND + r'''
  const S = {
    x3: { name: 'f(x) = x³, f′(x) = 3x²', f: x => x ** 3, df: x => 3 * x * x, w: [-2, 2], y: [-4, 4], dy: [-1, 12], note: 'Produktregel mit x³ = x · x²: f′ = 1 · x² + x · 2x = 3x² (Vorlesung, S. 3).' },
    sin: { name: 'f(x) = sin x, f′(x) = cos x', f: Math.sin, df: Math.cos, w: [-6.3, 6.3], y: [-1.4, 1.4], dy: [-1.4, 1.4], note: 'Wo sin ein Maximum hat, ist cos = 0. Wo sin am steilsten steigt, ist cos = 1.' },
    tan: { name: 'f(x) = tan x, f′(x) = 1/cos²x = 1 + tan²x', f: Math.tan, df: x => 1 / Math.cos(x) ** 2, w: [-1.5, 1.5], y: [-6, 6], dy: [0, 8], note: 'Quotientenregel mit sin/cos: (cos²x + sin²x)/cos²x = 1/cos²x (Vorlesung, S. 3).' },
    inv: { name: 'f(x) = 1/x, f′(x) = −1/x²', f: x => 1 / x, df: x => -1 / (x * x), w: [-3, 3], y: [-4, 4], dy: [-6, 0.5], note: 'Quotientenregel mit f = 1, g = x: (0 · x − 1 · 1)/x² = −1/x². Überall negativ: auf jedem Ast fallend.' },
    abs: { name: 'f(x) = |x|, f′(x) = ±1', f: Math.abs, df: x => x > 0 ? 1 : x < 0 ? -1 : NaN, w: [-2, 2], y: [-0.5, 2], dy: [-1.5, 1.5], note: 'Für x ≠ 0 ist f′ = ±1. Bei 0 ist f nicht differenzierbar, f′ hat dort eine Lücke.' },
  };
  let key = 'x3', x = 1;
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1], 6, 2.2, 0, 1.55), B = mkAx(s.w[0], s.w[1], s.dy[0], s.dy[1], 6, 1.25, 0, 0);
    axes(v, A, 'x', 'f'); axes(v, B, 'x', 'f′');
    fplot(v, A, s.f, C.c2, 2.5, 1200); fplot(v, B, s.df, C.line, 1.5, 1200); fplot(v, B, s.df, C.c1, 2.5, 600, s.w[0], x);
    const y = s.f(x), m = s.df(x);
    if (isFinite(m)) fplot(v, A, t => y + m * (t - x), C.c3, 1.6, 20);
    if (A.inY(y)) v.dot(A.P(x, y), C.fg, 6);
    if (isFinite(m) && B.inY(m)) { v.dot(B.P(x, m), C.c1, 6); v.line(B.P(x, m), A.P(x, Math.max(s.y[0], Math.min(s.y[1], y))), C.muted, 1, [2, 4]); }
    MW.info(infoEl, s.name, [['x', fmt(x, 3)], ['f(x)', fmt(y, 4)], ['Steigung f′(x)', isFinite(m) ? fmt(m, 4) : 'nicht definiert'], ['Kontrolle: Differenzenquotient', isFinite(m) ? fmt(nd(s.f, x), 4) : '–']], s.note);
  });
  const sl = MW.player(ctl, { label: 'x', t0: -2, t1: 2, duration: 8, value: x, onTime: t => { x = Math.abs(t) < 1e-9 ? 1e-9 : t; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), t => { key = t; const s = S[key];
    const inp = ctl.querySelector('input[type=range]'); inp.min = s.w[0]; inp.max = s.w[1]; inp.step = (s.w[1] - s.w[0]) / 400;
    x = Math.max(s.w[0], Math.min(s.w[1], x)); inp.value = x; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 1.3
W.append(dict(file='1-3-kettenregel.html', title='Kettenregel: (f ∘ g)′(x) = f′(g(x)) · g′(x)',
  sub='Links die innere Funktion g mit Tangente in x, Mitte die äussere Funktion f mit Tangente in g(x), rechts die Verkettung h = f ∘ g. Die Steigung rechts ist das Produkt der beiden anderen Steigungen.',
  hint='Beispiel wählen, x verschieben.', legend=[('--c4', 'innere g'), ('--c5', 'äussere f'), ('--c2', 'h = f ∘ g'), ('--c3', 'Tangenten')], js=AX + ND + r'''
  const S = {
    cos3: { name: 'h(x) = cos³x:  f(u) = u³, g(x) = cos x', g: Math.cos, dg: x => -Math.sin(x), f: u => u ** 3, df: u => 3 * u * u, gx: [-0.5, 3.6], gy: [-1.2, 1.2], fu: [-1.2, 1.2], fy: [-1.2, 1.2], hy: [-1.2, 1.2],
      res: 'h′(x) = 3 cos²x · (−sin x)' },
    cotx2: { name: 'h(x) = cot(x²):  f(u) = cot u, g(x) = x²', g: x => x * x, dg: x => 2 * x, f: u => 1 / Math.tan(u), df: u => -1 / Math.sin(u) ** 2, gx: [0.3, 1.7], gy: [0, 3], fu: [0.05, 3], fy: [-4, 4], hy: [-4, 4],
      res: 'h′(x) = −1/sin²(x²) · 2x' },
    tanx2: { name: 'h(x) = tan(x²):  f(u) = tan u, g(x) = x²', g: x => x * x, dg: x => 2 * x, f: Math.tan, df: u => 1 / Math.cos(u) ** 2, gx: [-1.2, 1.2], gy: [0, 1.5], fu: [0, 1.5], fy: [0, 6], hy: [0, 6],
      res: 'h′(x) = 1/cos²(x²) · 2x  (Skript, S. 9)' },
  };
  let key = 'cos3', x = 0.8;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], h = t => s.f(s.g(t));
    const G = mkAx(s.gx[0], s.gx[1], s.gy[0], s.gy[1], 1.95, 3.2, 0, 0), F = mkAx(s.fu[0], s.fu[1], s.fy[0], s.fy[1], 1.95, 3.2, 2.3, 0), H = mkAx(s.gx[0], s.gx[1], s.hy[0], s.hy[1], 1.95, 3.2, 4.6, 0);
    axes(v, G, 'x', 'g', null, null); axes(v, F, 'u', 'f', null, null); axes(v, H, 'x', 'h', null, null);
    fplot(v, G, s.g, C.c4, 2.3, 400); fplot(v, F, s.f, C.c5, 2.3, 600); fplot(v, H, h, C.c2, 2.3, 600);
    const u = s.g(x), mg = s.dg(x), mf = s.df(u), mh = mf * mg;
    fplot(v, G, t => u + mg * (t - x), C.c3, 1.4, 10); fplot(v, F, t => s.f(u) + mf * (t - u), C.c3, 1.4, 10); fplot(v, H, t => h(x) + mh * (t - x), C.c3, 1.4, 10);
    v.dot(G.P(x, u), C.fg, 5); if (F.inY(s.f(u))) v.dot(F.P(u, s.f(u)), C.fg, 5); if (H.inY(h(x))) v.dot(H.P(x, h(x)), C.fg, 5);
    MW.info(infoEl, s.res, [['innere Ableitung g′(x)', fmt(mg, 4)], ['äussere Ableitung f′(g(x))', fmt(mf, 4)], ['Produkt', fmt(mh, 4)], ['Kontrolle: Differenzenquotient von h', fmt(nd(h, x), 4)]],
      'Zuerst wird die innere Steigung g′(x) gebildet, dann mit der äusseren Steigung an der Stelle u = g(x) multipliziert, nicht an der Stelle x.');
  });
  const sl = MW.slider(ctl, { label: 'x', min: -0.5, max: 3.6, step: 0.01, value: x, onInput: t => { x = t; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), t => { key = t; const s = S[key], inp = sl.el.querySelector('input');
    inp.min = s.gx[0]; inp.max = s.gx[1]; x = (s.gx[0] + s.gx[1]) / 2 + 0.2; sl.set(x); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 1.4
W.append(dict(file='1-4-ableitung-umkehrfunktion.html', title='Ableitung der Umkehrfunktion: Steigungen werden Kehrwerte',
  sub='Die Graphen von f und f⁻¹ sind an y = x gespiegelt. Die Spiegelung macht aus einer Tangente mit Steigung m eine mit Steigung 1/m. Darum (f⁻¹)′(b) = 1/f′(a) mit a = f⁻¹(b).',
  hint='Beispiel wählen, Punkt ziehen.', legend=[('--c2', 'f'), ('--c3', 'f⁻¹'), ('--c1', 'Tangenten'), ('--muted', 'y = x')], js=EQ + r'''
  const PI = Math.PI;
  const S = {
    exp: { name: 'f = eˣ, f⁻¹ = ln', f: Math.exp, df: Math.exp, g: Math.log, D: [-4, 1.6], a: 0.5, res: '(ln x)′ = 1/e^(ln x) = 1/x' },
    sin: { name: 'f = sin auf [−π/2, π/2], f⁻¹ = arcsin', f: Math.sin, df: Math.cos, g: Math.asin, D: [-PI / 2, PI / 2], a: 0.6, res: '(arcsin x)′ = 1/cos(arcsin x) = 1/√(1 − x²)' },
    cos: { name: 'f = cos auf [0, π], f⁻¹ = arccos', f: Math.cos, df: x => -Math.sin(x), g: Math.acos, D: [0, PI], a: 1.2, res: '(arccos x)′ = −1/sin(arccos x) = −1/√(1 − x²)' },
    tan: { name: 'f = tan auf (−π/2, π/2), f⁻¹ = arctan', f: Math.tan, df: x => 1 / Math.cos(x) ** 2, g: Math.atan, D: [-1.45, 1.45], a: 0.7, res: '(arctan x)′ = cos²(arctan x) = 1/(1 + x²)' },
    sq: { name: 'f = x² auf [0, ∞), f⁻¹ = √x', f: x => x * x, df: x => 2 * x, g: Math.sqrt, D: [0, 2.1], a: 1, res: '(√x)′ = 1/(2√x)  (Skript: x^(1/m), m = 2)' },
  };
  let key = 'exp', a = 0.5;
  const box = { xmin: -3.2, xmax: 4.6, ymin: -2.4, ymax: 4.4 };
  const view = MW.View2D(cv, box, v => {
    const C = v.C, s = S[key]; v.grid(1);
    v.line([-2.4, -2.4], [4.4, 4.4], C.muted, 1.3, [6, 4]);
    gplot(v, s.f, s.D[0], s.D[1], C.c2, 2.6, -2.4, 4.4, 800);
    gplot(v, y => s.g(y), -6, 6, C.c3, 2.6, -2.4, 4.4, 2000);
    const b = s.f(a), m = s.df(a), L = 0.9;
    const seg = (P, mm) => { const n = Math.hypot(1, mm); v.line([P[0] - L / n, P[1] - L * mm / n], [P[0] + L / n, P[1] + L * mm / n], C.c1, 2); };
    seg([a, b], m); if (Math.abs(m) > 1e-9) seg([b, a], 1 / m);
    v.line([a, b], [b, a], C.muted, 1, [2, 3]);
    v.dot([a, b], C.c2, 6); v.text([a, b], '(a, b)', C.c2, 8, -8, 12); v.dot([b, a], C.c3, 6); v.text([b, a], '(b, a)', C.c3, 8, 16, 12);
    MW.info(infoEl, s.res, [['a, b = f(a)', fmt(a, 3) + ', ' + fmt(b, 3)], ['Steigung f′(a)', fmt(m, 4)], ['Steigung (f⁻¹)′(b)', Math.abs(m) > 1e-9 ? fmt(1 / m, 4) : 'senkrecht'], ['Produkt', Math.abs(m) > 1e-9 ? '1' : '–']],
      'Herleitung (Vorlesung S. 5, Skript S. 10): f(f⁻¹(x)) = x ableiten mit der Kettenregel gibt f′(f⁻¹(x)) · (f⁻¹)′(x) = 1.');
  });
  const clampA = t => { const s = S[key]; return Math.max(s.D[0] + 1e-3, Math.min(s.D[1] - 1e-3, t)); };
  view.handle(() => [a, S[key].f(a)], p => { a = clampA(p[0]); sl.set(a); });
  const sl = MW.slider(ctl, { label: 'a', min: -4, max: 3.2, step: 0.01, value: a, onInput: t => { a = clampA(t); view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), t => { key = t; const s = S[key], inp = sl.el.querySelector('input');
    inp.min = s.D[0]; inp.max = s.D[1]; a = s.a; sl.set(a); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 2.1
W.append(dict(file='2-1-lineare-ersatzfunktion.html', title='Lineare Ersatzfunktion t(x) = f(x₀) + f′(x₀)(x − x₀)',
  sub='Oben f und ihre Tangente t in x₀, der Fehler φ(x) = f(x) − t(x) als senkrechte Strecke. Unten der Quotient φ(x)/Δx: er geht für x → x₀ gegen 0. Der Fehler wird also schneller klein als Δx.',
  hint='Funktion wählen, x₀ und x verschieben.', tall=True, legend=[('--c2', 'f'), ('--c3', 't'), ('--c1', 'Fehler φ'), ('--c5', 'φ(x)/Δx')], js=AX + r'''
  const S = {
    cos: { name: 'cos x', f: Math.cos, df: x => -Math.sin(x), x0: Math.PI / 4, w: [-1.5, 3], y: [-1.4, 1.6], free: true, note: 'Vorlesung (S. 6): bei x₀ = 0 ist t(x) = 1, bei x₀ = π/4 ist t(x) = (1/√2)(1 + π/4 − x).' },
    sin: { name: 'sin x', f: Math.sin, df: Math.cos, x0: Math.PI / 3, w: [-1.5, 3], y: [-1.4, 1.6], free: true, note: 'Skript (S. 15): bei x₀ = 0 ist t(x) = x (Pendel: mg sin φ ≈ mg φ), bei x₀ = π/3 ist t(x) = ½(x − π/3) + √3/2.' },
    ln: { name: 'ln x', f: Math.log, df: x => 1 / x, x0: 1, w: [0.05, 3.5], y: [-2.5, 1.6], free: true, note: 'Vorlesung (S. 6): bei x₀ = 1 ist t(x) = x − 1.' },
    sq: { name: '√(1 + x) bei x₀ = 0', f: x => Math.sqrt(1 + x), df: x => 0.5 / Math.sqrt(1 + x), x0: 0, w: [-0.99, 3], y: [-0.2, 2.6], free: false, note: '(1 + x)^α ≈ 1 + αx mit α = 1/2: √(1 + x) ≈ 1 + x/2 (Skript S. 17, Vorlesung S. 8–9).' },
    isq: { name: '1/√(1 + x) bei x₀ = 0', f: x => 1 / Math.sqrt(1 + x), df: x => -0.5 / (1 + x) ** 1.5, x0: 0, w: [-0.8, 3], y: [-0.6, 2.4], free: false, note: 'α = −1/2: 1/√(1 + x) ≈ 1 − x/2.' },
    inv: { name: '1/(1 + x) bei x₀ = 0', f: x => 1 / (1 + x), df: x => -1 / (1 + x) ** 2, x0: 0, w: [-0.8, 3], y: [-0.6, 3.2], free: false, note: 'α = −1: 1/(1 + x) ≈ 1 − x. Darum ist „2 % teurer“ fast dasselbe wie „vorher 2 % billiger“ (Skript S. 19).' },
  };
  let key = 'cos', x0 = Math.PI / 4, x = Math.PI / 4 + 0.9;
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1], 6, 2.25, 0, 1.5);
    axes(v, A, 'x', 'y');
    const y0 = s.f(x0), m = s.df(x0), t = u => y0 + m * (u - x0), phi = u => s.f(u) - t(u);
    fplot(v, A, s.f, C.c2, 2.5, 800); fplot(v, A, t, C.c3, 1.8, 20);
    v.dot(A.P(x0, y0), C.fg, 6); v.text(A.P(x0, y0), 'x₀', C.fg, -8, -10, 12);
    const fx = s.f(x), tx = t(x);
    v.line(A.P(x, Math.max(s.y[0], Math.min(s.y[1], tx))), A.P(x, Math.max(s.y[0], Math.min(s.y[1], fx))), C.c1, 3);
    if (A.inY(fx)) v.dot(A.P(x, fx), C.c2, 5); if (A.inY(tx)) v.dot(A.P(x, tx), C.c3, 5);
    const B = mkAx(s.w[0], s.w[1], -1, 1, 6, 1.15, 0, 0); axes(v, B, 'x', 'φ/Δx', null, 0.5);
    fplot(v, B, u => Math.abs(u - x0) < 1e-6 ? 0 : phi(u) / (u - x0), C.c5, 2.2, 800);
    v.dot(B.P(x0, 0), C.c5, 4, true);
    const q = Math.abs(x - x0) < 1e-9 ? 0 : phi(x) / (x - x0); if (B.inY(q)) v.dot(B.P(x, q), C.c5, 5);
    MW.info(infoEl, 't(x) = ' + fmt(y0, 4) + (m < 0 ? ' − ' : ' + ') + fmt(Math.abs(m), 4) + ' · (x − ' + fmt(x0, 3) + ')',
      [['Δx = x − x₀', fmt(x - x0, 4)], ['Fehler φ(x) = f(x) − t(x)', fmt(phi(x), 6)], ['φ(x)/Δx', fmt(q, 5)]], s.note);
  });
  const s0 = MW.slider(ctl, { label: 'x₀', min: -1.5, max: 3, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  const s1 = MW.slider(ctl, { label: 'x', min: -1.5, max: 3, step: 0.005, value: x, onInput: u => { x = u; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; const s = S[key];
    [s0, s1].forEach(sl => { const inp = sl.el.querySelector('input'); inp.min = s.w[0]; inp.max = s.w[1]; });
    x0 = s.x0; x = Math.min(s.w[1], x0 + 0.8); s0.set(x0); s1.set(x); s0.el.querySelector('input').disabled = !s.free; view.redraw(); }).set(key);
'''))

if __name__ == '__main__':
    print(build('analysis-w4', W))
