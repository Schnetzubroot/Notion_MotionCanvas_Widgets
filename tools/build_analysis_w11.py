"""Widgets zu Analysis I, Woche 11: Kap. VIII Potenzreihen (Stammbach, Teil C, Kap. VIII.1-5, S. 3-33,
PDF-Seiten 129-159). Reihen und Partialsummen, Potenzreihen und Konvergenzbereich, Taylorpolynom, Taylorreihe
und Binomialreihe, Koeffizientenvergleich, Anwendungen (nicht elementare Integrale, Potenzreihenansatz bei DGL).
Zu Kap. VIII gibt es (noch) keine Vorlesungsnotizen; die Quellen sind Skript und alte Prüfungen."""
from template import build
from build_analysis_w1 import AX, BOX

EXTRA = r'''
  function dplot(v, A, f, color, w = 1.3, N = 300, a = A.x0, b = A.x1) { let seg = [];
    const fl = () => { if (seg.length > 1) v.poly(seg, color, w, [5, 4]); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x); if (!isFinite(y) || !A.inY(y)) { fl(); continue; } seg.push(A.P(x, y)); } fl(); }
  const fac = k => { let s = 1; for (let i = 2; i <= k; i++) s *= i; return s; };
  const poly = (c, x, x0 = 0) => { let s = 0; for (let k = c.length - 1; k >= 0; k--) s = s * (x - x0) + c[k]; return s; };
  const sci = x => !isFinite(x) ? '–' : (x !== 0 && (Math.abs(x) >= 1e6 || Math.abs(x) < 1e-4)) ? x.toExponential(2).replace('.', ',').replace(/e\+?(-?)(\d+)/, (m, s, d) => ' · 10^' + (s ? '−' : '') + d) : fmt(x, 5);
  const simpson = (f, a, b, n = 400) => { const h = (b - a) / n; let s = f(a) + f(b); for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2); return s * h / 3; };
  // Intervall-Band für den Konvergenzbereich auf der x-Achse
  function band(v, A, a, b, inA, inB, color) {
    const y = A.y0, lo = Math.max(a, A.x0), hi = Math.min(b, A.x1);
    if (hi > lo) { v.poly([A.P(lo, A.y0), A.P(hi, A.y0), A.P(hi, A.y1), A.P(lo, A.y1)], color, 0, null, true, v.C.fill); v.line(A.P(lo, y), A.P(hi, y), color, 5); }
    if (isFinite(a) && a >= A.x0) v.dot(A.P(a, y), color, 6, !inA);
    if (isFinite(b) && b <= A.x1) v.dot(A.P(b, y), color, 6, !inB);
  }
'''

W = []

# ---------------------------------------------------------------- VIII.1
W.append(dict(file='1-1-reihen-partialsummen.html', title='Reihen: die Folge der Partialsummen sₙ',
  sub='Eine Reihe konvergiert, wenn ihre Partialsummen sₙ = a₀ + a₁ + … + aₙ konvergieren. Die Punkte zeigen sₙ über n. Die harmonische Reihe wächst ohne Grenze, obwohl aₖ → 0. Bei der alternierenden harmonischen Reihe springt sₙ hin und her und schliesst den Grenzwert ein.',
  hint='Reihe wählen und n vergrössern.', legend=[('--c1', 'Partialsummen sₙ'), ('--c2', 'Grenzwert s'), ('--c3', 'Glieder aₙ')], js=AX + EXTRA + r'''
  const S = {
    geo: { name: 'Σ (1/2)ᵏ, geometrisch', a: k => 0.5 ** k, s: 2, ss: '2 = 1/(1 − 1/2)',
      note: 'Skript S. 3, Vorlesung Kap. I S. 7: 1 + x + x² + … = 1/(1 − x) für |x| < 1. Hier x = 1/2.' },
    harm: { name: 'Σ 1/(k + 1), harmonisch', a: k => 1 / (k + 1), s: null, ss: 'divergiert',
      note: 'Skript S. 4: Die harmonische Reihe divergiert, obwohl aₖ → 0 und |aₙ| < |aₙ₋₁| (Skript S. 5). aₖ → 0 ist also nur notwendig, nicht hinreichend. Die Partialsummen wachsen etwa wie ln n (eigene Beobachtung).' },
    alt: { name: 'Σ (−1)ᵏ/(k + 1), alternierend harmonisch', a: k => (k % 2 ? -1 : 1) / (k + 1), s: Math.LN2, ss: 'ln 2 ≈ 0.69315',
      note: 'Skript S. 4–5: Die Schritte wechseln die Richtung und werden kürzer, also liegt s immer zwischen sₙ₋₁ und sₙ (Leibniz-Kriterium, Skript S. 5). Die Summe ist log 2 (Skript S. 8). Die Konvergenz ist sehr langsam.' },
    efac: { name: 'Σ 1/k!', a: k => 1 / fac(k), s: Math.E, ss: 'e ≈ 2.71828',
      note: 'Vorlesung Kap. I S. 5–7: monoton wachsend und durch 3 beschränkt, also konvergent mit Grenzwert e.' },
    osz: { name: 'Σ (−1)ᵏ', a: k => (k % 2 ? -1 : 1), s: null, ss: 'divergiert (pendelt zwischen 1 und 0)',
      note: 'Skript S. 5: Konvergiert eine Reihe, so gilt aₖ → 0. Hier ist |aₖ| = 1, also divergiert die Reihe sicher.' },
  };
  let key = 'alt', N = 20;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = S[key]; const s = []; let t = 0;
    for (let k = 0; k <= N; k++) { t += c.a(k); s.push(t); }
    let lo = Math.min(0, ...s), hi = Math.max(...s, c.s || 0, 1); const pad = 0.08 * (hi - lo); lo -= pad; hi += pad;
    const A = mkAx(-0.5, N + 0.5, lo, hi); axes(v, A, 'n', 'sₙ', N > 60 ? 20 : N > 25 ? 5 : N > 10 ? 2 : 1);
    if (c.s !== null) { v.line(A.P(-0.5, c.s), A.P(N + 0.5, c.s), C.c2, 1.8, [6, 4]); v.text(A.P(N + 0.5, c.s), 's', C.c2, -10, -6, 13); }
    const big = N > 60;
    for (let k = 0; k <= N; k++) { if (!big) v.line(A.P(k, s[k] - c.a(k)), A.P(k, s[k]), C.c3, 1.4); v.dot(A.P(k, s[k]), C.c1, big ? 2.5 : 4); }
    const rows = [['Reihe', c.name], ['aₙ', fmt(c.a(N), 6)], ['sₙ', fmt(s[N], 6)], ['Summe', c.ss]];
    if (c.s !== null) rows.push(['|s − sₙ|', sci(Math.abs(c.s - s[N]))]);
    if (key === 'alt' && N >= 1) rows.push(['s liegt zwischen', fmt(Math.min(s[N - 1], s[N]), 5) + ' und ' + fmt(Math.max(s[N - 1], s[N]), 5)]);
    MW.info(infoEl, 'n = ' + N, rows, c.note);
  });
  MW.slider(ctl, { label: 'n', min: 1, max: 200, step: 1, value: N, fmt: u => fmt(u, 0), onInput: u => { N = u; view.redraw(); } });
  MW.select(ctl, 'Reihe', Object.entries(S).map(([k, c]) => [k, c.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- VIII.2
W.append(dict(file='2-1-konvergenzbereich.html', title='Potenzreihen: Konvergenzbereich und Partialsummen',
  sub='Eine Potenzreihe Σ aₖ(x − x₀)ᵏ konvergiert auf einem Intervall mit Mittelpunkt x₀ (grün markiert). Dort nähern sich die Partialsummen der Funktion, ausserhalb laufen sie davon. Ob die Randpunkte dazugehören, muss man einzeln prüfen (gefüllt: Konvergenz, hohl: Divergenz).',
  hint='Reihe wählen und den Grad n erhöhen.', legend=[('--c2', 'Funktion'), ('--c1', 'Partialsumme vom Grad n'), ('--c3', 'Konvergenzbereich')], js=AX + EXTRA + r'''
  const S = {
    geo: { name: '1/(1 − x) = 1 + x + x² + …', f: x => 1 / (1 - x), c: k => 1, x0: 0, I: [-1, 1, false, false], ax: [-2, 2, -2, 6], iv: '(−1, 1)',
      note: 'Skript S. 6: geometrische Reihe, aₖ = 1. Konvergenzbereich (−1, 1). Bei x = 1 und x = −1 divergiert sie (die Glieder gehen nicht gegen 0).' },
    log: { name: 'log(1 + x) = x − x²/2 + x³/3 − …', f: x => Math.log(1 + x), c: k => k ? (k % 2 ? 1 : -1) / k : 0, x0: 0, I: [-1, 1, false, true], ax: [-1.6, 2, -3, 2], iv: '(−1, 1]',
      note: 'Skript S. 7–8, (2.2): 1/(1 + t) gliedweise integriert. Bei x = −1 entsteht die (negative) harmonische Reihe: Divergenz. Bei x = 1 die alternierende harmonische Reihe: Konvergenz gegen log 2.' },
    atan: { name: 'arctan x = x − x³/3 + x⁵/5 − …', f: Math.atan, c: k => k % 2 ? ((k - 1) / 2 % 2 ? -1 : 1) / k : 0, x0: 0, I: [-1, 1, true, true], ax: [-2, 2, -2.2, 2.2], iv: '[−1, 1]',
      note: 'Skript S. 8: 1/(1 + t²) gliedweise integriert. Das Skript gibt |x| < 1 an. Dass die Reihe auch in x = ±1 konvergiert, folgt aus dem Leibniz-Kriterium (Skript S. 5), eigene Überlegung.' },
    shift: { name: '1/(x + 2) mit Mittelpunkt x₀ = 1', f: x => 1 / (x + 2), c: k => (k % 2 ? -1 : 1) / 3 ** (k + 1), x0: 1, I: [-2, 4, false, false], ax: [-3.5, 5.5, -1.5, 2.5], iv: '(−2, 4)',
      note: 'Skript S. 8: 1/(x + 2) = 1/3 · 1/(1 + (x − 1)/3) = Σ (−1)ᵏ (x − 1)ᵏ / 3ᵏ⁺¹. Konvergenz für |x − 1|/3 < 1, also (−2, 4). Das Intervall hat den Mittelpunkt x₀ = 1.' },
    exp: { name: 'eˣ = 1 + x + x²/2! + …', f: Math.exp, c: k => 1 / fac(k), x0: 0, I: [-Infinity, Infinity, true, true], ax: [-4, 4, -2, 12], iv: 'ganz ℝ',
      note: 'Skript S. 14: Die Exponentialreihe konvergiert für alle x. Die Partialsummen brauchen für grosse |x| aber einen hohen Grad.' },
  };
  let key = 'log', n = 5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = S[key], A = mkAx(...c.ax); axes(v, A, 'x', 'y');
    band(v, A, c.I[0], c.I[1], c.I[2], c.I[3], C.c3);
    const co = []; for (let k = 0; k <= n; k++) co.push(c.c(k));
    fplot(v, A, c.f, C.c2, 2.6, 800); fplot(v, A, x => poly(co, x, c.x0), C.c1, 2.2, 800);
    v.dot(A.P(c.x0, c.f(c.x0)), C.fg, 4.5); v.text(A.P(c.x0, c.f(c.x0)), 'x₀', C.fg, 6, 16, 12);
    const xs = [c.x0 + 0.5, c.I[1] === Infinity ? 2 : c.I[1], c.I[1] === Infinity ? 3.5 : c.x0 + 1.2 * (c.I[1] - c.x0)];
    MW.info(infoEl, c.name, [['Konvergenzbereich', c.iv], ['Grad n', String(n)]].concat(xs.map(x => ['x = ' + fmt(x, 2) + ':  Pₙ(x) / f(x)', sci(poly(co, x, c.x0)) + '  /  ' + sci(c.f(x))])),
      c.note + ' Im Innern des Konvergenzintervalls darf man gliedweise addieren, multiplizieren, ableiten und integrieren (Skript S. 7).');
  });
  MW.slider(ctl, { label: 'Grad n', min: 0, max: 30, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'Reihe', Object.entries(S).map(([k, c]) => [k, c.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- VIII.3
W.append(dict(file='3-1-taylorpolynom.html', title='Taylorpolynom Pₙ von f in x₀',
  sub='Pₙ hat in x₀ denselben Wert und dieselben ersten n Ableitungen wie f. P₁ ist die lineare Ersatzfunktion. Je höher n, desto grösser das Intervall um x₀, in dem Pₙ die Funktion gut annähert (Skript S. 9–13).',
  hint='Funktion wählen, x₀ und n verschieben.', legend=[('--c2', 'f'), ('--c1', 'Taylorpolynom Pₙ'), ('--c3', 'P₁ (lineare Ersatzfunktion)')], js=AX + EXTRA + r'''
  // k-te Ableitung in x0
  const F = {
    sin: { name: 'sin x', f: Math.sin, d: (k, x) => [Math.sin, Math.cos, x => -Math.sin(x), x => -Math.cos(x)][k % 4](x), ax: [-4, 6, -2.5, 2.5], x0: Math.PI / 6, lo: -3, hi: 5 },
    exp: { name: 'eˣ', f: Math.exp, d: (k, x) => Math.exp(x), ax: [-3, 3, -1, 8], x0: 0, lo: -2, hi: 2 },
    cos: { name: 'cos x', f: Math.cos, d: (k, x) => [Math.cos, x => -Math.sin(x), x => -Math.cos(x), Math.sin][k % 4](x), ax: [-7, 7, -2.5, 2.5], x0: 0, lo: -5, hi: 5 },
    ln: { name: 'ln(1 + x)', f: x => Math.log(1 + x), d: (k, x) => k ? (k % 2 ? 1 : -1) * fac(k - 1) / (1 + x) ** k : Math.log(1 + x), ax: [-1.5, 3, -3, 2], x0: 0, lo: -0.8, hi: 2 },
  };
  let key = 'sin', n = 2, x0 = Math.PI / 6;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = F[key], A = mkAx(...c.ax); axes(v, A, 'x', 'y');
    const co = []; for (let k = 0; k <= n; k++) co.push(c.d(k, x0) / fac(k));
    fplot(v, A, c.f, C.c2, 2.6, 800);
    if (n >= 2) fplot(v, A, x => c.f(x0) + c.d(1, x0) * (x - x0), C.c3, 1.4, 200);
    fplot(v, A, x => poly(co, x, x0), C.c1, 2.3, 800);
    v.dot(A.P(x0, c.f(x0)), C.fg, 5.5); v.text(A.P(x0, c.f(x0)), 'x₀', C.fg, 6, -8, 12);
    // Bereich |f − Pn| < 0.01 um x0
    let a = x0, b = x0; const ok = x => Math.abs(c.f(x) - poly(co, x, x0)) < 0.01;
    while (b < A.x1 && ok(b + 0.01)) b += 0.01; while (a > A.x0 && ok(a - 0.01)) a -= 0.01;
    v.line(A.P(a, A.y0), A.P(b, A.y0), C.c1, 5);
    const terms = co.map((ck, k) => Math.abs(ck) < 1e-12 ? null : fmt(ck, 4) + (k ? ' (x − x₀)' + (k > 1 ? '^' + k : '') : '')).filter(Boolean).slice(0, 5).join(' + ').replace(/\+ -/g, '− ') + (n > 4 ? ' + …' : '');
    MW.info(infoEl, 'Pₙ mit n = ' + n + ' von ' + c.name + ' in x₀ = ' + fmt(x0, 3), [['Pₙ(x)', terms || '0'],
      ['Koeffizient aₖ', 'f⁽ᵏ⁾(x₀) / k!'], ['|f − Pₙ| < 0.01 auf', '[' + fmt(a, 2) + ', ' + fmt(b, 2) + ']  (Balken auf der x-Achse)']],
      'Skript S. 10: Pₙ(x) = f(x₀) + f′(x₀)/1! (x − x₀) + … + f⁽ⁿ⁾(x₀)/n! (x − x₀)ⁿ. Beispiele im Skript: sin in x₀ = π/6 mit n = 2 (S. 10–11), eˣ in 0 (S. 11–13), cos in 0 (S. 12). Restgliedabschätzungen behandelt das Skript nicht (S. 12).');
  });
  const sx = MW.slider(ctl, { label: 'x₀', min: -3, max: 5, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  MW.slider(ctl, { label: 'n', min: 0, max: 12, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; const c = F[key], inp = sx.el.querySelector('input');
    inp.min = c.lo; inp.max = c.hi; x0 = c.x0; sx.set(x0); view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- VIII.4 Binomialreihe
W.append(dict(file='4-1-binomialreihe.html', title='Binomialreihe (1 + x)^α = Σ (α über n) xⁿ',
  sub='Die Taylorreihe von (1 + x)^α um 0 konvergiert für jedes α mindestens auf (−1, 1). Ist α eine natürliche Zahl, bricht sie ab: Dann ist sie ein Polynom und gilt für alle x. α = −1 gibt die geometrische Reihe mit Faktor −x.',
  hint='α und den Grad n verschieben.', legend=[('--c2', '(1 + x)^α'), ('--c1', 'Partialsumme vom Grad n'), ('--c3', 'Konvergenz mindestens hier')], js=AX + EXTRA + r'''
  let al = -0.5, n = 4;
  const bin = (a, k) => { let s = 1; for (let i = 0; i < k; i++) s *= (a - i) / (i + 1); return s; };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A = mkAx(-2, 2.5, -1.5, 5); axes(v, A, 'x', 'y', 0.5, 1);
    const nat = Math.abs(al - Math.round(al)) < 1e-9 && Math.round(al) >= 0;
    band(v, A, nat ? -Infinity : -1, nat ? Infinity : 1, false, false, C.c3);
    const co = []; for (let k = 0; k <= n; k++) co.push(bin(al, k));
    fplot(v, A, x => x > -1 || nat ? Math.pow(1 + x, al) : NaN, C.c2, 2.6, 800);
    fplot(v, A, x => poly(co, x), C.c1, 2.3, 800);
    const sh = co.slice(0, 5).map((c, k) => fmt(c, 4) + (k ? 'x' + (k > 1 ? '^' + k : '') : '')).join(' + ').replace(/\+ -/g, '− ');
    MW.info(infoEl, 'α = ' + fmt(al, 2) + (nat ? ' (natürliche Zahl: Polynom)' : ''), [['Reihe', sh + (n > 4 ? ' + …' : '')],
      ['(α über n) = α(α − 1)⋯(α − n + 1)/n!', fmt(co[n], 5)], ['x = 0.5:  Pₙ / f', fmt(poly(co, 0.5), 5) + ' / ' + fmt(Math.pow(1.5, al), 5)],
      ['x = 1.5:  Pₙ / f', sci(poly(co, 1.5)) + ' / ' + fmt(Math.pow(2.5, al), 5)]],
      'Skript S. 18–19: Mit f⁽ⁿ⁾(0) = α(α − 1)⋯(α − n + 1) wird die Taylorreihe (4.2) zur Binomialreihe. Sie konvergiert für jedes α wenigstens auf (−1, 1); für α ∈ {0, 1, 2, …} bricht sie ab. Beispiele im Skript: α = −1 (geometrische Reihe), α = −1/2 mit −x² (führt zu arcsin, S. 19), α = 1/2 (Ellipsenumfang, S. 23).');
  });
  MW.slider(ctl, { label: 'α', min: -2, max: 3, step: 0.05, value: al, onInput: u => { al = u; view.redraw(); } });
  MW.slider(ctl, { label: 'Grad n', min: 0, max: 25, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
'''))

# ---------------------------------------------------------------- VIII.4 Koeffizientenvergleich
W.append(dict(file='4-2-koeffizientenvergleich.html', title='Koeffizientenvergleich: Reihe eines Quotienten f = g/h',
  sub='Ansatz f = c₀ + c₁x + c₂x² + …, dann h · f = g Glied für Glied vergleichen. Das Gleichungssystem lässt sich von oben nach unten auflösen. Die Tabelle zeigt die Koeffizienten, der Graph die Partialsumme.',
  hint='Beispiel wählen und den Grad n erhöhen.', legend=[('--c2', 'f'), ('--c1', 'Partialsumme vom Grad n')], js=AX + EXTRA + r'''
  const sinC = k => k % 2 ? ((k - 1) / 2 % 2 ? -1 : 1) / fac(k) : 0, cosC = k => k % 2 ? 0 : (k / 2 % 2 ? -1 : 1) / fac(k), shC = k => k % 2 ? 1 / fac(k) : 0;
  const E = {
    tan: { name: 'tan x = sin x / cos x (Skript S. 20–21)', g: sinC, h: cosC, f: Math.tan, ax: [-2.2, 2.2, -4, 4], lim: Math.PI / 2,
      note: 'Skript S. 20–21: cos x · tan x = sin x, Koeffizientenvergleich gibt c₁ = 1, c₃ = 1/3, c₅ = 2/15. Die Reihe konvergiert für |x| < π/2 (gestrichelt). Die geraden Koeffizienten verschwinden, weil tan ungerade ist (Skript S. 21).' },
    sinh: { name: 'x / sinh x (Prüfung Herbst 1990)', g: k => k === 1 ? 1 : 0, h: shC, f: x => Math.abs(x) < 1e-9 ? 1 : x / Math.sinh(x), ax: [-5, 5, -0.5, 1.5], lim: null,
      note: 'Alte Prüfung Herbst 1990 (zweistündig), Aufgabe 6, Lösung S. 198–199: x = (c₀ + c₁x + …)(x + x³/3! + …). Ergebnis 1 − x²/6 + 7x⁴/360 + …. Hier ist g = x, also verschiebt sich der Vergleich um eine Potenz.' },
    cos1: { name: '1 / (1 + cos x) (Prüfung Frühling 1989)', g: k => k ? 0 : 1, h: k => (k ? 0 : 1) + cosC(k), f: x => 1 / (1 + Math.cos(x)), ax: [-4, 4, -0.5, 4], lim: null,
      note: 'Alte Prüfung Frühling 1989 (zweistündig), Aufgabe 4, Lösung S. 206–207: 1 = (2 − x²/2 + x⁴/24 − …)(c₀ + c₁x + …). Ergebnis 1/2 + x²/8 + x⁴/48 + …. f ist gerade, also nur gerade Potenzen.' },
  };
  let key = 'tan', n = 5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, e = E[key], A = mkAx(...e.ax); axes(v, A, 'x', 'y');
    // h·c = g rekursiv: c_k = (g_k − Σ_{j=1..k} h_j c_{k−j}) / h_0; bei sinh: h_0 = 0, also über x-Verschiebung
    const c = [];
    if (e.h(0) === 0) { for (let k = 0; k <= n; k++) { let s = e.g(k + 1); for (let j = 1; j <= k; j++) s -= e.h(j + 1) * c[k - j]; c.push(s / e.h(1)); } }
    else { for (let k = 0; k <= n; k++) { let s = e.g(k); for (let j = 1; j <= k; j++) s -= e.h(j) * c[k - j]; c.push(s / e.h(0)); } }
    if (e.lim) { [-e.lim, e.lim].forEach(x => v.line(A.P(x, A.y0), A.P(x, A.y1), C.muted, 1.2, [5, 4])); }
    fplot(v, A, e.f, C.c2, 2.6, 900); fplot(v, A, x => poly(c, x), C.c1, 2.2, 900);
    const fr = x => { if (Math.abs(x) < 1e-12) return '0'; for (let d = 1; d <= 200000; d++) { const m = x * d; if (Math.abs(m - Math.round(m)) < 1e-9) return (Math.round(m) < 0 ? '−' : '') + Math.abs(Math.round(m)) + (d > 1 ? '/' + d : ''); } return fmt(x, 6); };
    MW.info(infoEl, e.name, c.map((ck, k) => ['c' + '₀₁₂₃₄₅₆₇₈₉'[k % 10] + (k >= 10 ? '(' + k + ')' : ''), fr(ck)]).slice(0, 10), e.note);
  });
  MW.slider(ctl, { label: 'Grad n', min: 0, max: 15, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(E).map(([k, e]) => [k, e.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- VIII.5 nicht elementare Integrale
W.append(dict(file='5-1-reihen-fuer-integrale.html', title='Nicht elementare Integrale als Reihe',
  sub='Integrand in eine Potenzreihe entwickeln, dann gliedweise integrieren. Gestrichelt der numerisch berechnete Wert, durchgezogen die abgebrochene Reihe mit N Gliedern. Für kleine Parameter reichen wenige Glieder.',
  hint='Anwendung wählen und die Anzahl Glieder N erhöhen.', legend=[('--c2', 'numerischer Wert'), ('--c1', 'Reihe mit N Gliedern')], js=AX + EXTRA + r'''
  const dfr = n => { let s = 1; for (let i = 1; i <= n; i++) s *= (2 * i - 1) / (2 * i); return s; };   // 1·3⋯(2n−1) / (2·4⋯2n)
  const M = {
    pend: { name: 'Pendel: T/T₀ über Maximalausschlag α', xl: 'α in °', yl: 'T/T₀', ax: [0, 175, 0.9, 3],
      ex: a => { const k = Math.sin(a * Math.PI / 360); return 2 / Math.PI * simpson(u => 1 / Math.sqrt(1 - k * k * Math.sin(u) ** 2), 0, Math.PI / 2, 600); },
      se: (a, N) => { const k = Math.sin(a * Math.PI / 360); let s = 0; for (let n = 0; n < N; n++) s += dfr(n) ** 2 * k ** (2 * n); return s; },
      at: 60, lab: 'α = 60°', note: 'Skript S. 24–26: T = 2π√(l/g)(1 + (1/2)²k² + (1·3/(2·4))²k⁴ + …) mit k = sin(α/2). Für kleine α bleibt T ≈ T₀ = 2π√(l/g), der Wert der linearisierten Theorie. Für grosse α wird T deutlich länger.' },
    ell: { name: 'Ellipsenumfang: U/(2πa) über k² = (a² − b²)/a²', xl: 'k', yl: 'U/(2πa)', ax: [0, 1, 0.6, 1.02],
      ex: k => 2 / Math.PI * simpson(t => Math.sqrt(1 - k * k * Math.cos(t) ** 2), 0, Math.PI / 2, 600),
      se: (k, N) => { let s = 1; for (let n = 1; n < N; n++) s -= dfr(n) ** 2 * k ** (2 * n) / (2 * n - 1); return s; },
      at: 0.6, lab: 'k = 0.6', note: 'Skript S. 22–24: U = 2πa(1 − (1/2)² k²/1 − (1·3/(2·4))² k⁴/3 − …). Für kreisähnliche Ellipsen (k klein) konvergiert die Reihe schnell, für k → 1 langsam.' },
    erf: { name: 'Fehlerfunktion Φ(x) = (2/√π) ∫₀ˣ e^(−t²) dt', xl: 'x', yl: 'Φ(x)', ax: [-3, 3, -1.5, 1.5],
      ex: x => 2 / Math.sqrt(Math.PI) * simpson(t => Math.exp(-t * t), 0, x, 400),
      se: (x, N) => { let s = 0; for (let n = 0; n < N; n++) s += (n % 2 ? -1 : 1) * x ** (2 * n + 1) / ((2 * n + 1) * fac(n)); return 2 / Math.sqrt(Math.PI) * s; },
      at: 1, lab: 'x = 1', note: 'Skript S. 26–27: e^(−t²) = 1 − t² + t⁴/2! − …, gliedweise integriert Φ(x) = (2/√π)(x − x³/3 + x⁵/(5·2!) − x⁷/(7·3!) + …). Die Reihe konvergiert für alle x, braucht für grosse |x| aber viele Glieder.' },
  };
  let key = 'pend', N = 2;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, m = M[key], A = mkAx(...m.ax); axes(v, A, m.xl, m.yl);
    dplot(v, A, x => m.ex(x), C.c2, 2, key === 'pend' ? 140 : 160); fplot(v, A, x => m.se(x, N), C.c1, 2.3, 400);
    const e = m.ex(m.at), s = m.se(m.at, N); v.dot(A.P(m.at, e), C.c2, 5); v.dot(A.P(m.at, s), C.c1, 5);
    MW.info(infoEl, m.name, [['Glieder N', String(N)], [m.lab + ': Reihe', fmt(s, 6)], [m.lab + ': numerisch', fmt(e, 6)], ['Fehler', sci(Math.abs(s - e))]],
      m.note + ' Der gestrichelte Vergleichswert ist numerisch mit der Simpson-Regel berechnet (nicht aus den Kursunterlagen).');
  });
  MW.slider(ctl, { label: 'Glieder N', min: 1, max: 12, step: 1, value: N, fmt: u => fmt(u, 0), onInput: u => { N = u; view.redraw(); } });
  MW.select(ctl, 'Anwendung', Object.entries(M).map(([k, m]) => [k, m.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- VIII.5 DGL
W.append(dict(file='5-2-dgl-potenzreihenansatz.html', title='Potenzreihenansatz für Differentialgleichungen',
  sub='Ansatz y = c₀ + c₁x + c₂x² + … in die DGL einsetzen, Koeffizienten vergleichen, rekursiv auflösen. Gestrichelt die numerische Lösung, durchgezogen die Reihe mit m nicht verschwindenden Gliedern.',
  hint='DGL wählen und m erhöhen.', legend=[('--c2', 'numerische Lösung'), ('--c1', 'Reihe mit m Gliedern')], js=AX + EXTRA + r'''
  // Runge-Kutta 4 für y'' = F(x, y, y')
  const rk = (F, y0, v0, X, n = 2000) => { const h = X / n, out = [[0, y0]]; let x = 0, y = y0, v = v0;
    for (let i = 0; i < n; i++) { const k1 = [v, F(x, y, v)], k2 = [v + h / 2 * k1[1], F(x + h / 2, y + h / 2 * k1[0], v + h / 2 * k1[1])],
      k3 = [v + h / 2 * k2[1], F(x + h / 2, y + h / 2 * k2[0], v + h / 2 * k2[1])], k4 = [v + h * k3[1], F(x + h, y + h * k3[0], v + h * k3[1])];
      y += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); x += h; out.push([x, y]); } return out; };
  let key = 'x2', m = 3, a = -1;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C; let A, num, ser, rows, note;
    if (key === 'x2') {
      A = mkAx(0, 4.5, -1.5, 1.5); axes(v, A, 'x', 'y', 0.5, 0.5);
      const c = [0, 1]; for (let k = 2; k <= 4 * m + 2; k++) c[k] = k < 4 ? 0 : -c[k - 4] / ((k - 1) * k);
      num = rk((x, y) => -x * x * y, 0, 1, 4.5); ser = x => poly(c, x);
      const nz = c.map((ck, k) => [k, ck]).filter(p => p[1] !== 0).slice(0, m);
      rows = [['Rekursion', 'c₂ = c₃ = 0,  (k + 3)(k + 4) cₖ₊₄ = −cₖ'], ['Reihe', nz.slice(0, 4).map(([k, ck]) => (ck < 0 ? '− ' : '+ ') + (k === 1 ? 'x' : 'x^' + k + '/' + fmt(Math.round(1 / Math.abs(ck)), 0))).join(' ').replace(/^\+ /, '') + (m > 4 ? ' …' : '')]];
      note = 'Skript S. 32–33: y″ + x²y = 0 mit y(0) = 0, y′(0) = 1. Koeffizientenvergleich: 2c₂ = 0, 2·3c₃ = 0, 3·4c₄ + c₀ = 0, 4·5c₅ + c₁ = 0, …, also y = x − x⁵/(4·5) + x⁹/(4·5·8·9) − …. Die Lösung ist nicht elementar; die Reihe konvergiert für alle x (Skript S. 33).';
    } else {
      A = mkAx(0, 3, -0.5, 3); axes(v, A, 'x', 'y', 0.5, 0.5);
      const c = []; for (let k = 0; k < m; k++) c.push(a ** k / fac(k));
      num = null; ser = x => poly(c, x); dplot(v, A, x => Math.exp(a * x), C.c2, 2, 200);
      rows = [['Rekursion', 'k cₖ = a cₖ₋₁,  c₀ = y(0) = 1'], ['cₖ', 'aᵏ/k!'], ['Reihe', '1 + ax + (ax)²/2! + … = e^(ax)']];
      note = 'Skript S. 31–32: y′ = a y mit y(0) = 1. Einsetzen gibt c₁ = a c₀, 2c₂ = a c₁, 3c₃ = a c₂, …, also cₖ = aᵏ/k!. Die Reihe ist die Exponentialreihe von e^(ax), keineswegs überraschend.';
    }
    if (num) { const seg = num.filter(p => A.inY(p[1])).map(p => A.P(p[0], p[1])); v.poly(seg, C.c2, 2, [5, 4]); }
    fplot(v, A, ser, C.c1, 2.3, 600);
    const xe = key === 'x2' ? 3 : 2, ye = key === 'x2' ? num[Math.round(3 / 4.5 * 2000)][1] : Math.exp(a * 2);
    rows.push(['x = ' + xe + ': Reihe / Lösung', fmt(ser(xe), 5) + ' / ' + fmt(ye, 5)]);
    MW.info(infoEl, key === 'x2' ? 'y″ + x² y = 0,  y(0) = 0,  y′(0) = 1' : 'y′ = ' + fmt(a, 2) + ' · y,  y(0) = 1', rows, note);
  });
  const sa = MW.slider(ctl, { label: 'a', min: -2, max: 1, step: 0.1, value: a, onInput: u => { a = u; view.redraw(); } });
  MW.slider(ctl, { label: 'Glieder m', min: 1, max: 12, step: 1, value: m, fmt: u => fmt(u, 0), onInput: u => { m = u; view.redraw(); } });
  MW.select(ctl, 'DGL', [['x2', 'y″ + x²y = 0 (Skript S. 32)'], ['ay', 'y′ = ay (Skript S. 31)']], u => { key = u; sa.el.style.display = key === 'ay' ? '' : 'none'; view.redraw(); }).set(key);
  sa.el.style.display = 'none';
'''))

if __name__ == '__main__':
    print(build('analysis-w11', W))
