# Claude-Code-Skills

## Instagram-Skills (`ig-*`)

Übernommen aus [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
(Commit `d03c56b`). Lizenz: MIT, siehe `LICENSE-instagram-agent-skill`.

Die Skills erzeugen nur Entwürfe (Reels, Captions, Carousels, Stories, Kommentare, DMs).
Veröffentlicht wird immer manuell. Arbeitsdateien wie `voice.md`, `swipe.md`, `log.md`
und `plan.md` legen die Skills unter `~/.claude/instagram/` ab, also nicht im Repo.

### Eigene Anpassungen gegenüber dem Original

- `ig-reel/hooks.json`: Jedes `match`-Muster der 26 Hook-Formeln ist um deutsche
  Formulierungen ergänzt (jeweils mit `|` hinten angehängt, die englischen
  Muster sind unverändert). Beispiele: „Was dir keiner sagt …“ (#3),
  „Diesen Fehler machen …“ (#7), „Ab 1. März …“ (#19).
- `ig-viral/swipe.py`, `ig-reel/hookscore.py`: Die Wortzählung erkennt Umlaute
  und ß (vorher wurde „für“ als zwei Wörter gezählt).

Bei einem Update aus dem Original-Repo müssen diese Änderungen erneut
eingearbeitet werden.

Bekannte Grenze: Der Hook-Score (`hookscore.py`) bleibt auf Englisch ausgelegt.
Bei deutschen Hooks zählen großgeschriebene Substantive als „Namen“ (Konkretheit
zu hoch) und Spannungswörter werden nicht erkannt (Stakes zu niedrig). Den Score
bei deutschen Hooks nur als groben Anhaltspunkt lesen.
