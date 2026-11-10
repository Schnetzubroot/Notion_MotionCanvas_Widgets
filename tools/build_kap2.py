"""Widgets zu Kapitel 2 (Woche 2): Geschwindigkeit."""
from template import build

W = []

# gemeinsame Hilfsfunktion: Kurve nach Bogenlänge parametrisieren
ARC = r'''
  function arcCurve(f, a, b, N = 600) {
    const P = [], L = [0];
    for (let i = 0; i <= N; i++) P.push(f(a + (b - a) * i / N));
    for (let i = 1; i <= N; i++) L.push(L[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
    const total = L[N];
    const at = s => { s = Math.max(0, Math.min(total, s)); let i = 1; while (i < N && L[i] < s) i++;
      const u = (s - L[i - 1]) / (L[i] - L[i - 1] || 1), p = [P[i - 1][0] + u * (P[i][0] - P[i - 1][0]), P[i - 1][1] + u * (P[i][1] - P[i - 1][1])];
      const tau = V.unit([P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]]); return { p, tau }; };
    return { P, total, at };
  }
'''

CURVE = r'''
  const r = t => [-2.6 + 1.3 * t, 0.3 + 1.6 * Math.sin(0.9 * t)];
  const rd = t => [1.3, 1.44 * Math.cos(0.9 * t)];
  const curve = []; for (let i = 0; i <= 160; i++) curve.push(r(4 * i / 160));
'''

# ---------------------------------------------------------------- 2.1
W.append(dict(file='2-1-differenzenquotient.html', title='Ableitung einer Vektorfunktion als Grenzwert',
  sub='ṙ = lim (r(t + Δt) − r(t)) / Δt für Δt → 0. Mach Δt klein: Der Differenzenquotient dreht in die Tangentenrichtung und wird zu ṙ.',
  hint='Δt verkleinern.', legend=[('--fg', 'r(t), r(t + Δt)'), ('--c3', 'Δr'), ('--c4', 'Δr / Δt'), ('--c1', 'ṙ(t)')], js=CURVE + r'''
  let t = 1.2, dt = 1.2;
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 3.4, ymin: -0.6, ymax: 3 }, v => {
    const C = v.C; v.grid(1, true, false);
    v.poly(curve, C.line, 2); v.text(curve[150], 'C', C.muted, 6, -6, 13, false);
    const M = r(t), M2 = r(t + dt), dr = V.sub(M2, M), q = V.mul(dr, 1 / dt), d = rd(t);
    v.arrow([0, 0], M, C.fg, 1.6); v.arrow([0, 0], M2, C.fg, 1.2); v.text(V.mul(M, 0.5), 'r(t)', C.fg, -40, 0, 12);
    v.text(V.mul(M2, 0.6), 'r(t+Δt)', C.fg, 6, 0, 12);
    v.arrow(M, dr, C.c3, 2.5);
    v.arrow(M, V.mul(q, 0.7), C.c4, 3);
    v.arrow(M, V.mul(d, 0.7), C.c1, 2, 9);
    v.dot(M, C.fg, 5); v.dot(M2, C.fg, 4); v.text(M, 'M(t)', C.fg, -10, 18, 12); v.text(M2, 'M(t+Δt)', C.fg, 6, 16, 12);
    MW.info(infoEl, 'Δt = ' + fmt(dt), [['Δr / Δt', fv(q)], ['ṙ(t)', fv(d)], ['|Δr/Δt − ṙ|', fmt(V.norm(V.sub(q, d)), 3)]],
      'Für Δt → 0 geht der Differenzenquotient gegen ṙ. Der Vektor ṙ liegt auf der Tangente an die Kurve in M(t). (Pfeile Δr/Δt und ṙ sind mit 0,7 skaliert.)');
  });
  MW.slider(ctl, { label: 'Δt', min: 0.02, max: 1.6, step: 0.01, value: dt, onInput: x => { dt = x; view.redraw(); } });
  MW.slider(ctl, { label: 't', min: 0.2, max: 2.3, step: 0.01, value: t, onInput: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='2-1-differential.html', title='Differential dr = ṙ dt als lineare Näherung',
  sub='Die echte Änderung ist Δr = ṙ Δt + u Δt. Der Fehler u Δt wird schneller klein als Δt, weil u → 0 für Δt → 0.',
  hint='Δt verkleinern.', legend=[('--c3', 'Δr (echt)'), ('--c1', 'ṙ Δt (Differential)'), ('--c5', 'u Δt (Fehler)')], js=CURVE + r'''
  let t = 1.2, dt = 1.2;
  const view = MW.View2D(cv, { xmin: -3.2, xmax: 3.4, ymin: -0.6, ymax: 3 }, v => {
    const C = v.C; v.grid(1, true, false);
    v.poly(curve, C.line, 2);
    const M = r(t), M2 = r(t + dt), dr = V.sub(M2, M), lin = V.mul(rd(t), dt), err = V.sub(dr, lin);
    v.line(V.sub(M, V.mul(rd(t), 1.2)), V.add(M, V.mul(rd(t), 1.8)), C.line, 1, [4, 4]);
    v.arrow(M, dr, C.c3, 3); v.arrow(M, lin, C.c1, 2.5); v.arrow(V.add(M, lin), err, C.c5, 2.5);
    v.dot(M, C.fg, 5); v.dot(M2, C.fg, 4); v.text(M, 'M(t)', C.fg, -10, 18, 12); v.text(M2, 'M(t+Δt)', C.fg, 6, -6, 12);
    MW.info(infoEl, 'Δt = ' + fmt(dt), [['|Δr|', fmt(V.norm(dr), 3)], ['|ṙ Δt|', fmt(V.norm(lin), 3)], ['|u| = |Δr/Δt − ṙ|', fmt(V.norm(err) / dt, 3)], ['|u Δt| / Δt', fmt(V.norm(err) / dt, 3)]],
      'Das Differential dr = ṙ dt liegt immer auf der Tangente (gestrichelt). Je kleiner Δt, desto kleiner wird der violette Fehler im Verhältnis zu Δt.');
  });
  MW.slider(ctl, { label: 'Δt', min: 0.02, max: 1.6, step: 0.01, value: dt, onInput: x => { dt = x; view.redraw(); } });
  MW.slider(ctl, { label: 't', min: 0.2, max: 2.3, step: 0.01, value: t, onInput: x => { t = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 2.2
W.append(dict(file='2-2-bogenlaenge-schwingung.html', title='Bogenlänge s und Schnelligkeit ṡ',
  sub='Bewegung auf einer festen Kurve: s(t) = s₀ sin(2πt/T), gemessen ab A. Der Betrag |ṡ| sagt, wie schnell; das Vorzeichen von ṡ sagt, in welche Richtung.',
  hint='Abspielen.', legend=[('--c2', 's(t) im Diagramm'), ('--c1', 'v = ṡ τ')], js=ARC + r'''
  const cur = arcCurve(x => [x, 0.9 + 0.35 * x * x - 0.04 * x ** 4], -2.6, 2.6);
  const mid = cur.total / 2, s0 = 2.2; let t = 0.1;
  const view = MW.View2D(cv, { xmin: -3, xmax: 3, ymin: -2.7, ymax: 2.6 }, v => {
    const C = v.C;
    v.poly(cur.P, C.line, 2.5);
    const A = cur.at(mid); v.dot(A.p, C.muted, 4); v.text(A.p, 'A (s = 0)', C.muted, -24, 18, 12, false);
    v.arrow(cur.at(mid + 1.4).p, V.mul(cur.at(mid + 1.4).tau, 0.5), C.muted, 1.5, 7); v.text(cur.at(mid + 1.4).p, '+s', C.muted, 4, -8, 12, false);
    const s = s0 * Math.sin(2 * Math.PI * t), sd = s0 * 2 * Math.PI * Math.cos(2 * Math.PI * t), P = cur.at(mid + s);
    v.arrow(P.p, V.mul(P.tau, sd * 0.12), C.c1, 3); v.dot(P.p, C.fg, 7); v.text(P.p, 'M', C.fg, 6, -10);
    // Diagramm s(t)
    const gx = tt => -2.6 + 5.2 * tt, gy = ss => -1.6 + ss * 0.4;
    v.line([-2.7, -1.6], [2.8, -1.6], C.muted, 1); v.line([-2.6, -2.6], [-2.6, -0.6], C.muted, 1);
    v.text([2.7, -1.6], 't', C.muted, 0, -6, 12, false); v.text([-2.6, -0.6], 's', C.muted, 6, 4, 12, false);
    const g = []; for (let i = 0; i <= 100; i++) g.push([gx(i / 100), gy(s0 * Math.sin(2 * Math.PI * i / 100))]); v.poly(g, C.c2, 2);
    v.dot([gx(t), gy(s)], C.c2, 5); v.line([gx(t), -2.6], [gx(t), -0.6], C.line, 1, [3, 3]);
    MW.info(infoEl, sd > 0.05 ? 'ṡ > 0: M läuft in Richtung wachsender s' : sd < -0.05 ? 'ṡ < 0: M läuft zurück' : 'ṡ = 0: Umkehrpunkt',
      [['t / T', fmt(t)], ['s', fmt(s)], ['ṡ', fmt(sd)], ['|ṡ|', fmt(Math.abs(sd))]],
      'Aus s(t) allein erfährt man nichts über die Form der Bahnkurve, nur wie weit M entlang der Kurve von A entfernt ist.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 5, value: 0.1, label: 't/T', onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='2-2-gleichfoermig.html', title='Gleichförmige Bewegung: konstante Schnelligkeit, aber veränderliche Geschwindigkeit',
  sub='Gleichförmig heisst ṡ = konst., also s = s₀ + ṡ t. Auf einer gekrümmten Bahn ändert sich trotzdem die Richtung von v. Erst auf einer Geraden ist die Bewegung geradlinig gleichförmig.',
  hint='Abspielen.', legend=[('--c1', 'v jetzt'), ('--field', 'v zu früheren Zeiten')], js=ARC + r'''
  const cur = arcCurve(a => [2.4 * Math.cos(a), 1.3 * Math.sin(a) + 0.2 * Math.sin(3 * a)], 0, 2 * Math.PI, 900);
  const sd = 1.5; let t = 2.5;
  const view = MW.View2D(cv, { xmin: -3, xmax: 3, ymin: -1.8, ymax: 1.8 }, v => {
    const C = v.C; v.poly(cur.P, C.line, 2.5);
    const sNow = (sd * t) % cur.total;
    for (let k = 1; k <= 6; k++) { const s = sNow - k * 1.2; if (s < 0) continue; const P = cur.at(s); v.arrow(P.p, V.mul(P.tau, sd * 0.5), C.field, 1.6, 7); v.dot(P.p, C.field, 3); }
    const P = cur.at(sNow); v.arrow(P.p, V.mul(P.tau, sd * 0.5), C.c1, 3); v.dot(P.p, C.fg, 6); v.text(P.p, 'M', C.fg, 6, -8);
    MW.info(infoEl, 'Gleichförmig: |v| = ṡ = ' + fmt(sd) + ' bleibt konstant', [['Richtung von v', fv(P.tau)]],
      'Alle Pfeile sind gleich lang, zeigen aber in verschiedene Richtungen. Konstante Schnelligkeit bedeutet nicht konstante Geschwindigkeit.');
  });
  MW.player(ctl, { t0: 0, t1: 9, duration: 9, value: 2.5, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='2-2-v-tau.html', title='Geschwindigkeit v = ṡ τ',
  sub='τ ist der Einheitsvektor tangential zur Bahn in Richtung wachsender s. Bei ṡ > 0 zeigt v wie τ, bei ṡ < 0 entgegen.',
  hint='ṡ ändern, M auf der Kurve verschieben.', legend=[('--c2', 'τ (Betrag 1)'), ('--c1', 'v = ṡ τ')], js=ARC + r'''
  const cur = arcCurve(x => [x, 0.4 * Math.sin(1.3 * x) + 0.1 * x], -2.8, 2.8);
  let sd = 1.2, pos = 0.45;
  const view = MW.View2D(cv, { xmin: -3, xmax: 3, ymin: -1.6, ymax: 1.6 }, v => {
    const C = v.C; v.poly(cur.P, C.line, 2.5);
    v.arrow(cur.P[560], V.sub(cur.P[600], cur.P[560]), C.muted, 1.5, 8); v.text(cur.P[580], '+s', C.muted, 0, -10, 12, false);
    const P = cur.at(pos * cur.total);
    v.arrow(P.p, P.tau, C.c2, 2.5); v.text(V.add(P.p, P.tau), 'τ', C.c2, 4, -4);
    v.arrow(P.p, V.mul(P.tau, sd), C.c1, 3.5, 12); v.text(V.add(P.p, V.mul(P.tau, sd)), 'v', C.c1, 4, 16);
    v.dot(P.p, C.fg, 6); v.text(P.p, 'M', C.fg, -16, -8);
    MW.info(infoEl, 'ṡ = ' + fmt(sd) + (sd < 0 ? ': v zeigt entgegen τ' : sd > 0 ? ': v zeigt wie τ' : ': v = 0'),
      [['|v|', fmt(Math.abs(sd))], ['τ', fv(P.tau)]], 'Die Geschwindigkeit ist immer tangential zur Bahnkurve. Ihr Betrag ist |ṡ|.');
  });
  MW.slider(ctl, { label: 'ṡ', min: -2, max: 2, step: 0.05, value: sd, onInput: x => { sd = x; view.redraw(); } });
  MW.slider(ctl, { label: 'Lage', min: 0.05, max: 0.95, step: 0.005, value: pos, onInput: x => { pos = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 2.3
W.append(dict(file='2-3-sehne-bogen.html', title='Sehne und Bogen: dr/ds = τ',
  sub='Δs ist die Bogenlänge von M nach M\', |Δr| die Länge der Sehne. Für Δs → 0 wird |Δr|/Δs → 1, und Δr/Δs wird zum Einheitsvektor τ.',
  hint='Δs verkleinern.', legend=[('--c2', 'Bogen Δs'), ('--c3', 'Sehne Δr'), ('--c4', 'Δr / Δs'), ('--c1', 'τ')], js=r'''
  const R = 2; let ds = 2.5; const a0 = -0.4;
  const view = MW.View2D(cv, { xmin: -2.2, xmax: 2.8, ymin: -1.2, ymax: 2.4 }, v => {
    const C = v.C;
    v.arc([0, 0], R, a0 - 0.4, a0 + 2.4, C.line, 2);
    const a1 = a0 + ds / R, M = [R * Math.cos(a0), R * Math.sin(a0)], M2 = [R * Math.cos(a1), R * Math.sin(a1)];
    v.arc([0, 0], R, a0, a1, C.c2, 5);
    const dr = V.sub(M2, M), tau = [-Math.sin(a0), Math.cos(a0)];
    v.arrow(M, dr, C.c3, 2.5);
    v.arrow(M, V.mul(dr, 1 / ds), C.c4, 3); v.arrow(M, tau, C.c1, 2, 9);
    v.dot(M, C.fg, 5); v.dot(M2, C.fg, 5); v.text(M, 'M', C.fg, 8, 6); v.text(M2, "M'", C.fg, 8, -4);
    MW.info(infoEl, '|Δr| / Δs = ' + fmt(V.norm(dr) / ds, 4), [['Δs (Bogen)', fmt(ds, 3)], ['|Δr| (Sehne)', fmt(V.norm(dr), 3)], ['Winkel zwischen Δr/Δs und τ', fmt((ds / R / 2) * 180 / Math.PI, 1) + '°']],
      'Die Sehne ist immer kürzer als der Bogen, aber für Δs → 0 werden beide gleich lang. Darum ist dr/ds ein Einheitsvektor: der Tangentenvektor τ.');
  });
  MW.slider(ctl, { label: 'Δs', min: 0.05, max: 4, step: 0.01, value: ds, onInput: x => { ds = x; view.redraw(); } });
'''))

W.append(dict(file='2-3-v-gleich-rdot.html', title='v = ṙ: Geschwindigkeit ist die Ableitung des Ortsvektors',
  sub='Die Spitze des Ortsvektors r(t) zeichnet die Bahnkurve. Seine zeitliche Ableitung ṙ ist die Geschwindigkeit v, tangential zur Bahn.',
  hint='Abspielen.', legend=[('--fg', 'r(t)'), ('--c1', 'v = ṙ'), ('--c3', 'Bahnkurve')], js=r'''
  const r = t => [2.2 * Math.cos(t) - 0.3, 1.3 * Math.sin(t) + 0.4 * Math.sin(2 * t)];
  const rd = t => [-2.2 * Math.sin(t), 1.3 * Math.cos(t) + 0.8 * Math.cos(2 * t)];
  let t = 1;
  const view = MW.View2D(cv, { xmin: -3, xmax: 2.6, ymin: -1.9, ymax: 1.9 }, v => {
    const C = v.C; v.grid(1, true, false);
    const pts = []; for (let i = 0; i <= 120; i++) pts.push(r(t * i / 120)); v.poly(pts, C.c3, 2.5);
    const M = r(t); v.arrow([0, 0], M, C.fg, 2); v.text(V.mul(M, 0.5), 'r', C.fg, 6, -4);
    v.arrow(M, V.mul(rd(t), 0.5), C.c1, 3); v.text(V.add(M, V.mul(rd(t), 0.5)), 'v', C.c1, 4, -4);
    v.dot(M, C.fg, 6); v.dot([0, 0], C.fg, 4); v.text([0, 0], 'O', C.fg, -14, 16);
    MW.info(infoEl, 'v = ṙ = ' + fv(rd(t)), [['r', fv(M)], ['Schnelligkeit |v|', fmt(V.norm(rd(t)))]],
      'Formel (2.5): v = ṙ. Zusammen mit v = ṡ τ (2.3) sind das zwei gleichwertige Definitionen der Geschwindigkeit. (v ist mit 0,5 skaliert.)');
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 8, value: 1, onTime: x => { t = x; view.redraw(); } });
'''))

# ---------------------------------------------------------------- 2.4
W.append(dict(file='2-4-v-kartesisch.html', title='Kartesische Komponenten: Stabspitze (Buchbeispiel)',
  sub='x = 3 cos(3πt), y = 4 cos(3πt), z = sin(3πt). Einfach komponentenweise ableiten: v = (−9π sin 3πt, −12π sin 3πt, 3π cos 3πt) cm/s.',
  hint='t ziehen oder abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'v'), ('--c3', 'ẋ e_x + ẏ e_y'), ('--c2', 'ż e_z')], js=r'''
  let t = 0.1; const k = 0.07, pi = Math.PI;
  const r = tt => [3 * Math.cos(3 * pi * tt), 4 * Math.cos(3 * pi * tt), Math.sin(3 * pi * tt)];
  const vel = tt => [-9 * pi * Math.sin(3 * pi * tt), -12 * pi * Math.sin(3 * pi * tt), 3 * pi * Math.cos(3 * pi * tt)];
  const view = MW.View3D(cv, { extent: 4.2, yaw: -40, pitch: 20 }, v => {
    const C = v.C; v.axes(4.5);
    const pts = []; for (let i = 0; i <= 120; i++) pts.push(r(i / 120 * (2 / 3))); v.poly(pts, C.field, 1.5);
    const M = r(t), vv = vel(t);
    v.arrow(M, [k * vv[0], k * vv[1], 0], C.c3, 2); v.arrow(V.add(M, [k * vv[0], k * vv[1], 0]), [0, 0, k * vv[2]], C.c2, 2);
    v.arrow(M, V.mul(vv, k), C.c1, 3.5); v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, -8);
    const sp = 3 * pi * Math.sqrt(1 + 24 * Math.sin(3 * pi * t) ** 2);
    const note = Math.abs(Math.cos(3 * pi * t)) < 0.02 ? 'ż = 0: v ist horizontal (t = 1/6, 1/2, 5/6 s).' : Math.abs(Math.sin(3 * pi * t)) < 0.02 ? 'ẋ = ẏ = 0: v ist vertikal (t = 0, 1/3, 2/3, 1 s).' : 'v ist immer tangential zur Ellipse.';
    MW.info(infoEl, 't = ' + fmt(t, 3) + ' s', [['v (cm/s)', fv(vv, 1)], ['Schnelligkeit |v|', fmt(sp, 2) + ' cm/s'], ['ż', fmt(vv[2], 2)], ['ẏ / ẋ', Math.abs(vv[0]) > 1e-6 ? fmt(vv[1] / vv[0], 3) : '–']],
      note + ' ė_x = ė_y = ė_z = 0, darum entstehen keine Zusatzterme.');
  });
  MW.player(ctl, { t0: 0, t1: 1, duration: 8, value: 0.1, onTime: x => { t = x; view.redraw(); }, fmt: x => fmt(x, 3) + ' s' });
  MW.button(ctl, 't = 1/6', () => { t = 1 / 6; view.redraw(); });
  MW.button(ctl, 't = 1/3', () => { t = 1 / 3; view.redraw(); });
'''))

W.append(dict(file='2-4-dr-zylindrisch.html', title='Herleitung: dr = dρ e<sub>ρ</sub> + ρ dφ e<sub>φ</sub> + dz e<sub>z</sub>',
  sub='Draufsicht. Ändert sich ρ um dρ, bewegt sich M radial um dρ. Ändert sich φ um dφ, läuft M auf einem Kreis mit Radius ρ: der Weg ist ρ dφ, nicht dφ.',
  hint='dρ und dφ einstellen, ρ vergrössern.', legend=[('--c1', 'dρ e_ρ'), ('--c3', 'ρ dφ e_φ'), ('--fg', 'dr')], js=r'''
  let rho = 2, phi = 0.5, drho = 0.5, dphi = 0.35;
  const view = MW.View2D(cv, { xmin: -0.6, xmax: 3.8, ymin: -0.4, ymax: 3.2 }, v => {
    const C = v.C; v.grid(1);
    const er = [Math.cos(phi), Math.sin(phi)], ep = [-Math.sin(phi), Math.cos(phi)], M = V.mul(er, rho);
    const M2 = V.mul([Math.cos(phi + dphi), Math.sin(phi + dphi)], rho + drho);
    v.line([0, 0], M, C.line, 1, [4, 4]); v.arc([0, 0], rho, 0, phi + dphi + 0.3, C.line, 1, [4, 4]);
    v.arc([0, 0], 0.5, phi, phi + dphi, C.muted, 1.5); v.text([0.6 * Math.cos(phi + dphi / 2), 0.6 * Math.sin(phi + dphi / 2)], 'dφ', C.muted, 2, 4, 12);
    v.arc([0, 0], rho, phi, phi + dphi, C.c3, 4);
    v.arrow(M, V.mul(er, drho), C.c1, 3); v.arrow(V.add(M, V.mul(er, drho)), V.mul(ep, rho * dphi), C.c3, 3);
    v.arrow(M, V.sub(M2, M), C.fg, 2, 9);
    v.dot(M, C.fg, 5); v.text(M, 'M', C.fg, 6, 16); v.dot(M2, C.fg, 4); v.text(M2, "M'", C.fg, 6, -6);
    MW.info(infoEl, 'Weg in φ-Richtung: ρ dφ = ' + fmt(rho * dphi, 3), [['dρ', fmt(drho, 3)], ['dφ (Winkel!)', fmt(dphi, 3)], ['ρ', fmt(rho)], ['|dr| (für kleine dρ, dφ)', fmt(Math.hypot(drho, rho * dphi), 3)]],
      'Durch dt teilen: v = ρ̇ e_ρ + ρφ̇ e_φ + ż e_z. Der Faktor ρ im mittleren Term kommt genau von diesem Kreisbogen.');
  });
  MW.slider(ctl, { label: 'dρ', min: 0, max: 0.8, step: 0.01, value: drho, onInput: x => { drho = x; view.redraw(); } });
  MW.slider(ctl, { label: 'dφ', min: 0, max: 0.6, step: 0.01, value: dphi, onInput: x => { dphi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'ρ', min: 0.5, max: 2.6, step: 0.05, value: rho, onInput: x => { rho = x; view.redraw(); } });
'''))

W.append(dict(file='2-4-erho-ableitung.html', title='Warum ė<sub>ρ</sub> = φ̇ e<sub>φ</sub>',
  sub='Zeichnet man e<sub>ρ</sub> immer ab demselben Punkt, läuft seine Spitze auf dem Einheitskreis. Die Änderung Δe<sub>ρ</sub> zeigt für kleine Δφ in Richtung e<sub>φ</sub> und hat die Länge Δφ.',
  hint='Δφ verkleinern.', legend=[('--c1', 'e_ρ(φ), e_ρ(φ+Δφ)'), ('--c3', 'Δe_ρ / Δφ'), ('--c2', 'e_φ')], js=r'''
  let phi = 0.5, dphi = 1;
  const view = MW.View2D(cv, { xmin: -1.4, xmax: 1.8, ymin: -0.4, ymax: 1.6 }, v => {
    const C = v.C; v.grid(0.5, true, false);
    v.circle([0, 0], 1, C.line, 1.5);
    const e1 = [Math.cos(phi), Math.sin(phi)], e2 = [Math.cos(phi + dphi), Math.sin(phi + dphi)], ep = [-Math.sin(phi), Math.cos(phi)];
    v.arrow([0, 0], e1, C.c1, 3); v.arrow([0, 0], e2, C.c1, 1.8);
    v.text(e1, 'e_ρ(φ)', C.c1, 6, 8, 12); v.text(e2, 'e_ρ(φ+Δφ)', C.c1, -30, -8, 12);
    const de = V.sub(e2, e1);
    v.line(e1, e2, C.muted, 1, [3, 3]);
    v.arrow(e1, V.mul(de, 1 / dphi), C.c3, 3); v.arrow(e1, ep, C.c2, 2, 9);
    v.arc([0, 0], 0.3, phi, phi + dphi, C.muted, 1.5);
    MW.info(infoEl, '|Δe_ρ| / Δφ = ' + fmt(V.norm(de) / dphi, 4),
      [['Δe_ρ / Δφ', fv(V.mul(de, 1 / dphi), 3)], ['e_φ', fv(ep, 3)]],
      'Für Δφ → 0 wird Δe_ρ/Δφ = e_φ, also de_ρ/dφ = e_φ. Mit der Kettenregel: ė_ρ = (de_ρ/dφ) φ̇ = φ̇ e_φ. Genauso: ė_φ = −φ̇ e_ρ.');
  });
  MW.slider(ctl, { label: 'Δφ', min: 0.02, max: 1.5, step: 0.01, value: dphi, onInput: x => { dphi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: 0, max: 1.5, step: 0.01, value: phi, onInput: x => { phi = x; view.redraw(); } });
'''))

W.append(dict(file='2-4-v-zylindrisch-elektron.html', title='Zylindrische Komponenten: Elektron (Buchbeispiel)',
  sub='ρ = R₁ + a t, φ = b t, z = a t ergibt v = a e<sub>ρ</sub> + b(R₁ + a t) e<sub>φ</sub> + a e<sub>z</sub>. Nur die φ-Komponente wächst, weil ρ wächst.',
  hint='Abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c1', 'ρ̇ e_ρ = a e_ρ'), ('--c3', 'ρφ̇ e_φ'), ('--c2', 'ż e_z = a e_z'), ('--fg', 'v')], js=r'''
  const R1 = 0.6, R2 = 2.4, a = 1, b = 2.5, t2 = (R2 - R1) / a, k = 0.4; let t = 0.4;
  const r = tt => [(R1 + a * tt) * Math.cos(b * tt), (R1 + a * tt) * Math.sin(b * tt), a * tt];
  const view = MW.View3D(cv, { extent: 2.8, yaw: 25, pitch: 20, center: [0, 0, 0.9] }, v => {
    const C = v.C; v.axes(2.6);
    const pts = []; for (let i = 0; i <= 150; i++) pts.push(r(t2 * i / 150)); v.poly(pts, C.field, 1.5);
    const M = r(t), ph = b * t, er = [Math.cos(ph), Math.sin(ph), 0], ep = [-Math.sin(ph), Math.cos(ph), 0], rho = R1 + a * t;
    const c1 = V.mul(er, a * k), c2 = V.mul(ep, b * rho * k), c3 = [0, 0, a * k];
    v.arrow(M, c1, C.c1, 2.5); v.arrow(V.add(M, c1), c2, C.c3, 2.5); v.arrow(V.add(V.add(M, c1), c2), c3, C.c2, 2.5);
    v.arrow(M, V.add(V.add(c1, c2), c3), C.fg, 3);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, -16, 14);
    MW.info(infoEl, 't = ' + fmt(t), [['ρ̇ = a', fmt(a)], ['ρφ̇ = bρ', fmt(b * rho)], ['ż = a', fmt(a)], ['|v| = √(2a² + b²ρ²)', fmt(Math.sqrt(2 * a * a + b * b * rho * rho))]],
      'Zur Zeit t = 0 ist v = a e_ρ + bR₁ e_φ + a e_z, beim Auftreffen auf die Anode v = a e_ρ + bR₂ e_φ + a e_z. (Pfeile mit 0,4 skaliert.)');
  });
  MW.player(ctl, { t0: 0, t1: t2, duration: 6, value: 0.4, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='2-4-kreisbewegung-omega.html', title='Kreisbewegung: v = ω × r',
  sub='ω = φ̇ e<sub>z</sub> steht senkrecht auf der Kreisebene. r darf von jedem Punkt A auf der Drehachse ausgehen: Das Ergebnis v = ω × AM ist immer dasselbe.',
  hint='Punkt A auf der Achse verschieben. Ziehen im Bild dreht die Ansicht.', legend=[('--c2', 'ω'), ('--c4', 'r = AM'), ('--c1', 'v = ω × r')], js=r'''
  const R = 1.8, z0 = 1.2; let zA = 0, phi = 0.9, pd = 1;
  const view = MW.View3D(cv, { extent: 2.6, center: [0, 0, 0.8] }, v => {
    const C = v.C; v.axes(2.4);
    v.poly(v.circlePts([0, 0, z0], [0, 0, 1], R, 0, 2 * Math.PI, 90, [1, 0, 0]), C.line, 1.5);
    v.line([0, 0, -1], [0, 0, 3], C.line, 1, [4, 4]);
    const M = [R * Math.cos(phi), R * Math.sin(phi), z0], A = [0, 0, zA], w = [0, 0, pd], rA = V.sub(M, A), vel = V.cross(w, rA);
    v.arrow([0, 0, 0], V.mul(w, 0.9), C.c2, 3.5); v.text(V.mul(w, 0.9), 'ω', C.c2, 6, 0);
    v.arrow(A, rA, C.c4, 2.5); v.dot(A, C.c4, 5); v.text(A, 'A', C.c4, -16, 4);
    v.arrow(M, V.mul(vel, 0.6), C.c1, 3); v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, 14);
    MW.info(infoEl, 'v = ' + fv(vel), [['r = AM', fv(rA)], ['|v| = R φ̇', fmt(V.norm(vel))], ['z_A', fmt(zA)]],
      'Der Anteil von AM parallel zu ω fällt im Kreuzprodukt weg (e_z × e_z = 0). Darum ist v unabhängig davon, wo A auf der Achse liegt.');
  });
  MW.slider(ctl, { label: 'z_A', min: -1, max: 2.8, step: 0.05, value: zA, onInput: x => { zA = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ', min: 0, max: 6.28, step: 0.01, value: phi, onInput: x => { phi = x; view.redraw(); } });
  MW.slider(ctl, { label: 'φ̇', min: -2, max: 2, step: 0.05, value: pd, onInput: x => { pd = x; view.redraw(); } });
'''))

W.append(dict(file='2-4-v-sphaerisch-kreisel.html', title='Sphärische Komponenten: Achsenspitze des Kreisels (Buchbeispiel)',
  sub='r = R konstant, also ṙ = 0. Es bleiben v = Rθ̇ e<sub>θ</sub> + R sin θ ψ̇ e<sub>ψ</sub> mit θ̇ = θ₀ω₁ cos(ω₁t) und ψ̇ = ω₂.',
  hint='Abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c4', 'Rθ̇ e_θ'), ('--c3', 'R sin θ ψ̇ e_ψ'), ('--fg', 'v')], js=r'''
  const R = 2, th0 = 0.25, w1 = 4, w2 = 1, k = 0.5; let t = 0.6;
  const th = tt => Math.PI / 6 + th0 * Math.sin(w1 * tt);
  const A = tt => { const a = th(tt), p = w2 * tt; return [R * Math.sin(a) * Math.cos(p), R * Math.sin(a) * Math.sin(p), R * Math.cos(a)]; };
  const view = MW.View3D(cv, { extent: 2.2, yaw: 25, pitch: 30, center: [0, 0, 1] }, v => {
    const C = v.C; v.axes(2.4);
    const pts = []; for (let i = 0; i <= 200; i++) pts.push(A(2 * Math.PI * i / 200)); v.poly(pts, C.field, 1.5);
    const a = th(t), p = w2 * t, P = A(t);
    const et = [Math.cos(a) * Math.cos(p), Math.cos(a) * Math.sin(p), -Math.sin(a)], eps = [-Math.sin(p), Math.cos(p), 0];
    const thd = th0 * w1 * Math.cos(w1 * t), c1 = V.mul(et, R * thd * k), c2 = V.mul(eps, R * Math.sin(a) * w2 * k);
    v.arrow(P, c1, C.c4, 2.5); v.arrow(V.add(P, c1), c2, C.c3, 2.5); v.arrow(P, V.add(c1, c2), C.fg, 3);
    v.line([0, 0, 0], P, C.muted, 1.5); v.dot(P, C.fg, 6); v.text(P, 'A', C.fg, -16, -4);
    MW.info(infoEl, Math.abs(thd) < 0.03 ? 'θ̇ = 0: v ist horizontal (Umkehrpunkt in θ)' : 't = ' + fmt(t),
      [['θ̇', fmt(thd)], ['Rθ̇', fmt(R * thd)], ['R sin θ ψ̇', fmt(R * Math.sin(a) * w2)], ['|v|', fmt(Math.hypot(R * thd, R * Math.sin(a) * w2))]],
      'Der Faktor sin θ: Bei Änderung von ψ läuft der Punkt auf einem Parallelkreis mit Radius r sin θ, nicht r. (Pfeile mit 0,5 skaliert.)');
  });
  MW.player(ctl, { t0: 0, t1: 2 * Math.PI, duration: 10, value: 0.6, onTime: x => { t = x; view.redraw(); } });
'''))

W.append(dict(file='2-4-zp22-helix.html', title='ZP1 2022 A1: Schraubenlinie mit abnehmender Geschwindigkeit',
  sub='ρ = R, z = Rφ tan α, v<sub>φ</sub> und v<sub>z</sub> proportional zu e<sup>kt</sup>, v(0) = v₀(e<sub>φ</sub> + e<sub>z</sub>), z(t₁) = 2R bei v(t₁) = v₀/2 · (e<sub>φ</sub> + e<sub>z</sub>). Hier R = v₀ = 1.',
  hint='Abspielen. Ziehen im Bild dreht die Ansicht.', legend=[('--c3', 'v_φ e_φ'), ('--c2', 'v_z e_z'), ('--c1', 'v')], js=r'''
  const k = -0.25, t1 = 4 * Math.log(2); let t = 1;
  const phi = tt => (1 / k) * (Math.exp(k * tt) - 1);
  const P = tt => [Math.cos(phi(tt)), Math.sin(phi(tt)), phi(tt)];
  const view = MW.View3D(cv, { extent: 2.6, yaw: 20, pitch: 18, center: [0, 0, 1.8] }, v => {
    const C = v.C; v.axes(1.6);
    for (const zz of [0, 2, 4]) v.poly(v.circlePts([0, 0, zz], [0, 0, 1], 1, 0, 2 * Math.PI, 72, [1, 0, 0]), C.line, 1, zz === 2 ? null : [3, 3]);
    v.text([1, 0, 2], 'z = 2R', C.muted, 6, 0, 12, false); v.text([1, 0, 4], 'Grenze z → 4R', C.muted, 6, 0, 12, false);
    const pts = []; for (let i = 0; i <= 200; i++) pts.push(P(12 * i / 200)); v.poly(pts, C.field, 1.5);
    const M = P(t), f = phi(t), ep = [-Math.sin(f), Math.cos(f), 0], s = Math.exp(k * t);
    v.arrow(M, V.mul(ep, s), C.c3, 2.5); v.arrow(V.add(M, V.mul(ep, s)), [0, 0, s], C.c2, 2.5); v.arrow(M, V.add(V.mul(ep, s), [0, 0, s]), C.c1, 3);
    v.dot(M, C.fg, 6); v.text(M, 'M', C.fg, 8, 14);
    MW.info(infoEl, Math.abs(t - t1) < 0.05 ? 't = t₁: z = 2R und v halbiert' : 't = ' + fmt(t),
      [['e^{kt}', fmt(s, 3)], ['φ(t) = (v₀/kR)(e^{kt} − 1)', fmt(f, 3)], ['z = Rφ', fmt(f, 3)], ['v = v₀ e^{kt} (e_φ + e_z)', fmt(s, 3) + ' · (e_φ + e_z)']],
      'tan α = v_z/v_φ = 1. Aus e^{kt₁} = 1/2 und φ(t₁) = 2 folgt k = −v₀/(4R). Bei t = 0 gilt e_φ = e_y, also v(0) = v₀(e_y + e_z).');
  });
  MW.player(ctl, { t0: 0, t1: 12, duration: 10, value: 1, onTime: x => { t = x; view.redraw(); } });
  MW.button(ctl, 't = t₁', () => { t = t1; view.redraw(); });
'''))

W.append(dict(file='2-4-zp24-v-zylindrisch.html', title='ZP1 2024 A1.3: Geschwindigkeit in zylindrischer Basis',
  sub='M₁: ρ = R, φ = (2π/3) sin(μt), z = 2Rt/T − R/2. Dann v = ρφ̇ e<sub>φ</sub> + ż e<sub>z</sub> = (2πμR/3) cos(μt) e<sub>φ</sub> + (2R/T) e<sub>z</sub>. Hier R = T = 1, μ = 1.',
  hint='t ziehen. Ziehen im Bild dreht die Ansicht.', legend=[('--c3', 'ρφ̇ e_φ'), ('--c2', 'ż e_z'), ('--c1', 'v')], js=r'''
  const mu = 1, k = 0.35; let t = 2;
  const ph = tt => 2 * Math.PI / 3 * Math.sin(mu * tt);
  const P = tt => [Math.cos(ph(tt)), Math.sin(ph(tt)), 2 * tt - 0.5];
  const view = MW.View3D(cv, { extent: 2.6, yaw: 109, pitch: 15, center: [0, 0, 1.6] }, v => {
    const C = v.C; v.axes(1.6);
    for (const zz of [-0.5, 1.5, 3.5]) v.poly(v.circlePts([0, 0, zz], [0, 0, 1], 1, 0, 2 * Math.PI, 72, [1, 0, 0]), C.line, 1, [3, 3]);
    const pts = []; for (let i = 0; i <= 150; i++) pts.push(P(2 * i / 150)); v.poly(pts, C.field, 1.5);
    const M = P(t), f = ph(t), ep = [-Math.sin(f), Math.cos(f), 0], vp = 2 * Math.PI * mu / 3 * Math.cos(mu * t), vz = 2;
    v.arrow(M, V.mul(ep, vp * k), C.c3, 2.5); v.arrow(V.add(M, V.mul(ep, vp * k)), [0, 0, vz * k], C.c2, 2.5); v.arrow(M, V.add(V.mul(ep, vp * k), [0, 0, vz * k]), C.c1, 3);
    v.dot(M, C.fg, 6); v.text(M, 'M₁', C.fg, 8, 14);
    MW.info(infoEl, 't = ' + fmt(t), [['ρ̇', '0 (ρ = R konstant)'], ['φ̇ = (2π/3) μ cos(μt)', fmt(vp)], ['ρφ̇ = R φ̇', fmt(vp)], ['ż = 2R/T', fmt(vz)]],
      'Bei t = 2: v = (2πμR/3) cos(2μ) e_φ + (2R/T) e_z (Lösung b). Typische Fehler: R vergessen, μ aus der Kettenregel vergessen, t zu früh einsetzen. (Pfeile mit 0,35 skaliert.)');
  });
  MW.slider(ctl, { label: 't', min: 0, max: 2, step: 0.01, value: t, onInput: x => { t = x; view.redraw(); } });
'''))

if __name__ == '__main__':
    files = build('kap2', W)
    print(len(files), 'Widgets:', ', '.join(files))
