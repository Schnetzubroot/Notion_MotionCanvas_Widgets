"""Erzeugt index.html mit allen Widgets, gruppiert nach Kapitel."""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = {
    '1-1': '1.1 Bezugskörper und Koordinaten', '1-2': '1.2 Kartesische Koordinaten', '1-3': '1.3 Zylindrische Koordinaten',
    '1-4': '1.4 Sphärische Koordinaten', '1-5': '1.5 Vektorielle Darstellung der Bewegung',
    '2-1': '2.1 Vektorfunktion einer skalaren Variable', '2-2': '2.2 Schnelligkeit und Geschwindigkeit',
    '2-3': '2.3 Ortsvektor und Geschwindigkeit', '2-4': '2.4 Komponenten der Geschwindigkeit',
}

def title(p):
    return re.search(r'<title>(.*?)</title>', p.read_text(encoding='utf-8')).group(1)

parts = ['<h2>Werkzeuge</h2><ul>'
         '<li><a href="werkzeuge/vektorrechner.html">Vektorrechner</a> (Addition, Skalar-, Kreuz- und Spatprodukt, Projektionen, Zentralachse)</li>'
         '<li><a href="werkzeuge/rechenblatt.html">Rechenblatt</a> (eigene Rechnungen wie in GeoGebra, mit 3D-Ansicht)</li>'
         '<li><a href="werkzeuge/koordinaten-spielplatz.html">Koordinaten-Spielplatz</a> (Punkte, Koordinatenlinien, Flächen, Bahnkurven)</li></ul>']
for key, name in SECTIONS.items():
    files = sorted((ROOT / f'kap{key[0]}').glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="kap{key[0]}/{f.name}">{title(f)}</a></li>' for f in files)
    parts.append(f'<h2>{html.escape(name)}</h2><ul>{items}</ul>')
parts.append('<h2>3.5 / 3.6 Allgemeinste und ebene Bewegung</h2><ul>'
             '<li><a href="kinemate-3d.html">Kinemate, Invarianten und Zentralachse</a></li>'
             '<li><a href="momentanzentrum.html">Momentanzentrum einer ebenen Bewegung</a></li></ul>')

page = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mechanik-Widgets</title>
<link rel="stylesheet" href="lib/core.css">
<style>
  main {{ max-width: 760px; margin: 0 auto; padding: 20px 16px; }}
  h1 {{ font-size: 22px; }} h2 {{ font-size: 16px; margin: 22px 0 6px; }}
  ul {{ margin: 0; padding-left: 18px; }} li {{ margin: 3px 0; }}
  a {{ color: var(--c2); text-decoration: none; }} a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<main>
  <h1>Interaktive Widgets zu Ingenieurmechanik 1</h1>
  <p class="sub">Begleitmaterial zu Sayir, Dual, Kaufmann, Mazza: Ingenieurmechanik 1 (ETH Zürich). Ein Widget pro Situation.</p>
  {''.join(parts)}
</main>
</body>
</html>
"""
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print('index.html geschrieben')
