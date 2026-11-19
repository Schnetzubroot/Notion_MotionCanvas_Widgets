"""Widgets zu Kapitel 3.4–3.5 (Woche 4): Kreiselung, Kinemate und Invarianten, Zentralachse und Schraube."""
from template import build

W = []

ROT = r'''
  // Drehung von p um die Achse durch A mit Richtung k (Einheitsvektor) um den Winkel th (Rodrigues)
  const rot = (p, A, k, th) => { const q = V.sub(p, A), c = Math.cos(th), s = Math.sin(th);
    return V.add(A, V.add(V.add(V.mul(q, c), V.mul(V.cross(k, q), s)), V.mul(k, V.dot(k, q) * (1 - c)))); };
'''

# ---------------------------------------------------------------- 3.4
W.append(dict(file='3-4-kreiselung.html', title='Kreiselung: momentane Rotation um eine wandernde Achse (Fig. 3.11)', tall=True,
  sub='Bei der Kreiselung ruht nur ein Punkt O dauernd. In jedem Augenblick ruht aber eine ganze Achse μ durch O, und v = ω × OM. Die Achse wandert dabei im Raum (fester Polkegel) und im Körper (beweglicher Polkegel).',
  hint='Abspielen, Öffnungswinkel β ändern, Ansicht ziehen.', legend=[('--c5', 'Momentanachse μ, ω'), ('--c1', 'v = ω × OM'), ('--c2', 'μ im Raum (fester Polkegel)'), ('--c3', 'μ im Körper (beweglicher Polkegel)')], js=ROT + r'''
  let beta = 35, w = 2, t = 2.2;
  const box = []; [-0.7, 0.7].forEach(x => [-0.5, 0.5].forEach(y => [-0.4, 0.9].forEach(z => box.push([x, y, z]))));
  const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
  const kOf = s => { const b = beta * MW.deg; return [Math.sin(b) * Math.cos(s), Math.sin(b) * Math.sin(s), Math.cos(b)]; };
  const place = (R, p) => V.add(V.add(V.mul(R[0], p[0]), V.mul(R[1], p[1])), V.mul(R[2], p[2]));
  // Orientierung durch Integration von dR/dt = ω × R (Achse k(s) wandert, ω = w k(s))
  function integrate(tEnd) {
    let R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    const body = u => R.map(c => V.dot(c, u)), hist = [{ k: kOf(0), b: body(kOf(0)) }];
    const n = Math.max(1, Math.ceil(tEnd / 0.02)), dt = tEnd / n;
    for (let i = 1; i <= n; i++) { const k = kOf((i - 0.5) * dt); R = R.map(c => rot(c, [0, 0, 0], k, w * dt)); const k1 = kOf(i * dt); hist.push({ k: k1, b: body(k1) }); }
    return { R, hist };
  }
  const view = MW.View3D(cv, { extent: 1.75, yaw: 35, pitch: 20, center: [0, 0, 0.3] }, v => {
    const C = v.C, { R, hist } = integrate(t), k = V.unit(kOf(t)), om = V.mul(k, w), O = [0, 0, 0];
    const P = box.map(p => place(R, p));
    if (hist.length > 1) { v.poly(hist.map(h => V.mul(h.k, 1.6)), C.c2, 2, null); v.poly(hist.map(h => V.mul(place(R, h.b), 1.6)), C.c3, 2, null); }
    v.line(V.mul(k, -1.9), V.mul(k, 2.1), C.c5, 1.6, [8, 3, 2, 3]); v.text(V.mul(k, 2.1), 'μ', C.c5, 6, 0);
    v.arrow(O, V.mul(k, 0.35 * w + 0.2), C.c5, 3); v.text(V.mul(k, 0.35 * w + 0.2), 'ω', C.c5, 6, 0);
    edges.forEach(([i, j]) => v.line(P[i], P[j], C.fg, 1.6));
    let vmax = 0;
    P.forEach(p => { const vp = V.cross(om, p); vmax = Math.max(vmax, V.norm(vp)); v.arrow(p, V.mul(vp, 0.22), C.c1, 1.8, 7); });
    const Q = V.mul(k, 1.35); v.dot(Q, C.c5, 4); v.text(Q, 'v = 0', C.c5, 8, 12, 12);
    v.dot(O, C.fg, 5); v.text(O, 'O', C.fg, -14, 14);
    MW.info(infoEl, 'v_M = ω × OM mit ω = ' + fv(om) + ' (momentan)', [['Öffnungswinkel β der Kegel', fmt(beta, 0) + '°'], ['|ω|', fmt(w)], ['grösstes |v| der Ecken', fmt(vmax)], ['v auf der Achse μ', '0']],
      'Nur O ruht für alle Zeiten. Die Achse μ durch O ruht nur in diesem Augenblick (Buch Fig. 3.11). Beide Spuren berühren sich in der Momentanachse: Die Kreiselung ist ein Abrollen des beweglichen auf dem festen Polkegel.');
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 10, value: t, label: 't', fmt: x => fmt(x), onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'β', min: 5, max: 80, step: 1, value: beta, unit: '°', onInput: x => { beta = x; view.redraw(); } });
  MW.slider(ctl, { label: '|ω|', min: 0.5, max: 4, step: 0.1, value: w, onInput: x => { w = x; view.redraw(); } });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

# ---------------------------------------------------------------- 3.5 Kinemate und Invarianten
W.append(dict(file='3-5-kinemate-wechsel.html', title='Kinemate, Bezugspunktwechsel und Invarianten (Würfel)', tall=True,
  sub='Der Bewegungszustand ist die Kinemate {v<sub>B</sub>, ω}. Wechselt man den Bezugspunkt, gilt v<sub>B\'</sub> = v<sub>B</sub> + ω × BB\'. Dabei bleiben ω (1. Invariante) und ω · v (2. Invariante) gleich.',
  hint='Bezugspunkt wählen, Beispiel wählen oder v_A und ω einstellen.', legend=[('--c1', 'v in allen Ecken'), ('--c5', 'ω'), ('--c3', 'v_ω (Anteil ∥ ω, überall gleich)'), ('--c4', 'v_⊥ (Anteil ⊥ ω)')], js=r'''
  const P0 = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], NAMES = 'ABCDEFGH';
  const edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  const PRE = { zp23: ['Allgemein (ZP1 2023 A1)', [3, 1, 1], [0, 1, 1]], transl: ['Translation (ω = 0)', [1, 0.5, 0], [0, 0, 0]], rot0: ['Rotation, A auf μ (v_A = 0)', [0, 0, 0], [0, 1, 1]],
    rotp: ['Rotation, A nicht auf μ (v_A ⊥ ω)', [1, 0, 1], [0, 1, 0]], schr: ['Schraubung', [1, 2, 0], [0, 2, 0]] };
  let vA = [3, 1, 1], om = [0, 1, 1], ref = 0;
  const sl = [];
  const view = MW.View3D(cv, { extent: 1.6, yaw: 35, pitch: 22, center: [0.5, 0.5, 0.5] }, v => {
    const C = v.C, A = P0[0], vel = p => V.add(vA, V.cross(om, V.sub(p, A))), sc = 0.2;
    edges.forEach(([i, j]) => v.line(P0[i], P0[j], C.fg, 1.6));
    P0.forEach((p, i) => { if (i !== ref) v.arrow(p, V.mul(vel(p), sc), C.c1, 1.6, 7); v.dot(p, C.fg, 3.5); v.text(p, NAMES[i], C.muted, 7, -7, 12); });
    const B = P0[ref], vB = vel(B), w2 = V.dot(om, om), vw = w2 > 1e-9 ? V.mul(om, V.dot(vB, om) / w2) : [0, 0, 0], vp = V.sub(vB, vw);
    if (V.norm(vp) > 1e-9 && V.norm(vw) > 1e-9) { v.line(V.add(B, V.mul(vw, sc)), V.add(B, V.mul(vB, sc)), C.line, 1, [3, 3]); v.line(V.add(B, V.mul(vp, sc)), V.add(B, V.mul(vB, sc)), C.line, 1, [3, 3]); }
    if (V.norm(vw) > 1e-9) v.arrow(B, V.mul(vw, sc), C.c3, 3.4);
    if (V.norm(vp) > 1e-9) v.arrow(B, V.mul(vp, sc), C.c4, 2.6);
    if (V.norm(om) > 1e-9) { v.arrow(B, V.mul(om, 0.45), C.c5, 3); v.text(V.add(B, V.mul(om, 0.45)), 'ω', C.c5, 6, 0); }
    v.arrow(B, V.mul(vB, sc), C.c1, 3.4); v.dot(B, C.fg, 6); v.text(B, 'v_' + NAMES[ref], C.c1, 10, 14, 13);
    const dot = V.dot(om, vB), zero = V.norm(om) < 1e-9 ? 'Translation (ω = 0)' : Math.abs(dot) < 1e-9 ? (V.norm(vB) < 1e-9 ? 'Rotation, ' + NAMES[ref] + ' liegt auf μ' : 'Rotation, ' + NAMES[ref] + ' liegt nicht auf μ (v ⊥ ω)') : 'Schraubung (ω · v ≠ 0)';
    MW.info(infoEl, 'Kinemate in ' + NAMES[ref] + ': {v_' + NAMES[ref] + ' = ' + fv(vB) + ', ω = ' + fv(om) + '}', [['v_' + NAMES[ref] + ' = v_A + ω × A' + NAMES[ref], fv(vB)], ['ω (1. Invariante)', fv(om)], ['ω · v (2. Invariante)', fmt(dot)],
      ['v_ω = (ω · v) ω / |ω|²', fv(vw)], ['v_⊥ = v − v_ω', fv(vp)], ['Zustand', zero]],
      'Wechsle den Bezugspunkt: v und v_⊥ ändern sich, ω, ω · v und v_ω (violett) bleiben gleich. Gilt ω · v = 0, ist der Zustand eine momentane Rotation oder Translation, sonst eine Schraubung.');
  });
  MW.select(ctl, 'Bezugspunkt', NAMES.split('').map((n, i) => [i, n]), x => { ref = +x; view.redraw(); }).set(ref);
  const pre = MW.select(ctl, 'Beispiel', Object.entries(PRE).map(([k, a]) => [k, a[0]]), x => { vA = PRE[x][1].slice(); om = PRE[x][2].slice(); sl.forEach((s, i) => s.set(i < 3 ? vA[i] : om[i - 3])); view.redraw(); });
  pre.set('zp23');
  ['x', 'y', 'z'].forEach((c, i) => sl.push(MW.slider(ctl, { label: 'v_A,' + c, min: -3, max: 3, step: 0.5, value: vA[i], onInput: x => { vA[i] = x; view.redraw(); } })));
  ['x', 'y', 'z'].forEach((c, i) => sl.push(MW.slider(ctl, { label: 'ω_' + c, min: -2, max: 2, step: 0.5, value: om[i], onInput: x => { om[i] = x; view.redraw(); } })));
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

# ---------------------------------------------------------------- 3.5 Zentralachse und Schraube
W.append(dict(file='3-5-schraube.html', title='Schraubung um die Zentralachse', tall=True,
  sub='Die allgemeinste Bewegung ist momentan eine Schraubung um die Zentralachse ζ: Drehen mit ω um ζ und gleichzeitig Verschieben mit v<sub>ω</sub> entlang ζ. Jeder Punkt hat v = v<sub>ω</sub> + ω × ρ mit dem Abstand ρ zu ζ.',
  hint='Abspielen, Steigung und Abstand ändern.', legend=[('--c5', 'Zentralachse ζ'), ('--c1', 'ω × ρ (senkrecht zu ζ)'), ('--c3', 'v_ω (entlang ζ, überall gleich)'), ('--c4', 'v = v_ω + ω × ρ'), ('--c2', 'Bahn von M (Schraubenlinie)')], js=ROT + r'''
  let h = 0.25, d = 0.9, t = 3.5;                     // ω = 1 e_z, v_ω = h e_z, Abstand d von ζ
  const half = 0.2, box = []; [-1, 1].forEach(x => [-1, 1].forEach(y => [-1, 1].forEach(z => box.push([x * half, y * half, z * half]))));
  const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]], ez = [0, 0, 1];
  const move = (p, s) => V.add(rot(p, [0, 0, 0], ez, s), [0, 0, h * s]);
  const view = MW.View3D(cv, { extent: 2.3, yaw: 40, pitch: 18, center: [0, 0, 1.2] }, v => {
    const C = v.C, M0 = [d, 0, 0], M = move(M0, t);
    v.line([0, 0, -0.6], [0, 0, 3.4], C.c5, 1.6, [8, 3, 2, 3]); v.text([0, 0, 3.4], 'ζ', C.c5, 6, 0);
    const tr = []; for (let i = 0; i <= 160; i++) tr.push(move(M0, t * i / 160));
    v.poly(tr, C.c2, 2, null);
    const P = box.map(p => move(V.add(M0, p), t)); edges.forEach(([i, j]) => v.line(P[i], P[j], C.fg, 1.4));
    const vo = [0, 0, h], vp = V.cross(ez, V.sub(M, [0, 0, M[2]])), vt = V.add(vo, vp), D = [0, 0, M[2]], sc = 1.8;
    v.line(D, M, C.line, 1, [3, 3]); v.dot(D, C.c5, 3);
    v.arrow(M, V.mul(vp, sc), C.c1, 2.4); v.arrow(M, V.mul(vo, sc), C.c3, 3); v.arrow(M, V.mul(vt, sc), C.c4, 3.4); v.dot(M, C.fg, 5); v.text(M, 'M', C.fg, 8, -8);
    v.arrow([0, 0, 0], [0, 0, 0.9], C.c5, 3); v.text([0, 0, 0.9], 'ω', C.c5, 8, 0);
    MW.info(infoEl, 'ω = (0, 0, 1), v_ω = (0, 0, ' + fmt(h) + ')', [['Steigung v_ω / ω', fmt(h)], ['Ganghöhe 2π v_ω / ω', fmt(2 * Math.PI * h)], ['Abstand ρ von ζ', fmt(d)], ['|v_M| = √(v_ω² + (ωρ)²)', fmt(V.norm(vt))], ['kleinste Schnelligkeit (auf ζ)', fmt(Math.abs(h))]],
      Math.abs(h) < 1e-9 ? 'Steigung 0: v_ω = 0, die Schraubung ist eine reine Rotation um ζ (2. Invariante ω · v = 0).' : 'Auf ζ ist die Schnelligkeit am kleinsten, nämlich |v_ω|. Mit dem Abstand zu ζ wächst nur der Anteil ω × ρ.');
  });
  MW.player(ctl, { t0: 0, t1: 3 * Math.PI, duration: 9, value: t, label: 'Φ', fmt: x => fmt(x / MW.deg, 0) + '°', onTime: x => { t = x; view.redraw(); } });
  MW.slider(ctl, { label: 'v_ω / ω', min: -0.3, max: 0.3, step: 0.05, value: h, onInput: x => { h = x; view.redraw(); } });
  MW.slider(ctl, { label: 'Abstand ρ', min: 0.2, max: 1.6, step: 0.1, value: d, onInput: x => { d = x; view.redraw(); } });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

if __name__ == '__main__':
    print(build('kap3', W))
