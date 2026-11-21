# Reel: Buchenstammholz-Anlieferung (Entwurf v1)

**Datei:** `natura_reel.mp4` · 1080×1920 (9:16) · 30 fps · 30,0 s · H.264/AAC

## Wichtig: Das ist eine Foto-Version
Grundlage sind 5 Standfotos, kein Video. Bewegung entsteht durch langsame Zooms und
Schwenks (Ken-Burns-Effekt). Es gibt deshalb **keine echte Vorbeifahrt, kein echtes
Abladen und keinen Originalton** (Motor, Kran, Aufsetzen der Stämme). Die Musik ist eine
selbst erzeugte, rechtefreie Instrumentalspur (`music.py`).

## Schnittplan
| Zeit | Foto | Inhalt | Text |
|---|---|---|---|
| 0,0–1,2 | 3 | Nahaufnahme Stirnfläche + Rinde, Push-in | „Buchenstammholz auf dem Weg zum Kunden" |
| 1,2–3,0 | 4 | Lkw mit Nachläufer in ganzer Länge, Schwenk | (Text läuft bis 3,0 s) |
| 3,0–6,6 | 2 | MAN von vorn, Kran, Ladung | – |
| 6,6–8,4 | 2 | Detail Natura-Schriftzug an der Tür | – |
| 8,4–10,2 | 3 | Detail Ladung, Gurte, Rungen | – |
| 10,2–13,8 | 5 | Heckansicht bei der Einfahrt | – |
| 13,8–19,2 | 1 | Kran im Einsatz (längste Einstellung) | – |
| 19,2–22,8 | 1 | Detail Kranführer + Greifer | – |
| 22,8–27,0 | 1 | Ruhiges Bild, Stämme im Vordergrund | „Danke für die langjährige Zusammenarbeit." |
| 27,0–30,0 | – | Endkarte NATURA Waldservice GmbH | natura-waldservice.de |

Schnitte liegen auf dem Takt (100 BPM, 0,6 s pro Schlag).

## Offene Punkte vor Veröffentlichung
- **Logo:** Die Endkarte nutzt einen Text-Schriftzug als Platzhalter. Offizielle Logodatei (SVG/PNG) einsetzen.
- **Farben:** Grün `#28442D` und Beige `#F0E7D3` sind angenommen, nicht aus einem CI-Handbuch.
- **Kundenhof:** Ob die Fotos beim Kunden entstanden sind, ist nicht belegt. Kund:in vor Veröffentlichung um Freigabe bitten, falls der Hof erkennbar ist.
- **Mitarbeitende** sind erkennbar im Bild (Kranführer, Person am Nachläufer): Einverständnis für Social Media prüfen.
- **Musik:** Für mehr Wirkung in der App einen Titel aus der Meta Sound Collection unterlegen (für Unternehmenskonten lizenziert) und die eingebettete Spur leiser stellen oder entfernen.

## Neu rendern
```bash
python3 music.py music.wav
python3 render.py natura_reel.mp4   # benötigt ffmpeg, Pillow, numpy, Schriftart Inter
```
