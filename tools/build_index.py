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
    '3-1': '3.1 Satz der projizierten Geschwindigkeiten', '3-2': '3.2 Translation', '3-3': '3.3 Rotation',
    '3-4': '3.4 Kreiselung', '3-5': '3.5 Allgemeinste Bewegung: Kinemate, Zentralachse, Schraube', '3-6': '3.6 Ebene Bewegung: Momentanzentrum, Polbahnen, Fachwerke',
    '4-1': '4.1 Zum Kraftbegriff',
}

def title(p):
    return re.search(r'<title>(.*?)</title>', p.read_text(encoding='utf-8')).group(1)

parts = ['<h2>Werkzeuge</h2><p class="sub"><a href="werkzeuge/">Werkzeugkasten</a>: alle Werkzeuge auf einer Seite, mit Tabs (ein Notion-Embed für alles).</p><ul>'
         '<li><a href="werkzeuge/vektorrechner.html">Vektorrechner</a> (Addition, Skalar-, Kreuz- und Spatprodukt, Projektionen, Zentralachse)</li>'
         '<li><a href="werkzeuge/rechenblatt.html">3D-Plotter</a> (Vektoren, Punkte, Ebenen und Kurven im Raum, wie in GeoGebra)</li>'
         '<li><a href="werkzeuge/funktionsplotter.html">2D-Plotter</a> (Funktionen y = f(x), Parameterkurven, Vektoren und Vektorfelder in der Ebene, wie in GeoGebra)</li>'
         '<li><a href="werkzeuge/koordinaten-spielplatz.html">Koordinaten</a> (Punkte, Koordinatenlinien, Flächen, Bahnkurven)</li>'
         '<li><a href="mechskizze/index.html">Skizzen (MechSkizze-Editor)</a> (Skizzen als Text: Freikörperbilder, Lager, Kräfte, Geschwindigkeiten; <a href="mechskizze/index.html#skizzen">alle Skizzen</a>)</li></ul>']
for key, name in SECTIONS.items():
    files = sorted((ROOT / f'kap{key[0]}').glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="kap{key[0]}/{f.name}">{title(f)}</a></li>' for f in files)
    parts.append(f'<h2>{html.escape(name)}</h2><ul>{items}</ul>')
parts.append('<h2>3.5 / 3.6 Weitere Werkzeuge (Beispiele aus Buch und ZP1)</h2><ul>'
             '<li><a href="kinemate-3d.html">Kinemate, Invarianten und Zentralachse</a></li>'
             '<li><a href="momentanzentrum.html">Momentanzentrum einer ebenen Bewegung</a></li></ul>')

# Analysis I (Stammbach, Teil A)
ANA = {
    ('analysis-w1', '1-1'): 'Analysis I.1 Folgen und ihre Darstellung', ('analysis-w1', '1-2'): 'Analysis I.1 Nullfolgen und Konvergenz',
    ('analysis-w1', '1-3'): 'Analysis I.1 Monoton und beschränkt', ('analysis-w1', '1-4'): 'Analysis I.1 Rechenregeln',
    ('analysis-w1', '1-5'): 'Analysis I.1 Geometrische Folge und Reihe',
    ('analysis-w2', '2-1'): 'Analysis I.2 Funktionsbegriff', ('analysis-w2', '2-2'): 'Analysis I.2 Beispiele von Funktionen',
    ('analysis-w2', '2-3'): 'Analysis I.2 Elementare Funktionen', ('analysis-w2', '3-1'): 'Analysis I.3 Einseitige Grenzwerte',
    ('analysis-w2', '3-2'): 'Analysis I.3 sin x / x und Rechenregeln', ('analysis-w2', '3-3'): 'Analysis I.3 Stetigkeit',
    ('analysis-w3', '4-1'): 'Analysis I.4 Zwischenwertsatz', ('analysis-w3', '5-1'): 'Analysis I.5 Koordinatentransformationen',
    ('analysis-w3', '5-2'): 'Analysis I.5 Graphen skizzieren, Schwingungen', ('analysis-w3', '6-1'): 'Analysis I.6 Injektiv, surjektiv, bijektiv',
    ('analysis-w3', '6-2'): 'Analysis I.6 Umkehrfunktion', ('analysis-w3', '6-3'): 'Analysis I.6 Arcus-Funktionen',
    ('analysis-w3', '7-1'): 'Analysis I.7 Asymptoten',
}
parts.append('<h1 style="margin-top:32px">Analysis I</h1><p class="sub">Begleitmaterial zu U. Stammbach: Analysis I/II, Teil A (ETH Zürich).</p>')
for (folder, key), name in ANA.items():
    files = sorted((ROOT / folder).glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="{folder}/{f.name}">{title(f)}</a></li>' for f in files)
    parts.append(f'<h2>{html.escape(name)}</h2><ul>{items}</ul>')

# Chemistry (Brown, Chemistry: The Central Science)
CHEM = {('chemistry-w2', '10-4'): 'Chemistry 10.3–10.4 Gas laws and ideal gas law', ('chemistry-w2', '10-6'): 'Chemistry 10.6 Kinetic-molecular theory'}
parts.append('<h1 style="margin-top:32px">Chemistry</h1><p class="sub">Companion widgets for 151-0909-00L Chemistry (ETH Zürich), Brown et al.: Chemistry: The Central Science.</p>')
for (folder, key), name in CHEM.items():
    files = sorted((ROOT / folder).glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="{folder}/{f.name}">{title(f)}</a></li>' for f in files)
    parts.append(f'<h2>{html.escape(name)}</h2><ul>{items}</ul>')

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
