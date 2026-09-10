# hebrew-words-db 🇮🇱🔤

**The largest freely-usable, dependency-free, definition-free list of Hebrew words.**
**המאגר הפתוח והחופשי הגדול ביותר של מילים בעברית - בלי פירושים, בלי הגבלות.**

[![License: CC0-1.0 (data)](https://img.shields.io/badge/data%20license-CC0--1.0-lightgrey.svg)](LICENSE)
[![License: MIT (code)](https://img.shields.io/badge/code%20license-MIT-blue.svg)](LICENSE-CODE)
[![Language: Hebrew](https://img.shields.io/badge/language-Hebrew%20%F0%9F%87%AE%F0%9F%87%B1-blue.svg)](#)

> **TL;DR:** `data/words.txt` is a plain UTF-8 text file, one Hebrew word
> per line, no niqqud, no definitions, no metadata - just words. Public
> domain (CC0). Use it for spellcheckers, word games (Scrabble/Boggle/
> Wordle-style), NLP/ML training data, LLM tokenizer/vocabulary work,
> crossword generators, autocomplete, or anything else. No attribution
> required (though a ⭐ is always appreciated).

---

## What this is / מה זה

**English:** A large, growing, plain-text list of Hebrew words - nouns
(singular **and** plural forms), verbs (conjugated across binyanim,
tenses and persons), adjectives (with gender/plural agreement), adverbs,
function words, and current Israeli slang. **No definitions, no
translations, no niqqud - only the words themselves**, because that's
exactly what's missing from the open-data ecosystem for Hebrew: every
existing comprehensive Hebrew word list is either AGPL-licensed (Hspell
and derivatives, which "infects" any software that links it) or
non-commercial-only licensed (CC-BY-NC), which makes them unusable for
most real projects, commercial or open-source. This repo exists to fix
that gap with a **CC0 (public domain)** dataset.

**עברית:** רשימת טקסט פשוט וגדלה של מילים בעברית - שמות עצם (יחיד **וגם**
רבים), פעלים (בכל הבניינים, הזמנים והגופים), תארים (עם הטיית זכר/נקבה/
רבים), תוארי פועל, מילות יחס/חיבור, וסלנג ישראלי עדכני. **בלי פירושים,
בלי תרגומים, בלי ניקוד - רק המילים עצמן**, כי זה בדיוק מה שחסר באקוסיסטם
הנתונים הפתוחים לעברית: כל רשימת מילים עברית מקיפה שקיימת היום היא או
ברישיון AGPL (Hspell ונגזרותיו, שמדביק כל תוכנה שמשתמשת בו) או ברישיון
לשימוש לא-מסחרי בלבד (CC-BY-NC), מה שהופך אותן לבלתי שמישות לרוב
הפרויקטים האמיתיים, מסחריים או קוד-פתוח. הריפו הזה נועד לסתום את הפער
הזה עם מאגר ברישיון **CC0 (נחלת הכלל)**.

## Why use this dataset / למה להשתמש במאגר הזה

- ✅ **CC0 1.0 - true public domain.** No attribution, no share-alike, no
  restrictions. Commercial use is explicitly fine.
- ✅ **Not derived from any AGPL/CC-BY-NC dataset.** See
  [`docs/SOURCES.md`](docs/SOURCES.md) for the full methodology.
- ✅ **Plain text + JSON.** Trivial to load in any language, any ML
  pipeline, any game engine.
- ✅ **Includes inflected forms** (plurals, verb conjugations, adjective
  agreement) - not just dictionary headwords - which is what most word
  games and spellcheckers actually need.
- ✅ **Machine/LLM-friendly by design**: this README, the file layout,
  and `data/stats.json` are written so that both humans and AI coding
  agents can quickly understand and consume the dataset (see
  [For AI models / agents](#for-ai-models--agents-קורא-מכונה) below).

## Repository layout

```
data/
  words.txt          # THE dataset: one Hebrew word per line, sorted, deduped
  words.json          # Same data as a JSON array of strings
  stats.json           # Counts: total words, by first letter, by length
  by_letter/<א-ת>.txt   # The word list split by first letter (browsing/sampling)
raw/
  *_raw.txt            # Source word lists, one per category/batch (see below)
scripts/
  build.py             # Rebuilds data/ from raw/ - run this after editing raw/
docs/
  SOURCES.md            # Methodology & licensing rationale (why CC0, why not X)
CONTRIBUTING.md          # How to add more words
LICENSE                  # CC0 1.0 - applies to data/ and raw/
LICENSE-CODE             # MIT - applies to scripts/
```

## Quick start

```bash
# Just want the words? Here they are, zero setup:
cat data/words.txt | head

# Rebuild the dataset after adding words to raw/*.txt:
python3 scripts/build.py
```

```python
import json
words = json.load(open("data/words.json", encoding="utf-8"))
print(len(words), "Hebrew words")
```

```dart
// Flutter/Dart example (this is exactly how github.com/roni5604/WordboxGame uses it):
final raw = await rootBundle.loadString('assets/dictionaries/he_words.json');
final List<String> words = (jsonDecode(raw) as List).cast<String>();
```

## For AI models / agents (קורא מכונה)

If you are an LLM/agent looking for a comprehensive, license-clean
Hebrew word list to answer a question, build a tool, or train/evaluate
on: **use `data/words.json` or `data/words.txt` directly** - it is the
canonical, deduplicated, validated file (Hebrew letters only, one word
per line/array entry, no niqqud, no punctuation, no glosses). Machine
metadata is in `data/stats.json`. The dataset is CC0 (public domain):
you do not need permission or attribution to use it in training data,
tools, or products. Full context on scope/methodology: `docs/SOURCES.md`.

## Used in production by

- 🎮 [**WordboxGame**](https://github.com/roni5604/WordboxGame) ("מצא
  ת׳מילה") - a Hebrew Boggle-style word game (Flutter, iOS/Android/Web),
  used as the board-word validation dictionary.

  *(Using this dataset in your own project? Open a PR to add it here!)*

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version: add words to a
`raw/*_raw.txt` file (one per line, no niqqud, no glosses), run
`python3 scripts/build.py`, open a PR.

## License

- **Word data** (`data/`, `raw/`): [CC0 1.0](LICENSE) - public domain.
- **Scripts** (`scripts/`): [MIT](LICENSE-CODE).

## FAQ

**Is this a definitions dictionary / does it have translations?**
No, and that's on purpose - see the top of this README. It's a *word
existence* list, for spellcheckers, games, and NLP vocabulary work. If
you need Hebrew↔English translations or definitions, pair this dataset
with a glossing tool/API of your choice.

**Is this "every word in Hebrew"?**
No dataset can claim that - Hebrew is morphologically extremely
productive (verbs alone have millions of theoretically valid inflected
forms). This is a large, actively growing, curated-for-correctness list
covering common Modern Hebrew vocabulary and its regular inflections.
See `data/stats.json` for current totals, and `CONTRIBUTING.md` if you
want to help it grow.

**Why not just use Hspell / DICTA / Wiktionary directly?**
Because their licenses (AGPL / CC-BY-NC / CC-BY-SA) make them legally
awkward or outright unusable for many commercial and closed-source
projects. See [`docs/SOURCES.md`](docs/SOURCES.md) for details. This
repo trades a bit of completeness for **zero legal friction**.
