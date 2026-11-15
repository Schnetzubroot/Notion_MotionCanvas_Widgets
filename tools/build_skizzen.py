"""Schreibt skizzen/index.json (Liste aller MechSkizze-Dateien mit Titel) für Editor und Übersicht."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
items = []
for f in sorted((ROOT / 'skizzen').rglob('*.mech')):
    m = re.search(r'^\s*titel\s+"([^"]*)"', f.read_text(encoding='utf-8'), re.M)
    items.append({'s': f.relative_to(ROOT / 'skizzen').with_suffix('').as_posix(), 'titel': m.group(1) if m else f.stem})
(ROOT / 'skizzen' / 'index.json').write_text(json.dumps(items, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(items), 'Skizzen')
