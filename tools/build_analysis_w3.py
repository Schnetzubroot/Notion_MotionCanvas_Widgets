"""Widgets zu Analysis I, Woche 3: Kapitel I.4 Zwischenwertsatz, I.5 Koordinatentransformationen,
I.6 Die inverse Funktion, I.7 Asymptoten (Stammbach, Teil A, S. 34-61; Vorlesungsnotizen Kap. I, S. 18-27)."""
from template import build
from build_analysis_w1 import AX, BOX

# Graph in einer View2D mit gleicher Skalierung: unterbricht ausserhalb [ylo, yhi] und bei NaN
EQ = r'''
  function gplot(v, f, a, b, color, w = 2.2, ylo = -1e9, yhi = 1e9, N = 600, dash) {
    let seg = [];
    const flush = () => { if (seg.length > 1) v.poly(seg, color, w, dash); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x);
      if (!isFinite(y) || y < ylo || y > yhi) { flush(); continue; } seg.push([x, y]); }
    flush();
  }
'''
TALLBOX = '{ xmin: -0.75, xmax: 6.25, ymin: -0.45, ymax: 3.75 }'

W = []

# ---------------------------------------------------------------- 4.1
W.append(dict(file='4-1-zwischenwertsatz.html', title='Zwischenwertsatz: jeder Wert zwischen f(a) und f(b) wird angenommen',
  sub='f stetig auf [a, b], m zwischen f(a) und f(b). Dann gibt es (mindestens) ein ξ ∈ [a, b] mit f(ξ) = m. Welches ξ, sagt der Satz nicht. Ohne Stetigkeit kann die Aussage falsch sein.',
  hint='Funktion wählen, m verschieben.', legend=[('--c2', 'Graph von f auf [a, b]'), ('--c4', 'Werte zwischen f(a) und f(b)'), ('--c1', 'Stellen ξ mit f(ξ) = m')], js=AX + r'''
  const S = {
    cub: { name: 'f(x) = 2x³ − 3x² − 6x + 6 auf [−2, 3]', f: x => 2 * x ** 3 - 3 * x * x - 6 * x + 6, a: -2, b: 3, y: [-12, 17], cont: true,
      note: 'Für m zwischen etwa −1 und 9.5 gibt es drei Stellen ξ. Der Satz garantiert nur eine.' },
    cos: { name: 'f(x) = x² − cos x auf [0, π/2]', f: x => x * x - Math.cos(x), a: 0, b: Math.PI / 2, y: [-1.3, 2.8], cont: true,
      note: 'Vorlesung: f(0) = −1 < 0 < π²/4 = f(π/2). Also gibt es ein ξ mit ξ² = cos ξ.' },
    exp: { name: 'f(x) = x − e^(−x) auf [0, 1]', f: x => x - Math.exp(-x), a: 0, b: 1, y: [-1.2, 0.9], cont: true,
      note: 'Skript: f(0) = −1, f(1) = 1 − 1/e ≈ 0.63. Mit m = 0 folgt: x = e^(−x) hat eine Lösung in [0, 1].' },
    jump: { name: 'Sprungfunktion: x für x < 1, x + 1 für x ≥ 1, auf [0, 2]', f: x => x < 1 ? x : x + 1, a: 0, b: 2, y: [-0.4, 3.4], cont: false,
      note: 'Eigenes Gegenbeispiel (nicht aus dem Skript): f ist bei x = 1 nicht stetig. Werte m in [1, 2) werden übersprungen.' },
  };
  let key = 'cos', m = 0;
  const roots = (s, m) => { const out = [], N = 4000; let px = s.a, py = s.f(s.a) - m; if (Math.abs(py) < 1e-12) out.push(px);
    for (let i = 1; i <= N; i++) { const x = s.a + (s.b - s.a) * i / N, y = s.f(x) - m;
      if (Math.abs(y) < 1e-12) out.push(x); else if (py * y < 0 && Math.abs(y - py) < 0.5 * (s.y[1] - s.y[0])) { let lo = px, hi = x;
        for (let k = 0; k < 60; k++) { const c = (lo + hi) / 2; if ((s.f(lo) - m) * (s.f(c) - m) <= 0) hi = c; else lo = c; } out.push((lo + hi) / 2); }
      px = x; py = y; }
    return out; };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], pad = 0.08 * (s.b - s.a), A = mkAx(s.a - pad, s.b + pad, s.y[0], s.y[1]); axes(v, A, 'x', 'y');
    const fa = s.f(s.a), fb = s.f(s.b), lo = Math.min(fa, fb), hi = Math.max(fa, fb);
    v.poly([A.P(s.a, lo), A.P(s.b, lo), A.P(s.b, hi), A.P(s.a, hi)], null, 1, null, true, 'rgba(216,154,0,0.10)');
    v.line(A.P(A.x0, lo), A.P(A.x0, hi), C.c4, 6);
    if (s.cont) fplot(v, A, s.f, C.c2, 2.5, 800, s.a, s.b);
    else { fplot(v, A, s.f, C.c2, 2.5, 400, s.a, 1 - 1e-9); fplot(v, A, s.f, C.c2, 2.5, 400, 1, s.b); v.dot(A.P(1, 1), C.c2, 5, true); v.dot(A.P(1, 2), C.c2, 5); }
    v.dot(A.P(s.a, fa), C.fg, 5); v.text(A.P(s.a, fa), 'f(a)', C.fg, 6, fa < 0 ? 16 : -8, 12);
    v.dot(A.P(s.b, fb), C.fg, 5); v.text(A.P(s.b, fb), 'f(b)', C.fg, -34, fb < 0 ? 16 : -8, 12);
    [s.a, s.b].forEach(x => v.line(A.P(x, s.y[0]), A.P(x, s.y[1]), C.muted, 1, [3, 3]));
    v.line(A.P(A.x0, m), A.P(A.x1, m), C.c1, 1.5, [6, 4]); v.text(A.P(A.x1, m), 'y = m', C.c1, -50, -6, 12);
    const between = m >= lo - 1e-12 && m <= hi + 1e-12, R = roots(s, m);
    R.forEach(x => { v.line(A.P(x, m), A.P(x, A.inY(0) ? 0 : s.y[0]), C.c1, 1, [2, 3]); v.dot(A.P(x, m), C.c1, 6); });
    MW.info(infoEl, !between ? 'm liegt nicht zwischen f(a) und f(b): Satz macht keine Aussage'
      : R.length ? R.length + ' Stelle' + (R.length > 1 ? 'n' : '') + ' ξ mit f(ξ) = m' : 'Keine Stelle ξ: der Wert m wird übersprungen',
      [['f(a)', fmt(fa, 4)], ['f(b)', fmt(fb, 4)], ['m', fmt(m, 3)], ['ξ', R.length ? R.map(x => fmt(x, 4)).join(', ') : '–']],
      s.note, between && !R.length);
  });
  const sl = MW.slider(ctl, { label: 'm', min: -12, max: 17, step: 0.01, value: m, onInput: x => { m = x; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; const s = S[key];
    m = key === 'jump' ? 1.5 : key === 'cub' ? 2 : 0; rng(); view.redraw(); }).set(key);
  function rng() { const s = S[key], inp = ctl.querySelector('input[type=range]'); inp.min = s.y[0]; inp.max = s.y[1]; sl.set(m); }
  rng();
'''))

W.append(dict(file='4-1-bisektion.html', title='Beweisidee als Verfahren: Intervallhalbierung (Bisektion)',
  sub='x₁ = a, y₁ = b. Mitte c = ½(x<sub>i</sub> + y<sub>i</sub>): ist f(c) ≥ m, wird c das neue y, sonst das neue x. Die Intervalle halbieren sich, x<sub>n</sub> wächst, y<sub>n</sub> fällt, beide konvergieren gegen dasselbe ξ.',
  hint='Schritt i erhöhen.', tall=True, legend=[('--c2', 'Graph von f'), ('--c3', 'x_i'), ('--c4', 'y_i'), ('--c1', 'Intervall [x_i, y_i]')], js=AX + r'''
  const S = {
    exp: { name: 'x = e^(−x): f(x) = x − e^(−x) auf [0, 1]', f: x => x - Math.exp(-x), a: 0, b: 1, y: [-1.1, 0.75] },
    cos: { name: 'x² = cos x: f(x) = x² − cos x auf [0, π/2]', f: x => x * x - Math.cos(x), a: 0, b: Math.PI / 2, y: [-1.1, 2.6] },
  };
  let key = 'exp', n = 4;
  const seq = s => { const X = [s.a], Y = [s.b]; for (let i = 1; i < 20; i++) { const c = (X[i - 1] + Y[i - 1]) / 2;
    if (s.f(c) >= 0) { X.push(X[i - 1]); Y.push(c); } else { X.push(c); Y.push(Y[i - 1]); } } return [X, Y]; };
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, s = S[key], [X, Y] = seq(s), A = mkAx(s.a, s.b, s.y[0], s.y[1], 6, 2.15, 0, 1.55); axes(v, A, 'x', 'f(x)');
    fplot(v, A, s.f, C.c2, 2.5, 600);
    const xi = X[n - 1], yi = Y[n - 1];
    v.poly([A.P(xi, s.y[0]), A.P(yi, s.y[0]), A.P(yi, s.y[1]), A.P(xi, s.y[1])], null, 1, null, true, 'rgba(209,69,59,0.10)');
    v.dot(A.P(xi, s.f(xi)), C.c3, 6); v.dot(A.P(yi, s.f(yi)), C.c4, 6);
    // Intervall-Leiter
    const B = mkAx(s.a, s.b, 0, 1, 6, 1.3, 0, 0);
    v.text(B.P(s.a, 0), 'Intervalle [x_i, y_i], i = 1 … ' + n, C.muted, 0, 14, 11, false);
    for (let i = 1; i <= n; i++) { const yy = 1.02 - i / 21; v.line(B.P(X[i - 1], yy), B.P(Y[i - 1], yy), i === n ? C.c1 : C.line, i === n ? 4 : 3);
      v.dot(B.P(X[i - 1], yy), C.c3, 2.5); v.dot(B.P(Y[i - 1], yy), C.c4, 2.5); }
    const rows = []; for (let i = Math.max(1, n - 4); i <= n; i++) rows.push(['i = ' + i, 'x = ' + X[i - 1].toFixed(10) + ',  y = ' + Y[i - 1].toFixed(10)]);
    MW.info(infoEl, 'y_i − x_i = (b − a)/2^(i−1) = ' + ((s.b - s.a) / 2 ** (n - 1)).toExponential(2), rows,
      key === 'exp' ? 'Gleiche Werte wie die Tabelle im Skript (Teil A, S. 35). Grenzwert ξ ≈ 0.56714.' : 'Beispiel aus der Vorlesung (Notizen Kap. I, S. 19). Der Satz liefert nur die Existenz, das Verfahren eine Näherung.');
  });
  MW.select(ctl, 'Gleichung', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'i', min: 1, max: 20, step: 1, value: n, fmt: x => String(x), onInput: x => { n = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 5.1
W.append(dict(file='5-1-transformationen.html', title='Die sechs grundlegenden Koordinatentransformationen',
  sub='(1) f(x − a): Verschiebung in x. (2) f(x) + b: Verschiebung in y. (3) f(cx): Stauchen/Strecken in x. (4) d·f(x): Strecken in y. (5) 1/f(x): Null- und Polstellen tauschen. (6) f(1/x): Inneres und Äusseres von [−1, 1] tauschen.',
  hint='Grundfunktion und Transformation wählen, Parameter ändern.', legend=[('--line', 'f (Original)'), ('--c2', 'transformierte Funktion')], js=AX + r'''
  const F = {
    cub: { name: 'f(x) = 2x³ − 3x² − 6x + 6 (Skript)', f: x => 2 * x ** 3 - 3 * x * x - 6 * x + 6, y: [-30, 30] },
    cos: { name: 'f(x) = cos x', f: Math.cos, y: [-3, 3] },
    exp: { name: 'f(x) = 2^x', f: x => Math.pow(2, x), y: [-3, 6] },
  };
  const T = {
    1: { name: '(1) f(x − a)', p: ['a', -3, 3, 2], g: (f, p) => x => f(x - p), d: p => 'Verschiebung um ' + fmt(p) + ' entlang der x-Achse (' + (p >= 0 ? 'nach rechts' : 'nach links') + ').' },
    2: { name: '(2) f(x) + b', p: ['b', -10, 10, 4], g: (f, p) => x => f(x) + p, d: p => 'Verschiebung um ' + fmt(p) + ' entlang der y-Achse.' },
    3: { name: '(3) f(c · x)', p: ['c', -3, 3, 2], g: (f, p) => x => f(p * x), d: p => (Math.abs(p) > 1 ? 'Stauchung' : 'Streckung') + ' um den Faktor |c| = ' + fmt(Math.abs(p)) + ' entlang der x-Achse' + (p < 0 ? ', dazu Spiegelung an der y-Achse.' : '.') },
    4: { name: '(4) d · f(x)', p: ['d', -3, 3, 2], g: (f, p) => x => p * f(x), d: p => 'Streckung um den Faktor |d| = ' + fmt(Math.abs(p)) + ' entlang der y-Achse' + (p < 0 ? ', dazu Spiegelung an der x-Achse.' : '.') },
    5: { name: '(5) 1 / f(x)', p: null, g: f => x => 1 / f(x), d: () => 'Wo f Nullstellen hat, hat 1/f Pole. |f| < 1 wird zu |1/f| > 1 und umgekehrt.' },
    6: { name: '(6) f(1/x)', p: null, g: f => x => f(1 / x), d: () => 'Das Verhalten von f für |x| > 1 erscheint in −1 < x < 1 und umgekehrt. Für x → ±∞ geht f(1/x) → f(0).' },
  };
  let fk = 'cub', tk = '1', p = 2;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, b = F[fk], t = T[tk], yr = tk === '5' ? [-3, 3] : tk === '2' && fk !== 'cub' ? [b.y[0] - 3, b.y[1] + 3] : b.y;
    const A = mkAx(-4, 4, yr[0], yr[1]); axes(v, A, 'x', 'y', 1);
    const pp = t.p && tk === '3' && Math.abs(p) < 0.05 ? 0.05 : p;
    fplot(v, A, b.f, C.line, 2, 800);
    const g = t.g(b.f, pp); fplot(v, A, g, C.c2, 2.6, 2000);
    if (tk === '6') [-1, 1].forEach(x => v.line(A.P(x, yr[0]), A.P(x, yr[1]), C.muted, 1, [3, 3]));
    if (tk === '5') [-1, 1].forEach(y => v.line(A.P(-4, y), A.P(4, y), C.muted, 1, [3, 3]));
    MW.info(infoEl, t.name + (t.p ? ' mit ' + t.p[0] + ' = ' + fmt(pp) : ''), [['Grundfunktion', b.name], ['Wirkung', t.d(pp)]],
      tk === '1' ? 'Vorlesung: f(x − a) schiebt um a nach rechts. Das Skript schreibt f(x + a) und schiebt um a nach links: dieselbe Aussage mit −a.' :
      tk === '6' && fk === 'cub' ? 'Skript: lim_{x→∞} f(1/x) = lim_{ξ→0+} f(ξ) = 6.' : '');
  });
  const ps = MW.slider(ctl, { label: 'Parameter', min: -3, max: 3, step: 0.05, value: p, onInput: x => { p = x; view.redraw(); } });
  MW.select(ctl, 'Grundfunktion', Object.entries(F).map(([k, s]) => [k, s.name]), x => { fk = x; view.redraw(); }).set(fk);
  MW.select(ctl, 'Transformation', Object.entries(T).map(([k, s]) => [k, s.name]), x => { tk = x; const t = T[tk];
    if (t.p) p = t.p[3]; setRange(); view.redraw(); }).set(tk);
  function setRange() { const t = T[tk], inp = ctl.querySelector('input[type=range]'); if (!t.p) { inp.disabled = true; return; }
    inp.disabled = false; inp.min = t.p[1]; inp.max = t.p[2]; ps.set(p); }
  setRange();
'''))

# ---------------------------------------------------------------- 5.2
W.append(dict(file='5-2-schrittweise-skizzieren.html', title='Graphen schrittweise aus bekannten Graphen aufbauen',
  sub='Eine kompliziertere Funktion als Kette der sechs Grundtransformationen lesen und den Graphen Schritt für Schritt entstehen lassen. Hellgrau: vorheriger Schritt.',
  hint='Beispiel wählen, Schritt erhöhen.', legend=[('--line', 'vorheriger Schritt'), ('--c2', 'aktueller Schritt')], js=AX + r'''
  const E = {
    rat: { name: 'f(x) = 3/((x + 5)(x − 2))  (Skript)', win: [-8, 5, -3, 3], steps: [
      ['p(x) = (x + 5)(x − 2)', x => (x + 5) * (x - 2), 'Parabel, nach oben offen, Nullstellen −5 und 2, Scheitel bei x = −3/2.'],
      ['1/p(x)', x => 1 / ((x + 5) * (x - 2)), 'Transformation (5): Nullstellen von p werden Pole, der Scheitel wird zum Hochpunkt.'],
      ['3/p(x)', x => 3 / ((x + 5) * (x - 2)), 'Transformation (4) mit d = 3: Streckung in y-Richtung. Lage der Extremalstelle (x = −3/2) bleibt.']] },
    cos: { name: 'g(x) = 2 cos(3x + 1/2)  (Skript)', win: [-1, 4, -2.6, 2.6], steps: [
      ['cos x', Math.cos, 'Ausgangsgraph.'],
      ['cos(3x)', x => Math.cos(3 * x), 'Transformation (3) mit c = 3: Stauchung in x-Richtung, Periode 2π/3.'],
      ['cos(3x + 1/2) = cos(3(x + 1/6))', x => Math.cos(3 * x + 0.5), 'Transformation (1): Verschiebung um 1/6 nach links.'],
      ['2 cos(3x + 1/2)', x => 2 * Math.cos(3 * x + 0.5), 'Transformation (4) mit d = 2: Amplitude 2.']] },
    tan: { name: 'f(x) = (1/3) tan(2x − π/2) + 2  (Vorlesung)', win: [-3.2, 3.2, -3, 5], steps: [
      ['tan x', Math.tan, 'Ausgangsgraph, Pole bei ±π/2.'],
      ['tan(2x)', x => Math.tan(2 * x), 'Transformation (3) mit c = 2: Periode π/2.'],
      ['tan(2x − π/2) = tan(2(x − π/4))', x => Math.tan(2 * x - Math.PI / 2), 'Transformation (1): Verschiebung um π/4 nach rechts.'],
      ['(1/3) tan(2x − π/2)', x => Math.tan(2 * x - Math.PI / 2) / 3, 'Transformation (4) mit d = 1/3: Stauchung in y-Richtung.'],
      ['(1/3) tan(2x − π/2) + 2', x => Math.tan(2 * x - Math.PI / 2) / 3 + 2, 'Transformation (2) mit b = 2: Verschiebung nach oben.']] },
  };
  let key = 'rat', k = 0;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, e = E[key], [x0, x1, y0, y1] = e.win, A = mkAx(x0, x1, y0, y1); axes(v, A, 'x', 'y');
    if (k > 0) fplot(v, A, e.steps[k - 1][1], C.line, 2, 2000);
    fplot(v, A, e.steps[k][1], C.c2, 2.6, 2000);
    MW.info(infoEl, 'Schritt ' + (k + 1) + ' von ' + e.steps.length + ': ' + e.steps[k][0], [], e.steps[k][2]);
  });
  const sl = MW.slider(ctl, { label: 'Schritt', min: 0, max: 2, step: 1, value: 0, fmt: x => String(x + 1), onInput: x => { k = x; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(E).map(([k, s]) => [k, s.name]), x => { key = x; k = 0;
    const inp = ctl.querySelector('input[type=range]'); inp.max = E[key].steps.length - 1; sl.set(0); view.redraw(); }).set(key);
'''))

W.append(dict(file='5-2-schwingung.html', title='Harmonische Schwingung t → A cos(ωt + φ)',
  sub='A > 0 Amplitude, ω > 0 Kreisfrequenz, T = 2π/ω Schwingungsdauer, ν = 1/T = ω/2π Frequenz, φ ∈ (−π, π) Nullphasenwinkel. Hellgrau: cos t.',
  hint='A, ω und φ ändern.', legend=[('--line', 'cos t'), ('--c2', 'A cos(ωt + φ)'), ('--c4', 'Periode T'), ('--c1', 'Amplitude A')], js=AX + r'''
  let Am = 2, w = 3, ph = 0.5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A = mkAx(-1, 7, -3.3, 3.3); axes(v, A, 't', 'y', 1, 1);
    fplot(v, A, Math.cos, C.line, 1.6, 800);
    const f = t => Am * Math.cos(w * t + ph); fplot(v, A, f, C.c2, 2.6, 1500);
    const T = 2 * Math.PI / w, t0 = -ph / w; // Maximum bei t0
    v.dot(A.P(t0, Am), C.c1, 5); v.line(A.P(t0, 0), A.P(t0, Am), C.c1, 2); v.text(A.P(t0, Am / 2), 'A', C.c1, 6, 4, 12);
    if (t0 + T < 7) { v.line(A.P(t0, -3.0), A.P(t0 + T, -3.0), C.c4, 3); v.text(A.P(t0 + T / 2, -3.0), 'T', C.c4, -4, -6, 12); v.dot(A.P(t0 + T, Am), C.c1, 4, true); }
    MW.info(infoEl, 'y(t) = ' + fmt(Am) + ' cos(' + fmt(w) + ' t ' + (ph < 0 ? '− ' : '+ ') + fmt(Math.abs(ph)) + ')',
      [['Schwingungsdauer T = 2π/ω', fmt(T, 3)], ['Frequenz ν = ω/2π', fmt(1 / T, 3)], ['erstes Maximum bei t = −φ/ω', fmt(t0, 3)]],
      'Als Kette: cos t → cos(ωt) (Transformation 3) → cos(ω(t + φ/ω)) (Transformation 1) → A · … (Transformation 4).');
  });
  MW.slider(ctl, { label: 'A', min: 0.5, max: 3, step: 0.1, value: Am, onInput: x => { Am = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω', min: 0.5, max: 6, step: 0.1, value: w, onInput: x => { w = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: -3.1, max: 3.1, step: 0.05, value: ph, onInput: x => { ph = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 6.1
W.append(dict(file='6-1-injektiv-surjektiv.html', title='Injektiv, surjektiv, bijektiv: der Horizontalen-Test',
  sub='Injektiv: jede Horizontale schneidet Γ(f) höchstens einmal. Surjektiv auf B: jede Horizontale auf Höhe y ∈ B schneidet mindestens einmal (W(f) = B). Bijektiv: genau einmal, dann gibt es f<sup>−1</sup>.',
  hint='Funktion wählen, Höhe y verschieben.', legend=[('--c2', 'Γ(f)'), ('--c4', 'Zielbereich B'), ('--c3', 'Wertebereich W(f)'), ('--c1', 'Schnittpunkte')], js=AX + r'''
  const I = Infinity, PI = Math.PI;
  const S = {
    sqR: { name: 'x² mit D = ℝ, B = ℝ', f: x => x * x, D: [-I, I], B: [-I, I], Wf: [0, I], win: [-3, 3, -2, 6], inj: false, sur: false, Dt: 'ℝ', Bt: 'ℝ', Wt: '[0, ∞)' },
    sqP: { name: 'x² mit D = [0, ∞), B = [0, ∞)', f: x => x * x, D: [0, I], B: [0, I], Wf: [0, I], win: [-3, 3, -2, 6], inj: true, sur: true, Dt: '[0, ∞)', Bt: '[0, ∞)', Wt: '[0, ∞)' },
    sinR: { name: 'sin x mit D = ℝ, B = ℝ', f: Math.sin, D: [-I, I], B: [-I, I], Wf: [-1, 1], win: [-7, 7, -2, 2], inj: false, sur: false, Dt: 'ℝ', Bt: 'ℝ', Wt: '[−1, 1]' },
    sinE: { name: 'sin x mit D = [−π/2, π/2], B = [−1, 1]', f: Math.sin, D: [-PI / 2, PI / 2], B: [-1, 1], Wf: [-1, 1], win: [-7, 7, -2, 2], inj: true, sur: true, Dt: '[−π/2, π/2]', Bt: '[−1, 1]', Wt: '[−1, 1]' },
    lin: { name: '2x + 3 mit D = ℝ, B = ℝ', f: x => 2 * x + 3, D: [-I, I], B: [-I, I], Wf: [-I, I], win: [-4, 2, -4, 6], inj: true, sur: true, Dt: 'ℝ', Bt: 'ℝ', Wt: 'ℝ' },
    expR: { name: '2^x mit D = ℝ, B = ℝ', f: x => Math.pow(2, x), D: [-I, I], B: [-I, I], Wf: [0, I], win: [-4, 3, -2, 6], inj: true, sur: false, Dt: 'ℝ', Bt: 'ℝ', Wt: '(0, ∞)' },
  };
  let key = 'sqR', y0 = 2;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], [x0, x1, ya, yb] = s.win, A = mkAx(x0, x1, ya, yb); axes(v, A, 'x', 'y');
    const cl = (u, a, b) => Math.max(a, Math.min(b, u));
    v.line(A.P(x0, cl(s.B[0], ya, yb)), A.P(x0, cl(s.B[1], ya, yb)), C.c4, 7);
    v.line(A.P(x0 + 0.03 * (x1 - x0), cl(s.Wf[0], ya, yb)), A.P(x0 + 0.03 * (x1 - x0), cl(s.Wf[1], ya, yb)), C.c3, 5);
    const a = Math.max(x0, s.D[0]), b = Math.min(x1, s.D[1]);
    if (a > x0 || b < x1) fplot(v, A, s.f, C.line, 1.5, 800);
    fplot(v, A, s.f, C.c2, 2.8, 800, a, b);
    v.line(A.P(x0, y0), A.P(x1, y0), C.c1, 1.5, [6, 4]);
    const R = []; const N = 3000; let px = a, py = s.f(a) - y0;
    for (let i = 1; i <= N; i++) { const x = a + (b - a) * i / N, y = s.f(x) - y0; if (py === 0) R.push(px); else if (py * y < 0) R.push(px - py * (x - px) / (y - py)); px = x; py = y; }
    if (py === 0) R.push(px);
    R.forEach(x => v.dot(A.P(x, y0), C.c1, 6));
    const inB = y0 >= s.B[0] && y0 <= s.B[1];
    MW.info(infoEl, s.inj && s.sur ? 'bijektiv: es gibt f⁻¹ : B → D' : s.inj ? 'injektiv, aber nicht surjektiv' : s.sur ? 'surjektiv, aber nicht injektiv' : 'weder injektiv noch surjektiv',
      [['D(f)', s.Dt], ['B', s.Bt], ['W(f)', s.Wt], ['Schnittpunkte auf Höhe y = ' + fmt(y0), inB ? String(R.length) + (key === 'sinR' ? ' (im Fenster; insgesamt unendlich viele)' : '') : 'y ∉ B']],
      key === 'expR' ? 'Mit B = (0, ∞) statt ℝ wird 2^x bijektiv, die Inverse ist log₂ x. Einschränken von B macht surjektiv.'
      : key === 'sqR' ? 'Einschränken von D(f) macht injektiv: z.B. D = [0, ∞) (dann f⁻¹ = √y) oder D = (−∞, 0] (dann f⁻¹ = −√y).'
      : key === 'sinR' ? 'Einschränken auf [−π/2, π/2] und B = [−1, 1] führt zum Arcus Sinus.' : '', !(s.inj && s.sur));
  });
  const sl = MW.slider(ctl, { label: 'y', min: -4, max: 6, step: 0.01, value: y0, onInput: x => { y0 = x; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; const w = S[key].win;
    const inp = ctl.querySelector('input[type=range]'); inp.min = w[2]; inp.max = w[3]; y0 = Math.min(w[3], Math.max(w[2], key.startsWith('sin') ? 0.5 : 2)); sl.set(y0); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 6.2
W.append(dict(file='6-2-umkehrfunktion-spiegelung.html', title='Umkehrfunktion: Spiegelung an der Winkelhalbierenden y = x',
  sub='Ist (a, b) auf dem Graphen von f, also f(a) = b, dann ist a = f<sup>−1</sup>(b) und (b, a) liegt auf dem Graphen von f<sup>−1</sup>. Die beiden Punkte liegen spiegelbildlich zu y = x.',
  hint='Funktion wählen, a verschieben oder den Punkt ziehen.', legend=[('--c2', 'f'), ('--c3', 'f⁻¹'), ('--muted', 'y = x')], js=EQ + r'''
  const S = {
    lin: { name: 'f(x) = 2x + 3  ⟶  f⁻¹(x) = (x − 3)/2', f: x => 2 * x + 3, g: x => (x - 3) / 2, D: [-6, 6], Dg: [-6, 9], Dt: 'ℝ', Wt: 'ℝ', a: -1 },
    exp: { name: 'f(x) = 2^x  ⟶  f⁻¹(x) = log₂ x', f: x => Math.pow(2, x), g: x => Math.log2(x), D: [-6, 3], Dg: [0.001, 8], Dt: 'ℝ', Wt: '(0, ∞)', a: 1 },
    sqP: { name: 'f(x) = x², D = [0, ∞)  ⟶  f⁻¹(x) = √x', f: x => x * x, g: Math.sqrt, D: [0, 3], Dg: [0, 9], Dt: '[0, ∞)', Wt: '[0, ∞)', a: 1.5 },
    sqN: { name: 'f(x) = x², D = (−∞, 0]  ⟶  f⁻¹(x) = −√x', f: x => x * x, g: x => -Math.sqrt(x), D: [-3, 0], Dg: [0, 9], Dt: '(−∞, 0]', Wt: '[0, ∞)', a: -1.5 },
    hyp: { name: 'f(x) = √(x² − 1), D = [1, ∞)  ⟶  f⁻¹(x) = √(x² + 1)', f: x => Math.sqrt(x * x - 1), g: x => Math.sqrt(x * x + 1), D: [1, 6], Dg: [0, 6], Dt: '[1, ∞)', Wt: '[0, ∞)', a: 2 },
  };
  let key = 'sqP', a = 1.5, inv = true;
  const box = { xmin: -3.6, xmax: 4.6, ymin: -2.6, ymax: 4.4 };
  const view = MW.View2D(cv, box, v => {
    const C = v.C, s = S[key]; v.grid(1);
    v.line([box.xmin, box.xmin], [box.ymax, box.ymax], C.muted, 1.3, [6, 4]); v.text([3.6, 3.6], 'y = x', C.muted, 6, 14, 12, false);
    gplot(v, s.f, s.D[0], s.D[1], C.c2, 2.8, -3, 5);
    if (s.D[0] > -6 && key !== 'hyp') v.dot([s.D[0], s.f(s.D[0])], C.c2, 4);
    if (inv) gplot(v, s.g, s.Dg[0], s.Dg[1], C.c3, 2.8, -3, 5);
    const b = s.f(a), P = [a, b], Q = [b, a];
    v.dot(P, C.c2, 6); v.text(P, '(a, b)', C.c2, 8, -6, 12);
    if (inv) { v.line(P, Q, C.c1, 1.2, [3, 3]); v.dot(Q, C.c3, 6); v.text(Q, '(b, a)', C.c3, 8, 16, 12); }
    MW.info(infoEl, s.name, [['D(f) = W(f⁻¹)', s.Dt], ['W(f) = D(f⁻¹)', s.Wt], ['a, b = f(a)', fmt(a, 3) + ', ' + fmt(b, 3)], ['f⁻¹(b)', fmt(s.g(b), 3)]],
      key === 'sqP' || key === 'sqN' ? 'x² auf ganz ℝ ist nicht injektiv, also nicht umkehrbar. Je nach Einschränkung von D(f) erhält man √x oder −√x, nicht „±√x“.'
      : key === 'hyp' ? 'Skript: f ist gerade, erst die Einschränkung auf [1, ∞) macht f injektiv.' : 'f⁻¹(f(a)) = a und f(f⁻¹(y)) = y.');
  });
  view.handle(() => [a, S[key].f(a)], p => { const s = S[key]; a = Math.max(s.D[0], Math.min(s.D[1], p[0])); sl.set(a); });
  const sl = MW.slider(ctl, { label: 'a', min: -3, max: 3, step: 0.01, value: a, onInput: x => { const s = S[key]; a = Math.max(s.D[0], Math.min(s.D[1], x)); view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; a = S[key].a; sl.set(a); view.redraw(); }).set(key);
  MW.check(ctl, 'f⁻¹ zeigen', inv, x => { inv = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 6.3
W.append(dict(file='6-3-arcus-funktionen.html', title='Arcus-Funktionen: sin, cos, tan einschränken und umkehren',
  sub='sin auf [−π/2, π/2] → arcsin : [−1, 1] → [−π/2, π/2]. cos auf [0, π] → arccos : [−1, 1] → [0, π]. tan auf (−π/2, π/2) → arctan : ℝ → (−π/2, π/2). Eine andere Einschränkung liefert eine andere Umkehrfunktion.',
  hint='Funktion wählen, y verschieben.', tall=True, legend=[('--line', 'ganze Funktion'), ('--c2', 'eingeschränkte Funktion'), ('--c3', 'Umkehrfunktion'), ('--muted', 'y = x')], js=EQ + r'''
  const PI = Math.PI;
  const S = {
    sin: { name: 'sin auf [−π/2, π/2]  ⟶  arcsin', f: Math.sin, D: [-PI / 2, PI / 2], g: Math.asin, W: [-1, 1], Dt: '[−π/2, π/2]', Wt: '[−1, 1]', inv: 'arcsin' },
    cos: { name: 'cos auf [0, π]  ⟶  arccos', f: Math.cos, D: [0, PI], g: Math.acos, W: [-1, 1], Dt: '[0, π]', Wt: '[−1, 1]', inv: 'arccos' },
    tan: { name: 'tan auf (−π/2, π/2)  ⟶  arctan', f: Math.tan, D: [-PI / 2 + 1e-3, PI / 2 - 1e-3], g: Math.atan, W: [-3.5, 3.5], Dt: '(−π/2, π/2)', Wt: 'ℝ', inv: 'arctan' },
    sin2: { name: 'sin auf [π/2, 3π/2]  ⟶  π − arcsin', f: Math.sin, D: [PI / 2, 3 * PI / 2], g: y => PI - Math.asin(y), W: [-1, 1], Dt: '[π/2, 3π/2]', Wt: '[−1, 1]', inv: 'π − arcsin' },
  };
  let key = 'sin', y = 0.5;
  const box = { xmin: -3.4, xmax: 5.4, ymin: -2.4, ymax: 5.2 };
  const view = MW.View2D(cv, box, v => {
    const C = v.C, s = S[key]; v.grid(1);
    v.line([-2.4, -2.4], [5.2, 5.2], C.muted, 1.3, [6, 4]);
    gplot(v, s.f, -12, 12, C.line, 1.4, -2.4, 5.2, 3000);
    gplot(v, s.f, s.D[0], s.D[1], C.c2, 3, -2.4, 5.2, 800);
    gplot(v, s.g, s.W[0], s.W[1], C.c3, 3, -2.4, 5.2, 800);
    const x = s.g(y);
    v.line([box.xmin, y], [x, y], C.c1, 1, [3, 3]); v.dot([x, y], C.c2, 6); v.dot([y, x], C.c3, 6); v.line([x, y], [y, x], C.c1, 1, [2, 3]);
    v.text([y, x], s.inv + '(' + fmt(y, 2) + ')', C.c3, 8, -6, 12);
    MW.info(infoEl, s.inv + '(' + fmt(y, 3) + ') = ' + fmt(x, 4), [['D(f) = W(f⁻¹)', s.Dt], ['W(f) = D(f⁻¹)', s.Wt], ['Probe f(f⁻¹(y))', fmt(s.f(x), 4)]],
      key === 'sin2' ? 'Vorlesung: Auf [π/2, 3π/2] ist sin ebenfalls injektiv. Die Umkehrfunktion ist y ↦ π − arcsin y, nicht der übliche arcsin. Probe: 1 ↦ π/2, 0 ↦ π, −1 ↦ 3π/2.'
      : key === 'cos' ? 'Skript: arccos 1 = 0, arccos 0 = π/2, arccos(−1) = π.' : 'Die Einschränkung ist willkürlich, hat sich aber in der Literatur durchgesetzt (Skript, S. 56).');
  });
  const sl = MW.slider(ctl, { label: 'y', min: -1, max: 1, step: 0.01, value: y, onInput: x => { y = x; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; const s = S[key];
    const inp = ctl.querySelector('input[type=range]'); inp.min = s.W[0]; inp.max = s.W[1]; y = Math.max(s.W[0], Math.min(s.W[1], y)); sl.set(y); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- 7.1
W.append(dict(file='7-1-asymptoten.html', title='Asymptoten: f − g → 0 für x → ±∞',
  sub='g heisst Asymptote von f für x → ∞, wenn lim (f(x) − g(x)) = 0. Oben f und g, unten die Differenz f − g. Asymptoten müssen keine Geraden sein.',
  hint='Beispiel wählen, Fenster vergrössern.', tall=True, legend=[('--c2', 'f'), ('--c1', 'Asymptote g'), ('--c5', 'Asymptote für x → −∞'), ('--c3', 'f − g')], js=AX + r'''
  const S = {
    a: { name: '(2x + 1)/(x − 1)  →  2', f: x => (2 * x + 1) / (x - 1), g: x => 2, h: null, gt: 'g(x) = 2 (beide Richtungen)', note: 'Skript: (2x + 1)/(x − 1) = 2 + 3/(x − 1). Der Pol bei x = 1 („vertikale Asymptote“) ist nach unserer Definition keine Asymptote.' },
    b: { name: '(x² + 2x − 8)/(x − 3)  →  x + 5', f: x => (x * x + 2 * x - 8) / (x - 3), g: x => x + 5, h: null, gt: 'g(x) = x + 5 (beide Richtungen)', note: 'Skript: Polynomdivision ergibt x + 5 + 7/(x − 3). Pol bei x = 3.' },
    c: { name: '−1 + √(x² + 1)  →  x − 1 bzw. −x − 1', f: x => -1 + Math.sqrt(x * x + 1), g: x => x - 1, h: x => -x - 1, gt: 'g(x) = x − 1 für x → ∞, h(x) = −x − 1 für x → −∞', note: 'Skript: √(x² + 1) − x = 1/(√(x² + 1) + x) → 0. Da f gerade ist, folgt die Aussage für x → −∞ ebenso.' },
    d: { name: '(x³ − 3x + 5)/(x − 1)  →  x² + x − 2', f: x => (x ** 3 - 3 * x + 5) / (x - 1), g: x => x * x + x - 2, h: null, gt: 'g(x) = x² + x − 2 (beide Richtungen)', note: 'Skript: = x² + x − 2 + 3/(x − 1). Die Asymptote ist eine Parabel.' },
    e: { name: '2025 e^(−x²) + sin x  →  sin x', f: x => 2025 * Math.exp(-x * x) + Math.sin(x), g: Math.sin, h: null, gt: 'g(x) = sin x', note: 'Vorlesung: bei x = 0 dominiert 2025 e^(−x²), verschwindet aber für x → ∞. Asymptoten sind nicht immer Geraden.' },
  };
  let key = 'c', X = 6;
  const view = MW.View2D(cv, ''' + TALLBOX + r''', v => {
    const C = v.C, s = S[key];
    let lo = Infinity, hi = -Infinity; for (let i = 0; i <= 200; i++) { const x = -X + 2 * X * i / 200; [s.g(x), s.h ? s.h(x) : s.g(x)].forEach(y => { lo = Math.min(lo, y); hi = Math.max(hi, y); }); }
    const pad = 0.15 * (hi - lo) + Math.max(2, X / 2), A = mkAx(-X, X, lo - pad, hi + pad, 6, 2.3, 0, 1.45); axes(v, A, 'x', 'y');
    fplot(v, A, s.g, C.c1, 1.8, 800, s.h ? 0 : -X, X); if (s.h) fplot(v, A, s.h, C.c5, 1.8, 800, -X, 0);
    fplot(v, A, s.f, C.c2, 2.6, 2000);
    const B = mkAx(-X, X, -1.5, 1.5, 6, 1.05, 0, 0); axes(v, B, 'x', 'f − g', null, 1);
    const d = x => s.f(x) - (s.h && x < 0 ? s.h(x) : s.g(x)); fplot(v, B, d, C.c3, 2.2, 2000);
    MW.info(infoEl, s.gt, [['f(X) − g(X), X = ' + fmt(X, 1), fmt(d(X), 6)], ['f(−X) − g(−X)', fmt(d(-X), 6)]], s.note);
  });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'Fenster ±X', min: 3, max: 60, step: 0.5, value: X, onInput: x => { X = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('analysis-w3', W))
