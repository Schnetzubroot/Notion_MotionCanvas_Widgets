"""Widgets zu Analysis I, Woche 8: Kap. II.7-8 (Stammbach, Teil A, Kap. II, S. 57-69 und 76-79).
Höhere Ableitungen, konvex/konkav, Wende- und Sattelpunkte, harmonische Schwingung,
Darstellungsformen ebener Kurven, Kurven in Polarkoordinaten.
Vorlesung 18 (04.11.2026) und 19 (06.11.2026), Notizen Kap. II S. 30-41."""
from template import build
from build_analysis_w1 import AX, BOX

EXTRA = r'''
  function dplot(v, A, f, color, w = 1.3, N = 300, a = A.x0, b = A.x1) { let seg = [];
    const fl = () => { if (seg.length > 1) v.poly(seg, color, w, [5, 4]); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x); if (!isFinite(y) || !A.inY(y)) { fl(); continue; } seg.push(A.P(x, y)); } fl(); }
  const KX = 'rgba(15, 157, 88, 0.11)', KV = 'rgba(209, 69, 59, 0.10)';
  // gleiche Skalierung in x und y (Zeichenfläche 6 × 3.4)
  const eqAx = (xc, yc, hw) => mkAx(xc - hw, xc + hw, yc - hw * 3.4 / 6, yc + hw * 3.4 / 6);
  const range = (f, a, b, N = 400) => { let lo = Infinity, hi = -Infinity; for (let i = 0; i <= N; i++) { const y = f(a + (b - a) * i / N); if (isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); } } const p = 0.08 * (hi - lo || 1); return [lo - p, hi + p]; };
  const roots = (g, a, b, N = 2000) => { const r = []; let px = a, pg = g(a);
    for (let i = 1; i <= N; i++) { const x = a + (b - a) * i / N, y = g(x); if (isFinite(y) && isFinite(pg) && pg * y < 0) { let l = px, h = x; for (let k = 0; k < 60; k++) { const m = (l + h) / 2; (g(l) * g(m) <= 0) ? h = m : l = m; } r.push((l + h) / 2); } px = x; pg = y; } return r; };
  const cplot = (v, A, r, t0, t1, color, w = 2.2, N = 600) => { let seg = []; const fl = () => { if (seg.length > 1) v.poly(seg, color, w); seg = []; };
    for (let i = 0; i <= N; i++) { const p = r(t0 + (t1 - t0) * i / N); if (!isFinite(p[0]) || !isFinite(p[1]) || !A.inY(p[1]) || p[0] < A.x0 || p[0] > A.x1) { fl(); continue; } seg.push(A.P(p[0], p[1])); } fl(); };
'''

W = []

# ---------------------------------------------------------------- II.7 konvex / konkav
W.append(dict(file='7-1-konvex-konkav.html', title='Zweite Ableitung: konvex (Linkskurve) und konkav (Rechtskurve)',
  sub='Wo f″ > 0 ist, wächst die Steigung: der Graph ist nach links gekrümmt (konvex, grün hinterlegt). Wo f″ < 0 ist, ist er nach rechts gekrümmt (konkav, rot hinterlegt). Wechselt f″ das Vorzeichen, liegt ein Wendepunkt vor.',
  hint='Funktion wählen und x₀ verschieben. f′ und f″ lassen sich einblenden.', legend=[('--c2', 'f'), ('--c4', 'f′'), ('--c5', 'f″'), ('--c1', 'Tangente in x₀')], js=AX + EXTRA + r'''
  const cb = x => Math.cbrt(x);
  const F = {
    poly: { name: 'Polynom aus dem Skript (S. 58)', a: -5.6, b: 6.6,
      f: x => x ** 5 - 3.5 * x ** 4 - 32 * x ** 3 + 88.5 * x ** 2 + 126 * x - 270, d1: x => 5 * x ** 4 - 14 * x ** 3 - 96 * x ** 2 + 177 * x + 126, d2: x => 20 * x ** 3 - 42 * x ** 2 - 192 * x + 177,
      note: 'Skript S. 57–58 (Fig. 1): f(x) = x⁵ − 7/2 x⁴ − 32x³ + 177/2 x² + 126x − 270 = ½(x + 5)(x + 2)(2x − 3)(x − 3)(x − 6). Lokale Extrema bei den Nullstellen von f′, Wendepunkte bei den Nullstellen von f″ (x ≈ −2.69, 0.83, 3.96). Die Graphen von f′ und f″ sind hier gestaucht dargestellt (eigene Skalierung).' },
    gauss: { name: 'Glockenkurve e^(−x²/2)', a: -4, b: 4,
      f: x => Math.exp(-x * x / 2), d1: x => -x * Math.exp(-x * x / 2), d2: x => (x * x - 1) * Math.exp(-x * x / 2),
      note: 'Vorlesung 18, Notizen Kap. II S. 34 und Skript S. 60–61: f′(x) = −x e^(−x²/2), f″(x) = (x² − 1) e^(−x²/2). Wendepunkte bei x = ±1, also (±1, e^(−1/2)). Für |x| < 1 Rechtskurve, für |x| > 1 Linkskurve.' },
    cube: { name: 'x³ (Sattelpunkt)', a: -2, b: 2,
      f: x => x ** 3, d1: x => 3 * x * x, d2: x => 6 * x,
      note: 'Notizen Kap. II S. 33: f″(x) = 6x wechselt in 0 das Vorzeichen und f′(0) = 0. Also ist 0 ein Sattelpunkt (ein Wendepunkt mit waagrechter Tangente).' },
    sin: { name: 'sin x (Wendepunkt, kein Sattel)', a: -4, b: 4,
      f: Math.sin, d1: Math.cos, d2: x => -Math.sin(x),
      note: 'Notizen Kap. II S. 33: f″(x) = −sin x wechselt in 0 das Vorzeichen, aber f′(0) = cos 0 = 1 ≠ 0. Also Wendepunkt, aber kein Sattelpunkt.' },
    root: { name: '∛(x + 1) (senkrechte Tangente)', a: -3, b: 1,
      f: x => cb(x + 1), d1: x => 1 / (3 * cb(x + 1) ** 2), d2: x => -2 / (9 * cb(x + 1) ** 5),
      note: 'Notizen Kap. II S. 34: Bei x = −1 geht eine Links- in eine Rechtskurve über, aber f′(−1) und f″(−1) existieren nicht (senkrechte Tangente). Nach der Definition der Vorlesung (f″(x₀) = 0 nötig) ist das kein Wendepunkt. Das Skript (S. 58, mit (x − 1)^(1/3)) beschreibt nur den Wechsel von konvex zu konkav.' },
  };
  let key = 'gauss', x0 = 0.5, s1 = false, s2 = true;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = F[key], [y0, y1] = range(c.f, c.a, c.b), A = mkAx(c.a, c.b, y0, y1); axes(v, A, 'x', 'y');
    // Hintergrund nach Vorzeichen von f″
    const N = 300, dx = (c.b - c.a) / N;
    for (let i = 0; i < N; i++) { const x = c.a + (i + 0.5) * dx, s = c.d2(x); if (!isFinite(s) || s === 0) continue;
      v.poly([A.P(c.a + i * dx, y0), A.P(c.a + (i + 1) * dx + 1e-9, y0), A.P(c.a + (i + 1) * dx + 1e-9, y1), A.P(c.a + i * dx, y1)], null, 0, null, true, s > 0 ? KX : KV); }
    // f′, f″ skaliert, damit sie ins Bild passen
    const sc = g => { const [l, h] = range(g, c.a, c.b); const m = Math.max(Math.abs(l), Math.abs(h)), M = Math.max(Math.abs(y0), Math.abs(y1)); return m > M ? M / m : 1; };
    const k1 = sc(c.d1), k2 = sc(c.d2);
    if (s1) fplot(v, A, x => k1 * c.d1(x), C.c4, 1.6, 600);
    if (s2) fplot(v, A, x => k2 * c.d2(x), C.c5, 1.6, 600);
    fplot(v, A, c.f, C.c2, 2.6, 800);
    const W = roots(c.d2, c.a, c.b).filter(x => Math.abs(c.d2(x)) < 1e-6 || key !== 'root');
    W.forEach(x => { const sad = Math.abs(c.d1(x)) < 1e-6; v.dot(A.P(x, c.f(x)), sad ? C.c1 : C.c5, 6, true); v.text(A.P(x, c.f(x)), sad ? 'S' : 'W', sad ? C.c1 : C.c5, 8, 16, 12); });
    const fx = c.f(x0), m = c.d1(x0), q = c.d2(x0);
    if (isFinite(m)) fplot(v, A, x => fx + m * (x - x0), C.c1, 1.5, 4);
    v.dot(A.P(x0, fx), C.fg, 5);
    const bend = !isFinite(q) ? 'nicht definiert' : q > 1e-9 ? 'f″ > 0: Linkskurve (konvex)' : q < -1e-9 ? 'f″ < 0: Rechtskurve (konkav)' : 'f″ = 0';
    MW.info(infoEl, c.name + ', x₀ = ' + fmt(x0, 2), [['f(x₀)', fmt(fx, 4)], ['f′(x₀)', isFinite(m) ? fmt(m, 4) : 'existiert nicht'], ['f″(x₀)', isFinite(q) ? fmt(q, 4) : 'existiert nicht'], ['Krümmung', bend],
      ['Wendepunkte (W) / Sattelpunkte (S)', W.length ? W.map(x => 'x ≈ ' + fmt(x, 3) + (Math.abs(c.d1(x)) < 1e-6 ? ' (S)' : '')).join(', ') : 'keine']].concat(s1 || s2 ? [['Skalierung', 'f′ × ' + fmt(k1, 3) + ',  f″ × ' + fmt(k2, 3)]] : []), c.note);
  });
  const sx = MW.slider(ctl, { label: 'x₀', min: -4, max: 4, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; const c = F[u]; const i = sx.el.querySelector('input'); i.min = c.a; i.max = c.b; x0 = Math.min(c.b, Math.max(c.a, (c.a + c.b) / 2 + 0.37)); sx.set(x0); view.redraw(); }).set(key);
  MW.check(ctl, 'f′ zeigen', s1, u => { s1 = u; view.redraw(); });
  MW.check(ctl, 'f″ zeigen', s2, u => { s2 = u; view.redraw(); });
'''))

# ---------------------------------------------------------------- II.7 Kriterium mit höheren Ableitungen
W.append(dict(file='7-2-hoehere-ableitungen-test.html', title='Extremum oder Sattelpunkt? Die erste nicht verschwindende Ableitung entscheidet',
  sub='Sind f′(x₀) = … = f⁽ⁿ⁻¹⁾(x₀) = 0, aber f⁽ⁿ⁾(x₀) ≠ 0, dann gilt: n gerade ergibt ein lokales Extremum, n ungerade einen Sattelpunkt (Vorlesung 18, Notizen S. 33).',
  hint='Funktion wählen und den Exponenten n ändern.', legend=[('--c2', 'f'), ('--c1', 'x₀')], js=AX + EXTRA + r'''
  const fac = k => { let s = 1; for (let i = 2; i <= k; i++) s *= i; return s; };
  const F = {
    pow: { name: 'xⁿ in x₀ = 0', f: (x, n) => x ** n, ders: n => Array.from({ length: n + 1 }, (_, k) => k === n ? fac(n) : 0) },
    neg: { name: '−xⁿ in x₀ = 0', f: (x, n) => -(x ** n), ders: n => Array.from({ length: n + 1 }, (_, k) => k === n ? -fac(n) : 0) },
    cos: { name: 'cos x − 1 + x²/2 in x₀ = 0 (n fest = 4)', f: x => Math.cos(x) - 1 + x * x / 2, ders: () => [0, 0, 0, 0, 1], fixed: true },
    sin: { name: 'sin x − x in x₀ = 0 (n fest = 3)', f: x => Math.sin(x) - x, ders: () => [0, 0, 0, -1], fixed: true },
  };
  let key = 'pow', n = 3;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = F[key], d = c.ders(n), m = d.length - 1, f = x => c.f(x, n);
    const A = c.fixed ? mkAx(-2.5, 2.5, ...range(f, -2.5, 2.5)) : mkAx(-1.6, 1.6, -1.6, 1.6); axes(v, A, 'x', 'y');
    fplot(v, A, f, C.c2, 2.6, 600); v.dot(A.P(0, f(0)), C.c1, 6);
    const ext = m % 2 === 0, sgn = d[m] > 0;
    const res = ext ? (sgn ? 'lokales Minimum (f⁽ⁿ⁾ > 0)' : 'lokales Maximum (f⁽ⁿ⁾ < 0)') : 'Sattelpunkt (n ungerade)';
    MW.info(infoEl, c.name, d.slice(1).map((y, k) => ['f' + ['′', '″', '‴', '⁽⁴⁾', '⁽⁵⁾', '⁽⁶⁾', '⁽⁷⁾', '⁽⁸⁾'][k] + '(0)', fmt(y, 4)]).concat([['erste Ableitung ≠ 0', 'Ordnung ' + m + (ext ? ' (gerade)' : ' (ungerade)')], ['Ergebnis', res]]),
      'Notizen Kap. II S. 33: Für xⁿ ist f⁽ⁿ⁾(0) = n! und alle früheren Ableitungen sind 0. n gerade: Minimum, n ungerade: Sattelpunkt. Die Beispiele cos x − 1 + x²/2 und sin x − x sind eigene Beispiele zum selben Satz.');
  });
  const sn = MW.slider(ctl, { label: 'n', min: 2, max: 8, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'Funktion', Object.entries(F).map(([k, c]) => [k, c.name]), u => { key = u; sn.el.style.display = F[u].fixed ? 'none' : ''; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- II.7 Schwingung
W.append(dict(file='7-3-harmonische-schwingung.html', title='Harmonische und gedämpfte Schwingung',
  sub='s̈ + ω²s = 0 hat die Lösungen s(t) = B cos ωt + C sin ωt = A cos(ωt + φ). Mit Dämpfung a > 0 wird daraus e^(−at)·A cos(ωt + φ): die Kurve pendelt zwischen den Hüllkurven ±A e^(−at).',
  hint='B, C, ω und die Dämpfung a verändern.', legend=[('--c2', 's(t)'), ('--c4', 'Hüllkurven ±A e^(−at)'), ('--c1', 'Nullstellen')], js=AX + EXTRA + r'''
  let B = 1, Cc = 1, w = 2, a = 0;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A0 = Math.hypot(B, Cc), phi = Math.atan2(-Cc, B), T = 4 * Math.PI;
    const Ay = Math.max(A0, 0.5) * 1.15, A = mkAx(0, T, -Ay, Ay); axes(v, A, 't', 's', Math.PI / 2);
    const s = t => Math.exp(-a * t) * (B * Math.cos(w * t) + Cc * Math.sin(w * t));
    if (A0 > 0) { fplot(v, A, t => A0 * Math.exp(-a * t), C.c4, 1.4); fplot(v, A, t => -A0 * Math.exp(-a * t), C.c4, 1.4); }
    fplot(v, A, s, C.c2, 2.6, 900);
    const z = roots(s, 0, T, 3000); z.forEach(t => v.dot(A.P(t, 0), C.c1, 4));
    MW.info(infoEl, 's(t) = ' + (a ? 'e^(−' + fmt(a, 2) + 't) · ' : '') + '(' + fmt(B, 2) + ' cos ' + fmt(w, 2) + 't + ' + fmt(Cc, 2) + ' sin ' + fmt(w, 2) + 't)',
      [['Amplitude A = √(B² + C²)', fmt(A0, 4)], ['Phase φ (B = A cos φ, C = −A sin φ)', fmt(phi, 4) + ' = ' + fmt(phi * 180 / Math.PI, 1) + '°'], ['Periode 2π/ω', fmt(2 * Math.PI / w, 4)], ['Nullstellen im Bild', String(z.length)]],
      'Notizen Kap. II S. 35 und Skript S. 61–63: B cos ωt + C sin ωt = A cos(ωt + φ). Beim Ausmultiplizieren von A cos(ωt + φ) = A cos φ cos ωt − A sin φ sin ωt folgt B = A cos φ und C = −A sin φ (die Notizen enthalten dazu einen Korrekturhinweis). Dämpfung: Skript S. 63–64 mit Beispiel e^(−t) sin t. Die Nullstellen hängen nicht von a ab.');
  });
  MW.slider(ctl, { label: 'B', min: -2, max: 2, step: 0.05, value: B, onInput: u => { B = u; view.redraw(); } });
  MW.slider(ctl, { label: 'C', min: -2, max: 2, step: 0.05, value: Cc, onInput: u => { Cc = u; view.redraw(); } });
  MW.slider(ctl, { label: 'ω', min: 0.5, max: 4, step: 0.05, value: w, onInput: u => { w = u; view.redraw(); } });
  MW.slider(ctl, { label: 'Dämpfung a', min: 0, max: 0.8, step: 0.01, value: a, onInput: u => { a = u; view.redraw(); } });
'''))

# ---------------------------------------------------------------- II.8 Darstellungsformen
W.append(dict(file='8-1-darstellungsformen.html', title='Ebene Kurven: Parameterform, implizite und explizite Form',
  sub='Dieselbe Kurve kann man als Parameterdarstellung r(t) = (x(t), y(t)) (I), implizit F(x, y) = 0 (II) oder explizit y = f(x) (III, oft mehrere Äste) beschreiben. Der Punkt zeigt, welcher Parameterwert t zu welchem Punkt gehört.',
  hint='Kurve wählen und t verschieben.', legend=[('--c2', 'Kurve (Parameterform)'), ('--c3', 'Ast f₁ (oben)'), ('--c5', 'Ast f₂ (unten)'), ('--c1', 'Punkt r(t)')], js=AX + EXTRA + r'''
  const ch = Math.cosh, sh = Math.sinh;
  const K = {
    kreis: { name: 'Kreis', r: t => [Math.cos(t), Math.sin(t)], t: [0, 2 * Math.PI], ax: [0, 0, 2.2], I: '(cos t, sin t), 0 ≤ t < 2π', II: 'x² + y² − 1 = 0', III: 'f₁,₂(x) = ±√(1 − x²), −1 ≤ x ≤ 1',
      f1: x => Math.sqrt(1 - x * x), f2: x => -Math.sqrt(1 - x * x), src: 'Notizen Kap. II S. 36–37, Skript S. 65–66' },
    ellipse: { name: 'Ellipse (a = 2, b = 1)', r: t => [2 * Math.cos(t), Math.sin(t)], t: [0, 2 * Math.PI], ax: [0, 0, 3], I: '(a cos t, b sin t)', II: 'x²/a² + y²/b² − 1 = 0', III: 'f₁,₂(x) = ±b √(1 − x²/a²)',
      f1: x => Math.sqrt(1 - x * x / 4), f2: x => -Math.sqrt(1 - x * x / 4), src: 'Notizen Kap. II S. 38, Skript S. 66–67' },
    hyp: { name: 'Hyperbel, rechter Ast (a = b = 1)', r: t => [ch(t), sh(t)], t: [-2, 2], ax: [1.8, 0, 3], I: '(a cosh t, b sinh t), t ∈ ℝ', II: 'x²/a² − y²/b² − 1 = 0, x > 0', III: 'f₁,₂(x) = ±b √(x²/a² − 1), x ≥ a',
      f1: x => Math.sqrt(x * x - 1), f2: x => -Math.sqrt(x * x - 1), src: 'Notizen Kap. II S. 38, Skript S. 67–68 (cosh² − sinh² = 1)' },
    neil: { name: 'Neil’sche Parabel', r: t => [t * t, t ** 3], t: [-1.6, 1.6], ax: [1.2, 0, 2.6], I: '(t², t³)', II: 'x³ − y² = 0', III: 'f₁,₂(x) = ±x^(3/2), x ≥ 0',
      f1: x => x ** 1.5, f2: x => -(x ** 1.5), src: 'Notizen Kap. II S. 37: t eliminieren, x = t² und y = t³ ergibt x³ = t⁶ = y². In (0, 0) hat die Kurve eine Spitze.' },
    par: { name: 'Parabel x + y² = 0', r: t => [-t * t, t], t: [-2, 2], ax: [-1.6, 0, 2.6], I: '(−t², t)', II: 'x + y² = 0', III: 'f₁,₂(x) = ±√(−x), x ≤ 0 (oder einfacher: x = −y² als Funktion von y)',
      f1: x => Math.sqrt(-x), f2: x => -Math.sqrt(-x), src: 'Notizen Kap. II S. 38–39' },
  };
  let key = 'ellipse', t = 0.8;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = K[key], A = eqAx(...c.ax); axes(v, A, 'x', 'y', 0.5, 0.5);
    fplot(v, A, c.f1, C.c3, 5, 800); fplot(v, A, c.f2, C.c5, 5, 800);
    cplot(v, A, c.r, c.t[0], c.t[1], C.c2, 2.2, 800);
    const tt = c.t[0] + (c.t[1] - c.t[0]) * t / (2 * Math.PI), p = c.r(tt);
    v.line(A.P(0, 0), A.P(p[0], p[1]), C.muted, 1, [4, 4]); v.dot(A.P(p[0], p[1]), C.c1, 6);
    const F = key === 'kreis' ? p[0] ** 2 + p[1] ** 2 - 1 : key === 'ellipse' ? p[0] ** 2 / 4 + p[1] ** 2 - 1 : key === 'hyp' ? p[0] ** 2 - p[1] ** 2 - 1 : key === 'neil' ? p[0] ** 3 - p[1] ** 2 : p[0] + p[1] ** 2;
    MW.info(infoEl, c.name + ':  t = ' + fmt(tt, 3) + ',  r(t) = ' + fv(p, 3), [['I Parameterform', c.I], ['II implizit', c.II + '   (im Punkt: F = ' + fmt(F, 6) + ')'], ['III explizit', c.III], ['Ast', p[1] >= 0 ? 'oben (f₁)' : 'unten (f₂)']],
      c.src + '. Übergänge: I → II durch Elimination von t; II → III durch Auflösen nach y; III → I mit x = t, y = f(t) (Skript S. 69). Keine der Darstellungen ist eindeutig.');
  });
  MW.slider(ctl, { label: 'Parameter (Anteil)', min: 0, max: 2 * Math.PI, step: 0.01, value: t, fmt: u => fmt(u / (2 * Math.PI) * 100, 0) + ' %', onInput: u => { t = u; view.redraw(); } });
  MW.select(ctl, 'Kurve', Object.entries(K).map(([k, c]) => [k, c.name]), u => { key = u; view.redraw(); }).set(key);
'''))

# ---------------------------------------------------------------- II.8 Polarkoordinaten
W.append(dict(file='8-2-polarkurven.html', title='Kurven in Polarkoordinaten ρ = ρ(φ)',
  sub='Eine Polarkurve ist die Parameterkurve r(φ) = (ρ(φ) cos φ, ρ(φ) sin φ). Den Tangentenvektor erhält man durch Ableiten nach φ. Der Winkel ω zwischen Ortsvektor und Tangente ist bei der logarithmischen Spirale konstant.',
  hint='Kurve wählen und φ verschieben.', legend=[('--c2', 'Kurve'), ('--c4', 'Ortsvektor'), ('--c1', 'Tangente')], js=AX + EXTRA + r'''
  let k = 0.2, phi = 1.2, key = 'spir';
  const K = {
    spir: { name: 'log. Spirale ρ = e^(kφ)', rho: p => Math.exp(k * p), drho: p => k * Math.exp(k * p), ph: [-12, 9], ax: [0, 0, 6],
      note: () => 'Notizen Kap. II S. 41 und Skript S. 76–79: ρ = C e^(kφ). cos ω = k/√(k² + 1) = ' + fmt(k / Math.hypot(k, 1), 4) + ', unabhängig von φ. Vertikale Tangente wo tan φ = k, horizontale wo tan φ = −1/k (Skript S. 77–78).' },
    inv: { name: 'ρ = 1/φ (Prüfung Herbst 1996)', rho: p => 1 / p, drho: p => -1 / (p * p), ph: [0.25, 14], ax: [0.2, 0.6, 1.4],
      note: () => 'Prüfung Herbst 1996, zweistündig, Aufg. 4 (Aufgabensammlung S. 47, Lösung S. 151): Tangente in φ = π/2 ist 2x − πy + 2 = 0, sie schneidet die x-Achse in (−1, 0). Für φ → ∞ läuft die Kurve in den Ursprung, für φ → 0 nähert sie sich der Geraden y = 1 (eigene Beobachtung).' },
    lim: { name: 'ρ = 1 + (√2/2) cos φ (Prüfung Herbst 1990)', rho: p => 1 + Math.SQRT1_2 * Math.cos(p), drho: p => -Math.SQRT1_2 * Math.sin(p), ph: [0, 2 * Math.PI], ax: [0.2, 0, 2.1],
      note: () => 'Prüfung Herbst 1990, zweistündig, Aufg. 5 (Aufgabensammlung S. 71, Lösung S. 198): Die Tangente in P = (0, 1), also φ = π/2, schneidet die x-Achse in (−√2, 0). Die Aufgabe betrachtet nur 0 ≤ φ ≤ π.' },
    astro: { name: 'Astroide in Polarform (Serie 8)', rho: p => (Math.abs(Math.cos(p)) ** (2 / 3) + Math.abs(Math.sin(p)) ** (2 / 3)) ** -1.5, drho: null, ph: [0, 2 * Math.PI], ax: [0, 0, 1.8],
      note: () => 'Übung 9 (Lino Wenger), Folien S. 4–6: x^(2/3) + y^(2/3) = 1 wird zu ρ(φ) = (cos^(2/3) φ + sin^(2/3) φ)^(−3/2). Minimaler Radius 1/2 bei φ = π/4 + kπ/2, maximaler Radius 1 bei den Spitzen.' },
  };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, c = K[key], A = eqAx(...c.ax); axes(v, A, 'x', 'y', c.ax[2] > 3 ? 1 : 0.5, c.ax[2] > 3 ? 1 : 0.5);
    const r = p => { const q = c.rho(p); return [q * Math.cos(p), q * Math.sin(p)]; };
    cplot(v, A, r, c.ph[0], c.ph[1], C.c2, 2.4, 2000);
    const p = Math.min(c.ph[1], Math.max(c.ph[0], phi)), q = c.rho(p), P = r(p);
    const dq = c.drho ? c.drho(p) : (c.rho(p + 1e-5) - c.rho(p - 1e-5)) / 2e-5;
    const T = [dq * Math.cos(p) - q * Math.sin(p), dq * Math.sin(p) + q * Math.cos(p)], L = Math.hypot(...T);
    v.line(A.P(0, 0), A.P(...P), C.c4, 2);
    const s = 3 * c.ax[2]; v.line(A.P(P[0] - s * T[0] / L, P[1] - s * T[1] / L), A.P(P[0] + s * T[0] / L, P[1] + s * T[1] / L), C.c1, 1.6);
    v.dot(A.P(...P), C.c1, 6);
    const cosw = (P[0] * T[0] + P[1] * T[1]) / (Math.hypot(...P) * L);
    const slope = Math.abs(T[0]) < 1e-9 ? 'vertikal' : fmt(T[1] / T[0], 4);
    MW.info(infoEl, c.name + ',  φ = ' + fmt(p, 3), [['ρ(φ)', fmt(q, 4)], ['r(φ)', fv(P, 4)], ['ṙ(φ) = (ρ̇ cos φ − ρ sin φ, ρ̇ sin φ + ρ cos φ)', fv(T, 4)], ['Steigung ẏ/ẋ', slope], ['Winkel ω (Ortsvektor, Tangente)', fmt(Math.acos(Math.max(-1, Math.min(1, cosw))) * 180 / Math.PI, 2) + '°']], c.note());
  });
  const sp = MW.slider(ctl, { label: 'φ', min: -12, max: 14, step: 0.01, value: phi, onInput: u => { phi = u; view.redraw(); } });
  const sk = MW.slider(ctl, { label: 'k', min: -0.5, max: 0.5, step: 0.01, value: k, onInput: u => { k = u; view.redraw(); } });
  MW.select(ctl, 'Kurve', Object.entries(K).map(([q, c]) => [q, c.name]), u => { key = u; const c = K[u], i = sp.el.querySelector('input'); i.min = c.ph[0]; i.max = c.ph[1]; phi = u === 'inv' || u === 'lim' ? Math.PI / 2 : 1.2; sp.set(phi); sk.el.style.display = u === 'spir' ? '' : 'none'; view.redraw(); }).set(key);
'''))

if __name__ == '__main__':
    print(build('analysis-w8', W))
