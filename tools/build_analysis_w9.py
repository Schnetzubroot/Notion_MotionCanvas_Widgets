"""Widgets zu Analysis I, Woche 9: Kap. II.8 (Tangente, Zykloide, Krümmung, Krümmungskreis, Evolute; Skript Teil A,
Kap. II, S. 69-79; Vorlesung 20 vom 09.11.2026, Notizen Kap. II S. 42-47) und Kap. III.1-2 (bestimmtes Integral,
Riemann'sche Summe, Mittelwertsatz der Integralrechnung, Hauptsatz; Skript Teil A, Kap. III, S. 3-11).
Zu Kap. III gibt es keine Vorlesungsnotizen."""
from template import build
from build_analysis_w1 import AX, BOX
from build_analysis_w8 import EXTRA

EXTRA9 = EXTRA + r'''
  const simpson = (f, a, b, n = 400) => { if (a === b) return 0; const h = (b - a) / n; let s = f(a) + f(b); for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2); return s * h / 3; };
  const POS = 'rgba(47, 111, 219, 0.22)', NEG = 'rgba(209, 69, 59, 0.22)';
  // Fläche zwischen Graph und x-Achse von a bis b, oberhalb blau, unterhalb rot
  function area(v, A, f, a, b, N = 300) { if (a === b) return; const lo = Math.min(a, b), hi = Math.max(a, b), dx = (hi - lo) / N;
    for (let i = 0; i < N; i++) { const x0 = lo + i * dx, x1 = x0 + dx, y0 = f(x0), y1 = f(x1), cy = A.y0 <= 0 && A.y1 >= 0 ? 0 : A.y0;
      const cl = y => Math.max(A.y0, Math.min(A.y1, y));
      v.poly([A.P(x0, cy), A.P(x0, cl(y0)), A.P(x1, cl(y1)), A.P(x1, cy)], null, 0, null, true, (y0 + y1) >= 0 ? POS : NEG); } }
'''

W = []

# ---------------------------------------------------------------- II.8 Zykloide, Tangente, Normale
W.append(dict(file='8-3-zykloide-tangente.html', title='Zykloide, Tangenten- und Normalenvektor',
  sub='Ein Rad mit Radius a = 1 rollt auf der x-Achse. Ein Punkt im Abstand b vom Mittelpunkt beschreibt r(t) = (t − b sin t, 1 − b cos t). Der Tangentenvektor ṙ(t) = (ẋ, ẏ) zeigt in Laufrichtung, der Normalenvektor n = (−ẏ, ẋ) steht senkrecht darauf.',
  hint='t abspielen oder ziehen, b verändern. Bei b = 1 ist ṙ(0) = 0: Spitze.', legend=[('--c2', 'Bahnkurve'), ('--c1', 'Tangentenvektor ṙ'), ('--c3', 'Normalenvektor n'), ('--c4', 'Rad')], js=AX + EXTRA9 + r'''
  let key = 'zyk', b = 1, t = 2;
  const K = {
    zyk: { name: 'Zykloide', r: t => [t - b * Math.sin(t), 1 - b * Math.cos(t)], d: t => [1 - b * Math.cos(t), b * Math.sin(t)], T: [0, 4 * Math.PI], ax: [2 * Math.PI, 1.3, 7] },
    zw: { name: 'Zwiebelkurve (cos t, sin 2t)', r: t => [Math.cos(t), Math.sin(2 * t)], d: t => [-Math.sin(t), 2 * Math.cos(2 * t)], T: [0, 2 * Math.PI], ax: [0, 0, 2.1] },
  };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = K[key], A = eqAx(...c.ax); axes(v, A, 'x', 'y', key === 'zyk' ? Math.PI : 0.5, key === 'zyk' ? 1 : 0.5);
    cplot(v, A, c.r, c.T[0], c.T[1], C.c2, 2.2, 1200);
    const tt = Math.min(c.T[1], t), p = c.r(tt), d = c.d(tt), L = Math.hypot(...d), n = [-d[1], d[0]];
    if (key === 'zyk') { v.circle(A.P(tt, 1), A.X(1) - A.X(0), C.c4, 1.5); v.line(A.P(tt, 1), A.P(...p), C.c4, 1.5); v.dot(A.P(tt, 1), C.c4, 3); }
    else { [Math.PI / 4, 3 * Math.PI / 4, 5 * Math.PI / 4, 7 * Math.PI / 4].forEach(s => v.dot(A.P(...c.r(s)), C.c5, 5, true)); [0, Math.PI].forEach(s => v.dot(A.P(...c.r(s)), C.c4, 5, true)); }
    const sc = key === 'zyk' ? 1 : 0.4;
    v.arrow(A.P(...p), [(A.X(d[0] * sc) - A.X(0)), (A.Y(d[1] * sc) - A.Y(0))], C.c1, 2.5);
    v.arrow(A.P(...p), [(A.X(n[0] * sc) - A.X(0)), (A.Y(n[1] * sc) - A.Y(0))], C.c3, 2);
    v.dot(A.P(...p), C.fg, 5);
    const slope = Math.abs(d[0]) < 1e-9 ? (Math.abs(d[1]) < 1e-9 ? 'nicht definiert (ṙ = 0)' : 'vertikal') : fmt(d[1] / d[0], 4);
    const note = key === 'zyk' ? 'Notizen Kap. II S. 42–44 und Skript S. 70: b = a gewöhnliche, b > a verlängerte, b < a verkürzte Zykloide. Für b = a ist ṙ(2kπ) = 0: Die Kurve hat dort eine Spitze, obwohl x(t) und y(t) beliebig oft differenzierbar sind (singulärer Punkt).'
      : 'Notizen Kap. II S. 45 und Skript S. 70–71: ẏ = 2 cos 2t = 0 für t = π/4 + kπ/2 (horizontale Tangenten in (±1/√2, ±1), violett), ẋ = −sin t = 0 für t = 0, π (vertikale Tangenten, gelb). Im Ursprung (t = π/2, 3π/2) kreuzt sich die Kurve mit den Steigungen ±2.';
    MW.info(infoEl, c.name + ',  t = ' + fmt(tt, 3), [['r(t)', fv(p, 4)], ['ṙ(t) = (ẋ, ẏ)', fv(d, 4)], ['|ṙ(t)|', fmt(L, 4)], ['Steigung ẏ/ẋ', slope], ['Normale n = (−ẏ, ẋ)', fv(n, 4)], ['Tangente', 'R(s) = r(t) + s · ṙ(t)']], note);
  });
  const pl = MW.player(ctl, { label: 't', t0: 0, t1: 4 * Math.PI, value: t, onTime: u => { t = u; view.redraw(); } });
  const sb = MW.slider(ctl, { label: 'b', min: 0, max: 2, step: 0.01, value: b, onInput: u => { b = u; view.redraw(); } });
  MW.select(ctl, 'Kurve', [['zyk', 'Zykloide'], ['zw', 'Zwiebelkurve (cos t, sin 2t)']], u => { key = u; sb.el.style.display = u === 'zyk' ? '' : 'none'; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- II.8 Krümmung, Krümmungskreis, Evolute
W.append(dict(file='8-4-kruemmungskreis.html', title='Krümmung, Krümmungskreis und Evolute',
  sub='k = (ẋÿ − ẏẍ)/(ẋ² + ẏ²)^(3/2). k > 0: Linkskurve, k < 0: Rechtskurve. Der Krümmungskreis hat Radius 1/|k| und schmiegt sich der Kurve an. Seine Mittelpunkte bilden die Evolute.',
  hint='Kurve wählen und t verschieben. Die Evolute lässt sich einblenden.', legend=[('--c2', 'Kurve'), ('--c1', 'Krümmungskreis'), ('--c5', 'Evolute'), ('--c3', 'Normale m')], js=AX + EXTRA9 + r'''
  const s = Math.sin, c = Math.cos;
  const K = {
    ell: { name: 'Ellipse (2 cos t, sin t)', r: t => [2 * c(t), s(t)], d: t => [-2 * s(t), c(t)], dd: t => [-2 * c(t), -s(t)], T: [0, 2 * Math.PI], ax: [0, 0, 3.2],
      note: 'Skript S. 73: k(t) = ab/(a² sin² t + b² cos² t)^(3/2). Scheitel: k(0) = a/b² = 2, k(π/2) = b/a² = 1/4. Die Evolute hat vier Spitzen, jeweils gegenüber einem Scheitel (eigene Beobachtung).' },
    par: { name: 'Parabel (t, t²)', r: t => [t, t * t], d: t => [1, 2 * t], dd: t => [0, 2], T: [-2, 2], ax: [0, 1.4, 2.6],
      note: 'Skript S. 75–76: k(t) = 2/(1 + 4t²)^(3/2), Evolute (−4t³, 1/2 + 3t²), explizit y = 1/2 + 3 (x/4)^(2/3) (Neil’sche Parabel).' },
    sin: { name: 'Sinuskurve (t, sin t)', r: t => [t, s(t)], d: t => [1, c(t)], dd: t => [0, -s(t)], T: [-1, 7.3], ax: [3.14, 0, 4.4],
      note: 'k = −sin t/(1 + cos² t)^(3/2) (eigene Rechnung mit der Formel aus Skript S. 73). k wechselt bei t = kπ das Vorzeichen: dort liegen die Wendepunkte (Notizen Kap. II S. 47).' },
    zyk: { name: 'Zykloide (t − sin t, 1 − cos t)', r: t => [t - s(t), 1 - c(t)], d: t => [1 - c(t), s(t)], dd: t => [s(t), c(t)], T: [0.05, 2 * Math.PI - 0.05], ax: [Math.PI, 0, 4.2],
      note: 'Skript S. 74–75: k(t) = −1/(2a √(2(1 − cos t))) mit a = 1, also überall Rechtskurve. Die Evolute (at + a sin t, −a + a cos t) ist wieder eine Zykloide, um (aπ, −2a) verschoben.' },
    evo: { name: 'Kreisevolvente (Prüfung HS23)', r: t => [c(t) + t * s(t), s(t) - t * c(t)], d: t => [t * c(t), t * s(t)], dd: t => [c(t) - t * s(t), s(t) + t * c(t)], T: [0.05, 3 * Math.PI], ax: [0, 0, 10],
      note: 'Übung 9, Folie 8 (Prüfung HS23, A1): r(t) = (cos t, sin t) + t (sin t, −cos t). Eigene Rechnung: ṙ = (t cos t, t sin t), ẋÿ − ẏẍ = t², also k(t) = 1/t. Die Evolute ist der Einheitskreis (der Faden wird von ihm abgewickelt).' },
  };
  let key = 'ell', u = 0.3, ev = true;
  const kr = (cc, t) => { const d = cc.d(t), e = cc.dd(t), L = Math.hypot(...d); return { k: (d[0] * e[1] - d[1] * e[0]) / L ** 3, m: [-d[1] / L, d[0] / L], d, L }; };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, cc = K[key], A = eqAx(...cc.ax); axes(v, A, 'x', 'y', cc.ax[2] > 6 ? 2 : cc.ax[2] > 3.5 ? 1 : 0.5, cc.ax[2] > 6 ? 2 : cc.ax[2] > 3.5 ? 1 : 0.5);
    if (ev) cplot(v, A, t => { const q = kr(cc, t), p = cc.r(t); return Math.abs(q.k) < 1e-3 ? [NaN, NaN] : [p[0] + q.m[0] / q.k, p[1] + q.m[1] / q.k]; }, cc.T[0], cc.T[1], C.c5, 1.6, 1500);
    cplot(v, A, cc.r, cc.T[0], cc.T[1], C.c2, 2.6, 1200);
    const t = cc.T[0] + (cc.T[1] - cc.T[0]) * u, p = cc.r(t), q = kr(cc, t);
    v.arrow(A.P(...p), [A.X(q.m[0]) - A.X(0), A.Y(q.m[1]) - A.Y(0)], C.c3, 2);
    let rows = [['t', fmt(t, 3)], ['r(t)', fv(p, 4)], ['k(t)', fmt(q.k, 5) + (q.k > 1e-9 ? '  (Linkskurve)' : q.k < -1e-9 ? '  (Rechtskurve)' : '  (k = 0)')]];
    if (Math.abs(q.k) > 1e-6) { const R = 1 / Math.abs(q.k), M = [p[0] + q.m[0] / q.k, p[1] + q.m[1] / q.k];
      v.circle(A.P(...M), (A.X(R) - A.X(0)), C.c1, 1.8); v.line(A.P(...p), A.P(...M), C.c1, 1, [4, 4]); v.dot(A.P(...M), C.c1, 4.5);
      rows = rows.concat([['Krümmungsradius 1/|k|', fmt(R, 4)], ['Mittelpunkt M = r + (1/k) m', fv(M, 4)]]); }
    else rows.push(['Krümmungskreis', 'entartet (k = 0, Gerade)']);
    v.dot(A.P(...p), C.fg, 5.5);
    MW.info(infoEl, cc.name, rows, 'Skript S. 72–74: m = (−ẏ, ẋ)/√(ẋ² + ẏ²) ist der Normaleneinheitsvektor nach links. Für k < 0 liegt M auf der rechten Seite. ' + cc.note);
  });
  MW.slider(ctl, { label: 't (Anteil)', min: 0, max: 1, step: 0.001, value: u, fmt: z => fmt(z * 100, 1) + ' %', onInput: z => { u = z; view.redraw(); } });
  MW.select(ctl, 'Kurve', Object.entries(K).map(([q, cc]) => [q, cc.name]), z => { key = z; view.redraw(); }).set(key);
  MW.check(ctl, 'Evolute zeigen', ev, z => { ev = z; view.redraw(); });
'''))

# ---------------------------------------------------------------- III.1 Riemannsumme
W.append(dict(file='III-1-riemannsumme.html', title='Riemann’sche Summe und bestimmtes Integral',
  sub='Teile [a, b] in n Stücke, wähle in jedem einen Zwischenpunkt ξₖ und addiere f(ξₖ)·Δxₖ. Wird die Einteilung feiner, strebt die Summe gegen das Integral. Flächen unterhalb der x-Achse zählen negativ.',
  hint='Funktion, n und die Lage der Zwischenpunkte ξₖ wählen.', legend=[('--c2', 'f'), ('--c1', 'Zwischenpunkte (ξₖ, f(ξₖ))')], js=AX + EXTRA9 + r'''
  const F = {
    x2: { name: 'x² auf [0, 2]', f: x => x * x, a: 0, b: 2, I: 8 / 3, Is: 'b³/3 = 8/3', note: 'Skript S. 4–5: Mit ξₖ = xₖ (rechte Endpunkte) und 1² + … + n² = n(n + 1)(2n + 1)/6 ergibt sich ∫₀ᵇ x² dx = b³/3.' },
    sin: { name: 'sin x auf [0, 3π/2]', f: Math.sin, a: 0, b: 1.5 * Math.PI, I: 1, Is: '[−cos x] = 0 + 1 = 1', note: 'Der Teil unter der x-Achse (π bis 3π/2) zählt negativ (Skript S. 4). Ergebnis mit dem Hauptsatz (Skript S. 11).' },
    cub: { name: 'x³ − 3x auf [−2, 2.5]', f: x => x ** 3 - 3 * x, a: -2, b: 2.5, I: (2.5 ** 4 / 4 - 1.5 * 2.5 ** 2) - (16 / 4 - 6), Is: '[x⁴/4 − 3x²/2] von −2 bis 2.5', note: 'Eigenes Beispiel. Die positiven und negativen Anteile heben sich teilweise auf.' },
    exp: { name: 'eˣ auf [0, 1]', f: Math.exp, a: 0, b: 1, I: Math.E - 1, Is: 'e − 1', note: 'Eigenes Beispiel; Stammfunktion eˣ (Skript S. 12).' },
  };
  let key = 'x2', n = 6, mode = 'r', seed = 1;
  const rnd = i => { const x = Math.sin((i + 1) * 12.9898 * seed) * 43758.5453; return x - Math.floor(x); };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = F[key], [y0, y1] = range(c.f, c.a, c.b), A = mkAx(c.a - 0.05 * (c.b - c.a), c.b + 0.05 * (c.b - c.a), Math.min(y0, -0.1), Math.max(y1, 0.1)); axes(v, A, 'x', 'y');
    const dx = (c.b - c.a) / n; let S = 0;
    for (let k = 0; k < n; k++) { const xl = c.a + k * dx, t = mode === 'l' ? 0 : mode === 'm' ? 0.5 : mode === 'r' ? 1 : rnd(k), xi = xl + t * dx, y = c.f(xi); S += y * dx;
      v.poly([A.P(xl, 0), A.P(xl, y), A.P(xl + dx, y), A.P(xl + dx, 0)], C.muted, 1, null, true, y >= 0 ? POS : NEG);
      if (n <= 80) v.dot(A.P(xi, y), C.c1, n > 30 ? 2.5 : 4); }
    fplot(v, A, c.f, C.c2, 2.6, 600);
    MW.info(infoEl, c.name + ',  n = ' + n, [['Feinheit Δx', fmt(dx, 5)], ['Riemann’sche Summe Σ f(ξₖ) Δxₖ', fmt(S, 6)], ['Integral', fmt(c.I, 6) + '  (' + c.Is + ')'], ['Fehler', fmt(S - c.I, 6)]],
      'Skript S. 3–4 (Definition nach Riemann): Für stetiges f existiert der Grenzwert und hängt weder von der Einteilung noch von den Zwischenpunkten ab. ' + c.note);
  });
  MW.slider(ctl, { label: 'n', min: 1, max: 200, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'ξₖ', [['l', 'linker Rand'], ['m', 'Mitte'], ['r', 'rechter Rand'], ['z', 'zufällig']], u => { mode = u; seed = 1 + Math.random(); view.redraw(); }).set(mode);
  MW.select(ctl, 'Funktion', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- III.2 Hauptsatz und MWS
W.append(dict(file='III-2-hauptsatz.html', title='Hauptsatz: Fₐ(x) = ∫ₐˣ f(t) dt hat die Ableitung f(x)',
  sub='Oben: die Fläche unter f von a bis x (blau positiv, rot negativ) und das Rechteck aus dem Mittelwertsatz mit Höhe f(ξ). Unten: die Flächenfunktion Fₐ. Ihre Tangente in x hat genau die Steigung f(x).',
  hint='Funktion wählen und die obere Grenze x verschieben.', legend=[('--c2', 'f (oben)'), ('--c3', 'Fₐ (unten)'), ('--c1', 'Tangente an Fₐ, Steigung f(x)'), ('--c4', 'Mittelwert-Rechteck')], tall=True, js=AX + EXTRA9 + r'''
  const F = {
    sin: { name: 'sin t, a = 0', f: Math.sin, a: 0, r: [-0.5, 7], Fs: '1 − cos x' },
    lin: { name: 't² − 1, a = −1.5', f: t => t * t - 1, a: -1.5, r: [-2, 2.2], Fs: 'x³/3 − x − 0.375' },
    gauss: { name: 'e^(−t²) (nicht elementar), a = 0', f: t => Math.exp(-t * t), a: 0, r: [-3, 3], Fs: 'nicht elementar ausdrückbar (Skript S. 14)' },
    inv: { name: '1/t, a = 1', f: t => 1 / t, a: 1, r: [0.15, 5], Fs: 'log x' },
  };
  let key = 'sin', x = 2;
  const view = MW.View2D(cv, { xmin: -0.75, xmax: 6.25, ymin: -0.45, ymax: 4.15 }, v => {
    const C = v.C, c = F[key], [a0, b0] = c.r, Fa = s => simpson(c.f, c.a, s, 200);
    const [fy0, fy1] = range(c.f, a0, b0), [Fy0, Fy1] = range(Fa, a0, b0, 120);
    const T = mkAx(a0, b0, Math.min(fy0, -0.1), Math.max(fy1, 0.1), 6, 1.75, 0, 1.95), B = mkAx(a0, b0, Math.min(Fy0, -0.1), Math.max(Fy1, 0.1), 6, 1.75, 0, 0);
    axes(v, T, 't', 'f'); axes(v, B, 'x', 'Fₐ');
    area(v, T, c.f, c.a, x);
    const I = Fa(x), mean = x !== c.a ? I / (x - c.a) : c.f(x);
    // ξ aus dem Mittelwertsatz
    const xs = x !== c.a ? roots(s => c.f(s) - mean, Math.min(c.a, x), Math.max(c.a, x), 600) : [x];
    if (x !== c.a) v.poly([T.P(c.a, 0), T.P(c.a, mean), T.P(x, mean), T.P(x, 0)], C.c4, 1.5, [5, 4], true);
    fplot(v, T, c.f, C.c2, 2.4, 600); v.line(T.P(c.a, T.y0), T.P(c.a, T.y1), C.muted, 1, [3, 3]); v.text(T.P(c.a, T.y0), 'a', C.muted, 4, -4, 12);
    xs.slice(0, 2).forEach(s => { v.dot(T.P(s, c.f(s)), C.c4, 4.5); v.text(T.P(s, T.y0), 'ξ', C.c4, -3, -4, 12); });
    v.line(T.P(x, T.y0), T.P(x, T.y1), C.fg, 1, [2, 3]); v.dot(T.P(x, c.f(x)), C.fg, 5);
    fplot(v, B, Fa, C.c3, 2.4, 150);
    const m = c.f(x), h = 0.18 * (b0 - a0); v.line(B.P(x - h, I - m * h), B.P(x + h, I + m * h), C.c1, 2);
    v.dot(B.P(x, I), C.fg, 5);
    MW.info(infoEl, c.name + ',  x = ' + fmt(x, 3), [['Fₐ(x) = ∫ₐˣ f(t) dt', fmt(I, 5)], ['Steigung der Tangente an Fₐ', fmt((Fa(x + 1e-4) - Fa(x - 1e-4)) / 2e-4, 5)], ['f(x)', fmt(m, 5)], ['Mittelwert Fₐ(x)/(x − a) = f(ξ)', fmt(mean, 5)], ['ξ', xs.length ? xs.slice(0, 2).map(s => fmt(s, 4)).join(', ') : '–'], ['geschlossen', c.Fs]],
      'Skript S. 7–10: Mittelwertsatz der Integralrechnung (b − a) f(ξ) = ∫ₐᵇ f(x) dx, daraus der Hauptsatz d/dx ∫ₐˣ f(t) dt = f(x). Fₐ ist eine Stammfunktion von f; jede andere unterscheidet sich nur um eine Konstante (Skript S. 10). Fₐ wird hier numerisch (Simpson) berechnet.');
  });
  const sx = MW.slider(ctl, { label: 'x', min: -0.5, max: 7, step: 0.01, value: x, onInput: u => { x = u; view.redraw(); } });
  MW.select(ctl, 'f', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; const c = F[u], i = sx.el.querySelector('input'); i.min = c.r[0]; i.max = c.r[1]; x = Math.min(c.r[1], c.a + 1.3); sx.set(x); view.redraw(); }).set(key);
'''))

if __name__ == '__main__':
    print(build('analysis-w9', W))
