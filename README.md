# Interaktive Widgets zu Ingenieurmechanik 1

Begleitmaterial zu Sayir, Dual, Kaufmann, Mazza: *Ingenieurmechanik 1* (ETH Zürich).
Die Seiten werden über GitHub Pages ausgeliefert und in Notion eingebettet. Übersicht: `index.html`.

| Ordner | Inhalt |
| --- | --- |
| `kap1/` | Woche 1, Kapitel 1: Koordinaten und vektorielle Darstellung (25 Widgets) |
| `kap2/` | Woche 2, Kapitel 2: Geschwindigkeit (15 Widgets) |
| `kinemate-3d.html`, `momentanzentrum.html` | Kapitel 3.5 und 3.6 |
| `analysis-w1/` | Analysis I, Woche 1, Kapitel I.1: Folgen, Konvergenz (Stammbach, Teil A) |
| `analysis-w2/` | Analysis I, Woche 2, Kapitel I.2–3: Funktionen, Grenzwerte, Stetigkeit |
| `werkzeuge/` | Vektorrechner, Rechenblatt (eigene Rechnungen) und Koordinaten-Spielplatz (freie Werkzeuge, Szenario per `?szenario=zp25` wählbar) |
| `lib/` | gemeinsame Bibliothek (`core.js`, `core.css`) |
| `tools/` | Build-Skripte: `python3 tools/build_kap1.py`, `build_kap2.py`, `build_analysis_w1.py`, `build_analysis_w2.py`, `build_index.py` |

Jedes Widget zeigt genau eine Situation. Die HTML-Dateien in `kap1/`, `kap2/`, `analysis-w1/` und `analysis-w2/` werden aus den Build-Skripten erzeugt.
