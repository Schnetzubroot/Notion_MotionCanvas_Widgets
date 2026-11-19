"""Widgets zu Analysis I, Woche 5: Kapitel II.2 Differentiale und Fehlerrechnung, II.3 Mittelwertsatz
(lokale Extrema, Rolle, Monotonie, Bernoulli-Hôpital), II.4 Extremalaufgaben und Anhang A Komplexe Zahlen
(Stammbach, Teil A, Kap. II S. 17-34 und Teil C, Anhang S. 3-6; Vorlesungsnotizen Kap. II S. 8-19, Kap. A S. 1-3)."""
from template import build
from build_analysis_w1 import AX, BOX
from build_analysis_w3 import EQ, TALLBOX

# Nullstellen von g auf [a, b] (Vorzeichenwechsel + Bisektion), nur für die Anzeige
ROOTS = r'''
  const nd = (f, x, h = 1e-5) => (f(x + h) - f(x - h)) / (2 * h);
  function roots(g, a, b, N = 2000) { const out = []; let px = a, py = g(a);
    if (Math.abs(py) < 1e-12) out.push(a);
    for (let i = 1; i <= N; i++) { const x = a + (b - a) * i / N, y = g(x);
      if (!isFinite(y) || !isFinite(py)) { px = x; py = y; continue; }
      if (Math.abs(y) < 1e-12) { if (!out.length || Math.abs(out[out.length - 1] - x) > 1e-6) out.push(x); }
      else if (py * y < 0) { let lo = px, hi = x; for (let k = 0; k < 60; k++) { const c = (lo + hi) / 2; if (g(lo) * g(c) <= 0) hi = c; else lo = c; }
        const r = (lo + hi) / 2; if (!out.length || Math.abs(out[out.length - 1] - r) > 1e-6) out.push(r); }
      px = x; py = y; }
    return out; }
'''

W = []

# ---------------------------------------------------------------- 2.2
W.append(dict(file='2-2-fehlerrechnung.html', title='Fehlerrechnung: Δf ≈ df = f′(x₀) · dx',
  sub='Ein Messwert x₀ hat den Fehler dx. Der exakte Fehler im Resultat ist Δf = f(x₀ + dx) − f(x₀). Das Differential df = f′(x₀) · dx liest ihn an der Tangente ab. Für kleine dx sind beide fast gleich.',
  hint='Beispiel wählen, Messwert und Messfehler verschieben.', legend=[('--c2', 'f'), ('--c3', 'Tangente (Differential)'), ('--c1', 'exakter Fehler Δf'), ('--c5', 'df')], js=AX + r'''
  const PI = Math.PI, c = 2;   // b(β) = (a/sin α) · sin β, hier mit a/sin α = 2
  const S = {
    V: { name: 'Kugelvolumen V(x) = (4π/3)(x/2)³, x = Durchmesser', f: x => 4 * PI / 3 * (x / 2) ** 3, df: x => PI / 2 * x * x, w: [0, 4], y: [-2, 36], x0: 2, var: 'x',
      rel: x => '3 · dx/x', note: 'Vorlesung S. 11, Skript S. 21–22: dV = (π/2)x² dx, dV/V = 3 · dx/x. Der relative Fehler im Volumen ist dreimal der relative Messfehler.' },
    O: { name: 'Kugeloberfläche O(x) = 4π(x/2)², x = Durchmesser', f: x => 4 * PI * (x / 2) ** 2, df: x => 2 * PI * x, w: [0, 4], y: [-2, 52], x0: 2, var: 'x',
      rel: x => '2 · dx/x', note: 'Vorlesung S. 11, Skript S. 22: dO = 2πx dx, dO/O = 2 · dx/x.' },
    b: { name: 'Dreieck: b(β) = (a/sin α) · sin β, hier a/sin α = 2', f: x => c * Math.sin(x), df: x => c * Math.cos(x), w: [0, PI], y: [-0.4, 2.6], x0: 0.5, var: 'β',
      rel: x => 'cot β · dβ', note: 'Vorlesung S. 10, Skript S. 21: db = (a/sin α) cos β dβ, db/b = cot β · dβ. Kein a, kein α. Gross für kleine β, fast 0 für β ≈ π/2.' },
  };
  let key = 'V', x0 = 2, dx = 0.4;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1]); axes(v, A, s.var, '');
    const y0 = s.f(x0), m = s.df(x0), x1 = x0 + dx, Df = s.f(x1) - y0, d = m * dx;
    fplot(v, A, s.f, C.c2, 2.5, 600); fplot(v, A, u => y0 + m * (u - x0), C.c3, 1.6, 20);
    const cl = y => Math.max(s.y[0], Math.min(s.y[1], y));
    v.line(A.P(x0, y0), A.P(x1, y0), C.muted, 1, [3, 3]);
    v.line(A.P(x1, cl(y0)), A.P(x1, cl(y0 + Df)), C.c1, 3.5);
    const s0 = v.toS(A.P(x1, cl(y0))), s1 = v.toS(A.P(x1, cl(y0 + d))), px = s0[0] + 7 * Math.sign(dx || 1);
    v.sLine([px, s0[1]], [px, s1[1]], C.c5, 3.5);
    v.dot(A.P(x0, y0), C.fg, 6); v.text(A.P(x0, y0), s.var + '₀', C.fg, -18, -8, 12);
    if (A.inY(y0 + Df)) v.dot(A.P(x1, y0 + Df), C.c2, 4.5);
    const f0 = Math.abs(y0) > 1e-12;
    MW.info(infoEl, s.name, [[s.var + '₀, d' + s.var, fmt(x0, 3) + ', ' + fmt(dx, 3)], ['exakter Fehler Δf', fmt(Df, 5)], ['Differential df = f′(' + s.var + '₀) · d' + s.var, fmt(d, 5)],
      ['relativer Fehler Δf/f', f0 ? fmt(Df / y0, 4) : '–'], ['df/f = ' + s.rel(x0), f0 ? fmt(d / y0, 4) : '–']], s.note);
  });
  const s0 = MW.slider(ctl, { label: 'Messwert', min: 0.1, max: 4, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  const s1 = MW.slider(ctl, { label: 'Messfehler', min: -0.8, max: 0.8, step: 0.005, value: dx, onInput: u => { dx = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name.split(':')[0].split(' V(')[0].split(' O(')[0]]), u => { key = u; const s = S[key], inp = s0.el.querySelector('input');
    inp.min = s.w[0] + 0.05; inp.max = s.w[1] - 0.05; x0 = s.x0; s0.set(x0); dx = key === 'b' ? 0.2 : 0.4; s1.set(dx); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 3.1
W.append(dict(file='3-1-rolle.html', title='Lokale Extrema und Satz von Rolle',
  sub='Hat eine differenzierbare Funktion an zwei Stellen x₁ < x₂ den gleichen Wert, so gibt es dazwischen ein ξ mit f′(ξ) = 0: eine waagrechte Tangente. Ohne Differenzierbarkeit kann das scheitern.',
  hint='Beispiel wählen, die Höhe c verschieben: sie legt x₁ und x₂ fest.', legend=[('--c2', 'f'), ('--c4', 'Höhe c'), ('--c1', 'ξ mit f′(ξ) = 0'), ('--c3', 'waagrechte Tangente')], js=AX + ROOTS + r'''
  const S = {
    cub: { name: 'f(x) = x³ − 3x (eigenes Beispiel)', f: x => x ** 3 - 3 * x, df: x => 3 * x * x - 3, w: [-2.3, 2.3], y: [-3.5, 3.5], c: 0.5, diff: true,
      note: 'Lokales Maximum bei x = −1, lokales Minimum bei x = 1, dort ist f′ = 0 (Satz Vorlesung S. 12, Skript S. 23).' },
    sin: { name: 'f(x) = sin x (eigenes Beispiel)', f: Math.sin, df: Math.cos, w: [-0.5, 6.8], y: [-1.4, 1.4], c: 0.3, diff: true,
      note: 'Zwischen zwei Stellen gleicher Höhe liegt immer ein Hoch- oder Tiefpunkt mit cos ξ = 0.' },
    abs: { name: 'f(x) = |x| (nicht differenzierbar bei 0)', f: Math.abs, df: x => Math.sign(x), w: [-1.5, 1.5], y: [-0.3, 1.5], c: 0.6, diff: false,
      note: 'f(x₁) = f(x₂), aber f′ ist nie 0: f′ = −1 links und +1 rechts. Bei 0 ist f nicht differenzierbar, deshalb gilt Rolle hier nicht (Skript S. 24, Bemerkung).' },
    x3: { name: 'f(x) = x³ (f′(0) = 0 ohne Extremum)', f: x => x ** 3, df: x => 3 * x * x, w: [-1.6, 1.6], y: [-3, 3], c: 0.5, diff: true,
      note: 'f′(0) = 0, aber 0 ist keine Extremalstelle (Vorlesung S. 12). Die Umkehrung des Satzes gilt nicht. Weil f streng wachsend ist, gibt es auch nie zwei Stellen gleicher Höhe.' },
  };
  let key = 'cub', c = 0.5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1]); axes(v, A, 'x', 'y');
    v.line(A.P(s.w[0], c), A.P(s.w[1], c), C.c4, 1.6, [6, 4]);
    fplot(v, A, s.f, C.c2, 2.5, 800);
    const xs = roots(x => s.f(x) - c, s.w[0], s.w[1]);
    const crit = s.diff ? roots(s.df, s.w[0], s.w[1]) : [];
    xs.forEach((x, i) => { v.dot(A.P(x, c), C.c4, 5); v.text(A.P(x, c), 'x' + '₁₂₃₄₅'[i], C.c4, -6, 18, 12); });
    const rows = [['Stellen mit f(x) = c', xs.length ? xs.map(x => fmt(x, 3)).join(', ') : 'keine']];
    const xis = [];
    for (let i = 0; i + 1 < xs.length; i++) crit.filter(t => t > xs[i] && t < xs[i + 1]).forEach(t => { if (!xis.includes(t)) xis.push(t); });
    crit.forEach(t => { const y = s.f(t), on = xis.includes(t), col = on ? C.c1 : C.muted;
      v.line(A.P(t - 0.35 * (s.w[1] - s.w[0]) / 6, y), A.P(t + 0.35 * (s.w[1] - s.w[0]) / 6, y), C.c3, 2);
      v.dot(A.P(t, y), col, on ? 6 : 4.5, !on); v.text(A.P(t, y), on ? 'ξ' : '', col, -4, y > c ? -10 : 20, 13); });
    const kind = t => { const h = 1e-3, l = s.f(t - h), r = s.f(t + h), y = s.f(t); return l < y && r < y ? 'lok. Max' : l > y && r > y ? 'lok. Min' : 'kein Extremum'; };
    rows.push(['Stellen mit f′ = 0', crit.length ? crit.map(t => fmt(t, 3) + ' (' + kind(t) + ')').join(', ') : 'keine']);
    rows.push(['ξ zwischen x₁ und x₂', xs.length >= 2 ? (xis.length ? xis.map(t => fmt(t, 3)).join(', ') : 'keines') : 'c schneidet nur ' + xs.length + '×']);
    MW.info(infoEl, s.name, rows, s.note, !s.diff && xs.length >= 2);
  });
  const sc = MW.slider(ctl, { label: 'Höhe c', min: -3.5, max: 3.5, step: 0.01, value: c, onInput: u => { c = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; const s = S[key], inp = sc.el.querySelector('input');
    inp.min = s.y[0]; inp.max = s.y[1]; c = s.c; sc.set(c); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 3.2
W.append(dict(file='3-2-mittelwertsatz.html', title='Mittelwertsatz: irgendwo ist die Tangente parallel zur Sekante',
  sub='Für f differenzierbar auf [a, b] gibt es ein ξ ∈ (a, b) mit f′(ξ) = (f(b) − f(a))/(b − a). Die Sekante lässt sich parallel verschieben, bis sie den Graphen berührt. Die Hilfsfunktion g aus dem Beweis hat g(a) = g(b).',
  hint='Beispiel wählen, a und b verschieben.', legend=[('--c2', 'f'), ('--c1', 'Sekante'), ('--c3', 'parallele Tangente(n) in ξ'), ('--c5', 'Hilfsfunktion g')], js=AX + ROOTS + r'''
  const S = {
    cub: { name: 'f(x) = x³ − 3x (eigenes Beispiel)', f: x => x ** 3 - 3 * x, df: x => 3 * x * x - 3, w: [-2.3, 2.3], y: [-3.5, 3.5], ab: [-2, 1.5], diff: true },
    exp: { name: 'f(x) = eˣ (eigenes Beispiel)', f: Math.exp, df: Math.exp, w: [-2, 2], y: [-0.5, 7.5], ab: [-1.5, 1.8], diff: true },
    sin: { name: 'f(x) = sin x (eigenes Beispiel)', f: Math.sin, df: Math.cos, w: [-0.5, 6.8], y: [-1.4, 1.4], ab: [0.3, 4], diff: true },
    abs: { name: 'f(x) = |x| auf [−1, 1] (Gegenbeispiel)', f: Math.abs, df: x => Math.sign(x), w: [-1.5, 1.5], y: [-0.4, 1.6], ab: [-1, 1], diff: false },
  };
  let key = 'cub', a = -2, b = 1.5, showG = true;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1]); axes(v, A, 'x', 'y');
    if (b - a < 1e-3) { MW.info(infoEl, s.name, [['', 'a muss kleiner als b sein']], ''); return; }
    const fa = s.f(a), fb = s.f(b), m = (fb - fa) / (b - a), g = x => s.f(x) - m * (x - a);
    v.poly([A.P(a, s.y[0]), A.P(b, s.y[0]), A.P(b, s.y[1]), A.P(a, s.y[1])], null, 1, null, true, C.fill);
    if (showG) fplot(v, A, g, C.c5, 1.6, 600, a, b);
    fplot(v, A, s.f, C.c2, 2.5, 800);
    fplot(v, A, x => fa + m * (x - a), C.c1, 2, 20);
    const xis = s.diff ? roots(x => s.df(x) - m, a, b, 4000).filter(t => t > a + 1e-6 && t < b - 1e-6) : [];
    xis.forEach(t => { const y = s.f(t); fplot(v, A, x => y + m * (x - t), C.c3, 1.6, 20); v.dot(A.P(t, y), C.c3, 6); v.text(A.P(t, y), 'ξ', C.c3, -4, -10, 13); });
    v.dot(A.P(a, fa), C.fg, 5.5); v.text(A.P(a, fa), 'a', C.fg, -14, -6, 12); v.dot(A.P(b, fb), C.fg, 5.5); v.text(A.P(b, fb), 'b', C.fg, 6, -6, 12);
    const rows = [['Sekantensteigung (f(b) − f(a))/(b − a)', fmt(m, 4)],
      ['ξ mit f′(ξ) = Sekantensteigung', xis.length ? xis.map(t => fmt(t, 4)).join(', ') : 'keines']];
    if (showG) rows.push(['g(a) = g(b)', fmt(g(a), 4) + ' = ' + fmt(g(b), 4)]);
    const note = s.diff ? 'Beweis (Vorlesung S. 14, Skript S. 25): g(x) = f(x) − ((f(b) − f(a))/(b − a))(x − a) erfüllt g(a) = g(b). Rolle liefert g′(ξ) = 0, also f′(ξ) = Sekantensteigung.'
      : 'Vorlesung S. 14: Auf [−1, 1] ist die Sekante waagrecht, aber f′ ist nur −1 oder +1. Weil f bei 0 nicht differenzierbar ist, gilt der MWS nicht.';
    MW.info(infoEl, s.name, rows, note, !s.diff && !xis.length && a < 0 && b > 0);
  });
  const sa = MW.slider(ctl, { label: 'a', min: -2.3, max: 2.3, step: 0.01, value: a, onInput: u => { a = Math.min(u, b - 0.02); view.redraw(); } });
  const sb = MW.slider(ctl, { label: 'b', min: -2.3, max: 2.3, step: 0.01, value: b, onInput: u => { b = Math.max(u, a + 0.02); view.redraw(); } });
  MW.check(ctl, 'Hilfsfunktion g', showG, t => { showG = t; view.redraw(); });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; const s = S[key];
    [sa, sb].forEach(sl => { const inp = sl.el.querySelector('input'); inp.min = s.w[0]; inp.max = s.w[1]; });
    [a, b] = s.ab; sa.set(a); sb.set(b); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 3.3
W.append(dict(file='3-3-bernoulli-hopital.html', title='Regel von Bernoulli-Hôpital: lim f/g = lim f′/g′ bei „0/0“',
  sub='Oben Zähler f und Nenner g. Unten die Quotienten f/g und f′/g′ als Funktion von x. Im Fall f(a) = g(a) = 0 laufen beide gegen denselben Grenzwert. Fehlt diese Voraussetzung, darf die Regel nicht angewendet werden.',
  hint='Beispiel wählen, x gegen a schieben.', tall=True, legend=[('--c2', 'Zähler f'), ('--c4', 'Nenner g'), ('--c1', 'f/g'), ('--c3', 'f′/g′')], js=AX + r'''
  const S = {
    sinx: { name: 'lim sin x / x für x → 0', f: Math.sin, g: x => x, df: Math.cos, dg: x => 1, a: 0, w: [-3, 3], y: [-3, 3], q: [-0.2, 1.6], L: 1, ok: true,
      note: 'Vorlesung S. 16: = lim cos x / 1 = 1. Ein zweites Mal darf man nicht ableiten: cos x / 1 ist kein Fall „0/0“.' },
    exp: { name: 'lim (eˣ − e)/ln x für x → 1', f: x => Math.exp(x) - Math.E, g: Math.log, df: Math.exp, dg: x => 1 / x, a: 1, w: [0.2, 2], y: [-2, 5], q: [0, 5], L: Math.E, ok: true,
      note: 'Vorlesung S. 16, Skript S. 27: = lim eˣ/(1/x) = e.' },
    sq: { name: 'lim (x²/2 − sin x²)/ln(1 + x²) für x → 0', f: x => x * x / 2 - Math.sin(x * x), g: x => Math.log(1 + x * x), df: x => x - 2 * x * Math.cos(x * x), dg: x => 2 * x / (1 + x * x), a: 0, w: [-1.5, 1.5], y: [-1.2, 1.2], q: [-1.2, 0.6], L: -0.5, ok: true,
      note: 'Vorlesung S. 16: f′/g′ = ((1 + x²)/2)(1 − 2cos x²) → −1/2.' },
    cos: { name: 'lim x²/(1 − cos x) für x → 0', f: x => x * x, g: x => 1 - Math.cos(x), df: x => 2 * x, dg: Math.sin, a: 0, w: [-3, 3], y: [-0.5, 4], q: [0, 4], L: 2, ok: true,
      note: 'Skript S. 27: = lim 2x/sin x. Das ist wieder „0/0“, ein zweites Mal ableiten gibt lim 2/cos x = 2.' },
    trap: { name: 'Falle: lim eˣ/x für x → 0', f: Math.exp, g: x => x, df: Math.exp, dg: x => 1, a: 0, w: [-2, 2], y: [-2.5, 4], q: [-6, 6], L: null, ok: false,
      note: 'Vorlesung S. 16: f(0) = e⁰ = 1 ≠ 0. Die Voraussetzung f(a) = g(a) = 0 fehlt. f′/g′ = eˣ → 1, aber f/g → +∞ von rechts und −∞ von links.' },
  };
  let key = 'sinx', d = 0.8;
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, s = S[key], x = s.a + d;
    const A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1], 6, 1.6, 0, 2.15); axes(v, A, 'x', '');
    fplot(v, A, s.g, C.c4, 2.2, 600); fplot(v, A, s.f, C.c2, 2.5, 600);
    v.line(A.P(s.a, s.y[0]), A.P(s.a, s.y[1]), C.muted, 1, [3, 3]);
    v.dot(A.P(s.a, s.f(s.a)), C.c2, 4.5, true); v.dot(A.P(s.a, s.g(s.a)), C.c4, 4.5, true);
    if (A.inY(s.f(x))) v.dot(A.P(x, s.f(x)), C.c2, 5); if (A.inY(s.g(x))) v.dot(A.P(x, s.g(x)), C.c4, 5);
    const B = mkAx(s.w[0], s.w[1], s.q[0], s.q[1], 6, 1.75, 0, 0); axes(v, B, 'x', 'Quotient');
    if (s.L !== null) v.line(B.P(s.w[0], s.L), B.P(s.w[1], s.L), C.muted, 1.2, [5, 4]);
    const safe = h => u => Math.abs(u - s.a) < 1e-9 ? NaN : h(u);
    fplot(v, B, safe(u => s.df(u) / s.dg(u)), C.c3, 2, 800);
    fplot(v, B, safe(u => s.f(u) / s.g(u)), C.c1, 2.4, 800);
    const q1 = s.f(x) / s.g(x), q2 = s.df(x) / s.dg(x);
    if (B.inY(q1)) v.dot(B.P(x, q1), C.c1, 5); if (B.inY(q2)) v.dot(B.P(x, q2), C.c3, 5);
    v.line(B.P(s.a, s.q[0]), B.P(s.a, s.q[1]), C.muted, 1, [3, 3]);
    MW.info(infoEl, s.name, [['f(a), g(a)', fmt(s.f(s.a), 4) + ', ' + fmt(s.g(s.a), 4)], ['x', fmt(x, 4)], ['f(x)/g(x)', Math.abs(d) < 1e-9 ? '–' : fmt(q1, 5)], ['f′(x)/g′(x)', Math.abs(d) < 1e-9 ? '–' : fmt(q2, 5)],
      ['Grenzwert', s.L === null ? 'existiert nicht' : fmt(s.L, 5)]], s.note, !s.ok);
  });
  MW.slider(ctl, { label: 'x − a', min: -1, max: 1, step: 0.002, value: d, onInput: u => { d = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 4.1
W.append(dict(file='4-1-kandidaten-extremalstellen.html', title='Globale Extrema: Kandidaten (I), (II), (III) vergleichen',
  sub='Eine lokale Extremalstelle ist (I) eine Stelle mit f′ = 0, (II) eine Stelle, an der f nicht differenzierbar ist, oder (III) ein Randpunkt. Man sammelt alle Kandidaten und vergleicht die Funktionswerte.',
  hint='Beispiel wählen. Mit „D = ℝ“ aus wird D(f) auf [a, b] eingeschränkt.', legend=[('--c2', 'f'), ('--c3', '(I) f′ = 0'), ('--c5', '(II) nicht differenzierbar'), ('--c4', '(III) Rand')], js=AX + r'''
  const S = {
    cbrt: { name: 'f(x) = (x − 1) · ∛(x²)', f: x => (x - 1) * Math.cbrt(x * x), w: [-1, 2], y: [-2.2, 1.7], I: [0.4], II: [0], ab: [-0.5, 1.5],
      note: 'Skript S. 30–32, Vorlesung S. 17–18: f′(x) = (5x − 2)/(3∛x). (I) x = 2/5, f(2/5) = −(3/5)∛(4/25) ≈ −0.326 (lokales Minimum). (II) x = 0, f(0) = 0 (lokales Maximum). (III) Für x → ±∞ geht f → ±∞: auf ℝ kein globales Extremum.' },
    x3: { name: 'f(x) = x³', f: x => x ** 3, w: [-1.5, 1.5], y: [-3.4, 3.4], I: [0], II: [], ab: [-1, 1],
      note: 'Skript S. 29: x = 0 erfüllt f′(0) = 0, ist aber keine Extremalstelle. Kandidat heisst nur „verdächtig“, nicht „Extremum“.' },
    x4: { name: 'f(x) = x⁴', f: x => x ** 4, w: [-1.5, 1.5], y: [-0.5, 4.5], I: [0], II: [], ab: [-1, 1.2],
      note: 'Skript S. 29: x = 0 ist globale Minimalstelle, aber f″(0) = 0. Die zweite Ableitung entscheidet hier nichts, der Vergleich der Werte schon.' },
  };
  let key = 'cbrt', R = true, a = -0.5, b = 1.5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(s.w[0], s.w[1], s.y[0], s.y[1]); axes(v, A, 'x', 'y');
    const lo = R ? s.w[0] : a, hi = R ? s.w[1] : b;
    if (!R) { fplot(v, A, s.f, C.grid, 2, 600); v.poly([A.P(a, s.y[0]), A.P(b, s.y[0]), A.P(b, s.y[1]), A.P(a, s.y[1])], null, 1, null, true, C.fill); }
    fplot(v, A, s.f, C.c2, 2.6, 800, lo, hi);
    const inside = t => R || (t > a && t < b);
    const K = [];
    s.I.filter(inside).forEach(t => K.push(['(I)', t, C.c3])); s.II.filter(inside).forEach(t => K.push(['(II)', t, C.c5]));
    if (!R) { K.push(['(III)', a, C.c4]); K.push(['(III)', b, C.c4]); }
    K.forEach(([lab, t, col]) => { const y = s.f(t); v.dot(A.P(t, y), col, 6); v.text(A.P(t, y), lab, col, -10, y > 0.5 * s.y[1] ? 18 : -10, 11); });
    const vals = K.map(k => s.f(k[1]));
    let gmax = '–', gmin = '–';
    if (R) { gmax = key === 'x4' ? 'keines (f → ∞)' : 'keines (f → +∞)'; gmin = key === 'x4' ? 'x = 0, f = 0' : 'keines (f → −∞)'; }
    else { const M = Math.max(...vals), m = Math.min(...vals);
      gmax = K.filter((k, i) => Math.abs(vals[i] - M) < 1e-9).map(k => 'x = ' + fmt(k[1], 3)).join(', ') + ', f = ' + fmt(M, 4);
      gmin = K.filter((k, i) => Math.abs(vals[i] - m) < 1e-9).map(k => 'x = ' + fmt(k[1], 3)).join(', ') + ', f = ' + fmt(m, 4); }
    MW.info(infoEl, s.name + (R ? ', D(f) = ℝ' : ', D(f) = [' + fmt(a, 2) + ', ' + fmt(b, 2) + ']'),
      [['Kandidaten', K.length ? K.map((k, i) => k[0] + ' x = ' + fmt(k[1], 3) + ' → f = ' + fmt(vals[i], 4)).join(';  ') : 'keine'],
       ['(III) Rand', R ? 'kein Rand, Grenzwerte x → ±∞ ansehen' : 'a, b'], ['globales Maximum', gmax], ['globales Minimum', gmin]],
      s.note + (R ? '' : ' Das eingeschränkte Intervall ist eine eigene Erweiterung (nicht aus dem Skript).'));
  });
  MW.check(ctl, 'D = ℝ', R, t => { R = t; [sa, sb].forEach(sl => sl.el.querySelector('input').disabled = R); view.redraw(); });
  const sa = MW.slider(ctl, { label: 'a', min: -1.5, max: 2, step: 0.01, value: a, onInput: u => { a = Math.min(u, b - 0.05); view.redraw(); } });
  const sb = MW.slider(ctl, { label: 'b', min: -1.5, max: 2, step: 0.01, value: b, onInput: u => { b = Math.max(u, a + 0.05); view.redraw(); } });
  [sa, sb].forEach(sl => sl.el.querySelector('input').disabled = R);
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; const s = S[key];
    [sa, sb].forEach(sl => { const inp = sl.el.querySelector('input'); inp.min = s.w[0]; inp.max = s.w[1]; });
    [a, b] = s.ab; sa.set(a); sb.set(b); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 4.2
W.append(dict(file='4-2-abstand-punkt-strecke.html', title='Extremalaufgabe: kürzester Abstand von P zur Strecke AB',
  sub='A = (−1, 1), B = (0, 2), P = (p, 0). Gesucht ist der Punkt Q = (x, x + 2) auf AB mit minimalem Abstand. Man minimiert f(x) = (p − x)² + (x + 2)² auf [−1, 0]. Welcher Kandidat gewinnt, hängt von p ab.',
  hint='p verschieben und beobachten, wann das Minimum auf den Rand springt.', tall=True, legend=[('--c2', 'Strecke AB / f(x)'), ('--c1', 'kürzeste Verbindung'), ('--c3', 'Kandidat f′ = 0'), ('--c4', 'Randpunkte')], js=AX + r'''
  let p = 1;
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, G = mkAx(-2.5, 4.5, -0.5, 2.6, 6, 1.9, 0, 1.85);
    axes(v, G, 'x', 'y', 1, 1);
    const f = x => (p - x) ** 2 + (x + 2) ** 2, xs = p / 2 - 1, inI = xs > -1 && xs < 0;
    const K = [[-1, C.c4], [0, C.c4]]; if (inI) K.push([xs, C.c3]);
    const best = K.reduce((m, k) => f(k[0]) < f(m[0]) ? k : m, K[0]), xm = best[0];
    v.line(G.P(-1, 1), G.P(0, 2), C.c2, 3);
    v.dot(G.P(-1, 1), C.fg, 4.5); v.text(G.P(-1, 1), 'A', C.fg, -16, 4, 12); v.dot(G.P(0, 2), C.fg, 4.5); v.text(G.P(0, 2), 'B', C.fg, 6, 4, 12);
    v.line(G.P(p, 0), G.P(xm, xm + 2), C.c1, 2); v.dot(G.P(xm, xm + 2), C.c1, 5.5); v.text(G.P(xm, xm + 2), 'Q', C.c1, 8, 4, 12);
    v.dot(G.P(p, 0), C.fg, 6); v.text(G.P(p, 0), 'P', C.fg, -4, -10, 12);
    const fv = [f(-1), f(0), f(xm)], fl = Math.min(...fv), fh = Math.max(...fv), pad = Math.max(0.3, 0.15 * (fh - fl));
    const H = mkAx(-1.25, 0.25, Math.max(0, fl - pad), fh + pad, 6, 1.35, 0, 0); axes(v, H, 'x', 'f(x) = |PQ|²');
    fplot(v, H, f, C.c2, 2.4, 300, -1, 0);
    K.forEach(([t, col]) => { v.dot(H.P(t, f(t)), col, t === xm ? 7 : 5, t !== xm); });
    const lage = p <= 0 ? 'p ≤ 0: x_min = −1 (Punkt A)' : p >= 2 ? 'p ≥ 2: x_min = 0 (Punkt B)' : '0 ≤ p ≤ 2: x_min = p/2 − 1';
    MW.info(infoEl, lage, [['f(−1) = p² + 2p + 2', fmt(f(-1), 4)], ['f(0) = p² + 4', fmt(f(0), 4)],
      ['f′(x) = 0 bei x = p/2 − 1', fmt(xs, 3) + (inI ? ' (in [−1, 0], f = (p + 2)²/2 = ' + fmt(f(xs), 4) + ')' : ' (ausserhalb von [−1, 0])')],
      ['Minimum', 'x = ' + fmt(xm, 3) + ', |PQ| = ' + fmt(Math.sqrt(f(xm)), 4)]],
      'Skript S. 32–34. Da f″ = 4 > 0, ist x = p/2 − 1 eine lokale Minimalstelle, sofern sie in [−1, 0] liegt.');
  });
  MW.slider(ctl, { label: 'p', min: -2, max: 4, step: 0.01, value: p, onInput: u => { p = u; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 4.3
W.append(dict(file='4-3-kreuzquerschnitt.html', title='Kreuzförmiger Querschnitt im Kreis: maximale Fläche',
  sub='Ein Kreuz aus zwei Rechtecken wird in einen Kreis vom Radius r gelegt. Mit x = r cos α, y = r sin α ist A(α) = 4r²(sin 2α − sin²α) auf [0, π/4]. Das globale Maximum liegt bei tan 2α = 2.',
  hint='α verschieben und die Fläche rechts verfolgen.', legend=[('--c2', 'Kreuz'), ('--muted', 'Kreis vom Radius r'), ('--c1', 'A(α)/r²'), ('--c3', 'Maximum')], js=AX + r'''
  const D = Math.PI / 180, aMax = Math.atan(2) / 2, Af = t => 4 * (Math.sin(2 * t) - Math.sin(t) ** 2);
  let al = 20 * D;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, cx = 1.45, cy = 1.55, R = 1.45, x = R * Math.cos(al), y = R * Math.sin(al);
    v.circle([cx, cy], R, C.muted, 1.5);
    const rect = (w, h) => [[cx - w, cy - h], [cx + w, cy - h], [cx + w, cy + h], [cx - w, cy + h]];
    v.poly(rect(x, y), C.c2, 1.5, null, true, C.fill); v.poly(rect(y, x), C.c2, 1.5, null, true, C.fill);
    v.poly([[cx - y, cy - y], [cx + y, cy - y], [cx + y, cy + y], [cx - y, cy + y]], C.c2, 1.5, null, true, C.fill);
    v.line([cx, cy], [cx + x, cy + y], C.fg, 1.2); v.arc([cx, cy], 0.35, 0, al, C.fg, 1.2);
    v.text([cx + 0.35, cy], 'α', C.fg, 4, -4, 12); v.text([cx + x, cy + y], 'r', C.fg, 4, -4, 12);
    v.line([cx + y, cy], [cx + x, cy], C.c1, 1.2, [3, 3]); v.text([cx + (x + y) / 2, cy], 'x − y', C.c1, 0, 14, 11, false, 'center');
    v.line([cx + x, cy], [cx + x, cy + y], C.c1, 1.2, [3, 3]); v.text([cx + x, cy + y / 2], 'y', C.c1, -10, 4, 11, false);
    const A = mkAx(0, 45, 0, 2.8, 2.9, 3.2, 3.25, 0.15); axes(v, A, 'α in °', 'A/r²', 15, 0.5);
    fplot(v, A, t => Af(t * D), C.c1, 2.4, 300);
    v.dot(A.P(aMax / D, Af(aMax)), C.c3, 6, true); v.dot(A.P(al / D, Af(al)), C.c1, 6);
    const a = Af(al);
    MW.info(infoEl, 'α = ' + fmt(al / D, 3) + '°, A = ' + fmt(a, 4) + ' r²', [['x = r cos α, y = r sin α', fmt(Math.cos(al), 3) + ' r, ' + fmt(Math.sin(al), 3) + ' r'],
      ['Füllfaktor A/(πr²)', fmt(100 * a / Math.PI, 3) + ' %'], ['Maximum', 'α = arctan(2)/2 ≈ ' + fmt(aMax / D, 3) + '°, A ≈ ' + fmt(Af(aMax), 3) + ' r²'],
      ['Rand', 'A(0) = 0, A(π/4) = 2r²']],
      'Vorlesung S. 18–19, Skript S. 29–30: A = 4y(2x − y), A′(α) = 4r²(2cos 2α − sin 2α) = 0 ⇔ tan 2α = 2. Im Maximum x ≈ 0.851 r, y ≈ 0.526 r, Füllfaktor 78.7 %.');
  });
  MW.slider(ctl, { label: 'α', min: 0, max: 45, step: 0.1, value: 20, fmt: u => fmt(u, 3) + '°', onInput: u => { al = u * D; view.redraw(); } });
'''))

# ---------------------------------------------------------------- A.1
W.append(dict(file='A-1-komplexe-ebene.html', title='Komplexe Zahlen in der Ebene: +, ·, Konjugation, 1/z, z/w',
  sub='z = a + ib ist der Punkt (a, b). Addition ist Vektoraddition. Konjugation spiegelt an der reellen Achse. Für z ≠ 0 ist 1/z = z̄/|z|²: gleiche Richtung wie z̄, Betrag 1/|z|.',
  hint='Rechenart wählen, z und w ziehen.', legend=[('--c2', 'z'), ('--c4', 'w'), ('--c1', 'Resultat'), ('--muted', 'Einheitskreis')], js=r'''
  const cm = (p, q) => [p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0]], ab2 = p => p[0] * p[0] + p[1] * p[1];
  const inv = p => [p[0] / ab2(p), -p[1] / ab2(p)], cj = p => [p[0], -p[1]];
  const cs = p => { const r = x => Math.round(x * 1000) / 1000; const a = r(p[0]), b = r(p[1]); return (a === 0 && b !== 0 ? '' : fmt(a, 4)) + (b === 0 ? (a === 0 ? '0' : '') : (b < 0 ? (a === 0 ? '−' : ' − ') : (a === 0 ? '' : ' + ')) + (Math.abs(b) === 1 ? '' : fmt(Math.abs(b), 4)) + 'i'); };
  const arg = p => Math.atan2(p[1], p[0]) / Math.PI * 180;
  const OP = {
    add: { name: 'z + w', two: true, f: (z, w) => [z[0] + w[0], z[1] + w[1]], note: 'Skript (1.1), S. 3: Real- und Imaginärteile werden addiert, wie bei Vektoren.' },
    mul: { name: 'z · w', two: true, f: cm, note: 'Skript (1.2), S. 3: (aa′ − bb′) + i(ab′ + a′b). Beträge werden multipliziert, Winkel addiert (Skript S. 5). Vorlesung S. 1: (5 + 3i)(4 − 8i) = 44 − 28i.' },
    conj: { name: 'z̄', two: false, f: z => cj(z), note: 'Spiegelung an der reellen Achse. Re z = (z + z̄)/2 und z · z̄ = |z|² (Vorlesung S. 1, Skript S. 6).' },
    inv: { name: '1/z', two: false, f: z => inv(z), note: 'Vorlesung S. 2–3: 1/z = z̄/|z|². Liegt z ausserhalb des Einheitskreises, liegt 1/z innerhalb. Ist Im z > 0, so ist Im(1/z) < 0.' },
    div: { name: 'z / w', two: true, f: (z, w) => cm(z, inv(w)), note: 'Erweitern mit w̄ (Vorlesung S. 2): (3 + 2i)/(4 − i) = (3 + 2i)(4 + i)/17 = (10 + 11i)/17.' },
  };
  let op = 'div', z = [3, 2], w = [4, -1];
  const view = MW.View2D(cv, { xmin: -5.6, xmax: 5.6, ymin: -3.3, ymax: 3.3, xlabel: 'Re', ylabel: 'Im' }, v => {
    const C = v.C, o = OP[op]; v.grid(1); v.circle([0, 0], 1, C.muted, 1.4, [5, 4]);
    const r = ab2(z) > 1e-12 && (op !== 'div' || ab2(w) > 1e-12) ? o.f(z, w) : null;
    if (op === 'add' && r) { v.line(z, r, C.c4, 1, [3, 3]); v.line(w, r, C.c2, 1, [3, 3]); }
    if (op === 'inv' || op === 'conj') { v.line([0, 0], cj(z), C.muted, 1, [2, 3]); v.dot(cj(z), C.muted, 4, true); v.text(cj(z), 'z̄', C.muted, 6, 14, 12); }
    v.arrow([0, 0], z, C.c2, 2.2, 9); v.dot(z, C.c2, 6); v.text(z, 'z', C.c2, 8, -6, 13);
    if (o.two) { v.arrow([0, 0], w, C.c4, 2.2, 9); v.dot(w, C.c4, 6); v.text(w, 'w', C.c4, 8, -6, 13); }
    if (r) { v.arrow([0, 0], r, C.c1, 2.6, 10); v.text(r, o.name, C.c1, 8, 16, 13); }
    const rows = [['z', cs(z) + ',  |z| = ' + fmt(Math.sqrt(ab2(z)), 4) + ',  arg = ' + fmt(arg(z), 4) + '°']];
    if (o.two) rows.push(['w', cs(w) + ',  |w| = ' + fmt(Math.sqrt(ab2(w)), 4) + ',  arg = ' + fmt(arg(w), 4) + '°']);
    rows.push([o.name, r ? cs(r) + ',  |·| = ' + fmt(Math.sqrt(ab2(r)), 4) + ',  arg = ' + fmt(arg(r), 4) + '°' : 'nicht definiert (Division durch 0)']);
    MW.info(infoEl, o.name + (r ? ' = ' + cs(r) : ''), rows, o.note, !r);
  });
  const snap = p => [Math.round(p[0] * 4) / 4, Math.round(p[1] * 4) / 4];
  view.handle(() => z, p => { z = snap(p); });
  view.handle(() => OP[op].two ? w : [99, 99], p => { w = snap(p); });
  MW.select(ctl, 'Rechenart', Object.entries(OP).map(([k, o]) => [k, o.name]), u => { op = u;
    if (op === 'inv') z = [1, 3]; else if (op === 'div') { z = [3, 2]; w = [4, -1]; } else if (op === 'mul') { z = [1, 1]; w = [1, 2]; } else if (op === 'add') { z = [2, 1]; w = [-1, 2]; } else z = [2, 1.5];
    view.redraw(); }).set(op);
'''))

if __name__ == '__main__':
    print(build('analysis-w5', W))
