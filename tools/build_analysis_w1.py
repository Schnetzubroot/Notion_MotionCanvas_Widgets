"""Widgets zu Analysis I, Woche 1: Kapitel I.1 Folgen, Konvergenz (Stammbach, Teil A, S. 3-15)."""
from template import build

# gemeinsame Hilfen: Achsenkreuz mit eigener Skalierung in x und y (View2D hat gleiche Skalierung)
AX = r'''
  const mkAx = (x0, x1, y0, y1, W = 6, H = 3.4, ox = 0, oy = 0) => {
    const X = x => ox + (x - x0) / (x1 - x0) * W, Y = y => oy + (y - y0) / (y1 - y0) * H;
    return { x0, x1, y0, y1, W, H, ox, oy, X, Y, P: (x, y) => [X(x), Y(y)], inY: y => y >= y0 && y <= y1 };
  };
  const nice = r => { const raw = r / 6, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p; };
  function axes(v, A, xl, yl, xs, ys) {
    const C = v.C; xs = xs || nice(A.x1 - A.x0); ys = ys || nice(A.y1 - A.y0);
    for (let x = Math.ceil(A.x0 / xs - 1e-9) * xs; x <= A.x1 + 1e-9; x += xs) { v.line(A.P(x, A.y0), A.P(x, A.y1), C.grid, 1); v.text(A.P(x, A.y0), fmt(x, 3), C.muted, 0, 15, 11, false, 'center'); }
    for (let y = Math.ceil(A.y0 / ys - 1e-9) * ys; y <= A.y1 + 1e-9; y += ys) { v.line(A.P(A.x0, y), A.P(A.x1, y), C.grid, 1); v.text(A.P(A.x0, y), fmt(y, 3), C.muted, -5, 4, 11, false, 'right'); }
    if (A.y0 <= 0 && A.y1 >= 0) v.line(A.P(A.x0, 0), A.P(A.x1, 0), C.muted, 1.3);
    if (A.x0 <= 0 && A.x1 >= 0) v.line(A.P(0, A.y0), A.P(0, A.y1), C.muted, 1.3);
    if (xl) v.text(A.P(A.x1, A.y0), xl, C.muted, -2, -6, 12, false, 'right');
    if (yl) v.text(A.P(A.x0, A.y1), yl, C.muted, 6, 14, 12, false);
  }
  // Graph einer Funktion, unterbrochen bei Sprüngen und ausserhalb des Fensters
  function fplot(v, A, f, color, w = 2, N = 600, a = A.x0, b = A.x1) {
    const H = A.y1 - A.y0, inside = y => y >= A.y0 && y <= A.y1, cl = y => Math.max(A.y0, Math.min(A.y1, y));
    let seg = [], px = null, py = null;
    const flush = () => { if (seg.length > 1) v.poly(seg, color, w); seg = []; };
    for (let i = 0; i <= N; i++) { const x = a + (b - a) * i / N, y = f(x);
      if (!isFinite(y)) { flush(); px = null; continue; }
      if (px !== null && Math.abs(y - py) > 2 * H && !(inside(y) && inside(py))) { flush(); px = x; py = y; if (inside(y)) seg.push(A.P(x, y)); continue; }
      if (px !== null && inside(y) !== inside(py)) { // Rand schneiden
        const yb = inside(py) ? (y > A.y1 ? A.y1 : A.y0) : (py > A.y1 ? A.y1 : A.y0), xb = px + (x - px) * (yb - py) / (y - py);
        if (inside(py)) { seg.push(A.P(xb, yb)); flush(); } else { flush(); seg.push(A.P(xb, yb)); }
      } else if (px !== null && !inside(y) && !inside(py) && (y - A.y1) * (py - A.y1) < 0 && (y - A.y0) * (py - A.y0) < 0) { flush(); }
      if (inside(y)) seg.push(A.P(x, y));
      px = x; py = y; }
    flush();
  }
'''
BOX = '{ xmin: -0.75, xmax: 6.25, ymin: -0.45, ymax: 3.55 }'

W = []

# ---------------------------------------------------------------- 1.1
W.append(dict(file='1-1-folgen-darstellung.html', title='Folgen als Punkte (n, a<sub>n</sub>)',
  sub='Eine Folge ordnet jeder natürlichen Zahl n eine reelle Zahl a<sub>n</sub> zu. Zeichnet man die Glieder als Punkte (n, a<sub>n</sub>), sieht man Beschränktheit und Monotonie direkt.',
  hint='Folge wählen, Anzahl Glieder ändern.', legend=[('--c2', 'Glieder (n, a_n)'), ('--c3', 'Parallelstreifen')], js=AX + r'''
  const S = {
    lin: { name: 'a_n = −5 + 3n (explizit)', f: n => -5 + 3 * n, bd: false },
    alt: { name: 'a_n = 1/2 + (−1)^n / n²', f: n => 0.5 + (-1) ** n / (n * n), bd: [-0.5, 0.75] },
    inv: { name: 'a_n = 1/n', f: n => 1 / n, bd: [0, 1] },
    osc: { name: 'a_n = (−1)^n', f: n => (-1) ** n, bd: [-1, 1] },
    her: { name: 'a₁ = 1, a_{n+1} = ½(a_n + 3/a_n) (rekursiv)', f: null, bd: [1, 2] },
  };
  const heron = []; { let a = 1; for (let n = 1; n <= 60; n++) { heron.push(a); a = 0.5 * (a + 3 / a); } } S.her.f = n => heron[n - 1];
  let key = 'alt', N = 20, strip = true;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], vals = []; for (let n = 1; n <= N; n++) vals.push(s.f(n));
    let lo = Math.min(...vals), hi = Math.max(...vals); if (s.bd) { lo = Math.min(lo, s.bd[0]); hi = Math.max(hi, s.bd[1]); }
    const pad = 0.12 * (hi - lo || 1), A = mkAx(0, N + 1, Math.min(0, lo - pad), hi + pad);
    axes(v, A, 'n', 'a_n', N > 20 ? 5 : N > 10 ? 2 : 1);
    if (strip && s.bd) { v.poly([A.P(0, s.bd[0]), A.P(N + 1, s.bd[0]), A.P(N + 1, s.bd[1]), A.P(0, s.bd[1])], null, 1, null, true, C.fill);
      v.line(A.P(0, s.bd[0]), A.P(N + 1, s.bd[0]), C.c3, 1.5, [5, 4]); v.line(A.P(0, s.bd[1]), A.P(N + 1, s.bd[1]), C.c3, 1.5, [5, 4]); }
    vals.forEach((y, i) => v.dot(A.P(i + 1, y), C.c2, 4.5));
    let inc = true, dec = true; for (let i = 1; i < vals.length; i++) { if (vals[i] < vals[i - 1] - 1e-15) inc = false; if (vals[i] > vals[i - 1] + 1e-15) dec = false; }
    const mono = key === 'her' ? 'ab n = 2 monoton fallend' : inc ? 'monoton wachsend' : dec ? 'monoton fallend' : 'nicht monoton';
    MW.info(infoEl, s.name, [['a₁, a₂, a₃, a₄', vals.slice(0, 4).map(x => fmt(x, 4)).join(', ')], ['a_' + N, fmt(vals[N - 1], 6)], ['beschränkt', s.bd ? 'ja, alle Glieder in [' + fmt(s.bd[0], 2) + ', ' + fmt(s.bd[1], 2) + ']' : 'nein, kein Streifen reicht'], ['Monotonie', mono]],
      key === 'lin' ? 'Die Glieder wachsen um 3 pro Schritt über jede Schranke hinaus. Kein waagrechter Streifen endlicher Breite enthält alle Punkte.'
      : key === 'her' ? 'Rekursive Folge: a_{n+1} wird aus a_n berechnet. So rechnet ein Taschenrechner √3 ≈ 1.7320508.'
      : 'Beschränkt heisst: alle Punkte liegen in einem waagrechten Streifen endlicher Breite.');
  });
  MW.select(ctl, 'Folge', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'Glieder', min: 4, max: 40, step: 1, value: N, fmt: x => String(x), onInput: x => { N = x; view.redraw(); } });
  MW.check(ctl, 'Streifen zeigen', strip, x => { strip = x; view.redraw(); });
'''))

# ---------------------------------------------------------------- 1.2
W.append(dict(file='1-2-epsilon-streifen.html', title='Konvergenz: der ε-Streifen um den Grenzwert',
  sub='a<sub>n</sub> → a heisst: Zu jedem noch so kleinen ε > 0 gibt es ein m, so dass alle Glieder ab a<sub>m</sub> im Streifen |a<sub>n</sub> − a| < ε liegen. Ausserhalb bleiben nur endlich viele.',
  hint='ε verkleinern: m wird grösser, aber es gibt immer eins.', legend=[('--c3', 'Streifen a ± ε'), ('--c2', 'Glieder im Streifen ab m'), ('--c1', 'Glieder ausserhalb')], js=AX + r'''
  const S = {
    alt: { name: 'a_n = 1/2 + (−1)^n / n²', f: n => 0.5 + (-1) ** n / (n * n), a: 0.5, y: [-0.6, 0.85] },
    inv: { name: 'a_n = 1/n (Nullfolge)', f: n => 1 / n, a: 0, y: [-0.3, 1.1] },
    rat: { name: 'a_n = (n + 3)/(2n + 5)', f: n => (n + 3) / (2 * n + 5), a: 0.5, y: [0.4, 0.62] },
    osc: { name: 'a_n = (−1)^n (divergent)', f: n => (-1) ** n, a: 0, y: [-1.3, 1.3] },
  };
  let key = 'alt', le = Math.log10(0.05);
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], eps = Math.pow(10, le), N = 40;
    // m: kleinster Index, ab dem alle (geprüft bis 5000) im Streifen liegen
    let m = null, last = 0; for (let n = 1; n <= 5000; n++) if (Math.abs(s.f(n) - s.a) >= eps) last = n;
    if (last < 5000) m = last + 1;
    const A = mkAx(0, N + 1, s.y[0], s.y[1]); axes(v, A, 'n', 'a_n', 5);
    v.poly([A.P(0, s.a - eps), A.P(N + 1, s.a - eps), A.P(N + 1, s.a + eps), A.P(0, s.a + eps)].map(p => [p[0], Math.max(A.oy, Math.min(A.oy + A.H, p[1]))]), null, 1, null, true, C.fill);
    [s.a - eps, s.a + eps].forEach(y => { if (A.inY(y)) v.line(A.P(0, y), A.P(N + 1, y), C.c3, 1.5, [5, 4]); });
    v.line(A.P(0, s.a), A.P(N + 1, s.a), C.c3, 1); v.text(A.P(N + 1, s.a), key === 'osc' ? 'a = 0 ?' : 'a = ' + fmt(s.a), C.c3, -4, -6, 12, true, 'right');
    if (m && m <= N) { v.line(A.P(m - 0.5, s.y[0]), A.P(m - 0.5, s.y[1]), C.muted, 1.2, [3, 3]); v.text(A.P(m - 0.5, s.y[1]), 'm = ' + m, C.fg, 4, 14, 12); }
    let out = 0; for (let n = 1; n <= N; n++) { const y = s.f(n), inside = Math.abs(y - s.a) < eps; if (!inside) out++; if (A.inY(y)) v.dot(A.P(n, y), inside ? C.c2 : C.c1, 4.5); }
    MW.info(infoEl, m ? 'ε = ' + fmt(eps, 4) + ' → m = ' + m : 'ε = ' + fmt(eps, 4) + ': kein m gefunden', [['Glieder ausserhalb (n < m)', m ? String(m - 1) : 'unendlich viele'], ['|a_m − a|', m ? fmt(Math.abs(s.f(m) - s.a), 5) : '–']],
      key === 'osc' ? 'Die Glieder springen zwischen −1 und +1. Für ε ≤ 1 liegt um keinen Kandidaten a ein Streifen, der fast alle Glieder enthält. Die Folge ist divergent (aber beschränkt).'
      : key === 'rat' ? '|a_n − 1/2| = 1/(2(2n + 5)) < ε gilt für n > (1/(2ε) − 5)/2. Für jedes ε gibt es also ein m.'
      : key === 'inv' ? '|1/n| < ε gilt für n > 1/ε. Darum ist 1/n eine Nullfolge.'
      : '|a_n − 1/2| = 1/n² < ε gilt für n > 1/√ε.', !m);
  });
  MW.select(ctl, 'Folge', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); }).set(key);
  MW.slider(ctl, { label: 'ε', min: -3, max: -0.3, step: 0.01, value: le, fmt: x => fmt(Math.pow(10, x), 4), onInput: x => { le = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 1.3
W.append(dict(file='1-3-e-folge.html', title='Monoton und beschränkt ⇒ konvergent: die Zahl e',
  sub='a<sub>n</sub> = 1 + 1/1! + 1/2! + … + 1/n! wächst strikt. Mit 1/k! ≤ 1/2<sup>k−1</sup> folgt a<sub>n</sub> ≤ 3 − 1/2<sup>n−1</sup> < 3. Also konvergiert die Folge, obwohl man den Limes vorher nicht kennt.',
  hint='n vergrössern.', legend=[('--c2', 'a_n'), ('--c3', 'Schranke 3 − 1/2^(n−1)'), ('--c1', 'Limes e')], js=AX + r'''
  let N = 6;
  const a = [], b = []; { let s = 1, f = 1; for (let n = 1; n <= 15; n++) { f *= n; s += 1 / f; a.push(s); b.push(3 - 1 / 2 ** (n - 1)); } }
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, A = mkAx(0, 15.5, 0, 3.4); axes(v, A, 'n', '', 1, 0.5);
    v.line(A.P(0, 3), A.P(15.5, 3), C.c3, 1.2, [6, 4]); v.text(A.P(0, 3), '3', C.c3, 4, -6, 12);
    v.line(A.P(0, Math.E), A.P(15.5, Math.E), C.c1, 1.2, [2, 3]); v.text(A.P(15.5, Math.E), 'e', C.c1, -10, 16, 13);
    for (let n = 1; n <= N; n++) { v.dot(A.P(n, b[n - 1]), C.c3, 4, true); v.dot(A.P(n, a[n - 1]), C.c2, 4.5); }
    MW.info(infoEl, 'a_' + N + ' = ' + fmt(a[N - 1], 10), [['Schranke 3 − 1/2^' + (N - 1), fmt(b[N - 1], 6)], ['e − a_' + N, fmt(Math.E - a[N - 1], 10)], ['Zuwachs a_n − a_{n−1} = 1/n!', fmt(N > 1 ? a[N - 1] - a[N - 2] : 1, 10)]],
      'Die Zuwächse 1/n! werden so schnell klein, dass die Summe unter 3 bleibt. Satz: monoton und beschränkt ⇒ konvergent. Der Limes ist e = 2.718281828…');
  });
  MW.slider(ctl, { label: 'n', min: 1, max: 15, step: 1, value: N, fmt: x => String(x), onInput: x => { N = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-harmonisch.html', title='Die harmonische Folge ist nicht beschränkt',
  sub='a<sub>n</sub> = 1 + 1/2 + … + 1/n wächst strikt, aber immer langsamer. Wegen a<sub>2n</sub> − a<sub>n</sub> ≥ 1/2 gilt a<sub>2<sup>r</sup></sub> ≥ 1 + r/2. Die Glieder werden beliebig gross: keine Konvergenz.',
  hint='r vergrössern: Das Fenster wächst bis n = 2^r.', legend=[('--c2', 'a_n'), ('--c3', 'Schranke 1 + r/2 bei n = 2^r')], js=AX + r'''
  let R = 6;
  const H = [0]; for (let n = 1; n <= 4096; n++) H.push(H[n - 1] + 1 / n);
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, N = 2 ** R, A = mkAx(0, N, 0, Math.ceil(H[N] + 0.5)); axes(v, A, 'n', 'a_n', null, 1);
    const pts = []; const st = Math.max(1, Math.floor(N / 400)); for (let n = 1; n <= N; n += st) pts.push(A.P(n, H[n]));
    if (N <= 64) for (let n = 1; n <= N; n++) v.dot(A.P(n, H[n]), C.c2, 3); else v.poly(pts, C.c2, 2.2);
    for (let r = 0; r <= R; r++) { const n = 2 ** r; v.dot(A.P(n, 1 + r / 2), C.c3, 4.5, true); v.line(A.P(n, 1 + r / 2), A.P(n, H[n]), C.c3, 1, [2, 2]); }
    MW.info(infoEl, 'n = 2^' + R + ' = ' + N, [['a_n', fmt(H[N], 4)], ['Schranke 1 + r/2', fmt(1 + R / 2, 2)], ['Zuwachs von a_n bis a_2n', '≥ 1/2']],
      'Jede Verdoppelung von n bringt mindestens 1/2 dazu. Nach genug Verdoppelungen ist jede Schranke überschritten. Eine nicht beschränkte Folge kann nicht konvergieren.');
  });
  MW.slider(ctl, { label: 'r', min: 2, max: 12, step: 1, value: R, fmt: x => String(x), onInput: x => { R = x; view.redraw(); } });
'''))

W.append(dict(file='1-3-heron.html', title='Rekursive Folge für √c (Heron-Verfahren)',
  sub='a<sub>1</sub> = 1, a<sub>n+1</sub> = ½(a<sub>n</sub> + c/a<sub>n</sub>). Für b<sub>n</sub> = a<sub>n</sub> − √c gilt b<sub>n+1</sub> = b<sub>n</sub>²/(2a<sub>n</sub>) ≥ 0 und |b<sub>n+1</sub>| < ½|b<sub>n</sub>|. Also a<sub>n</sub> → √c.',
  hint='c und den Startwert ändern.', legend=[('--c2', 'a_n'), ('--c1', '√c')], js=AX + r'''
  let c = 3, a1 = 1;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, a = [a1]; for (let n = 1; n < 8; n++) a.push(0.5 * (a[n - 1] + c / a[n - 1]));
    const hi = Math.max(...a, Math.sqrt(c)) * 1.12, A = mkAx(0, 8.5, 0, hi); axes(v, A, 'n', 'a_n', 1);
    v.line(A.P(0, Math.sqrt(c)), A.P(8.5, Math.sqrt(c)), C.c1, 1.4, [5, 4]); v.text(A.P(8.5, Math.sqrt(c)), '√c', C.c1, -6, -6, 13, true, 'right');
    v.poly(a.map((y, i) => A.P(i + 1, y)), C.line, 1.2);
    a.forEach((y, i) => v.dot(A.P(i + 1, y), C.c2, 5));
    const b = a.map(x => x - Math.sqrt(c)), rows = [];
    for (let n = 0; n < 6; n++) rows.push(['n = ' + (n + 1), 'a = ' + fmt(a[n], 10) + ',  b = ' + (Math.abs(b[n]) < 1e-12 ? '0' : b[n].toExponential(2))]);
    MW.info(infoEl, '√' + fmt(c) + ' = ' + fmt(Math.sqrt(c), 10), rows,
      'Ab n = 2 ist b_n ≥ 0: Die Folge nähert sich √c von oben. Der Fehler wird mindestens halbiert, in der Praxis sogar quadriert (die Zahl der richtigen Stellen verdoppelt sich).');
  });
  MW.slider(ctl, { label: 'c', min: 0.5, max: 10, step: 0.1, value: c, onInput: x => { c = x; view.redraw(); } });
  MW.slider(ctl, { label: 'a₁', min: 0.2, max: 6, step: 0.1, value: a1, onInput: x => { a1 = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 1.4
W.append(dict(file='1-4-rechenregeln.html', title='Rechenregeln: durch die höchste Potenz kürzen',
  sub='Bei Quotienten von Polynomen in n kürzt man durch die höchste Potenz im Nenner. Dann stehen nur noch konvergente Folgen da, und die Rechenregeln dürfen angewendet werden.',
  hint='Beispiel wählen.', legend=[('--c2', 'a_n'), ('--c1', 'Grenzwert')], js=AX + r'''
  const S = {
    a: { name: '(n + 3)/(2n + 5)', f: n => (n + 3) / (2 * n + 5), L: 0.5, step: '= (1 + 3/n)/(2 + 5/n) → (1 + 0)/(2 + 0) = 1/2' },
    b: { name: '(n³ + n² + 1)/(−3n³ + 13)', f: n => (n ** 3 + n * n + 1) / (-3 * n ** 3 + 13), L: -1 / 3, step: '= (1 + 1/n + 1/n³)/(−3 + 13/n³) → −1/3' },
    c: { name: '17n²/(18n + 1)', f: n => 17 * n * n / (18 * n + 1), L: null, step: '= 17n/(18 + 1/n): Zähler wächst über alle Grenzen, Nenner → 18. Grenzwert existiert nicht.' },
    d: { name: '(2n²/(n² + 3))⁴', f: n => (2 * n * n / (n * n + 3)) ** 4, L: 16, step: '= (2/(1 + 3/n²))⁴ → 2⁴ = 16 (Produktregel viermal)' },
    e: { name: 'Warnung: n · (1/n)', f: n => 1, L: 1, step: 'Hier ist lim(n · 1/n) = 1. Aber „lim n · lim 1/n = ∞ · 0“ ist keine Rechnung: lim n existiert nicht, die Regel gilt nicht.' },
  };
  let key = 'a', N = 30;
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, s = S[key], vals = []; for (let n = 1; n <= N; n++) vals.push(s.f(n));
    let lo = Math.min(...vals, s.L ?? Infinity), hi = Math.max(...vals, s.L ?? -Infinity); const pad = 0.15 * (hi - lo || 1);
    const A = mkAx(0, N + 1, lo - pad, hi + pad); axes(v, A, 'n', 'a_n', 5);
    if (s.L !== null) { v.line(A.P(0, s.L), A.P(N + 1, s.L), C.c1, 1.4, [5, 4]); v.text(A.P(N + 1, s.L), 'Limes ' + fmt(s.L, 4), C.c1, -4, -6, 12, true, 'right'); }
    vals.forEach((y, i) => v.dot(A.P(i + 1, y), C.c2, 4));
    MW.info(infoEl, 'a_n = ' + s.name, [['Umformung', s.step], ['a_' + N, fmt(vals[N - 1], 6)]],
      'Die Rechenregeln (Summe, Differenz, Produkt, Quotient) gelten nur, wenn die einzelnen Folgen konvergieren (beim Quotienten Nenner-Limes ≠ 0).', s.L === null);
  });
  MW.select(ctl, 'Beispiel', Object.entries(S).map(([k, s]) => [k, s.name]), x => { key = x; view.redraw(); });
  MW.slider(ctl, { label: 'Glieder', min: 5, max: 60, step: 1, value: N, fmt: x => String(x), onInput: x => { N = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 1.5
W.append(dict(file='1-5-geometrische-folge.html', title='Geometrische Folge a<sub>n</sub> = a q<sup>n</sup>',
  sub='Für |q| < 1 ist die Folge eine Nullfolge: |a q<sup>m</sup>| < ε gilt für m > (log ε − log|a|)/log|q|. Für |q| > 1 wächst |a<sub>n</sub>| über alle Grenzen.',
  hint='q und ε ändern.', legend=[('--c2', 'a qⁿ'), ('--c3', 'Streifen ±ε'), ('--c1', 'm aus der Formel')], js=AX + r'''
  let a = 2, q = 0.8, le = Math.log10(0.1);
  const view = MW.View2D(cv, ''' + BOX + r''', v => {
    const C = v.C, N = 30, eps = Math.pow(10, le), vals = []; for (let n = 0; n <= N; n++) vals.push(a * q ** n);
    const lim = Math.min(Math.max(...vals.map(Math.abs)), 12) * 1.1, A = mkAx(-0.5, N + 0.5, -lim, lim); axes(v, A, 'n', 'a_n', 5);
    v.poly([A.P(-0.5, -eps), A.P(N + 0.5, -eps), A.P(N + 0.5, eps), A.P(-0.5, eps)], C.c3, 1, [5, 4], true, C.fill);
    let mStr = '–';
    if (Math.abs(q) < 1 && q !== 0) { const mb = (Math.log(eps) - Math.log(Math.abs(a))) / Math.log(Math.abs(q)), m = Math.max(0, Math.floor(mb) + 1); mStr = fmt(mb, 2) + '  ⇒  m = ' + m;
      if (m <= N) { v.line(A.P(m - 0.5, -lim), A.P(m - 0.5, lim), C.c1, 1.4, [3, 3]); v.text(A.P(m - 0.5, lim), 'm = ' + m, C.c1, 4, 14, 12); } }
    vals.forEach((y, n) => { if (A.inY(y)) v.dot(A.P(n, y), C.c2, 4); });
    const kind = Math.abs(q) < 1 ? 'Nullfolge' : Math.abs(q) === 1 ? (q === 1 ? 'konstant' : 'springt zwischen ±a, divergent') : 'nicht beschränkt, divergent';
    MW.info(infoEl, '|q| ' + (Math.abs(q) < 1 ? '< 1' : Math.abs(q) > 1 ? '> 1' : '= 1') + ': ' + kind, [['(log ε − log|a|)/log|q|', mStr], ['a_30', fmt(vals[N], 6)]],
      q < 0 ? 'Bei q < 0 wechselt das Vorzeichen bei jedem Schritt. Für die Konvergenz zählt nur |q|.' : 'Wegen log|q| < 0 dreht sich beim Auflösen nach m das Ungleichheitszeichen.');
  });
  MW.slider(ctl, { label: 'q', min: -1.15, max: 1.15, step: 0.01, value: q, onInput: x => { q = x; view.redraw(); } });
  MW.slider(ctl, { label: 'a', min: 0.5, max: 4, step: 0.1, value: a, onInput: x => { a = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ε', min: -3, max: 0, step: 0.01, value: le, fmt: x => fmt(Math.pow(10, x), 4), onInput: x => { le = x; view.redraw(); } });
'''))

W.append(dict(file='1-5-geometrische-reihe.html', title='Geometrische Reihe: s<sub>n</sub> = 1 + x + … + x<sup>n</sup> → 1/(1 − x)',
  sub='Links: die Folge der Teilsummen s<sub>n</sub> für festes x. Rechts: das Polynom s<sub>N</sub>(x) neben 1/(1 − x). Für |x| < 1 nähern sich die Teilsummen dem Funktionswert, für |x| ≥ 1 nicht.',
  hint='x und N ändern.', tall=True, legend=[('--c2', 's_n bzw. s_N(x)'), ('--c1', '1/(1 − x)')], js=AX + r'''
  let x = 0.6, N = 6;
  const view = MW.View2D(cv, { xmin: -0.7, xmax: 7.6, ymin: -0.5, ymax: 3.7 }, v => {
    const C = v.C, s = []; let p = 1, sum = 0; for (let n = 0; n <= 30; n++) { sum += p; s.push(sum); p *= x; }
    const lim = 1 / (1 - x), conv = Math.abs(x) < 1;
    const ymax = Math.min(12, Math.max(4, conv ? lim * 1.3 : 6)), ymin = Math.min(-1, ...s.filter(isFinite).map(y => Math.max(y, -6)));
    const A = mkAx(0, 30.5, ymin, ymax, 3.4, 3.2); axes(v, A, 'n', 's_n', 10);
    if (conv) { v.line(A.P(0, lim), A.P(30.5, lim), C.c1, 1.3, [5, 4]); }
    s.forEach((y, n) => { if (A.inY(y)) v.dot(A.P(n, y), n === N ? C.fg : C.c2, n === N ? 5 : 3.2); });
    const B = mkAx(-1.5, 1.5, -1, 8, 3.2, 3.2, 4.1, 0); axes(v, B, 'x', '', 0.5, 2);
    fplot(v, B, t => 1 / (1 - t), C.c1, 2, 600, -1.5, 0.995); fplot(v, B, t => 1 / (1 - t), C.c1, 2, 200, 1.005, 1.5);
    v.poly([B.P(-1, -1), B.P(1, -1), B.P(1, 8), B.P(-1, 8)], null, 1, null, true, C.fill);
    fplot(v, B, t => { let q = 1, r = 0; for (let k = 0; k <= N; k++) { r += q; q *= t; } return r; }, C.c2, 2);
    if (B.inY(s[N])) v.dot(B.P(x, s[N]), C.fg, 5); if (conv && B.inY(lim)) v.dot(B.P(x, lim), C.c1, 4, true);
    v.line(B.P(x, -1), B.P(x, 8), C.muted, 1, [3, 3]);
    MW.info(infoEl, conv ? '|x| < 1: s_n → 1/(1 − x) = ' + fmt(lim, 5) : '|x| ≥ 1: die Reihe divergiert', [['s_' + N + ' = (1 − x^' + (N + 1) + ')/(1 − x)', fmt(s[N], 5)], ['s_30', fmt(s[30], 5)]],
      'Die Formel 1 + x + x² + … = 1/(1 − x) gilt nur auf D = (−1, 1) (blau hinterlegt). Ausserhalb ist die linke Seite gar nicht definiert, obwohl die rechte Seite einen Wert hat.', !conv);
  });
  MW.slider(ctl, { label: 'x', min: -1.2, max: 1.2, step: 0.01, value: x, onInput: t => { x = t; view.redraw(); } });
  MW.slider(ctl, { label: 'N', min: 0, max: 30, step: 1, value: N, fmt: t => String(t), onInput: t => { N = t; view.redraw(); } });
'''))

W.append(dict(file='1-3-rekursion-wurzel.html', title='Übung: a<sub>1</sub> = 1, a<sub>n+1</sub> = √(2 + a<sub>n</sub>)',
  sub='Links die Glieder (n, a<sub>n</sub>) im Streifen 0 < a<sub>n</sub> < 2. Rechts das Treppendiagramm: Von a<sub>n</sub> senkrecht zur Kurve y = √(2 + x) ergibt a<sub>n+1</sub>, waagrecht zur Diagonalen y = x überträgt den Wert zurück auf die x-Achse.',
  hint='Schritte erhöhen. Startwert ändern, auch über 2.', tall=True, legend=[('--c2', 'Glieder a_n'), ('--c3', 'Schranken 0 und 2'), ('--c1', 'Grenzwert L = 2'), ('--c4', 'y = √(2 + x)')], js=AX + r'''
  let a1 = 1, N = 5;
  const f = x => Math.sqrt(2 + x);
  const view = MW.View2D(cv, { xmin: -0.7, xmax: 7.7, ymin: -0.5, ymax: 3.75 }, v => {
    const C = v.C, a = [a1]; for (let n = 1; n < 12; n++) a.push(f(a[n - 1]));
    const top = Math.max(2.4, a1 * 1.08), lo = a1 < 2 ? 0 : 2, hi = a1 < 2 ? 2 : a1;
    // links: Folge
    const A = mkAx(0, 12.5, 0, top, 3.4, 3.2); axes(v, A, 'n', 'a_n', 2, 0.5);
    v.poly([A.P(0, lo), A.P(12.5, lo), A.P(12.5, hi), A.P(0, hi)], null, 1, null, true, C.fill);
    v.line(A.P(0, 0), A.P(12.5, 0), C.c3, 2); v.text(A.P(10, 0), 'u = 0', C.c3, 0, -6, 12, true, 'right');
    v.line(A.P(0, 2), A.P(12.5, 2), C.c1, 1.6, [6, 4]); v.text(A.P(12.5, 2), a1 < 2 ? 'o = 2 = L' : 'L = 2', C.c1, -4, -6, 12, true, 'right');
    for (let n = 1; n <= N; n++) v.dot(A.P(n, a[n - 1]), n === N ? C.fg : C.c2, n === N ? 5.5 : 4.5);
    // rechts: Treppendiagramm
    const T = Math.max(3, a1 * 1.1), B = mkAx(0, T, 0, T, 3.2, 3.2, 4.3, 0); axes(v, B, 'x', 'y', 0.5, 0.5);
    if (a1 < 2) v.poly([B.P(0, 0), B.P(2, 0), B.P(2, 2), B.P(0, 2)], C.c3, 1, [3, 3], true, 'rgba(15,157,88,0.10)');
    v.line(B.P(0, 0), B.P(T, T), C.muted, 1.4);
    fplot(v, B, f, C.c4, 2.5, 300, 0, T);
    v.dot(B.P(2, 2), C.c1, 5); v.text(B.P(2, 2), 'Fixpunkt (2, 2)', C.c1, 8, 16, 11);
    let x = a[0], path = [B.P(x, 0)];
    for (let n = 1; n < N; n++) { const y = f(x); path.push(B.P(x, y)); path.push(B.P(y, y)); x = y; }
    v.poly(path, C.c2, 1.6);
    for (let n = 1; n <= N; n++) v.dot(B.P(a[n - 1], 0), n === N ? C.fg : C.c2, n === N ? 5 : 3.5);
    const inc = a1 < 2;
    MW.info(infoEl, inc ? '0 < a_n < 2, wachsend → konvergent gegen 2' : (a1 === 2 ? 'konstant 2' : '2 < a_n, fallend → konvergent gegen 2'),
      [['a_1 … a_' + Math.min(N, 6), a.slice(0, Math.min(N, 6)).map(t => fmt(t, 4)).join(', ')], ['a_' + N, fmt(a[N - 1], 8)], ['2 − a_' + N, fmt(2 - a[N - 1], 8)]],
      inc ? 'Grünes Quadrat = Induktionsschritt: Liegt a_n zwischen 0 und 2, liegt die Kurve dort unter 2, also auch a_{n+1}. Weil die Kurve über der Diagonalen liegt, ist a_{n+1} > a_n.'
          : 'Startwert über 2: Jetzt liegt die Kurve unter der Diagonalen. Die Folge fällt, bleibt aber über 2. Untere Schranke 2, wieder konvergent gegen L = 2.');
  });
  MW.slider(ctl, { label: 'Schritte n', min: 1, max: 12, step: 1, value: N, fmt: t => String(t), onInput: t => { N = t; view.redraw(); } });
  MW.slider(ctl, { label: 'a₁', min: 0, max: 4, step: 0.05, value: a1, onInput: t => { a1 = t; view.redraw(); } });
'''))

if __name__ == '__main__':
    print(build('analysis-w1', W))
