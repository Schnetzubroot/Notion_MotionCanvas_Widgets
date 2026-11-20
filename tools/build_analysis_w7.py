"""Widgets zu Analysis I, Woche 7: Anhang A Polynome und Nullstellen, Crashkurs lineare DGL (Vorlesung 15 vom
26.10.2026), Kap. II.5 Exponential-, Logarithmus- und hyperbolische Funktionen, II.6 Grössenordnungen
(Stammbach, Teil C, Anhang S. 20-23 und Kap. VII S. 83-85; Teil A, Kap. II S. 35-56;
Vorlesungsnotizen Kap. A S. 7-10, Kap. II S. 20-30)."""
from template import build
from build_analysis_w1 import AX, BOX
from build_analysis_w6 import CPLX

TALL = '{ xmin: -0.75, xmax: 6.25, ymin: -0.55, ymax: 3.75 }'
# gestrichelter Graph und Umrechnung Welt -> Achsenkoordinaten
EXTRA = r'''
  function dplot(v, A, f, color, w = 1.3, N = 300, a = A.x0, b = A.x1) { let seg = [];
    const fl = () => { if (seg.length > 1) v.poly(seg, color, w, [5, 4]); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x); if (!isFinite(y) || !A.inY(y)) { fl(); continue; } seg.push(A.P(x, y)); } fl(); }
  const inv = (A, p) => [A.x0 + (p[0] - A.ox) / A.W * (A.x1 - A.x0), A.y0 + (p[1] - A.oy) / A.H * (A.y1 - A.y0)];
  const sci = x => !isFinite(x) ? '–' : (x !== 0 && (Math.abs(x) >= 1e6 || Math.abs(x) < 1e-4)) ? x.toExponential(3).replace('.', ',').replace(/e\+?(-?)(\d+)/, (m, s, d) => ' · 10^' + (s ? '−' : '') + d) : fmt(x, 5);
'''

W = []

# ---------------------------------------------------------------- A.5
W.append(dict(file='A-5-nullstellen-polynome.html', title='Nullstellen reeller Polynome: komplexe Nullstellen kommen in Paaren',
  sub='Links die Nullstellen in der komplexen Ebene, rechts der Graph von p(x) für reelle x. Mit z₀ ist auch z̄₀ eine Nullstelle. Der Graph zeigt nur die reellen Nullstellen. Die Vielfachheiten zusammen ergeben immer den Grad.',
  hint='z₀ und die reellen Nullstellen ziehen. z₀ auf die reelle Achse ziehen: doppelte reelle Nullstelle.', legend=[('--c1', 'komplexes Paar z₀, z̄₀'), ('--c3', 'reelle Nullstellen'), ('--c2', 'p(x)')], js=AX + EXTRA + CPLX + r'''
  const L = mkAx(-2.4, 2.4, -2.4, 2.4, 3.3, 3.3, -0.6, 0), G = mkAx(-2.4, 2.4, -6, 6, 3.05, 3.3, 3.1, 0);
  const s3 = Math.sqrt(3) / 2;
  const EX = { g2: ['Grad 2: α² − 2α + 2 (Vorlesung A S. 10)', 2, [1, 1], []], g3: ['Grad 3: x³ − 1 (Vorlesung A S. 10)', 3, [-0.5, s3], [1]],
    g4: ['Grad 4: x⁴ − x (Vorlesung A S. 10)', 4, [-0.5, s3], [0, 1]], g4b: ['Grad 4: (x² + 1)(x² − 4) (eigenes Beispiel)', 4, [0, 1], [-2, 2]] };
  let gr = 2, z0 = [1, 1], R = [];
  const coeffs = () => { let c = [z0[0] * z0[0] + z0[1] * z0[1], -2 * z0[0], 1];   // aufsteigend
    R.slice(0, gr - 2).forEach(r => { const d = [0].concat(c); for (let i = 0; i < c.length; i++) d[i] -= r * c[i]; c = d; }); return c; };
  const ev = (c, x) => c.reduceRight((s, a) => s * x + a, 0);
  const sup = k => String(k).split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[+d]).join('');
  const pstr = c => { let s = ''; for (let k = c.length - 1; k >= 0; k--) { const a = Math.round(c[k] * 1000) / 1000; if (a === 0) continue;
      const m = k === 0 || Math.abs(a) !== 1 ? fmt(Math.abs(a), 3) : ''; s += (s ? (a < 0 ? ' − ' : ' + ') : (a < 0 ? '−' : '')) + m + (k ? 'x' + (k > 1 ? sup(k) : '') : ''); } return s || '0'; };
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C;
    for (let k = -2; k <= 2; k++) { v.line(L.P(k, -2.4), L.P(k, 2.4), C.grid, 1); v.line(L.P(-2.4, k), L.P(2.4, k), C.grid, 1); }
    v.line(L.P(-2.4, 0), L.P(2.4, 0), C.muted, 1.3); v.line(L.P(0, -2.4), L.P(0, 2.4), C.muted, 1.3);
    v.text(L.P(2.4, 0), 'Re', C.muted, -4, -6, 12, false, 'right'); v.text(L.P(0, 2.4), 'Im', C.muted, 6, 12, 12, false);
    axes(v, G, 'x', 'p(x)', 1, 2);
    const real = Math.abs(z0[1]) < 1e-9, c = coeffs(), rs = R.slice(0, gr - 2);
    v.line(L.P(z0[0], z0[1]), L.P(z0[0], -z0[1]), C.c1, 1, [3, 3]);
    v.dot(L.P(z0[0], z0[1]), C.c1, 6.5); v.dot(L.P(z0[0], -z0[1]), C.c1, 6.5, true);
    if (!real) { v.text(L.P(z0[0], z0[1]), 'z₀', C.c1, 8, -6, 13); v.text(L.P(z0[0], -z0[1]), 'z̄₀', C.c1, 8, 16, 13); }
    rs.forEach((r, i) => { v.dot(L.P(r, 0), C.c3, 6); v.text(L.P(r, 0), 'x' + '₁₂'[i], C.c3, -4, 18, 12); });
    fplot(v, G, x => ev(c, x), C.c2, 2.5, 800);
    // Nullstellen mit Vielfachheit
    const all = [[z0[0], z0[1]], [z0[0], -z0[1]]].concat(rs.map(r => [r, 0])), cl = [];
    all.forEach(p => { const f = cl.find(q => Math.hypot(q.p[0] - p[0], q.p[1] - p[1]) < 1e-6); if (f) f.k++; else cl.push({ p, k: 1 }); });
    const reals = cl.filter(q => Math.abs(q.p[1]) < 1e-9);
    reals.forEach(q => { v.dot(G.P(q.p[0], 0), C.c3, 5.5); if (q.k > 1) v.text(G.P(q.p[0], 0), q.k + '-fach', C.c3, 0, 18, 11, true, 'center'); });
    const list = cl.map(q => cs(q.p) + (q.k > 1 ? ' (' + q.k + '-fach)' : '')).join(',  ');
    const multi = cl.some(q => q.k > 1);
    MW.info(infoEl, 'p(x) = ' + pstr(c), [['Nullstellen', list], ['verschiedene reelle Nullstellen', String(reals.length)],
      ['nicht reelle Nullstellen', real ? '0' : '2 (z₀ und z̄₀)'], ['Summe der Vielfachheiten', cl.reduce((s, q) => s + q.k, 0) + ' = Grad ' + gr],
      ['(x − z₀)(x − z̄₀)', 'x² − 2 Re z₀ · x + |z₀|² = ' + pstr([z0[0] ** 2 + z0[1] ** 2, -2 * z0[0], 1])]],
      'Skript Anhang S. 20–23: Jedes Polynom vom Grad n ≥ 1 hat eine Nullstelle (Fundamentalsatz, S. 20) und zerfällt in n Linearfaktoren (S. 21). Bei reellen Koeffizienten ist mit z₀ auch z̄₀ Nullstelle, und (z − z₀)(z − z̄₀) ist ein reelles quadratisches Polynom (S. 22–23). '
      + (multi ? 'Hier gibt es eine mehrfache Nullstelle: Bei gerader Vielfachheit berührt der Graph die x-Achse nur.' : 'Vorlesung A S. 9: Bei ungeradem Grad bleibt mindestens eine reelle Nullstelle übrig.'));
  });
  const snapC = p => { const q = [Math.round(p[0] * 4) / 4, Math.round(p[1] * 4) / 4]; return [Math.max(-2.25, Math.min(2.25, q[0])), Math.max(-2.25, Math.min(2.25, q[1]))]; };
  view.handle(() => L.P(z0[0], z0[1]), p => { z0 = snapC(inv(L, p)); });
  [0, 1].forEach(i => view.handle(() => gr - 2 > i ? L.P(R[i], 0) : [99, 99], p => { R[i] = snapC(inv(L, p))[0]; }));
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([k, e]) => [k, e[0]]), u => { const e = EX[u]; gr = e[1]; z0 = e[2].slice(); R = e[3].slice(); view.redraw(); }).set('g2');
'''))

# ---------------------------------------------------------------- A.6
W.append(dict(file='A-6-dgl-ansatz.html', title='Lineare DGL y″ + p y′ + q y = 0: Ansatz y = eᵅˣ',
  sub='Der Ansatz y = eᵅˣ führt auf das Polynom α² + pα + q = 0. Links seine Nullstellen in der komplexen Ebene, rechts die Lösung zu den Anfangswerten y(0) und y′(0). Komplexe Nullstellen μ ± iω geben eine Schwingung e^(μx)(A cos ωx + B sin ωx).',
  hint='p und q einstellen, Anfangswerte verschieben.', legend=[('--c1', 'Nullstellen α'), ('--c2', 'Lösung y(x)'), ('--muted', 'Hüllkurve ±√(A² + B²) e^(μx)')], js=AX + EXTRA + CPLX + r'''
  const L = mkAx(-3, 3, -3, 3, 2.1, 2.1, -0.65, 1.4), G = mkAx(-2, 6, -6, 6, 3.95, 3.6, 2.05, -0.3);
  const EX = { lec: ['y″ − 2y′ + 2y = 0 (Vorlesung A S. 9–10)', -2, 2, 1, 0], harm: ['y″ + 4y = 0, ω = 2 (Skript Anhang S. 12)', 0, 4, 1, 0],
    damp: ['y″ + 0.6y′ + 4y = 0, gedämpft (eigenes Beispiel)', 0.6, 4, 2, 0], real: ['y″ − y′ − 2y = 0, reelle α (eigenes Beispiel)', -1, -2, 1, 0] };
  let p = -2, q = 2, y0 = 1, v0 = 0;
  const view = MW.View2D(cv, ''' + TALL + r''', v => {
    const C = v.C;
    for (let k = -3; k <= 3; k++) { v.line(L.P(k, -3), L.P(k, 3), C.grid, 1); v.line(L.P(-3, k), L.P(3, k), C.grid, 1); }
    v.line(L.P(-3, 0), L.P(3, 0), C.muted, 1.2); v.line(L.P(0, -3), L.P(0, 3), C.muted, 1.2);
    v.text(L.P(3, 0), 'Re α', C.muted, -2, -6, 11, false, 'right'); v.text(L.P(0, 3), 'Im α', C.muted, 5, 12, 11, false);
    v.text(L.P(-3, 3), 'α² + pα + q = 0', C.fg, 0, -10, 12);
    axes(v, G, 'x', 'y', 1, 2);
    const Dis = p * p - 4 * q; let y, al, gen, note, env = null;
    if (Dis > 1e-9) { const a1 = (-p + Math.sqrt(Dis)) / 2, a2 = (-p - Math.sqrt(Dis)) / 2, A = (v0 - a2 * y0) / (a1 - a2), B = y0 - A;
      y = x => A * Math.exp(a1 * x) + B * Math.exp(a2 * x); al = [[a1, 0], [a2, 0]];
      gen = 'y = A e^(' + fmt(a1, 3) + 'x) + B e^(' + fmt(a2, 3) + 'x)'; note = 'Zwei reelle Nullstellen: Der gleiche Ansatz liefert direkt zwei reelle Lösungen (Skript Teil C, Kap. VII S. 83–84). In der Vorlesung kam nur der komplexe Fall vor.';
      gen += ',  A = ' + fmt(A, 3) + ', B = ' + fmt(B, 3); }
    else if (Dis >= -1e-9) { const a = -p / 2, A = y0, B = v0 - a * y0; y = x => (A + B * x) * Math.exp(a * x); al = [[a, 0], [a, 0]];
      gen = 'y = (A + Bx) e^(' + fmt(a, 3) + 'x),  A = ' + fmt(A, 3) + ', B = ' + fmt(B, 3);
      note = 'Doppelte Nullstelle: Die zweite Lösung ist x · eᵅˣ. Das ist ausserhalb der Vorlesungsnotizen; es steht im Skript Teil C, Kap. VII S. 84.'; }
    else { const mu = -p / 2, om = Math.sqrt(-Dis) / 2, A = y0, B = (v0 - mu * y0) / om; y = x => Math.exp(mu * x) * (A * Math.cos(om * x) + B * Math.sin(om * x));
      al = [[mu, om], [mu, -om]]; env = x => Math.hypot(A, B) * Math.exp(mu * x);
      gen = 'y = e^(' + fmt(mu, 3) + 'x)(A cos ' + fmt(om, 3) + 'x + B sin ' + fmt(om, 3) + 'x),  A = ' + fmt(A, 3) + ', B = ' + fmt(B, 3);
      note = 'Vorlesung A S. 9–10: e^((μ ± iω)x) = e^(μx)(cos ωx ± i sin ωx) löst die DGL komplex. Real- und Imaginärteil sind dann reelle Lösungen. Für y″ − 2y′ + 2y = 0 ist α = 1 ± i und y = A eˣ cos x + B eˣ sin x. '
        + (mu > 1e-9 ? 'μ > 0: die Schwingung wächst.' : mu < -1e-9 ? 'μ < 0: die Schwingung klingt ab.' : 'μ = 0: reine Schwingung mit Kreisfrequenz ω.'); }
    if (env) { dplot(v, G, env, C.muted); dplot(v, G, x => -env(x), C.muted); }
    fplot(v, G, y, C.c2, 2.5, 900);
    v.dot(G.P(0, y0), C.fg, 5.5); const h = 0.5; v.line(G.P(-h, y0 - v0 * h), G.P(h, y0 + v0 * h), C.c3, 2);
    al.forEach((a, i) => { if (Math.abs(a[0]) <= 3 && Math.abs(a[1]) <= 3) { v.dot(L.P(a[0], a[1]), C.c1, 6, i === 1 && Dis < 0); } });
    if (Dis < -1e-9) v.text(L.P(al[0][0], al[0][1]), 'μ + iω', C.c1, 8, -4, 11);
    MW.info(infoEl, 'α² ' + (p < 0 ? '− ' : '+ ') + fmt(Math.abs(p), 2) + 'α ' + (q < 0 ? '− ' : '+ ') + fmt(Math.abs(q), 2) + ' = 0', [
      ['Nullstellen α', Dis < -1e-9 ? cs(al[0]) + ',  ' + cs(al[1]) : al[0][0] === al[1][0] ? fmt(al[0][0], 4) + ' (doppelt)' : fmt(al[0][0], 4) + ',  ' + fmt(al[1][0], 4)],
      ['Lösung', gen], ['Anfangswerte', 'y(0) = ' + fmt(y0, 2) + ',  y′(0) = ' + fmt(v0, 2)]], note);
  });
  const sp = MW.slider(ctl, { label: 'p', min: -4, max: 4, step: 0.1, value: p, onInput: u => { p = u; view.redraw(); } });
  const sq = MW.slider(ctl, { label: 'q', min: -4, max: 6, step: 0.1, value: q, onInput: u => { q = u; view.redraw(); } });
  const sy = MW.slider(ctl, { label: 'y(0)', min: -3, max: 3, step: 0.1, value: y0, onInput: u => { y0 = u; view.redraw(); } });
  const sv = MW.slider(ctl, { label: 'y′(0)', min: -3, max: 3, step: 0.1, value: v0, onInput: u => { v0 = u; view.redraw(); } });
  MW.select(ctl, 'Beispiel', Object.entries(EX).map(([k, e]) => [k, e[0]]), u => { const e = EX[u]; [p, q, y0, v0] = e.slice(1); sp.set(p); sq.set(q); sy.set(y0); sv.set(v0); view.redraw(); }).set('lec');
'''))

# ---------------------------------------------------------------- 5.1
W.append(dict(file='5-1-exponentialfunktion-e.html', title='Exponentialfunktion und die Zahl e',
  sub='eˣ ist die Lösung von f′ = f mit f(0) = 1. Daraus folgen eˣ ≥ 1 + x, die Schranken (1 + 1/n)ⁿ < e < (1 + 1/(n − 1))ⁿ und damit e = lim (1 + 1/n)ⁿ, sowie die Reihe eˣ = Σ xᵏ/k!.',
  hint='Ansicht wählen, dann n bzw. x verschieben.', legend=[('--c2', 'eˣ bzw. e'), ('--c1', 'untere Schranke / Teilsumme'), ('--c4', 'obere Schranke'), ('--c3', 'Tangente 1 + x')], js=AX + EXTRA + r'''
  const fac = k => { let s = 1; for (let i = 2; i <= k; i++) s *= i; return s; };
  const T = (n, x) => { let s = 0; for (let k = 0; k <= n; k++) s += x ** k / fac(k); return s; };
  let mode = 'folge', N = 10, x0 = 1, n = 3;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, E = Math.E;
    if (mode === 'folge') {
      const A = mkAx(0, N + 1, 1.9, 4.1); axes(v, A, 'n', '', N > 30 ? 10 : N > 12 ? 5 : 1, 0.5);
      v.line(A.P(0, E), A.P(N + 1, E), C.c2, 1.8, [6, 4]); v.text(A.P(N + 1, E), 'e', C.c2, -12, -6, 13);
      for (let k = 1; k <= N; k++) { v.dot(A.P(k, (1 + 1 / k) ** k), C.c1, 4); if (k >= 2) v.dot(A.P(k, (1 + 1 / (k - 1)) ** k), C.c4, 4); }
      const a = (1 + 1 / N) ** N, b = (1 + 1 / (N - 1)) ** N;
      MW.info(infoEl, 'n = ' + N + ':  ' + fmt(a, 5) + ' < e < ' + fmt(b, 5), [['aₙ = (1 + 1/n)ⁿ', fmt(a, 6)], ['(1 + 1/(n − 1))ⁿ', fmt(b, 6)], ['e', fmt(E, 6)], ['Breite', fmt(b - a, 6)]],
        'Vorlesung S. 21–22, Skript S. 38–39: e = (e^(1/n))ⁿ > (1 + 1/n)ⁿ wegen eˣ > 1 + x. Genauso 1/e = (e^(−1/n))ⁿ > (1 − 1/n)ⁿ. Beide Schranken streben gegen denselben Grenzwert, also e = lim (1 + 1/n)ⁿ ≈ 2.718.');
    } else if (mode === 'tangente') {
      const A = mkAx(-2.5, 2, -1, 7); axes(v, A, 'x', 'y', 0.5, 1);
      fplot(v, A, Math.exp, C.c2, 2.5); fplot(v, A, x => 1 + x, C.c3, 2);
      const e = Math.exp(x0), t = 1 + x0; v.line(A.P(x0, t), A.P(x0, e), C.c1, 3); v.dot(A.P(x0, e), C.c2, 5); v.dot(A.P(x0, t), C.c3, 5); v.dot(A.P(0, 1), C.fg, 5);
      MW.info(infoEl, 'eˣ − (1 + x) = ' + fmt(e - t, 5) + ' ≥ 0', [['x', fmt(x0, 3)], ['eˣ', fmt(e, 5)], ['1 + x', fmt(t, 5)]],
        'Vorlesung S. 22: Die Tangente an eˣ bei 0 ist t(x) = 1 + x, und eˣ ≥ 1 + x mit Gleichheit nur bei x = 0. Begründung: für x > 0 ist (eˣ)′ > 1 = (1 + x)′, für x < 0 ist (eˣ)′ < 1. Skript S. 38: f″ = f > 0, der Graph ist nach links gekrümmt.');
    } else {
      const A = mkAx(-3, 3, -2, 12); axes(v, A, 'x', 'y', 1, 2);
      fplot(v, A, Math.exp, C.c2, 2.6); fplot(v, A, x => T(n, x), C.c1, 2.2);
      const s1 = T(n, 1); v.dot(A.P(1, s1), C.c1, 5); v.dot(A.P(1, E), C.c2, 5);
      MW.info(infoEl, 'Teilsumme mit Grad n = ' + n, [['Tₙ(x) = Σₖ₌₀ⁿ xᵏ/k!', n === 0 ? '1' : '1 + x' + (n >= 2 ? ' + x²/2' : '') + (n >= 3 ? ' + x³/6' : '') + (n >= 4 ? ' + … + xⁿ/' + fac(n) : '')], ['Tₙ(1)', fmt(s1, 7)], ['e − Tₙ(1)', sci(E - s1)]],
        'Vorlesung S. 23, Skript S. 39–40: Ansatz exp(x) = Σ bₙxⁿ. Aus exp′ = exp folgt bₙ₊₁ = bₙ/(n + 1), mit b₀ = 1 also bₙ = 1/n!. Für x = 1 ergibt das e = 1 + 1/1! + 1/2! + …. Konvergenz zeigt man erst bei den Potenzreihen (Kap. VIII).');
    }
  });
  const sN = MW.slider(ctl, { label: 'n', min: 2, max: 60, step: 1, value: N, fmt: u => fmt(u, 0), onInput: u => { N = u; view.redraw(); } });
  const sX = MW.slider(ctl, { label: 'x', min: -2.5, max: 1.9, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  const sT = MW.slider(ctl, { label: 'Grad n', min: 0, max: 10, step: 1, value: n, fmt: u => fmt(u, 0), onInput: u => { n = u; view.redraw(); } });
  const show = () => { sN.el.style.display = mode === 'folge' ? '' : 'none'; sX.el.style.display = mode === 'tangente' ? '' : 'none'; sT.el.style.display = mode === 'reihe' ? '' : 'none'; };
  MW.select(ctl, 'Ansicht', [['folge', 'Schranken für e'], ['tangente', 'eˣ ≥ 1 + x'], ['reihe', 'Reihe für eˣ']], u => { mode = u; show(); view.redraw(); }).set(mode);
  show();
'''))

# ---------------------------------------------------------------- 5.2
W.append(dict(file='5-2-logarithmus-basis.html', title='aˣ und der Logarithmus zur Basis a',
  sub='aˣ = e^(x ln a) hat die Ableitung ln a · aˣ. Für a > 1 ist aˣ streng wachsend, also umkehrbar. Die Umkehrfunktion log_a x = ln x / ln a ist das Spiegelbild an y = x. Die Tangentensteigungen in gespiegelten Punkten sind Kehrwerte.',
  hint='Basis a und die Stelle x₀ verschieben.', legend=[('--c2', 'y = aˣ'), ('--c1', 'y = log_a x'), ('--c3', 'Tangenten'), ('--muted', 'y = x')], js=r'''
  function gplot(v, f, a, b, color, w = 2.4, ylo = -9, yhi = 9, N = 700) { let seg = [];
    const fl = () => { if (seg.length > 1) v.poly(seg, color, w); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x); if (!isFinite(y) || y < ylo || y > yhi) { fl(); continue; } seg.push([x, y]); } fl(); }
  let a = Math.E, x0 = 0.6;
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 6.2, ymin: -2.4, ymax: 2.97 }, v => {
    const C = v.C; v.grid(1);
    const b = v.bounds(); v.line([b.x0, b.x0], [b.y1 + 1, b.y1 + 1], C.muted, 1.2, [5, 4]);
    if (Math.abs(a - 1) < 0.02) { gplot(v, x => 1, b.x0, b.x1, C.c2); MW.info(infoEl, 'a = 1', [['1ˣ', '= 1 für alle x']], 'Für a = 1 ist aˣ konstant, also nicht injektiv: Es gibt keinen Logarithmus zur Basis 1.', true); return; }
    const la = Math.log(a), f = x => Math.exp(la * x), g = x => Math.log(x) / la;
    gplot(v, f, b.x0, b.x1, C.c2, 2.6, b.y0 - 1, b.y1 + 1); gplot(v, g, 1e-4, b.x1, C.c1, 2.6, b.y0 - 1, b.y1 + 1, 2000);
    const y0 = f(x0), m1 = la * y0, m2 = 1 / m1, h = 0.8 / Math.hypot(1, m1), k = 0.8 / Math.hypot(1, m2);
    v.line([x0 - h, y0 - m1 * h], [x0 + h, y0 + m1 * h], C.c3, 2); v.line([y0 - k, x0 - m2 * k], [y0 + k, x0 + m2 * k], C.c3, 2);
    v.line([x0, y0], [y0, x0], C.muted, 1, [2, 3]);
    v.dot([x0, y0], C.c2, 5.5); v.text([x0, y0], '(x₀, aˣ⁰)', C.c2, -8, -10, 12, true, 'right'); v.dot([y0, x0], C.c1, 5.5); v.text([y0, x0], '(aˣ⁰, x₀)', C.c1, 8, 16, 12);
    MW.info(infoEl, 'a = ' + fmt(a, 3) + ',  ln a = ' + fmt(la, 4), [['aˣ⁰ = e^(x₀ ln a)', fmt(y0, 4)], ['(aˣ)′ an x₀ = ln a · aˣ⁰', fmt(m1, 4)],
      ['log_a(aˣ⁰) = ln(aˣ⁰)/ln a', fmt(g(y0), 4) + ' = x₀'], ['(log_a)′ an aˣ⁰ = 1/(aˣ⁰ ln a)', fmt(m2, 4)], ['Produkt der Steigungen', fmt(m1 * m2, 4)]],
      'Vorlesung S. 26, Skript S. 42–43: aˣ := e^(x ln a), (aˣ)′ = ln a · aˣ, log_a x = ln x / ln a. Im Skript heisst der natürliche Logarithmus log, in der Vorlesung ln. '
      + (a < 1 ? 'Hier ist 0 < a < 1: aˣ ist streng fallend, aber ebenfalls umkehrbar (Vorlesung S. 26, Bemerkung).' : 'Für a > 1 ist ln a > 0, also aˣ streng wachsend.'));
  });
  const sa = MW.slider(ctl, { label: 'a', min: 0.2, max: 5, step: 0.01, value: a, onInput: u => { a = u; view.redraw(); } });
  MW.slider(ctl, { label: 'x₀', min: -2, max: 1.5, step: 0.01, value: x0, onInput: u => { x0 = u; view.redraw(); } });
  MW.select(ctl, 'Basis', [['e', 'a = e'], ['2', 'a = 2'], ['10', 'a = 10'], ['0.5', 'a = 1/2']], u => { a = u === 'e' ? Math.E : +u; sa.set(a); view.redraw(); }).set('e');
'''))

# ---------------------------------------------------------------- 5.3
W.append(dict(file='5-3-hyperbolische-funktionen.html', title='cosh, sinh und die Hyperbel x² − y² = 1',
  sub='Wie (cos t, sin t) auf dem Einheitskreis liegt, liegt (cosh t, sinh t) auf dem rechten Ast der Hyperbel x² − y² = 1. Beide markierten Flächen haben den Inhalt |t|. Rechts die Graphen: cosh = ½eˣ + ½e⁻ˣ, sinh = ½eˣ − ½e⁻ˣ.',
  hint='t verschieben.', legend=[('--c4', 'Kreis: (cos t, sin t)'), ('--c2', 'cosh'), ('--c1', 'sinh'), ('--muted', '½eˣ, ½e⁻ˣ')], js=AX + EXTRA + r'''
  const H = mkAx(-1.5, 4, -3.9, 3.9, 2.6, 3.7, -0.65, -0.3), G = mkAx(-2.2, 2.2, -4, 4, 3.1, 3.7, 2.95, -0.3);
  const ch = Math.cosh, sh = Math.sinh;
  let t = 0.9;
  const view = MW.View2D(cv, ''' + TALL + r''', v => {
    const C = v.C;
    v.line(H.P(-1.5, 0), H.P(4, 0), C.muted, 1.2); v.line(H.P(0, -3.9), H.P(0, 3.9), C.muted, 1.2);
    v.line(H.P(0, 0), H.P(3.9, 3.9), C.grid, 1, [4, 4]); v.line(H.P(0, 0), H.P(3.9, -3.9), C.grid, 1, [4, 4]);
    const circ = [], hyp = []; for (let i = 0; i <= 120; i++) { const s = 2 * Math.PI * i / 120; circ.push(H.P(Math.cos(s), Math.sin(s))); }
    for (let i = 0; i <= 120; i++) { const s = -2.06 + 4.12 * i / 120; hyp.push(H.P(ch(s), sh(s))); }
    v.poly(circ, C.c4, 1.4); v.poly(hyp, C.c2, 2.2);
    const sec = (fx, fy, T) => { const pts = [H.P(0, 0)]; for (let i = 0; i <= 80; i++) { const s = -T + 2 * T * i / 80; pts.push(H.P(fx(s), fy(s))); } return pts; };
    const a = Math.abs(t);
    v.poly(sec(ch, sh, a), C.c2, 1.2, null, true, C.fill);
    if (a <= Math.PI) v.poly(sec(Math.cos, Math.sin, a), C.c4, 1.2, [3, 3], true, C.fill);
    v.dot(H.P(ch(t), sh(t)), C.c2, 6); v.text(H.P(ch(t), sh(t)), '(cosh t, sinh t)', C.c2, -8, t >= 0 ? -6 : 16, 11, true, 'right');
    v.dot(H.P(ch(t), -sh(t)), C.c2, 4.5, true);
    v.dot(H.P(Math.cos(t), Math.sin(t)), C.c4, 5.5);
    axes(v, G, 'x', '', 1, 1);
    dplot(v, G, x => Math.exp(x) / 2, C.muted); dplot(v, G, x => Math.exp(-x) / 2, C.muted);
    fplot(v, G, ch, C.c2, 2.5); fplot(v, G, sh, C.c1, 2.5);
    v.line(G.P(t, -4), G.P(t, 4), C.muted, 1, [2, 3]); v.dot(G.P(t, ch(t)), C.c2, 5); v.dot(G.P(t, sh(t)), C.c1, 5);
    const y = sh(t);
    MW.info(infoEl, 't = ' + fmt(t, 3), [['cosh t = (eᵗ + e⁻ᵗ)/2', fmt(ch(t), 5)], ['sinh t = (eᵗ − e⁻ᵗ)/2', fmt(y, 5)],
      ['cosh² t − sinh² t', fmt(ch(t) ** 2 - y ** 2, 6)], ['Fläche (Hyperbel) = Fläche (Kreis)', fmt(a, 4) + (a > Math.PI ? ' (Kreissektor nur für |t| ≤ π)' : '')],
      ['Arsinh(sinh t) = ln(y + √(y² + 1))', fmt(Math.log(y + Math.sqrt(y * y + 1)), 5) + ' = t']],
      'Vorlesung S. 23–25, Skript S. 43–48: cosh² − sinh² = 1, cosh′ = sinh, sinh′ = cosh, cosh ist gerade, sinh ungerade. sinh ist streng wachsend; die Umkehrfunktion ist Arsinh y = ln(y + √(y² + 1)), die von cosh auf [0, ∞) ist Arcosh y = ln(y + √(y² − 1)). Die Kettenlinie hat die Form a cosh(x/a) (Skript S. 44).');
  });
  MW.slider(ctl, { label: 't', min: -2, max: 2, step: 0.01, value: t, onInput: u => { t = u; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 6.1
W.append(dict(file='6-1-groessenordnungen.html', title='Grössenordnungen: f = o(g), wenn f(x)/g(x) → 0',
  sub='Oben f und g, unten der Quotient f/g auf dem gewählten Fenster. f ist von kleinerer Grössenordnung als g, wenn f/g gegen 0 strebt. Kleine Fenster täuschen: x¹⁰ liegt lange über eˣ, und ln x / x^(1/10) fällt erst nach x ≈ 22 000.',
  hint='Paar wählen und das Fenster vergrössern.', tall=True, legend=[('--c2', 'f'), ('--c4', 'g'), ('--c1', 'f/g')], js=AX + EXTRA + r'''
  const S = {
    x3e: { name: 'f = x³, g = eˣ', f: x => x ** 3, g: Math.exp, lo: 0, s: [0.3, 1.6], s0: 0.6, res: 'x³ = o(eˣ) für x → ∞',
      note: 'Vorlesung S. 27–28, Skript S. 52–54: xʳ = o(eˣ) für alle r > 0. Die Graphen schneiden sich noch einmal bei x ≈ 4.54 (Skript S. 53, Fig. 5).' },
    x10: { name: 'f = x¹⁰, g = eˣ', f: x => x ** 10, g: Math.exp, lo: 0, s: [0.3, 2.2], s0: 1.4, res: 'x¹⁰ = o(eˣ) für x → ∞',
      note: 'Skript S. 52–53, Fig. 4 und 6: „Der Eindruck trügt.“ Erst bei x ≈ 35.8 überholt eˣ wieder x¹⁰ (Vorlesung S. 28–29: ≈ 35). Danach geht der Quotient schnell gegen 0.' },
    lnx3: { name: 'f = ln x, g = x³', f: Math.log, g: x => x ** 3, lo: 1, s: [0.3, 1.5], s0: 0.8, res: 'ln x = o(x³) für x → ∞',
      note: 'Vorlesung S. 27: lim ln x / x³ = lim (1/x)/(3x²) = 0 mit Bernoulli-Hôpital.' },
    lnsq: { name: 'f = ln x, g = √x', f: Math.log, g: Math.sqrt, lo: 1, s: [0.5, 4], s0: 2, res: 'ln x = o(√x) für x → ∞', logx: true,
      note: 'Skript S. 55, Fig. 7: ln x = o(xᵏ) für jedes k > 0. Achse: log₁₀ x.' },
    ln10: { name: 'f = ln x, g = x^(1/10)', f: Math.log, g: x => x ** 0.1, lo: 1, s: [1, 40], s0: 3, res: 'ln x = o(x^(1/10)) für x → ∞', logx: true,
      note: 'Skript S. 55, Fig. 7. Der Quotient wächst bis x = e¹⁰ ≈ 22 026 (Maximum 10/e ≈ 3.68) und fällt erst danach gegen 0. Achse: log₁₀ x. (Die Lage des Maximums ist eigene Rechnung.)' },
    lin: { name: 'f = x, g = 2x', f: x => x, g: x => 2 * x, lo: 0.01, s: [0.3, 3], s0: 1, res: 'f/g = 1/2 ↛ 0: gleiche Grössenordnung, nicht o',
      note: 'Vorlesung S. 27, Skript S. 51: x, 2x und x + c sind von gleicher Grössenordnung. Strebt f/g gegen A ≠ 0, wachsen f und g gleich schnell.' },
    em: { name: 'f = e⁻ˣ, g = x⁻²', f: x => Math.exp(-x), g: x => x ** -2, lo: 0.5, s: [0.5, 1.7], s0: 1, res: 'e⁻ˣ = o(x⁻²) für x → ∞',
      note: 'Vorlesung S. 28, Skript S. 55: Beide gehen gegen 0, aber e⁻ˣ schneller: e⁻ˣ / x⁻ʳ = xʳ/eˣ → 0.' },
    ln0: { name: 'f = ln x, g = −x^(−1/2) für x → 0⁺', f: Math.log, g: x => -(x ** -0.5), zero: true, s: [-12, -0.5], s0: -2, res: 'ln x = o(−x^(−1/2)) für x → 0⁺', logx: true,
      note: 'Vorlesung S. 29, Skript S. 56: ln x = o(−x⁻ʳ) für x → 0⁺ und jedes r > 0. Beide streben gegen −∞, −x⁻ʳ schneller. Hier ist das Fenster [10^s, 1], Achse: log₁₀ x.' },
    pole: { name: 'f = 1/x, g = 1/(1 − cos x) für x → 0⁺', f: x => 1 / x, g: x => 1 / (1 - Math.cos(x)), zero: true, s: [-6, -0.3], s0: -1, res: '1/x = o(1/(1 − cos x)) für x → 0⁺', logx: true,
      note: 'Vorlesung S. 29: lim (1 − cos x)/x = lim sin x = 0, also hat 1/(1 − cos x) die „stärkere“ Polstelle. Fenster [10^s, 1], Achse: log₁₀ x.' },
  };
  let key = 'x10', s = 1.4;
  const view = MW.View2D(cv, ''' + TALL + r''', v => {
    const C = v.C, c = S[key], N = 700;
    const a = c.zero ? 10 ** s : c.lo, b = c.zero ? 1 : 10 ** s;
    const ua = c.logx ? Math.log10(a) : a, ub = c.logx ? Math.log10(b) : b, X = u => c.logx ? 10 ** u : u;
    const fs = [], gs = [], qs = [];
    for (let i = 0; i <= N; i++) { const x = X(ua + (ub - ua) * i / N); fs.push(c.f(x)); gs.push(c.g(x)); qs.push(c.f(x) / c.g(x)); }
    const rng = (arr, inc0) => { let lo = Infinity, hi = -Infinity; arr.forEach(y => { if (isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); } });
      if (inc0) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); } if (hi - lo < 1e-12) { hi += 1; lo -= 1; } const p = 0.06 * (hi - lo); return [lo - p, hi + p]; };
    const r1 = rng(fs.concat(gs), false), r2 = rng(qs, true);
    const A = mkAx(ua, ub, r1[0], r1[1], 6, 1.75, 0, 1.95), B = mkAx(ua, ub, r2[0], r2[1], 6, 1.6, 0, 0);
    const xl = c.logx ? 'log₁₀ x' : 'x';
    axes(v, A, xl, ''); axes(v, B, xl, 'f/g');
    fplot(v, A, u => c.g(X(u)), C.c4, 2.4, N); fplot(v, A, u => c.f(X(u)), C.c2, 2.4, N); fplot(v, B, u => c.f(X(u)) / c.g(X(u)), C.c1, 2.4, N);
    const xe = c.zero ? a : b, q = c.f(xe) / c.g(xe);
    MW.info(infoEl, c.res, [[c.zero ? 'linker Fensterrand x' : 'rechter Fensterrand X', sci(xe)], ['f', sci(c.f(xe))], ['g', sci(c.g(xe))], ['f/g', sci(q)]], c.note);
  });
  const sl = MW.slider(ctl, { label: 'Fenster s', min: 0.3, max: 2.2, step: 0.01, value: s, fmt: u => (S[key].zero ? '[10^' + fmt(u, 2) + ', 1]' : 'bis 10^' + fmt(u, 2)), onInput: u => { s = u; view.redraw(); } });
  MW.select(ctl, 'Paar', Object.entries(S).map(([k, c]) => [k, c.name]), u => { key = u; const c = S[key], inp = sl.el.querySelector('input');
    inp.min = c.s[0]; inp.max = c.s[1]; inp.step = (c.s[1] - c.s[0]) / 400; s = c.s0; sl.set(s); view.redraw(); }).set(key);
'''))

if __name__ == '__main__':
    print(build('analysis-w7', W))
