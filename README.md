# Interaktive Widgets zu Ingenieurmechanik 1

Begleitmaterial zu Sayir, Dual, Kaufmann, Mazza: *Ingenieurmechanik 1* (ETH Zürich).
Die Seiten werden über GitHub Pages ausgeliefert und in Notion eingebettet. Übersicht: `index.html`.

| Ordner | Inhalt |
| --- | --- |
| `kap1/` | Woche 1, Kapitel 1: Koordinaten und vektorielle Darstellung (25 Widgets) |
| `kap2/` | Woche 2, Kapitel 2: Geschwindigkeit (15 Widgets) |
| `kap3/` | Woche 3, Kapitel 3.1–3.3: Satz der projizierten Geschwindigkeiten, Translation, Rotation (9 Widgets) |
| `kinemate-3d.html`, `momentanzentrum.html` | Kapitel 3.5 und 3.6 |
| `mechskizze/` | MechSkizze: Editor (`index.html`), Einzelansicht zum Einbetten (`ansicht.html?s=kap3/3-1-spg`), Sprachreferenz (`REFERENZ.md`) |
| `skizzen/` | MechSkizze-Dateien (`.mech`), nach Kapitel; `index.json` wird von `tools/build_skizzen.py` erzeugt |
| `analysis-w1/` | Analysis I, Woche 1, Kapitel I.1: Folgen, Konvergenz (Stammbach, Teil A) |
| `analysis-w2/` | Analysis I, Woche 2, Kapitel I.2–3: Funktionen, Grenzwerte, Stetigkeit |
| `analysis-w3/` | Analysis I, Woche 3, Kapitel I.4–7: Zwischenwertsatz, Koordinatentransformationen, Umkehrfunktion, Asymptoten |
| `werkzeuge/` | Vektorrechner, Rechenblatt (eigene Rechnungen) und Koordinaten-Spielplatz (freie Werkzeuge, Szenario per `?szenario=zp25` wählbar) |
| `lib/` | gemeinsame Bibliothek (`core.js`, `core.css`) und MechSkizze-Renderer (`mechskizze.js`, läuft auch in Node) |
| `tools/` | Build-Skripte: `python3 tools/build_kap1.py`, `build_kap2.py`, `build_kap3.py`, `build_skizzen.py`, `build_analysis_w1.py`, `build_analysis_w2.py`, `build_analysis_w3.py`, `build_index.py` |

Jedes Widget zeigt genau eine Situation. Die HTML-Dateien in `kap1/`, `kap2/`, `kap3/`, `analysis-w1/`, `analysis-w2/` und `analysis-w3/` werden aus den Build-Skripten erzeugt.

## MechSkizze

MechSkizze ist eine Textsprache für Mechanik-Skizzen (Sprache: `mechskizze/REFERENZ.md`). Eine Skizze ist eine `.mech`-Datei in `skizzen/`.
In Notion bettet man sie so ein: `https://schnetzubroot.github.io/Notion_MotionCanvas_Widgets/mechskizze/ansicht.html?s=kap3/3-1-spg`.
Die Ansicht zeigt den Text und einen Link in den Editor. Neue Skizze: Datei anlegen, dann `python3 tools/build_skizzen.py`.
