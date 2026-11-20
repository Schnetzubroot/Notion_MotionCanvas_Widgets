"""Widgets for Chemistry (151-0909-00L), week 5: Thermodynamics II (Lecture 5, Brown Ch. 19).
Sources: Lecture_5_slides p. 14, 23-29; Exercise5_notes p. 5-8; PS5 Problems 3-5.
Every preset uses numbers from these files; nothing is invented."""
from template import build
from build_analysis_w1 import AX, BOX

W = []

# ---------------------------------------------------------------- 19.5 / 19.6
W.append(dict(file='19-6-gibbs-temperature.html', title='ΔG = ΔH − TΔS: how temperature decides spontaneity',
  sub='At constant T and P a process is spontaneous when ΔG &lt; 0. ΔG is a straight line in T: it starts at ΔH (T = 0) and has slope −ΔS. '
      'If ΔH and ΔS have the same sign, the line crosses zero at T = ΔH/ΔS and temperature decides.',
  hint='Pick an example from the course or set ΔH and ΔS yourself, then move T.',
  legend=[('--c2', 'ΔG(T) = ΔH − TΔS'), ('--fill', 'ΔG < 0: spontaneous'), ('--c1', 'current T'), ('--c4', 'crossover T = ΔH/ΔS')], js=AX + r'''
  // [label, ΔH in kJ/mol, ΔS in J/(mol·K), source]
  const P = {
    nh3:  ['N2 + 3 H2 → 2 NH3', -92.4, -199, 'Lecture_5_slides [page 23–24]'],
    nf3:  ['N2 + 3 F2 → 2 NF3', -249, -278, 'PS5 Problem 4(a)'],
    ncl3: ['N2 + 3 Cl2 → 2 NCl3', 460, -275, 'PS5 Problem 4(b)'],
    n2f4: ['N2F4 → 2 NF2', 85, 198, 'PS5 Problem 4(c)'],
    baco3:['BaCO3(s) → BaO(s) + CO2(g)', 269.3, 171.9, 'PS5 Problem 3(a)'],
    pbs:  ['2 PbS + 3 O2 → 2 PbO + 2 SO2', -844, -165, 'Exercise5_notes [page 8], SP6'],
    ice:  ['H2O(s) → H2O(l)', 6.0, 22, 'Lecture_5_slides [page 14]'],
    br2:  ['Br2(l) → Br2(g), Trouton', 30.71, 88, 'PS5 Problem 5'],
    own:  ['your own values', 50, 100, ''],
  };
  const CASE = {
    i:   ['(i)', 'ΔH < 0, ΔS > 0', 'spontaneous at all temperatures'],
    ii:  ['(ii)', 'ΔH > 0, ΔS < 0', 'nonspontaneous at all temperatures'],
    iii: ['(iii)', 'ΔH < 0, ΔS < 0', 'spontaneous at low T, nonspontaneous at high T'],
    iv:  ['(iv)', 'ΔH > 0, ΔS > 0', 'spontaneous at high T, nonspontaneous at low T'],
  };
  let key = 'nh3', dH = P.nh3[1], dS = P.nh3[2], T = 298.15, Tmax = 1000;
  const G = t => dH - t * dS / 1000;  // kJ/mol
  const kind = () => dH <= 0 ? (dS >= 0 ? 'i' : 'iii') : (dS <= 0 ? 'ii' : 'iv');
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, g0 = G(0), g1 = G(Tmax), g = G(T);
    let lo = Math.min(0, g0, g1), hi = Math.max(0, g0, g1); const pad = 0.12 * ((hi - lo) || 1); lo -= pad; hi += pad;
    const A = mkAx(0, Tmax, lo, hi);
    v.poly([A.P(0, lo), A.P(Tmax, lo), A.P(Tmax, 0), A.P(0, 0)], null, 1, null, true, C.fill);
    axes(v, A, 'T (K)', 'ΔG (kJ/mol)');
    v.text(A.P(0, 0), '↓ spontaneous (ΔG < 0)', C.muted, 8, 16, 11, false);
    v.text(A.P(0, 0), '↑ nonspontaneous (ΔG > 0)', C.muted, 8, -7, 11, false);
    fplot(v, A, G, C.c2, 2.6, 2);
    const k = kind(), cr = dS !== 0 ? dH * 1000 / dS : NaN, hasCr = (k === 'iii' || k === 'iv') && cr > 0;
    if (hasCr && cr <= Tmax) { v.line(A.P(cr, lo), A.P(cr, hi), C.c4, 1.4, [5, 4]); v.dot(A.P(cr, 0), C.c4, 5);
      v.text(A.P(cr, 0), 'T = ' + fmt(cr, 0) + ' K', C.c4, 6, -8, 12, true); }
    v.line(A.P(T, lo), A.P(T, g), C.c1, 1, [3, 3]); v.dot(A.P(T, g), C.c1, 6);
    const c = CASE[k], src = P[key][3];
    const rows = [
      ['ΔH, ΔS', fmt(dH, 2) + ' kJ/mol, ' + fmt(dS, 1) + ' J/(mol·K)'],
      ['ΔG at ' + fmt(T, 2) + ' K', fmt(dH, 2) + ' − (' + fmt(T, 2) + ' K)(' + fmt(dS / 1000, 4) + ' kJ/(mol·K)) = ' + fmt(g, 2) + ' kJ/mol'],
      ['at this T', g < 0 ? 'spontaneous' : g > 0 ? 'nonspontaneous' : 'equilibrium (ΔG = 0)'],
      ['case ' + c[0] + ' ' + c[1], c[2]],
      ['crossover T = ΔH/ΔS', hasCr ? fmt(cr, 0) + ' K' + (cr > Tmax ? ' (beyond the plot, raise T_max)' : '') : 'none: ΔG never changes sign'],
    ];
    MW.info(infoEl, P[key][0], rows,
      (src ? 'Values from ' + src + '. ' : '') + 'Convert ΔS from J to kJ before subtracting. The line assumes ΔH and ΔS do not change with T, '
      + 'which is only an approximation far from 298 K. At the crossover ΔG = 0: for melting or boiling that is the melting or boiling point.');
  });
  let sH, sS, sT, sM;
  const fitT = () => { const cr = dH * 1000 / dS; Tmax = (dH * dS > 0 && cr > 0) ? Math.min(3000, Math.max(400, Math.ceil(cr * 1.3 / 50) * 50)) : 1000; sM.set(Tmax); };
  const sel = MW.select(ctl, 'Example', Object.entries(P).map(([k, p]) => [k, p[0]]), x => {
    key = x; if (x !== 'own') { dH = P[x][1]; dS = P[x][2]; sH.set(dH); sS.set(dS); fitT(); } view.redraw(); }).set(key);
  sH = MW.slider(ctl, { label: 'ΔH', min: -1000, max: 1000, step: 0.1, value: dH, fmt: x => fmt(x, 1) + ' kJ/mol', onInput: x => { dH = x; key = 'own'; sel.set('own'); view.redraw(); } });
  sS = MW.slider(ctl, { label: 'ΔS', min: -1000, max: 1000, step: 0.1, value: dS, fmt: x => fmt(x, 1) + ' J/(mol·K)', onInput: x => { dS = x; key = 'own'; sel.set('own'); view.redraw(); } });
  sT = MW.slider(ctl, { label: 'T', min: 0, max: 3000, step: 0.05, value: T, fmt: x => fmt(x, 2) + ' K', onInput: x => { T = x; view.redraw(); } });
  sM = MW.slider(ctl, { label: 'T_max (plot)', min: 400, max: 3000, step: 50, value: Tmax, fmt: x => x + ' K', onInput: x => { Tmax = x; view.redraw(); } });
  MW.button(ctl, '298.15 K', () => { T = 298.15; sT.set(T); view.redraw(); });
'''))

if __name__ == '__main__':
    print(build('chemistry-w5', W))
