"""Widgets zu Kapitel 11 (Woche 11): Statisch bestimmte Fachwerke.

Pendelstütze, Abzählkriterium u = s + r − 2k, Knotengleichgewicht, Dreikräfteschnitt, PdvL, räumliches Tetraeder.
Beispiele: Buch Fig. 11.6 (Dreigelenkbogen aus 10 Stäben) und Übungsheft Kap. 6, Aufgabe 1 (Abb. 6.7).
"""
from template import build

W = []

# Gemeinsame Fachwerk-Bibliothek: Modelle, Gleichungslöser, Zeichnen, schöne Zahlen.
TRUSS = r'''
  const h3 = Math.sqrt(3) / 2;
  const MODELS = {
    buch: { name: 'Buch Fig. 11.6', N: { A: [0, 0], E: [1, 0], D: [0.5, h3], C: [1.5, h3], H: [2, 0], G: [2.5, h3], B: [3, 0] },
      bars: [['A', 'E'], ['A', 'D'], ['D', 'E'], ['D', 'C'], ['E', 'C'], ['C', 'H'], ['C', 'G'], ['G', 'H'], ['G', 'B'], ['H', 'B']], num: true,
      sup: { A: 'xy', B: 'xy' }, loads: { D: [0, -1], G: [-Math.sqrt(3), 0] }, lbl: { D: 'F', G: 'F√3' },
      order: ['A', 'D', 'E', 'C', 'H', 'G', 'B'], box: { xmin: -0.6, xmax: 3.6, ymin: -0.55, ymax: 1.75 } },
    ueb1: { name: 'Übungsheft Abb. 6.7 (Aufgabe 1)', N: { A: [0, 0], B: [0.5, 0], C: [1, 0], D: [1.5, 0], E: [2, 0], F: [2.5, 0], G: [0, 1], H: [0.5, 1], I: [1, 1], J: [1.5, 1], K: [2, 1], L: [2.5, 1] },
      bars: 'G-H H-I I-J J-K K-L A-B B-C C-D D-E E-F G-A G-B H-B B-I I-C I-D J-D D-K K-E K-F L-F'.split(' ').map(s => s.split('-')), num: false,
      sup: { A: 'xy', E: 'y' }, loads: { G: [1, 0], L: [1, 0], C: [0, -1] }, lbl: { G: 'F', L: 'F', C: 'F' },
      box: { xmin: -0.6, xmax: 3.4, ymin: -0.6, ymax: 1.9 } },
  };
  const barName = (m, i) => m.num ? String(i + 1) : m.bars[i][0] + m.bars[i][1];
  const sName = (m, i) => 'S' + (m.num ? sub(i + 1) : '_' + m.bars[i][0] + m.bars[i][1]);
  const sub = n => String(n).split('').map(c => '₀₁₂₃₄₅₆₇₈₉'[+c]).join('');
  const unit = (m, i, from) => { const [a, b] = m.bars[i]; const p = from === a ? m.N[a] : m.N[b], q = from === a ? m.N[b] : m.N[a]; return V.unit(V.sub(q, p)); };
  // Gauss mit Spaltenpivot; liefert x oder null (singulär)
  const gauss = (A, b) => { const n = A.length, M = A.map((r, i) => [...r, b[i]]);
    for (let c = 0; c < n; c++) { let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      if (Math.abs(M[p][c]) < 1e-10) return null; [M[c], M[p]] = [M[p], M[c]];
      for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; } }
    return M.map((r, i) => r[n] / r[i]); };
  // reduzierte Zeilenstufenform: Rang und Basis des Nullraums
  const rref = A => { const M = A.map(r => [...r]), m = M.length, n = m ? M[0].length : 0, piv = []; let row = 0;
    for (let c = 0; c < n && row < m; c++) { let p = row; for (let r = row + 1; r < m; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      if (Math.abs(M[p][c]) < 1e-9) continue; [M[row], M[p]] = [M[p], M[row]]; const d = M[row][c]; for (let k = 0; k < n; k++) M[row][k] /= d;
      for (let r = 0; r < m; r++) if (r !== row) { const f = M[r][c]; if (f) for (let k = 0; k < n; k++) M[r][k] -= f * M[row][k]; }
      piv.push(c); row++; }
    const free = []; for (let c = 0; c < n; c++) if (!piv.includes(c)) free.push(c);
    const null_ = free.map(f => { const x = new Array(n).fill(0); x[f] = 1; piv.forEach((c, r) => { x[c] = -M[r][f]; }); return x; });
    return { rank: piv.length, null: null_ }; };
  // Gleichgewichtsmatrix: Unbekannte = Stabkräfte (Zug positiv) + Lagerkomponenten
  const eqSystem = m => { const keys = Object.keys(m.N), cols = m.bars.map((_, i) => ({ t: 'S', i }));
    keys.forEach(k => { const s = m.sup[k] || ''; if (s.includes('x')) cols.push({ t: 'R', k, d: 0 }); if (s.includes('y')) cols.push({ t: 'R', k, d: 1 }); });
    const A = [], b = [];
    keys.forEach(k => [0, 1].forEach(d => { const row = cols.map(c => c.t === 'S' ? (m.bars[c.i].includes(k) ? unit(m, c.i, k)[d] : 0) : (c.k === k && c.d === d ? 1 : 0));
      A.push(row); b.push(-((m.loads[k] || [0, 0])[d])); }));
    return { keys, cols, A, b }; };
  const solveTruss = m => { const sys = eqSystem(m); if (sys.A.length !== sys.cols.length) return null; const x = gauss(sys.A, sys.b); if (!x) return null;
    const S = m.bars.map((_, i) => x[i]), R = {}; sys.cols.forEach((c, j) => { if (c.t === 'R') { R[c.k] = R[c.k] || [0, 0]; R[c.k][c.d] = x[j]; } }); return { S, R }; };
  const gcd = (a, b) => b ? gcd(b, a % b) : a;
  // Zahl als p/q·√r erkennen (Buchform), sonst Dezimalzahl
  const nice = (x, d = 3) => { if (Math.abs(x) < 1e-9) return '0';
    for (const r of [1, 3, 2, 5, 6, 15]) for (let q = 1; q <= 36; q++) { const p = x * q / Math.sqrt(r), pr = Math.round(p);
      if (pr !== 0 && Math.abs(p - pr) < 1e-7 && Math.abs(pr) <= 300) { const g = gcd(Math.abs(pr), q), P = Math.abs(pr) / g, Q = q / g;
        return (x < 0 ? '−' : '') + (r > 1 ? (P === 1 ? '' : P) + '√' + r : P) + (Q > 1 ? '/' + Q : ''); } }
    return fmt(x, d); };
  const niceF = x => { const s = nice(x); return s === '0' ? '0' : s === '1' ? 'F' : s === '−1' ? '−F' : s + '·F'; };
  // Zeichnen: Stäbe, Knoten, Lager, Lasten
  const drawSup = (v, p, type, C) => { const s = 0.13; v.poly([p, [p[0] - s, p[1] - 1.5 * s], [p[0] + s, p[1] - 1.5 * s]], C.fg, 1.6, null, true);
    const y0 = p[1] - 1.5 * s - (type === 'y' ? 0.07 : 0); if (type === 'y') { v.line([p[0] - 1.4 * s, y0], [p[0] + 1.4 * s, y0], C.fg, 1.6); }
    for (let i = -1; i <= 1; i += 0.5) v.line([p[0] + i * s * 1.2, y0], [p[0] + i * s * 1.2 - 0.06, y0 - 0.07], C.muted, 1); };
  const drawLoads = (v, m, C, k = 0.42) => Object.entries(m.loads).forEach(([n, f]) => { const d = V.mul(f, k), p = m.N[n];
    v.arrow(V.sub(p, d), d, C.c4, 3, 11); v.text(V.sub(p, d), m.lbl[n], C.c4, 4, -6, 13); });
  const labelAt = (v, m, i, txt, col, bold) => { const [a, b] = m.bars[i], p = m.N[a], q = m.N[b], d = V.sub(q, p);
    if (Math.abs(d[0]) < 1e-6) v.text(V.add(p, V.mul(d, 0.3)), txt, col, 5, 0, 10.5, bold);
    else if (Math.abs(d[1]) < 1e-6) v.text(V.add(p, V.mul(d, 0.5)), txt, col, 0, -6, 10.5, bold, 'center');
    else v.text(V.add(p, V.mul(d, 0.64)), txt, col, 0, 4, 10.5, bold, 'center'); };
  const cx = (x, u) => { const c = nice(x); return c === '0' ? '0' : c === '1' ? u : c === '−1' ? '−' + u : c + '·' + u; };
  const barCol = (C, s) => Math.abs(s) < 1e-7 ? C.muted : s > 0 ? C.c2 : C.c1;
'''

# ---------------------------------------------------------------- 11.1 Pendelstütze
W.append(dict(file='11-1-pendelstuetze.html', title='Pendelstütze: Stabkraft S als Zug positiv',
  sub='Ein Stab eines idealen Fachwerks ist gelenkig angeschlossen, gewichtslos und nur an den Enden belastet. Gleichgewicht am Stab verlangt, dass beide Endkräfte auf der Stabachse liegen und entgegengesetzt gleich sind: S′ = −S. Eine Zahl S genügt; S > 0 heisst Zug, S < 0 Druck (Buch Gl. 11.1).',
  hint='Stabenden A und A′ ziehen, S einstellen, Querlast zuschalten.', legend=[('--c2', 'Zug (S > 0)'), ('--c1', 'Druck (S < 0)'), ('--c5', 'Kräfte auf die Knoten'), ('--c4', 'Querlast F')], js=TRUSS + r'''
  let A = [-1.6, -0.4], Cp = [1.5, 0.6], S = 1, quer = false;
  const view = MW.View2D(cv, { xmin: -3.4, xmax: 3.4, ymin: -1.9, ymax: 1.9 }, v => {
    const C = v.C, e = V.unit(V.sub(Cp, A)), n = [-e[1], e[0]], L = V.norm(V.sub(Cp, A)), col = barCol(C, S), k = 0.7;
    v.line(A, Cp, C.fg, 7); v.dot(A, C.bg, 6, true); v.dot(Cp, C.bg, 6, true); v.text(A, 'A', C.fg, -18, 18, 14); v.text(Cp, "A′", C.fg, 8, 18, 14);
    // Endkräfte auf den Stab: Zug zeigt nach aussen (äussere Normale e_N)
    const fA = V.mul(e, -S * k), fC = V.mul(e, S * k);
    if (!quer) { v.arrow(A, fA, col, 3.4, 12); v.arrow(Cp, fC, col, 3.4, 12); v.text(V.add(A, fA), 'S', col, -14, -6, 14); v.text(V.add(Cp, fC), "S′ = −S", col, 6, -6, 14);
      // Kräfte des Stabs auf die Knoten (Reaktionsprinzip): entgegengesetzt
      const off = V.mul(n, -0.55); const a2 = V.add(A, off), c2 = V.add(Cp, off);
      v.dot(a2, C.c5, 5); v.dot(c2, C.c5, 5); v.arrow(a2, V.mul(fA, -0.8), C.c5, 2.4, 10); v.arrow(c2, V.mul(fC, -0.8), C.c5, 2.4, 10);
      v.text(a2, 'Knoten A', C.c5, -30, 22, 12, false); v.text(c2, "Knoten A′", C.c5, -30, 22, 12, false); }
    else { const M = V.mul(V.add(A, Cp), 0.5), Fq = V.mul(n, -0.9); v.arrow(V.sub(M, Fq), Fq, C.c4, 3.4, 12); v.text(V.sub(M, Fq), 'F', C.c4, 6, 0, 14);
      const fA2 = V.add(fA, V.mul(n, 0.45)), fC2 = V.add(fC, V.mul(n, 0.45));
      v.arrow(A, fA2, C.c5, 3.2, 12); v.arrow(Cp, fC2, C.c5, 3.2, 12); v.text(V.add(A, fA2), 'Endkraft', C.c5, -40, -8, 12, false); v.text(V.add(Cp, fC2), 'Endkraft', C.c5, 4, -8, 12, false);
      v.line(A, V.add(A, V.mul(e, -1.2)), C.muted, 1, [4, 4]); v.line(Cp, V.add(Cp, V.mul(e, 1.2)), C.muted, 1, [4, 4]); }
    const rows = quer ? [['Querlast F in der Mitte', 'Querkomponenten F/2 an jedem Ende'], ['Endkräfte', 'nicht mehr auf der Stabachse']] :
      [['Stabkraft S', fmt(S, 2) + ' F'], ['Beanspruchung', Math.abs(S) < 1e-9 ? 'Nullstab' : S > 0 ? 'Zug (Pfeile zeigen vom Stab weg)' : 'Druck (Pfeile zeigen zum Stab hin)'], ['Stablänge', fmt(L, 2)]];
    MW.info(infoEl, quer ? 'Keine Pendelstütze: Querlast zwischen den Knoten' : 'Pendelstütze: S = S e_N, S′ = −S', rows,
      quer ? 'Mit einer Last zwischen den Enden braucht das Momentengleichgewicht Querkräfte an den Enden (Übungsheft Abb. 6.3). Beim Zerlegen müssen dann Kräfte quer zum Stab eingeführt werden.'
        : 'Die Knoten spüren die Gegenkräfte. Bei Zug ziehen die Stäbe an den Knoten, bei Druck drücken sie. Im Knotengleichgewicht führt man deshalb jede Stabkraft als Zug ein (Pfeil vom Knoten weg in den Stab).', quer);
  });
  view.handle(() => Cp, p => { Cp = p; }); view.handle(() => A, p => { A = p; });
  MW.slider(ctl, { label: 'S', min: -1.5, max: 1.5, step: 0.05, value: S, unit: ' F', onInput: x => { S = x; view.redraw(); } });
  MW.check(ctl, 'Querlast in Stabmitte', false, x => { quer = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 11.2 Abzählkriterium
W.append(dict(file='11-2-bestimmtheit.html', title='Statische Bestimmtheit: u = s + r − 2k', tall=True,
  sub='Ein ebenes ideales Fachwerk mit s Stäben, k Knoten und r Lagerkomponenten hat s + r Unbekannte und 2k Knotengleichungen. Der Grad der statischen Unbestimmtheit ist u = s + r − 2k (Buch Gl. 11.2). u = 0 ist notwendig, aber nicht hinreichend: Stäbe am falschen Ort machen das Fachwerk beweglich.',
  hint='Stäbe anklicken (ein/aus), Lager wählen oder ein Beispiel laden.', legend=[('--fg', 'vorhandener Stab'), ('--grid', 'möglicher Stab (aus)'), ('--c1', 'Mechanismus: Knotengeschwindigkeiten')], js=TRUSS + r'''
  const N = {}, cand = []; for (let i = 0; i < 4; i++) { N['u' + i] = [i, 0]; N['o' + i] = [i, 1]; }
  for (let i = 0; i < 3; i++) cand.push(['u' + i, 'u' + (i + 1)], ['o' + i, 'o' + (i + 1)], ['u' + i, 'o' + (i + 1)], ['o' + i, 'u' + (i + 1)]);
  for (let i = 0; i < 4; i++) cand.push(['u' + i, 'o' + i]);
  const key = b => b.join('-');
  const PRE = {
    n: { t: 'N-Träger (statisch bestimmt)', b: ['u0-u1', 'u1-u2', 'u2-u3', 'o0-o1', 'o1-o2', 'o2-o3', 'u0-o0', 'u1-o1', 'u2-o2', 'u3-o3', 'u0-o1', 'u1-o2', 'u2-o3'], l: 'fl' },
    plus: { t: 'Eine Diagonale zu viel (u = 1)', b: ['u0-u1', 'u1-u2', 'u2-u3', 'o0-o1', 'o1-o2', 'o2-o3', 'u0-o0', 'u1-o1', 'u2-o2', 'u3-o3', 'u0-o1', 'o0-u1', 'u1-o2', 'u2-o3'], l: 'fl' },
    falsch: { t: 'u = 0, aber beweglich', b: ['u0-u1', 'u1-u2', 'u2-u3', 'o0-o1', 'o1-o2', 'o2-o3', 'u0-o0', 'u1-o1', 'u2-o2', 'u3-o3', 'u0-o1', 'o0-u1', 'u2-o3'], l: 'fl' },
    lager: { t: 'Zwei Loslager (r = 2)', b: ['u0-u1', 'u1-u2', 'u2-u3', 'o0-o1', 'o1-o2', 'o2-o3', 'u0-o0', 'u1-o1', 'u2-o2', 'u3-o3', 'u0-o1', 'u1-o2', 'u2-o3'], l: 'll' },
    zwei: { t: 'Zwei Festlager (u = 1, äusserlich unbestimmt)', b: ['u0-u1', 'u1-u2', 'u2-u3', 'o0-o1', 'o1-o2', 'o2-o3', 'u0-o0', 'u1-o1', 'u2-o2', 'u3-o3', 'u0-o1', 'u1-o2', 'u2-o3'], l: 'ff' },
  };
  let on = new Set(PRE.n.b), lag = 'fl';
  const supOf = l => ({ fl: { u0: 'xy', u3: 'y' }, ll: { u0: 'y', u3: 'y' }, ff: { u0: 'xy', u3: 'xy' } }[l]);
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 3.6, ymin: -0.55, ymax: 1.45 }, v => {
    const C = v.C, bars = cand.filter(b => on.has(key(b))), m = { N, bars, sup: supOf(lag), loads: {} };
    const sys = eqSystem(m), s = bars.length, k = Object.keys(N).length, r = sys.cols.length - s, u = s + r - 2 * k;
    const At = sys.A[0].map((_, j) => sys.A.map(row => row[j]));               // Kompatibilität: Transponierte
    const kin = rref(At), eq = rref(sys.A), rank = eq.rank, dof = 2 * k - rank, red = s + r - rank;
    cand.forEach(b => { if (!on.has(key(b))) v.line(N[b[0]], N[b[1]], C.grid, 2, [5, 4]); });
    bars.forEach(b => v.line(N[b[0]], N[b[1]], C.fg, 3.4));
    Object.entries(m.sup).forEach(([n, t]) => drawSup(v, N[n], t, C));
    Object.keys(N).forEach(n => v.dot(N[n], C.fg, 5));
    if (dof > 0 && kin.null.length) { const x = kin.null[0], sc = 0.35 / Math.max(...x.map(Math.abs));
      Object.keys(N).forEach((n, i) => { const vel = [x[2 * i] * sc, x[2 * i + 1] * sc]; if (V.norm(vel) > 1e-6) v.arrow(N[n], vel, C.c1, 2.4, 9); }); }
    let head, warn = false;
    if (dof > 0) { head = (u >= 0 ? 'Beweglich (Mechanismus), obwohl u = ' + u : 'Beweglich: zu wenig Stäbe oder Lager') ; warn = true; }
    else if (red > 0) head = 'Statisch unbestimmt vom Grad ' + red;
    else head = 'Statisch bestimmt';
    MW.info(infoEl, head, [['Stäbe s', s], ['Lagerkomponenten r', r], ['Knoten k', k], ['u = s + r − 2k', u], ['Rang der Gleichgewichtsmatrix', rank + ' von 2k = ' + 2 * k], ['Freiheitsgrade des Mechanismus', dof]],
      dof > 0 ? 'Die roten Pfeile zeigen einen zulässigen Bewegungszustand: kein Stab ändert seine Länge (Satz der projizierten Geschwindigkeiten). Ein solches Fachwerk kann allgemeine Lasten nicht tragen.'
        : red > 0 ? 'Mehr Unbekannte als unabhängige Gleichungen. Die Stabkräfte hängen von den Verformungen ab (Festigkeitslehre, Band 2).' : 'Jede Stabkraft und jede Lagerkraft folgt eindeutig aus den 2k Knotengleichungen.', warn);
  });
  cv.addEventListener('click', e => { const r = cv.getBoundingClientRect(), p = view.toW(e.clientX - r.left, e.clientY - r.top); let best = null, bd = 0.12;
    cand.forEach(b => { const a = N[b[0]], c = N[b[1]], d = V.sub(c, a), t = Math.max(0, Math.min(1, V.dot(V.sub(p, a), d) / V.dot(d, d))), q = V.add(a, V.mul(d, t)), dist = V.norm(V.sub(p, q));
      if (dist < bd) { bd = dist; best = b; } });
    if (best) { const kk = key(best); on.has(kk) ? on.delete(kk) : on.add(kk); view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(PRE).map(([k, p]) => [k, p.t]), x => { on = new Set(PRE[x].b); lag = PRE[x].l; lagSel.set(lag); view.redraw(); });
  const lagSel = MW.select(ctl, 'Lager', [['fl', 'Festlager links, Loslager rechts (r = 3)'], ['ff', 'zwei Festlager (r = 4)'], ['ll', 'zwei Loslager (r = 2)']], x => { lag = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 11.2 Knotengleichgewicht
W.append(dict(file='11-2-knotengleichgewicht.html', title='Knotengleichgewicht: Knoten für Knoten zu allen Stabkräften', tall=True,
  sub='Zuerst die Lagerkräfte aus dem Gleichgewicht am ganzen Fachwerk. Dann jeden Knoten freischneiden, alle Stabkräfte als Zug einführen und Σ F<sub>x</sub> = 0, Σ F<sub>y</sub> = 0 aufstellen. Man beginnt an einem Knoten mit höchstens zwei unbekannten Stabkräften. Überzählige Gleichungen dienen als Kontrolle.',
  hint='Mit „Nächster Knoten“ durch die Rechnung gehen.', legend=[('--c2', 'Zug'), ('--c1', 'Druck'), ('--muted', 'noch unbekannt / Nullstab'), ('--c4', 'Lasten'), ('--c5', 'Lagerkräfte')], js=TRUSS + r'''
  let mk = 'buch', step = 0;
  const plan = m => { const keys = m.order || Object.keys(m.N), known = new Set(), seq = [], left = new Set(keys);
    while (left.size) { let pick = null; for (const k of (m.order ? [...left].sort((a, b) => keys.indexOf(a) - keys.indexOf(b)) : [...left])) {
        const unk = m.bars.map((b, i) => i).filter(i => m.bars[i].includes(k) && !known.has(i)); if (unk.length <= 2) { pick = [k, unk]; break; } }
      if (!pick) break; seq.push(pick); pick[1].forEach(i => known.add(i)); left.delete(pick[0]); }
    return seq; };
  let view;
  const draw = v => {
    const C = v.C, m = MODELS[mk], sol = solveTruss(m), seq = plan(m), done = new Set();
    seq.slice(0, step).forEach(([, unk]) => unk.forEach(i => done.add(i)));
    const cur = step > 0 ? seq[step - 1] : null;
    m.bars.forEach((b, i) => { const s = sol.S[i], kn = done.has(i), col = kn ? barCol(C, s) : C.muted, w = kn ? 2 + Math.min(5, Math.abs(s) * 4) : 2;
      v.line(m.N[b[0]], m.N[b[1]], col, w, kn && Math.abs(s) < 1e-7 ? [6, 4] : (kn ? null : [3, 3]));
      labelAt(v, m, i, kn ? barName(m, i) + ': ' + nice(s) : barName(m, i), kn ? col : C.muted, kn); });
    Object.entries(m.sup).forEach(([n, t]) => drawSup(v, m.N[n], t, C));
    drawLoads(v, m, C);
    Object.keys(m.N).forEach(n => { v.dot(m.N[n], C.fg, 4); v.text(m.N[n], n, C.fg, 6, 16, 13); });
    if (cur) { const [k, unk] = cur, p = m.N[k]; v.circle(p, 0.2, C.c5, 2);
      const rows = [], terms = [[], []];
      m.bars.forEach((b, i) => { if (!b.includes(k)) return; const e = unit(m, k === b[0] ? i : i, k), isU = unk.includes(i);
        v.arrow(p, V.mul(e, 0.42), isU ? C.c3 : barCol(C, sol.S[i]), isU ? 3.4 : 2.2, 10);
        [0, 1].forEach(d => { if (Math.abs(e[d]) > 1e-9) { const c = nice(e[d]); terms[d].push((c === '1' ? '' : c === '−1' ? '−' : c + '·') + sName(m, i)); } }); });
      if (m.sup[k]) { const R = sol.R[k]; [0, 1].forEach(d => { if (m.sup[k].includes('xy'[d])) { terms[d].push(k + '_' + 'xy'[d]); } });
        v.arrow(V.sub(p, V.mul(R, 0.3)), V.mul(R, 0.3), C.c5, 2.6, 10); }
      if (m.loads[k]) [0, 1].forEach(d => { const f = m.loads[k][d]; if (Math.abs(f) > 1e-9) terms[d].push(niceF(f)); });
      const eqs = terms.map((t, d) => ['Σ F_' + 'xy'[d], (t.join(' + ').replace(/\+ −/g, '− ') || '0') + ' = 0']);
      const res = unk.map(i => [sName(m, i), niceF(sol.S[i]) + (Math.abs(sol.S[i]) < 1e-7 ? ' (Nullstab)' : sol.S[i] > 0 ? ' (Zug)' : ' (Druck)')]);
      const ctrl = 2 - unk.length;
      MW.info(infoEl, 'Schritt ' + step + ' von ' + seq.length + ': Knoten ' + k + (unk.length ? ', Unbekannte ' + unk.map(i => sName(m, i)).join(', ') : ', nur Kontrolle'),
        [eqs[0], eqs[1], ...res], ctrl > 0 ? ctrl + (ctrl === 1 ? ' Gleichung bleibt' : ' Gleichungen bleiben') + ' als Kontrolle der bisherigen Werte übrig.' : 'Zwei Gleichungen, zwei Unbekannte.');
    } else { const lr = Object.entries(sol.R).map(([n, R]) => [n + '_x, ' + n + '_y', niceF(R[0]) + ',  ' + niceF(R[1])]);
      MW.info(infoEl, 'Schritt 0: Lagerkräfte aus dem Gleichgewicht am ganzen Fachwerk', lr, mk === 'buch' ? 'Beim Dreigelenkbogen braucht man für A_x, B_x zusätzlich die Momentenbedingung um C an einer Hälfte (Buch S. 163).' : 'Momentenbedingung um A liefert E_y, dann die Komponentenbedingungen (Übungsheft S. 71).');
      Object.entries(sol.R).forEach(([n, R]) => { const p = m.N[n]; v.arrow(V.sub(p, V.mul(R, 0.3)), V.mul(R, 0.3), C.c5, 2.6, 10); }); }
  };
  const box = () => MODELS[mk].box;
  let o = { ...box() }; view = MW.View2D(cv, o, draw);
  MW.select(ctl, 'Fachwerk', [['buch', MODELS.buch.name], ['ueb1', MODELS.ueb1.name]], x => { mk = x; step = 0; Object.assign(o, box()); view.redraw(); });
  MW.button(ctl, '◀ Zurück', () => { step = Math.max(0, step - 1); view.redraw(); });
  MW.button(ctl, 'Nächster Knoten ▶', () => { step = Math.min(plan(MODELS[mk]).length, step + 1); view.redraw(); });
  MW.button(ctl, 'Alle', () => { step = plan(MODELS[mk]).length; view.redraw(); });
'''))

# ---------------------------------------------------------------- 11.3 Dreikräfteschnitt
W.append(dict(file='11-3-dreikraefteschnitt.html', title='Dreikräfteschnitt (Ritterschnitt): eine Gleichung, eine Unbekannte', tall=True,
  sub='Man schneidet drei Stäbe, die nicht alle vom gleichen Knoten ausgehen, und betrachtet einen Teil. Die Momentenbedingung um den Schnittpunkt P der Achsen zweier geschnittener Stäbe enthält nur noch die dritte Stabkraft. Sind die beiden anderen Stäbe parallel, nimmt man die Komponentenbedingung senkrecht zu ihnen.',
  hint='Schnitt und gesuchte Stabkraft wählen.', legend=[('--c3', 'gesuchte Stabkraft'), ('--c2', 'andere geschnittene Stäbe (Zug angesetzt)'), ('--c4', 'Lasten'), ('--c5', 'Lagerkräfte'), ('--c1', 'Momentenpunkt P')], js=TRUSS + r'''
  const CUTS = {
    'b451': { m: 'buch', bars: [3, 4, 0], side: ['A', 'D', 'E'], t: 'Buch: Stäbe 4, 5, 1, linker Teil' },
    'b134': { m: 'buch', bars: [0, 2, 3], side: ['A', 'D'], t: 'Buch: Stäbe 1, 3, 4, linker Teil' },
    'b7810': { m: 'buch', bars: [6, 7, 9], side: ['G', 'B'], t: 'Buch Fig. 11.11: Stäbe 7, 8, 10, rechter Teil' },
    'b6710': { m: 'buch', bars: [5, 6, 9], side: ['G', 'H', 'B'], t: 'Buch: Stäbe 6, 7, 10, rechter Teil' },
    'u1': { m: 'ueb1', bars: [4, 17, 8], side: ['E', 'F', 'K', 'L'], t: 'Übungsheft Abb. 6.9: JK, DK, DE, rechter Teil' },
  };
  let ck = 'b7810', want = 0;
  const inter = (p1, d1, p2, d2) => { const det = d1[0] * (-d2[1]) - d1[1] * (-d2[0]); if (Math.abs(det) < 1e-9) return null;
    const r = V.sub(p2, p1), t = (r[0] * (-d2[1]) - r[1] * (-d2[0])) / det; return V.add(p1, V.mul(d1, t)); };
  const cr = (a, b) => a[0] * b[1] - a[1] * b[0];
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 3.6, ymin: -0.7, ymax: 1.6 }, v => {
    const C = v.C, cut = CUTS[ck], m = MODELS[cut.m], sol = solveTruss(m), side = new Set(cut.side);
    // Teil zeichnen
    m.bars.forEach((b, i) => { const inS = side.has(b[0]) && side.has(b[1]), isCut = cut.bars.includes(i);
      if (isCut) { const sn = side.has(b[0]) ? b[0] : b[1], on = sn === b[0] ? b[1] : b[0]; v.line(m.N[sn], V.add(m.N[sn], V.mul(V.sub(m.N[on], m.N[sn]), 0.45)), C.fg, 3);
        v.line(V.add(m.N[sn], V.mul(V.sub(m.N[on], m.N[sn]), 0.55)), m.N[on], C.grid, 2, [4, 4]); }
      else v.line(m.N[b[0]], m.N[b[1]], inS ? C.fg : C.grid, inS ? 3 : 2, inS ? null : [4, 4]);
      const mid = V.mul(V.add(m.N[b[0]], m.N[b[1]]), 0.5); if (m.num) v.text(mid, barName(m, i), inS || isCut ? C.muted : C.grid, -12, -4, 11, false); });
    Object.keys(m.N).forEach(n => { v.dot(m.N[n], side.has(n) ? C.fg : C.grid, 4); v.text(m.N[n], n, side.has(n) ? C.fg : C.grid, 6, 16, 13); });
    Object.entries(m.sup).forEach(([n, t]) => { if (side.has(n)) { const R = sol.R[n], p = m.N[n]; v.arrow(V.sub(p, V.mul(R, 0.3)), V.mul(R, 0.3), C.c5, 2.6, 10); } });
    Object.entries(m.loads).forEach(([n, f]) => { if (!side.has(n)) return; const d = V.mul(f, 0.42), p = m.N[n]; v.arrow(V.sub(p, d), d, C.c4, 3, 11); v.text(V.sub(p, d), m.lbl[n], C.c4, 4, -6, 13); });
    // Geschnittene Stäbe: Kraft am Teil als Zug (vom Knoten in Richtung des abgeschnittenen Knotens)
    const info = cut.bars.map(i => { const b = m.bars[i], sn = side.has(b[0]) ? b[0] : b[1]; return { i, p: m.N[sn], e: unit(m, i, sn) }; });
    info.forEach((c, j) => { v.arrow(c.p, V.mul(c.e, 0.4), j === want ? C.c3 : C.c2, j === want ? 3.6 : 2.4, 11); v.text(V.add(c.p, V.mul(c.e, 0.4)), sName(m, c.i), j === want ? C.c3 : C.c2, 4, -4, 13); });
    const k = info[want], o = info.filter((_, j) => j !== want), P = inter(o[0].p, o[0].e, o[1].p, o[1].e);
    // Bekannte äussere Kräfte am Teil
    const ext = []; cut.side.forEach(n => { if (m.loads[n]) ext.push([m.N[n], m.loads[n], m.lbl[n]]); if (sol.R[n]) ext.push([m.N[n], sol.R[n], n]); });
    let rows, head, note, res;
    if (P) { v.dot(P, C.c1, 6); v.text(P, 'P', C.c1, 8, -8, 15);
      v.line(o[0].p, P, C.c2, 1, [2, 4]); v.line(o[1].p, P, C.c2, 1, [2, 4]);
      const arm = cr(V.sub(k.p, P), k.e), Mext = ext.reduce((s, [p, f]) => s + cr(V.sub(p, P), f), 0); res = -Mext / arm;
      const foot = V.add(k.p, V.mul(k.e, V.dot(V.sub(P, k.p), k.e))); v.line(P, foot, C.c3, 1.4, [5, 3]); v.line(k.p, foot, C.c3, 1, [2, 3]);
      head = 'Momentenbedingung um P (Schnittpunkt von ' + o.map(c => sName(m, c.i)).join(' und ') + ')';
      rows = [['Hebelarm von ' + sName(m, k.i) + ' um P', nice(Math.abs(arm)) + ' L'], ['Moment der Lasten und Lagerkräfte um P', niceF(Mext) + 'L'], ['Gleichung', nice(arm) + 'L·' + sName(m, k.i) + ' + (' + niceF(Mext) + 'L) = 0']];
      note = 'Die Kräfte ' + o.map(c => sName(m, c.i)).join(', ') + ' gehen durch P und liefern kein Moment. P darf ausserhalb des Teils liegen.'; }
    else { const n = [-o[0].e[1], o[0].e[0]], comp = V.dot(k.e, n), Fext = ext.reduce((s, [, f]) => s + V.dot(f, n), 0); res = -Fext / comp;
      v.arrow(k.p, V.mul(n, 0.5), C.c1, 1.8, 9); v.text(V.add(k.p, V.mul(n, 0.5)), 'n', C.c1, 4, -4, 13);
      head = o.map(c => sName(m, c.i)).join(' und ') + ' sind parallel: Komponentenbedingung senkrecht dazu';
      rows = [['Richtung n', fv(n.map(x => +x.toFixed(3)))], ['Komponente von ' + sName(m, k.i), nice(comp) + '·' + sName(m, k.i)], ['Lasten und Lagerkräfte in n', niceF(Fext)]];
      note = 'Bei parallelen Stäben gibt es keinen Schnittpunkt. Die Komponente senkrecht zu ihnen enthält nur die gesuchte Stabkraft (Buch S. 168, Stab 8).'; }
    rows.push([sName(m, k.i), niceF(res) + (Math.abs(res) < 1e-7 ? ' (Nullstab)' : res > 0 ? ' (Zug)' : ' (Druck)')], ['Kontrolle Knotengleichgewicht', niceF(sol.S[k.i])]);
    MW.info(infoEl, head, rows, note);
  });
  const sel = MW.select(ctl, 'Schnitt', Object.entries(CUTS).map(([k, c]) => [k, c.t]), x => { ck = x; want = 0; wsel.set(0); view.redraw(); });
  sel.set(ck);
  const wsel = MW.select(ctl, 'Gesucht', [[0, '1. geschnittener Stab'], [1, '2. geschnittener Stab'], [2, '3. geschnittener Stab']], x => { want = +x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 11.4 PdvL
W.append(dict(file='11-4-pdvl.html', title='PdvL: Stab entfernen, Mechanismus bewegen, P = 0', tall=True,
  sub='Man entfernt den Stab mit der gesuchten Stabkraft und ersetzt ihn durch die Kräfte S und −S an seinen Knoten (Zug angesetzt). Das statisch bestimmte Fachwerk wird so zum Mechanismus mit einem Freiheitsgrad. Für jeden zulässigen Bewegungszustand gilt P = 0. Lagerkräfte leisten nichts und werden nicht gebraucht.',
  hint='Stab wählen, Auslenkung schieben.', legend=[('--c1', 'Geschwindigkeiten (Bewegungszustand)'), ('--c3', 'Stabkräfte S, −S'), ('--c4', 'Lasten'), ('--muted', 'ausgelenkte Lage')], js=TRUSS + r'''
  let mk = 'buch', rem = 7, eps = 0.25;
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 3.6, ymin: -0.8, ymax: 1.9 }, v => {
    const C = v.C, m0 = MODELS[mk], keys = Object.keys(m0.N), bars = m0.bars.filter((_, i) => i !== rem);
    // Kompatibilität: (v_i − v_j)·e_ij = 0 für alle verbleibenden Stäbe, Lagerbindungen
    const rows = []; bars.forEach(([a, b]) => { const e = V.unit(V.sub(m0.N[b], m0.N[a])), r = new Array(2 * keys.length).fill(0), ia = keys.indexOf(a), ib = keys.indexOf(b);
      r[2 * ia] = -e[0]; r[2 * ia + 1] = -e[1]; r[2 * ib] = e[0]; r[2 * ib + 1] = e[1]; rows.push(r); });
    Object.entries(m0.sup).forEach(([n, t]) => [0, 1].forEach(d => { if (t.includes('xy'[d])) { const r = new Array(2 * keys.length).fill(0); r[2 * keys.indexOf(n) + d] = 1; rows.push(r); } }));
    const ns = rref(rows).null;
    if (ns.length !== 1) { MW.info(infoEl, 'Kein Mechanismus mit einem Freiheitsgrad', [['Freiheitsgrade', ns.length]], '', true); return; }
    let x = ns[0]; const vel = {}; keys.forEach((n, i) => vel[n] = [x[2 * i], x[2 * i + 1]]);
    // Normierung: Rotationsschnelligkeit ω = 1 eines Körpers, der sich um ein festes Lager dreht (Geschwindigkeiten in ωL)
    let om = 0, omTxt = ''; for (const [n, t] of Object.entries(m0.sup)) { if (t !== 'xy' || om) continue;
      for (const [a, b] of bars) { if (a !== n && b !== n) continue; const j = a === n ? b : a, r = V.sub(m0.N[j], m0.N[n]), w = (r[0] * vel[j][1] - r[1] * vel[j][0]) / V.dot(r, r);
        if (Math.abs(w) > 1e-6) { om = w; omTxt = 'Drehung um ' + n; break; } } }
    if (!om) om = Math.max(...keys.map(n => V.norm(vel[n])));
    keys.forEach(n => { vel[n] = V.mul(vel[n], 1 / om); });
    const vmax = Math.max(...keys.map(n => V.norm(vel[n])));
    const [ra, rb] = m0.bars[rem], e = V.unit(V.sub(m0.N[rb], m0.N[ra]));
    let Pl = 0; const terms = [];
    Object.entries(m0.loads).forEach(([n, f]) => { const p = V.dot(f, vel[n]); Pl += p; terms.push([m0.lbl[n] + ' in ' + n + ':  F·v_' + n, cx(p, 'FωL')]); });
    const cS = V.dot(e, V.sub(vel[ra], vel[rb])), S = -Pl / cS;
    // ausgelenkte Lage
    const Nd = {}; keys.forEach(n => Nd[n] = V.add(m0.N[n], V.mul(vel[n], eps * 0.4 / vmax)));
    bars.forEach(([a, b]) => v.line(Nd[a], Nd[b], C.muted, 1.4, [5, 4]));
    m0.bars.forEach((b, i) => { if (i === rem) { v.line(m0.N[b[0]], m0.N[b[1]], C.c3, 1.4, [6, 5]); return; } v.line(m0.N[b[0]], m0.N[b[1]], C.fg, 3); });
    Object.entries(m0.sup).forEach(([n, t]) => drawSup(v, m0.N[n], t, C));
    drawLoads(v, m0, C);
    keys.forEach(n => { v.dot(m0.N[n], C.fg, 4); v.text(m0.N[n], n, C.fg, 6, 16, 13); if (V.norm(vel[n]) > 1e-6) v.arrow(m0.N[n], V.mul(vel[n], 0.5 / vmax), C.c1, 2.4, 9); });
    v.arrow(m0.N[ra], V.mul(e, 0.35), C.c3, 3.2, 10); v.arrow(m0.N[rb], V.mul(e, -0.35), C.c3, 3.2, 10);
    v.text(V.add(m0.N[ra], V.mul(e, 0.35)), 'S', C.c3, 4, -4, 14); v.text(V.add(m0.N[rb], V.mul(e, -0.35)), '−S', C.c3, 4, -4, 14);
    const sol = solveTruss(m0);
    MW.info(infoEl, 'Stab ' + barName(m0, rem) + ' entfernt: P = Σ F·v + S·e·(v_' + ra + ' − v_' + rb + ') = 0', [...terms,
      ['Stabkraft:  S·e·(v_' + ra + ' − v_' + rb + ')', cx(cS, 'S·ωL')], [sName(m0, rem) + ' = −(Σ F·v) / (' + cx(cS, 'ωL') + ')', niceF(S) + (Math.abs(S) < 1e-7 ? ' (Nullstab)' : S > 0 ? ' (Zug)' : ' (Druck)')],
      ['Kontrolle Knotengleichgewicht', niceF(sol.S[rem])]],
      'Normierung: ' + omTxt + ' mit Rotationsschnelligkeit ω, Geschwindigkeiten in ωL; ω kürzt sich heraus. Feste Lager haben v = 0, ihre Lagerkräfte leisten also nichts. Kontrolle: Geschwindigkeiten an jedem verbleibenden Stab erfüllen den Satz der projizierten Geschwindigkeiten.');
  });
  const opts = m => m.bars.map((_, i) => [i, 'Stab ' + barName(m, i)]);
  const msel = MW.select(ctl, 'Fachwerk', [['buch', MODELS.buch.name], ['ueb1', MODELS.ueb1.name]], x => { mk = x; rem = x === 'buch' ? 7 : 17; rebuild(); view.redraw(); });
  let bsel; const rebuild = () => { if (bsel) bsel.el && bsel.el.remove(); const s = document.createElement('label'); s.textContent = 'Stab '; const se = document.createElement('select');
    opts(MODELS[mk]).forEach(([v, t]) => { const o = document.createElement('option'); o.value = v; o.textContent = t; se.appendChild(o); }); se.value = rem;
    se.addEventListener('change', () => { rem = +se.value; view.redraw(); }); s.appendChild(se); ctl.insertBefore(s, ctl.children[1] || null); bsel = { el: s }; };
  rebuild();
  MW.slider(ctl, { label: 'Auslenkung', min: -1, max: 1, step: 0.05, value: eps, onInput: x => { eps = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 11.5 Tetraeder
W.append(dict(file='11-5-tetraeder.html', title='Räumliches Fachwerk: Tetraeder mit Last F in der Spitze', tall=True,
  sub='Im Raum liefert jeder Knoten drei Komponentenbedingungen, also u = s + r − 3k (Buch Gl. 11.3). Beim Tetraeder (s = 6, k = 4) braucht es r = 6 Lagerkomponenten. Mit der Last F in der Spitze D tragen die drei Schrägstäbe Druck und die drei Grundstäbe Zug (Mitschrift S. 81–82).',
  hint='Höhe der Spitze ändern, Ansicht ziehen.', legend=[('--c2', 'Zug'), ('--c1', 'Druck'), ('--c4', 'Last F'), ('--c5', 'Lagerkräfte F/3')], js=TRUSS + r'''
  let H = Math.sqrt(2 / 3);
  const view = MW.View3D(cv, { extent: 0.85, yaw: -60, pitch: 20, center: [0.5, 0.29, 0.4] }, v => {
    const C = v.C, A = [0, 0, 0], B = [1, 0, 0], Cc = [0.5, h3, 0], M = [0.5, h3 / 3, 0], D = [0.5, h3 / 3, H];
    const l = Math.hypot(1 / Math.sqrt(3), H), sa = H / l, ca = (1 / Math.sqrt(3)) / l;
    const Sleg = -1 / (3 * sa), Sbase = -Sleg * ca / Math.sqrt(3);
    [[A, B], [B, Cc], [Cc, A]].forEach(([p, q]) => v.line(p, q, C.c2, 2 + Sbase * 3));
    [A, B, Cc].forEach(p => v.line(p, D, C.c1, 2 + Math.min(6, -Sleg * 3)));
    v.arrow(V.add(D, [0, 0, 0.45]), [0, 0, -0.45], C.c4, 3, 11); v.text(V.add(D, [0, 0, 0.45]), 'F', C.c4, 6, 0, 14);
    [A, B, Cc].forEach(p => { v.arrow(V.add(p, [0, 0, -0.3]), [0, 0, 0.3], C.c5, 2.4, 9); });
    [['A', A], ['B', B], ['C', Cc], ['D', D]].forEach(([n, p]) => { v.dot(p, C.fg, 4); v.text(p, n, C.fg, 6, -6, 14); });
    v.line(D, M, C.muted, 1, [3, 3]);
    const reg = Math.abs(H - Math.sqrt(2 / 3)) < 0.01;
    MW.info(infoEl, reg ? 'Regelmässiges Tetraeder: H = L√(2/3)' : 'Spitze in der Höhe H = ' + fmt(H, 2) + ' L', [['Neigung der Schrägstäbe sin α', fmt(sa, 3)],
      ['Knoten D, z-Richtung', '3·S_schräg·sin α + F = 0'], ['S_schräg', (reg ? nice(Sleg) : fmt(Sleg, 3)) + ' F  (Druck)'],
      ['Knoten A, horizontal', '√3·S_grund + S_schräg·cos α = 0'], ['S_grund', (reg ? nice(Sbase) : fmt(Sbase, 3)) + ' F  (Zug)'], ['Lagerkraft je Fusspunkt', 'F/3 (vertikal)']],
      'Regelmässig: S_schräg = −(F/3)√(3/2), S_grund = (F/9)√(3/2) (Mitschrift S. 82). Je flacher das Tetraeder, desto grösser werden alle Stabkräfte.');
  });
  const hs = MW.slider(ctl, { label: 'H / L', min: 0.2, max: 1.6, step: 0.01, value: H, onInput: x => { H = x; view.redraw(); } });
  MW.button(ctl, 'Regelmässig', () => { H = Math.sqrt(2 / 3); hs.set(H); view.redraw(); });
'''))

if __name__ == '__main__':
    print(build('kap11', W))
