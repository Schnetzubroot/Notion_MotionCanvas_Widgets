"""Widgets zu Kapitel 3.6 (Woche 5): ebene Bewegung, Momentanzentrum, Polbahnen, Planetengetriebe, ebene Fachwerke."""
from template import build

W = []

# ---------------------------------------------------------------- 3.6 Momentanzentrum
W.append(dict(file='3-6-momentanzentrum.html', title='Satz vom Momentanzentrum: v = ω r (Fig. 3.19)',
  sub='Bei einer ebenen Bewegung mit ω ≠ 0 gibt es einen einzigen ruhenden Punkt Z der Ebene. Jeder Punkt M bewegt sich senkrecht zu ZM mit der Schnelligkeit v = ω r, r = |ZM|.',
  hint='Z und die Punkte ziehen, ω ändern.', legend=[('--c1', 'v = ω × ZM'), ('--c5', 'Momentanzentrum Z'), ('--c2', 'Kreise um Z')], js=r'''
  let Z = [0.2, 0.1], om = 1.0; const pts = [[-2.4, 1.2], [0.9, 1.7], [2.5, -0.6], [-0.6, -1.4]];
  const view = MW.View2D(cv, { xmin: -4, xmax: 4, ymin: -2.7, ymax: 3 }, v => {
    const C = v.C, plate = [[-2.6, -1.9], [2.9, -1.7], [3.1, 2.4], [-2.4, 2.6]];
    v.poly(plate, C.line, 1.5, null, true, C.fill); v.text([-2.4, 2.6], 'K', C.muted, 6, -14, 13, false);
    const rows = [];
    pts.forEach((p, i) => {
      const zm = V.sub(p, Z), r = V.norm(zm), vel = [-om * zm[1], om * zm[0]];
      if (r > 0.02) v.circle(Z, r, C.c2, 1, [4, 4]);
      v.line(Z, p, C.line, 1, [3, 3]);
      v.arrow(p, V.mul(vel, 0.5), C.c1, 2.8); v.dot(p, C.fg, 5); v.text(p, 'M' + (i + 1), C.fg, 7, 14, 12);
      rows.push(['M' + (i + 1) + ': r = ' + fmt(r) + ', v = ω r', fmt(Math.abs(om) * r)]);
    });
    v.dot(Z, C.c5, 7); v.text(Z, 'Z', C.c5, 9, 14, 14);
    MW.info(infoEl, 'v_Z = 0, v_M ⊥ ZM, |v_M| = |ω| r' + (om === 0 ? ' (ω = 0: Translation)' : ''), [['ω', fmt(om)], ...rows],
      'Die Schnelligkeit wächst linear mit dem Abstand r zu Z, und die Pfeile stehen senkrecht auf ZM (tangential zu den gestrichelten Kreisen).');
  });
  view.handle(() => Z, p => { Z = p; }); pts.forEach((_, i) => view.handle(() => pts[i], p => { pts[i] = p; }));
  MW.slider(ctl, { label: 'ω', min: -2, max: 2, step: 0.1, value: om, onInput: x => { om = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.6 Polbahnen (Leiter)
W.append(dict(file='3-6-polbahnen.html', title='Polbahnen einer an der Wand rutschenden Leiter (Fig. 3.22/3.23)',
  sub='Das Momentanzentrum Z liegt über B und neben A: Z = (L cos φ, L sin φ). Die feste Polbahn ist der Viertelkreis um O mit Radius L, die bewegliche Polbahn der Kreis um die Stabmitte M mit Radius L/2. Die Leiter bewegt sich, als rolle der kleine Kreis im grossen.',
  hint='φ ändern oder abspielen.', legend=[('--c2', 'feste Polbahn (Radius L um O)'), ('--c3', 'bewegliche Polbahn (Radius L/2 um M)'), ('--c1', 'v_A, v_B'), ('--c5', 'Momentanzentrum Z')], js=r'''
  const L = 3; let phi = 50, trace = true, ghost = true;
  const view = MW.View2D(cv, { xmin: -0.8, xmax: 4.2, ymin: -0.6, ymax: 3.9 }, v => {
    const C = v.C, f = phi * MW.deg, A = [0, L * Math.sin(f)], B = [L * Math.cos(f), 0], M = V.mul(V.add(A, B), 0.5), Z = [B[0], A[1]];
    v.arrow([-0.6, 0], [4.1, 0], C.muted, 1.2, 8); v.arrow([0, -0.4], [0, 3.8], C.muted, 1.2, 8); v.text([4.1, 0], 'x', C.muted, -4, -8, 13, false); v.text([0, 3.8], 'y', C.muted, 8, -4, 13, false);
    if (ghost) for (let a = 85; a >= 10; a -= 5) { const g = a * MW.deg; v.line([0, L * Math.sin(g)], [L * Math.cos(g), 0], C.line, 1); }
    const fixed = []; for (let a = 5; a <= 90; a += 1) fixed.push([L * Math.cos(a * MW.deg), L * Math.sin(a * MW.deg)]); v.poly(fixed, C.muted, 1.2, [4, 4]);
    if (trace) { const tr = []; for (let a = phi; a <= 88; a += 1) tr.push([L * Math.cos(a * MW.deg), L * Math.sin(a * MW.deg)]); if (tr.length > 1) v.poly(tr, C.c2, 3.2, null); }
    v.circle(M, L / 2, C.c3, 2.2, null, null);
    v.line(A, B, C.fg, 6);
    v.line(A, Z, C.line, 1, [3, 3]); v.line(B, Z, C.line, 1, [3, 3]);
    const u = 1, vB = [u, 0], om = u / A[1], vA = [0, -om * B[0]];
    v.arrow(B, V.mul(vB, 0.7), C.c1, 2.6); v.arrow(A, V.mul(vA, 0.7), C.c1, 2.6);
    v.dot(A, C.fg, 5); v.dot(B, C.fg, 5); v.dot(M, C.c3, 4); v.dot([0, 0], C.muted, 4); v.dot(Z, C.c5, 7);
    v.text(A, 'A', C.fg, -16, 4); v.text(B, 'B', C.fg, 6, 16); v.text(M, 'M', C.c3, 8, -6, 12); v.text(Z, 'Z', C.c5, 8, -10, 14); v.text([0, 0], 'O', C.muted, -14, 14, 12);
    MW.info(infoEl, 'Z = (L cos φ, L sin φ) = (' + fmt(Z[0]) + ', ' + fmt(Z[1]) + ')', [['φ', fmt(phi, 0) + '°'], ['|OZ|', fmt(V.norm(Z))], ['|MZ|', fmt(V.norm(V.sub(Z, M)))], ['ω = v_B / |ZB| (für v_B = 1)', fmt(om)], ['v_A = v_B cot φ (nach unten)', fmt(Math.abs(vA[1]))]],
      'Z liegt immer im Abstand L von O (feste Polbahn) und im Abstand L/2 von M (bewegliche Polbahn, Satz des Thales). Alle Punkte der Leiter ausser A, B laufen auf Ellipsen.');
  });
  MW.player(ctl, { t0: 8, t1: 85, duration: 6, value: phi, label: 'φ', fmt: x => fmt(x, 0) + '°', onTime: x => { phi = x; view.redraw(); } });
  MW.check(ctl, 'Spur von Z', true, x => { trace = x; view.redraw(); });
  MW.check(ctl, 'frühere Lagen', true, x => { ghost = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 3.6 Planetengetriebe
W.append(dict(file='3-6-planetengetriebe.html', title='Planetengetriebe (Fig. 3.21)',
  sub='Das Planetenrad mit R<sub>3</sub> = (R<sub>2</sub> − R<sub>1</sub>)/2 rollt zwischen Sonnenrad (R<sub>1</sub>, ω<sub>1</sub>) und Hohlrad (R<sub>2</sub>, ω<sub>2</sub>). Die Kontaktpunkte P, Q haben die Geschwindigkeiten R<sub>1</sub>ω<sub>1</sub> und R<sub>2</sub>ω<sub>2</sub>, dazwischen ist die Verteilung linear.',
  hint='Abspielen, Radien und Drehzahlen ändern.', legend=[('--c1', 'v_P, v_Q'), ('--c4', 'v_M (Mittelwert)'), ('--c5', 'Momentanzentrum des Planeten')], js=r'''
  let R1 = 1, R2 = 3, w1 = 1, w2 = 0, t = 1.0;
  const view = MW.View2D(cv, { xmin: -4.4, xmax: 4.4, ymin: -3.6, ymax: 3.6 }, v => {
    const C = v.C, R3 = (R2 - R1) / 2, Lm = (R1 + R2) / 2, wA = (R1 * w1 + R2 * w2) / (R1 + R2), w3 = R2 > R1 ? (R2 * w2 - R1 * w1) / (R2 - R1) : 0;
    const th = wA * t, er = [Math.cos(th), Math.sin(th)], et = [-Math.sin(th), Math.cos(th)], M = V.mul(er, Lm), S = V.mul(er, R1), T = V.mul(er, R2);
    v.circle([0, 0], R2 + 0.25, C.line, 1.5, null, null); v.circle([0, 0], R2, C.fg, 2, null, C.fill);
    const spoke = (c, r, a, col) => v.line(V.add(c, V.mul([Math.cos(a), Math.sin(a)], r * 0.55)), V.add(c, V.mul([Math.cos(a), Math.sin(a)], r)), col, 2);
    for (let i = 0; i < 6; i++) { v.line(V.mul([Math.cos(w2 * t + i * Math.PI / 3), Math.sin(w2 * t + i * Math.PI / 3)], R2), V.mul([Math.cos(w2 * t + i * Math.PI / 3), Math.sin(w2 * t + i * Math.PI / 3)], R2 + 0.25), C.fg, 2); }
    v.circle([0, 0], R1, C.fg, 2, null, C.bg || null); for (let i = 0; i < 4; i++) spoke([0, 0], R1, w1 * t + i * Math.PI / 2, C.muted);
    v.circle(M, R3, C.c2, 2.2, null, C.fill); for (let i = 0; i < 4; i++) spoke(M, R3, w3 * t + i * Math.PI / 2, C.muted);
    v.line([0, 0], M, C.line, 2.4, [6, 3]);
    const vS = V.mul(et, R1 * w1), vT = V.mul(et, R2 * w2), vM = V.mul(et, (R1 * w1 + R2 * w2) / 2), sc = 0.7;
    v.arrow(S, V.mul(vS, sc), C.c1, 2.6); v.arrow(T, V.mul(vT, sc), C.c1, 2.6); v.arrow(M, V.mul(vM, sc), C.c4, 3);
    v.dot(S, C.fg, 4); v.dot(T, C.fg, 4); v.dot(M, C.fg, 4); v.dot([0, 0], C.fg, 4);
    v.text(S, 'P', C.fg, -14, -8, 12); v.text(T, 'Q', C.fg, 8, -8, 12); v.text(M, 'M', C.fg, -4, 14, 12);
    if (Math.abs(w3) > 1e-6) { const rz = R1 - R1 * w1 / w3; if (Math.abs(rz) < 12) { const Zp = V.mul(er, rz); v.dot(Zp, C.c5, 6); v.text(Zp, 'Z', C.c5, 8, 14, 13); } }
    MW.info(infoEl, 'ω_Arm = (R₁ω₁ + R₂ω₂)/(R₁ + R₂) = ' + fmt(wA), [['R₃ = (R₂ − R₁)/2', fmt(R3)], ['L = (R₁ + R₂)/2', fmt(Lm)], ['v_M = (R₁ω₁ + R₂ω₂)/2', fmt((R1 * w1 + R2 * w2) / 2)], ['ω_Planet = (R₂ω₂ − R₁ω₁)/(R₂ − R₁)', fmt(w3)]],
      'Auf der Geraden P–Q ist die Geschwindigkeit linear: v_M ist der Mittelwert von v_P und v_Q. Ruht das Hohlrad (ω₂ = 0), gilt ω_Arm = R₁ω₁/(R₁ + R₂).');
  });
  MW.player(ctl, { t0: 0, t1: 6.3, duration: 8, value: t, label: 't', fmt: x => fmt(x), onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'R₁', min: 0.6, max: 2, step: 0.1, value: R1, onInput: x => { R1 = x; if (R2 < R1 + 0.8) { R2 = R1 + 0.8; s2.set(R2); } view.redraw(); } });
  const s2 = MW.slider(ctl, { label: 'R₂', min: 1.4, max: 3.6, step: 0.1, value: R2, onInput: x => { R2 = Math.max(x, R1 + 0.8); s2.set(R2); view.redraw(); } });
  MW.slider(ctl, { label: 'ω₁', min: -2, max: 2, step: 0.5, value: w1, onInput: x => { w1 = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω₂', min: -2, max: 2, step: 0.5, value: w2, onInput: x => { w2 = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 3.6 Fachwerk (ZP1 2023 A2)
W.append(dict(file='3-6-fachwerk.html', title='Ebenes Fachwerk (ZP1 2023 A2): Körper, Parallelogramm, Rotationsgeschwindigkeiten',
  sub='Das Fachwerk besteht aus drei starren Teilen: dem Dreiecksbereich mit F (rotiert um F), dem Dreiecksbereich mit H (rotiert um H) und dem Parallelogramm DIJK. Die Stäbe DK und IJ haben gleiche Rotationsgeschwindigkeit, ebenso DI und KJ (Parallelogrammregel).',
  hint='ω der Platte um F ändern.', legend=[('--c1', 'Körper um F'), ('--c2', 'Körper um H'), ('--c3', 'Parallelogramm D–I–J–K'), ('--c4', 'Geschwindigkeiten')], js=r'''
  const L = 1, h = Math.sqrt(3) / 2; let om = 1;
  const N = { A: [0, 0], F: [1, 0], B: [0.5, h], E: [1.5, h], C: [1, 2 * h], D: [2, 2 * h], I: [3, 2 * h], K: [2.5, h], J: [3.5, h], G: [3, 0], H: [4, 0] };
  const left = ['A-F', 'A-B', 'B-F', 'B-E', 'E-F', 'B-C', 'C-E', 'C-D', 'D-E'], par = ['D-I', 'D-K', 'I-J', 'K-J'], right = ['K-G', 'G-J', 'G-H', 'J-H'];
  const rotv = (Zc, wz, p) => [-wz * (p[1] - Zc[1]), wz * (p[0] - Zc[0])];
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 4.6, ymin: -1.0, ymax: 2.2 }, v => {
    const C = v.C, wF = -om, wH = 2 * om, wDK = -4 * om;                  // z-Komponenten
    const vel = { D: rotv(N.F, wF, N.D) }; ['A', 'B', 'C', 'E'].forEach(k => vel[k] = rotv(N.F, wF, N[k])); ['K', 'J', 'G'].forEach(k => vel[k] = rotv(N.H, wH, N[k]));
    vel.I = V.add(vel.D, rotv([0, 0], wH, V.sub(N.I, N.D)));                   // DI hat ω = ω_H
    const res = V.norm(V.sub(vel.K, V.add(vel.D, rotv([0, 0], wDK, V.sub(N.K, N.D))))), res2 = V.norm(V.sub(vel.I, V.add(vel.J, rotv([0, 0], wDK, V.sub(N.I, N.J)))));
    const draw = (list, col, wd) => list.forEach(s => { const [a, b] = s.split('-'); v.line(N[a], N[b], col, wd); });
    draw(left, C.c1, 3); draw(right, C.c2, 3); draw(par, C.c3, 3);
    Object.keys(N).forEach(k => { v.dot(N[k], C.fg, 4); v.text(N[k], k, C.fg, 5, -10, 12); });
    ['D', 'I', 'J', 'K', 'G', 'E'].forEach(k => v.arrow(N[k], V.mul(vel[k], 0.35), C.c4, 2.4));
    [N.F, N.H].forEach(p => { v.dot(p, C.c5, 6); }); v.text(N.F, 'F', C.c5, -2, 16, 13); v.text(N.H, 'H', C.c5, -2, 16, 13);
    MW.info(infoEl, 'Platte um F: ω = (0, 0, −' + fmt(om) + ') · v_D = ωL(√3, −1)', [['v_D', fv(vel.D)], ['ω_DK (A2.2)', fmt(wDK / om, 0) + ' ω, also |ω_DK| = 4ω'], ['ω_H (Körper um H)', fmt(wH / om, 0) + ' ω'], ['|v_G| = ω_H · HG (A2.3)', fmt(V.norm(vel.G)) + '  (= 2ωL)'], ['Kontrolle v_K, v_I zweimal berechnet', fmt(res + res2, 6)]],
      'Aus v_K = v_D + ω_DK × DK und v_K = ω_H × HK folgt ω_H = 2ω und ω_DK = −4ω. Die Parallelogrammregel liefert ω_DI = ω_KJ = ω_H.');
  });
  MW.slider(ctl, { label: 'ω', min: 0.25, max: 2, step: 0.25, value: om, onInput: x => { om = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('kap3', W))
