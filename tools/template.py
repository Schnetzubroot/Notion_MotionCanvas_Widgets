"""Erzeugt die Widget-HTML-Dateien aus kurzen Definitionen.

Jede Definition: dict(file, title, sub, hint, legend=[(css-var, text)], tall=False, js="...").
Im JS stehen zur Verfügung: MW, V, fmt, fv, ctl (Steuerleiste), infoEl, cv (Canvas).
"""
import html
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

TPL = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{plain}</title>
<link rel="stylesheet" href="../lib/core.css">
</head>
<body>
<div class="wrap">
  <h1>{title}</h1>
  <p class="sub">{sub}</p>
  <div class="stage">
    <canvas id="cv"{cls}></canvas>{legend}
    <div class="hint">{hint}</div>
  </div>
  <div class="ctl" id="ctl"></div>
  <div class="info" id="info"></div>
</div>
<script src="../lib/core.js"></script>
<script>
(() => {{
  const {{ V, fmt, fv }} = MW;
  const ctl = document.getElementById('ctl'), infoEl = document.getElementById('info'), cv = document.getElementById('cv');
{js}
}})();
</script>
</body>
</html>
"""


def build(folder, widgets):
    out = ROOT / folder
    out.mkdir(exist_ok=True)
    for w in widgets:
        legend = ''
        if w.get('legend'):
            items = ''.join(f'<div><span class="sw" style="background:var({c})"></span>{t}</div>' for c, t in w['legend'])
            legend = f'\n    <div class="legend">{items}</div>'
        page = TPL.format(title=w['title'], plain=html.escape(re.sub('<[^>]+>', '', w['title'])), sub=w['sub'], hint=w.get('hint', ''),
                          cls=' class="tall"' if w.get('tall') else '', legend=legend, js=w['js'])
        (out / w['file']).write_text(page, encoding='utf-8')
    return [w['file'] for w in widgets]
