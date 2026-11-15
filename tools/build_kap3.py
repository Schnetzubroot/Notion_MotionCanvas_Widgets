"""Widgets zu Kapitel 3.1–3.3 (Woche 3): Satz der projizierten Geschwindigkeiten, Translation, Rotation."""
from template import build

W = []

ROT = r'''
  // Drehung von p um die Achse durch A mit Richtung k (Einheitsvektor) um den Winkel th (Rodrigues)
  const rot = (p, A, k, th) => { const q = V.sub(p, A), c = Math.cos(th), s = Math.sin(th);
    return V.add(A, V.add(V.add(V.mul(q, c), V.mul(V.cross(k, q), s)), V.mul(k, V.dot(k, q) * (1 - c)))); };
'''

# ---------------------------------------------------------------- 3.1
W.append(dict(file='3-1-spg.html', title='Satz der projizierten Geschwindigkeiten',
  sub='Bei einem starren Körper haben die Geschwindigkeiten zweier Punkte M und N gleiche Projektionen auf die Verbindungsgerade MN: v<sub>M</sub> · MN = v<sub>N</sub> · MN. Sonst würde sich der Abstand MN ändern.',
  hint='Pfeilspitzen und Punkte ziehen.', legend=[('--c1', 'v_M'), ('--c2', 'v_N'), ('--c3', "Projektionen v'_M, v'_N")], js=r'''
  let M = [-1.4, -0.3], N = [1.3, 0.5], vM = [0.7, 1.2], vN = [1.1, -0.7];
  const view = MW.View2D(cv, { xmin: -3, xmax: 3, ymin: -1.8, ymax: 2.2 }, v => {
    const C = v.C, e = V.unit(V.sub(N, M)), n = [-e[1], e[0]];
    const cap = []; for (let i = 0; i <= 20; i++) { const a = Math.PI / 2 + Math.PI * i / 20; cap.push(V.add(M, V.add(V.mul(e, 0.45 * Math.cos(a)), V.mul(n, 0.45 * Math.sin(a))))); }
    for (let i = 0; i <= 20; i++) { const a = -Math.PI / 2 + Math.PI * i / 20; cap.push(V.add(N, V.add(V.mul(e, 0.45 * Math.cos(a)), V.mul(n, 0.45 * Math.sin(a))))); }
    v.poly(cap, C.line, 1.5, null, true, C.fill); v.text(cap[30], 'K', C.muted, 6, 14, 13, false);
    v.line(V.sub(M, V.mul(e, 1.2)), V.add(N, V.mul(e, 1.2)), C.muted, 1, [6, 4]);
    const pM = V.dot(vM, e), pN = V.dot(vN, e);
    v.line(V.add(M, vM), V.add(M, V.mul(e, pM)), C.line, 1, [3, 3]); v.line(V.add(N, vN), V.add(N, V.mul(e, pN)), C.line, 1, [3, 3]);
    v.arrow(M, V.mul(e, pM), C.c3, 4); v.arrow(N, V.mul(e, pN), C.c3, 4);
    v.arrow(M, vM, C.c1, 2.5); v.arrow(N, vN, C.c2, 2.5);
    v.dot(M, C.fg, 5); v.dot(N, C.fg, 5); v.text(M, 'M', C.fg, -16, 16); v.text(N, 'N', C.fg, 6, 16);
    v.text(V.add(M, vM), 'v_M', C.c1, 4, -4); v.text(V.add(N, vN), 'v_N', C.c2, 4, -4);
    const rate = pN - pM, ok = Math.abs(rate) < 0.02;
    MW.info(infoEl, ok ? 'Satz erfüllt: Der Abstand MN bleibt momentan gleich.' : (rate > 0 ? 'Verletzt: MN wird länger.' : 'Verletzt: MN wird kürzer.') + ' So kann sich kein starrer Körper bewegen.',
      [["v'_M = v_M · e_MN", fmt(pM)], ["v'_N = v_N · e_MN", fmt(pN)], ['d|MN|/dt = v\'_N − v\'_M', fmt(rate)]],
      'Die Komponenten senkrecht zu MN dürfen verschieden sein: Sie drehen die Strecke MN, ändern aber ihre Länge nicht.', !ok);
  });
  view.handle(() => V.add(M, vM), p => { vM = V.sub(p, M); }); view.handle(() => V.add(N, vN), p => { vN = V.sub(p, N); });
  view.handle(() => M, p => { M = p; }); view.handle(() => N, p => { N = p; });
  MW.button(ctl, 'v_N korrigieren (Satz erfüllen)', () => { const e = V.unit(V.sub(N, M)); vN = V.add(vN, V.mul(e, V.dot(vM, e) - V.dot(vN, e))); view.redraw(); });
'''))

W.append(dict(file='3-1-leiter.html', title='Beispiel aus dem Buch: Stab AB zwischen zwei Führungen (Fig. 3.3)',
  sub='A gleitet auf der x-Achse mit v<sub>A</sub> = v e<sub>x</sub>, B auf der y-Achse. Der Satz der projizierten Geschwindigkeiten liefert v<sub>B</sub> = v cot φ e<sub>y</sub>, ganz ohne Ableiten.',
  hint='φ ändern.', legend=[('--c1', 'v_A'), ('--c2', 'v_B'), ('--c3', 'gleiche Projektionen auf AB')], js=r'''
  const L = 2.4; let phi = 40;
  const view = MW.View2D(cv, { xmin: -2.8, xmax: 1.4, ymin: -0.6, ymax: 2.9 }, v => {
    const C = v.C, f = phi * MW.deg, A = [-L * Math.cos(f), 0], B = [0, L * Math.sin(f)], e = [Math.cos(f), Math.sin(f)];
    v.arrow([-2.7, 0], [3.9, 0], C.muted, 1.2, 8); v.arrow([0, -0.5], [0, 3.3], C.muted, 1.2, 8);
    v.text([1.2, 0], 'x', C.muted, -4, -8, 13, false); v.text([0, 2.8], 'y', C.muted, 8, 4, 13, false); v.text([0, 0], 'O', C.muted, 6, 16, 12, false);
    v.line(A, B, C.fg, 6);
    const vA = [1, 0], vB = [0, 1 / Math.tan(f)], p = Math.cos(f);
    v.line(V.add(A, vA), V.add(A, V.mul(e, p)), C.line, 1, [3, 3]); v.line(V.add(B, vB), V.add(B, V.mul(e, p)), C.line, 1, [3, 3]);
    v.arrow(A, V.mul(e, p), C.c3, 4.5); v.arrow(B, V.mul(e, p), C.c3, 4.5);
    v.arrow(A, vA, C.c1, 2.5); v.arrow(B, vB, C.c2, 2.5);
    v.arc(A, 0.45, 0, f, C.muted, 1.2); v.text(A, 'φ', C.muted, 34, -6, 13, false);
    v.dot(A, C.fg, 5); v.dot(B, C.fg, 5); v.text(A, 'A', C.fg, -6, 18); v.text(B, 'B', C.fg, -18, 0);
    MW.info(infoEl, 'v_B = v cot φ = ' + fmt(1 / Math.tan(f)) + ' v', [["v'_A = v cos φ", fmt(Math.cos(f)) + ' v'], ["v'_B = v_B sin φ", fmt(Math.sin(f) / Math.tan(f)) + ' v'], ['φ', fmt(phi, 0) + '°']],
      'Für φ → 0 (Stab liegt auf der x-Achse) würde v_B unendlich gross. Darum muss dort v = 0 sein (Buch S. 39).');
  });
  MW.slider(ctl, { label: 'φ', min: 8, max: 85, step: 1, value: phi, unit: '°', onInput: x => { phi = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.2
W.append(dict(file='3-2-translation.html', title='Translation: kongruente Bahnkurven, gleiche Geschwindigkeiten',
  sub='Bei einer Translation bleibt jeder Verbindungsvektor a = MN in Betrag und Richtung konstant. Alle Punkte haben denselben Translationsvektor R und dieselbe Geschwindigkeit: v<sub>M</sub> = v<sub>N</sub>, ω = 0.',
  hint='Abspielen, Bahn wählen.', legend=[('--c2', 'Bahnkurven'), ('--c1', 'v (überall gleich)'), ('--c4', 'Translationsvektor R')], js=r'''
  const shape = [[0, 0], [0.9, -0.2], [1.2, 0.35], [0.6, 0.7], [-0.1, 0.5]], pts = [[0, 0], [1.2, 0.35], [0.6, 0.7]], names = ['M', 'N', 'P'];
  const paths = {
    gerade: { r: t => [-2.6 + 3.2 * t, -1 + 1.2 * t], d: t => [3.2, 1.2] },
    krumm: { r: t => [-2.6 + 3.4 * t, -1 + 3 * t * (1 - t) * 1.6], d: t => [3.4, 4.8 * (1 - 2 * t)] },
    kreis: { r: t => [-0.6 + 1.2 * Math.cos(Math.PI - 2 * Math.PI * t), -0.4 + 1.2 * Math.sin(Math.PI - 2 * Math.PI * t)], d: t => [2.4 * Math.PI * Math.sin(Math.PI - 2 * Math.PI * t), -2.4 * Math.PI * Math.cos(Math.PI - 2 * Math.PI * t)] },
  };
  let kind = 'krumm', t = 0.55;
  const view = MW.View2D(cv, { xmin: -3, xmax: 2.6, ymin: -1.7, ymax: 2.1 }, v => {
    const C = v.C, P = paths[kind], o = P.r(t), o0 = P.r(0), vel = V.mul(P.d(t), 0.22);
    pts.forEach(q => { const tr = []; for (let i = 0; i <= 120; i++) tr.push(V.add(P.r(i / 120), q)); v.poly(tr, C.c2, 1.3, [5, 4]); });
    v.poly(shape.map(q => V.add(o0, q)), C.line, 1.2, [3, 3], true);
    v.poly(shape.map(q => V.add(o, q)), C.fg, 2, null, true, C.fill);
    pts.forEach((q, i) => { const a = V.add(o0, q), b = V.add(o, q); v.arrow(a, V.sub(b, a), C.c4, 1.6, 8); v.arrow(b, vel, C.c1, 2.8); v.dot(b, C.fg, 4); v.text(b, names[i], C.fg, -14, -6, 13); });
    MW.info(infoEl, 'Translation: R_M = R_N = R_P, v_M = v_N = v_P', [['R', fv(V.sub(o, o0))], ['v', fv(V.mul(P.d(t), 1))], ['ω', '0']],
      kind === 'kreis' ? 'Kreisförmige Translation: Alle Punkte laufen auf gleich grossen Kreisen, der Körper dreht sich dabei nicht (wie eine Gondel am Riesenrad).' :
      kind === 'krumm' ? 'Krummlinige Translation: Die Bahnen sind gekrümmt, aber kongruent (verschobene Kopien). v ändert sich mit der Zeit, ist aber zu jedem Zeitpunkt überall gleich.' :
      'Geradlinige Translation: Alle Bahnen sind parallele Geraden.');
  });
  MW.select(ctl, 'Bahn', [['krumm', 'krummlinig'], ['gerade', 'geradlinig'], ['kreis', 'kreisförmig']], k => { kind = k; view.redraw(); }).set('krumm');
  MW.player(ctl, { t0: 0, t1: 1, duration: 5, value: t, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='3-2-viergelenk.html', title='Viergelenk: kreisförmige Translation (Fig. 3.5)',
  sub='OA und O\'A\' sind gleich lang und drehen um O bzw. O\'. Der Koppelstab AA\' bleibt parallel zu OO\': kreisförmige Translation, alle seine Punkte haben dieselbe Geschwindigkeit. Mach O\'A\' länger und vergleiche.',
  hint='Abspielen, Länge von O\'A\' ändern.', legend=[('--c1', 'Geschwindigkeiten auf AA\''), ('--c2', 'Bahn der Mitte von AA\'')], js=r'''
  const d = 2.4, r1 = 1; let r2 = 1, phi = 1.0;
  const O = [0, 0], O2 = [d, 0];
  function pose(f) {
    const A = [r1 * Math.cos(f), r1 * Math.sin(f)], q = V.sub(O2, A), L = V.norm(q);
    if (L > d + r2 || L < Math.abs(d - r2)) return null;
    const a = (d * d - r2 * r2 + L * L) / (2 * L), h = Math.sqrt(Math.max(0, d * d - a * a)), u = V.unit(q), n = [-u[1], u[0]];
    const c1 = V.add(A, V.add(V.mul(u, a), V.mul(n, h))), c2 = V.add(A, V.sub(V.mul(u, a), V.mul(n, h))), ref = V.add(A, [d, 0]);
    return { A, A2: V.norm(V.sub(c1, ref)) < V.norm(V.sub(c2, ref)) ? c1 : c2 };
  }
  const view = MW.View2D(cv, { xmin: -1.6, xmax: 4.2, ymin: -1.7, ymax: 1.9 }, v => {
    const C = v.C;
    v.circle(O, r1, C.grid, 1, [4, 4]); v.circle(O2, r2, C.grid, 1, [4, 4]);
    const tr = []; for (let i = 0; i <= 180; i++) { const s = pose(2 * Math.PI * i / 180); if (s) tr.push(V.mul(V.add(s.A, s.A2), 0.5)); else if (tr.length) { v.poly(tr, C.c2, 1.4, [5, 4]); tr.length = 0; } }
    v.poly(tr, C.c2, 1.4, [5, 4]);
    const s = pose(phi); v.dot(O, C.fg, 5); v.dot(O2, C.fg, 5); v.text(O, 'O', C.fg, -16, 16); v.text(O2, "O'", C.fg, 6, 16);
    if (!s) { MW.info(infoEl, 'Diese Lage ist mit diesen Stablängen nicht möglich.', [], 'Mit O\'A\' ≠ OA kann die Kurbel OA nicht ganz umlaufen.', true); return; }
    const { A, A2 } = s, vA = [-r1 * Math.sin(phi), r1 * Math.cos(phi)];
    const p2 = V.sub(A2, O2), t2 = [-p2[1], p2[0]], e = V.unit(V.sub(A2, A));
    const k = V.dot(vA, e) / V.dot(t2, e), vA2 = V.mul(t2, k), Mid = V.mul(V.add(A, A2), 0.5), vMid = V.mul(V.add(vA, vA2), 0.5);
    v.line(O, A, C.fg, 4); v.line(O2, A2, C.fg, 4); v.line(A, A2, C.fg, 6);
    [[A, vA], [Mid, vMid], [A2, vA2]].forEach(([p, w]) => v.arrow(p, V.mul(w, 0.8), C.c1, 2.6));
    [A, A2].forEach(p => v.dot(p, C.bg, 4.5, true)); v.text(A, 'A', C.fg, -14, -8); v.text(A2, "A'", C.fg, 6, -8); v.dot(Mid, C.fg, 3);
    const ang = Math.atan2(A2[1] - A[1], A2[0] - A[0]) / MW.deg, tr2 = Math.abs(r2 - r1) < 1e-9;
    MW.info(infoEl, tr2 ? "Kreisförmige Translation: AA' bleibt horizontal." : "Keine Translation: AA' dreht sich.", [['|v_A|', fmt(V.norm(vA))], ["|v_A'|", fmt(V.norm(vA2))], ["Winkel von AA' zu OO'", fmt(ang, 1) + '°']],
      tr2 ? "Alle Punkte von AA' laufen auf gleich grossen Kreisen, deren Mittelpunkte auf OO' liegen (Buch S. 41)." : "Die Geschwindigkeiten auf AA' sind verschieden, die Bahn der Mitte ist kein Kreis mehr.", !tr2);
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 6, value: phi, label: 'φ', fmt: x => fmt(x / MW.deg, 0) + '°', onTime: x => { phi = x; view.redraw(); } });
  MW.slider(ctl, { label: "O'A'", min: 0.8, max: 1.3, step: 0.05, value: 1, onInput: x => { r2 = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.3
W.append(dict(file='3-3-rotation-3d.html', title='Rotation um eine feste Achse μ', tall=True,
  sub='Zwei Punkte A, B bleiben in Ruhe, damit die ganze Achse μ = AB. Jeder andere Punkt läuft auf einem Kreis senkrecht zu μ mit Mittelpunkt auf μ: v = ω × AM, |v| = ω · Abstand zur Achse.',
  hint='Ziehen zum Drehen der Ansicht.', legend=[('--c5', 'Achse μ, ω'), ('--c1', 'v = ω × AM'), ('--c2', 'Kreisbahn von M'), ('--c4', 'AM')], js=ROT + r'''
  const AX = { z: [0, 0, 1], schraeg: V.unit([1, 1, 2]) };
  let ax = 'schraeg', Phi = 0, lam = 0, w = 1;
  const box = []; [-0.6, 0.6].forEach(x => [-0.4, 0.4].forEach(y => [-0.3, 1.1].forEach(z => box.push([x + 0.9, y + 0.2, z]))));
  const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
  const view = MW.View3D(cv, { extent: 2.2, yaw: 40, pitch: 18, center: [0.3, 0.2, 0.6] }, v => {
    const C = v.C, k = AX[ax], A = [0, 0, 0], B = V.mul(k, 1.6), om = V.mul(k, w);
    v.line(V.mul(k, -1.4), V.mul(k, 2.6), C.c5, 1.5, [8, 3, 2, 3]); v.text(V.mul(k, 2.6), 'μ', C.c5, 6, 0);
    v.arrow(B, V.mul(om, 0.7), C.c5, 3); v.text(V.add(B, V.mul(om, 0.7)), 'ω', C.c5, 6, 0);
    const P = box.map(p => rot(p, A, k, Phi));
    edges.forEach(([i, j]) => v.line(P[i], P[j], C.fg, 1.6));
    P.forEach(p => v.arrow(p, V.mul(V.cross(om, V.sub(p, A)), 0.45), C.c1, 1.6, 7));
    const M = P[7], D = V.mul(k, V.dot(M, k)), Aref = V.mul(k, lam), r = V.norm(V.sub(M, D));
    v.poly(v.circlePts(D, k, r, 0, 2 * Math.PI, 96), C.c2, 1.4, [5, 4]); v.line(D, M, C.line, 1, [3, 3]); v.dot(D, C.muted, 3); v.text(D, 'D', C.muted, -14, 4, 12);
    v.arrow(Aref, V.sub(M, Aref), C.c4, 1.6, 8); v.dot(Aref, C.c4, 4); v.text(Aref, "A'", C.c4, -18, 4, 12);
    const vM = V.cross(om, V.sub(M, Aref)); v.arrow(M, V.mul(vM, 0.45), C.c1, 3.2); v.dot(M, C.fg, 5); v.text(M, 'M', C.fg, 6, -6);
    v.dot(A, C.c5, 5); v.dot(B, C.c5, 5); v.text(A, 'A', C.c5, 6, 14); v.text(B, 'B', C.c5, 8, 10);
    MW.info(infoEl, 'v_M = ω × A\'M, für jeden Punkt A\' auf μ gleich', [['|ω|', fmt(w)], ['Abstand DM zur Achse', fmt(r)], ['|v_M|', fmt(V.norm(vM))], ['ω · DM', fmt(w * r)], ['v_M · ω', fmt(V.dot(vM, om), 3)]],
      'Verschiebe A\' auf der Achse: AM ändert sich, v_M nicht, weil der Anteil von AM parallel zu ω im Kreuzprodukt wegfällt. v_M steht senkrecht auf ω und auf DM.');
  });
  MW.select(ctl, 'Achse', [['schraeg', 'schräg, e_μ ∥ (1, 1, 2)'], ['z', 'z-Achse']], x => { ax = x; view.redraw(); }).set('schraeg');
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 8, value: 0, label: 'Φ', fmt: x => fmt(x / MW.deg, 0) + '°', onTime: x => { Phi = x; view.redraw(); } });
  MW.slider(ctl, { label: "A' auf μ", min: -1.2, max: 2.2, step: 0.05, value: 0, onInput: x => { lam = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω', min: -1.5, max: 1.5, step: 0.1, value: 1, onInput: x => { w = x; view.redraw(); } });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

W.append(dict(file='3-3-welle.html', title='Rotierende Welle: v = R ω (Fig. 3.9)',
  sub='Alle Punkte drehen mit derselben Rotationsschnelligkeit ω. Die Schnelligkeit wächst linear mit dem Abstand zur Achse. Aus der Drehzahl n in U/min: ω = 2π n / 60.',
  hint='Drehzahl ändern.', legend=[('--c1', 'v_i = R_i ω'), ('--c5', 'ω (aus der Ebene)')], js=r'''
  const R = [1, 2, 3, 4]; let n = 600;
  const view = MW.View2D(cv, { xmin: -5.6, xmax: 5.6, ymin: -4.6, ymax: 5 }, v => {
    const C = v.C, w = 2 * Math.PI * n / 60, sc = 1.2 * n / 3000;
    R.slice().reverse().forEach((r, i) => v.circle([0, 0], r, C.line, 1.5, null, i % 2 ? null : C.fill));
    v.line([0, 0], [0, 4.6], C.muted, 1, [6, 3, 2, 3]);
    R.forEach((r, i) => { const p = [0, r], vel = r * 0.01 * w; v.arrow(p, [-r * sc, 0], C.c1, 2.6); v.dot(p, C.fg, 4); v.text(p, 'v' + (i + 1), C.c1, 6, -6, 12); });
    const tip = [-R[3] * sc, R[3]]; v.line([0, 0], V.mul(tip, 1.12), C.c1, 1, [4, 4]);
    v.circle([0, 0], 0.18, C.c5, 2); v.dot([0, 0], C.c5, 2.5); v.text([0, 0], 'ω', C.c5, 10, 16);
    MW.info(infoEl, 'ω = 2π · ' + fmt(n, 0) + ' / 60 = ' + fmt(w) + ' rad/s', R.map((r, i) => ['v' + (i + 1) + ' bei R' + (i + 1) + ' = ' + r + ' cm', fmt(r * 0.01 * w) + ' m/s']),
      'Gleiches ω, doppelter Radius gibt doppelte Schnelligkeit. Die Spitzen liegen auf einer Geraden durch die Achse (gestrichelt): v ist linear in r.');
  });
  MW.slider(ctl, { label: 'n', min: 0, max: 3000, step: 10, value: n, unit: ' U/min', onInput: x => { n = x; view.redraw(); } });
'''))

W.append(dict(file='3-3-rollen.html', title='Rollen ohne Gleiten: momentane Rotation um den Berührungspunkt', tall=True,
  sub='Beim Rollen ist der Berührungspunkt Z momentan in Ruhe. Die Geschwindigkeiten sind dann wie bei einer Rotation um Z verteilt: v = ω × ZM. Beim Gleiten hat der Berührungspunkt eine Geschwindigkeit ≠ 0.',
  hint='Abspielen, Verhältnis ωR / v_C ändern.', legend=[('--c1', 'Geschwindigkeiten'), ('--c2', 'Bahn eines Randpunktes'), ('--c5', 'Punkt in Ruhe')], js=r'''
  const R = 1, vC = 1; let k = 1, t = 1.2;
  const view = MW.View2D(cv, { xmin: -1.4, xmax: 7.4, ymin: -0.9, ymax: 2.8 }, v => {
    const C = v.C, w = k * vC / R, xc = vC * t, Cc = [xc, R], th = -w * t;
    v.line([-1.4, 0], [7.4, 0], C.fg, 2); for (let x = -1.3; x < 7.4; x += 0.3) v.line([x, 0], [x - 0.15, -0.15], C.line, 1);
    const tr = []; for (let i = 0; i <= 200; i++) { const s = 6.2 * i / 200, a = -Math.PI / 2 - w * s; tr.push([vC * s + R * Math.cos(a), R + R * Math.sin(a)]); } v.poly(tr, C.c2, 1.4, [5, 4]);
    v.circle(Cc, R, C.fg, 2, null, C.fill);
    for (let i = 0; i < 4; i++) { const a = th + i * Math.PI / 2; v.line(Cc, V.add(Cc, [R * Math.cos(a), R * Math.sin(a)]), C.line, 1); }
    const mark = V.add(Cc, [R * Math.cos(-Math.PI / 2 + th), R * Math.sin(-Math.PI / 2 + th)]); v.dot(mark, C.c2, 4.5);
    const vel = p => { const q = V.sub(p, Cc); return [vC + w * q[1], -w * q[0]]; }, sc = 0.45;
    for (let i = 0; i <= 4; i++) { const p = [xc, 2 * R * i / 4]; v.arrow(p, V.mul(vel(p), sc), C.c1, 2.2, 8); }
    v.line([xc, 0], [xc + vel([xc, 2 * R])[0] * sc, 2 * R], C.c1, 1, [4, 4]); v.line([xc + vel([xc, 0])[0] * sc, 0], [xc, 0], C.c1, 1);
    [Math.PI / 6, 5 * Math.PI / 6, Math.PI].forEach(a => { const p = V.add(Cc, [R * Math.cos(a), R * Math.sin(a)]); v.arrow(p, V.mul(vel(p), sc), C.c1, 2, 7); v.dot(p, C.fg, 3); });
    const y0 = R - vC / w; if (isFinite(y0) && y0 > -0.8 && y0 < 2.7) { v.dot([xc, y0], C.c5, 5.5); v.text([xc, y0], 'Ruhe', C.c5, 8, 4, 12); }
    v.dot([xc, 0], C.fg, 4); v.text([xc, 0], 'Z', C.fg, -14, 16); v.dot(Cc, C.fg, 4); v.text(Cc, 'C', C.fg, -14, -4);
    const vZ = vC - w * R, roll = Math.abs(vZ) < 1e-9;
    MW.info(infoEl, roll ? 'Rollen: v_Z = 0, momentane Rotation um Z' : 'Gleiten: v_Z = ' + fmt(vZ) + ' v_C ≠ 0', [['v_C', fmt(vC)], ['ω R', fmt(w * R)], ['v oben', fmt(vC + w * R)], ['v_Z (Berührungspunkt)', fmt(vZ)]],
      roll ? 'Die Geschwindigkeit wächst linear mit der Höhe über Z, der oberste Punkt ist doppelt so schnell wie C. Ein Randpunkt läuft auf einer Zykloide und steht in Z kurz still.' :
      'Der momentan ruhende Punkt liegt nicht mehr im Berührungspunkt. Die Bahn eines Randpunktes ist keine gewöhnliche Zykloide mehr.', !roll);
  });
  MW.player(ctl, { t0: 0, t1: 6, duration: 8, value: t, onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ωR / v_C', min: 0, max: 2, step: 0.05, value: 1, onInput: x => { k = x; view.redraw(); } });
'''))

W.append(dict(file='3-3-zp22-eisenbahnrad.html', title='ZP1 2022 A2: Eisenbahnrad mit Spurkranz',
  sub='Das Rad rollt auf dem Laufkreis r<sub>1</sub>, der Spurkranz r<sub>2</sub> > r<sub>1</sub> ragt unter die Schienenkante. ω = (0, 0, −ω). Wähle den ruhenden Punkt und vergleiche die Geschwindigkeitsverteilung auf dem senkrechten Durchmesser.',
  hint='Ruhenden Punkt wählen.', legend=[('--c1', 'v auf dem Durchmesser AB'), ('--c5', 'ruhender Punkt')], js=r'''
  const r1 = 0.8, r2 = 1.0, w = 1; let rest = 'r1';
  const view = MW.View2D(cv, { xmin: -2.4, xmax: 2.6, ymin: -1.5, ymax: 1.5 }, v => {
    const C = v.C, y0 = { r1: -r1, r2: -r2, m: 0 }[rest];
    v.circle([0, 0], r2, C.fg, 2, null, C.fill); v.circle([0, 0], r1, C.line, 1.2, [5, 4]);
    v.line([-2.4, -r1], [2.6, -r1], C.fg, 2.2); v.line([-2.4, -r1 - 0.28], [2.6, -r1 - 0.28], C.line, 1.4);
    const vel = y => w * (y - y0), sc = 0.9;
    for (let i = 0; i <= 10; i++) { const y = -r2 + 2 * r2 * i / 10; v.arrow([0, y], [vel(y) * sc, 0], C.c1, 1.8, 7); }
    v.line([vel(-r2) * sc, -r2], [vel(r2) * sc, r2], C.c1, 1, [4, 4]);
    v.dot([0, r2], C.fg, 4); v.text([0, r2], 'A', C.fg, -16, -4); v.dot([0, -r2], C.fg, 4); v.text([0, -r2], 'B', C.fg, -16, 14);
    v.dot([0, 0], C.fg, 3); v.text([0, 0], 'M', C.fg, -16, -4); v.dot([0, y0], C.c5, 6);
    v.text([-2.3, -r1], 'Schiene (Kontakt bei r₁)', C.muted, 0, -6, 12, false);
    const ok = rest === 'r1';
    MW.info(infoEl, ok ? 'Richtig: Ruhe im Kontaktpunkt des Laufkreises (Option d bzw. f)' : rest === 'r2' ? 'Falsch: Der Spurkranz berührt die Schiene nicht auf der Lauffläche' : 'Falsch: Das wäre eine reine Rotation um M, der Wagen stünde still',
      [['v_A (oben)', fmt(vel(r2)) + ' · ω e_x  →  (r₁ + r₂) ω'], ['v_M', fmt(vel(0)) + ' · ω e_x  →  r₁ ω'], ['v_B (Spurkranz unten)', fmt(vel(-r2)) + ' · ω e_x  →  (r₁ − r₂) ω']],
      'Mit r₁ = 0,8 und r₂ = 1. Der tiefste Punkt B liegt unter dem Kontaktpunkt und läuft darum rückwärts. Kinemate in B: {(r₁ − r₂) ω e_x, −ω e_z}.', !ok);
  });
  MW.select(ctl, 'Ruhender Punkt', [['r1', 'Kontakt Laufkreis (y = −r₁)'], ['r2', 'unterster Punkt B (y = −r₂)'], ['m', 'Mittelpunkt M']], x => { rest = x; view.redraw(); }).set('r1');
'''))

W.append(dict(file='3-3-zp25-kugel.html', title='ZP1 2025 A2: Rotierende Kugel', tall=True,
  sub='A = (0, 0, R) liegt auf der Achse, B = (−R, 0, 0), v<sub>B</sub> = v e<sub>y</sub>, AB ist die kürzeste Verbindung von B zur Achse, ω<sub>z</sub> = −v/(2R). Finde ω<sub>x</sub> und ω<sub>y</sub> mit den Reglern (R = v = 1).',
  hint='Regler verschieben, ziehen zum Drehen.', legend=[('--c5', 'ω und Achse'), ('--c1', 'v_B = ω × AB'), ('--c3', 'Soll: v e_y')], js=r'''
  let wx = 0, wy = 0; const wz = -0.5;
  const A = [0, 0, 1], B = [-1, 0, 0], Cp = [1, 0, 0];
  const view = MW.View3D(cv, { extent: 1.7, yaw: -30, pitch: 18 }, v => {
    const C = v.C, om = [wx, wy, wz];
    v.axes(1.6);
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]].forEach(n => v.poly(v.circlePts([0, 0, 0], n, 1, 0, 2 * Math.PI, 90), C.line, 1));
    if (V.norm(om) > 1e-9) { const e = V.unit(om); v.line(V.sub(A, V.mul(e, 1.4)), V.add(A, V.mul(e, 2.4)), C.c5, 1.4, [8, 3, 2, 3]); v.arrow(A, V.mul(om, 1.2), C.c5, 3); v.text(V.add(A, V.mul(om, 1.2)), 'ω', C.c5, 6, 0); }
    const vB = V.cross(om, V.sub(B, A)), vC = V.cross(om, V.sub(Cp, A));
    v.arrow(B, [0, 1, 0], C.c3, 4); v.arrow(B, vB, C.c1, 2.4); v.arrow(Cp, vC, C.c1, 2.4);
    [[A, 'A'], [B, 'B'], [Cp, 'C']].forEach(([p, n]) => { v.dot(p, C.fg, 4.5); v.text(p, n, C.fg, 6, -6); });
    const err = V.norm(V.sub(vB, [0, 1, 0])), ok = err < 1e-9;
    MW.info(infoEl, ok ? 'Gefunden: ω = (v/2R, 0, −v/2R), Antwort d' : 'v_B stimmt noch nicht mit v e_y überein', [['ω', fv(om)], ['v_B = ω × AB', fv(vB)], ['ω · AB', fmt(V.dot(om, V.sub(B, A)))], ['v_C = ω × AC', fv(vC)]],
      ok ? 'v_C = 0: C liegt auch auf der Achse. Die Achse geht durch A und C, Richtung (1, 0, −1), darum sind a) und b) richtig in A2.3.' :
      'Komponentenweise: ω × (−R, 0, −R) = (−Rω_y, R(ω_x − ω_z), Rω_y) = (0, v, 0). Also ω_y = 0 und ω_x = v/R + ω_z.', !ok);
  });
  MW.slider(ctl, { label: 'ω_x', min: -1, max: 1, step: 0.25, value: wx, onInput: x => { wx = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω_y', min: -1, max: 1, step: 0.25, value: wy, onInput: x => { wy = x; view.redraw(); } });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

if __name__ == '__main__':
    print(build('kap3', W))
