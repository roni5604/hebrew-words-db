# Game-ready word list / רשימה מוכנה למשחקים

Generated automatically by `scripts/build.py` from `data/words.txt` — do not edit by hand.

| File | Format |
|---|---|
| `he_words_game.json` | JSON array, the exact format of `assets/dictionaries/he_words.json` in the "מצא את המילה" (WordboxGame) app |
| `he_words_game.txt` | same words, one per line |

Rules: final letters (ך ם ן ף ץ) are normalized to their base form (כ מ נ פ צ), only words of 2–9 letters, deduplicated after normalization, sorted.

**Update the app in one step** (from the WordboxGame folder):

```bash
curl -L -o assets/dictionaries/he_words.json \
  https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/game/he_words_game.json
```

(or keep using `tool/sync_hebrew_words_db.py` + `tool/build_dictionary.py`, which also regenerates `letter_frequency.json` and merges the game's own seed words.)

עברית: הקובץ `he_words_game.json` בנוי בדיוק בפורמט של מילון האפליקציה "מצא את המילה" — אותיות סופיות מנורמלות, 2–9 אותיות, ממוין וללא כפילויות. אפשר להעתיק אותו ישירות ל-`assets/dictionaries/he_words.json`.
