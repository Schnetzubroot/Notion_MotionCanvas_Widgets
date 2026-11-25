"""Widgets zu Kapitel 7 (Woche 8): Streckenlast und Kräftemittelpunkt, Schwerpunkt zusammengesetzter Flächen."""
from template import build

W = []

# ---------------------------------------------------------------- 7.2
W.append(dict(file='7-2-streckenlast.html', title='Linienverteilte Kraft: Resultierende R und Kräftemittelpunkt x<sub>S</sub>',
  sub='Für eine Linienlast q(x) auf [0, L] gilt R = ∫ q dx (Fläche unter q) und x<sub>S</sub> = ∫ x q dx / ∫ q dx (Schwerpunkt dieser Fläche, Buch Gl. 7.7–7.10). Uniform: R = q<sub>0</sub>L bei L/2. Dreieck: R = q<sub>0</sub>L/2 bei 2L/3. Ein Trapez zerlegt man in Rechteck und Dreieck.',
  hint='q_A, q_B und L einstellen. „Lagerkräfte“ zeigt Festlager A und Loslager B.',
  legend=[('--c1', 'Linienlast q(x)'), ('--c3', 'Teilresultierende'), ('--c4', 'Resultierende R'), ('--c5', 'Lagerkräfte')], js=r'''
  let qA = 1, qB = 2.5, L = 4, split = true, sup = false;
  const view = MW.View2D(cv, { xmin: -0.8, xmax: 7.0, ymin: -2.6, ymax: 2.4 }, v => {
    const C = v.C, s = 0.6, qmin = Math.min(qA, qB), R = L * (qA + qB) / 2;
    v.poly([[0, 0], [L, 0]], C.fg, 6);
    const top = x => (qA + (qB - qA) * x / L) * s;
    v.poly([[0, 0], [0, top(0)], [L, top(L)], [L, 0]], C.c1, 1.6, null, true, 'rgba(120,140,200,0.12)');
    const n = Math.max(4, Math.round(L * 2));
    for (let i = 0; i <= n; i++) { const x = L * i / n, h = top(x); if (h > 0.05) v.arrow([x, h + 0.02], [0, -h], C.c1, 1.4, 7); }
    v.text([0, top(0)], 'q_A', C.c1, -8, -8, 13, true, 'right'); v.text([L, top(L)], 'q_B', C.c1, 8, -8, 13);
    let xS = NaN;
    if (R > 1e-9) xS = L * (qA + 2 * qB) / (3 * (qA + qB));
    const rows = [['R = L (q_A + q_B)/2', fmt(R, 2) + ' kN']];
    const yb = -1.7, hR = 1.0;
    if (isFinite(xS)) v.poly([[0, yb], [L, yb]], C.muted, 4);
    v.text([0, yb], 'Ersatzbild', C.muted, -4, 22, 12, false);
    if (split) {
      const R1 = qmin * L, R2 = Math.abs(qB - qA) * L / 2, x1 = L / 2, x2 = qB >= qA ? 2 * L / 3 : L / 3;
      if (qmin > 0.01) v.line([0, qmin * s], [L, qmin * s], C.c3, 1, [4, 3]);
      if (R1 > 0.01) { v.arrow([x1, yb + hR], [0, -hR], C.c3, 2.2, 9); v.text([x1, yb + hR], 'R₁', C.c3, 4, -4, 12); }
      if (R2 > 0.01) { v.arrow([x2, yb + hR], [0, -hR], C.c3, 2.2, 9); v.text([x2, yb + hR], 'R₂', C.c3, 4, -4, 12); }
      rows.push(['Rechteck: R₁ = q_min L bei L/2', fmt(R1, 2) + ' kN bei ' + fmt(x1, 2) + ' m'], ['Dreieck: R₂ = |q_B − q_A| L/2 bei ' + (qB >= qA ? '2L/3' : 'L/3'), fmt(R2, 2) + ' kN bei ' + fmt(x2, 2) + ' m']);
    }
    if (isFinite(xS)) { v.arrow([xS, yb + hR + 0.1], [0, -hR - 0.1], C.c4, 3.6, 11); v.text([xS, yb + hR + 0.1], 'R', C.c4, 8, 0, 15); v.dot([xS, yb], C.c4, 5);
      v.line([0, yb - 0.35], [xS, yb - 0.35], C.c4, 1.2); v.text([xS / 2, yb - 0.35], 'x_S', C.c4, 0, 16, 13, true, 'center');
      v.line([xS, 0], [xS, yb], C.c4, 1, [3, 3]);
      rows.push(['x_S = L (q_A + 2 q_B) / (3 (q_A + q_B))', fmt(xS, 3) + ' m'], ['x_S / L', fmt(xS / L, 3)]); }
    if (sup && isFinite(xS)) {
      v.poly([[0, 0], [-0.22, -0.4], [0.22, -0.4]], C.fg, 2); v.poly([[L, 0], [L - 0.22, -0.36], [L + 0.22, -0.36]], C.fg, 2); v.line([L - 0.3, -0.48], [L + 0.3, -0.48], C.fg, 2);
      const By = R * xS / L, Ay = R - By;
      v.arrow([0, -0.95], [0, 0.5], C.c5, 2.8, 9); v.text([0, -0.95], 'A_y', C.c5, 6, 14, 13);
      v.arrow([L, -0.95], [0, 0.5], C.c5, 2.8, 9); v.text([L, -0.95], 'B_y', C.c5, 6, 14, 13);
      rows.push(['ΣM_A: B_y L − R x_S = 0', 'B_y = ' + fmt(By, 2) + ' kN'], ['ΣF_y: A_y + B_y − R = 0', 'A_y = ' + fmt(Ay, 2) + ' kN']); }
    v.text([0, 0], 'A', C.muted, -16, 18, 14); v.text([L, 0], 'B', C.muted, 8, 18, 14);
    const tri = qA < 1e-9 || qB < 1e-9, uni = Math.abs(qA - qB) < 1e-9;
    MW.info(infoEl, uni ? 'Uniform: x_S = L/2' : tri ? 'Dreieck: R im Drittelpunkt auf der hohen Seite' : 'Trapez = Rechteck + Dreieck', rows,
      'Die Resultierende greift im Flächenschwerpunkt der Lastfläche an. Für Lagerkräfte darf man die Linienlast durch R in x_S ersetzen, für innere Kräfte (Kap. 14) nicht.');
  });
  MW.slider(ctl, { label: 'q_A', min: 0, max: 3, step: 0.25, value: qA, unit: ' kN/m', onInput: x => { qA = x; view.redraw(); } });
  MW.slider(ctl, { label: 'q_B', min: 0, max: 3, step: 0.25, value: qB, unit: ' kN/m', onInput: x => { qB = x; view.redraw(); } });
  MW.slider(ctl, { label: 'L', min: 2, max: 6, step: 0.5, value: L, unit: ' m', onInput: x => { L = x; view.redraw(); } });
  MW.check(ctl, 'in Rechteck + Dreieck zerlegen', true, x => { split = x; view.redraw(); });
  MW.check(ctl, 'Lagerkräfte', false, x => { sup = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 7.3
W.append(dict(file='7-3-schwerpunkt.html', title='Schwerpunkt einer zusammengesetzten Fläche', tall=True,
  sub='Für Teilflächen A<sub>i</sub> mit Teilschwerpunkten (x<sub>i</sub>, y<sub>i</sub>) gilt x<sub>S</sub> = Σ A<sub>i</sub>x<sub>i</sub> / Σ A<sub>i</sub>, y<sub>S</sub> = Σ A<sub>i</sub>y<sub>i</sub> / Σ A<sub>i</sub> (Buch Gl. 7.23 mit G<sub>i</sub> ∝ A<sub>i</sub> bei homogener Platte). Löcher zählen mit negativer Fläche. Dreht man die Schwerkraft, drehen sich alle Wirkungslinien um denselben Punkt S.',
  hint='Abmessungen einstellen, Loch ziehen, Richtung der Schwerkraft drehen.',
  legend=[('--c1', 'Rechteck 1'), ('--c3', 'Rechteck 2'), ('--c2', 'Loch (negativ)'), ('--c4', 'Schwerpunkt S, Gesamtgewicht')], js=r'''
  let b1 = 4, h1 = 1, b2 = 1, h2 = 3, r = 0.35, hole = [2.6, 0.5], useHole = true, gam = 0;
  const view = MW.View2D(cv, { xmin: -1.5, xmax: 6.5, ymin: -1.5, ymax: 5.0 }, v => {
    const C = v.C;
    const parts = [
      { n: 'Rechteck 1', A: b1 * h1, c: [b1 / 2, h1 / 2], col: C.c1 },
      { n: 'Rechteck 2', A: b2 * h2, c: [b2 / 2, h1 + h2 / 2], col: C.c3 } ];
    const inside = useHole && hole[0] - r >= 0 && hole[0] + r <= b1 && hole[1] - r >= 0 && hole[1] + r <= h1 || useHole && hole[0] - r >= 0 && hole[0] + r <= b2 && hole[1] - r >= h1 && hole[1] + r <= h1 + h2;
    if (useHole) parts.push({ n: 'Loch', A: -Math.PI * r * r, c: hole, col: C.c2 });
    v.poly([[0, 0], [b1, 0], [b1, h1], [0, h1]], C.c1, 2, null, true, 'rgba(90,120,220,0.14)');
    v.poly([[0, h1], [b2, h1], [b2, h1 + h2], [0, h1 + h2]], C.c3, 2, null, true, 'rgba(60,170,110,0.14)');
    if (useHole) v.circle(hole, r, C.c2, 2, [4, 3], C.bg);
    let A = 0, Sx = 0, Sy = 0; parts.forEach(p => { A += p.A; Sx += p.A * p.c[0]; Sy += p.A * p.c[1]; });
    const S = [Sx / A, Sy / A], g = [Math.sin(gam * MW.deg), -Math.cos(gam * MW.deg)];
    parts.forEach(p => { v.dot(p.c, p.col, 4); v.line(V.sub(p.c, V.mul(g, 6)), V.add(p.c, V.mul(g, 6)), p.col, 0.8, [2, 4]);
      v.arrow(p.c, V.mul(g, 0.25 * Math.sign(p.A) * Math.sqrt(Math.abs(p.A))), p.col, 2, 8); });
    v.line(V.sub(S, V.mul(g, 7)), V.add(S, V.mul(g, 7)), C.c4, 1.6, [7, 4]);
    v.arrow(S, V.mul(g, 0.35 * Math.sqrt(A)), C.c4, 3.6, 11); v.dot(S, C.c4, 6); v.text(S, 'S', C.c4, 10, -8, 16);
    const rows = parts.map(p => [p.n + ': A = ' + fmt(p.A, 3), '(x, y) = (' + fmt(p.c[0], 3) + ', ' + fmt(p.c[1], 3) + ')']);
    rows.push(['Σ A_i', fmt(A, 3)], ['Σ A_i x_i', fmt(Sx, 3)], ['Σ A_i y_i', fmt(Sy, 3)], ['S = (x_S, y_S)', '(' + fmt(S[0], 3) + ', ' + fmt(S[1], 3) + ')']);
    const outside = !(S[0] >= 0 && S[1] >= 0 && (S[1] <= h1 && S[0] <= b1 || S[1] >= h1 && S[1] <= h1 + h2 && S[0] <= b2));
    MW.info(infoEl, useHole && !inside ? 'Das Loch muss ganz in der Fläche liegen' : outside ? 'S liegt ausserhalb des Materials' : 'Gesamtschwerpunkt aus den Teilschwerpunkten',
      rows, 'Drehen Sie die Schwerkraft: Die Wirkungslinie der Resultierenden geht immer durch S. Genau das definiert den Kräftemittelpunkt (Buch 7.1). ' + (outside ? 'Wie bei der Hohlkugel braucht S nicht im Körper zu liegen (Buch 7.3).' : ''), useHole && !inside);
  });
  view.handle(() => hole, p => { hole = p; });
  MW.slider(ctl, { label: 'b₁', min: 1, max: 6, step: 0.25, value: b1, onInput: x => { b1 = x; view.redraw(); } });
  MW.slider(ctl, { label: 'h₁', min: 0.25, max: 2, step: 0.25, value: h1, onInput: x => { h1 = x; view.redraw(); } });
  MW.slider(ctl, { label: 'b₂', min: 0.25, max: 3, step: 0.25, value: b2, onInput: x => { b2 = x; view.redraw(); } });
  MW.slider(ctl, { label: 'h₂', min: 0, max: 4, step: 0.25, value: h2, onInput: x => { h2 = x; view.redraw(); } });
  MW.slider(ctl, { label: 'Loch r', min: 0.1, max: 0.5, step: 0.05, value: r, onInput: x => { r = x; view.redraw(); } });
  MW.check(ctl, 'Loch', true, x => { useHole = x; view.redraw(); });
  MW.slider(ctl, { label: 'Richtung der Schwerkraft', min: -90, max: 90, step: 5, value: gam, unit: '°', onInput: x => { gam = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('kap7', W))
