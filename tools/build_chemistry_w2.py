"""Widgets for Chemistry (151-0909-00L), week 2: gases (Lecture 2, Brown Ch. 10).
Sources: Lecture_2_slides p. 14-26, Exercise2_notes p. 7-10."""
from template import build
from build_analysis_w1 import AX, BOX

R = '8.314'
W = []

# ---------------------------------------------------------------- 10.3 / 10.4
W.append(dict(file='10-4-ideal-gas-law.html', title='Gas laws and the ideal gas law PV = nRT',
  sub='Boyle (n, T fixed): PV = const. Charles (n, P fixed): V/T = const. Avogadro (P, T fixed): V/n = const. Together: PV = nRT with R = 8.314 L·kPa/(mol·K). T always in kelvin.',
  hint='Choose a law, then move the sliders.', legend=[('--c2', 'current n, T or P'), ('--line', 'other values for comparison'), ('--c1', 'current state')], js=AX + r'''
  const R = ''' + R + r''';
  const L = {
    boyle: { name: 'Boyle: P–V at fixed n, T', x: 'V (L)', y: 'P (kPa)', xr: [0, 50], yr: [0, 600] },
    charles: { name: 'Charles: V–T at fixed n, P', x: 'T (K)', y: 'V (L)', xr: [0, 800], yr: [0, 80] },
    avo: { name: 'Avogadro: V–n at fixed P, T', x: 'n (mol)', y: 'V (L)', xr: [0, 5], yr: [0, 150] },
  };
  let key = 'boyle', n = 1, T = 273.15, P = 101.325, Vol = 22.41;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = L[key], A = mkAx(s.xr[0], s.xr[1], s.yr[0], s.yr[1]); axes(v, A, s.x, s.y);
    let pt, rows, head, note;
    if (key === 'boyle') {
      [0.5, 2].forEach(k => fplot(v, A, x => n * R * T * k / x, C.line, 1.4, 600, 0.3, 50));
      fplot(v, A, x => n * R * T / x, C.c2, 2.6, 800, 0.3, 50);
      P = n * R * T / Vol; pt = [Vol, P];
      head = 'P = nRT / V = ' + fmt(P, 1) + ' kPa'; rows = [['P · V', fmt(P * Vol, 0) + ' L·kPa (constant)'], ['n, T', fmt(n, 2) + ' mol, ' + fmt(T, 1) + ' K']];
      note = 'Halve V and P doubles. Grey curves: same n at T/2 and 2T.';
    } else if (key === 'charles') {
      [0.5, 2].forEach(k => fplot(v, A, x => n * R * x / (P * k), C.line, 1.4, 200));
      fplot(v, A, x => n * R * x / P, C.c2, 2.6, 400);
      Vol = n * R * T / P; pt = [T, Vol];
      v.text(A.P(0, 0), '0 K = −273.15 °C', C.muted, 8, -18, 11, false);
      head = 'V = nRT / P = ' + fmt(Vol, 2) + ' L'; rows = [['V / T', fmt(Vol / T, 4) + ' L/K (constant)'], ['T', fmt(T, 1) + ' K = ' + fmt(T - 273.15, 1) + ' °C']];
      note = 'V is proportional to T only in kelvin. The line extrapolates to V = 0 at 0 K. Grey lines: P/2 and 2P.';
    } else {
      [0.5, 2].forEach(k => fplot(v, A, x => x * R * T * k / P, C.line, 1.4, 200));
      fplot(v, A, x => x * R * T / P, C.c2, 2.6, 400);
      Vol = n * R * T / P; pt = [n, Vol];
      head = 'V = nRT / P = ' + fmt(Vol, 2) + ' L'; rows = [['V / n (molar volume)', fmt(Vol / n, 2) + ' L/mol'], ['P, T', fmt(P, 1) + ' kPa, ' + fmt(T, 1) + ' K']];
      note = 'Equal volumes of any gas at the same P and T contain the same number of molecules. At STP (273.15 K, 101.325 kPa): 22.41 L/mol.';
    }
    if (A.inY(pt[1])) { v.line(A.P(pt[0], s.yr[0]), A.P(pt[0], pt[1]), C.c1, 1, [3, 3]); v.line(A.P(s.xr[0], pt[1]), A.P(pt[0], pt[1]), C.c1, 1, [3, 3]); v.dot(A.P(pt[0], pt[1]), C.c1, 6); }
    MW.info(infoEl, head, rows, note, !A.inY(pt[1]));
  });
  function controls() {
    ctl.innerHTML = '';
    MW.select(ctl, 'Law', Object.entries(L).map(([k, s]) => [k, s.name]), x => { key = x; controls(); view.redraw(); }).set(key);
    const sl = (label, lo, hi, step, get, set, unit) => MW.slider(ctl, { label, min: lo, max: hi, step, value: get(), fmt: x => fmt(x, step < 0.1 ? 2 : 1) + ' ' + unit, onInput: x => { set(x); view.redraw(); } });
    if (key !== 'avo') sl('n', 0.1, 3, 0.01, () => n, x => n = x, 'mol');
    if (key !== 'charles') sl('T', 100, 800, 0.5, () => T, x => T = x, 'K');
    if (key !== 'boyle') sl('P', 20, 500, 0.025, () => P, x => P = x, 'kPa');
    if (key === 'boyle') sl('V', 1, 50, 0.1, () => Vol, x => Vol = x, 'L');
    if (key === 'charles') sl('T', 1, 800, 0.5, () => T, x => T = x, 'K');
    if (key === 'avo') sl('n', 0.05, 5, 0.01, () => n, x => n = x, 'mol');
    MW.button(ctl, 'STP', () => { n = 1; T = 273.15; P = 101.325; Vol = 22.41; controls(); view.redraw(); });
  }
  controls();
'''))

# ---------------------------------------------------------------- 10.6
W.append(dict(file='10-6-speed-distribution.html', title='Distribution of molecular speeds',
  sub='At the same T every gas has the same average kinetic energy, so lighter molecules move faster. Higher T or lighter gas: the peak moves right and the curve gets broader and lower. u_mp < u_av < u_rms.',
  hint='Choose gas and temperature for curves A and B.', legend=[('--c2', 'curve A'), ('--c1', 'curve B'), ('--muted', 'u_mp, u_av, u_rms (dashed)')], js=AX + r'''
  const R = ''' + R + r''', NA = 6.02214e23;
  const G = { H2: 2.016, He: 4.003, N2: 28.01, O2: 32.00, CO2: 44.01, Cl2: 70.90 };
  let gA = 'N2', tA = 273, gB = 'N2', tB = 373;
  const f = (u, M, T) => { const a = M / (2 * R * T); return 4 * Math.PI * Math.pow(a / Math.PI, 1.5) * u * u * Math.exp(-a * u * u); };
  const sp = (M, T) => ({ mp: Math.sqrt(2 * R * T / M), av: Math.sqrt(8 * R * T / (Math.PI * M)), rms: Math.sqrt(3 * R * T / M) });
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, S = [[G[gA] / 1000, tA, C.c2], [G[gB] / 1000, tB, C.c1]];
    const umax = Math.max(...S.map(([M, T]) => sp(M, T).rms)) * 2.4, fmax = Math.max(...S.map(([M, T]) => f(sp(M, T).mp, M, T))) * 1.12;
    const A = mkAx(0, umax, 0, fmax * 1e3); axes(v, A, 'u (m/s)', 'fraction per m/s (×10⁻³)');
    S.forEach(([M, T, col]) => { fplot(v, A, u => f(u, M, T) * 1e3, col, 2.6, 600);
      const q = sp(M, T); [q.mp, q.av, q.rms].forEach(u => v.line(A.P(u, 0), A.P(u, f(u, M, T) * 1e3), col, 1, [4, 4])); });
    const qa = sp(S[0][0], tA), qb = sp(S[1][0], tB), ek = T => (1.5 * R * T / NA).toExponential(2) + ' J';
    MW.info(infoEl, 'u_rms = √(3RT/M), M in kg/mol', [
      ['A: ' + gA + ', ' + tA + ' K', 'u_mp ' + fmt(qa.mp, 0) + ', u_av ' + fmt(qa.av, 0) + ', u_rms ' + fmt(qa.rms, 0) + ' m/s'],
      ['B: ' + gB + ', ' + tB + ' K', 'u_mp ' + fmt(qb.mp, 0) + ', u_av ' + fmt(qb.av, 0) + ', u_rms ' + fmt(qb.rms, 0) + ' m/s'],
      ['avg E_k per molecule A', ek(tA)], ['avg E_k per molecule B', ek(tB)]],
      'Average E_k = (3/2)RT/N_A depends only on T. u_rms is from Lecture 2; the u_mp and u_av formulas (√(2RT/M), √(8RT/πM)) are from Brown 10.6.');
  });
  const opts = Object.keys(G).map(k => [k, k + ' (' + G[k] + ' g/mol)']);
  MW.select(ctl, 'Gas A', opts, x => { gA = x; view.redraw(); }).set(gA);
  MW.slider(ctl, { label: 'T_A', min: 100, max: 1500, step: 1, value: tA, fmt: x => x + ' K', onInput: x => { tA = x; view.redraw(); } });
  MW.select(ctl, 'Gas B', opts, x => { gB = x; view.redraw(); }).set(gB);
  MW.slider(ctl, { label: 'T_B', min: 100, max: 1500, step: 1, value: tB, fmt: x => x + ' K', onInput: x => { tB = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('chemistry-w2', W))
