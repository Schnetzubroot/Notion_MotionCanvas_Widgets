"""Widgets zu Analysis I, Woche 2: Kapitel I.2 Funktionen und I.3 Grenzwerte von Funktionen, Stetigkeit (Stammbach, Teil A, S. 16-33)."""
from template import build
from build_analysis_w1 import AX, BOX

W = []

# ---------------------------------------------------------------- 2.1
W.append(dict(file='2-1-definitions-wertebereich.html', title='Definitionsbereich, Wertebereich, Graph',
  sub='f : A → B legt für jedes x ∈ D(f) genau einen Wert f(x) fest. D(f) ist die Menge der zulässigen Inputs, W(f) die Menge der tatsächlich angenommenen Werte. W(f) kann kleiner sein als der Zielbereich B.',
  hint='Funktion wählen, x verschieben.', legend=[('--c2', 'Graph Γ(f)'), ('--c3', 'D(f) auf der x-Achse'), ('--c4', 'W(f) auf der y-Achse')], js=AX + r'''
  const S = {
    sin: { name: 'f(x) = sin x', f: Math.sin, D: [[-5, 5, 1, 1]], W: [[-1, 1, 1, 1]], y: [-2, 2], Dt: 'ℝ', Wt: '[−1, 1]' },
    sq: { name: 'f(x) = √(x − 1)', f: x => x >= 1 ? Math.sqrt(x - 1) : NaN, D: [[1, 5, 1, 1]], W: [[0, 2.5, 1, 1]], y: [-1, 2.5], Dt: '[1, ∞)', Wt: '[0, ∞)' },
    rat: { name: 'f(x) = (x² + 5x + 4)/(x⁴ − 16)', f: x => (x * x + 5 * x + 4) / (x ** 4 - 16), D: [[-5, -2, 1, 0], [-2, 2, 0, 0], [2, 5, 0, 1]], W: null, y: [-3, 3], Dt: 'ℝ \\ {−2, 2}', Wt: '(aus der Formel nicht direkt ablesbar)', holes: [-2, 2] },
    sgn: { name: 'Sprungfunktion', f: x => x < 0 ? -1 : x > 0 ? 1 : 0, D: [[-5, 5, 1, 1]], W: null, y: [-2, 2], Dt: 'ℝ', Wt: '{−1, 0, 1}', jump: true },
    geo: { name: 'f(x) = 1/(1 − x), D(f) = (−1, 1)', f: x => x > -1 && x < 1 ? 1 / (1 - x) : NaN, D: [[-1, 1, 0, 0]], W: [[0.5, 3.2, 0, 1]], y: [-0.5, 3.2], Dt: '(−1, 1) (vorgegeben)', Wt: '(1/2, ∞)' },
  };
  let key = 'sq', x0 = 2.5;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], A = mkAx(-5, 5, s.y[0], s.y[1]); axes(v, A, 'x', 'y', 1, s.y[1] - s.y[0] > 4 ? 1 : 0.5);
    const yz = A.inY(0) ? 0 : s.y[0];
    s.D.forEach(([a, b, ca, cb]) => { v.line(A.P(a, yz), A.P(b, yz), C.c3, 6); if (a > -5) v.dot(A.P(a, yz), C.c3, 5, !ca); if (b < 5) v.dot(A.P(b, yz), C.c3, 5, !cb); });
    if (s.W) s.W.forEach(([a, b, ca, cb]) => { v.line(A.P(0, a), A.P(0, Math.min(b, s.y[1])), C.c4, 6); v.dot(A.P(0, a), C.c4, 5, !ca); });
    if (key === 'sgn') { [-1, 0, 1].forEach(y => v.dot(A.P(0, y), C.c4, 5)); v.line(A.P(-5, -1), A.P(0, -1), C.c2, 2.5); v.line(A.P(0, 1), A.P(5, 1), C.c2, 2.5);
      v.dot(A.P(0, -1), C.c2, 5, true); v.dot(A.P(0, 1), C.c2, 5, true); v.dot(A.P(0, 0), C.c2, 5); }
    else fplot(v, A, s.f, C.c2, 2.5, 1200);
    (s.holes || []).forEach(h => v.line(A.P(h, s.y[0]), A.P(h, s.y[1]), C.muted, 1, [3, 3]));
    const y0 = s.f(x0), ok = isFinite(y0);
    if (ok) { v.line(A.P(x0, yz), A.P(x0, y0), C.fg, 1, [3, 3]); v.line(A.P(x0, y0), A.P(0, y0), C.fg, 1, [3, 3]); if (A.inY(y0)) v.dot(A.P(x0, y0), C.fg, 6); }
    v.dot(A.P(x0, yz), ok ? C.fg : C.c1, 5); v.text(A.P(x0, yz), 'x', ok ? C.fg : C.c1, -4, 18, 12);
    MW.info(infoEl, s.name, [['D(f)', s.Dt], ['W(f)', s.Wt], ['Input x = ' + fmt(x0), ok ? 'Output f(x) = ' + fmt(y0, 4) : 'x ∉ D(f): kein Output']],
      key === 'rat' ? 'Ohne weitere Angabe ist D(f) der grösste Bereich, auf dem die Formel Sinn ergibt. Hier: Nenner x⁴ − 16 = 0 bei x = ±2.'
      : key === 'geo' ? 'Der Definitionsbereich kann auch vorgegeben sein. Dieselbe Formel mit anderem D(f) ist eine andere Funktion.'
      : key === 'sgn' ? 'Eine Funktion braucht keine einzelne Formel. Auch eine Fallunterscheidung legt für jedes x genau einen Wert fest.'
      : 'Zielbereich ℝ, Wertebereich kleiner: W(f) ≠ B ist der Normalfall.', !ok);
  });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'x', min: -5, max: 5, step: 0.01, value: x0, onInput: x => { x0 = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 2.2
W.append(dict(file='2-2-parameterkurven.html', title='Funktionen t → (x(t), y(t)): Kreis und Ellipse',
  sub='Eine Funktion f : ℝ → ℝ × ℝ ordnet jedem t einen Punkt der Ebene zu. t → (a cos t, b sin t) beschreibt eine Ellipse mit Halbachsen a und b, für a = b einen Kreis.',
  hint='Abspielen, a und b ändern.', legend=[('--c2', 'Bild f(ℝ)'), ('--c1', 'f(t)')], js=r'''
  let a = 2.4, b = 1.4, t = 0.8;
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 3.2, ymin: -2, ymax: 2 }, v => {
    const C = v.C; v.grid(1);
    const pts = []; for (let i = 0; i <= 200; i++) { const s = 2 * Math.PI * i / 200; pts.push([a * Math.cos(s), b * Math.sin(s)]); } v.poly(pts, C.c2, 2.2);
    const P = [a * Math.cos(t), b * Math.sin(t)];
    v.arc([0, 0], 0.5, 0, t % (2 * Math.PI), C.muted, 1.5); v.text([0.62 * Math.cos(t / 2), 0.62 * Math.sin(t / 2)], 't', C.muted, 0, 4, 12);
    v.line([P[0], 0], P, C.c3, 1, [3, 3]); v.line([0, P[1]], P, C.c3, 1, [3, 3]);
    v.dot(P, C.c1, 6); v.text(P, 'f(t)', C.c1, 8, -8);
    MW.info(infoEl, 'f(t) = (a cos t, b sin t) = ' + MW.fv(P), [['t', fmt(t % (2 * Math.PI), 2)], ['x²/a² + y²/b²', fmt(P[0] ** 2 / a ** 2 + P[1] ** 2 / b ** 2, 4)]],
      a === b ? 'a = b: Kreis mit Radius a, gleichförmig im Gegenuhrzeigersinn durchlaufen, Start in (a, 0).' : 'Für jedes t gilt x²/a² + y²/b² = 1: alle Bildpunkte liegen auf der Ellipse.');
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 6, value: t, onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'a', min: 0.5, max: 2.8, step: 0.1, value: a, onInput: x => { a = x; view.redraw(); } });
  MW.slider(ctl, { label: 'b', min: 0.5, max: 1.8, step: 0.1, value: b, onInput: x => { b = x; view.redraw(); } });
'''))

W.append(dict(file='2-2-schraubenlinie.html', title='Kurve im Raum: Schraubenlinie t → (cos t, sin t, h t/2π)',
  sub='Eine Funktion f : ℝ → ℝ³ beschreibt eine Raumkurve. Hier eine Rechts-Schraubenlinie mit Ganghöhe h auf dem Zylinder mit Radius 1 um die z-Achse.',
  hint='Abspielen, h ändern. Ziehen dreht die Ansicht.', legend=[('--c2', 'Schraubenlinie'), ('--c1', 'f(t)'), ('--field', 'Zylinder ρ = 1')], js=r'''
  let h = 1, t = 3;
  const view = MW.View3D(cv, { extent: 2.2, yaw: -35, pitch: 18, center: [0, 0, 1.2] }, v => {
    const C = v.C; v.axes(1.6);
    for (const z of [0, 2.4]) v.poly(v.circlePts([0, 0, z], [0, 0, 1], 1), C.field, 1, [3, 3]);
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; v.line([Math.cos(a), Math.sin(a), 0], [Math.cos(a), Math.sin(a), 2.4], C.grid, 1); }
    const pts = []; const tmax = 2.4 / h * 2 * Math.PI; for (let i = 0; i <= 400; i++) { const s = tmax * i / 400; pts.push([Math.cos(s), Math.sin(s), h * s / (2 * Math.PI)]); }
    v.poly(pts, C.c2, 2.2);
    const P = [Math.cos(t), Math.sin(t), h * t / (2 * Math.PI)]; v.line([P[0], P[1], 0], P, C.muted, 1, [3, 3]); v.dot(P, C.c1, 6); v.text(P, 'f(t)', C.c1, 8, -8);
    MW.info(infoEl, 'f(t) = ' + MW.fv(P), [['t', fmt(t)], ['Umläufe t/2π', fmt(t / (2 * Math.PI))], ['Ganghöhe h', fmt(h)]],
      'Nach einem vollen Umlauf (t → t + 2π) ist der Punkt um h höher. Projektion auf die xy-Ebene: der Einheitskreis.');
  });
  MW.player(ctl, { t0: 0, t1: 4 * Math.PI, duration: 8, value: t, onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'h', min: 0.3, max: 2.4, step: 0.05, value: h, onInput: x => { h = x; view.redraw(); } });
'''))

W.append(dict(file='2-2-eisenbahn.html', title='Kurvenradius einer Eisenbahnlinie: r(x) = ½(a²/x + x)',
  sub='Gegeben ist die halbe Sehne a, gemessen wird die Pfeilhöhe x. Pythagoras: a² + (r − x)² = r². Daraus r = ½(a²/x + x). Für die Anwendung ist nur D(r) = (0, a] interessant.',
  hint='x und a ändern.', tall=True, legend=[('--c2', 'Kreisbogen'), ('--c1', 'r'), ('--c3', 'a'), ('--c4', 'x')], js=AX + r'''
  let a = 1.5, x = 0.5;
  const view = MW.View2D(cv, { xmin: -0.5, xmax: 7.6, ymin: -0.6, ymax: 3.7 }, v => {
    const C = v.C, r = 0.5 * (a * a / x + x);
    // linke Skizze: Sehne horizontal bei y = 2.6, Bogen nach oben, Mittelpunkt unten
    const s = Math.min(1, 1.6 / a), cx = 1.8, top = 3.2, M = [cx, top - r * s];
    const th = Math.asin(Math.min(1, a / r)), pts = [];
    for (let i = 0; i <= 80; i++) { const ang = Math.PI / 2 - th + 2 * th * i / 80; pts.push([M[0] + r * s * Math.cos(ang), M[1] + r * s * Math.sin(ang)]); }
    v.poly(pts.filter(p => p[1] > -0.6), C.c2, 3);
    const yc = top - x * s, L = [cx - a * s, yc], R = [cx + a * s, yc];
    v.line(L, R, C.muted, 1.2); v.line([cx, yc], R, C.c3, 2.5); v.text([cx + a * s / 2, yc], 'a', C.c3, -4, 16, 13);
    v.line([cx, yc], [cx, top], C.c4, 2.5); v.text([cx, (yc + top) / 2], 'x', C.c4, 6, 4, 13);
    if (M[1] > -0.6) { v.line(M, R, C.c1, 2, [5, 4]); v.dot(M, C.fg, 4); v.text(M, 'M', C.fg, 6, 4, 12); v.line(M, [cx, yc], C.muted, 1, [2, 3]); }
    else v.text([cx, -0.3], 'M liegt weit unten (r gross)', C.muted, 0, 0, 11, false, 'center');
    v.text([(M[0] + R[0]) / 2, Math.max(-0.4, (M[1] + R[1]) / 2)], 'r', C.c1, 6, 0, 13);
    // rechter Graph r(x)
    const B = mkAx(0, 3, 0, 6, 3.2, 3.2, 4.2, 0); axes(v, B, 'x', 'r', 0.5, 1);
    v.poly([B.P(0, 0), B.P(a, 0), B.P(a, 6), B.P(0, 6)], null, 1, null, true, C.fill);
    fplot(v, B, t => 0.5 * (a * a / t + t), C.line, 1.5, 400, 0.01, 3);
    fplot(v, B, t => 0.5 * (a * a / t + t), C.c1, 2.5, 400, 0.01, a);
    if (B.inY(r)) v.dot(B.P(x, r), C.fg, 5);
    v.dot(B.P(a, a), C.c3, 4, true);
    MW.info(infoEl, 'r(' + fmt(x) + ') = ' + fmt(r, 3), [['a² + (r − x)²', fmt(a * a + (r - x) ** 2, 3)], ['r²', fmt(r * r, 3)]],
      x >= a - 1e-9 ? 'x = a: Halbkreis, r = a. Für x > a gibt die Formel zwar Werte, aber die Skizze passt nicht mehr: darum D(r) = (0, a].' : 'Je flacher der Bogen (x klein), desto grösser der Radius. Für x → 0 wächst r über alle Grenzen.');
  });
  MW.slider(ctl, { label: 'x', min: 0.08, max: 3, step: 0.01, value: x, onInput: t => { x = Math.min(t, 3); view.redraw(); } });
  MW.slider(ctl, { label: 'a', min: 0.6, max: 2.5, step: 0.05, value: a, onInput: t => { a = t; view.redraw(); } });
'''))

W.append(dict(file='2-2-roboterarm.html', title='Roboterarm: eine Funktion (φ, ψ) → P',
  sub='Jedes Winkelpaar (φ, ψ) aus A = [0, π] × [0, π] legt den Greiferpunkt P = (R cos φ + r cos(φ − ψ), R sin φ + r sin(φ − ψ)) fest. Links der Definitionsbereich A, rechts das Bild in der (x, y)-Ebene.',
  hint='φ und ψ ändern oder den Punkt links ziehen.', tall=True, legend=[('--c2', 'Punkt in A bzw. Bild P'), ('--field', 'Arbeitsbereich f(A)')], js=r'''
  const R = 1.6, r = 1; let phi = 1.0, psi = 0.9;
  const PI = Math.PI, f = (p, q) => [R * Math.cos(p) + r * Math.cos(p - q), R * Math.sin(p) + r * Math.sin(p - q)];
  const ox = 5.3, oy = 0.4; // Ursprung des Roboters im Bild
  const cloud = []; for (let i = 0; i <= 40; i++) for (let j = 0; j <= 40; j++) cloud.push(f(PI * i / 40, PI * j / 40));
  const sA = 0.75; // Massstab für A
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 8.1, ymin: -1.3, ymax: 3.3 }, v => {
    const C = v.C;
    // A
    v.poly([[0, 0], [PI * sA, 0], [PI * sA, PI * sA], [0, PI * sA]], C.c2, 1.5, null, true, C.fill);
    v.text([PI * sA / 2, 0], 'φ', C.muted, -4, 18, 13, false); v.text([0, PI * sA / 2], 'ψ', C.muted, -18, 4, 13, false);
    v.text([0, 0], '0', C.muted, -10, 14, 11, false); v.text([PI * sA, 0], 'π', C.muted, -2, 14, 11, false); v.text([0, PI * sA], 'π', C.muted, -14, 10, 11, false);
    v.text([PI * sA / 2, PI * sA], 'A', C.c2, -4, -8, 13);
    const Q = [phi * sA, psi * sA]; v.dot(Q, C.c2, 6); v.text(Q, '(φ, ψ)', C.c2, 8, -6, 12);
    // Bild
    cloud.forEach(p => v.dot([ox + p[0], oy + p[1]], C.field, 1.3));
    const E = [ox + R * Math.cos(phi), oy + R * Math.sin(phi)], P = f(phi, psi), PP = [ox + P[0], oy + P[1]];
    v.line([ox - 0.4, oy], [ox + 2.8, oy], C.muted, 1); v.line([ox, oy - 1.2], [ox, oy + 2.8], C.muted, 1);
    v.line([ox, oy], E, C.fg, 5); v.line(E, PP, C.fg, 4); v.dot([ox, oy], C.fg, 6); v.dot(E, C.fg, 5); v.dot(PP, C.c2, 7); v.text(PP, 'P', C.c2, 8, -6);
    v.arc([ox, oy], 0.45, 0, phi, C.c4, 1.5); v.text([ox + 0.55 * Math.cos(phi / 2), oy + 0.55 * Math.sin(phi / 2)], 'φ', C.c4, 0, 4, 12);
    v.line(E, [E[0] + 0.7 * Math.cos(phi), E[1] + 0.7 * Math.sin(phi)], C.line, 1, [3, 3]);
    v.arc(E, 0.4, phi - psi, phi, C.c5, 1.5); v.text([E[0] + 0.5 * Math.cos(phi - psi / 2), E[1] + 0.5 * Math.sin(phi - psi / 2)], 'ψ', C.c5, 2, 4, 12);
    MW.info(infoEl, 'f(φ, ψ) = P = ' + MW.fv(P), [['φ', fmt(phi)], ['ψ', fmt(psi)], ['Abstand |OP|', fmt(Math.hypot(...P), 3)]],
      'Definitionsbereich A ist ein Quadrat in der (φ, ψ)-Ebene, das Bild f(A) ein Teil der (x, y)-Ebene. Funktion = Abbildung zwischen beliebigen Mengen.');
  });
  view.handle(() => [phi * sA, psi * sA], p => { phi = Math.max(0, Math.min(PI, p[0] / sA)); psi = Math.max(0, Math.min(PI, p[1] / sA)); s1.set(phi); s2.set(psi); });
  const s1 = MW.slider(ctl, { label: 'φ', min: 0, max: PI, step: 0.01, value: phi, onInput: x => { phi = x; view.redraw(); } });
  const s2 = MW.slider(ctl, { label: 'ψ', min: 0, max: PI, step: 0.01, value: psi, onInput: x => { psi = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 2.3
W.append(dict(file='2-3-symmetrie-monotonie.html', title='Gerade, ungerade, monoton',
  sub='Gerade: f(−x) = f(x), Graph spiegelsymmetrisch zur y-Achse. Ungerade: f(−x) = −f(x), Graph punktsymmetrisch zum Ursprung. Beides verlangt einen zum Nullpunkt symmetrischen Definitionsbereich.',
  hint='Funktion wählen, x verschieben.', legend=[('--c2', 'Graph'), ('--c1', '(x, f(x))'), ('--c3', '(−x, f(−x))')], js=AX + r'''
  const cbrt = Math.cbrt;
  const S = {
    p2: ['x²', x => x * x, 'gerade', 'fallend auf (−∞, 0], wachsend auf [0, ∞)'],
    p3: ['x³', x => x ** 3, 'ungerade', 'strikt wachsend auf ℝ'],
    m1: ['x⁻¹ = 1/x', x => 1 / x, 'ungerade', 'strikt fallend auf (−∞, 0) und auf (0, ∞), aber nicht auf ganz D(f)'],
    m2: ['x⁻² = 1/x²', x => 1 / (x * x), 'gerade', 'wachsend auf (−∞, 0), fallend auf (0, ∞)'],
    h: ['x^(1/2) = √x', x => x >= 0 ? Math.sqrt(x) : NaN, 'weder (D(f) = [0, ∞) ist nicht symmetrisch)', 'strikt wachsend'],
    t: ['x^(2/3) = ∛(x²)', x => cbrt(x * x), 'gerade', 'fallend auf (−∞, 0], wachsend auf [0, ∞)'],
    sin: ['sin x', Math.sin, 'ungerade', 'periodisch (2π), wachsend auf [−π/2, π/2]'],
    cos: ['cos x', Math.cos, 'gerade', 'periodisch (2π), fallend auf [0, π]'],
    tan: ['tan x', Math.tan, 'ungerade', 'periodisch (π), strikt wachsend auf (−π/2, π/2)'],
    exp: ['eˣ', Math.exp, 'weder', 'strikt wachsend auf ℝ'],
    ln: ['ln x', x => x > 0 ? Math.log(x) : NaN, 'weder (D(f) = (0, ∞))', 'strikt wachsend'],
    mix: ['x² + x', x => x * x + x, 'weder', 'fallend auf (−∞, −1/2], wachsend auf [−1/2, ∞)'],
  };
  let key = 'p3', x0 = 1.2;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, [name, f, sym, mon] = S[key], A = mkAx(-4, 4, -3, 3); axes(v, A, 'x', 'y', 1, 1);
    fplot(v, A, f, C.c2, 2.5, 1600);
    const y1 = f(x0), y2 = f(-x0);
    if (isFinite(y1) && A.inY(y1)) { v.line(A.P(x0, 0), A.P(x0, y1), C.c1, 1, [3, 3]); v.dot(A.P(x0, y1), C.c1, 6); }
    if (isFinite(y2) && A.inY(y2)) { v.line(A.P(-x0, 0), A.P(-x0, y2), C.c3, 1, [3, 3]); v.dot(A.P(-x0, y2), C.c3, 6); }
    if (sym.startsWith('ungerade') && isFinite(y1) && A.inY(y1) && A.inY(-y1)) v.line(A.P(x0, y1), A.P(-x0, -y1), C.muted, 1, [2, 4]);
    if (sym.startsWith('gerade') && isFinite(y1) && A.inY(y1)) v.line(A.P(x0, y1), A.P(-x0, y1), C.muted, 1, [2, 4]);
    MW.info(infoEl, 'f(x) = ' + name + ': ' + sym, [['f(' + fmt(x0) + ')', fmt(y1, 4)], ['f(' + fmt(-x0) + ')', fmt(y2, 4)], ['Monotonie', mon]],
      'Test: f(−x) mit f(x) vergleichen. Gleich → gerade, entgegengesetzt → ungerade. Ein Gegenbeispiel genügt für „weder“.');
  });
  MW.select(ctl, 'Funktion', Object.entries(S).map(([k, s]) => [k, s[0]]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'x', min: 0.05, max: 3.9, step: 0.01, value: x0, onInput: x => { x0 = x; view.redraw(); } });
'''))

W.append(dict(file='2-3-exp-vs-potenz.html', title='Exponentialfunktion gegen Potenzfunktion',
  sub='Bei xⁿ ist die Basis variabel und der Exponent fest, bei aˣ umgekehrt. Für a > 1 überholt aˣ jede Potenz xⁿ, wenn x nur gross genug ist, auch wenn xⁿ lange vorne liegt.',
  hint='x-Fenster vergrössern, a und n ändern.', legend=[('--c1', 'aˣ'), ('--c2', 'xⁿ')], js=AX + r'''
  let a = 1.5, n = 3, X = 10;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, f = x => a ** x, g = x => x ** n;
    let ymax = 1; for (let i = 0; i <= 200; i++) { const x = X * i / 200; ymax = Math.max(ymax, Math.min(f(x), 1e300), g(x)); }
    const A = mkAx(0, X, 0, ymax * 1.05); axes(v, A, 'x', 'y');
    fplot(v, A, g, C.c2, 2.5); fplot(v, A, f, C.c1, 2.5);
    // letzter Schnittpunkt (Überholpunkt)
    let cross = null; for (let x = 200; x > 1; x -= 0.01) if (g(x) > f(x)) { cross = x; break; }
    if (cross && cross <= X) v.dot(A.P(cross, g(cross)), C.fg, 5, true);
    MW.info(infoEl, cross ? 'aˣ > xⁿ für alle x > ' + fmt(cross, 2) : 'aˣ > xⁿ für alle x > 1', [['a', fmt(a, 2)], ['n', String(n)], ['aˣ / xⁿ bei x = ' + fmt(X), fmt(f(X) / g(X), 3)]],
      cross && cross > X ? 'Im gewählten Fenster liegt xⁿ noch vorne. Fenster vergrössern: Bei x ≈ ' + fmt(cross, 1) + ' überholt aˣ.' : 'Je näher a bei 1 und je grösser n, desto später, aber immer, überholt die Exponentialfunktion.');
  });
  MW.slider(ctl, { label: 'a', min: 1.1, max: 3, step: 0.05, value: a, onInput: x => { a = x; view.redraw(); } });
  MW.slider(ctl, { label: 'n', min: 1, max: 6, step: 1, value: n, fmt: x => String(x), onInput: x => { n = x; view.redraw(); } });
  MW.slider(ctl, { label: 'x bis', min: 2, max: 60, step: 0.5, value: X, onInput: x => { X = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.1
W.append(dict(file='3-1-numerisches-experiment.html', title='Numerisches Experiment: f(x) = sin((x² + x + 1)/(x² − x − 2))',
  sub='Wir nähern uns ξ von links mit x<sub>k</sub> = ξ − 10<sup>−k</sup>. Bei ξ = 4 stabilisieren sich die Werte f(x<sub>k</sub>), bei ξ = 2 streuen sie chaotisch: dort geht das Argument des Sinus gegen −∞.',
  hint='ξ wählen, k erhöhen, hineinzoomen.', legend=[('--c2', 'Graph von f'), ('--c1', 'x_k und f(x_k)')], js=AX + r'''
  const f = x => Math.sin((x * x + x + 1) / (x * x - x - 2));
  let xi = 4, k = 3, z = 0.3;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, w = Math.pow(10, -z), A = mkAx(xi - w, xi + w * 0.25, -1.2, 1.2); axes(v, A, 'x', 'f(x)', null, 0.5);
    v.line(A.P(xi, -1.2), A.P(xi, 1.2), C.muted, 1.2, [4, 4]); v.text(A.P(xi, 1.2), 'ξ = ' + xi, C.fg, 4, 14, 12);
    fplot(v, A, f, C.c2, 1.6, 3000);
    const rows = [];
    for (let j = 1; j <= 9; j++) { const x = xi - Math.pow(10, -j), y = f(x);
      if (j <= k && x >= A.x0) v.dot(A.P(x, y), j === k ? C.c1 : C.c4, j === k ? 6 : 4);
      if (j <= k) rows.push(['x = ' + x.toFixed(j), fmt(y, 10)]); }
    MW.info(infoEl, xi === 4 ? 'ξ = 4: Werte nähern sich 0.8632093666…' : 'ξ = 2: Werte springen hin und her', rows.slice(-6),
      xi === 4 ? 'Bei x = 4 ist der Nenner x² − x − 2 = 10 ≠ 0. Das Argument strebt gegen 21/10 und sin(2.1) ≈ 0.8632.' : 'Bei x = 2 ist x² − x − 2 = (x − 2)(x + 1) = 0. Das Argument strebt gegen −∞, der Sinus pendelt unendlich oft zwischen −1 und 1. Der linke Grenzwert existiert nicht.', xi === 2);
  });
  MW.select(ctl, 'ξ', [['4', 'ξ = 4'], ['2', 'ξ = 2']], x => { xi = +x; view.redraw(); });
  MW.slider(ctl, { label: 'k', min: 1, max: 9, step: 1, value: k, fmt: x => String(x), onInput: x => { k = x; view.redraw(); } });
  MW.slider(ctl, { label: 'Zoom', min: 0, max: 3, step: 0.05, value: z, fmt: x => 'Fenster ' + fmt(Math.pow(10, -x), 3), onInput: x => { z = x; view.redraw(); } });
'''))

W.append(dict(file='3-1-einseitige-grenzwerte.html', title='Linker und rechter Grenzwert von 2<sup>−1/x</sup> bei ξ = 0',
  sub='Rechts: für x<sub>k</sub> → 0+ geht −1/x<sub>k</sub> → −∞, also 2<sup>−1/x<sub>k</sub></sup> → 0. Links: −1/x<sub>k</sub> → +∞, die Werte wachsen über alle Grenzen. Der rechte Grenzwert ist 0, der linke existiert nicht.',
  hint='Seite wählen, k erhöhen.', legend=[('--c2', 'Graph'), ('--c1', 'Folge (x_k, f(x_k))')], js=AX + r'''
  const f = x => Math.pow(2, -1 / x);
  let side = 1, k = 4;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A = mkAx(-2, 2, -0.5, 5); axes(v, A, 'x', 'y', 0.5, 1);
    fplot(v, A, f, C.c2, 2.5, 800, -2, -0.001); fplot(v, A, f, C.c2, 2.5, 800, 0.001, 2);
    v.line(A.P(-2, 1), A.P(2, 1), C.muted, 1, [2, 4]);
    const rows = [];
    for (let j = 1; j <= k; j++) { const x = side / (j + 0.5) , y = f(x); if (A.inY(y)) v.dot(A.P(x, y), j === k ? C.c1 : C.c4, j === k ? 6 : 4);
      v.dot(A.P(x, -0.5), C.muted, 2.5); }
    for (let j = Math.max(1, k - 4); j <= k; j++) { const x = side / (j + 0.5); rows.push(['x = ' + fmt(x, 4), 'f(x) = ' + (f(x) > 1e6 ? f(x).toExponential(2) : fmt(f(x), 6))]); }
    MW.info(infoEl, side > 0 ? 'x → 0+: f(x_k) → 0' : 'x → 0−: f(x_k) wächst über alle Grenzen', rows,
      side > 0 ? 'Jede Folge positiver x_k → 0 liefert f(x_k) → 0. Darum lim_{x→0+} 2^(−1/x) = 0.' : 'Für keine Folge negativer x_k → 0 konvergiert f(x_k). lim_{x→0−} 2^(−1/x) existiert nicht.', side < 0);
  });
  MW.select(ctl, 'Seite', [['1', 'von rechts (x → 0+)'], ['-1', 'von links (x → 0−)']], x => { side = +x; view.redraw(); });
  MW.slider(ctl, { label: 'k', min: 1, max: 30, step: 1, value: k, fmt: x => String(x), onInput: x => { k = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.2
W.append(dict(file='3-2-sinx-durch-x.html', title='Der Grenzwert sin x / x → 1 (Einschliessung)',
  sub='Am Einheitskreis: Dreieck ⊂ Sektor ⊂ grosses Dreieck, also ½ sin x cos x < ½ x < ½ tan x. Umgeformt: cos x < sin x / x < 1/cos x. Beide Schranken gehen für x → 0 gegen 1.',
  hint='x verkleinern.', tall=True, legend=[('--c3', 'Dreieck ½ sin x cos x'), ('--c2', 'Sektor ½ x'), ('--c4', 'Dreieck ½ tan x'), ('--c1', 'sin x / x')], js=AX + r'''
  let x = 0.9;
  const view = MW.View2D(cv, { xmin: -0.4, xmax: 7.6, ymin: -0.5, ymax: 3.7 }, v => {
    const C = v.C, s = 2.6, O = [0.1, 0.2], P = (u, w) => [O[0] + s * u, O[1] + s * w];
    const c = Math.cos(x), si = Math.sin(x), t = Math.tan(x);
    v.arc(O, s, 0, Math.PI / 2, C.line, 1.2);
    v.poly([P(0, 0), P(1, 0), P(1, Math.min(t, 1.35))], C.c4, 1.5, null, true, 'rgba(216,154,0,0.15)');
    const sec = [P(0, 0)]; for (let i = 0; i <= 40; i++) sec.push(P(Math.cos(x * i / 40), Math.sin(x * i / 40))); v.poly(sec, C.c2, 1.5, null, true, 'rgba(47,111,219,0.18)');
    v.poly([P(0, 0), P(c, 0), P(c, si)], C.c3, 1.5, null, true, 'rgba(15,157,88,0.25)');
    v.text(P(c, si / 2), 'sin x', C.c3, 4, 4, 11); v.text(P(c / 2, 0), 'cos x', C.c3, 0, 14, 11, true, 'center');
    if (t < 1.35) v.text(P(1, t / 2), 'tan x', C.c4, 4, 4, 11);
    v.text(P(0, 0), 'O', C.fg, -14, 14, 12); v.text(P(1, 0), '1', C.muted, -4, 14, 11, false);
    const B = mkAx(-1.6, 1.6, 0.3, 1.6, 3.4, 3.2, 4.0, 0); axes(v, B, 'x', '', 0.5, 0.25);
    fplot(v, B, u => Math.cos(u), C.c3, 1.5); fplot(v, B, u => 1 / Math.cos(u), C.c4, 1.5);
    fplot(v, B, u => Math.sin(u) / u, C.c1, 2.5, 400, -1.6, -1e-4); fplot(v, B, u => Math.sin(u) / u, C.c1, 2.5, 400, 1e-4, 1.6);
    v.dot(B.P(0, 1), C.c1, 5, true); v.line(B.P(x, 0.3), B.P(x, 1.6), C.muted, 1, [3, 3]);
    if (B.inY(si / x)) v.dot(B.P(x, si / x), C.c1, 5);
    MW.info(infoEl, 'cos x < sin x / x < 1/cos x', [['x', fmt(x, 3)], ['cos x', fmt(c, 6)], ['sin x / x', fmt(si / x, 6)], ['1/cos x', fmt(1 / c, 6)]],
      'Die Funktion ist bei 0 nicht definiert (Kreis rechts im Graph), aber gerade. Darum genügt der rechte Grenzwert: lim_{x→0} sin x / x = 1.');
  });
  MW.slider(ctl, { label: 'x', min: 0.02, max: 1.25, step: 0.005, value: x, onInput: t => { x = t; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.3
W.append(dict(file='3-3-stetigkeit.html', title='Stetigkeit: linker Grenzwert = f(ξ) = rechter Grenzwert',
  sub='f ist stetig in ξ, wenn die Annäherung von links, der Funktionswert und die Annäherung von rechts dasselbe liefern. Wähle ein Beispiel und nähere dich mit δ → 0 von beiden Seiten.',
  hint='Beispiel wählen, δ verkleinern.', legend=[('--c2', 'Graph'), ('--c3', 'f(ξ − δ)'), ('--c4', 'f(ξ + δ)'), ('--c1', 'f(ξ)')], js=AX + r'''
  const g = x => x === 0 ? 1 : Math.pow(2, -1 / x);
  const S = {
    g0: { name: 'g(x) = 2^(−1/x), g(0) = 1, bei ξ = 0', f: g, xi: 0, win: [-2, 2, -0.3, 4], L: '+∞ (existiert nicht)', R: '0', val: 1, ok: false, note: 'Drei verschiedene „Werte“: links unbeschränkt, rechts 0, g(0) = 1. Keine Beziehung, nicht stetig.' },
    g1: { name: 'dieselbe Funktion g bei ξ = 1', f: g, xi: 1, win: [-0.5, 2.5, -0.3, 1.5], L: '1/2', R: '1/2', val: 0.5, ok: true, note: 'Links, rechts und Funktionswert stimmen überein: g ist stetig in ξ = 1.' },
    sgn: { name: 'Sprungfunktion bei ξ = 0', f: x => x < 0 ? -1 : x > 0 ? 1 : 0, xi: 0, win: [-2, 2, -1.5, 1.5], L: '−1', R: '1', val: 0, ok: false, note: 'Beide einseitigen Grenzwerte existieren, sind aber verschieden: Sprungstelle.' },
    sinc: { name: 'sin x / x, bei 0 durch 1 ergänzt', f: x => x === 0 ? 1 : Math.sin(x) / x, xi: 0, win: [-6, 6, -0.4, 1.3], L: '1', R: '1', val: 1, ok: true, note: 'Ohne Ergänzung ist ξ = 0 nicht im Definitionsbereich. Mit f(0) := 1 wird die Funktion stetig, weil beide Grenzwerte 1 sind.' },
    rat: { name: 'x/(x − 2) bei ξ = 2', f: x => x / (x - 2), xi: 2, win: [-1, 5, -6, 8], L: '−∞', R: '+∞', val: NaN, ok: null, note: 'x = 2 gehört nicht zu D(f). Die Funktion ist trotzdem „stetig“: stetig in allen Punkten ihres Definitionsbereiches.' },
    sq: { name: 'x² bei ξ = π', f: x => x * x, xi: Math.PI, win: [0, 5, -1, 16], L: 'π²', R: 'π²', val: Math.PI ** 2, ok: true, note: 'So rechnet man mit π: x² auf 3, 3.1, 3.14, … auswerten. Das ist erlaubt, weil x² stetig ist.' },
  };
  let key = 'g0', ld = Math.log10(0.5);
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], d = Math.pow(10, ld), [x0, x1, y0, y1] = s.win, A = mkAx(x0, x1, y0, y1); axes(v, A, 'x', 'y');
    fplot(v, A, s.f, C.c2, 2.3, 1600, x0, s.xi - 1e-6); fplot(v, A, s.f, C.c2, 2.3, 1600, s.xi + 1e-6, x1);
    v.line(A.P(s.xi, y0), A.P(s.xi, y1), C.muted, 1, [4, 4]);
    const yl = s.f(s.xi - d), yr = s.f(s.xi + d);
    if (A.inY(yl)) v.dot(A.P(s.xi - d, yl), C.c3, 6); else v.text(A.P(s.xi - d, yl > y1 ? y1 : y0), yl > y1 ? '↑' : '↓', C.c3, -4, yl > y1 ? 14 : -4, 16);
    if (A.inY(yr)) v.dot(A.P(s.xi + d, yr), C.c4, 6); else v.text(A.P(s.xi + d, yr > y1 ? y1 : y0), yr > y1 ? '↑' : '↓', C.c4, -4, yr > y1 ? 14 : -4, 16);
    if (isFinite(s.val)) v.dot(A.P(s.xi, s.val), C.c1, 6);
    const head = s.ok === true ? 'stetig in ξ' : s.ok === false ? 'nicht stetig in ξ' : 'ξ ∉ D(f): Frage nach Stetigkeit stellt sich nicht';
    const show = y => !isFinite(y) ? '–' : Math.abs(y) > 1e6 ? y.toExponential(2) : fmt(y, 5);
    MW.info(infoEl, head, [['f(ξ − δ)', show(yl)], ['f(ξ)', isFinite(s.val) ? fmt(s.val, 5) : 'nicht definiert'], ['f(ξ + δ)', show(yr)], ['lim links / rechts', s.L + '  /  ' + s.R]], s.note, s.ok === false);
  });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); });
  MW.slider(ctl, { label: 'δ', min: -4, max: 0, step: 0.01, value: ld, fmt: x => fmt(Math.pow(10, x), 4), onInput: x => { ld = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('analysis-w2', W))
