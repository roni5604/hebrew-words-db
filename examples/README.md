# Examples · דוגמאות קוד

Ready-to-run code that shows what you can build with the Hebrew word list. Every Python example uses the standard library only and runs from this folder (it reads `../../data/words.txt`, or downloads it if you copied the file elsewhere).

קוד מוכן להרצה שמראה מה אפשר לבנות עם מאגר המילים. כל הדוגמאות ב-Python משתמשות רק בספרייה הסטנדרטית.

| Example | What it does | מה זה עושה |
|---|---|---|
| [`python/spellcheck.py`](python/spellcheck.py) | Spellchecker with "did you mean", prefix-aware, final-letter tolerant | בודק איות עם הצעות תיקון |
| [`python/wordle.py`](python/wordle.py) | Hebrew Wordle: answer & guess lists, scoring, terminal game | וורדל בעברית |
| [`python/anagrams.py`](python/anagrams.py) | Anagram solver + "words from these tiles" (Scrabble helper) | פותר אנגרמות ושבץ-נא |
| [`python/boggle.py`](python/boggle.py) | Boggle board solver with a trie | פותר לוח בוגל |
| [`python/wrong_layout.py`](python/wrong_layout.py) | Fix text typed in the wrong layout (`akuo` → `שלום`) | תיקון "שכחתי להחליף שפה" |
| [`python/passphrase.py`](python/passphrase.py) | Hebrew passphrases + password blocklist (Hebrew & English-keyboard forms) | סיסמאות ורשימה שחורה |
| [`python/llm_quality.py`](python/llm_quality.py) | Non-word rate for LLM / OCR / speech-to-text output, tokenizer fertility | בדיקת איכות פלט של מודלים ו-OCR |
| [`python/rhymes.py`](python/rhymes.py) | Approximate rhyme finder (חרוזים) | מחולל חרוזים |
| [`python/hebrew_words.py`](python/hebrew_words.py) | Shared helpers: load, clean niqqud, fold final letters, peel prefixes | פונקציות עזר |
| [`javascript/hebrew-words.mjs`](javascript/hebrew-words.mjs) | Browser/Node module: `isWord`, `autocomplete`, `fixLayout` | מודול JavaScript |
| [`javascript/autocomplete.html`](javascript/autocomplete.html) | Single-file autocomplete + spellcheck + layout fix demo | השלמה אוטומטית בקובץ אחד |
| [`javascript/password-strength.mjs`](javascript/password-strength.mjs) | Add Hebrew dictionaries to zxcvbn-ts | חוזק סיסמה בעברית |
| [`sql/postgres.sql`](sql/postgres.sql) | PostgreSQL table + trigram "did you mean" + autocomplete | PostgreSQL |
| [`sql/sqlite.py`](sql/sqlite.py) | Build an offline SQLite DB for mobile/desktop apps | מסד נתונים לאפליקציות |
| [`dart/hebrew_words.dart`](dart/hebrew_words.dart) | Flutter asset loader with prefix-aware `isWord` | Flutter |

```bash
cd examples/python
python3 spellcheck.py "שלומ עולמ"     # ✗ שלומ → שלום ...
python3 wrong_layout.py "akuo nv akunl" # שלום מה שלומך
python3 anagrams.py שלום               # ושלם מושל שולם שלמו
python3 passphrase.py                  # e.g. כיסא-ענן-מגדל-שוקולד
```

See [`docs/USE_CASES.md`](../docs/USE_CASES.md) for the full guide to use cases and Hebrew-specific pitfalls.
