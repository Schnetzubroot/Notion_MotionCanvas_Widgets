"""Widgets zu Kapitel 4.3–4.4 (Woche 6): Reaktionsprinzip und Freischneiden, Kraftdichten."""
from template import build

W = []

# ---------------------------------------------------------------- 4.3
W.append(dict(file='4-3-freischnitt.html', title='Reaktionsprinzip und Freischneiden: innere und äussere Kräfte',
  sub='Klotz A liegt auf Klotz B, B auf dem Boden. Wählen Sie das System, das Sie freischneiden. Nur die äusseren Kräfte (die Kräfte der Umgebung auf das System) bestimmen das Gleichgewicht. Kräfte zwischen zwei Teilen desselben Systems sind innere Kräfte und treten paarweise mit F<sub>AB</sub> = −F<sub>BA</sub> auf (Reaktionsprinzip).',
  hint='System wählen, Massen ändern.', legend=[('--c1', 'äussere Kräfte'), ('--c3', 'innere Kräfte (heben sich paarweise auf)'), ('--c5', 'Systemgrenze')], js=r'''
  let mA = 2, mB = 3, sys = 'A'; const g = 10, S = 0.025;
  const view = MW.View2D(cv, { xmin: -3.8, xmax: 3.8, ymin: -0.9, ymax: 3.1 }, v => {
    const C = v.C, NAB = mA * g, Fl = (mA + mB) * g;
    // Körper
    v.poly([[-3.4, 0], [3.4, 0]], C.fg, 2.5);
    for (let x = -3.4; x < 3.4; x += 0.3) v.line([x, 0], [x - 0.2, -0.2], C.muted, 1);
    v.poly([[-1.3, 0], [1.3, 0], [1.3, 1], [-1.3, 1]], C.line, 1.5, null, true, C.fill);
    v.poly([[-0.8, 1], [0.8, 1], [0.8, 1.8], [-0.8, 1.8]], C.line, 1.5, null, true, C.fill);
    v.text([-1.2, 0.5], 'B', C.fg, 0, 5, 16); v.text([0, 1.4], 'A', C.fg, -5, 5, 16);
    // Systemgrenze
    const box = sys === 'A' ? [[-0.95, 0.95], [0.95, 0.95], [0.95, 1.95], [-0.95, 1.95]] : sys === 'B' ? [[-1.45, -0.12], [1.45, -0.12], [1.45, 1.0], [-1.45, 1.0]] : [[-1.45, -0.12], [1.45, -0.12], [1.45, 1.95], [-1.45, 1.95]];
    if (sys === 'B') { box[2] = [1.45, 0.96]; box[3] = [-1.45, 0.96]; }
    v.poly(box, C.c5, 2, [6, 4], true);
    const ext = [], int = [];
    const WA = ['m_A g', [0, 1.4], [0, -mA * g * S]], WB = ['m_B g', [-0.7, 0.5], [0, -mB * g * S]];
    const BA = ['N_BA', [-0.35, 0.98], [0, NAB * S]], AB = ['N_AB', [0.35, 1.02], [0, -NAB * S]], FL = ['N_Boden', [0.7, 0], [0, Fl * S]];
    if (sys === 'A') { ext.push(WA, BA); }
    if (sys === 'B') { ext.push(WB, AB, FL); }
    if (sys === 'AB') { ext.push(WA, WB, FL); int.push(BA, AB); }
    const draw = (l, col) => l.forEach(([n, p, f]) => { v.arrow(p, f, col, 3); v.text(V.add(p, V.mul(f, 0.5)), n.replace(/_(\w+)/, '$1'), col, 8, 4, 12); });
    draw(ext, C.c1); draw(int, C.c3);
    const sum = ext.reduce((s, e) => s + e[2][1], 0) / S;
    const rows = ext.map(e => [e[0].replace('_', '') + ' (y)', fmt(e[2][1] / S, 0) + ' N']);
    rows.push(['Σ F_y (äussere)', fmt(sum, 0) + ' N']);
    MW.info(infoEl, sys === 'AB' ? 'System A+B: N_AB und N_BA sind innere Kräfte und fallen heraus' : sys === 'A' ? 'System A: der Kontakt mit B ist eine äussere Kraft N_BA' : 'System B: der Kontakt mit A ist eine äussere Kraft N_AB',
      [...rows, ['Reaktionsprinzip', 'N_BA = ' + fmt(NAB, 0) + ' N nach oben, N_AB = ' + fmt(NAB, 0) + ' N nach unten']],
      'Ruht das System, ist die Summe der äusseren Kräfte null. Für A: N_BA = m_A g. Für B: N_Boden = N_AB + m_B g. Für A+B: N_Boden = (m_A + m_B) g. Alle drei Rechnungen liefern dasselbe Ergebnis.');
  });
  MW.select(ctl, 'System', [['A', 'A (Klotz oben)'], ['B', 'B (Klotz unten)'], ['AB', 'A + B zusammen']], x => { sys = x; view.redraw(); });
  MW.slider(ctl, { label: 'm_A', min: 1, max: 5, step: 0.5, value: mA, unit: ' kg', onInput: x => { mA = x; view.redraw(); } });
  MW.slider(ctl, { label: 'm_B', min: 1, max: 5, step: 0.5, value: mB, unit: ' kg', onInput: x => { mB = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 4.4
W.append(dict(file='4-4-kraftdichte.html', title='Linienkraftdichte: Resultierende und Kräftemittelpunkt',
  sub='Eine Linienlast q(x) in N/m ersetzt man statisch durch die Resultierende R = ∫q dx (Fläche unter der Lastkurve) in ihrem Mittelpunkt x<sub>S</sub> = ∫x q dx / R (Schwerpunkt dieser Fläche).',
  hint='Form wählen, Intensitäten q₀ und q₁ ändern.', legend=[('--c1', 'Linienkraftdichte q(x)'), ('--c4', 'Resultierende R in x_S')], js=r'''
  let L = 4, q0 = 2, q1 = 2, form = 'gleich'; let s0, s1;
  const view = MW.View2D(cv, { xmin: -0.8, xmax: 6.0, ymin: -0.9, ymax: 3.6 }, v => {
    const C = v.C, k = 0.6, y0 = 0.25, q = x => q0 + (q1 - q0) * x / L, N = 12;
    const R = L * (q0 + q1) / 2, xS = R > 1e-9 ? L * (q0 + 2 * q1) / (3 * (q0 + q1)) : L / 2, MO = R * xS;
    const top = [[0, y0], [0, y0 + k * q0], [L, y0 + k * q1], [L, y0]];
    v.poly(top, C.c1, 1.5, null, true, 'rgba(120,120,120,0.10)');
    for (let i = 0; i <= N; i++) { const x = L * i / N, h = k * q(x); if (h > 0.05) v.arrow([x, y0 + h], [0, -h + 0.02], C.c1, 1.6, 7); }
    v.poly([[0, 0], [L, 0]], C.fg, 5);
    v.dot([0, 0], C.muted, 4); v.text([0, 0], 'O', C.muted, -4, 20, 13); v.text([L, 0], 'x = L', C.muted, -10, 20, 12);
    v.text([0, y0 + k * q0], 'q₀', C.c1, -22, 4, 13); v.text([L, y0 + k * q1], 'q₁', C.c1, 6, 4, 13);
    const len = 0.5 + R * 0.09;
    if (R > 1e-9) { v.arrow([xS, len + 0.02], [0, -len], C.c4, 4, 12); v.text([xS, len], 'R', C.c4, 6, -4, 15); v.dot([xS, 0], C.c4, 5);
      v.line([0, -0.45], [xS, -0.45], C.c4, 1.5); v.text([xS / 2, -0.45], 'x_S', C.c4, -8, 16, 13); v.line([0, -0.33], [0, -0.57], C.c4, 1.5); v.line([xS, -0.33], [xS, -0.57], C.c4, 1.5); }
    MW.info(infoEl, 'Resultierende R = Fläche unter q(x)', [['R = ∫q dx', fmt(R, 2) + ' N  (= L(q₀+q₁)/2)'], ['x_S = ∫x q dx / R', fmt(xS, 2) + ' m  (= L(q₀+2q₁) / (3(q₀+q₁)))'], ['Moment bez. O', 'M_O = ∫x q dx = R x_S = ' + fmt(MO, 2) + ' Nm']],
      form === 'gleich' ? 'Gleichförmige Last: R = qL im Balkenmittelpunkt x_S = L/2.' : form === 'dreieck' ? 'Dreieckslast (q₀ = 0): R = q₁L/2, x_S = 2L/3 vom Nullpunkt der Last.' : 'Trapez = Rechteck + Dreieck. Der Mittelpunkt liegt zwischen L/3 und 2L/3.');
  });
  const setForm = f => { form = f; if (f === 'gleich') { q1 = q0; } if (f === 'dreieck') { q0 = 0; } s0.set(q0); s1.set(q1); view.redraw(); };
  MW.select(ctl, 'Form', [['gleich', 'gleichförmig'], ['dreieck', 'Dreieck'], ['trapez', 'Trapez']], setForm);
  s0 = MW.slider(ctl, { label: 'q₀', min: 0, max: 4, step: 0.25, value: q0, unit: ' N/m', onInput: x => { q0 = x; if (form === 'gleich') { q1 = x; s1.set(x); } view.redraw(); } });
  s1 = MW.slider(ctl, { label: 'q₁', min: 0, max: 4, step: 0.25, value: q1, unit: ' N/m', onInput: x => { q1 = x; if (form === 'gleich') { q0 = x; s0.set(x); } view.redraw(); } });
  MW.slider(ctl, { label: 'L', min: 2, max: 5, step: 0.25, value: L, unit: ' m', onInput: x => { L = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('kap4', W))
