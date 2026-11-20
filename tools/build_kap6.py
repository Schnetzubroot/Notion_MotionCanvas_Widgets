"""Widgets zu Kapitel 6.1–6.4 (Woche 7): Äquivalenz, Moment, Kräftepaar, Hebelgesetz, Gleichgewicht."""
from template import build

W = []
HELP = r'''
  const cr = (a, b) => a[0] * b[1] - a[1] * b[0];          // z-Komponente von a × b (2D)
  const arcArrow = (v, c, r, a0, a1, col, w) => { const pts = []; const n = 40; for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; pts.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
    v.poly(pts, col, w); const e = pts[n], d = V.sub(pts[n], pts[n - 2]); v.arrow(V.sub(e, V.mul(V.unit(d), 0.12)), V.mul(V.unit(d), 0.14), col, w, 10); };
  const mArc = (v, c, M, col, r = 0.5) => { if (Math.abs(M) < 0.02) return; M > 0 ? arcArrow(v, c, r, 0.5, 5.0, col, 2.6) : arcArrow(v, c, r, 5.0, 0.5, col, 2.6); };
'''

# ---------------------------------------------------------------- 6.1
W.append(dict(file='6-1-aequivalenz.html', title='Statische Äquivalenz: eine Kräftegruppe wird durch {R, M<sub>O</sub>} ersetzt',
  sub='Zwei Kräftegruppen sind statisch äquivalent, wenn sie für jede Bewegung dieselbe Leistung haben, also in einem Punkt dieselbe Resultierende R und dasselbe Moment M<sub>O</sub> besitzen. Jede Gruppe darf daher durch die Dyname {R, M<sub>O</sub>} ersetzt werden, in der Ebene sogar (für R ≠ 0) durch eine einzige Kraft R auf der Wirkungslinie im Abstand d = |M<sub>O</sub>|/|R|.',
  hint='Kräfte, Angriffspunkte und Bezugspunkt O ziehen, Probebewegung wählen.', legend=[('--c1', 'Kräfte F_i'), ('--c4', 'Resultierende R'), ('--c2', 'Moment M_O'), ('--c5', 'Bezugspunkt O')], js=HELP + r'''
  let A = [[1.8, 0.8], [-1.2, 1.1], [0.6, -1.2]], F = [[0.2, 1.3], [1.0, 0.4], [-0.6, 0.7]], O = [-0.2, 0.0], vO = [0.5, 0.3], om = 0.6, single = true;
  const view = MW.View2D(cv, { xmin: -4.2, xmax: 4.2, ymin: -2.8, ymax: 2.8 }, v => {
    const C = v.C; let R = [0, 0], MO = 0, P1 = 0;
    const vel = p => V.add(vO, [-om * (p[1] - O[1]), om * (p[0] - O[0])]);
    F.forEach((f, i) => { R = V.add(R, f); MO += cr(V.sub(A[i], O), f); const w = vel(A[i]); P1 += (f[0] * w[0] + f[1] * w[1]) * 10;
      v.arrow(A[i], f, C.c1, 2.6); v.dot(A[i], C.c5, 4); v.text(V.add(A[i], f), 'F' + (i + 1), C.c1, 6, -4, 13); });
    v.dot(O, C.c5, 6); v.text(O, 'O', C.c5, -16, 16, 14);
    v.arrow(O, vO, C.c3, 2.4, 8);
    v.arrow(O, R, C.c4, 4, 12); v.text(V.add(O, R), 'R', C.c4, 6, -4, 15);
    mArc(v, O, MO, C.c2, 0.55); v.text(O, 'M_O', C.c2, 14, -14, 13);
    const Rn = V.norm(R); let P3 = null, d = 0, txt;
    if (Rn > 0.08) { const n = [-R[1] / Rn, R[0] / Rn]; d = -MO / Rn; const Q = V.add(O, V.mul(n, d)); const u = V.unit(R);
      if (single) { v.line(V.sub(Q, V.mul(u, 6)), V.add(Q, V.mul(u, 6)), C.c4, 1.2, [6, 4]); v.arrow(Q, R, C.c4, 4, 12); v.dot(Q, C.c4, 5); v.text(Q, 'Q', C.c4, -14, -8, 13); v.line(O, Q, C.c4, 1.2, [2, 3]); }
      const w = vel(Q); P3 = (R[0] * w[0] + R[1] * w[1]) * 10; txt = fmt(P3, 2) + ' W'; }
    const P2 = (vO[0] * R[0] + vO[1] * R[1]) * 10 + om * MO * 10;
    MW.info(infoEl, 'Gleiche Leistung bei jeder Probebewegung: statisch äquivalent', [['R', fv(V.mul(R, 10), 1) + ' N'], ['M_O (z)', fmt(MO * 10, 1) + ' Nm'], ['Abstand d der Ersatzkraft', Rn > 0.08 ? fmt(Math.abs(d), 2) + ' m' : 'R ≈ 0: Kräftepaar, keine Einzelkraft'],
      ['P der drei Kräfte', fmt(P1, 2) + ' W'], ['P der Dyname {R, M_O}', fmt(P2, 2) + ' W'], ['P der Ersatzkraft in Q', P3 === null ? '–' : txt]],
      'Die Probebewegung (v_O, ω) ist beliebig: Verändern Sie sie, die drei Leistungen bleiben gleich. Das ist der Grund, warum man Kräftegruppen nur durch ihre Dyname {R, M_O} beschreiben muss.');
  });
  F.forEach((_, i) => { view.handle(() => V.add(A[i], F[i]), p => { F[i] = V.sub(p, A[i]); }); view.handle(() => A[i], p => { A[i] = p; }); });
  view.handle(() => O, p => { O = p; });
  MW.slider(ctl, { label: 'v_Ox', min: -2, max: 2, step: 0.1, value: vO[0], unit: ' m/s', onInput: x => { vO[0] = x; view.redraw(); } });
  MW.slider(ctl, { label: 'v_Oy', min: -2, max: 2, step: 0.1, value: vO[1], unit: ' m/s', onInput: x => { vO[1] = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω', min: -2, max: 2, step: 0.1, value: om, unit: ' 1/s', onInput: x => { om = x; view.redraw(); } });
  MW.check(ctl, 'Ersatzkraft zeigen', true, x => { single = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 6.2
W.append(dict(file='6-2-verschiebungssatz.html', title='Moment einer Kräftegruppe und Verschiebungssatz M<sub>P</sub> = M<sub>O</sub> + PO × R',
  sub='Das Moment einer Kräftegruppe hängt vom Bezugspunkt ab. Wechselt man von O nach P, gilt M<sub>P</sub> = M<sub>O</sub> + PO × R. Ist R = 0 (Kräftepaar), ist das Moment vom Bezugspunkt unabhängig.',
  hint='Bezugspunkte O und P sowie die Kräfte ziehen.', legend=[('--c1', 'Kräfte F_i'), ('--c4', 'Resultierende R'), ('--c5', 'Bezugspunkt O'), ('--c2', 'Bezugspunkt P')], js=HELP + r'''
  let A = [[1.8, 0.8], [-1.2, 1.1], [0.6, -1.2]], F = [[0.2, 1.3], [1.0, 0.4], [-0.6, 0.7]], O = [-0.3, 0.2], P = [2.3, -1.3], kp = false;
  const view = MW.View2D(cv, { xmin: -4.2, xmax: 4.2, ymin: -2.8, ymax: 2.8 }, v => {
    const C = v.C; let R = [0, 0], MO = 0, MP = 0;
    F.forEach((f, i) => { R = V.add(R, f); MO += cr(V.sub(A[i], O), f); MP += cr(V.sub(A[i], P), f);
      v.line(O, A[i], C.c5, 1, [2, 4]); v.line(P, A[i], C.c2, 1, [2, 4]);
      v.arrow(A[i], f, C.c1, 2.6); v.dot(A[i], C.muted, 4); v.text(V.add(A[i], f), 'F' + (i + 1), C.c1, 6, -4, 13); });
    if (kp) { /* nichts */ }
    const MP2 = MO + cr(V.sub(O, P), R);
    v.dot(O, C.c5, 6); v.text(O, 'O', C.c5, -16, 16, 14); v.dot(P, C.c2, 6); v.text(P, 'P', C.c2, -16, 16, 14);
    mArc(v, O, MO, C.c5, 0.55); mArc(v, P, MP, C.c2, 0.55);
    v.arrow(O, R, C.c4, 3, 10); v.arrow(P, R, C.c4, 3, 10); v.text(V.add(P, R), 'R', C.c4, 6, -4, 14);
    MW.info(infoEl, 'M_P direkt = M_O + PO × R', [['R', fv(V.mul(R, 10), 1) + ' N'], ['M_O = Σ OA_i × F_i', fmt(MO * 10, 1) + ' Nm'], ['M_P = Σ PA_i × F_i', fmt(MP * 10, 1) + ' Nm'], ['M_O + PO × R', fmt(MP2 * 10, 1) + ' Nm'], ['PO × R (z)', fmt(cr(V.sub(O, P), R) * 10, 1) + ' Nm']],
      'Die Resultierende R ist in jedem Bezugspunkt gleich, nur das Moment ändert sich um PO × R. Schieben Sie die Kräfte so, dass R = 0 wird (Kräftepaar): dann ist M_P = M_O überall.');
  });
  F.forEach((_, i) => { view.handle(() => V.add(A[i], F[i]), p => { F[i] = V.sub(p, A[i]); }); view.handle(() => A[i], p => { A[i] = p; }); });
  view.handle(() => O, p => { O = p; }); view.handle(() => P, p => { P = p; });
'''))

W.append(dict(file='6-2-moment-3d.html', title='Moment einer Kraft bezüglich Punkt und Achse im Raum', tall=True,
  sub='Das Moment einer Kraft F in A bezüglich O ist M<sub>O</sub> = OA × F. Das Moment bezüglich einer Achse durch O mit Einheitsvektor e ist die Komponente M<sub>e</sub> = e·M<sub>O</sub>. Der Betrag |M<sub>O</sub>| = F·d mit dem Hebelarm d (Abstand der Wirkungslinie von O).',
  hint='Regler für A und F, Achse wählen, Ansicht ziehen.', legend=[('--c1', 'Kraft F in A'), ('--c2', 'Moment M_O = OA × F'), ('--c3', 'Achse e'), ('--c4', 'Achsenmoment M_e = (e·M_O) e')], js=r'''
  let Ap = [1.2, 0.8, 0.4], Fv = [0.3, 1.0, 0.8], ax = 'z';
  const axes = { x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1], d1: V.unit([1, 1, 0]), d2: V.unit([1, 1, 1]) };
  const view = MW.View3D(cv, { extent: 2.2, yaw: 40, pitch: 22, center: [0.5, 0.4, 0.5] }, v => {
    const C = v.C, O = [0, 0, 0], e = axes[ax], Mo = V.cross(Ap, Fv), Me = V.dot(e, Mo), Fn = V.norm(Fv), d = Fn > 1e-9 ? V.norm(Mo) / Fn : 0;
    v.floor(3); v.axes(2.6);
    v.line(V.mul(e, -2.3), V.mul(e, 2.3), C.c3, 2, [8, 4]); v.text(V.mul(e, 2.3), 'e', C.c3, 4, 4, 15);
    v.line(O, Ap, C.muted, 1.5, [4, 3]); v.dot(Ap, C.c5, 5); v.text(Ap, 'A', C.c5, 6, 14, 14);
    v.arrow(Ap, Fv, C.c1, 3.4); v.text(V.add(Ap, Fv), 'F', C.c1, 6, -4, 15);
    v.arrow(O, V.mul(Mo, 0.4), C.c2, 3.4); v.text(V.mul(Mo, 0.4), 'M_O', C.c2, 6, -4, 14);
    if (Math.abs(Me) > 1e-3) { v.arrow(O, V.mul(e, Me * 0.4), C.c4, 5, 12); }
    MW.info(infoEl, 'Moment bezüglich Punkt O und Achse e', [['OA, F', fv(Ap) + ',  ' + fv(Fv)], ['M_O = OA × F', fv(Mo)], ['|M_O|, Hebelarm d = |M_O| / |F|', fmt(V.norm(Mo), 2) + ',  d = ' + fmt(d, 2)], ['e', fv(e)], ['M_e = e·M_O', fmt(Me, 2)]],
      'M_O ist senkrecht zu OA und F. Die Achse e = e_z liefert M_z = (OA × F)_z = x F_y − y F_x, also nur die Komponente in der xy-Ebene. M_e ist null, wenn die Wirkungslinie die Achse schneidet oder parallel zu ihr ist.');
  });
  [['A_x', 0], ['A_y', 1], ['A_z', 2]].forEach(([n, i]) => MW.slider(ctl, { label: n, min: -2, max: 2, step: 0.1, value: Ap[i], onInput: x => { Ap[i] = x; view.redraw(); } }));
  [['F_x', 0], ['F_y', 1], ['F_z', 2]].forEach(([n, i]) => MW.slider(ctl, { label: n, min: -2, max: 2, step: 0.1, value: Fv[i], onInput: x => { Fv[i] = x; view.redraw(); } }));
  MW.select(ctl, 'Achse', [['z', 'e_z'], ['x', 'e_x'], ['y', 'e_y'], ['d1', '(1,1,0)/√2'], ['d2', '(1,1,1)/√3']], x => { ax = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 6.3
W.append(dict(file='6-3-kraeftepaar.html', title='Kräftepaar: das Moment M = A′A × F ist vom Bezugspunkt unabhängig',
  sub='Zwei entgegengesetzt gleiche Kräfte F in A und −F in A′ mit verschiedenen Wirkungslinien bilden ein Kräftepaar (R = 0). Sein Moment M = A′A × F hat den Betrag M = b·F (b = Abstand der Wirkungslinien) und ist ein freier Vektor.',
  hint='A, A′, die Kraft und den Bezugspunkt P ziehen.', legend=[('--c1', 'F in A und −F in A′'), ('--c2', 'Moment M des Kräftepaars'), ('--c5', 'Bezugspunkt P')], js=HELP + r'''
  let A = [-0.8, 0.9], A2 = [1.0, -0.7], F = [1.5, 0.5], P = [-2.2, -1.6];
  const view = MW.View2D(cv, { xmin: -4.0, xmax: 4.0, ymin: -2.6, ymax: 2.6 }, v => {
    const C = v.C, mF = V.mul(F, -1), M = cr(V.sub(A, A2), F), b = Math.abs(M) / (V.norm(F) || 1);
    const u = V.unit(F), L = 5;
    v.line(V.sub(A, V.mul(u, L)), V.add(A, V.mul(u, L)), C.line, 1, [5, 4]); v.line(V.sub(A2, V.mul(u, L)), V.add(A2, V.mul(u, L)), C.line, 1, [5, 4]);
    v.arrow(A, F, C.c1, 3.4); v.arrow(A2, mF, C.c1, 3.4); v.dot(A, C.fg, 5); v.dot(A2, C.fg, 5);
    v.text(A, 'A', C.fg, -16, -8, 14); v.text(A2, "A′", C.fg, 8, 16, 14); v.text(V.add(A, F), 'F', C.c1, 6, -6, 15); v.text(V.add(A2, mF), '−F', C.c1, -22, 14, 15);
    const mid = V.mul(V.add(A, A2), 0.5); mArc(v, mid, M, C.c2, 0.6); v.text(mid, 'M', C.c2, 16, -16, 15);
    v.dot(P, C.c5, 6); v.text(P, 'P', C.c5, -16, 16, 14);
    const m1 = cr(V.sub(A, P), F), m2 = cr(V.sub(A2, P), mF);
    MW.info(infoEl, 'Summe der Momente um P ist unabhängig von P', [['R = F + (−F)', '0'], ['M = A′A × F', fmt(M * 10, 1) + ' Nm  (' + (M >= 0 ? 'gegen' : 'im') + ' Uhrzeigersinn)'], ['Breite b, Betrag F', fmt(b, 2) + ' m,  ' + fmt(V.norm(F) * 10, 1) + ' N'], ['b·F', fmt(b * V.norm(F) * 10, 1) + ' Nm'],
      ['Moment von F um P', fmt(m1 * 10, 1) + ' Nm'], ['Moment von −F um P', fmt(m2 * 10, 1) + ' Nm'], ['Summe um P', fmt((m1 + m2) * 10, 1) + ' Nm']],
      'Verschieben Sie P: die beiden Einzelmomente ändern sich, ihre Summe nicht. Auch das ganze Paar darf in der Ebene verschoben und gedreht werden, solange M gleich bleibt.');
  });
  view.handle(() => A, p => { A = p; }); view.handle(() => A2, p => { A2 = p; }); view.handle(() => V.add(A, F), p => { F = V.sub(p, A); }); view.handle(() => P, p => { P = p; });
'''))

W.append(dict(file='6-3-hebelgesetz.html', title='Parallele Kräfte: Kräftemittelpunkt und Hebelgesetz',
  sub='Zwei parallele Kräfte F<sub>1</sub> in x<sub>1</sub> und F<sub>2</sub> in x<sub>2</sub> haben die Resultierende R = F<sub>1</sub> + F<sub>2</sub> im Kräftemittelpunkt x<sub>S</sub> = (F<sub>1</sub>x<sub>1</sub> + F<sub>2</sub>x<sub>2</sub>)/R. Das Hebelgesetz: |F<sub>1</sub>|·|x<sub>S</sub> − x<sub>1</sub>| = |F<sub>2</sub>|·|x<sub>S</sub> − x<sub>2</sub>|. Für F<sub>2</sub> = −F<sub>1</sub> entsteht ein Kräftepaar.',
  hint='Kräfte F₁, F₂ und Positionen x₁, x₂ einstellen (Pfeilspitzen und Fusspunkte ziehbar).', legend=[('--c1', 'F_1'), ('--c3', 'F_2'), ('--c4', 'Resultierende R in S')], js=r'''
  let x1 = -1.8, x2 = 2.2, f1 = 2, f2 = 3, s1, s2;
  const view = MW.View2D(cv, { xmin: -4.4, xmax: 4.4, ymin: -2.4, ymax: 2.6 }, v => {
    const C = v.C, k = 0.45, R = f1 + f2, par = Math.abs(R) < 1e-6;
    v.poly([[-4, 0], [4, 0]], C.fg, 4);
    v.arrow([x1, 0], [0, f1 * k], C.c1, 3.6); v.text([x1, f1 * k], 'F₁', C.c1, 8, 0, 15); v.dot([x1, 0], C.c1, 4);
    v.arrow([x2, 0], [0, f2 * k], C.c3, 3.6); v.text([x2, f2 * k], 'F₂', C.c3, 8, 0, 15); v.dot([x2, 0], C.c3, 4);
    let rows, head, note;
    if (!par) { const xS = (f1 * x1 + f2 * x2) / R; v.arrow([xS, 0], [0, R * k], C.c4, 4.6, 12); v.dot([xS, 0], C.c4, 6); v.text([xS, R * k], 'R', C.c4, 8, 0, 16); v.text([xS, 0], 'S', C.c4, -4, 20, 14);
      rows = [['R = F₁ + F₂', fmt(R, 2)], ['x_S', fmt(xS, 2)], ['|F₁|·|x_S − x₁|', fmt(Math.abs(f1) * Math.abs(xS - x1), 2)], ['|F₂|·|x_S − x₂|', fmt(Math.abs(f2) * Math.abs(xS - x2), 2)]];
      head = f1 * f2 > 0 ? 'Gleichsinnig: S liegt zwischen den Kräften, näher an der grösseren' : 'Gegensinnig: S liegt ausserhalb, auf der Seite der grösseren Kraft';
      note = 'Die beiden Produkte sind gleich: das ist das Hebelgesetz (Momentengleichgewicht um S).'; }
    else { const M = f1 * (x2 - x1) * -1; rows = [['R', '0'], ['Moment M = F₁·(x₂ − x₁)', fmt(Math.abs(f1 * (x2 - x1)), 2)], ['Breite b', fmt(Math.abs(x2 - x1), 2)]]; head = 'F₂ = −F₁: Kräftepaar, kein Kräftemittelpunkt'; note = 'Es gibt keine Einzelkraft, die dieselbe Wirkung hat. M = b F.'; }
    MW.info(infoEl, head, rows, note, par);
  });
  view.handle(() => [x1, f1 * 0.45], p => { f1 = Math.round(p[1] / 0.45 * 4) / 4; s1.set(f1); x1 = p[0]; });
  view.handle(() => [x2, f2 * 0.45], p => { f2 = Math.round(p[1] / 0.45 * 4) / 4; s2.set(f2); x2 = p[0]; });
  s1 = MW.slider(ctl, { label: 'F₁', min: -4, max: 4, step: 0.25, value: f1, onInput: x => { f1 = x; view.redraw(); } });
  s2 = MW.slider(ctl, { label: 'F₂', min: -4, max: 4, step: 0.25, value: f2, onInput: x => { f2 = x; view.redraw(); } });
  MW.button(ctl, 'F₂ = −F₁ (Kräftepaar)', () => { f2 = -f1; s2.set(f2); view.redraw(); });
'''))

# ---------------------------------------------------------------- 6.4
W.append(dict(file='6-4-gleichgewicht.html', title='Gleichgewicht eines Balkens: R = 0 und M<sub>A</sub> = 0',
  sub='Ein starrer Körper ist im Gleichgewicht, wenn die Resultierende R und das Moment M<sub>O</sub> aller Kräfte (Lasten und Lagerreaktionen) verschwinden. In der Ebene gibt das drei Gleichungen: ΣF<sub>x</sub> = 0, ΣF<sub>y</sub> = 0, ΣM<sub>A</sub> = 0, genau genug für Festlager A (A<sub>x</sub>, A<sub>y</sub>) und Loslager B (B<sub>y</sub>).',
  hint='Einzelkraft (Betrag, Richtung, Lage) und Gleichlast verändern.', legend=[('--c1', 'Last F und q'), ('--c4', 'Lagerreaktionen (unbekannte Vektoren positiv angesetzt)')], js=r'''
  let L = 4, xF = 2.5, Fm = 3, th = -60, q = 0.5;
  const view = MW.View2D(cv, { xmin: -1.2, xmax: 9.0, ymin: -2.6, ymax: 3.2 }, v => {
    const C = v.C, k = 0.3, thr = th * MW.deg, Fx = Fm * Math.cos(thr), Fy = Fm * Math.sin(thr), Q = q * L;
    const Ax = -Fx, By = (Q * L / 2 - xF * Fy) / L, Ay = Q - Fy - By;
    // Balken und Lager
    v.poly([[0, 0], [L, 0]], C.fg, 6);
    v.poly([[0, 0], [-0.28, -0.5], [0.28, -0.5]], C.fg, 2, null, true, 'rgba(120,120,120,0.15)'); v.poly([[-0.5, -0.55], [0.5, -0.55]], C.fg, 2);
    v.poly([[L, 0], [L - 0.28, -0.45], [L + 0.28, -0.45]], C.fg, 2, null, true, 'rgba(120,120,120,0.15)'); v.circle([L - 0.14, -0.57], 0.1, C.fg, 2); v.circle([L + 0.14, -0.57], 0.1, C.fg, 2); v.poly([[L - 0.5, -0.67], [L + 0.5, -0.67]], C.fg, 2);
    v.text([0, 0], 'A', C.muted, -18, -14, 15); v.text([L, 0], 'B', C.muted, 10, -14, 15);
    // Gleichlast
    if (q > 0.01) { v.poly([[0, 0.55], [L, 0.55]], C.c1, 1.5); for (let i = 0; i <= 8; i++) v.arrow([L * i / 8, 0.55], [0, -0.5], C.c1, 1.6, 7); v.text([L / 2, 0.55], 'q', C.c1, 0, -6, 14, true, 'center'); }
    // Einzelkraft: Spitze im Lastpunkt
    if (Fm > 0.01) { v.arrow([xF - Fx * k, -Fy * k], [Fx * k, Fy * k], C.c1, 3.6); v.dot([xF, 0], C.c1, 4); v.text([xF - Fx * k, -Fy * k], 'F', C.c1, -4, -8, 15); }
    // Reaktionen
    const react = (p, f, n) => { if (Math.hypot(f[0], f[1]) > 0.02) { v.arrow(p, V.mul(f, k), C.c4, 3.6); v.text(V.add(p, V.mul(f, k)), n, C.c4, 8, -4, 14); } };
    react([0, 0], [Ax, 0], 'A_x'); react([0, 0], [0, Ay], 'A_y'); react([L, 0], [0, By], 'B_y');
    // Kräftepolygon
    const O = [6.4, 0.8], seq = [['F', [Fx, Fy], C.c1], ['Q', [0, -Q], C.c1], ['A_x', [Ax, 0], C.c4], ['A_y', [0, Ay], C.c4], ['B_y', [0, By], C.c4]];
    let p = O; const ks = 0.38; v.text([5.2, -2.3], 'Kräftepolygon (geschlossen)', C.muted, 0, 0, 12, false);
    seq.forEach(([n, f, c]) => { if (Math.hypot(f[0], f[1]) < 0.02) return; const d = V.mul(f, ks); v.arrow(p, d, c, 2.4, 8); p = V.add(p, d); });
    v.dot(O, C.fg, 3);
    MW.info(infoEl, 'Lagerreaktionen aus ΣF = 0 und ΣM_A = 0', [['ΣF_x = A_x + F cosθ = 0', 'A_x = ' + fmt(Ax, 2) + ' kN'], ['ΣM_A = B_y L + x_F F sinθ − Q L/2 = 0', 'B_y = ' + fmt(By, 2) + ' kN'], ['ΣF_y = A_y + B_y + F sinθ − Q = 0', 'A_y = ' + fmt(Ay, 2) + ' kN'], ['Q = qL', fmt(Q, 2) + ' kN'], ['Kontrolle ΣM_B', fmt(-Ay * L + Fy * (xF - L) + Q * L / 2, 2) + ' kNm']],
      'Unbekannte Vektoren positiv ansetzen: ein negatives Ergebnis heisst, dass die Reaktion in Wirklichkeit entgegengesetzt wirkt (Pfeil wird dann umgedreht). Das Kräftepolygon schliesst sich, weil R = 0.');
  });
  MW.slider(ctl, { label: 'F', min: 0, max: 6, step: 0.5, value: Fm, unit: ' kN', onInput: x => { Fm = x; view.redraw(); } });
  MW.slider(ctl, { label: 'θ', min: -180, max: 0, step: 5, value: th, unit: '°', onInput: x => { th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'x_F', min: 0, max: 4, step: 0.25, value: xF, unit: ' m', onInput: x => { xF = x; view.redraw(); } });
  MW.slider(ctl, { label: 'q', min: 0, max: 3, step: 0.25, value: q, unit: ' kN/m', onInput: x => { q = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('kap6', W))
