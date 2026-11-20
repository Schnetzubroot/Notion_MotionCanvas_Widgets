"""Widgets for Chemistry (151-0909-00L), weeks 6 and 7.
Week 6: hydrogen transitions (Lecture 6, Brown 6.3). Sources: Lecture_6_slides p. 9-11, Exercise6_notes p. 2, 9, PS6 Problems 2, 8.
Week 7: VSEPR shapes (Lecture 7, Brown 9.1-9.2). Sources: Lecture_7_slides p. 27-33, Exercise7_notes p. 6.
Constants: h, c from Exam_Info_Sheets_HS26 p. 1; hcR_H = 2.18e-18 J as used in Exercise 6 and PS6."""
from template import build
from build_analysis_w1 import BOX

W6, W7 = [], []

# ---------------------------------------------------------------- 6.3 hydrogen
W6.append(dict(file='6-3-hydrogen-transitions.html', title='Hydrogen atom: energy levels and spectral lines',
  sub='E<sub>n</sub> = −hcR<sub>H</sub>/n² = −2.18 × 10⁻¹⁸ J / n². A jump from n<sub>i</sub> to n<sub>f</sub> changes the energy by ΔE = E<sub>f</sub> − E<sub>i</sub>. '
      'ΔE &lt; 0: a photon is emitted; ΔE &gt; 0: a photon must be absorbed. Its wavelength is λ = hc/|ΔE|.',
  hint='Choose n_i and n_f. The right side shows all lines that end (or start) on n_f, on a logarithmic wavelength axis.',
  legend=[('--c1', 'selected transition'), ('--muted', 'other lines of the same series')], js=r'''
  const h = 6.626e-34, c = 2.998e8, A = 2.18e-18, NMAX = 8;
  const En = n => n === Infinity ? 0 : -A / (n * n);
  let ni = 3, nf = 2;
  const lam = (a, b) => h * c / Math.abs(En(b) - En(a)) * 1e9;  // nm
  // wavelength -> CSS color (approximation for display only)
  function wl2rgb(w) {
    let r = 0, g = 0, b = 0;
    if (w >= 380 && w < 440) { r = (440 - w) / 60; b = 1; } else if (w < 490) { g = (w - 440) / 50; b = 1; } else if (w < 510) { g = 1; b = (510 - w) / 20; }
    else if (w < 580) { r = (w - 510) / 70; g = 1; } else if (w < 645) { r = 1; g = (645 - w) / 65; } else if (w <= 780) { r = 1; }
    const f = w < 420 ? 0.3 + 0.7 * (w - 380) / 40 : w > 700 ? 0.3 + 0.7 * (780 - w) / 80 : 1;
    return 'rgb(' + [r, g, b].map(x => Math.round(255 * Math.pow(x * f, 0.8))).join(',') + ')';
  }
  const region = w => w < 10 ? 'X-ray' : w < 400 ? 'ultraviolet' : w <= 750 ? 'visible' : w < 1e6 ? 'infrared' : 'microwave';
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C;
    // ---- left: energy-level diagram, x in [0, 2.4], E in [-2.18e-18, 0] -> y in [0.1, 3.3]
    const Y = E => 3.3 + (E / A) * 3.2;
    v.text([0, 3.45], 'E (10⁻¹⁹ J)', C.muted, 0, 0, 11, false);
    const levels = [1, 2, 3, 4, 5, 6, 7, 8, Infinity];
    levels.forEach(n => { const y = Y(En(n)), act = n === ni || n === nf;
      v.line([0.55, y], [2.3, y], act ? C.fg : C.line, act ? 2.2 : 1.2);
      if (n <= 4 || n === Infinity) { v.text([0.5, y], fmt(En(n) * 1e19, 2), C.muted, 0, 4, 10, false, 'right');
        v.text([2.3, y], n === Infinity ? 'n = ∞' : 'n = ' + n, C.muted, 6, 4, 11, false); } });
    v.text([2.3, Y(En(6))], '…', C.muted, 10, 2, 11, false);
    if (ni !== nf) { const x = 1.45; v.arrow([x, Y(En(ni))], [0, Y(En(nf)) - Y(En(ni))], C.c1, 3, 11); }
    // ---- right: series on a log wavelength axis, x in [3.0, 6.1]
    const L0 = Math.log10(50), L1 = Math.log10(5000), X = w => 3.0 + (Math.log10(w) - L0) / (L1 - L0) * 3.1, yb = 1.2, yt = 2.4;
    for (let w = 380; w < 780; w += 4) v.poly([[X(w), yb], [X(w + 4), yb], [X(w + 4), yt], [X(w), yt]], null, 1, null, true, wl2rgb(w + 2));
    v.line([3.0, yb], [6.1, yb], C.muted, 1.2);
    [50, 100, 200, 500, 1000, 2000, 5000].forEach(w => { v.line([X(w), yb], [X(w), yb - 0.06], C.muted, 1); v.text([X(w), yb], String(w), C.muted, 0, 26, 10, false, 'center'); });
    v.text([6.1, yb], 'λ (nm)', C.muted, 0, 42, 11, false, 'right');
    v.text([X(150), yt], 'UV', C.muted, 0, -8, 11, false, 'center'); v.text([X(540), yt], 'visible', C.muted, 0, -8, 11, false, 'center'); v.text([X(2200), yt], 'infrared', C.muted, 0, -8, 11, false, 'center');
    const lo = Math.min(ni, nf);
    for (let n = lo + 1; n <= 40; n++) { const w = lam(lo, n); if (w >= 50 && w <= 5000) v.line([X(w), yb], [X(w), yt], C.muted, 1.4); }
    const wInf = lam(lo, Infinity); if (wInf >= 50 && wInf <= 5000) v.line([X(wInf), yb], [X(wInf), yt + 0.15], C.muted, 1, [3, 3]);
    let rows, head, warn = false;
    if (ni === nf) { head = 'n_i = n_f: no transition'; rows = []; warn = true; }
    else {
      const dE = En(nf) - En(ni), w = lam(ni, nf), em = dE < 0;
      if (w >= 50 && w <= 5000) { v.line([X(w), yb - 0.1], [X(w), yt + 0.3], C.c1, 3); v.text([X(w), yt + 0.3], fmt(w, w < 1000 ? 1 : 0) + ' nm', C.c1, 0, -6, 12, true, 'center'); }
      const fi = ni === Infinity ? '0' : '1/' + ni + '²', ff = nf === Infinity ? '0' : '1/' + nf + '²';
      head = (em ? 'Emission' : 'Absorption') + ': n = ' + (ni === Infinity ? '∞' : ni) + ' → ' + (nf === Infinity ? '∞' : nf);
      rows = [['ΔE = −2.18 × 10⁻¹⁸ J (' + ff + ' − ' + fi + ')', fmt(dE * 1e19, 3) + ' × 10⁻¹⁹ J'],
              ['photon', em ? 'emitted, E = ' + fmt(-dE * 1e19, 3) + ' × 10⁻¹⁹ J' : 'absorbed, E = ' + fmt(dE * 1e19, 3) + ' × 10⁻¹⁹ J'],
              ['λ = hc/|ΔE|', fmt(w, 1) + ' nm (' + region(w) + ')'],
              ['ν = c/λ', (c / (w * 1e-9)).toExponential(3).replace('e+', ' × 10^') + ' s⁻¹']];
      if (nf === Infinity) rows.push(['n_f = ∞', 'ionization: H → H⁺ + e⁻' + (ni === 1 ? ' (Exercise 6 SP5 gets 91.7 nm with R_H rounded to 1.09 × 10⁷ m⁻¹)' : '')]);
    }
    MW.info(infoEl, head, rows, 'Grey lines: all transitions between n = ' + lo + ' and higher levels; dashed: the series limit (n = ∞). '
      + 'Lines ending on n = 1 are UV, on n = 2 partly visible, on n = 3 infrared. Colors are approximate.', warn);
  });
  const opt = [1, 2, 3, 4, 5, 6, 7, 8].map(n => [String(n), String(n)]).concat([['inf', '∞']]);
  const val = s => s === 'inf' ? Infinity : +s;
  MW.select(ctl, 'n_i (start)', opt, x => { ni = val(x); view.redraw(); }).set(String(ni));
  MW.select(ctl, 'n_f (end)', opt, x => { nf = val(x); view.redraw(); }).set(String(nf));
  const presets = [['3→2: red line, PS6 8B', 3, 2], ['2→1: PS6 8A', 2, 1], ['4→3: PS6 8C', 4, 3], ['3→1: Lecture 6', 3, 1], ['5→1: PS6 Problem 2', 5, 1], ['1→∞: Exercise 6 SP5', 1, Infinity]];
  const selI = ctl.querySelectorAll('select')[0], selF = ctl.querySelectorAll('select')[1];
  MW.select(ctl, 'Course example', [['', '—']].concat(presets.map((p, i) => [String(i), p[0]])), x => { if (x === '') return; const p = presets[+x];
    ni = p[1]; nf = p[2]; selI.value = ni === Infinity ? 'inf' : String(ni); selF.value = nf === Infinity ? 'inf' : String(nf); view.redraw(); });
'''))

# ---------------------------------------------------------------- 9.2 VSEPR
W7.append(dict(file='9-2-vsepr-shapes.html', title='VSEPR: electron-domain and molecular geometry in 3D',
  sub='Electron domains (bonds and lone pairs) around the central atom spread as far apart as possible. All domains give the electron-domain geometry; '
      'the atoms alone give the molecular geometry. A double or triple bond counts as one domain.',
  hint='Drag to rotate. Choose the number of domains and lone pairs.', tall=True,
  legend=[('--c2', 'central atom'), ('--c3', 'bonded atom'), ('--c4', 'lone pair'), ('--line', 'electron-domain shape')], js=r'''
  const s3 = Math.sqrt(3) / 2, t = 1 / Math.sqrt(3);
  const POS = {
    2: [[1, 0, 0], [-1, 0, 0]],
    3: [[1, 0, 0], [-0.5, s3, 0], [-0.5, -s3, 0]],
    4: [[t, t, t], [t, -t, -t], [-t, t, -t], [-t, -t, t]],
    5: [[1, 0, 0], [-0.5, s3, 0], [-0.5, -s3, 0], [0, 0, 1], [0, 0, -1]],   // equatorial first, then axial
    6: [[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], // trans pair first
  };
  // [domains, lone pairs] -> [electron-domain geometry, molecular geometry, example, central, outer, angles]
  const T = {
    '2,0': ['linear', 'linear', 'CO2', 'C', 'O', '180°'],
    '3,0': ['trigonal planar', 'trigonal planar', 'BF3', 'B', 'F', '120°'],
    '3,1': ['trigonal planar', 'bent', 'NO2⁻', 'N', 'O', '< 120°'],
    '4,0': ['tetrahedral', 'tetrahedral', 'CH4', 'C', 'H', '109.5°'],
    '4,1': ['tetrahedral', 'trigonal pyramidal', 'NH3', 'N', 'H', '107° (ideal 109.5°)'],
    '4,2': ['tetrahedral', 'bent', 'H2O', 'O', 'H', '104.5° (ideal 109.5°)'],
    '5,0': ['trigonal bipyramidal', 'trigonal bipyramidal', 'PCl5', 'P', 'Cl', '90°, 120°'],
    '5,1': ['trigonal bipyramidal', 'seesaw', 'SF4', 'S', 'F', '≈ 90°, ≈ 120°'],
    '5,2': ['trigonal bipyramidal', 'T-shaped', 'ClF3', 'Cl', 'F', '≈ 90°'],
    '5,3': ['trigonal bipyramidal', 'linear', 'XeF2', 'Xe', 'F', '180°'],
    '6,0': ['octahedral', 'octahedral', 'SF6', 'S', 'F', '90°'],
    '6,1': ['octahedral', 'square pyramidal', 'BrF5', 'Br', 'F', '≈ 90°'],
    '6,2': ['octahedral', 'square planar', 'XeF4', 'Xe', 'F', '90°'],
  };
  const MAXLP = { 2: 0, 3: 1, 4: 2, 5: 3, 6: 2 };
  // which positions hold lone pairs: 5 domains -> equatorial first; 6 domains -> trans pair first; others -> first slots
  const lpIdx = (d, k) => [...Array(k).keys()];
  let D = 4, LP = 1, showShape = true;
  const view = MW.View3D(cv, { extent: 1.7, yaw: 25, pitch: 18 }, v => {
    const C = v.C, P = POS[D], lps = new Set(lpIdx(D, LP)), R = 1.25, row = T[D + ',' + LP];
    const Pw = P.map(p => V.mul(p, R));
    if (showShape) { // edges of the electron-domain polyhedron
      for (let i = 0; i < Pw.length; i++) for (let j = i + 1; j < Pw.length; j++) {
        const d = V.norm(V.sub(Pw[i], Pw[j])), dmin = Math.min(...Pw.map((a, k) => k === i ? 9 : V.norm(V.sub(a, Pw[i]))));
        if (D > 2 && d < dmin * 1.05 + 1e-6) v.line(Pw[i], Pw[j], C.line, 1, [4, 4]); }
    }
    const items = Pw.map((p, i) => ({ p, i, lp: lps.has(i), z: v.depth(p) })).sort((a, b) => a.z - b.z);
    const center = { p: [0, 0, 0], center: true, z: 0 };
    const all = items.concat([center]).sort((a, b) => a.z - b.z);
    items.forEach(it => { if (!it.lp) v.line([0, 0, 0], it.p, C.fg, 4); });
    all.forEach(it => {
      if (it.center) { v.dot([0, 0, 0], C.c2, 15); v.text([0, 0, 0], row[3], '#fff', 0, 5, 12, true, 'center'); return; }
      if (it.lp) { const q = V.mul(it.p, 0.62), e = V.mul(it.p, 0.08);
        v.line([0, 0, 0], V.mul(it.p, 0.4), C.c4, 1.5, [2, 3]);
        const s = v.toS(q); v.ctx.save(); v.ctx.globalAlpha = 0.28; v.sDot(s, C.c4, 22); v.ctx.restore();
        const perp = V.mul(V.unit(V.cross(it.p, Math.abs(it.p[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0])), 0.07);
        v.dot(V.add(q, perp), C.c4, 3.5); v.dot(V.sub(q, perp), C.c4, 3.5);
      } else { v.dot(it.p, C.c3, 12); v.text(it.p, row[4], '#fff', 0, 4, 11, true, 'center'); }
    });
    MW.info(infoEl, row[1] + ' (' + row[2] + ')', [
      ['electron domains', D + ' = ' + (D - LP) + ' bonding + ' + LP + ' lone pair' + (LP === 1 ? '' : 's')],
      ['electron-domain geometry', row[0]], ['molecular geometry', row[1]], ['bond angles', row[5]]],
      (D === 5 && LP > 0 ? 'With 5 domains the lone pairs sit in the equatorial plane, where they have the most room. ' : '')
      + (D === 6 && LP === 2 ? 'The two lone pairs sit opposite each other (trans). ' : '')
      + 'Lone pairs take more space than bonding pairs, so real angles are a bit smaller than ideal (CH4 109.5°, NH3 107°, H2O 104.5°). '
      + 'Table: Exercise7_notes p. 6 (Brown Tables 9.2–9.3).');
  });
  const lpOpts = () => [...Array(MAXLP[D] + 1).keys()].map(k => [String(k), String(k)]);
  MW.select(ctl, 'Electron domains', [2, 3, 4, 5, 6].map(n => [String(n), String(n)]), x => { D = +x; if (LP > MAXLP[D]) LP = MAXLP[D]; fillLP(); view.redraw(); }).set(String(D));
  MW.select(ctl, 'Lone pairs', [['0', '0'], ['1', '1'], ['2', '2'], ['3', '3']], x => { LP = +x; view.redraw(); });
  const lpEl = ctl.querySelectorAll('select')[1];
  function fillLP() { [...lpEl.options].forEach(o => { o.disabled = +o.value > MAXLP[D]; }); lpEl.value = String(LP); }
  fillLP();
  const ex = Object.entries(T).map(([k, r]) => [k, r[2] + ': ' + r[1]]);
  MW.select(ctl, 'Example', [['', '—']].concat(ex), x => { if (!x) return; [D, LP] = x.split(',').map(Number);
    ctl.querySelectorAll('select')[0].value = String(D); fillLP(); view.redraw(); });
  MW.check(ctl, 'Show domain shape', showShape, x => { showShape = x; view.redraw(); });
  MW.button(ctl, 'Reset view', () => view.resetView());
'''))

if __name__ == '__main__':
    print(build('chemistry-w6', W6))
    print(build('chemistry-w7', W7))
