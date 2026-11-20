"""Widgets zu Analysis I, Woche 6: Anhang A Komplexe Zahlen, Polarform, Euler-Formel, Multiplikation in
Polarkoordinaten, Wurzeln (Stammbach, Teil C, Anhang S. 4-10 und 14-16; Vorlesungsnotizen Kap. A S. 3-7,
Vorlesungen 13 und 14 vom 21. und 23.10.2026)."""
from template import build

# gemeinsame Hilfen für komplexe Zahlen (auch von Woche 7 benutzt)
CPLX = r'''
  const cm = (p, q) => [p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0]];
  const ab = p => Math.hypot(p[0], p[1]), arg = p => Math.atan2(p[1], p[0]);
  const pol = (r, t) => [r * Math.cos(t), r * Math.sin(t)];
  const cs = p => { const r = x => Math.round(x * 1000) / 1000; const a = r(p[0]), b = r(p[1]);
    return (a === 0 && b !== 0 ? '' : fmt(a, 3)) + (b === 0 ? (a === 0 ? '0' : '') : (b < 0 ? (a === 0 ? '−' : ' − ') : (a === 0 ? '' : ' + ')) + (Math.abs(b) === 1 ? '' : fmt(Math.abs(b), 3)) + 'i'); };
  // Winkel als Vielfaches von π, wenn möglich (Nenner bis 12)
  const piF = x => { const q = x / Math.PI; for (let d = 1; d <= 12; d++) { const n = Math.round(q * d); if (Math.abs(q * d - n) < 1e-6) {
      if (n === 0) return '0'; const a = Math.abs(n); return (n < 0 ? '−' : '') + (a === 1 ? '' : a) + 'π' + (d === 1 ? '' : '/' + d); } } return fmt(x, 4); };
  const deg = x => fmt(x * 180 / Math.PI, 2) + '°';
  // Betrag schön: √n, wenn r² fast ganzzahlig ist
  const rF = r => { const s = r * r, n = Math.round(s); if (Math.abs(s - n) < 1e-6 && n > 0) { const k = Math.round(Math.sqrt(n)); return k * k === n ? String(k) : '√' + n + ' ≈ ' + fmt(r, 4); } return fmt(r, 4); };
  const norm = t => { while (t <= -Math.PI + 1e-12) t += 2 * Math.PI; while (t > Math.PI + 1e-12) t -= 2 * Math.PI; return t; };
  const snap = p => [Math.round(p[0] * 4) / 4, Math.round(p[1] * 4) / 4];
'''

W = []

# ---------------------------------------------------------------- A.2
W.append(dict(file='A-2-polarform.html', title='Polarform z = r · eⁱᵠ und Euler-Formel',
  sub='Jede Zahl z ≠ 0 hat einen Betrag r = |z| und einen Winkel φ = arg z. Dann ist z = r(cos φ + i sin φ) = r · eⁱᵠ. Der Punkt eⁱᵠ liegt auf dem Einheitskreis. Achtung beim Winkel: arctan(b/a) allein trifft für a < 0 den falschen Quadranten.',
  hint='z ziehen oder ein Beispiel wählen.', legend=[('--c2', 'z'), ('--c3', 'a = r cos φ, b = r sin φ'), ('--c1', 'Winkel φ'), ('--c5', 'eⁱᵠ'), ('--c4', 'z̄')], js=CPLX + r'''
  const S3 = Math.sqrt(3);
  const EX = { a: ['1 + √3 i (Vorlesung S. 3)', [1, S3]], b: ['3 − √3 i (Vorlesung S. 3)', [3, -S3]], c: ['−√3 + √3 i (Skript S. 7)', [-S3, S3]],
    d: ['−2 − i (eigenes Beispiel)', [-2, -1]], e: ['−1 (eigenes Beispiel)', [-1, 0]] };
  let z = [1, S3], conj = false;
  const view = MW.View2D(cv, { xmin: -3.6, xmax: 3.6, ymin: -2.3, ymax: 2.3, xlabel: 'Re', ylabel: 'Im' }, v => {
    const C = v.C; v.grid(1); v.circle([0, 0], 1, C.muted, 1.4, [5, 4]);
    const r = ab(z), ph = arg(z);
    if (r < 1e-9) { v.dot([0, 0], C.c2, 6); MW.info(infoEl, 'z = 0', [['arg z', 'nicht definiert']], 'Für z = 0 gibt es keinen Winkel, die Polarform braucht z ≠ 0 (Skript S. 5).', true); return; }
    v.line([z[0], 0], z, C.c3, 1.3, [4, 3]); v.line([0, z[1]], z, C.c3, 1.3, [4, 3]);
    v.text([z[0], 0], 'a', C.c3, 0, z[1] >= 0 ? 16 : -8, 12, true, 'center'); v.text([0, z[1]], 'b', C.c3, z[0] >= 0 ? -12 : 6, 4, 12);
    v.arc([0, 0], 0.42, 0, ph, C.c1, 2.2); v.text(pol(0.62, ph / 2), 'φ', C.c1, -4, 5, 13);
    const u = pol(1, ph); v.line([0, 0], u, C.c5, 1.2); v.dot(u, C.c5, 5); v.text(u, 'eⁱᵠ', C.c5, 6, ph > 0 ? 16 : -8, 12);
    if (conj) { const w = [z[0], -z[1]]; v.arc([0, 0], 0.7, 0, -ph, C.c4, 1.6, [4, 3]); v.arrow([0, 0], w, C.c4, 2, 9); v.dot(w, C.c4, 5); v.text(w, 'z̄ = r e⁻ⁱᵠ', C.c4, 8, 14, 12); }
    v.arrow([0, 0], z, C.c2, 2.6, 10); v.dot(z, C.c2, 6); v.text(z, 'z', C.c2, 8, -8, 14);
    v.text(pol(r / 2, ph), 'r', C.c2, 6, -6, 13);
    const naive = Math.abs(z[0]) < 1e-12 ? null : Math.atan(z[1] / z[0]);
    const rows = [['kartesisch z = a + ib', cs(z)], ['r = |z| = √(a² + b²)', rF(r)],
      ['arctan(b/a)', naive === null ? 'nicht definiert (a = 0)' : piF(naive) + ' = ' + deg(naive)],
      ['φ = arg z ∈ (−π, π]', piF(ph) + ' = ' + deg(ph)],
      ['Polarform', fmt(r, 3) + ' · e^(i · ' + piF(ph) + ')'],
      ['Euler: r(cos φ + i sin φ)', fmt(r, 3) + ' · (' + fmt(Math.cos(ph), 4) + ' + ' + fmt(Math.sin(ph), 4) + ' i)']];
    if (conj) rows.push(['z̄ = r · e⁻ⁱᵠ', cs([z[0], -z[1]])]);
    const bad = z[0] < 0;
    MW.info(infoEl, 'z = ' + cs(z) + ' = ' + fmt(r, 3) + ' · e^(i · ' + piF(ph) + ')', rows,
      bad ? 'Hier ist a < 0: arctan(b/a) liegt in (−π/2, π/2) und zeigt in den falschen Quadranten. Skript S. 4: φ = arctan(b/a) + π für a < 0 (danach, falls nötig, 2π abziehen, damit φ ∈ (−π, π]).'
          : 'Skript S. 4–5: r = √(a² + b²), z = |z| · eⁱᵠ mit eⁱᵠ = cos φ + i sin φ (Formel (1.3)). Vorlesung S. 3: 1 + √3 i hat r = 2 und φ = arctan √3 = π/3, weil z im 1. Quadranten liegt.', bad);
  });
  view.handle(() => z, p => { z = snap(p); });
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([k, e]) => [k, e[0]]), u => { z = EX[u][1].slice(); view.redraw(); }).set('a');
  MW.check(ctl, 'Konjugierte z̄', conj, t => { conj = t; view.redraw(); });
'''))

# ---------------------------------------------------------------- A.3
W.append(dict(file='A-3-drehstreckung.html', title='Multiplikation in Polarform: Beträge multiplizieren, Winkel addieren',
  sub='Mit w = |w| · eⁱᵅ ist z · w = |z||w| · e^(i(φ + α)). Die Multiplikation mit w dreht z um den Winkel α und streckt um den Faktor |w|. Für |w| = 1 ist es eine reine Drehung, z bleibt auf seinem Kreis um 0. Potenzen: zⁿ = |z|ⁿ eⁱⁿᵠ.',
  hint='z ziehen, |w| und den Winkel α einstellen, oder zu „Potenzen“ wechseln.', legend=[('--c2', 'z'), ('--c4', 'w'), ('--c1', 'z · w bzw. zᵏ'), ('--muted', 'Kreis um 0 durch z')], js=CPLX + r'''
  const S3 = Math.sqrt(3), D = Math.PI / 180;
  const EX = {
    i: ['· i (Drehung um 90°)', 'mul', [2, 1], 1, 90, 3],
    mi: ['· (−i) mit z = 3 − √3 i (Vorlesung S. 3)', 'mul', [3, -S3], 1, -90, 3],
    half: ['· ½e^(−iπ/4) (Vorlesung S. 5)', 'mul', [2, 2], 0.5, -45, 3],
    rot: ['· eⁱᵅ mit α < 0 (Vorlesung S. 5)', 'mul', [1.5, 1.5], 1, -60, 3],
    p3: ['(cos φ + i sin φ)³ (Vorlesung S. 5)', 'pow', pol(1, 35 * D), 1, 0, 3],
    sp: ['Spirale z, z², …, z¹² (eigenes Beispiel)', 'pow', pol(1.12, 28 * D), 1, 0, 12],
  };
  let mode = 'mul', z = [2, 1], R = 1, al = 90 * D, n = 3;
  const view = MW.View2D(cv, { xmin: -5.2, xmax: 5.2, ymin: -3.3, ymax: 3.3, xlabel: 'Re', ylabel: 'Im' }, v => {
    const C = v.C; v.grid(1); v.circle([0, 0], 1, C.grid, 1.2);
    const r = ab(z), ph = arg(z); v.circle([0, 0], r, C.muted, 1.3, [5, 4]);
    v.arc([0, 0], 0.55, 0, ph, C.c2, 1.8);
    if (mode === 'mul') {
      const w = pol(R, al), p = cm(z, w);
      v.arc([0, 0], 0.95, ph, ph + al, C.c4, 2, [4, 3]); v.text(pol(1.15, ph + al / 2), 'α', C.c4, -4, 5, 13);
      v.arrow([0, 0], w, C.c4, 2, 9); v.dot(w, C.c4, 5); v.text(w, 'w', C.c4, 8, -6, 13);
      v.arrow([0, 0], z, C.c2, 2.4, 10); v.dot(z, C.c2, 6); v.text(z, 'z', C.c2, 8, -6, 13);
      v.arrow([0, 0], p, C.c1, 2.6, 10); v.text(p, 'z · w', C.c1, 8, 16, 13);
      MW.info(infoEl, 'z · w = ' + cs(p), [['z', cs(z) + ',  |z| = ' + fmt(r, 3) + ',  arg z = ' + deg(ph)],
        ['w = |w| eⁱᵅ', cs(w) + ',  |w| = ' + fmt(R, 3) + ',  α = ' + deg(al)],
        ['|z · w| = |z| · |w|', fmt(r, 3) + ' · ' + fmt(R, 3) + ' = ' + fmt(r * R, 4)],
        ['arg(z · w) = arg z + α', deg(ph) + ' + ' + deg(al) + (Math.abs(norm(ph + al) - (ph + al)) > 1e-9 ? ' ≙ ' + deg(norm(ph + al)) : '')]],
        'Skript S. 5: |z · z′| = |z| · |z′|, arg(z · z′) = arg z + arg z′. Skript S. 14–16: · eⁱᵅ ist eine Drehung um α, · r (reell) eine Streckung. '
        + (R === 1 ? 'Hier |w| = 1: z · w bleibt auf dem Kreis durch z (Vorlesung S. 5).' : 'Vorlesung S. 5: w = ½e^(−iπ/4) dreht um 45° im Uhrzeigersinn und halbiert den Betrag.'));
    } else {
      const pts = [[1, 0]]; let q = [1, 0];
      for (let k = 1; k <= n; k++) { q = cm(q, z); pts.push(q); }
      v.poly(pts, C.c1, 1.6, [3, 3]);
      const sup = k => String(k).split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[+d]).join('');
      pts.forEach((p, k) => { if (k) { v.dot(p, C.c1, 4.5); if (n <= 8 || k === n) v.text(p, k === 1 ? 'z' : 'z' + sup(k), C.c1, 7, -6, 12); } });
      v.arc([0, 0], 0.8, 0, n * ph, C.c1, 1.6, [4, 3]);
      v.arrow([0, 0], z, C.c2, 2.4, 10); v.dot(z, C.c2, 6);
      const zn = pts[n];
      MW.info(infoEl, 'zⁿ = ' + cs(zn) + '  (n = ' + n + ')', [['z', cs(z) + ',  |z| = ' + fmt(r, 4) + ',  φ = ' + deg(ph)],
        ['|zⁿ| = |z|ⁿ', fmt(r, 4) + '^' + n + ' = ' + fmt(r ** n, 4)], ['arg zⁿ = n · φ', n + ' · ' + deg(ph) + ' = ' + deg(n * ph) + ' ≙ ' + deg(norm(n * ph))]],
        'Skript S. 7: zⁿ = |z|ⁿ · eⁱⁿᵠ. Für |z| = 1 bleiben alle Potenzen auf dem Einheitskreis, sonst laufen sie spiralförmig nach aussen oder innen. Vorlesung S. 5: Im((cos φ + i sin φ)³) = sin 3φ.');
    }
  });
  view.handle(() => z, p => { z = snap(p); });
  const sR = MW.slider(ctl, { label: '|w|', min: 0.25, max: 2, step: 0.05, value: R, onInput: u => { R = u; view.redraw(); } });
  const sA = MW.slider(ctl, { label: 'α', min: -180, max: 180, step: 1, value: 90, fmt: u => fmt(u, 0) + '°', onInput: u => { al = u * D; view.redraw(); } });
  const sN = MW.slider(ctl, { label: 'n', min: 1, max: 12, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  const show = () => { sR.el.style.display = sA.el.style.display = mode === 'mul' ? '' : 'none'; sN.el.style.display = mode === 'pow' ? '' : 'none'; };
  const md = MW.select(ctl, 'Rechnung', [['mul', 'z · w'], ['pow', 'Potenzen z, z², …, zⁿ']], u => { mode = u; show(); view.redraw(); });
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([k, e]) => [k, e[0]]), u => { const e = EX[u];
    mode = e[1]; md.set(mode); z = e[2].slice(); R = e[3]; sR.set(R); al = e[4] * D; sA.set(e[4]); n = e[5]; sN.set(n); show(); view.redraw(); }).set('i');
  show();
'''))

# ---------------------------------------------------------------- A.4
W.append(dict(file='A-4-wurzeln.html', title='n-te Wurzeln: zⁿ = c hat n Lösungen auf einem regelmässigen n-Eck',
  sub='Ansatz z = ρeⁱᵠ: aus ρⁿ eⁱⁿᵠ = |c| eⁱᵅ folgt ρ = ⁿ√|c| und nφ = α „modulo 2π“. Das gibt φₖ = (α + 2πk)/n für k = 0, …, n − 1. Die Lösungen sind die Ecken eines regelmässigen n-Ecks um 0.',
  hint='c ziehen, n einstellen oder ein Beispiel wählen.', legend=[('--c2', 'c'), ('--c1', 'Lösungen zₖ'), ('--c3', 'Kreis mit Radius ⁿ√|c|'), ('--muted', 'Einheitskreis')], js=CPLX + r'''
  const EX = { i2: ['z² = i (Vorlesung S. 6)', [0, 1], 2], c3: ['z³ = −3 + 3i (Vorlesung S. 6)', [-3, 3], 3], a5: ['z⁵ = ia mit a = 2 (Vorlesung S. 7)', [0, 2], 5],
    e6: ['z⁶ = 1 (Skript S. 22–23)', [1, 0], 6], m2: ['z² = −1', [-1, 0], 2] };
  let c = [0, 1], n = 2;
  const view = MW.View2D(cv, { xmin: -4.6, xmax: 4.6, ymin: -3.3, ymax: 3.3, xlabel: 'Re', ylabel: 'Im' }, v => {
    const C = v.C; v.grid(1); v.circle([0, 0], 1, C.muted, 1.3, [5, 4]);
    const R = ab(c), a = arg(c);
    v.arrow([0, 0], c, C.c2, 2.2, 9); v.dot(c, C.c2, 6); v.text(c, 'c', C.c2, 8, -6, 14);
    if (R < 1e-9) { MW.info(infoEl, 'c = 0', [['Lösung', 'nur z = 0']], 'Für c = 0 gibt es nur die Lösung z = 0 (n-fach). Der Satz „genau n Lösungen“ gilt für c ≠ 0 (Vorlesung S. 6).', true); return; }
    const rho = Math.pow(R, 1 / n), Z = [];
    for (let k = 0; k < n; k++) Z.push(pol(rho, (a + 2 * Math.PI * k) / n));
    v.circle([0, 0], rho, C.c3, 1.4, [3, 3]);
    v.arc([0, 0], 0.5, 0, a, C.c2, 1.6); v.arc([0, 0], 0.8, 0, a / n, C.c1, 2);
    if (n > 2) v.poly(Z, C.c1, 1.6, null, true, C.fill); else v.line(Z[0], Z[1], C.c1, 1.4, [4, 3]);
    Z.forEach((p, k) => { v.line([0, 0], p, C.c1, 1, [2, 3]); v.dot(p, C.c1, 6); v.text(p, 'z' + '₁₂₃₄₅₆₇₈₉'[k], C.c1, 8, p[1] >= 0 ? -6 : 16, 13); });
    const rows = [['c in Polarform', fmt(R, 3) + ' · e^(i · ' + piF(a) + ')'], ['ρ = ⁿ√|c|', rF(rho)],
      ['Winkelabstand 2π/n', piF(2 * Math.PI / n) + ' = ' + deg(2 * Math.PI / n)]];
    Z.forEach((p, k) => rows.push(['z' + '₁₂₃₄₅₆₇₈₉'[k] + ', φ = (' + piF(a) + ' + ' + (k ? (k === 1 ? '' : k) + '2π' : '0') + ')/' + n, cs(p) + ' = ' + fmt(rho, 3) + ' e^(i · ' + piF((a + 2 * Math.PI * k) / n) + ')']));
    MW.info(infoEl, 'zⁿ = ' + cs(c) + ' mit n = ' + n + ': ' + n + ' Lösungen', rows,
      'Skript S. 8–10: Ansatz z = ρeⁱᵠ, ρ = ⁿ√|c|, nφ = α modulo 2π. Vorlesung S. 6: z² = i = e^(iπ/2) = e^(i5π/2) gibt z₁ = e^(iπ/4) und z₂ = e^(i5π/4); der Repräsentant e^(i9π/2) gibt wieder z₁. Vorlesung S. 7: Drei Punkte sind nur dann die dritten Wurzeln einer Zahl, wenn sie ein gleichseitiges Dreieck um 0 bilden.');
  });
  view.handle(() => c, p => { c = snap(p); });
  const sN = MW.slider(ctl, { label: 'n', min: 2, max: 9, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([k, e]) => [k, e[0]]), u => { const e = EX[u]; c = e[1].slice(); n = e[2]; sN.set(n); view.redraw(); }).set('i2');
'''))

if __name__ == '__main__':
    print(build('analysis-w6', W))
