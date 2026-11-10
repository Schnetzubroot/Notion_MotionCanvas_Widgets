"""Widgets zu Kapitel 1 (Woche 1): Bewegung eines materiellen Punktes."""
from template import build

W = []

# ---------------------------------------------------------------- 1.1
W.append(dict(file='1-1-bezugskoerper.html', title='Bewegung hängt vom Bezugskörper ab',
  sub='Ein Ball fällt im fahrenden Zug aus der Hand. Wähle, von welchem Bezugskörper aus du die Bewegung beschreibst.',
  hint='Abspielen und Bezugskörper wechseln.', legend=[('--c1', 'Bahnkurve des Balls')], js=r'''
  const u = 2.5, g = 9.81, h = 2, T = Math.sqrt(2 * h / g);
  let frame = 'zug', t = 0.75 * T;
  const view = MW.View2D(cv, { xmin: -1.2, xmax: 3.6, ymin: -0.4, ymax: 2.6 }, v => {
    const C = v.C, sh = frame === 'zug' ? 0 : u * t;          // Verschiebung des Zuges im gewählten System
    const gshift = frame === 'zug' ? -u * t : 0;               // Verschiebung des Bodens
    for (let x = -3; x < 8; x += 0.4) v.line([x + (gshift % 0.4), 0], [x + (gshift % 0.4) - 0.15, -0.15], C.muted, 1);
    v.line([-2, 0], [6, 0], C.muted, 2);
    v.poly([[sh - 0.6, 0.1], [sh + 1.6, 0.1], [sh + 1.6, 2.4], [sh - 0.6, 2.4]], C.line, 2, null, true, C.fill);
    v.text([sh - 0.55, 2.25], 'Zug', C.muted, 0, 0, 12, false);
    const ball = tt => [0.5 + (frame === 'zug' ? 0 : u * tt), h - g * tt * tt / 2];
    const pts = []; for (let i = 0; i <= 60; i++) pts.push(ball(t * i / 60));
    v.poly(pts, C.c1, 2.5);
    v.dot(ball(t), C.c1, 7);
    v.text([-1.1, 2.45], 'Bezugskörper: ' + (frame === 'zug' ? 'Zug (Boden bewegt sich)' : 'Boden (Zug bewegt sich)'), C.fg, 0, 0, 13);
    MW.info(infoEl, frame === 'zug' ? 'Im Zug: senkrechte Gerade' : 'Vom Boden aus: Parabel',
      [['Zeit t', fmt(t) + ' s'], ['Zuggeschwindigkeit', u + ' m/s']],
      'Dieselbe Bewegung hat je nach Bezugskörper eine andere Bahnkurve. Deshalb muss man immer zuerst den Bezugskörper festlegen.');
  });
  MW.select(ctl, 'Bezugskörper:', [['zug', 'Zug'], ['boden', 'Boden']], f => { frame = f; view.redraw(); });
  MW.player(ctl, { t0: 0, t1: T, duration: 3, value: 0.75 * T, onTime: x => { t = x; view.redraw(); }, fmt: x => fmt(x) + ' s' });
'''))

W.append(dict(file='1-1-starrer-koerper.html', title='Starrer Körper: Abstände bleiben konstant',
  sub='Eine Platte verschiebt und dreht sich. Der Abstand zwischen zwei beliebigen Punkten P und Q bleibt immer gleich.',
  hint='Abspielen oder Zeit ziehen.', legend=[('--c2', 'Platte'), ('--c3', 'Abstand a = |PQ|')], js=r'''
  let t = 0.5;
  const shape = [[-1, -0.6], [1.2, -0.6], [1.4, 0.5], [-0.4, 0.9]], P = [-0.6, -0.3], Q = [1.0, 0.4];
  const pose = tt => ({ c: [-2 + 3.2 * tt, 0.3 + 0.8 * Math.sin(Math.PI * tt)], a: 1.4 * tt });
  const tr = (p, ps) => [ps.c[0] + p[0] * Math.cos(ps.a) - p[1] * Math.sin(ps.a), ps.c[1] + p[0] * Math.sin(ps.a) + p[1] * Math.cos(ps.a)];
  const view = MW.View2D(cv, { xmin: -3.6, xmax: 3.6, ymin: -1.6, ymax: 2.4 }, v => {
    const C = v.C;
    [0, 1].forEach(k => { const ps = pose(k); v.poly(shape.map(p => tr(p, ps)), C.line, 1, [4, 4], true); });
    v.text(tr([-1, -0.6], pose(0)), 'Lage zur Zeit t₁', C.muted, 0, 16, 12, false);
    v.text(tr([1.2, -0.6], pose(1)), 'Lage zur Zeit t₂', C.muted, -60, 16, 12, false);
    const ps = pose(t), p = tr(P, ps), q = tr(Q, ps);
    v.poly(shape.map(s => tr(s, ps)), C.c2, 2, null, true, C.fill);
    v.line(p, q, C.c3, 3); v.dot(p, C.fg, 5); v.dot(q, C.fg, 5);
    v.text(p, 'P', C.fg, -14, 16); v.text(q, 'Q', C.fg, 6, -6);
    v.text([(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], 'a', C.c3, 6, -8);
    MW.info(infoEl, 'Abstand bleibt konstant', [['Zeit', fmt(t)], ['a = |PQ|', fmt(Math.hypot(q[0] - p[0], q[1] - p[1]), 3)]],
      'Die Lage ändert sich (Verschiebung und Drehung), aber der Abstand a ändert sich nie. Genau das definiert einen starren Körper.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 4, value: 0.5, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='1-1-rechtssystem.html', title='Rechtssystem Oxyz',
  sub='Die positiven Achsen Ox, Oy, Oz bilden ein Rechtssystem: e<sub>x</sub> × e<sub>y</sub> = e<sub>z</sub> (rechte Hand: Daumen x, Zeigefinger y, Mittelfinger z).',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'e_x'), ('--c3', 'e_y'), ('--c2', 'e_z'), ('--c5', 'e_x × e_y')], js=r'''
  let flip = false;
  const view = MW.View3D(cv, { extent: 1.8, yaw: 35, pitch: 20 }, v => {
    const C = v.C, ex = [1, 0, 0], ey = flip ? [0, -1, 0] : [0, 1, 0], ez = [0, 0, 1];
    v.arrow([0, 0, 0], ex, C.c1, 3); v.text(ex, 'x', C.c1, 4, 4);
    v.arrow([0, 0, 0], ey, C.c3, 3); v.text(ey, 'y', C.c3, 4, 4);
    v.arrow([0, 0, 0], ez, C.c2, 3); v.text(ez, 'z', C.c2, 4, 4);
    const c = V.cross(ex, ey);
    v.arrow([0, 0, 0], V.mul(c, 1.3), C.c5, 1.8); v.text(V.mul(c, 1.3), 'e_x × e_y', C.c5, 6, 0, 12);
    const ok = V.dot(c, ez) > 0;
    MW.info(infoEl, ok ? 'Rechtssystem' : 'Linkssystem (nicht erlaubt)', [['e_x × e_y', fv(c, 0)], ['e_z', fv(ez, 0)]],
      ok ? 'e_x × e_y zeigt in Richtung e_z.' : 'Mit umgedrehter y-Achse zeigt e_x × e_y entgegen e_z. Alle Formeln mit Kreuzprodukten bekämen falsche Vorzeichen.', !ok);
  });
  MW.check(ctl, 'y-Achse umdrehen', false, f => { flip = f; view.redraw(); });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

# ---------------------------------------------------------------- 1.2
W.append(dict(file='1-2-kartesisch-punkt.html', title='Kartesische Koordinaten eines Punktes',
  sub='x, y, z sind die Abstände der Projektionen M<sub>x</sub>, M<sub>y</sub>, M<sub>z</sub> vom Ursprung, mit Vorzeichen.',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'x'), ('--c3', 'y'), ('--c2', 'z')], js=r'''
  const s = { x: 2, y: 1.5, z: 1.5 };
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, { x, y, z } = s, M = [x, y, z], Mxy = [x, y, 0];
    v.floor(3); v.axes(3.2);
    v.line([x, 0, 0], Mxy, C.muted, 1, [4, 4]); v.line([0, y, 0], Mxy, C.muted, 1, [4, 4]);
    v.line(Mxy, M, C.muted, 1, [4, 4]); v.line([0, 0, z], M, C.muted, 1, [4, 4]);
    v.line([0, 0, 0], [x, 0, 0], C.c1, 4); v.line([0, 0, 0], [0, y, 0], C.c3, 4); v.line([0, 0, 0], [0, 0, z], C.c2, 4);
    v.dot([x, 0, 0], C.c1, 4); v.text([x, 0, 0], 'Mx', C.c1, -6, 18, 12);
    v.dot([0, y, 0], C.c3, 4); v.text([0, y, 0], 'My', C.c3, 4, 16, 12);
    v.dot([0, 0, z], C.c2, 4); v.text([0, 0, z], 'Mz', C.c2, -26, 0, 12);
    v.dot(Mxy, C.muted, 3); v.text(Mxy, 'Mxy', C.muted, 6, 14, 11, false);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -6);
    MW.info(infoEl, 'M = (' + fmt(x) + ', ' + fmt(y) + ', ' + fmt(z) + ')',
      [['x = OMx', fmt(x)], ['y = OMy', fmt(y)], ['z = OMz', fmt(z)], ['Abstand |OM|', fmt(Math.hypot(x, y, z))]],
      'Jede Koordinate liegt in (−∞, ∞). Das Vorzeichen sagt, auf welcher Seite von O die Projektion liegt.');
  });
  ['x', 'y', 'z'].forEach(k => MW.slider(ctl, { label: k, min: -3, max: 3, step: 0.1, value: s[k], onInput: val => { s[k] = val; view.redraw(); } }));
'''))

W.append(dict(file='1-2-kartesisch-linien.html', title='Kartesische Koordinatenlinien',
  sub='Hält man zwei Koordinaten fest und ändert die dritte, läuft der Punkt auf einer Geraden parallel zur Achse dieser Koordinate.',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'x-Linie (y, z fest)'), ('--c3', 'y-Linie (x, z fest)'), ('--c2', 'z-Linie (x, y fest)')], js=r'''
  const s = { x: 1.5, y: 1.5, z: 1 };
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, M = [s.x, s.y, s.z];
    v.floor(3); v.axes(3.2);
    v.line([-3, s.y, s.z], [3, s.y, s.z], C.c1, 2.5); v.line([s.x, -3, s.z], [s.x, 3, s.z], C.c3, 2.5); v.line([s.x, s.y, -2.5], [s.x, s.y, 2.5], C.c2, 2.5);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    MW.info(infoEl, 'Drei Geraden, paarweise senkrecht', [['M', fv(M)]],
      'Kartesische Koordinaten sind geradlinig orthogonal: Alle drei Koordinatenlinien sind Geraden und stehen in M senkrecht aufeinander.');
  });
  ['x', 'y', 'z'].forEach(k => MW.slider(ctl, { label: k, min: -2.5, max: 2.5, step: 0.1, value: s[k], onInput: val => { s[k] = val; view.redraw(); } }));
'''))

W.append(dict(file='1-2-kartesisch-flaechen.html', title='Kartesische Koordinatenfläche',
  sub='Hält man nur eine Koordinate fest, kann sich der Punkt in einer Ebene bewegen, die parallel zu einer Koordinatenebene ist.',
  hint='Ziehen zum Drehen.', js=r'''
  const s = { x: 1.5, y: 1, z: 1 }; let keep = 'z';
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, M = [s.x, s.y, s.z], L = 2.6;
    v.floor(3); v.axes(3.2);
    let q;
    if (keep === 'z') q = [[-L, -L, s.z], [L, -L, s.z], [L, L, s.z], [-L, L, s.z]];
    if (keep === 'x') q = [[s.x, -L, -L], [s.x, L, -L], [s.x, L, L], [s.x, -L, L]];
    if (keep === 'y') q = [[-L, s.y, -L], [L, s.y, -L], [L, s.y, L], [-L, s.y, L]];
    v.poly(q, C.c2, 1.5, null, true, C.fill);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    const name = { z: 'parallel zu Oxy', x: 'parallel zu Oyz', y: 'parallel zu Ozx' }[keep];
    MW.info(infoEl, keep + ' = ' + fmt(s[keep]) + ': Ebene ' + name, [['M', fv(M)]], 'Die drei kartesischen Koordinatenflächen durch M sind Ebenen und stehen senkrecht aufeinander.');
  });
  MW.select(ctl, 'Fest halten:', [['z', 'z = konst.'], ['x', 'x = konst.'], ['y', 'y = konst.']], k => { keep = k; view.redraw(); });
  ['x', 'y', 'z'].forEach(k => MW.slider(ctl, { label: k, min: -2.5, max: 2.5, step: 0.1, value: s[k], onInput: val => { s[k] = val; view.redraw(); } }));
'''))

W.append(dict(file='1-2-bahnkurve-ellipse.html', title='Bahnkurve: Stabspitze (Buchbeispiel Fig. 1.6)',
  sub='x = 3 cos(3πt), y = 4 cos(3πt), z = sin(3πt) in cm, t ∈ [0, 1] s. Die Bahnkurve ist eine Ellipse in der Ebene y = 4x/3.',
  hint='Abspielen oder t ziehen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'Bahnkurve'), ('--c2', 'Ebene y = 4x/3')], js=r'''
  let t = 0.45;
  const r = tt => [3 * Math.cos(3 * Math.PI * tt), 4 * Math.cos(3 * Math.PI * tt), Math.sin(3 * Math.PI * tt)];
  const view = MW.View3D(cv, { extent: 4.2, yaw: -40, pitch: 20 }, v => {
    const C = v.C; v.axes(4.5);
    v.poly([[-3.6, -4.8, -1.4], [3.6, 4.8, -1.4], [3.6, 4.8, 1.4], [-3.6, -4.8, 1.4]], null, 1, null, true, C.fill);
    const all = []; for (let i = 0; i <= 120; i++) all.push(r(i / 120 * (2 / 3)));
    v.poly(all, C.line, 1, [4, 4]);
    const tr = []; for (let i = 0; i <= 120; i++) tr.push(r(t * i / 120));
    v.poly(tr, C.c1, 2.5);
    v.dot(r(0), C.muted, 4); v.text(r(0), 'M(0)', C.muted, 6, 14, 12, false);
    v.dot(r(1), C.muted, 4); v.text(r(1), 'M(1)', C.muted, 6, 14, 12, false);
    const M = r(t); v.dot(M, C.fg, 6); v.text(M, 'M(t)', C.fg, 8, -8);
    MW.info(infoEl, 't = ' + fmt(t) + ' s', [['x', fmt(M[0]) + ' cm'], ['y', fmt(M[1]) + ' cm'], ['z', fmt(M[2]) + ' cm'], ['y − 4x/3', fmt(M[1] - 4 * M[0] / 3)]],
      'Drei Funktionen x(t), y(t), z(t) beschreiben die Bewegung. Zusammen sind sie die Parameterdarstellung der Bahnkurve. y − 4x/3 ist immer 0: Die Kurve liegt in einer Ebene.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 6, value: 0.45, onTime: x => { t = x; view.redraw(); }, fmt: x => fmt(x) + ' s' });
'''))

# ---------------------------------------------------------------- 1.3
W.append(dict(file='1-3-zylindrisch-punkt.html', title='Zylindrische Koordinaten (ρ, φ, z)',
  sub='ρ = Abstand von der z-Achse, φ = Winkel von Ox zur Projektion OM<sub>xy</sub> (gegen den Uhrzeigersinn positiv), z wie kartesisch.',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'ρ'), ('--c3', 'φ'), ('--c2', 'z')], js=r'''
  const s = { rho: 2, phi: 1.1, z: 1.5 };
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, x = s.rho * Math.cos(s.phi), y = s.rho * Math.sin(s.phi), M = [x, y, s.z], Mxy = [x, y, 0];
    v.floor(3); v.axes(3.2);
    v.line([0, 0, 0], Mxy, C.c1, 4); v.text(V.mul(Mxy, 0.5), 'ρ', C.c1, 4, 16);
    const arc = v.circlePts([0, 0, 0], [0, 0, 1], 0.9, 0, s.phi, 40, [1, 0, 0]); v.poly(arc, C.c3, 2.5);
    v.text(arc[Math.floor(arc.length / 2)], 'φ', C.c3, 4, 14);
    v.line(Mxy, M, C.c2, 4); v.text(V.add(Mxy, [0, 0, s.z / 2]), 'z', C.c2, 8, 0);
    v.line([0, 0, 0], [0, 0, s.z], C.muted, 1, [4, 4]); v.line([0, 0, s.z], M, C.muted, 1, [4, 4]);
    v.dot(Mxy, C.muted, 3); v.text(Mxy, 'Mxy', C.muted, 6, 14, 11, false);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    MW.info(infoEl, '(ρ, φ, z) = (' + fmt(s.rho) + ', ' + fmt(s.phi) + ', ' + fmt(s.z) + ')',
      [['x = ρ cos φ', fmt(x)], ['y = ρ sin φ', fmt(y)], ['z', fmt(s.z)], ['φ in Grad', fmt(s.phi * 180 / Math.PI, 1) + '°']],
      s.rho < 0.05 ? 'ρ = 0: M liegt auf der z-Achse. Dort ist φ beliebig, also nicht eindeutig (Koordinatensingularität).' : 'Wertebereiche: ρ ∈ [0, ∞), φ ∈ (−∞, ∞), z ∈ (−∞, ∞).');
  });
  MW.slider(ctl, { label: 'ρ', min: 0, max: 3, step: 0.05, value: s.rho, onInput: x => { s.rho = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: -3.14, max: 6.28, step: 0.01, value: s.phi, onInput: x => { s.phi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'z', min: -2, max: 2.5, step: 0.05, value: s.z, onInput: x => { s.z = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-umrechnung-quadrant.html', title='Umrechnung kartesisch → zylindrisch: Achtung beim Winkel',
  sub='ρ = √(x² + y²). Für φ liefert der Taschenrechner arctan(y/x) nur Werte zwischen −90° und 90°. Im 2. und 3. Quadranten muss man 180° addieren.',
  hint='Ziehe den Punkt M (Draufsicht auf die xy-Ebene).', legend=[('--c1', 'ρ'), ('--c3', 'richtiger Winkel φ'), ('--c4', 'arctan(y/x)')], js=r'''
  let M = [-1.5, 1.2];
  const view = MW.View2D(cv, { xmin: -3, xmax: 3, ymin: -2.4, ymax: 2.4 }, v => {
    const C = v.C; v.grid(1);
    const phi = Math.atan2(M[1], M[0]), naive = Math.abs(M[0]) < 1e-9 ? NaN : Math.atan(M[1] / M[0]);
    v.line([0, 0], M, C.c1, 3); v.text(V.mul(M, 0.5), 'ρ', C.c1, 4, -6);
    v.arc([0, 0], 0.6, 0, phi < 0 ? phi + 2 * Math.PI : phi, C.c3, 2.5);
    if (isFinite(naive)) { v.arc([0, 0], 0.95, 0, naive, C.c4, 2, [4, 3]); v.line([0, 0], [2.6 * Math.cos(naive), 2.6 * Math.sin(naive)], C.c4, 1, [4, 3]); }
    v.dot(M, C.fg, 7); v.text(M, 'M', C.fg, 8, -8);
    const wrong = isFinite(naive) && Math.abs(Math.cos(naive - phi) - 1) > 1e-6;
    const d = x => fmt(x * 180 / Math.PI, 1) + '°';
    MW.info(infoEl, wrong ? 'arctan(y/x) zeigt in die falsche Richtung' : 'arctan(y/x) stimmt hier',
      [['x, y', fmt(M[0]) + ', ' + fmt(M[1])], ['ρ = √(x² + y²)', fmt(Math.hypot(M[0], M[1]))], ['richtiges φ', d(phi < 0 ? phi + 2 * Math.PI : phi)], ['arctan(y/x)', isFinite(naive) ? d(naive) : 'nicht definiert (x = 0)']],
      wrong ? 'M liegt links der y-Achse (x < 0). Richtig ist φ = arctan(y/x) + 180°.' : 'Für x > 0 (1. und 4. Quadrant) ist arctan(y/x) korrekt.', wrong);
  });
  view.handle(() => M, p => { M = [Math.round(p[0] * 10) / 10, Math.round(p[1] * 10) / 10]; });
'''))

W.append(dict(file='1-3-zylindrisch-linien.html', title='Zylindrische Koordinatenlinien',
  sub='Durch M gehen drei Koordinatenlinien: eine radiale Halbgerade (φ, z fest), ein Parallelkreis (ρ, z fest) und eine axiale Gerade (ρ, φ fest).',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'ρ-Linie: Halbgerade'), ('--c3', 'φ-Linie: Kreis'), ('--c2', 'z-Linie: Gerade')], js=r'''
  const s = { rho: 1.8, phi: 1.1, z: 1 };
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, c = Math.cos(s.phi), sn = Math.sin(s.phi), M = [s.rho * c, s.rho * sn, s.z];
    v.floor(3); v.axes(3.2);
    v.line([0, 0, s.z], [3.2 * c, 3.2 * sn, s.z], C.c1, 2.5); v.dot([0, 0, s.z], C.c1, 3);
    v.poly(v.circlePts([0, 0, s.z], [0, 0, 1], s.rho, 0, 2 * Math.PI, 90, [1, 0, 0]), C.c3, 2.5);
    v.line([M[0], M[1], -2.5], [M[0], M[1], 2.8], C.c2, 2.5);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    MW.info(infoEl, 'Krummlinig orthogonal', [['(ρ, φ, z)', '(' + fmt(s.rho) + ', ' + fmt(s.phi) + ', ' + fmt(s.z) + ')']],
      'Die drei Linien stehen in M senkrecht aufeinander, aber die φ-Linie ist ein Kreis. Die ρ-Linie beginnt auf der z-Achse und ist nur eine Halbgerade, weil ρ ≥ 0.');
  });
  MW.slider(ctl, { label: 'ρ', min: 0.3, max: 2.8, step: 0.05, value: s.rho, onInput: x => { s.rho = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: 0, max: 6.28, step: 0.01, value: s.phi, onInput: x => { s.phi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'z', min: -2, max: 2.5, step: 0.05, value: s.z, onInput: x => { s.z = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-zylindrisch-flaechen.html', title='Zylindrische Koordinatenfläche',
  sub='Hält man eine Koordinate fest, entsteht eine Fläche: ρ = konst. ist ein Kreiszylinder, φ = konst. eine Halbebene durch Oz, z = konst. eine Ebene.',
  hint='Ziehen zum Drehen.', js=r'''
  const s = { rho: 1.6, phi: 1.1, z: 1 }; let keep = 'rho';
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, c = Math.cos(s.phi), sn = Math.sin(s.phi), M = [s.rho * c, s.rho * sn, s.z];
    v.floor(3); v.axes(3.2);
    if (keep === 'rho') {
      for (const zz of [-1.5, -0.5, 0.5, 1.5, 2.5]) v.poly(v.circlePts([0, 0, zz], [0, 0, 1], s.rho, 0, 2 * Math.PI, 72, [1, 0, 0]), C.c2, 1);
      for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; v.line([s.rho * Math.cos(a), s.rho * Math.sin(a), -1.5], [s.rho * Math.cos(a), s.rho * Math.sin(a), 2.5], C.c2, 1); }
    } else if (keep === 'phi') {
      v.poly([[0, 0, -1.5], [3 * c, 3 * sn, -1.5], [3 * c, 3 * sn, 2.5], [0, 0, 2.5]], C.c2, 1.5, null, true, C.fill);
      v.line([0, 0, -1.5], [0, 0, 2.5], C.c2, 3);
    } else {
      v.poly(v.circlePts([0, 0, s.z], [0, 0, 1], 2.8, 0, 2 * Math.PI, 72, [1, 0, 0]), C.c2, 1.5, null, true, C.fill);
    }
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    const head = { rho: 'ρ = ' + fmt(s.rho) + ': Kreiszylinder um die z-Achse', phi: 'φ = ' + fmt(s.phi) + ': Halbebene, die an der z-Achse endet', z: 'z = ' + fmt(s.z) + ': Ebene parallel zu Oxy' }[keep];
    MW.info(infoEl, head, [], keep === 'phi' ? 'Nur eine Halbebene! Die Ebene x = 0 besteht deshalb aus zwei Halbebenen: φ = π/2 und φ = −π/2 (ZP1 2025, A1.4 f).' : 'Der Name „zylindrische Koordinaten“ kommt von der Fläche ρ = konstant.');
  });
  MW.select(ctl, 'Fest halten:', [['rho', 'ρ = konst.'], ['phi', 'φ = konst.'], ['z', 'z = konst.']], k => { keep = k; view.redraw(); });
  MW.slider(ctl, { label: 'ρ', min: 0.3, max: 2.8, step: 0.05, value: s.rho, onInput: x => { s.rho = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: 0, max: 6.28, step: 0.01, value: s.phi, onInput: x => { s.phi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'z', min: -1.5, max: 2.5, step: 0.05, value: s.z, onInput: x => { s.z = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-elektron.html', title='Elektron zwischen Kathode und Anode (Buchbeispiel Fig. 1.9)',
  sub='ρ = R₁ + a t, φ = b t, z = a t. Das Elektron startet auf der Kathode (ρ = R₁) und erreicht die Anode (ρ = R₂) zur Zeit t₂ = (R₂ − R₁)/a.',
  hint='Abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'Bahnkurve'), ('--line', 'Kathode R₁, Anode R₂')], js=r'''
  const R1 = 0.6, R2 = 2.4, a = 1, b = 4.5, t2 = (R2 - R1) / a; let t = 1.2;
  const r = tt => [(R1 + a * tt) * Math.cos(b * tt), (R1 + a * tt) * Math.sin(b * tt), a * tt];
  const view = MW.View3D(cv, { extent: 3, yaw: 30, pitch: 18, center: [0, 0, 0.9] }, v => {
    const C = v.C; v.axes(2.8);
    for (const R of [R1, R2]) for (const zz of [0, t2 * a]) v.poly(v.circlePts([0, 0, zz], [0, 0, 1], R, 0, 2 * Math.PI, 72, [1, 0, 0]), C.line, 1);
    for (const R of [R1, R2]) for (let k = 0; k < 8; k++) { const q = k * Math.PI / 4; v.line([R * Math.cos(q), R * Math.sin(q), 0], [R * Math.cos(q), R * Math.sin(q), t2 * a], C.line, 1); }
    const pts = []; for (let i = 0; i <= 200; i++) pts.push(r(t * i / 200));
    v.poly(pts, C.c1, 2.5);
    const M = r(t); v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    const rho = R1 + a * t;
    MW.info(infoEl, 't = ' + fmt(t) + (t >= t2 - 1e-6 ? ' = t₂: Elektron trifft die Anode' : ''),
      [['ρ', fmt(rho)], ['φ', fmt(b * t)], ['z', fmt(a * t)], ['ρ − z', fmt(rho - a * t) + ' = R₁']],
      'ρ − z ist immer R₁: Die Bahn liegt auf einem Kegel mit halbem Öffnungswinkel π/4 um die z-Achse („Schraubenlinie auf einem Kegel“).');
  });
  MW.player(ctl, { t0: 0, t1: t2, duration: 5, loop: false, value: 1.2, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-kreispendel.html', title='Kreisbewegung: harmonische Schwingung eines Kreispendels',
  sub='ρ = R ist konstant, die Bewegung steckt ganz im Drehwinkel φ(t) = φ₀ sin(2πt/T). Die Bogenlänge s = Rφ kann ebenfalls als Parameter dienen.',
  hint='Abspielen, φ₀ ändern.', legend=[('--c3', 'Winkel φ'), ('--c1', 'Bogenlänge s = Rφ')], js=r'''
  const R = 2; let t = 0.15, phi0 = 0.6;
  const view = MW.View2D(cv, { xmin: -2.8, xmax: 2.8, ymin: -2.6, ymax: 0.5 }, v => {
    const C = v.C, phi = phi0 * Math.sin(2 * Math.PI * t), down = -Math.PI / 2;
    v.line([-0.6, 0], [0.6, 0], C.muted, 3);
    v.arc([0, 0], R, down - phi0, down + phi0, C.line, 1, [4, 4]);
    v.line([0, 0], [0, -R - 0.2], C.muted, 1, [4, 4]);
    const M = [R * Math.cos(down + phi), R * Math.sin(down + phi)];
    v.arc([0, 0], R, down, down + phi, C.c1, 4);
    v.arc([0, 0], 0.5, down, down + phi, C.c3, 2.5);
    v.line([0, 0], M, C.fg, 2); v.dot(M, C.fg, 9); v.dot([0, 0], C.fg, 4); v.text([0, 0], 'O', C.fg, 6, -6);
    MW.info(infoEl, 'φ = ' + fmt(phi) + ' rad = ' + fmt(phi * 180 / Math.PI, 1) + '°',
      [['t / T', fmt(t)], ['s = R φ', fmt(R * phi)], ['Amplitude φ₀', fmt(phi0)], ['R', fmt(R)]],
      'Bogenlänge s = Rφ gilt nur mit φ im Bogenmaß.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 3, value: 0.15, onTime: x => { t = x; view.redraw(); }, label: 't/T' });
  MW.slider(ctl, { label: 'φ₀', min: 0.1, max: 1.4, step: 0.05, value: phi0, onInput: x => { phi0 = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-zp24-treffen.html', title='ZP1 2024 A1.2: Wann treffen sich M₁ und M₂?',
  sub='M₁: ρ = R, φ = (2π/3) sin(μt), z = 2Rt/T − R/2.  M₂: x = Rt/T, y = √3 Rt/T, z = R(t²/T² + 1/4).  Mit R = T = 1.',
  hint='μ wählen, dann abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'M₁ (zylindrisch)'), ('--c2', 'M₂ (kartesisch)')], js=r'''
  let mu = Math.PI / 3, t = 0.5;
  const m1 = tt => { const p = 2 * Math.PI / 3 * Math.sin(mu * tt); return [Math.cos(p), Math.sin(p), 2 * tt - 0.5]; };
  const m2 = tt => [tt, Math.sqrt(3) * tt, tt * tt + 0.25];
  const view = MW.View3D(cv, { extent: 1.8, yaw: 20, pitch: 18, center: [0, 0.4, 0.4] }, v => {
    const C = v.C; v.axes(1.6);
    for (const zz of [-0.5, 0.5, 1.5]) v.poly(v.circlePts([0, 0, zz], [0, 0, 1], 1, 0, 2 * Math.PI, 72, [1, 0, 0]), C.line, 1);
    const p1 = [], p2 = []; for (let i = 0; i <= 100; i++) { const tt = t * i / 100; p1.push(m1(tt)); p2.push(m2(tt)); }
    v.poly(p1, C.c1, 2.5); v.poly(p2, C.c2, 2.5);
    const A = m1(t), B = m2(t); v.dot(A, C.c1, 6); v.dot(B, C.c2, 6); v.text(A, 'M₁', C.c1, 8, -6); v.text(B, 'M₂', C.c2, 8, 14);
    const d = V.norm(V.sub(A, B));
    MW.info(infoEl, d < 0.02 ? 'Die Punkte treffen sich!' : 'Abstand |M₁M₂| = ' + fmt(d),
      [['t / T', fmt(t)], ['μ T', fmt(mu)], ['ρ₂ = 2Rt/T', fmt(2 * t)], ['φ₁', fmt(2 * Math.PI / 3 * Math.sin(mu * t))]],
      'ρ₂ = R nur bei t = T/2. Dann stimmt auch z (beide R/2). φ₂ = π/3 erfordert sin(μT/2) = 1/2, also μ = π/(3T) (oder 5π/(3T)).');
  });
  MW.select(ctl, 'μT =', [[String(Math.PI / 3), 'π/3 (Lösung f)'], [String(Math.PI / 6), 'π/6 (Falle d)'], [String(5 * Math.PI / 6), '5π/6 (Falle b)'], [String(5 * Math.PI / 3), '5π/3 (zweite Lösung)']], x => { mu = +x; view.redraw(); });
  MW.player(ctl, { t0: 0, t1: 1, duration: 5, loop: false, value: 0.5, onTime: x => { t = x; view.redraw(); }, label: 't/T' });
'''))

# ---------------------------------------------------------------- 1.4
W.append(dict(file='1-4-sphaerisch-punkt.html', title='Sphärische Koordinaten (r, θ, ψ)',
  sub='r = |OM|, θ = Winkel von der z-Achse zu OM (nicht von der xy-Ebene!), ψ = Winkel von Ox zu OM<sub>xy</sub> (wie φ).',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'r'), ('--c4', 'θ (ab z-Achse)'), ('--c3', 'ψ')], js=r'''
  const s = { r: 2.5, th: 0.8, ps: 1.1 };
  const view = MW.View3D(cv, { extent: 3.2 }, v => {
    const C = v.C, st = Math.sin(s.th), M = [s.r * st * Math.cos(s.ps), s.r * st * Math.sin(s.ps), s.r * Math.cos(s.th)], Mxy = [M[0], M[1], 0];
    v.floor(3); v.axes(3.2);
    v.line([0, 0, 0], M, C.c1, 4); v.text(V.mul(M, 0.55), 'r', C.c1, 6, -4);
    const n = V.cross([0, 0, 1], [Math.cos(s.ps), Math.sin(s.ps), 0]);
    const th = v.circlePts([0, 0, 0], n, 0.9, 0, s.th, 40, [0, 0, 1]);
    v.poly(th, C.c4, 2.5); v.text(th[20], 'θ', C.c4, 4, -4);
    const ps = v.circlePts([0, 0, 0], [0, 0, 1], 0.7, 0, s.ps, 40, [1, 0, 0]); v.poly(ps, C.c3, 2.5); v.text(ps[20], 'ψ', C.c3, 4, 14);
    v.line([0, 0, 0], Mxy, C.muted, 1, [4, 4]); v.line(Mxy, M, C.muted, 1, [4, 4]);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    MW.info(infoEl, '(r, θ, ψ) = (' + fmt(s.r) + ', ' + fmt(s.th) + ', ' + fmt(s.ps) + ')',
      [['x = r sin θ cos ψ', fmt(M[0])], ['y = r sin θ sin ψ', fmt(M[1])], ['z = r cos θ', fmt(M[2])], ['ρ = r sin θ', fmt(s.r * st)]],
      'θ = 0: Nordpol (auf +z). θ = π/2: in der xy-Ebene (z = 0). θ = π: Südpol. Häufigste Prüfungsfalle: z = r cos θ, nicht r sin θ.');
  });
  MW.slider(ctl, { label: 'r', min: 0.5, max: 3, step: 0.05, value: s.r, onInput: x => { s.r = x; view.redraw(); } });
  MW.slider(ctl, { label: 'θ', min: 0, max: 3.14, step: 0.01, value: s.th, onInput: x => { s.th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ψ', min: 0, max: 6.28, step: 0.01, value: s.ps, onInput: x => { s.ps = x; view.redraw(); } });
'''))

W.append(dict(file='1-4-sphaerisch-linien.html', title='Sphärische Koordinatenlinien',
  sub='Durch M gehen: eine radiale Halbgerade (θ, ψ fest), ein Meridiankreis (r, ψ fest) und ein Parallelkreis (r, θ fest).',
  hint='Ziehen zum Drehen.', legend=[('--c1', 'r-Linie: Halbgerade'), ('--c4', 'θ-Linie: Meridian'), ('--c3', 'ψ-Linie: Parallelkreis')], js=r'''
  const s = { r: 2, th: 0.9, ps: 1.1 };
  const view = MW.View3D(cv, { extent: 3 }, v => {
    const C = v.C, er = [Math.sin(s.th) * Math.cos(s.ps), Math.sin(s.th) * Math.sin(s.ps), Math.cos(s.th)], M = V.mul(er, s.r);
    v.axes(3);
    v.poly(v.circlePts([0, 0, 0], [0, 0, 1], s.r, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [3, 3]);
    v.line([0, 0, 0], V.mul(er, 3.2), C.c1, 2.5);
    const n = V.cross([0, 0, 1], [Math.cos(s.ps), Math.sin(s.ps), 0]);
    v.poly(v.circlePts([0, 0, 0], n, s.r, 0, Math.PI, 90, [0, 0, 1]), C.c4, 2.5);
    v.poly(v.circlePts([0, 0, s.r * Math.cos(s.th)], [0, 0, 1], s.r * Math.sin(s.th), 0, 2 * Math.PI, 90, [1, 0, 0]), C.c3, 2.5);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    MW.info(infoEl, 'Krummlinig orthogonal', [['(r, θ, ψ)', '(' + fmt(s.r) + ', ' + fmt(s.th) + ', ' + fmt(s.ps) + ')']],
      'Der Meridian läuft von Pol zu Pol (θ von 0 bis π). Auf der z-Achse (θ = 0 oder π) ist ψ nicht definiert, im Ursprung sind es θ und ψ (Koordinatensingularitäten).');
  });
  MW.slider(ctl, { label: 'r', min: 0.6, max: 2.6, step: 0.05, value: s.r, onInput: x => { s.r = x; view.redraw(); } });
  MW.slider(ctl, { label: 'θ', min: 0.05, max: 3.09, step: 0.01, value: s.th, onInput: x => { s.th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ψ', min: 0, max: 6.28, step: 0.01, value: s.ps, onInput: x => { s.ps = x; view.redraw(); } });
'''))

W.append(dict(file='1-4-sphaerisch-flaechen.html', title='Sphärische Koordinatenfläche',
  sub='r = konst. ist eine Kugel um O (daher der Name), θ = konst. ein Kegel um die z-Achse, ψ = konst. eine Halbebene durch Oz.',
  hint='Ziehen zum Drehen.', js=r'''
  const s = { r: 2, th: 0.8, ps: 1.1 }; let keep = 'r';
  const view = MW.View3D(cv, { extent: 3 }, v => {
    const C = v.C, er = [Math.sin(s.th) * Math.cos(s.ps), Math.sin(s.th) * Math.sin(s.ps), Math.cos(s.th)], M = V.mul(er, s.r);
    v.axes(3);
    if (keep === 'r') {
      for (let k = 1; k < 6; k++) { const th = k * Math.PI / 6; v.poly(v.circlePts([0, 0, s.r * Math.cos(th)], [0, 0, 1], s.r * Math.sin(th), 0, 2 * Math.PI, 72, [1, 0, 0]), C.c2, 1); }
      for (let k = 0; k < 6; k++) { const p = k * Math.PI / 6; v.poly(v.circlePts([0, 0, 0], [-Math.sin(p), Math.cos(p), 0], s.r, 0, 2 * Math.PI, 90, [0, 0, 1]), C.c2, 1); }
    } else if (keep === 'th') {
      const L = 2.8;
      for (let k = 0; k < 12; k++) { const p = k * Math.PI / 6; v.line([0, 0, 0], V.mul([Math.sin(s.th) * Math.cos(p), Math.sin(s.th) * Math.sin(p), Math.cos(s.th)], L), C.c2, 1); }
      v.poly(v.circlePts([0, 0, L * Math.cos(s.th)], [0, 0, 1], L * Math.sin(s.th), 0, 2 * Math.PI, 72, [1, 0, 0]), C.c2, 1.5);
    } else {
      v.poly([[0, 0, -2.6], [2.8 * Math.cos(s.ps), 2.8 * Math.sin(s.ps), -2.6], [2.8 * Math.cos(s.ps), 2.8 * Math.sin(s.ps), 2.6], [0, 0, 2.6]], C.c2, 1.5, null, true, C.fill);
    }
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    const head = { r: 'r = ' + fmt(s.r) + ': Kugel um O', th: 'θ = ' + fmt(s.th) + ': Kegel um die z-Achse mit Spitze in O', ps: 'ψ = ' + fmt(s.ps) + ': Halbebene durch die z-Achse' }[keep];
    MW.info(infoEl, head, [], keep === 'th' ? 'Sonderfall θ = π/2: Der Kegel wird zur xy-Ebene (z = 0).' : '');
  });
  MW.select(ctl, 'Fest halten:', [['r', 'r = konst.'], ['th', 'θ = konst.'], ['ps', 'ψ = konst.']], k => { keep = k; view.redraw(); });
  MW.slider(ctl, { label: 'r', min: 0.6, max: 2.6, step: 0.05, value: s.r, onInput: x => { s.r = x; view.redraw(); } });
  MW.slider(ctl, { label: 'θ', min: 0.1, max: 3.04, step: 0.01, value: s.th, onInput: x => { s.th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ψ', min: 0, max: 6.28, step: 0.01, value: s.ps, onInput: x => { s.ps = x; view.redraw(); } });
'''))

W.append(dict(file='1-4-kreisel.html', title='Achsenspitze eines Kreisels (Buchbeispiel Fig. 1.13)',
  sub='r = R, θ = π/6 + θ₀ sin(ω₁t), ψ = ω₂t. Die Bahn ist eine Sinuslinie auf der Kugel zwischen θ = π/6 ± θ₀. Sie schliesst sich nach einer Umdrehung, wenn n = ω₁/ω₂ ganzzahlig ist.',
  hint='n wählen und abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'Bahnkurve der Spitze A'), ('--line', 'Parallelkreise π/6 ± θ₀')], js=r'''
  const R = 2, th0 = 0.25; let n = 4, psi = 2 * Math.PI;
  const A = p => { const th = Math.PI / 6 + th0 * Math.sin(n * p); return [R * Math.sin(th) * Math.cos(p), R * Math.sin(th) * Math.sin(p), R * Math.cos(th)]; };
  const view = MW.View3D(cv, { extent: 2.2, yaw: 30, pitch: 30, center: [0, 0, 1] }, v => {
    const C = v.C; v.axes(2.4);
    for (const th of [Math.PI / 6 - th0, Math.PI / 6 + th0]) v.poly(v.circlePts([0, 0, R * Math.cos(th)], [0, 0, 1], R * Math.sin(th), 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [4, 3]);
    const pts = []; const N = Math.max(60, Math.round(psi * 60)); for (let i = 0; i <= N; i++) pts.push(A(psi * i / N));
    v.poly(pts, C.c1, 2);
    const P = A(psi); v.line([0, 0, 0], P, C.fg, 2); v.dot(P, C.fg, 6); v.text(P, 'A', C.fg, 8, -6);
    MW.info(infoEl, 'Umdrehungen: ' + fmt(psi / (2 * Math.PI), 2), [['n = ω₁/ω₂', fmt(n, 2)], ['θ', fmt(Math.PI / 6 + th0 * Math.sin(n * psi))]],
      Number.isInteger(n) ? 'n ganzzahlig: Die Bahn wiederholt sich nach jeder ganzen Umdrehung.' : 'n rational, aber nicht ganz: Die Bahn wiederholt sich erst nach mehreren Umdrehungen. Bei irrationalem n schliesst sie sich nie.');
  });
  MW.select(ctl, 'n = ω₁/ω₂:', [['4', '4'], ['3', '3'], ['2.5', '2,5'], ['1.5', '1,5']], x => { n = +x; psi = 0; view.redraw(); });
  MW.player(ctl, { t0: 0, t1: 4 * Math.PI, duration: 10, loop: false, value: 2 * Math.PI, label: 'ψ', onTime: x => { psi = x; view.redraw(); } });
'''))

W.append(dict(file='1-4-zp25-kugel.html', title='ZP1 2025 A1: Punkt auf der Kugel',
  sub='r = R, θ = (2π/3)(1 − cos μt), ψ = μt, mit R = μ = 1. Wann ist z = R/2? Wie weit ist M von der Ebene x = 0 entfernt?',
  hint='t ziehen oder abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'Bahnkurve'), ('--c2', 'Ebene z = R/2')], js=r'''
  let t = Math.PI / 3;
  const M = tt => { const th = 2 * Math.PI / 3 * (1 - Math.cos(tt)), ps = tt; return [Math.sin(th) * Math.cos(ps), Math.sin(th) * Math.sin(ps), Math.cos(th)]; };
  const view = MW.View3D(cv, { extent: 1.5, yaw: 30, pitch: 22 }, v => {
    const C = v.C; v.axes(1.4);
    v.poly(v.circlePts([0, 0, 0], [0, 0, 1], 1, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [3, 3]);
    v.poly(v.circlePts([0, 0, 0], [0, 1, 0], 1, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [3, 3]);
    v.poly(v.circlePts([0, 0, 0.5], [0, 0, 1], Math.sqrt(3) / 2, 0, 2 * Math.PI, 72, [1, 0, 0]), C.c2, 1.5, null, true, C.fill);
    const pts = []; for (let i = 0; i <= 150; i++) pts.push(M(t * i / 150)); v.poly(pts, C.c1, 2.5);
    const P = M(t); v.dot(P, C.fg, 6); v.text(P, 'M', C.fg, 8, -6);
    const th = 2 * Math.PI / 3 * (1 - Math.cos(t));
    MW.info(infoEl, 't = ' + fmt(t) + (Math.abs(t - Math.PI / 3) < 0.01 ? ' = π/3: erstmals z = R/2' : Math.abs(t - Math.PI / 2) < 0.01 ? ' = π/2: Abstand zu x = 0 ist |x| = 0' : ''),
      [['θ', fmt(th)], ['z = R cos θ', fmt(P[2])], ['|x| (Abstand zur Ebene x = 0)', fmt(Math.abs(P[0]))], ['|OM|', fmt(V.norm(P))]],
      'z = R/2 ⇔ θ = π/3 ⇔ cos μt = 1/2 ⇔ t = π/(3μ). M bleibt immer auf der Kugel |OM| = R, erreicht also nie P = (R, R, R) mit |OP| = √3 R.');
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 10, value: Math.PI / 3, onTime: x => { t = x; view.redraw(); }, label: 'μt' });
  MW.button(ctl, 't = π/3', () => { t = Math.PI / 3; view.redraw(); });
  MW.button(ctl, 't = π/2', () => { t = Math.PI / 2; view.redraw(); });
'''))

# ---------------------------------------------------------------- 1.5
W.append(dict(file='1-5-zerlegung-basis.html', title='Zerlegung eines Vektors in einer Basis',
  sub='r = r₁ b₁ + r₂ b₂ nach der Parallelogrammregel. Die Basisvektoren müssen weder senkrecht noch Einheitsvektoren sein (hier eben gezeichnet).',
  hint='Ziehe die Spitzen von b₁, b₂ und r.', legend=[('--c1', 'r'), ('--c2', 'b₁, r₁ b₁'), ('--c3', 'b₂, r₂ b₂')], js=r'''
  let b1 = [1.2, 0], b2 = [0.5, 1], r = [2.6, 1.8];
  const view = MW.View2D(cv, { xmin: -1, xmax: 4.2, ymin: -0.6, ymax: 2.8 }, v => {
    const C = v.C; v.grid(1, true, false);
    const det = b1[0] * b2[1] - b1[1] * b2[0];
    if (Math.abs(det) < 1e-3) { MW.info(infoEl, 'b₁ und b₂ sind parallel: keine Basis', [], 'Basisvektoren dürfen nicht in einer Linie (in 3D: nicht in einer Ebene) liegen.', true); }
    const r1 = (r[0] * b2[1] - r[1] * b2[0]) / det, r2 = (b1[0] * r[1] - b1[1] * r[0]) / det;
    const A = V.mul(b1, r1);
    if (Math.abs(det) >= 1e-3) { v.arrow([0, 0], A, C.c2, 1.8); v.arrow(A, V.mul(b2, r2), C.c3, 1.8); v.line(V.mul(b2, r2), r, C.line, 1, [4, 4]); v.line([0, 0], V.mul(b2, r2), C.line, 1, [4, 4]); }
    v.arrow([0, 0], b1, C.c2, 3.5); v.text(b1, 'b₁', C.c2, 4, 16);
    v.arrow([0, 0], b2, C.c3, 3.5); v.text(b2, 'b₂', C.c3, -18, -4);
    v.arrow([0, 0], r, C.c1, 3); v.text(r, 'r', C.c1, 6, -6);
    if (Math.abs(det) >= 1e-3) MW.info(infoEl, 'r = ' + fmt(r1) + ' b₁ + ' + fmt(r2) + ' b₂', [['skalare Komponenten', 'r₁ = ' + fmt(r1) + ', r₂ = ' + fmt(r2)], ['vektorielle Komponenten', 'r₁b₁, r₂b₂']],
      'Die skalaren Komponenten hängen von der Basis ab. Der Pfeil r selbst bleibt derselbe.');
  });
  const snap = p => [Math.round(p[0] * 10) / 10, Math.round(p[1] * 10) / 10];
  view.handle(() => b1, p => { b1 = snap(p); }); view.handle(() => b2, p => { b2 = snap(p); }); view.handle(() => r, p => { r = snap(p); });
'''))

W.append(dict(file='1-5-basis-kartesisch.html', title='Kartesische Basis: konstante Einheitsvektoren',
  sub='r = x e<sub>x</sub> + y e<sub>y</sub> + z e<sub>z</sub>. Egal wo M ist: e<sub>x</sub>, e<sub>y</sub>, e<sub>z</sub> zeigen immer gleich.',
  hint='Abspielen: M bewegt sich, die Basis bleibt gleich. Ziehen dreht die Ansicht.', legend=[('--c1', 'e_x'), ('--c3', 'e_y'), ('--c2', 'e_z'), ('--fg', 'r')], js=r'''
  let t = 0.15;
  const M = tt => [2 * Math.cos(2 * Math.PI * tt), 1.6 * Math.sin(2 * Math.PI * tt), 1 + 0.6 * Math.sin(4 * Math.PI * tt)];
  const view = MW.View3D(cv, { extent: 3 }, v => {
    const C = v.C, P = M(t); v.floor(3); v.axes(3);
    const pts = []; for (let i = 0; i <= 100; i++) pts.push(M(i / 100)); v.poly(pts, C.line, 1, [4, 4]);
    v.line([0, 0, 0], [P[0], 0, 0], C.c1, 1.5, [3, 3]); v.line([P[0], 0, 0], [P[0], P[1], 0], C.c3, 1.5, [3, 3]); v.line([P[0], P[1], 0], P, C.c2, 1.5, [3, 3]);
    v.arrow([0, 0, 0], P, C.fg, 2.5); v.text(V.mul(P, 0.5), 'r', C.fg, 6, -4);
    v.arrow(P, [0.8, 0, 0], C.c1, 3); v.arrow(P, [0, 0.8, 0], C.c3, 3); v.arrow(P, [0, 0, 0.8], C.c2, 3);
    v.dot(P, C.fg, 5); v.text(P, 'M', C.fg, -16, 14);
    MW.info(infoEl, 'r = ' + fmt(P[0]) + ' e_x + ' + fmt(P[1]) + ' e_y + ' + fmt(P[2]) + ' e_z', [],
      'Die kartesischen Einheitsvektoren haben festen Betrag und feste Richtung. Darum gilt beim Ableiten ė_x = ė_y = ė_z = 0.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 8, value: 0.15, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='1-5-basis-zylindrisch.html', title='Zylindrische Basis: e<sub>ρ</sub> und e<sub>φ</sub> drehen mit φ',
  sub='e<sub>ρ</sub> radial, e<sub>φ</sub> tangential zum Kreis, e<sub>z</sub> axial. r = ρ e<sub>ρ</sub> + z e<sub>z</sub>: φ steht nicht in der Formel, steckt aber in der Richtung von e<sub>ρ</sub>.',
  hint='φ ändern: e_ρ und e_φ drehen mit, e_z nicht. Ziehen dreht die Ansicht.', legend=[('--c1', 'e_ρ'), ('--c3', 'e_φ'), ('--c2', 'e_z'), ('--fg', 'r = ρe_ρ + ze_z')], js=r'''
  const s = { rho: 2, phi: 1.1, z: 1.2 };
  const view = MW.View3D(cv, { extent: 2.3, pitch: 26 }, v => {
    const C = v.C, c = Math.cos(s.phi), sn = Math.sin(s.phi), er = [c, sn, 0], ep = [-sn, c, 0], M = [s.rho * c, s.rho * sn, s.z];
    v.floor(3); v.axes(3);
    v.poly(v.circlePts([0, 0, s.z], [0, 0, 1], s.rho, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [4, 4]);
    v.line([0, 0, 0], V.mul(er, s.rho), C.c1, 1.5, [3, 3]); v.line(V.mul(er, s.rho), M, C.c2, 1.5, [3, 3]);
    v.arrow([0, 0, 0], M, C.fg, 2.5);
    v.arrow(M, V.mul(er, 0.9), C.c1, 3); v.text(V.add(M, V.mul(er, 0.9)), 'e_ρ', C.c1, 4, 4, 12);
    v.arrow(M, V.mul(ep, 0.9), C.c3, 3); v.text(V.add(M, V.mul(ep, 0.9)), 'e_φ', C.c3, 4, 4, 12);
    v.arrow(M, [0, 0, 0.9], C.c2, 3); v.text(V.add(M, [0, 0, 0.9]), 'e_z', C.c2, 4, 4, 12);
    v.dot(M, C.fg, 5); v.text(M, 'M', C.fg, -16, 16);
    MW.info(infoEl, 'r = ' + fmt(s.rho) + ' e_ρ + ' + fmt(s.z) + ' e_z',
      [['e_ρ = (cos φ, sin φ, 0)', fv(er)], ['e_φ = (−sin φ, cos φ, 0)', fv(ep)], ['e_z', '(0, 0, 1)']],
      'e_ρ und e_φ hängen vom Winkel φ ab und sind darum keine konstanten Vektoren. Das erzeugt in Kapitel 2 den Zusatzterm ρφ̇ e_φ in der Geschwindigkeit.');
  });
  MW.slider(ctl, { label: 'φ', min: 0, max: 6.28, step: 0.01, value: s.phi, onInput: x => { s.phi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ρ', min: 0.5, max: 2.6, step: 0.05, value: s.rho, onInput: x => { s.rho = x; view.redraw(); } });
  MW.slider(ctl, { label: 'z', min: -1, max: 2.2, step: 0.05, value: s.z, onInput: x => { s.z = x; view.redraw(); } });
'''))

W.append(dict(file='1-5-basis-sphaerisch.html', title='Sphärische Basis: alle drei Vektoren drehen',
  sub='e<sub>r</sub> radial (von O nach M), e<sub>θ</sub> entlang des Meridians (θ wächst), e<sub>ψ</sub> entlang des Parallelkreises. r = r e<sub>r</sub>.',
  hint='θ und ψ ändern. Ziehen dreht die Ansicht.', legend=[('--c1', 'e_r'), ('--c4', 'e_θ'), ('--c3', 'e_ψ')], js=r'''
  const s = { r: 2, th: 1.0, ps: 1.1 };
  const view = MW.View3D(cv, { extent: 2.3, pitch: 26 }, v => {
    const C = v.C, st = Math.sin(s.th), ct = Math.cos(s.th), cp = Math.cos(s.ps), sp = Math.sin(s.ps);
    const er = [st * cp, st * sp, ct], et = [ct * cp, ct * sp, -st], eps = [-sp, cp, 0], M = V.mul(er, s.r);
    v.axes(3);
    v.poly(v.circlePts([0, 0, 0], [0, 0, 1], s.r, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1, [3, 3]);
    v.poly(v.circlePts([0, 0, 0], V.cross([0, 0, 1], [cp, sp, 0]), s.r, 0, Math.PI, 90, [0, 0, 1]), C.line, 1, [3, 3]);
    v.arrow([0, 0, 0], M, C.fg, 2.5); v.text(V.mul(M, 0.5), 'r', C.fg, -14, -4, 12);
    v.arrow(M, V.mul(er, 1.1), C.c1, 3); v.text(V.add(M, V.mul(er, 1.1)), 'e_r', C.c1, 4, 4, 12);
    v.arrow(M, V.mul(et, 1.1), C.c4, 3); v.text(V.add(M, V.mul(et, 1.1)), 'e_θ', C.c4, 4, 4, 12);
    v.arrow(M, V.mul(eps, 1.1), C.c3, 3); v.text(V.add(M, V.mul(eps, 1.1)), 'e_ψ', C.c3, 4, 4, 12);
    v.dot(M, C.fg, 5);
    MW.info(infoEl, 'r = ' + fmt(s.r) + ' e_r', [['e_r', fv(er)], ['e_θ', fv(et)], ['e_ψ', fv(eps)]],
      'Nur eine skalare Komponente (r). θ und ψ stecken in der Richtung von e_r (ZP1 2024 A1.4 b, ZP1 2025 A1.4 d).');
  });
  MW.slider(ctl, { label: 'θ', min: 0.05, max: 3.09, step: 0.01, value: s.th, onInput: x => { s.th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ψ', min: 0, max: 6.28, step: 0.01, value: s.ps, onInput: x => { s.ps = x; view.redraw(); } });
  MW.slider(ctl, { label: 'r', min: 0.6, max: 2.6, step: 0.05, value: s.r, onInput: x => { s.r = x; view.redraw(); } });
'''))

W.append(dict(file='1-5-nur-betrag.html', title='Nur der Betrag von r ändert sich: geradlinige Bewegung',
  sub='Richtung von r konstant, |r| veränderlich: Die Bahnkurve liegt auf einer Geraden durch den Ursprung O.',
  hint='Abspielen.', legend=[('--c1', 'r(t)'), ('--line', 'Bahnkurve')], js=r'''
  let t = 0.15; const e = V.unit([2, 1]);
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 3.2, ymin: -1.8, ymax: 1.8 }, v => {
    const C = v.C; v.grid(1);
    const L = 2.8 * Math.sin(2 * Math.PI * t);
    v.line(V.mul(e, -3.2), V.mul(e, 3.2), C.line, 1.5, [5, 4]);
    v.arrow([0, 0], V.mul(e, L), C.c1, 3); v.dot(V.mul(e, L), C.fg, 6); v.text(V.mul(e, L), 'M', C.fg, 6, -8);
    MW.info(infoEl, '|r| = ' + fmt(Math.abs(L)), [['Richtung', 'konstant (±)']], 'Die Spitze von r läuft nur entlang einer Geraden durch O.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 4, value: 0.15, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='1-5-nur-richtung.html', title='Nur die Richtung von r ändert sich: Bahn auf einer Kugel',
  sub='|r| konstant, Richtung veränderlich: Die Bahnkurve liegt auf einer Kugel |r| = konst. um O.',
  hint='Abspielen. Ziehen dreht die Ansicht.', legend=[('--c1', 'r(t)'), ('--c3', 'Bahnkurve')], js=r'''
  let t = 0.2; const R = 2;
  const M = tt => { const th = 1.1 + 0.5 * Math.sin(6 * Math.PI * tt), ps = 2 * Math.PI * tt; return [R * Math.sin(th) * Math.cos(ps), R * Math.sin(th) * Math.sin(ps), R * Math.cos(th)]; };
  const view = MW.View3D(cv, { extent: 2.3 }, v => {
    const C = v.C; v.axes(2.4);
    for (let k = 1; k < 6; k++) { const th = k * Math.PI / 6; v.poly(v.circlePts([0, 0, R * Math.cos(th)], [0, 0, 1], R * Math.sin(th), 0, 2 * Math.PI, 72, [1, 0, 0]), C.line, 1); }
    const pts = []; for (let i = 0; i <= 200; i++) pts.push(M(t * i / 200)); v.poly(pts, C.c3, 2.5);
    const P = M(t); v.arrow([0, 0, 0], P, C.c1, 3); v.dot(P, C.fg, 6); v.text(P, 'M', C.fg, 8, -6);
    MW.info(infoEl, '|r| = ' + fmt(V.norm(P)) + ' (konstant)', [], 'Die Spitze von r kann sich nur auf der Kugelfläche bewegen.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 8, value: 0.2, onTime: x => { t = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    files = build('kap1', W)
    print(len(files), 'Widgets:', ', '.join(files))
