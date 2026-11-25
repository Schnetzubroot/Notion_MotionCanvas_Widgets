"""Widgets zu Kapitel 9 (Woche 9): Standfestigkeit, Balken mit Auflagern, Dreigelenkbogen."""
from template import build

W = []

GAUSS = r'''
  const solve = (A, b) => { const n = b.length, M = A.map((r, i) => [...r, b[i]]);
    for (let c = 0; c < n; c++) { let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      if (Math.abs(M[p][c]) < 1e-10) return null; [M[c], M[p]] = [M[p], M[c]];
      for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; } }
    return M.map((r, i) => r[n] / r[i]); };
  const cr = (a, b) => a[0] * b[1] - a[1] * b[0];
  const fixSup = (v, p, C) => { v.poly([p, V.add(p, [-0.2, -0.36]), V.add(p, [0.2, -0.36])], C.fg, 2, null, true, 'rgba(120,120,120,0.15)'); v.line(V.add(p, [-0.34, -0.36]), V.add(p, [0.34, -0.36]), C.fg, 2); v.dot(p, C.bg, 4); v.dot(p, C.fg, 4, true); };
  const losSup = (v, p, C) => { v.poly([p, V.add(p, [-0.2, -0.32]), V.add(p, [0.2, -0.32])], C.fg, 2, null, true, 'rgba(120,120,120,0.15)'); v.line(V.add(p, [-0.34, -0.42]), V.add(p, [0.34, -0.42]), C.fg, 2); v.dot(p, C.bg, 4); v.dot(p, C.fg, 4, true); };
'''

# ---------------------------------------------------------------- 9.1
W.append(dict(file='9-1-standfestigkeit.html', title='Standfestigkeit: Klotz mit Kräftepaar (Übungsheft Aufgabe 4.1)',
  sub='Würfel (Kante a, Gewicht G) auf reibungsfreier Ebene, oben die Kraft F (nach oben positiv) und ein Kräftepaar aus zwei Kräften 2F. Gleichgewicht: N = G − F und e = (a/2)(G − 3F)/(G − F). Standfest, solange N > 0 und 0 < e < a, also −G < F < G/3.',
  hint='F einstellen. Die Normalkraft N wandert; verlässt sie die Standfläche, kippt der Klotz.',
  legend=[('--c1', 'Lasten'), ('--c4', 'Normalkraft N'), ('--c5', 'Standfläche')], js=r'''
  let f = 0.2;
  const a = 2, G = 1;
  const view = MW.View2D(cv, { xmin: -1.6, xmax: 3.6, ymin: -1.3, ymax: 3.4 }, v => {
    const C = v.C, k = 0.9, F = f * G, N = G - F, e = (a / 2) * (G - 3 * F) / (G - F);
    v.line([-1.4, 0], [3.4, 0], C.fg, 2.2); for (let i = 0; i < 20; i++) v.line([-1.3 + i * 0.24, 0], [-1.42 + i * 0.24, -0.14], C.muted, 1);
    v.line([0, -0.06], [a, -0.06], C.c5, 6);
    v.poly([[0, 0], [a, 0], [a, a], [0, a]], C.fg, 2, null, true, 'rgba(120,120,120,0.10)');
    const O = [a / 2, a / 2]; v.dot(O, C.fg, 4); v.text(O, 'O', C.fg, 8, -6, 13);
    v.arrow(O, [0, -G * k], C.c1, 3, 10); v.text(V.add(O, [0, -G * k]), 'G', C.c1, 6, 6, 14);
    if (Math.abs(F) > 0.01) { const t = [a / 2, a]; if (F > 0) v.arrow(t, [0, F * k], C.c1, 3, 10); else v.arrow(V.sub(t, [0, F * k]), [0, F * k], C.c1, 3, 10); v.text(V.add(t, [0, Math.abs(F) * k]), 'F', C.c1, 6, 0, 14);
      const c1 = [-2 * F * k * 0.5, 0], c2 = [2 * F * k * 0.5, 0];
      v.arrow(V.sub([a, a], c1), c1, C.c1, 2.6, 9); v.arrow(V.sub([0, a / 2], c2), c2, C.c1, 2.6, 9);
      v.text([a, a], '2F', C.c1, 6, -10, 13); v.text([0, a / 2], '2F', C.c1, -34, -8, 13); }
    const lift = N <= 0, tip = e < 0 || e > a;
    if (!lift) { const xe = Math.max(-1.2, Math.min(3.2, e)); v.arrow([xe, -0.95], [0, Math.min(0.9, N * k)], tip ? C.warn : C.c4, 3, 10); v.text([xe, -0.95], 'N', tip ? C.warn : C.c4, 6, 14, 14);
      v.line([0, -0.25], [xe, -0.25], C.c4, 1); v.text([xe / 2, -0.25], 'e', C.c4, 0, 16, 13, true, 'center'); }
    v.text([0, 0], 'A', C.muted, -14, 16, 13); v.text([a, 0], 'B', C.muted, 6, 16, 13);
    const head = lift ? 'N ≤ 0: der Klotz hebt ab (F ≥ G)' : e < 0 ? 'e < 0: N läge links von A, der Klotz kippt um A' : e > a ? 'e > a: N läge rechts von B, der Klotz kippt um B' : 'Standfest: N > 0 und 0 < e < a';
    MW.info(infoEl, head, [['F / G', fmt(f, 2)], ['ΣF_y: N + F − G = 0', 'N = ' + fmt(N, 3) + ' G'], ['ΣM_O: a F − N (a/2 − e) = 0', 'e = ' + (lift ? '–' : fmt(e / a, 3) + ' a')], ['Bedingung (5): kein Kippen um A', 'F < G/3'], ['Bedingung (6): kein Kippen um B', 'F > −G']],
      'Die x-Komponentenbedingung ist trivial (2F − 2F = 0), deshalb bleiben 2 Gleichungen für die 2 Unbekannten N und e (Übungsheft S. 56–57).', lift || tip);
  });
  MW.slider(ctl, { label: 'F / G', min: -1.4, max: 0.9, step: 0.02, value: f, onInput: x => { f = x; view.redraw(); } });
  MW.button(ctl, 'F = G/3', () => { f = 1 / 3; view.redraw(); });
'''))

# ---------------------------------------------------------------- 9.4 Dreigelenkbogen
W.append(dict(file='9-4-dreigelenkbogen.html', title='Dreigelenkbogen: Zerlegen macht ihn statisch bestimmt', tall=True,
  sub='Halbkreisbogen (Radius R) mit Festlagern in A und B (Übungsheft Abb. 5.1–5.3). Am Ganzen gibt es 4 Lagerunbekannte, aber nur 3 Gleichungen. Mit einem Gelenk C im Scheitel zerlegt man in zwei Teile: 6 Unbekannte (A<sub>x</sub>, A<sub>y</sub>, B<sub>x</sub>, B<sub>y</sub>, C<sub>x</sub>, C<sub>y</sub>), 2 × 3 Gleichungen. Der unbelastete Teil ist eine Pendelstütze: seine Kräfte zeigen genau auf das Gelenk.',
  hint='Last F auf dem Bogen verschieben (Punkt ziehen oder Regler), Richtung drehen, Lagerung umschalten.',
  legend=[('--c1', 'Last F'), ('--c4', 'Lagerkräfte'), ('--c3', 'Gelenkkraft in C'), ('--c5', 'Wirkungslinien')], js=GAUSS + r'''
  const R = 1.5, A = [0, 0], B = [2 * R, 0], Cg = [R, R];
  let th = 135, be = -90, mode = 'drei', sep = true;
  const onArc = t => [R + R * Math.cos(t * MW.deg), R * Math.sin(t * MW.deg)];
  const view = MW.View2D(cv, { xmin: -1.4, xmax: 4.6, ymin: -1.1, ymax: 3.0 }, v => {
    const C = v.C, P = onArc(th), F = [Math.cos(be * MW.deg), Math.sin(be * MW.deg)], k = 0.75;
    const left = th >= 90, gap = mode === 'drei' && sep ? 0.25 : 0;
    const shI = [-gap, 0], shII = [gap, 0];
    v.arc(V.add([R, 0], shI), R, Math.PI / 2, Math.PI, C.fg, 5); v.arc(V.add([R, 0], shII), R, 0, Math.PI / 2, C.fg, 5);
    fixSup(v, V.add(A, shI), C); (mode === 'los' ? losSup : fixSup)(v, V.add(B, shII), C);
    if (mode === 'drei') { v.dot(V.add(Cg, shI), C.bg, 5); v.dot(V.add(Cg, shI), C.fg, 5, true); if (gap) { v.dot(V.add(Cg, shII), C.bg, 5); v.dot(V.add(Cg, shII), C.fg, 5, true); } }
    v.text(V.add(A, shI), 'A', C.muted, -18, 4, 14); v.text(V.add(B, shII), 'B', C.muted, 10, 4, 14); v.text(Cg, 'C', C.muted, 0, -12, 14, true, 'center');
    v.text([0.2, 1.6], 'I', C.muted, 0, 0, 15); v.text([2.8, 1.6], 'II', C.muted, 0, 0, 15);
    const Pd = V.add(P, left ? shI : shII);
    v.arrow(V.sub(Pd, V.mul(F, k)), V.mul(F, k), C.c1, 3.4, 11); v.text(V.sub(Pd, V.mul(F, k)), 'F', C.c1, 6, -6, 15); v.dot(Pd, C.c1, 4);
    const kr = 1.6, draw = (p, f, n, col) => { if (Math.hypot(f[0], f[1]) < 1e-4) return; v.arrow(p, V.mul(f, kr), col, 3, 10); v.text(V.add(p, V.mul(f, kr)), n, col, 6, -4, 13); };
    let rows = [], head, note, warn = false;
    if (mode === 'zwei') { head = '2 Festlager ohne Gelenk: 4 Unbekannte, 3 Gleichungen, einfach statisch unbestimmt'; warn = true;
      note = 'A_x und B_x lassen sich ohne Verformungsbetrachtung nicht trennen (vgl. Buch Fig. 9.16). Mit dem Gelenk C wird das System wieder statisch bestimmt.';
      const By = -cr(P, F) / (2 * R), Ay = -F[1] - By; rows = [['ΣM_A: 2R B_y + (AP × F)_z = 0', 'B_y = ' + fmt(By, 3) + ' F'], ['ΣF_y', 'A_y = ' + fmt(Ay, 3) + ' F'], ['ΣF_x: A_x + B_x + F_x = 0', 'A_x, B_x einzeln unbestimmt']]; }
    else if (mode === 'los') { const By = -cr(P, F) / (2 * R), Ay = -F[1] - By, Ax = -F[0];
      draw(A, [Ax, 0], 'A_x', C.c4); draw(A, [0, Ay], 'A_y', C.c4); draw(B, [0, By], 'B_y', C.c4);
      head = 'Zweigelenkbogen (A fest, B Loslager): 3 Unbekannte, 3 Gleichungen, bestimmt';
      note = 'Statisch bestimmt, aber im echten (verformbaren) Bogen können grosse Verformungen auftreten. Deshalb B fest und dafür ein Gelenk in C (Übungsheft 5.3).';
      rows = [['A_x', fmt(Ax, 3) + ' F'], ['A_y', fmt(Ay, 3) + ' F'], ['B_y', fmt(By, 3) + ' F']]; }
    else {
      const FI = left ? F : [0, 0], FII = left ? [0, 0] : F;
      // x = [Ax, Ay, Bx, By, Cx, Cy], C = Kraft von II auf I
      const M = [[1, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1], [0, 0, 0, 0, -(Cg[1] - A[1]), Cg[0] - A[0]],
                 [0, 0, 1, 0, -1, 0], [0, 0, 0, 1, 0, -1], [0, 0, 0, 0, (Cg[1] - B[1]), -(Cg[0] - B[0])]];
      const b = [-FI[0], -FI[1], -cr(V.sub(P, A), FI), -FII[0], -FII[1], -cr(V.sub(P, B), FII)];
      const x = solve(M, b); const [Ax, Ay, Bx, By, Cx, Cy] = x;
      draw(V.add(A, shI), [Ax, Ay], 'A', C.c4); draw(V.add(B, shII), [Bx, By], 'B', C.c4);
      if (sep) { draw(V.add(Cg, shI), [Cx, Cy], 'C', C.c3); draw(V.add(Cg, shII), [-Cx, -Cy], '−C', C.c3); }
      const un = left ? [V.add(B, shII), V.add(Cg, shII)] : [V.add(A, shI), V.add(Cg, shI)];
      const u = V.unit(V.sub(un[1], un[0])); v.line(V.sub(un[0], V.mul(u, 0.6)), V.add(un[1], V.mul(u, 2.5)), C.c5, 1.4, [6, 4]);
      // Dreikräfte-Schnittpunkt am belasteten Teil
      const ld = left ? V.add(A, shI) : V.add(B, shII), fsup = left ? [Ax, Ay] : [Bx, By];
      const cA = V.add(Cg, left ? shI : shII), d1 = V.unit(fsup), d2 = F; const den = cr(d1, d2);
      if (Math.abs(den) > 1e-6) { const t = cr(V.sub(Pd, ld), d2) / den, Q = V.add(ld, V.mul(d1, t));
        if (Math.hypot(Q[0] - 1.5, Q[1] - 1) < 6) { v.line(ld, Q, C.c5, 1.2, [3, 3]); v.line(Pd, Q, C.c5, 1.2, [3, 3]); v.line(cA, Q, C.c5, 1.2, [3, 3]); v.dot(Q, C.c5, 4); } }
      head = 'Dreigelenkbogen: 6 Unbekannte, 6 Gleichungen, statisch bestimmt';
      note = 'Teil ' + (left ? 'II' : 'I') + ' ist unbelastet und nur in zwei Gelenken gehalten, also eine Pendelstütze: die Kraft wirkt längs ' + (left ? 'BC' : 'AC') + '. Am belasteten Teil schneiden sich die drei Wirkungslinien (Lagerkraft, Last, Gelenkkraft) in einem Punkt. Schneller Weg: ΣM_C am unbelasteten Teil gibt die Richtung, dann reichen die Gleichungen am Ganzen.';
      rows = [['A = (A_x, A_y)', '(' + fmt(Ax, 3) + ', ' + fmt(Ay, 3) + ') F'], ['B = (B_x, B_y)', '(' + fmt(Bx, 3) + ', ' + fmt(By, 3) + ') F'], ['C (von II auf I)', '(' + fmt(Cx, 3) + ', ' + fmt(Cy, 3) + ') F'],
        ['Kontrolle ΣF_x am Ganzen', fmt(Ax + Bx + F[0], 6)], ['Kontrolle ΣF_y am Ganzen', fmt(Ay + By + F[1], 6)]]; }
    MW.info(infoEl, head, rows, note, warn);
  });
  view.handle(() => V.add(onArc(th), th >= 90 ? [-(mode === 'drei' && sep ? 0.25 : 0), 0] : [(mode === 'drei' && sep ? 0.25 : 0), 0]), p => { const t = Math.atan2(p[1], p[0] - R) / MW.deg; th = Math.max(2, Math.min(178, Math.round(t))); ts.set(th); });
  const ts = MW.slider(ctl, { label: 'Lage θ der Last', min: 2, max: 178, step: 1, value: th, unit: '°', onInput: x => { th = x; view.redraw(); } });
  MW.slider(ctl, { label: 'Richtung β', min: -180, max: 180, step: 5, value: be, unit: '°', onInput: x => { be = x; view.redraw(); } });
  MW.select(ctl, 'Lagerung', [['drei', 'Dreigelenkbogen (A, B fest, Gelenk C)'], ['los', 'Zweigelenkbogen (B Loslager)'], ['zwei', 'Bogen starr, A und B fest']], x => { mode = x; view.redraw(); });
  MW.check(ctl, 'in C auseinanderziehen', true, x => { sep = x; view.redraw(); });
'''))

if __name__ == '__main__':
    print(build('kap9', W))
