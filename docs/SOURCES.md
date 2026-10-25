# Sources & Methodology / מקורות ומתודולוגיה

## English

This word list was **compiled, not copied**. No word list was scraped or
imported verbatim from any single existing proprietary or copyleft
dictionary/spellchecker database (specifically: **not** from Hspell /
`eyaler/hebrew_wordlists` (AGPLv3), **not** from DICTA's Hebrew
resources (CC-BY-NC-4.0), **not** from MILA's lexicon, and **not** a
scrape of Wiktionary/kaikki.org).

Instead, the words were generated from general knowledge of Modern
Hebrew vocabulary and grammar (an AI-assisted compilation process,
reviewed and normalized by scripts in `scripts/`), the same way a
fluent speaker or lexicographer would write down words they know from
memory, organized by semantic category (family, nature, food, verbs by
binyan/tense, adjectives with gender/plural agreement, common slang,
etc.).

A list of *which words exist in a language* is a factual/functional
compilation, not a creative work - similar in nature to a phone book or
a list of chemical element names. To remove any doubt and to make this
dataset maximally reusable, the word data (`data/`, `raw/`) is
dedicated to the public domain under **CC0 1.0** (see `LICENSE`). If you
individually verify a word against another dictionary and want to note
that dictionary as a cross-reference, feel free to open a PR that adds
it to this file - this file exists specifically to track any such
citations transparently.

## עברית

רשימת המילים הזו **הורכבה, לא הועתקה**. אף קובץ מילים לא "נשאב" או יובא
כמו שהוא ממאגר מילון/בודק-כתיב קיים כלשהו (בפרט: **לא** מ-Hspell /
`eyaler/hebrew_wordlists` (רישיון AGPLv3), **לא** ממשאבי DICTA
(CC-BY-NC-4.0, אסור מסחרית), **לא** ממאגר המילים של MILA, ו**לא** מסריקה
של ויקימילון/kaikki.org.

במקום זאת, המילים נכתבו מתוך ידע כללי על אוצר המילים והדקדוק של העברית
המודרנית (תהליך הרכבה בעזרת AI, שעבר נירמול וסינון אוטומטי בסקריפטים
בתיקיית `scripts/`) - בדיוק כמו שדובר עברית שוטף או לקסיקוגרף היה כותב
מהזיכרון רשימת מילים שהוא מכיר, מאורגנת לפי קטגוריות סמנטיות (משפחה,
טבע, אוכל, פעלים לפי בניין/זמן, תארים עם הטיית מין/רבים, סלנג נפוץ ועוד).

רשימה של *אילו מילים קיימות בשפה* היא הרכב עובדתי/פונקציונלי, לא יצירה
אמנותית - בדומה במהותה לספר טלפונים או לרשימת שמות של יסודות כימיים. כדי
להסיר כל ספק, ולהפוך את המאגר לשימושי ופתוח באמת, נתוני המילים (`data/`,
`raw/`) הוקדשו לנחלת הכלל תחת רישיון **CC0 1.0** (ראו `LICENSE`). אם
בדקתם מילה מול מילון אחר ורוצים לתעד את המילון הזה כאסמכתא צולבת, מוזמנים
לפתוח PR שמוסיף אותו לקובץ הזה - הקובץ הזה קיים בדיוק לצורך תיעוד שקוף
של אסמכתאות כאלה.

## Cross-references consulted for validation ideas (not copied)

- Academy of the Hebrew Language (האקדמיה ללשון העברית) - public spelling
  rules (`כללי הכתיב`) used only as a *style/spelling-convention*
  reference (e.g. when to use final letters), not as a word source.
- General public knowledge of Modern Hebrew as spoken/written in Israel
  (news, conversation, education) - for slang and everyday vocabulary
  coverage.

## Public-domain corpus used for gap-finding

- **Project Ben-Yehuda** (פרויקט בן-יהודה, public-domain Hebrew literature,
  github.com/projectbenyehuda/public_domain_dump). Token frequencies from
  the public-domain dump were used to *find candidate words missing from the
  list*. Every candidate was then judged individually (archaic forms, old
  spellings, names and multi-word tokens were discarded), rewritten in
  Modern ktiv male where needed, and reviewed before inclusion. The texts
  themselves are in the public domain, so this adds no license conditions.
  Batches from this source are the `raw/v3_corpus_*` and `raw/v3_corpus2_*`
  files.

## Quality process (all batches since v2)

Every AI-compiled batch is filtered against the existing data
(`scripts/new_words.py`), inflected by a shared generator
(`scripts/paradigm.py`) where possible, and then reviewed by an independent
reviewer pass that did not produce it; rejected words are removed before the
batch is built. Word-family "gap detectors" (e.g. lemmas missing possessive
forms, verbs missing tenses) and root-by-root sweeps are used to decide
*what* to look for — the words themselves are still written from knowledge
of Modern Hebrew, not copied from another list.

## Removal audits

In October 2026 every published word that an older open spell-checker
dictionary (Hspell, AGPL) does not recognise was reviewed by hand, and
clear errors were removed (invented inflections, wrong plurals, defective
spellings). The spell-checker was used only as a *filter for what to
review* — absence from it was never treated as an error on its own, and no
word was ever copied or added from it.
