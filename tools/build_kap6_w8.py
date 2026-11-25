"""Widget zu Kapitel 6.5 (Woche 8): Reduktion einer räumlichen Kräftegruppe, Zentralachse und Schraube."""
from template import build

W = []

W.append(dict(file='6-5-zentralachse.html', title='Reduktion einer Kräftegruppe: Invarianten, Zentralachse und Schraube', tall=True,
  sub='Jede Kräftegruppe lässt sich auf ihre Dyname {R, M<sub>O</sub>} reduzieren. R ist die 1. Invariante, R · M<sub>O</sub> die 2. Invariante. Auf der Zentralachse ζ ist das Moment minimal und parallel zu R: M<sub>Z</sub> = M<sup>(R)</sup> (Schraube). Ist R · M<sub>O</sub> = 0 (ebene oder parallele Kräfte), bleibt eine Einzelkraft auf ζ übrig (Buch 6.5, Reduktionssatz).',
  hint='Beispiel wählen, Ansicht ziehen (Shift/Rechtsklick verschiebt, Mausrad zoomt).',
  legend=[('--c1', 'Kräfte F_i'), ('--c2', 'Momente (Doppelpfeil)'), ('--c4', 'R'), ('--c5', 'Zentralachse ζ')], js=r'''
  const EX = {
    ueb: { name: 'Übungsheft 3.6 Aufgabe 1 (Quader 2a × 2a × a, a = 1, P = 1)', box: [[0, -2, 0], [2, 0, 1]],
      F: [[[0, -2, 1], [0, 3, 0], 'F₁'], [[2, 0, 0], [0, 0, -2], 'F₂'], [[0, -2, 1], [2.5, 0, 0], 'F₃'], [[2, 0, 1], [0, -1, 0], 'F₄']],
      M: [[[1.2, -1, 0], [3.75, 0, 0], 'M₁'], [[1, -2, 0.5], [0, -2, 0], 'M₂'], [[0.5, -0.6, 1], [0, 0, 1.5], 'M₃']] },
    zp: { name: 'ZP1 2024 A3 (Quader a × a × b, a = 1, b = 1.6, F = 1)', box: [[0, 0, 0], [1, 1, 1.6]],
      F: [[[1, 0, 0], [0, 0, -3], 'F_B'], [[0, 1, 0], [0, 0, 1], 'F_D'], [[1, 0, 1.6], [0, 2, 0], 'F_G']], M: [] },
    eben: { name: 'Ebene Kräftegruppe (alle Kräfte in z = 0)', box: null,
      F: [[[0, 1, 0], [1, 0, 0], 'F₁'], [[1, 0, 0], [0, 2, 0], 'F₂'], [[2, 1, 0], [-1, -1, 0], 'F₃']], M: [] },
    par: { name: 'Parallele Kräfte (alle in −z)', box: null,
      F: [[[0, 0, 0], [0, 0, -1], 'F₁'], [[2, 0, 0], [0, 0, -2], 'F₂'], [[0, 2, 0], [0, 0, -1], 'F₃']], M: [] },
    paar: { name: 'Kräftepaar (R = 0)', box: null,
      F: [[[0, 0, 0], [1.5, 0, 0], 'F'], [[0, 1, 1], [-1.5, 0, 0], '−F']], M: [] },
  };
  let ex = EX.ueb, showZ = true;
  const k = 0.45;
  const view = MW.View3D(cv, { extent: 2.6, yaw: -35, pitch: 22, center: [0.8, -0.4, 0.4] }, v => {
    const C = v.C; v.axes(2.4);
    if (ex.box) { const [p, q] = ex.box, X = [p[0], q[0]], Y = [p[1], q[1]], Z = [p[2], q[2]];
      for (const y of Y) for (const z of Z) v.line([X[0], y, z], [X[1], y, z], C.line, 1.2);
      for (const x of X) for (const z of Z) v.line([x, Y[0], z], [x, Y[1], z], C.line, 1.2);
      for (const x of X) for (const y of Y) v.line([x, y, Z[0]], [x, y, Z[1]], C.line, 1.2); }
    let R = [0, 0, 0], M = [0, 0, 0];
    ex.F.forEach(([p, f, n]) => { R = V.add(R, f); M = V.add(M, V.cross(p, f)); v.arrow(p, V.mul(f, k), C.c1, 2.6, 9); v.dot(p, C.c1, 3); v.text(V.add(p, V.mul(f, k)), n, C.c1, 4, -4, 13); });
    ex.M.forEach(([p, m, n]) => { M = V.add(M, m); const d = V.mul(m, 0.25); v.arrow(p, d, C.c2, 2.2, 9); v.arrow(p, V.mul(d, 0.84), C.c2, 2.2, 9); v.text(V.add(p, d), n, C.c2, 4, -4, 13); });
    const O = [0, 0, 0], Rn = V.norm(R), RM = V.dot(R, M);
    v.arrow(O, V.mul(R, k), C.c4, 3.6, 11); v.text(V.mul(R, k), 'R', C.c4, 6, -4, 15);
    v.arrow(O, V.mul(M, 0.25), C.c2, 3, 10); v.arrow(O, V.mul(M, 0.21), C.c2, 3, 10); v.text(V.mul(M, 0.25), 'M_O', C.c2, 6, -4, 14);
    const rows = [['R (1. Invariante)', fv(R, 2)], ['M_O', fv(M, 2)], ['R · M_O (2. Invariante)', fmt(RM, 3)]];
    let head, note;
    if (Rn < 1e-6) { head = 'R = 0: die Gruppe ist ein Kräftepaar, keine Zentralachse';
      note = 'Das Moment ist dann in jedem Punkt gleich (M_P = M_O + PO × R = M_O). Es gibt keine Einzelkraft, die die Gruppe ersetzt.'; }
    else { const MR = V.mul(R, RM / (Rn * Rn)), Z = V.mul(V.cross(R, M), 1 / (Rn * Rn)), u = V.mul(R, 1 / Rn);
      if (showZ) { v.line(V.sub(Z, V.mul(u, 3.5)), V.add(Z, V.mul(u, 3.5)), C.c5, 1.6, [7, 5]); v.text(V.add(Z, V.mul(u, 2.6)), 'ζ', C.c5, 6, 0, 16);
        v.dot(Z, C.c5, 5); v.text(Z, 'Z₀', C.c5, -22, 16, 14); v.line(O, Z, C.muted, 1, [2, 3]);
        v.arrow(Z, V.mul(R, k), C.c4, 3.6, 11);
        if (V.norm(MR) > 1e-6) { v.arrow(Z, V.mul(MR, 0.25), C.c2, 3, 10); v.arrow(Z, V.mul(MR, 0.21), C.c2, 3, 10); v.text(V.add(Z, V.mul(MR, 0.25)), 'M^(R)', C.c2, 6, 10, 13); } }
      rows.push(['M^(R) = (R·M_O / |R|²) R', fv(MR, 3)], ['|M^(R)|', fmt(V.norm(MR), 3)], ['Z₀ = (R × M_O) / |R|²', fv(Z, 3)], ['ζ', 'Z₀ + λ R']);
      if (Math.abs(RM) < 1e-9) { head = 'R · M_O = 0: Reduktion auf eine Einzelkraft {Z | R} auf ζ';
        note = 'Das gilt immer für ebene Kräftegruppen und für parallele Kräfte. Bei parallelen gleich gerichteten Kräften ist der Kräftemittelpunkt ein Punkt auf ζ (Kap. 7).'; }
      else { head = 'R · M_O ≠ 0: Schraube {R, M^(R)} auf der Zentralachse';
        note = 'In jedem Punkt Z von ζ ist das Moment M^(R) parallel zu R und so klein wie möglich. Kontrolle: M_Z0 = M_O + Z₀O × R = ' + fv(V.add(M, V.cross(V.mul(Z, -1), R)), 3) + '.'; } }
    MW.info(infoEl, head, rows, note);
  });
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([key, e]) => [key, e.name]), x => { ex = EX[x]; view.redraw(); });
  MW.check(ctl, 'Zentralachse zeigen', true, x => { showZ = x; view.redraw(); });
  MW.button(ctl, 'Ansicht zurücksetzen', () => view.resetView());
'''))

if __name__ == '__main__':
    print(build('kap6', W))
