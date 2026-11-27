"""Widgets zu Analysis I, Woche 10: Kap. III.3-6 (Stammbach, Teil A, Kap. III, S. 12-31). Integrieren und
Grundintegrale, partielle Integration, Substitution (mit Grenzen), Potenzen von sin/cos (Wallis), rationale
Funktionen (Partialbrüche, quadratische Ergänzung). Zu Kap. III gibt es keine Vorlesungsnotizen."""
from template import build
from build_analysis_w1 import AX, BOX
from build_analysis_w9 import EXTRA9

W = []

# ---------------------------------------------------------------- III.3 Stammfunktionen
W.append(dict(file='III-3-stammfunktionen.html', title='Stammfunktionen: F + C für jede Konstante C',
  sub='Ist F′ = f, dann ist auch F + C eine Stammfunktion. Die Graphen aller Stammfunktionen sind senkrecht gegeneinander verschoben und haben über jedem x dieselbe Steigung f(x).',
  hint='Grundintegral wählen, C und x verschieben.', legend=[('--c2', 'f'), ('--c3', 'Stammfunktionen F + C'), ('--c1', 'Tangenten bei x, Steigung f(x)')], js=AX + EXTRA9 + r'''
  const F = {
    pow: { name: '∫ x² dx = x³/3 + C', f: x => x * x, F: x => x ** 3 / 3, r: [-2, 2] },
    inv: { name: '∫ 1/x dx = log |x| + C', f: x => 1 / x, F: x => Math.log(Math.abs(x)), r: [-4, 4] },
    cos: { name: '∫ cos x dx = sin x + C', f: Math.cos, F: Math.sin, r: [-4, 4] },
    tan: { name: '∫ tan x dx = −log |cos x| + C', f: Math.tan, F: x => -Math.log(Math.abs(Math.cos(x))), r: [-1.5, 1.5] },
    at: { name: '∫ 1/(1 + x²) dx = arctan x + C', f: x => 1 / (1 + x * x), F: Math.atan, r: [-4, 4] },
    ars: { name: '∫ 1/√(x² + 1) dx = Arsinh x + C', f: x => 1 / Math.sqrt(x * x + 1), F: x => Math.log(x + Math.sqrt(x * x + 1)), r: [-4, 4] },
    ss: { name: '∫ 2 sin x cos x dx: sin² x oder −½ cos 2x', f: x => 2 * Math.sin(x) * Math.cos(x), F: x => Math.sin(x) ** 2, G: x => -0.5 * Math.cos(2 * x), r: [-3.2, 3.2] },
  };
  let key = 'pow', Cc = 0, x = 1;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = F[key], [a, b] = c.r;
    let lo = Infinity, hi = -Infinity; [c.f, c.F].forEach(g => { const [l, h] = range(g, a, b); lo = Math.min(lo, l); hi = Math.max(hi, h); });
    lo = Math.max(lo - 1.2, -6); hi = Math.min(hi + 1.2, 6); const A = mkAx(a, b, lo, hi); axes(v, A, 'x', 'y');
    for (let j = -2; j <= 2; j++) fplot(v, A, s => c.F(s) + Cc + j, C.c3, j === 0 ? 2.6 : 1.2, 600);
    if (c.G) fplot(v, A, c.G, C.c5, 2, 600);
    fplot(v, A, c.f, C.c2, 2.2, 600);
    const m = c.f(x);
    if (isFinite(m)) for (let j = -2; j <= 2; j++) { const y = c.F(x) + Cc + j, h = 0.35; v.line(A.P(x - h, y - m * h), A.P(x + h, y + m * h), C.c1, 1.6); }
    v.line(A.P(x, A.y0), A.P(x, A.y1), C.muted, 1, [3, 3]);
    const rows = [['x', fmt(x, 3)], ['f(x) = Steigung', fmt(m, 4)], ['F(x) + C', fmt(c.F(x) + Cc, 4)], ['Kontrolle (F(x + h) − F(x − h))/2h', fmt((c.F(x + 1e-5) - c.F(x - 1e-5)) / 2e-5, 4)]];
    if (c.G) rows.push(['−½ cos 2x − sin² x', fmt(c.G(x) - c.F(x), 4) + ' (konstant = C)']);
    MW.info(infoEl, c.name, rows, 'Skript S. 10–13: Die Menge aller Stammfunktionen heisst ∫ f(x) dx (unbestimmtes Integral). Jede Ableitungsregel liefert eine Integrationsregel. ' + (c.G ? 'Skript S. 10: sin² x und −½ cos 2x (violett) haben beide die Ableitung 2 sin x cos x, unterscheiden sich also nur um C = −½. Daraus folgt sin² x = ½(1 − cos 2x).' : key === 'inv' || key === 'tan' ? 'Achtung: Bei 1/x und tan x zerfällt der Definitionsbereich in Intervalle; auf jedem darf C anders sein (eigener Hinweis).' : ''));
  });
  const sx = MW.slider(ctl, { label: 'x', min: -2, max: 2, step: 0.01, value: x, onInput: u => { x = u; view.redraw(); } });
  MW.slider(ctl, { label: 'C', min: -2, max: 2, step: 0.05, value: Cc, onInput: u => { Cc = u; view.redraw(); } });
  MW.select(ctl, 'Grundintegral', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; const c = F[u], i = sx.el.querySelector('input'); i.min = c.r[0]; i.max = c.r[1]; x = c.r[1] * 0.4; sx.set(x); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- III.4 Partielle Integration
W.append(dict(file='III-4-partielle-integration.html', title='Partielle Integration: ∫ u′v dx = uv − ∫ uv′ dx',
  sub='Die Produktregel rückwärts gelesen. Man wählt u′ (wird integriert) und v (wird abgeleitet) so, dass das neue Integral ∫ uv′ dx einfacher wird. Unten wird das Ergebnis F durch Ableiten kontrolliert.',
  hint='Beispiel und Wahl von u′, v umschalten.', legend=[('--c2', 'Integrand f'), ('--c3', 'Stammfunktion F (mit F(0) = 0 bzw. F(1) = 0)')], js=AX + EXTRA9 + r'''
  const E = Math.exp, s = Math.sin, c = Math.cos;
  const X = {
    xe: { name: '∫ x eˣ dx', f: x => x * E(x), F: x => (x - 1) * E(x) + 1, r: [-3, 1.6],
      good: ['u′ = eˣ,  u = eˣ', 'v = x,  v′ = 1', '∫ x eˣ dx = x eˣ − ∫ eˣ dx = (x − 1) eˣ + C', 'Skript S. 15'],
      bad: ['u′ = x,  u = x²/2', 'v = eˣ,  v′ = eˣ', '∫ x eˣ dx = (x²/2) eˣ − ∫ (x²/2) eˣ dx: schwieriger!', 'Skript S. 16. Rückwärts gelesen liefert die Gleichung immerhin ∫ x² eˣ dx = (x² − 2x + 2) eˣ + C.'] },
    s2: { name: '∫ sin² x dx', f: x => s(x) ** 2, F: x => 0.5 * (x - s(x) * c(x)), r: [-3.5, 3.5],
      good: ['u′ = sin x,  u = −cos x', 'v = sin x,  v′ = cos x', '∫ sin² x dx = −sin x cos x + x − ∫ sin² x dx  ⇒  ∫ sin² x dx = ½(x − sin x cos x) + C', 'Skript S. 16–17: Das Ausgangsintegral tritt wieder auf. Man löst die Gleichung danach auf.'] },
    ecos: { name: '∫ eˣ cos 2x dx (a = 1, b = 2)', f: x => E(x) * c(2 * x), F: x => E(x) * (c(2 * x) + 2 * s(2 * x)) / 5 - 0.2, r: [-3, 2],
      good: ['u′ = e^(ax),  u = e^(ax)/a  (zweimal)', 'v = cos bx, dann v = sin bx', '∫ e^(ax) cos bx dx = e^(ax)(a cos bx + b sin bx)/(a² + b²) + C', 'Skript S. 17–18: Zweimal partiell integrieren, dann nach dem Ausgangsintegral auflösen.'] },
    log: { name: '∫ log x dx', f: Math.log, F: x => x * (Math.log(x) - 1) + 1, r: [0.02, 4],
      good: ['u′ = 1,  u = x', 'v = log x,  v′ = 1/x', '∫ log x dx = x log x − ∫ 1 dx = x(log x − 1) + C', 'Skript S. 18: Trick mit dem Faktor 1.'] },
    at: { name: '∫ arctan x dx', f: Math.atan, F: x => x * Math.atan(x) - 0.5 * Math.log(1 + x * x), r: [-4, 4],
      good: ['u′ = 1,  u = x', 'v = arctan x,  v′ = 1/(1 + x²)', '∫ arctan x dx = x arctan x − ½ log(1 + x²) + C', 'Skript S. 18: Im Restintegral mit 2 erweitern, damit im Zähler die Ableitung des Nenners steht.'] },
  };
  let key = 'xe', bad = false, x = 1;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, e = X[key], [a, b] = e.r; let lo = Infinity, hi = -Infinity;
    [e.f, e.F].forEach(g => { const [l, h] = range(g, a, b); lo = Math.min(lo, l); hi = Math.max(hi, h); });
    const A = mkAx(a, b, Math.min(lo, -0.2), Math.max(hi, 0.2)); axes(v, A, 'x', 'y');
    fplot(v, A, e.F, C.c3, 2.6, 600); fplot(v, A, e.f, C.c2, 2.2, 600);
    v.dot(A.P(x, e.F(x)), C.c3, 5); v.dot(A.P(x, e.f(x)), C.c2, 5);
    const h = 1e-5, dF = (e.F(x + h) - e.F(x - h)) / (2 * h), st = bad && e.bad ? e.bad : e.good;
    MW.info(infoEl, e.name + (bad && e.bad ? ' (ungünstige Wahl)' : ''), [['u′, u', st[0]], ['v, v′', st[1]], ['Rechnung', st[2]], ['Kontrolle bei x = ' + fmt(x, 2), 'F′(x) ≈ ' + fmt(dF, 5) + ',  f(x) = ' + fmt(e.f(x), 5)]], st[3] + ' Die Kontrolle durch Ableiten sollte man immer machen (Skript S. 21).');
  });
  const sx = MW.slider(ctl, { label: 'x', min: -3, max: 1.6, step: 0.01, value: x, onInput: u => { x = u; view.redraw(); } });
  MW.check(ctl, 'andere Wahl von u′, v', bad, u => { bad = u; view.redraw(); }); const cb = ctl.lastChild;
  MW.select(ctl, 'Beispiel', Object.entries(X).map(([k, e]) => [k, e.name]), u => { key = u; const e = X[u], i = sx.el.querySelector('input'); i.min = e.r[0]; i.max = e.r[1]; x = Math.min(e.r[1], 1); sx.set(x); cb.style.display = e.bad ? '' : 'none'; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- III.5 Substitution mit Grenzen
W.append(dict(file='III-5-substitution-grenzen.html', title='Substitution im bestimmten Integral: Grenzen mittransformieren',
  sub='Links das Integral in der alten Variablen, rechts nach der Substitution. Die Flächen sind gleich gross, obwohl die Graphen verschieden aussehen. Die Grenzen werden mit der Substitution umgerechnet.',
  hint='Beispiel wählen und die obere Grenze verschieben.', legend=[('--c2', 'Integrand in x'), ('--c5', 'Integrand in der neuen Variablen')], js=AX + EXTRA9 + r'''
  const S = {
    ell: { name: 'Ellipsenviertel: x = a sin t (a = 2, b = 1)', fx: x => Math.sqrt(Math.max(0, 1 - x * x / 4)), X: [0, 2], gt: t => 2 * Math.cos(t) ** 2, T: X => Math.asin(X / 2), Tr: [0, Math.PI / 2],
      lx: '∫₀^X b√(1 − x²/a²) dx', lt: '∫₀^(arcsin(X/a)) ab cos² t dt', sub: 'x = a sin t,  dx = a cos t dt,  √(1 − sin² t) = cos t für 0 ≤ t ≤ π/2', ex: X => (Math.asin(X / 2) + X / 2 * Math.sqrt(1 - X * X / 4)),
      note: 'Skript S. 22–23: F/4 = ∫₀ᵃ b√(1 − x²/a²) dx = ∫₀^(π/2) ab cos² t dt = πab/4. Die Substitution muss auf [0, π/2] eingeschränkt werden, damit sie injektiv ist und die Grenzen eindeutig sind.' },
    xs: { name: '∫ x sin(x²) dx: u = x²', fx: x => x * Math.sin(x * x), X: [0, 2.2], gt: u => 0.5 * Math.sin(u), T: X => X * X, Tr: [0, 4.84],
      lx: '∫₀^X x sin(x²) dx', lt: '½ ∫₀^(X²) sin u du', sub: 'u = x²,  du = 2x dx,  also x dx = du/2', ex: X => 0.5 * (1 - Math.cos(X * X)),
      note: 'Skript S. 20: ∫ x sin(x²) dx = −½ cos(x²) + C. Die Grenzen 0 und X werden zu 0 und X².' },
    sn: { name: '∫ sin² x cos x dx: u = sin x', fx: x => Math.sin(x) ** 2 * Math.cos(x), X: [0, Math.PI / 2], gt: u => u * u, T: X => Math.sin(X), Tr: [0, 1],
      lx: '∫₀^X sin² x cos x dx', lt: '∫₀^(sin X) u² du', sub: 'u = sin x,  du = cos x dx', ex: X => Math.sin(X) ** 3 / 3,
      note: 'Skript S. 19–20 mit n = 2: ∫ sinⁿ x cos x dx = sinⁿ⁺¹ x/(n + 1) + C. Eine Substitution drängt sich auf, wenn der Integrand u′(x) als Faktor enthält.' },
  };
  let key = 'ell', p = 0.7;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], Xv = s.X[0] + p * (s.X[1] - s.X[0]), Tv = s.T(Xv);
    const [l1, h1] = range(s.fx, ...s.X), [l2, h2] = range(s.gt, ...s.Tr);
    const L = mkAx(s.X[0], s.X[1], Math.min(l1, 0), Math.max(h1, 0.1), 2.8, 3.4, 0, 0), R = mkAx(s.Tr[0], s.Tr[1], Math.min(l2, 0), Math.max(h2, 0.1), 2.8, 3.4, 3.2, 0);
    axes(v, L, 'x', ''); axes(v, R, key === 'ell' ? 't' : 'u', '');
    area(v, L, s.fx, s.X[0], Xv); area(v, R, s.gt, s.Tr[0], Tv);
    fplot(v, L, s.fx, C.c2, 2.4, 400); fplot(v, R, s.gt, C.c5, 2.4, 400);
    v.line(L.P(Xv, L.y0), L.P(Xv, L.y1), C.fg, 1, [3, 3]); v.line(R.P(Tv, R.y0), R.P(Tv, R.y1), C.fg, 1, [3, 3]);
    v.text(L.P(Xv, L.y1), 'X', C.fg, 4, 14, 12); v.text(R.P(Tv, R.y1), 'neue Grenze', C.fg, 4, 14, 12);
    const I1 = simpson(s.fx, s.X[0], Xv), I2 = simpson(s.gt, s.Tr[0], Tv);
    MW.info(infoEl, s.name, [['Substitution', s.sub], ['links: ' + s.lx, fmt(I1, 6)], ['rechts: ' + s.lt, fmt(I2, 6)], ['obere Grenzen', 'X = ' + fmt(Xv, 4) + '  →  ' + fmt(Tv, 4)], ['geschlossen', fmt(s.ex(Xv), 6)]], s.note);
  });
  MW.slider(ctl, { label: 'obere Grenze', min: 0, max: 1, step: 0.002, value: p, fmt: u => fmt(u * 100, 0) + ' %', onInput: u => { p = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- III.6 sinⁿ und Wallis
W.append(dict(file='III-6-sinus-potenzen-wallis.html', title='Iₙ = ∫₀^(π/2) sinⁿ x dx und die Formel von Wallis',
  sub='Mit partieller Integration gilt Iₙ = (n − 1)/n · Iₙ₋₂, mit I₀ = π/2 und I₁ = 1. Die Spiegelung an x = π/4 zeigt Iₙ = Jₙ = ∫₀^(π/2) cosⁿ x dx. Aus Iₙ folgt das Wallis-Produkt für π/2.',
  hint='n vergrössern. Das Wallis-Produkt konvergiert langsam gegen π/2.', legend=[('--c2', 'sinⁿ x'), ('--c5', 'cosⁿ x (gespiegelt)')], js=AX + EXTRA9 + r'''
  let n = 4, k = 10;
  const I = m => m === 0 ? Math.PI / 2 : m === 1 ? 1 : (m - 1) / m * I(m - 2);
  const frac = m => { if (m < 2) return m ? '1' : 'π/2'; const num = [], den = []; for (let j = m; j >= 2; j -= 2) { num.push(j - 1); den.push(j); } return '(' + num.reverse().join('·') + ')/(' + den.reverse().join('·') + ')' + (m % 2 ? '' : ' · π/2'); };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A = mkAx(0, Math.PI / 2, 0, 1.1); axes(v, A, 'x', 'y', Math.PI / 8, 0.25);
    area(v, A, x => Math.sin(x) ** n, 0, Math.PI / 2);
    fplot(v, A, x => Math.cos(x) ** n, C.c5, 1.6, 300); fplot(v, A, x => Math.sin(x) ** n, C.c2, 2.6, 300);
    v.line(A.P(Math.PI / 4, 0), A.P(Math.PI / 4, 1.1), C.muted, 1, [4, 4]);
    let W = 1; for (let j = 1; j <= k; j++) W *= (2 * j) * (2 * j) / ((2 * j - 1) * (2 * j + 1));
    MW.info(infoEl, 'n = ' + n, [['Iₙ (Rekursion)', fmt(I(n), 6)], ['geschlossen', frac(n)], ['numerisch', fmt(simpson(x => Math.sin(x) ** n, 0, Math.PI / 2), 6)], ['Wallis-Produkt mit k = ' + k + ' Faktorpaaren', fmt(W, 6) + '  (π/2 = ' + fmt(Math.PI / 2, 6) + ')']],
      'Skript S. 24–28: Rekursion ∫ sinⁿ x dx = −(1/n) cos x sinⁿ⁻¹ x + (n − 1)/n ∫ sinⁿ⁻² x dx, also Iₙ = (n − 1)/n · Iₙ₋₂. Wallis: (2·2·4·4·…·2k·2k)/(1·3·3·5·…·(2k − 1)(2k + 1)) → π/2. Anwendung: ∫₀ᵃ x²√(a² − x²) dx = π a⁴/16 (Skript S. 28).');
  });
  MW.slider(ctl, { label: 'n', min: 0, max: 20, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.slider(ctl, { label: 'Wallis k', min: 1, max: 500, step: 1, value: k, fmt: u => fmt(u, 0), onInput: u => { k = u; view.redraw(); } });
'''))

# ---------------------------------------------------------------- III.6 rationale Funktionen
W.append(dict(file='III-6-partialbrueche.html', title='Rationale Funktionen: Partialbrüche und quadratische Ergänzung',
  sub='Hat der Nenner reelle Nullstellen, zerlegt man in Partialbrüche A/(x − x₁) + B/(x − x₂) + … und integriert zu Logarithmen. Hat er keine, führt quadratische Ergänzung auf ∫ 1/(u² + 1) du = arctan u.',
  hint='Beispiel wählen. Die gestrichelten Summanden addieren sich zum Integranden.', legend=[('--c2', 'Integrand'), ('--c4', 'Summand 1'), ('--c5', 'Summand 2'), ('--c3', 'Summand 3')], js=AX + EXTRA9 + r'''
  const R = {
    s30: { name: '1/(x² − 6x + 5)', f: x => 1 / (x * x - 6 * x + 5), parts: [x => 0.25 / (x - 5), x => -0.25 / (x - 1)], r: [-1, 7, -2, 2], poles: [1, 5],
      rows: [['Nenner', '(x − 5)(x − 1)'], ['Ansatz', 'A/(x − 5) + B/(x − 1),  A + B = 0,  −A − 5B = 1'], ['Koeffizienten', 'A = 1/4,  B = −1/4'], ['Integral', '¼ (log|x − 5| − log|x − 1|) + C = log|(x − 5)/(x − 1)|^(1/4) + C']],
      note: 'Skript S. 29–30. Die Theorie der Partialbrüche wird im Skript nicht behandelt, nur an Beispielen benützt.' },
    f89: { name: '4x/((x − 1)(x + 1)(x + 2))', f: x => 4 * x / ((x - 1) * (x + 1) * (x + 2)), parts: [x => (2 / 3) / (x - 1), x => 2 / (x + 1), x => (-8 / 3) / (x + 2)], r: [-4, 3, -8, 8], poles: [-2, -1, 1],
      rows: [['Ansatz', 'A/(x − 1) + B/(x + 1) + C/(x + 2)'], ['Koeffizienten', 'A = 2/3,  B = 2,  C = −8/3'], ['∫ von −½ bis ½', '(2/3) log(1/3) + 2 log 3 − (8/3) log(5/3) = (4/3) log(27/25) ≈ ' + fmt(4 / 3 * Math.log(27 / 25), 5)]],
      note: 'Prüfung Frühling 1989, dreistündig, Aufg. 7 (Aufgabensammlung S. 74, Lösung S. 203–204). Dort ist es der letzte Schritt einer Aufgabe zu G′(0); das Integral selbst ist reiner Stoff von III.6.' },
    s31: { name: '(3x − 1)/(x² − x + 1)', f: x => (3 * x - 1) / (x * x - x + 1), parts: [x => 1.5 * (2 * x - 1) / (x * x - x + 1), x => 0.5 / (x * x - x + 1)], r: [-4, 5, -2, 3.5], poles: [],
      rows: [['Zähler umbauen', '3x − 1 = (3/2)(2x − 1) + 1/2,  (x² − x + 1)′ = 2x − 1'], ['quadr. Ergänzung', 'x² − x + 1 = (x − ½)² + ¾'], ['Substitution', 'u = (2/√3)(x − ½)'], ['Integral', '(3/2) log(x² − x + 1) + (1/√3) arctan((2x − 1)/√3) + C']],
      note: 'Skript S. 30–31. Achtung: Im Skript steht das Endergebnis für ∫ 1/(x² − x + 1) dx = (2/√3) arctan(…); dieses wird noch mit ½ multipliziert.' },
  };
  let key = 's30', sp = true;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, e = R[key], A = mkAx(...e.r); axes(v, A, 'x', 'y');
    e.poles.forEach(p => v.line(A.P(p, A.y0), A.P(p, A.y1), C.muted, 1, [3, 3]));
    if (sp) e.parts.forEach((g, i) => dplot(v, A, g, [C.c4, C.c5, C.c3][i], 1.6, 800));
    fplot(v, A, e.f, C.c2, 2.6, 1200);
    const xt = 0.3, sum = e.parts.reduce((s, g) => s + g(xt), 0);
    MW.info(infoEl, '∫ ' + e.name + ' dx', e.rows.concat([['Kontrolle bei x = 0.3', 'f = ' + fmt(e.f(xt), 6) + ',  Summe = ' + fmt(sum, 6)]]), e.note);
  });
  MW.select(ctl, 'Beispiel', Object.entries(R).map(([k, e]) => [k, e.name]), u => { key = u; view.redraw(); }).set(key);
  MW.check(ctl, 'Summanden zeigen', sp, u => { sp = u; view.redraw(); });
'''))

if __name__ == '__main__':
    print(build('analysis-w10', W))
