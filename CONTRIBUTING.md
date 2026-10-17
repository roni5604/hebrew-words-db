# תרומה לפרויקט / Contributing

## עברית

תודה שאתם רוצים לעזור להגדיל את המילון! כמה כללים פשוטים:

1. **איפה מוסיפים מילים?** בקובץ חדש או קיים בתיקיית `raw/` (שמו חייב
   להסתיים ב-`_raw.txt`). מילה אחת בכל שורה. אפשר להוסיף שורת הערה
   שמתחילה ב-`#` כדי לתעד קטגוריה - היא תוסר אוטומטית.
2. **בלי ניקוד, בלי פירושים.** רק המילה עצמה, בכתיב מלא (עם אותיות
   סופיות ך/ם/ן/ף/ץ כשנכון). אין צורך (ואין רצון) לתעד את הפירוש - זה
   מילון של *אילו מילים קיימות*, לא מילון הגדרות.
3. **בלי העתקה ממילון קיים כמו שהוא.** ראו `docs/SOURCES.md` - המטרה
   היא מאגר שנכתב/מאומת ולא "שאיבה" של קובץ מילים קיים שיש עליו רישיון
   (AGPL/CC-BY-NC וכו').
4. **הריצו את סקריפט הבנייה** לפני שליחת PR:
   ```bash
   python3 scripts/build.py
   ```
   זה בונה מחדש את `data/words.txt`, `data/words.json`,
   `data/by_letter/*.txt` ו-`data/stats.json`, ומסנן שורות לא תקינות.
5. **בדקו את `data/stats.json` וודאו שהמספרים הגיוניים** (המספר הכולל
   עלה, אין שגיאות ולידציה גדולות מדי ב-stdout של הסקריפט).
6. פתחו Pull Request עם תיאור קצר של מה הוספתם (למשל "הוספתי 200 מילות
   סלנג צבאי").


### כלים שחוסכים עבודה

- **כללי הכתיבה המלאים:** [`docs/WORD_RULES.md`](docs/WORD_RULES.md) (בלי תחיליות צמודות כמו ו/ה/ב, כתיב מלא, בלי שמות פרטיים).
- **לפני שמוסיפים — בדקו מה חסר:** `python3 scripts/new_words.py --check מילה1 מילה2`
- **סינון קובץ מועמדים** כך שרק מילים חדשות ותקינות ייכנסו:
  `python3 scripts/new_words.py candidates.txt -o raw/my_batch_raw.txt --header "תיאור"`

## English

Thanks for helping grow this dictionary! A few simple rules:

1. **Where to add words?** In a new or existing file under `raw/` (must
   end with `_raw.txt`). One word per line. You may add a `#` comment
   line to label a category - it's stripped automatically.
2. **No niqqud (vowel points), no glosses/definitions.** Just the word
   itself, in full standard spelling (with final letters ך/ם/ן/ף/ץ where
   correct). This is a list of *which words exist*, not a definitions
   dictionary.
3. **No verbatim copying from an existing licensed word-list file.** See
   `docs/SOURCES.md` - the goal is a compiled/verified dataset, not a
   scrape/import of an existing AGPL/CC-BY-NC dataset.
4. **Run the build script** before opening a PR:
   ```bash
   python3 scripts/build.py
   ```
   This rebuilds `data/words.txt`, `data/words.json`,
   `data/by_letter/*.txt` and `data/stats.json`, filtering invalid lines.
5. **Check `data/stats.json`** and make sure the numbers look sane (total
   count increased, no huge amount of validation errors printed by the
   script).
6. Open a Pull Request describing what you added (e.g. "Added 200
   military slang words").

### Tools that save work

- **Full spelling rules:** [`docs/WORD_RULES.md`](docs/WORD_RULES.md) (no glued clitic prefixes like ו/ה/ב, ktiv male, no proper names).
- **Check what's missing before adding:** `python3 scripts/new_words.py --check word1 word2`
- **Filter a candidate file** so only new, valid words go in:
  `python3 scripts/new_words.py candidates.txt -o raw/my_batch_raw.txt --header "description"`
- After `build.py`, `python3 scripts/update_counts.py` refreshes the word count in the README, site and packages.
