"""Widgets zu Kapitel 4.1 (Woche 5): Zum Kraftbegriff."""
from template import build

W = []

W.append(dict(file='4-1-kraft.html', title='Kräfte als punktgebundene Vektoren (Fig. 4.1, 4.2)',
  sub='Eine Kraft ist ein Vektor mit Angriffspunkt {A<sub>i</sub> | F<sub>i</sub>} und einer physikalischen Wechselwirkung. Kräfte mit demselben Angriffspunkt addieren sich zur Resultierenden R = ΣF<sub>i</sub>. Die Vektorsumme von Kräften an verschiedenen Punkten hat keinen Angriffspunkt und ist daher keine Kraft.',
  hint='Angriffspunkte und Pfeilspitzen ziehen.', legend=[('--c1', 'F_1, F_2, F_3'), ('--c4', 'Resultierende R'), ('--c5', 'Angriffspunkt')], js=r'''
  let A = [[-2.4, 0.6], [0.2, 1.2], [1.8, -0.8]], F = [[1.4, 1.0], [-0.4, 1.6], [0.8, -0.2]], common = false; const AP = [0.0, 0.0], N = 100;   // 1 Längeneinheit = 100 N
  const view = MW.View2D(cv, { xmin: -3.6, xmax: 3.6, ymin: -2.2, ymax: 2.8 }, v => {
    const C = v.C, pt = i => common ? AP : A[i], sum = F.reduce((s, f) => V.add(s, f), [0, 0]);
    let acc = common ? AP : null;
    F.forEach((f, i) => { v.arrow(pt(i), f, C.c1, 2.8); v.dot(pt(i), C.c5, 5); v.text(V.add(pt(i), V.mul(f, 0.5)), 'F' + (i + 1), C.c1, 8, -8, 13); if (!common) v.text(pt(i), 'A' + (i + 1), C.muted, -16, 14, 12); });
    if (common) { v.text(AP, 'A', C.c5, -14, 14, 13); let q = AP; F.forEach(f => { const e = V.add(q, f); v.line(q, e, C.line, 1, [3, 3]); q = e; }); v.arrow(AP, sum, C.c4, 3.6); v.text(V.add(AP, V.mul(sum, 0.5)), 'R', C.c4, 8, 10, 14); }
    else { v.arrow([-3.3, -1.9], sum, C.c4, 2.4, 8); v.text(V.add([-3.3, -1.9], V.mul(sum, 0.5)), 'ΣF', C.c4, 4, 14, 13); }
    const row = (n, f) => [n, fv(V.mul(f, N)) + ' N'];
    MW.info(infoEl, common ? 'Gleicher Angriffspunkt A: R = ΣF_i ist eine Kraft {A | R}' : 'Verschiedene Angriffspunkte: ΣF_i ist ein Vektor, aber keine Kraft', [...F.map((f, i) => row('F' + (i + 1) + ' = (F_x, F_y)', f)), ['|R| bzw. |ΣF|', fmt(V.norm(sum) * N, 0) + ' N']],
      common ? 'Parallelogrammregel: Die Resultierende wirkt im gemeinsamen Angriffspunkt (gestrichelt: Kräftepolygon).' : 'Der Summenvektor (unten links) hat keinen klar definierten Angriffspunkt. Erst Reduktion von Kräftegruppen (Kap. 6) sagt, durch welche Kraft eine Gruppe ersetzt werden darf.', !common);
  });
  F.forEach((_, i) => { view.handle(() => V.add(common ? AP : A[i], F[i]), p => { F[i] = V.sub(p, common ? AP : A[i]); }); view.handle(() => common ? AP : A[i], p => { if (!common) A[i] = p; }); });
  MW.check(ctl, 'gleicher Angriffspunkt', false, x => { common = x; view.redraw(); });
'''))

if __name__ == '__main__':
    print(build('kap4', W))
