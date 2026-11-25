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
    '4-1': '4.1 Zum Kraftbegriff', '4-3': '4.3 Reaktionsprinzip und Freischneiden', '4-4': '4.4 Kraftdichten',
    '5-1': '5.1 Leistung einer Einzelkraft und eines Moments', '5-2': '5.2 Gesamtleistung am starren Körper',
    '6-1': '6.1 Statische Äquivalenz', '6-2': '6.2 Moment bezüglich Punkt und Achse', '6-3': '6.3 Kräftepaar, parallele Kräfte', '6-4': '6.4 Gleichgewicht',
    '6-5': '6.5 Reduktion einer Kräftegruppe', '7-2': '7.1–7.2 Kräftemittelpunkt, verteilte Kräfte', '7-3': '7.3 Schwerpunkt',
    '8-2': '8.2–8.4 Prinzip der virtuellen Leistungen, Hauptsatz der Statik', '9-1': '9.1 Standfestigkeit', '9-4': '9.3–9.4 Lagerkräfte, Dreigelenkbogen',
    '10-1': '10.1–10.2 Statik der Systeme', '10-3': '10.3 Statisch unbestimmte Systeme',
    '11-1': '11.1 Ideale Fachwerke, Pendelstützen', '11-2': '11.2 Knotengleichgewicht, statische Bestimmtheit', '11-3': '11.3 Dreikräfteschnitt',
    '11-4': '11.4 Prinzip der virtuellen Leistungen am Fachwerk', '11-5': '11.5 Räumliche Fachwerke',
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
    kap = 'kap' + key.split('-')[0]
    files = sorted((ROOT / kap).glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="{kap}/{f.name}">{title(f)}</a></li>' for f in files)
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
    ('analysis-w4', '1-1'): 'Analysis II.1 Differenzen- und Differentialquotient', ('analysis-w4', '1-2'): 'Analysis II.1 Ableitungsfunktion und Rechenregeln',
    ('analysis-w4', '1-3'): 'Analysis II.1 Kettenregel', ('analysis-w4', '1-4'): 'Analysis II.1 Ableitung der Umkehrfunktion',
    ('analysis-w4', '2-1'): 'Analysis II.2 Lineare Ersatzfunktion',
    ('analysis-w5', '2-2'): 'Analysis II.2 Differentiale und Fehlerrechnung', ('analysis-w5', '3-1'): 'Analysis II.3 Lokale Extrema, Satz von Rolle',
    ('analysis-w5', '3-2'): 'Analysis II.3 Mittelwertsatz', ('analysis-w5', '3-3'): 'Analysis II.3 Regel von Bernoulli-Hôpital',
    ('analysis-w5', '4-1'): 'Analysis II.4 Kandidaten für Extremalstellen', ('analysis-w5', '4-2'): 'Analysis II.4 Abstand Punkt–Strecke',
    ('analysis-w5', '4-3'): 'Analysis II.4 Kreuzförmiger Querschnitt', ('analysis-w5', 'A-1'): 'Analysis Anhang A: Komplexe Zahlen',
    ('analysis-w6', 'A-2'): 'Analysis Anhang A: Polarform und Euler-Formel', ('analysis-w6', 'A-3'): 'Analysis Anhang A: Multiplikation in Polarform',
    ('analysis-w6', 'A-4'): 'Analysis Anhang A: Wurzeln komplexer Zahlen',
    ('analysis-w7', 'A-5'): 'Analysis Anhang A: Polynome und Nullstellen', ('analysis-w7', 'A-6'): 'Analysis Anhang A: Lineare DGL mit Ansatz e^(αx)',
    ('analysis-w7', '5-1'): 'Analysis II.5 Exponentialfunktion und e', ('analysis-w7', '5-2'): 'Analysis II.5 Logarithmus und Basis a',
    ('analysis-w7', '5-3'): 'Analysis II.5 Hyperbolische Funktionen', ('analysis-w7', '6-1'): 'Analysis II.6 Grössenordnungen',
    ('analysis-w11', '1-1'): 'Analysis VIII.1 Konvergenz und Divergenz von Reihen', ('analysis-w11', '2-1'): 'Analysis VIII.2 Potenzreihen',
    ('analysis-w11', '3-1'): 'Analysis VIII.3 Taylorpolynom', ('analysis-w11', '4-1'): 'Analysis VIII.4 Taylorreihe und Binomialreihe',
    ('analysis-w11', '4-2'): 'Analysis VIII.4 Koeffizientenvergleich', ('analysis-w11', '5-1'): 'Analysis VIII.5 Anwendungen: nicht elementare Integrale',
    ('analysis-w11', '5-2'): 'Analysis VIII.5 Anwendungen: Potenzreihenansatz bei DGL',
}
parts.append('<h1 style="margin-top:32px">Analysis I</h1><p class="sub">Begleitmaterial zu U. Stammbach: Analysis I/II, Teil A und C (ETH Zürich).</p>')
for (folder, key), name in ANA.items():
    files = sorted((ROOT / folder).glob(f'{key}-*.html'))
    items = ''.join(f'<li><a href="{folder}/{f.name}">{title(f)}</a></li>' for f in files)
    parts.append(f'<h2>{html.escape(name)}</h2><ul>{items}</ul>')

# Chemistry (Brown, Chemistry: The Central Science)
CHEM = {('chemistry-w2', '10-4'): 'Chemistry 10.3–10.4 Gas laws and ideal gas law', ('chemistry-w2', '10-6'): 'Chemistry 10.6 Kinetic-molecular theory', ('chemistry-w5', '19-6'): 'Chemistry 19.5–19.6 Gibbs free energy and temperature', ('chemistry-w6', '6-3'): 'Chemistry 6.1–6.3 Hydrogen spectrum and Bohr model', ('chemistry-w7', '9-2'): 'Chemistry 9.1–9.2 Molecular shapes (VSEPR)'}
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
