"""Widgets zu Kapitel 5 (Woche 6): Leistung einer Einzelkraft, eines Moments, Gesamtleistung."""
from template import build

W = []
ARC = r'''
  // Kreisbogen als Polygon (Weltkoordinaten) mit Pfeilspitze am Ende
  const arcArrow = (v, c, r, a0, a1, col, w) => { const pts = []; const n = 40; for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; pts.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
    v.poly(pts, col, w); const e = pts[n], d = V.sub(pts[n], pts[n - 2]); v.arrow(V.sub(e, V.mul(V.unit(d), 0.12)), V.mul(V.unit(d), 0.14), col, w, 10); };
'''

# ---------------------------------------------------------------- 5.1
W.append(dict(file='5-1-leistung.html', title='Leistung einer Einzelkraft P = F·v und eines Moments P = ω·M',
  sub='Die Leistung einer Kraft F in einem Punkt, der sich mit der Geschwindigkeit v bewegt, ist das Skalarprodukt P = F·v = |F||v| cos α. Nur die Komponente von F in Richtung von v leistet Arbeit. Ein Moment M am rotierenden Körper leistet P = ω·M.',
  hint='Pfeilspitzen von F und v ziehen, oder auf Moment umschalten.', legend=[('--c1', 'Kraft F'), ('--c3', 'Geschwindigkeit v'), ('--c4', 'Komponente F∥ in Richtung v')], js=ARC + r'''
  let F = [1.6, 1.1], vv = [1.9, 0.3], mode = 'kraft', M = 3, om = 2; let sM, sO;
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 3.8, ymin: -2.2, ymax: 2.6 }, v => {
    const C = v.C, O = [0, 0];
    if (mode === 'kraft') {
      v.dot(O, C.fg, 6); v.text(O, 'M', C.fg, -16, 16, 14);
      const u = V.unit(vv), Fp = V.mul(u, V.dot(F, u)), P = V.dot(F, vv) * 10;   // 1 Einheit = 10 N bzw. 1 m/s
      v.line([-3, 0], [3.4, 0], C.line, 1, [2, 4]);
      v.arrow(O, vv, C.c3, 3.2); v.text(V.mul(vv, 1.0), 'v', C.c3, 6, 14, 15);
      v.arrow(O, F, C.c1, 3.2); v.text(V.mul(F, 1.0), 'F', C.c1, 6, -6, 15);
      v.line(F, Fp, C.muted, 1, [4, 3]); v.arrow(O, Fp, C.c4, 5, 11);
      let a = Math.atan2(F[1], F[0]) - Math.atan2(vv[1], vv[0]); if (a > Math.PI) a -= 2 * Math.PI; if (a < -Math.PI) a += 2 * Math.PI; const a0 = Math.atan2(vv[1], vv[0]); const pts = []; for (let i = 0; i <= 20; i++) { const t = a0 + a * i / 20; pts.push([0.6 * Math.cos(t), 0.6 * Math.sin(t)]); } v.poly(pts, C.fg, 1.4);
      const al = Math.acos(Math.max(-1, Math.min(1, V.dot(F, vv) / (V.norm(F) * V.norm(vv) || 1)))) / MW.deg;
      v.text([0.75 * Math.cos(a0 + a / 2), 0.75 * Math.sin(a0 + a / 2)], 'α', C.fg, -4, 5, 14);
      MW.info(infoEl, P > 0.05 ? 'P > 0: die Kraft treibt an (F hat eine Komponente in Richtung v)' : P < -0.05 ? 'P < 0: die Kraft bremst (F hat eine Komponente gegen v)' : 'P = 0: F steht senkrecht auf v, die Kraft leistet nichts',
        [['|F|, |v|', fmt(V.norm(F) * 10, 1) + ' N,  ' + fmt(V.norm(vv), 2) + ' m/s'], ['Winkel α', fmt(al, 0) + '°'], ['P = F·v', fmt(P, 1) + ' W'], ['P = |F||v| cos α', fmt(V.norm(F) * 10 * V.norm(vv) * Math.cos(al * MW.deg), 1) + ' W']],
        'Wirkt die Kraft senkrecht zur Bewegung (z. B. Normalkraft einer reibungsfreien Führung), ist ihre Leistung null.');
    } else {
      v.circle(O, 1.0, C.line, 2, null, 'rgba(120,120,120,0.08)'); v.dot(O, C.fg, 6); v.text(O, 'O', C.fg, 8, 18, 14);
      const sg = Math.sign(M) || 1;   // Moment: Bogen mit Pfeil
      if (Math.abs(M) > 0.05) { arcArrow(v, O, 1.7, sg > 0 ? 0.4 : 4.6, sg > 0 ? 4.6 : 0.4, C.c1, 3); }
      if (Math.abs(M) > 0.05) v.text([1.8, 0.7], 'M', C.c1, 4, -4, 16);
      if (Math.abs(om) > 0.05) { const so = Math.sign(om); arcArrow(v, O, 0.65, so > 0 ? 0.5 : 5.0, so > 0 ? 5.0 : 0.5, C.c3, 3); v.text([0, 0.0], 'ω', C.c3, -5, 5, 16); }
      const P = M * om;
      MW.info(infoEl, P > 0.05 ? 'P > 0: Moment und Drehung gleichsinnig, das Moment treibt an' : P < -0.05 ? 'P < 0: Moment und Drehung gegensinnig, das Moment bremst' : 'P = 0: keine Leistung (M = 0 oder ω = 0)',
        [['M (z-Komponente)', fmt(M, 1) + ' Nm (' + (M >= 0 ? 'gegen den Uhrzeigersinn' : 'im Uhrzeigersinn') + ')'], ['ω (z-Komponente)', fmt(om, 1) + ' 1/s (' + (om >= 0 ? 'gegen den Uhrzeigersinn' : 'im Uhrzeigersinn') + ')'], ['P = ω·M', fmt(P, 1) + ' W']],
        'Gleiche Bilanz wie bei der Kraft: Skalarprodukt aus Rotationsgeschwindigkeit und Moment (hier nur die z-Komponenten, P = ω M).');
    }
  });
  view.handle(() => V.add([0, 0], vv), p => { if (mode === 'kraft') vv = p; });
  view.handle(() => F, p => { if (mode === 'kraft') F = p; });
  MW.select(ctl, 'Modus', [['kraft', 'Einzelkraft: P = F·v'], ['moment', 'Moment: P = ω·M']], x => { mode = x; sM.el.style.display = sO.el.style.display = x === 'moment' ? '' : 'none'; view.redraw(); });
  sM = MW.slider(ctl, { label: 'M', min: -5, max: 5, step: 0.5, value: M, unit: ' Nm', onInput: x => { M = x; view.redraw(); } });
  sO = MW.slider(ctl, { label: 'ω', min: -4, max: 4, step: 0.5, value: om, unit: ' 1/s', onInput: x => { om = x; view.redraw(); } });
  sM.el.style.display = sO.el.style.display = 'none';
'''))

# ---------------------------------------------------------------- 5.2
W.append(dict(file='5-2-gesamtleistung.html', title='Gesamtleistung am starren Körper: P = v<sub>B</sub>·R + ω·M<sub>B</sub>',
  sub='Auf eine starre Platte wirken drei Kräfte. Ihre Gesamtleistung kann man als Summe ΣF<sub>i</sub>·v<sub>i</sub> rechnen oder, viel kürzer, aus der Kinemate {v<sub>B</sub>, ω} im Bezugspunkt B und den Kraftgrössen R = ΣF<sub>i</sub>, M<sub>B</sub> = ΣBA<sub>i</sub>×F<sub>i</sub>. Das Ergebnis ist dasselbe.',
  hint='Kraftpfeile und Angriffspunkte ziehen, Kinemate mit den Reglern setzen.', legend=[('--c1', 'Kräfte F_i'), ('--c3', 'Geschwindigkeiten v_i = v_B + ω × BA_i'), ('--c4', 'Resultierende R in B')], js=r'''
  let A = [[1.6, 0.6], [-1.4, 0.8], [0.4, -0.9]], F = [[0.0, 1.4], [1.0, 0.5], [-1.2, -0.4]], vB = [0.6, 0.0], om = 0.8;
  const cr = (a, b) => a[0] * b[1] - a[1] * b[0];
  const view = MW.View2D(cv, { xmin: -3.6, xmax: 3.6, ymin: -2.3, ymax: 2.5 }, v => {
    const C = v.C, B = [0, 0];
    v.poly([[-2.4, -1.3], [2.4, -1.3], [2.4, 1.3], [-2.4, 1.3]], C.line, 1.5, null, true, 'rgba(120,120,120,0.07)');
    v.dot(B, C.fg, 6); v.text(B, 'B', C.fg, -14, 16, 14);
    let P1 = 0, R = [0, 0], MB = 0; const rows = [];
    F.forEach((f, i) => {
      const r = A[i], vi = V.add(vB, [-om * r[1], om * r[0]]), Pi = (f[0] * vi[0] + f[1] * vi[1]) * 10;   // 1 Einheit Kraft = 10 N, Länge 1 m, Geschwindigkeit 1 m/s
      P1 += Pi; R = V.add(R, f); MB += cr(r, f) * 10;
      v.arrow(r, V.mul(vi, 0.7), C.c3, 2.2, 8); v.arrow(r, f, C.c1, 3); v.dot(r, C.c5, 5); v.text(r, 'A' + (i + 1), C.muted, -16, 16, 12); v.text(V.add(r, f), 'F' + (i + 1), C.c1, 6, -4, 13);
      rows.push(['F' + (i + 1) + '·v' + (i + 1), fmt(Pi, 1) + ' W']);
    });
    v.arrow(B, R, C.c4, 3.5, 11); v.text(R, 'R', C.c4, 6, -4, 14);
    v.arrow(B, V.mul(vB, 0.7), C.c3, 2.6, 8); v.text(V.mul(vB, 0.7), 'v_B', C.c3, 4, 14, 12);
    const P2 = (vB[0] * R[0] + vB[1] * R[1]) * 10 + om * MB;
    MW.info(infoEl, 'Zwei Wege, ein Ergebnis: ΣF_i·v_i = v_B·R + ω M_B', [...rows, ['Summe ΣF_i·v_i', fmt(P1, 1) + ' W'], ['R, M_B', fv(V.mul(R, 10), 1) + ' N,  ' + fmt(MB, 1) + ' Nm'], ['v_B·R + ω M_B', fmt(P2, 1) + ' W']],
      'Die Formel nutzt, dass v_i = v_B + ω × BA_i eine Kinemate ist, siehe Kap. 3.5. Kinemate {v_B, ω} und Dyname {R, M_B} sind dual: Das Skalarprodukt beider ist die Gesamtleistung.');
  });
  F.forEach((_, i) => { view.handle(() => V.add(A[i], F[i]), p => { F[i] = V.sub(p, A[i]); }); view.handle(() => A[i], p => { A[i] = [Math.max(-2.4, Math.min(2.4, p[0])), Math.max(-1.3, Math.min(1.3, p[1]))]; }); });
  MW.slider(ctl, { label: 'v_Bx', min: -2, max: 2, step: 0.1, value: vB[0], unit: ' m/s', onInput: x => { vB[0] = x; view.redraw(); } });
  MW.slider(ctl, { label: 'v_By', min: -2, max: 2, step: 0.1, value: vB[1], unit: ' m/s', onInput: x => { vB[1] = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ω', min: -2, max: 2, step: 0.1, value: om, unit: ' 1/s', onInput: x => { om = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('kap5', W))
