# Interaktive Widgets zu Ingenieurmechanik 1

Begleitmaterial zu Sayir, Dual, Kaufmann, Mazza: *Ingenieurmechanik 1* (ETH Zürich).
Die Seiten werden über GitHub Pages ausgeliefert und in Notion eingebettet. Übersicht: `index.html`.

| Ordner | Inhalt |
| --- | --- |
| `kap1/` | Woche 1, Kapitel 1: Koordinaten und vektorielle Darstellung (25 Widgets) |
| `kap2/` | Woche 2, Kapitel 2: Geschwindigkeit (15 Widgets) |
| `kap3/` | Woche 3, Kapitel 3.1–3.3: Satz der projizierten Geschwindigkeiten, Translation, Rotation (9 Widgets) |
| `kap3/` (Woche 4) | Kapitel 3.4–3.5: Kreiselung, Kinemate und Invarianten, Schraubung (`3-4-*`, `3-5-*`, 3 Widgets) |
| `kap3/` (Woche 5) | Kapitel 3.6: Satz vom Momentanzentrum, Polbahnen, Planetengetriebe, ebenes Fachwerk (`3-6-*`, 4 Widgets) |
| `kap4/` | Woche 5, Kapitel 4.1: Kräfte als punktgebundene Vektoren (1 Widget) |
| `kinemate-3d.html`, `momentanzentrum.html` | Kapitel 3.5 und 3.6: Zentralachse im 3D-Raum, Konstruktion des Momentanzentrums (freie Werkzeuge mit Beispielen aus ZP1) |
| `mechskizze/` | MechSkizze: Editor (`index.html`), Einzelansicht zum Einbetten (`ansicht.html?s=kap3/3-1-spg`), Sprachreferenz (`REFERENZ.md`) |
| `skizzen/` | MechSkizze-Dateien (`.mech`), nach Kapitel; `index.json` wird von `tools/build_skizzen.py` erzeugt |
| `analysis-w1/` | Analysis I, Woche 1, Kapitel I.1: Folgen, Konvergenz (Stammbach, Teil A) |
| `analysis-w2/` | Analysis I, Woche 2, Kapitel I.2–3: Funktionen, Grenzwerte, Stetigkeit |
| `analysis-w3/` | Analysis I, Woche 3, Kapitel I.4–7: Zwischenwertsatz, Koordinatentransformationen, Umkehrfunktion, Asymptoten |
| `analysis-w4/` | Analysis I, Woche 4, Kapitel II.1–2: Differentialquotient, Kettenregel, Ableitung der Umkehrfunktion, lineare Ersatzfunktion |
| `analysis-w5/` | Analysis I, Woche 5, Kapitel II.2–4 und Anhang A: Fehlerrechnung, Rolle, Mittelwertsatz, Bernoulli-Hôpital, Extremalaufgaben, komplexe Zahlen |
| `chemistry-w2/` | Chemistry (151-0909-00L), Woche 2, Brown Kap. 10: Gasgesetze, Geschwindigkeitsverteilung |
| `chemistry-w5/` | Chemistry (151-0909-00L), Woche 5, Brown Kap. 19: ΔG = ΔH − TΔS in Abhängigkeit von T |
| `chemistry-w6/` | Chemistry (151-0909-00L), Woche 6, Brown Kap. 6: Wasserstoff-Übergänge und Spektrallinien |
| `chemistry-w7/` | Chemistry (151-0909-00L), Woche 7, Brown Kap. 9: VSEPR-Geometrien in 3D |
| `werkzeuge/` | Werkzeugkasten `werkzeuge/` (alle Werkzeuge in Tabs: `#2d`, `#3d`, `#vektoren`, `#koordinaten`, `#skizzen`); Vektorrechner, 3D-Plotter (`rechenblatt.html`), 2D-Plotter (`funktionsplotter.html`, Beispiele per `?beispiel=2`) und Koordinaten (`koordinaten-spielplatz.html`) (freie Werkzeuge, Szenario per `?szenario=zp25` wählbar) |
| `lib/` | gemeinsame Bibliothek (`core.js`, `core.css`) und MechSkizze-Renderer (`mechskizze.js`, läuft auch in Node) |
| `tools/` | Build-Skripte: `python3 tools/build_kap1.py`, `build_kap2.py`, `build_kap3.py`, `build_kap3_w4.py`, `build_kap3_w5.py`, `build_kap4.py`, `build_skizzen.py`, `build_analysis_w1.py`, `build_analysis_w2.py`, `build_analysis_w3.py`, `build_analysis_w4.py`, `build_analysis_w5.py`, `build_chemistry_w2.py`, `build_chemistry_w5.py`, `build_chemistry_w6_w7.py`, `build_index.py` |

Jedes Widget zeigt genau eine Situation. Die HTML-Dateien in `kap1/`, `kap2/`, `kap3/`, `kap4/`, `analysis-w1/`, `analysis-w2/`, `analysis-w3/`, `analysis-w4/`, `analysis-w5/` `chemistry-w2/`, `chemistry-w5/`, `chemistry-w6/` und `chemistry-w7/` werden aus den Build-Skripten erzeugt.

## MechSkizze

MechSkizze ist eine Textsprache für Mechanik-Skizzen (Sprache: `mechskizze/REFERENZ.md`). Eine Skizze ist eine `.mech`-Datei in `skizzen/`.
In Notion bettet man sie so ein: `https://schnetzubroot.github.io/Notion_MotionCanvas_Widgets/mechskizze/ansicht.html?s=kap3/3-1-spg`.
Die Ansicht zeigt den Text und einen Link in den Editor. Neue Skizze: Datei anlegen, dann `python3 tools/build_skizzen.py`.
Als Handskizze (Gel-Marker-Look, farbig): `…/ansicht.html?s=kap3/3-1-spg&stil=hand` oder `stil hand` in der Skizze; Normschrift nach ISO 3098: `&schrift=norm` oder `schrift norm`. Die Schriften liegen in `lib/fonts/` (Zen Kurenaido, OFL; osifont, LGPL 3 mit Font-Ausnahme).
Beschriftungen verschieben: im Editor die Beschriftung ziehen. Der Editor schreibt dafür `verschiebe "F" um (dx,dy)` in den Text (Versatz zum Ankerpunkt in Pixeln, weit weg mit Hinweislinie); Doppelklick setzt sie zurück.

## 2D-Plotter

`werkzeuge/funktionsplotter.html` (2D-Plotter) zeichnet Funktionen einer Variablen: eine Zeile pro Objekt, z. B. `f(x) = a x^2 + b`, `a = regler(-3, 3, 1)`, `f'(x)`, `P = (1, f(1))`, `x = 2`, `f(x) = sqrt(x), 0 <= x <= 4`.
Vektorfunktionen: Parameterkurven `r(t) = (cos(t), sin(t)), 0 <= t <= 2pi` (mit `r(t0)` als Punkt und `r'(t0)` als Tangentenvektor), Vektorfelder `F(x, y) = (-y, x)` und Pfeile `pfeil(P, v)`.
Achsen einzeln skalieren: Achse ziehen (Maus oder Finger), Mausrad über einer Achse, Shift/Alt + Mausrad, Knöpfe x −/+ und y −/+; mit „gleich skaliert“ aus streckt ein Zwei-Finger-Zoom jede Achse getrennt.
Hell/Dunkel: Knopf „☾ Dunkel“ / „☀ Hell“ unter dem Bild; die Wahl wird gespeichert und im Teilen-Link mitgegeben (oder per `?theme=dark` / `?theme=light`). `lib/core.css` kennt dafür `<html data-theme="dark|light">`.
In Notion einbetten: Blatt bauen, „Link mit diesem Blatt kopieren“ klicken und den Link mit `/embed` einfügen. Der Link enthält Eingabe, Reglerstände, Farben und Ausschnitt.

## Werkzeugkasten

`werkzeuge/index.html` fasst 2D-Plotter, 3D-Plotter, Vektorrechner, Koordinaten und Skizzen (MechSkizze) in einer Seite mit Tabs zusammen. In Notion genügt ein Embed: `https://schnetzubroot.github.io/Notion_MotionCanvas_Widgets/werkzeuge/`.
Ein Tab wird beim ersten Öffnen geladen und behält danach seinen Inhalt; der zuletzt benutzte Tab wird gemerkt. `#2d`, `#3d`, `#vektoren`, `#koordinaten`, `#skizzen` öffnen direkt einen Tab (alte Namen wie `#plotter` gehen auch), `?2d=%23r%3D…` reicht einen geteilten Plotter-Link durch.
Die beiden Plotter werden gleich bedient: gleiche Eingabesprache (`f(x) = …`, `r(t) = (…), 0 ≤ t ≤ 2pi`, `f'(x)`, `regler(…)` mit ▶, `pfeil(P, v)`, Grossbuchstaben = Punkte, Kleinbuchstaben = Vektoren), gleiche Symbolleiste, Zoom-Knöpfe und Teilen-Link.
Hell/Dunkel gilt für alle Werkzeuge gemeinsam (`lib/core.js`, `MW.theme`, gespeichert als `mw-theme`). Jedes Werkzeug hat einen Knopf „Bild kopieren“ (`MW.snap`): er legt die aktuelle Ansicht als PNG in die Zwischenablage; wo das Einbetten die Zwischenablage sperrt, wird das Bild stattdessen heruntergeladen. Die einzelnen Seiten bleiben unter ihren alten Adressen erreichbar.
