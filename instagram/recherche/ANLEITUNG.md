# Reel-Recherche für `/ig-viral`

Ziel: herausfinden, welche Reel-Einstiege („Hooks“) in unserem Themenfeld
überdurchschnittlich gut laufen. Maßstab ist nicht die reine Aufrufzahl, sondern
der **Outlier-Faktor** = Aufrufe des Reels ÷ Median der Aufrufe dieses Accounts.
Ab etwa 3x ist ein Reel auffällig, unter 1,5x ist es ein normaler Tag.

## 1. Accounts auswählen (6–12)

- 4 direkt: Forst, Wald, Baumpflege, ähnliches Angebot
- 4 angrenzend: andere Branche, ähnliches Publikum (z. B. Garten, Naturschutz, Handwerk)
- 2–4 große Accounts, nur für das Format, nicht für Ton oder Frequenz

Möglichst Accounts, die höchstens etwa 10-mal so groß sind wie unserer.

## 2. Erfassen (manuell, im normalen Browser oder in der App)

`vorlage.tsv` kopieren, z. B. nach `2026-11.tsv`, und in Excel oder einem
Texteditor füllen. Spalten werden mit **Tabulator** getrennt; aus Excel als
„Text (Tabstopp-getrennt)“ speichern.

| Spalte | Inhalt |
| --- | --- |
| `account` | Handle, z. B. `@beispiel_forst` |
| `followers` | Followerzahl laut Profil, ohne Punkte |
| `median` | mittlerer Wert der Aufrufe der letzten 12 Reels (sortieren, mittleren nehmen) |
| `views` | Aufrufe dieses Reels, ohne Punkte |
| `hook` | erster Satz, gesprochen oder als Text eingeblendet, wörtlich |

Pro Account ca. 12 Reels, insgesamt mindestens 40. Darunter sind die Ergebnisse
kaum belastbar.

## 3. Auswerten

In Claude Code `/ig-viral` aufrufen und die Datei angeben, oder direkt:

```bash
python3 .claude/skills/ig-viral/swipe.py instagram/recherche/2026-11.tsv
```

## Bekannte Einschränkung: deutsche Hooks

Die Erkennung der 26 Hook-Formeln und der Hook-Score sind auf **englische**
Formulierungen ausgelegt. Deutsche Hooks erscheinen als `unclassified`. Die
Rangliste nach Outlier-Faktor stimmt trotzdem; die Muster liest man bei
deutschen Hooks von Hand heraus (bzw. lässt Claude das bei `/ig-viral` tun).

## Regeln

- Nur manuell lesen. Kein Scraping, keine Crawler, keine Scraping-Dienste
  (Nutzungsbedingungen von Instagram).
- Keine Zugangsdaten an Claude oder Tools weitergeben.
- Nur das Muster übernehmen (Aufbau, Länge, Art des Einstiegs), nie Video, Text
  oder Schnitt anderer.
- Datensparsam: nur die fünf Spalten oben, keine Kommentare oder Follower-Listen.
  Ausgefüllte Erfassungsdateien werden **nicht** ins Repo committet (siehe
  `.gitignore`) und nach der Auswertung gelöscht. Ob das so mit unserer
  Datenschutzdokumentation passt, bitte intern prüfen.
