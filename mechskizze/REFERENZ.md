# MechSkizze – Sprachreferenz

MechSkizze ist eine Textsprache für Mechanik-Skizzen (Körper, Lager, Kräfte, Momente, Fachwerke, 3D-Körper, Diagramme). In allen Kursdateien stehen die Figuren als Codeblöcke mit der Sprache `mech`. Der Editor zeichnet einen Block sofort: Text einfügen → Skizze erscheint.

**Für Claude:** Figuren aus diesen Blöcken lesen (Geometrie, Lager, Lasten, Masse). Eigene Skizzen in Antworten (Freikörperbilder, Lösungsskizzen) ebenfalls als `mech`-Codeblock schreiben, damit der Nutzer sie im Editor ansehen kann. Nur die unten aufgeführten Befehle verwenden.

## Grundregeln
- Eine Anweisung pro Zeile, mehrere mit `;` trennen. `#` beginnt einen Kommentar.
- Zahlen sind Ausdrücke mit Parametern: `2a`, `a/2`, `√3R`, `l*sqrt(3)/2`, `0.6a`. `sin/cos/tan` rechnen in Grad. Nicht gesetzte Parameter gelten als 1.
- Winkel in Grad (`30°` oder `30`), mathematisch positiv (gegen den Uhrzeigersinn, 0° = +x).
- Texte in `"…"`: `_` Index (`F_1`, `q_{max}`), `^` Exponent, `~` vor einem Zeichen = Vektor (unterstrichen, z. B. `~e_x`, `~F`; mehrere Zeichen: `~{AB}`). `√` gilt für die folgende Zahl bzw. den folgenden Buchstaben (`√3R` = √3·R); längere Radikanden in Klammern: `√(a^2+b^2)` (werden ohne Klammern unter den Wurzelstrich gesetzt).
- Punktnamen, die mit `_` beginnen, werden nicht beschriftet.

## Struktur
| Befehl | Bedeutung |
|---|---|
| `titel "…"` | Titel (wird nicht gezeichnet) |
| `param a=1 H=0.55` | Zahlenwerte nur fürs Zeichnen; Beschriftungen bleiben symbolisch |
| `massstab 0.5` | Skizze kleiner/grösser zeichnen (Symbole behalten ihre Grösse) |
| `system s = gedreht 30° [ursprung P]` | gedrehtes Koordinatensystem; mit `in s` in jeder Anweisung verwenden (z. B. `punkte in s: A(0,0) B(2a,0)`) |
| `teilbild "…" [2d]` | neues Teilbild daneben; `2d` = ebenes Teilbild innerhalb einer 3D-Skizze |
| `untereinander` / `nebeneinander` | Anordnung der Teilbilder |
| `ohne namen [A B]` | keine (bzw. diese) Punktnamen anzeigen |
| `beschrifte E "E ≡ (0,2R,√3R)" lage r` | Beschriftung eines Punktes ändern/platzieren (lage: r l o u or ol ur ul) |
| `stil hand [einfarbig]` | Handskizze: wie von Hand mit Gel-Marker gezeichnet (siehe unten); `stil sauber` = Standard |

## Punkte und Richtungen
| Form | Bedeutung |
|---|---|
| `punkte A(0,0) B(2a,0) _H(a,a)` | Punkte definieren (2D: (x,y); 3D: (x,y,z)) |
| `punkte W=B+(-a,a)` | Punkt relativ zu einem anderen |
| `knoten A(0,0) …` | wie punkte, als gefüllter Knotenpunkt gezeichnet |
| `A`, `(x,y)`, `A+(dx,dy)`, `mitte(A,B)`, `mitte(Körper)`, `teil(A,B,0.3)` | Punktausdrücke |
| `30°`, `+x`, `-y`, `+z`, `(dx,dy[,dz])`, `A->B`, `P` | Richtungen (Winkel, Achse, Vektor, von A nach B, zum Punkt P) |

## Körper und Geometrie
| Befehl | Bedeutung |
|---|---|
| `körper Platte = polygon A B C D "Beschreibung"` | starrer Körper (dicke Kontur); Text = Bedeutung, wird nicht gezeichnet |
| `körper Scheibe = kreis M radius r` | Kreisscheibe |
| `stab A-B C-D` / `balken A B` | Stab (dick) / Balken (sehr dick); Punkte auch als Ausdruck: `stab A-(1,0)` |
| `fachwerk A-B B-C … [nummeriert]` | Fachwerkstäbe mit Knoten; `nummeriert` = Stabnummern 1, 2, … |
| `linie A B C [gestrichelt\|punktiert\|strichpunkt\|dick\|dünn\|grau]` | freie Linie |
| `fläche A B C D [grau\|hellgrau\|schraffiert]` | Fläche (auch 3D-Platte) |
| `bogen M radius r von 0 bis 90 [dick]` | Kreisbogen |
| `kurve A B C D [geschlossen] [richtungspfeile] [grau]` | glatte Kurve durch Punkte (Bahnkurve, Körperumriss) |
| `kurve t von 0 bis 360: (cos(t), sin(t), t/360)` | Parameterkurve |
| `achse "ζ" P richtung (1,0,0) länge 3` | Strichpunkt-Achse |
| `marke A B` / `schwerpunkt S` / `gelenk C` | Punktmarke / Schwerpunktsymbol / Gelenk (Kreis) |
| `bruch P richtung 0°` | Bruchkante (Stab geht weiter) |
| `rechtwinklig P zwischen A und B` | Zeichen für rechten Winkel |

## Lager und Umgebung
| Befehl | Bedeutung |
|---|---|
| `festlager A [an decke\|an wand links\|an wand rechts\|richtung 30°] [grau]` | Gelenklager (Standard: Boden unten); Richtung = vom Boden zum Körper |
| `loslager E [richtung …]` | Rollenlager |
| `einspannung A richtung 0°` | Einspannung |
| `kugelgelenk A` / `schiebehülse A richtung 0°` | Kugelgelenk (3D) / Hülse |
| `querlager A [lang]` | kurzes bzw. langes Querlager |
| `boden P Q [schraffur unten]`, `ebene P -> Q schraffur unten` | Boden/Ebene mit Schraffur |
| `wand P richtung 90° länge L [mittig] [grau] schraffur links` | Wand/Decke |
| `seil A B`, `seil A richtung 135° länge L` | Seil/Faden |
| `feder A B`, `rolle M radius r` | Feder, Rolle |

## Lasten, Kinematik, Masse
| Befehl | Bedeutung |
|---|---|
| `kraft F bei C richtung +x [zu] [dick] [länge L] [lage r]` | Kraftpfeil; `zu` = Spitze am Punkt; Name = Beschriftung (`kraft "2F" bei …` für freie Beschriftung) |
| `moment M bei A [uhrzeiger]` | Moment als Drehpfeil (Standard: Gegenuhrzeigersinn) |
| `moment M bei A achse (0,0,1)` | Momentvektor (Doppelpfeil, 3D) |
| `drehpfeil P achse +z "ω"` | kleiner Drehpfeil um eine Achse (z. B. ω an einer Achse) |
| `last von A nach B q (0,1) seite oben höhe 0.5 "q_0"` | Streckenlast; `q (…)` mit 2 Werten linear, mit mehr Werten beliebiger Verlauf |
| `last … richtung -65° [nachaussen]` | schräge Lastpfeile; `nachaussen` = Pfeile zeigen von der Linie weg |
| `vektor v_A bei A richtung (1,0,2) länge L` | Geschwindigkeit, ω, Basisvektor usw. |
| `pfeil von P nach Q "y" [doppelt] [grau]` | freier Pfeil (z. B. Koordinatenachsen) |
| `aus O "z"` / `ein O "z"` | Vektor aus der Ebene (⊙) / in die Ebene (⊗) |
| `koordinaten P` / `basis P länge L [namen ~e_1 ~e_2 ~e_3]` | Achsenkreuz / Basisvektoren |
| `mass A-B "2h" [strich] [seite unten] [versatz d]` | Bemassung mit Pfeilen oder Endstrichen |
| `kante A-B "a" [aussen\|innen\|links\|rechts\|oben\|unten]` | Seitenbeschriftung |
| `winkel B zwischen A und W "45°" [radius 30]` | Winkelbogen; auch `horizontal`, `vertikal`, Winkelwerte, `+z`; in 3D in der Ebene der beiden Richtungen |
| `text P "G_2" [lage r] [kasten] [grau] [normal]` | Text |
| `diagramm "Q" basis (0,-2) länge 11 skala 0.25 punkte (0,0.67) (6,0.67) (6,-2.33) …` | Schnittgrössen-Diagramm (positiv nach unten, Sprünge durch gleiche x-Werte) |

## Handskizze (`stil hand`)
Die Skizze sieht aus wie von Hand mit Gel-Marker gezeichnet: leicht gewellte, ungleich dicke Linien, Handschrift und Farben nach Bedeutung. Gleiche Skizze = gleiches Bild (die Wellen hängen nur vom Element ab). Ohne `stil hand` bleibt alles wie bisher.

| Farbe | Elemente |
|---|---|
| Rot | Kräfte (`kraft`) und Streckenlasten (`last`) |
| Violett | Momente (`moment`, auch als Momentvektor) |
| Blau | Kinematik: `vektor`, `geschwindigkeit`, `drehpfeil` |
| Grün | Hilfselemente: `mass`, `kante`, `winkel`, `rechtwinklig`, `pfeil`, `koordinaten`, `basis`, gestrichelte Linien, Achsen |
| Dunkelblau | Körper, Stäbe, Linien, Texte, Punktnamen |
| Graublau | Lager, Boden, Wände |

| Befehl / Zusatz | Bedeutung |
|---|---|
| `stil hand` | Handskizze für diese Skizze |
| `stil hand einfarbig` | Handskizze ohne Farben (alles dunkelblau) |
| `… farbe rot` | Farbe eines Elements selbst wählen, an jede Anweisung anhängbar (`kraft A_x bei A richtung -x farbe orange`); gilt auch im normalen Stil. Farben: rot, blau, grün, violett, orange, braun, türkis, pink, grau, schwarz oder `#rrggbb` |

Ohne den Text zu ändern: im Editor das Häkchen **Handskizze** setzen (dazu optional **einfarbig**), in der Einzelansicht `ansicht.html?s=kap3/3-1-spg&stil=hand` (einfarbig: `&farben=aus`). So lässt sich jede Skizze in Notion als Handskizze einbetten.

## 3D
| Befehl | Bedeutung |
|---|---|
| `3d` | 3D-Modus, Standardansicht: z nach oben, y nach rechts, x nach vorne links |
| `3d azimut -49 elevation 35` | andere Blickrichtung (orthogonale Axonometrie) |
| `3d achsen (1,0) (0.55,0.42) (0,1)` | Bildrichtungen der x-, y-, z-Achse frei festlegen (wie in der Originalskizze) |
| `3d schräg` | Kavalierprojektion |
| `quader von P bis Q` | Quader, verdeckte Kanten gestrichelt |
| `kegel spitze A basis D radius R` | Kreiskegel |
| `zylinder basis M achse +z radius r höhe h` | Zylinder |
| `kugel M radius r [hellgrau]` | Kugel |
| `körper K = kreis M radius r normale (0,0,1)` | Kreis(scheibe) im Raum |

## Beispiel
```mech
titel "Serie 8, Aufgabe 3 – Quadratplatte an Faden"
param a=1
punkte A(0,0)  B(a,0)  C(a,-a)  D(0,-a)  _W=B+(-0.6a,0.6a)
körper Platte = polygon A B C D "homogen, Gewicht G"
festlager A an decke grau
seil B _W
wand _W richtung 90° länge 0.3a mittig grau schraffur links
winkel B zwischen A und _W "45°" radius 26
kraft G bei mitte(Platte)+(0,0.2a) richtung -y dick länge 0.95a
kraft F bei C richtung +x dick länge 0.55a
kante A-B "a" innen  A-D "a" innen
```
