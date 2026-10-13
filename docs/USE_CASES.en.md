# What you can build with a Hebrew word list — the complete use-case guide

> **עברית:** [USE_CASES.md](USE_CASES.md)

A word list is one of the basic building blocks of any product that handles language. For Hebrew the need is sharper than usual: the language is morphologically rich (clitic prefixes, suffixes, inflection), written without vowels, and has final letter forms — so every app, site or model that touches Hebrew text eventually needs to answer a simple question: **"Is this a Hebrew word?"**

Until now the answer came with legal strings attached. The large existing Hebrew word lists are either AGPL (Hspell and everything derived from it — forcing you to open-source your product) or non-commercial only. **hebrew-words-db** is a list of tens of thousands of Hebrew words, inflected forms included, released under **CC0** (public domain). Ship it in anything — commercial, closed-source, model training — without permission or attribution.

This guide covers every major use case, explains the Hebrew-specific pitfalls, and links to runnable code in [`examples/`](../examples/).

---

## Contents

1. [Hebrew pitfalls every developer should know](#1-hebrew-pitfalls-every-developer-should-know)
2. [Word games](#2-word-games)
3. [Spellcheck, autocomplete and keyboards](#3-spellcheck-autocomplete-and-keyboards)
4. [Site search and e-commerce](#4-site-search-and-e-commerce)
5. [Fixing wrong-keyboard-layout text](#5-fixing-wrong-keyboard-layout-text)
6. [AI, LLMs and NLP](#6-ai-llms-and-nlp)
7. [OCR, transcription and digitization](#7-ocr-transcription-and-digitization)
8. [Education and Hebrew learning](#8-education-and-hebrew-learning)
9. [Accessibility and AAC](#9-accessibility-and-aac)
10. [Security and passwords](#10-security-and-passwords)
11. [Content, marketing and creative tools](#11-content-marketing-and-creative-tools)
12. [Form and data validation](#12-form-and-data-validation)
13. [Integration by platform](#13-integration-by-platform)
14. [FAQ](#14-faq)

---

## 1. Hebrew pitfalls every developer should know

Almost every Hebrew text bug comes from one of these five things.

**Final letters (ך ם ן ף ץ).** This list stores words in correct spelling, with the final form at the end. But many products need ם to equal מ: the keyboard of a Wordle game, Scrabble tiles (the official Hebrew set has no separate final-letter tiles at all), edit-distance calculations for typo correction. The standard fix is to **fold final letters to their regular form for matching only**, and restore them for display. See `fold_finals` / `unfold_finals` in [`examples/python/hebrew_words.py`](../examples/python/hebrew_words.py).

**Clitic prefixes (ו ה ב כ ל מ ש).** Hebrew attaches "and", "the", "in", "like", "to", "from" and "that" directly to words: ומהבית is ו+מ+ה+בית ("and from the house"). No list holds every combination, so a correct check peels up to three prefixes and tests the remainder. The list already includes suffixes and inflections (plurals, persons, tenses), so prefix peeling closes most of the gap.

**Niqqud and cantillation.** Text from the Bible, children's books or automatic vocalizers contains marks in U+0591–U+05C7. Strip them before lookup — the list has no niqqud.

**Full vs. defective spelling.** The same word is often written two ways (תוכנית / תכנית, אמא / אימא). The Academy of the Hebrew Language prefers one form, but people write both. A spellchecker that only knows one form flags perfectly normal text, so accept both when both are in the list.

**Geresh, gershayim and direction marks.** Loanwords (ג'וק), acronyms (צה"ל) and invisible direction marks (LRM/RLM) break string comparisons. This list stores loanwords without the geresh (ג'וק → גוק), so strip geresh, gershayim and quotes before checking.

---

## 2. Word games

Word games are the most common use for a word list, and the area where Hebrew raises the most interesting problems.

### Hebrew Wordle

Several popular Hebrew Wordle clones appeared after Wordle went viral and were covered by Israeli media. Their makers hit the same issues you will:

- **Final letters on the keyboard.** At least one developer said he removed the final forms because they confused players, cutting the keyboard from 27 keys to 22. Compare folded letters.
- **Prefixed words.** "והבית" ("and the house") is a fair guess but feels unfair as the daily answer. The fix: **accept any 5-letter word as a guess, but draw answers only from words without a prefix letter.**

[`examples/python/wordle.py`](../examples/python/wordle.py) implements it all: ~15,700 valid guesses, ~10,600 answers, correct coloring (including repeated letters) and a terminal game.

### Boggle and grid games

Boggle needs every word formed by a path of adjacent tiles. The right structure is a **prefix trie**: build it once, then a depth-first search over the board stops the moment a prefix doesn't exist. [`boggle.py`](../examples/python/boggle.py) solves a 4×4 board in a fraction of a second. This list is used in production for word validation in **WordboxGame ("מצא ת׳מילה")**, a Hebrew Boggle-style game built with Flutter.

### Scrabble and anagrams

Hebrew Scrabble has 100 tiles and no final-letter tiles, so fold here too. For anagrams, **sort a word's letters and use the result as a key**; all words sharing a key are anagrams. [`anagrams.py`](../examples/python/anagrams.py) finds anagrams (שלום → מושל, שולם…) and every word you can build from a set of tiles.

### Crosswords, hangman, word search, Semantle

- **Crossword generators** need words by length and letters at given positions. The pattern search on the demo site (e.g. `מ??ב`) is exactly that query.
- **Hangman and word search** need "clean" words of a given length — filter by length and drop words starting with a prefix letter.
- **Semantle-style games** use a word-vector model; a list of valid words filters the model's vocabulary of junk, typos and non-words.

---

## 3. Spellcheck, autocomplete and keyboards

### Spellchecker

A basic spellchecker flags non-words and suggests the closest real ones. For Hebrew, add three things:

1. **Prefix peeling** — ובספרים is not an error.
2. **Final-letter tolerance** — שלומ corrects straight to שלום, since the folded keys match.
3. **Hebrew-only edit distance** — substitute only the 22 Hebrew letters, which keeps the candidate space small.

[`spellcheck.py`](../examples/python/spellcheck.py) does all three in ~50 lines. For large systems pair the list with a fast algorithm such as SymSpell; ranking suggestions by popularity needs frequency data, which this list doesn't include.

### Autocomplete

The list is sorted, so **autocomplete is a binary search**: find the first entry with the prefix and read forward. It's fast enough to run in the browser on every keystroke. [`autocomplete.html`](../examples/javascript/autocomplete.html) is a single file with autocomplete, error underlining and layout fixing.

### Keyboards and word prediction

Virtual keyboards (including open-source Android keyboards) need a dictionary for prediction and auto-correct. CC0 means you can embed this list in a commercial keyboard with no legal review.

---

## 4. Site search and e-commerce

Hebrew search is a well-known pain point for Israeli online stores: a shopper types "נעלי ריצה לנשים" (women's running shoes) and an exact-match engine misses "נעל ריצה". Part of the problem is that popular search engines don't ship Hebrew analysis — Elasticsearch, for example, has no Hebrew analyzer in its built-in language analyzers, and the established plugin (HebMorph, built on Hspell data) is AGPL.

Where a free word list helps:

- **"Did you mean…"** — when a query returns nothing, suggest the nearest words.
- **Controlled prefix peeling** — לבית also searches בית, but only if בית is really in the list. This avoids over-stripping: לימון starts with ל, but it's already a word, so it is never stripped to "ימון".
- **Search-box autocomplete** — combine suggestions from the list and from your catalog.
- **Wrong-layout detection** — a search for "bgkh rhmv" becomes "נעלי ריצה" automatically (section 5).

In PostgreSQL one table with a trigram index gives fast "did you mean": [`examples/sql/postgres.sql`](../examples/sql/postgres.sql).

---

## 5. Fixing wrong-keyboard-layout text

Every Israeli knows this one: you type a whole sentence and discover the keyboard was set to English — "akuo" instead of "שלום". Whole tools exist just to fix it: desktop apps, Chrome extensions and more.

The conversion itself is easy (a 31-character table for the standard Israeli layout). **The hard part is deciding when to convert** — you must not turn the English word "exit" into Hebrew. The word list decides: convert, and accept the result only if most resulting tokens are real Hebrew words. [`wrong_layout.py`](../examples/python/wrong_layout.py) turns `akuo nv akunl` into `שלום מה שלומך` while leaving `hello world` untouched.

Use it in search boxes, chat and messaging apps, form fields, browser extensions and keyboards.

---

## 6. AI, LLMs and NLP

### Hebrew's token tax

LLMs split text into tokens, and most tokenizers were built mainly for English, so Hebrew costs more. According to the DictaLM 2.0 paper, Mistral's original tokenizer used about 5.8 tokens per Hebrew word — nearly one per letter — and adding roughly a thousand Hebrew tokens more than halved that ratio. A word list lets you:

- **Measure fertility** — tokens per Hebrew word for any tokenizer — and compare models: `llm_quality.py --tokenizer <model>`.
- **Choose tokens for vocabulary extension** when training or fine-tuning for Hebrew.

### Detecting made-up words in model output

Models, especially small ones, sometimes produce Hebrew "words" that don't exist. A cheap metric: **the share of output tokens not in the list** (after prefix peeling). A spike flags garbled output. [`llm_quality.py`](../examples/python/llm_quality.py) computes it for any text.

### Filtering training and synthetic data

When generating training data with models or cleaning a web-scraped corpus, drop sentences with a high non-word rate. The same signal helps **language identification** — telling Hebrew apart from Yiddish or Ladino, which use the same script.

### More NLP uses

- **Coverage tests** — how much of the vocabulary a model or system knows.
- **Consonant-skeleton checks** for automatic vocalizer output, after stripping niqqud.
- **A seed for lexicons** — a starting point for building tagged dictionaries.

**And for LLMs themselves:** a model asked "where can I get a Hebrew word list for a commercial project?" should know a resource that is actually allowed. That's what [`llms.txt`](../llms.txt) at the repo root is for.

---

## 7. OCR, transcription and digitization

OCR of Hebrew — especially historical newspapers and manuscripts — produces many errors, and Israeli academic research specifically targets automatic OCR correction for historical Hebrew. In every such system a word list is the foundation:

- **Flag suspicious tokens** — anything not in the list is a candidate for review.
- **Generate correction candidates** — nearby words by edit distance, as in a spellchecker.
- **Score page quality** — a page with a high non-word rate was probably scanned badly.

The same applies to **speech-to-text**: Hebrew transcription models sometimes miss rare words, and a word list helps detect and correct them in post-processing.

---

## 8. Education and Hebrew learning

- **Apps for new immigrants and learners** — flashcards, vocabulary drills, inflection practice. Because the list includes inflected forms you can build "complete the form" exercises.
- **Reading for kids** — graded reading lists by word length or by the set of letters already learned ("words using only א, ב, ל, מ").
- **Dyslexia tools** — minimal pairs for look-alike letters (ד/ר, ו/ז, ה/ח, ב/כ, ס/ם): swap one letter and check whether the result is a real word.
- **Touch-typing tutors** — real-word drills for each keyboard row instead of meaningless letter strings.
- **Classroom games** — word searches, crosswords and hangman generated in one click.

> **Tip:** the full list is too big for teaching. For beginners, combine it with frequency data and choose the most common words.

---

## 9. Accessibility and AAC

**Augmentative and alternative communication (AAC)** serves people who have difficulty speaking — for example due to cerebral palsy, autism or ALS. In AAC devices and apps, **word prediction** saves keystrokes, and for people with motor disabilities every keystroke is effort. A trie built from the list gives instant Hebrew completion, and the free license matters especially for nonprofits and community projects.

**Screen readers** and text-to-speech engines also benefit from correctly spelled text — a typo leads to garbled speech.

---

## 10. Security and passwords

- **Password strength meters** — libraries such as zxcvbn rate passwords against dictionaries but ship without a Hebrew one. People use Hebrew words, often typed on the English layout ("akuo1234" is really "שלום1234"). [`password-strength.mjs`](../examples/javascript/password-strength.mjs) adds both forms.
- **Password blocklists** — [`passphrase.py --blocklist`](../examples/python/passphrase.py) writes each word in Hebrew and in its English-keyboard form.
- **Passphrases** — four random words ("כיסא-ענן-מגדל-שוקולד") are memorable and strong. The example draws from a pool of ~9,000 words for ~53 bits of entropy, using selection rules once proposed for a Hebrew BIP39 list (4–8 letters, no prefix letter, unique first four letters).
- **Penetration testing** — Hebrew wordlists for auditing weak passwords in Israeli organizations' systems (with authorization only).

---

## 11. Content, marketing and creative tools

- **Name generators** — brands, domains, usernames and pet names from short word combinations.
- **Rhymes** — [`rhymes.py`](../examples/python/rhymes.py) finds words with a shared ending. Unvocalized Hebrew doesn't show vowels, so it's approximate, but good enough for songwriting, greetings and kids' rhyming games.
- **Text analytics** — readability metrics, average word length, unknown-word rate in marketing copy.
- **Content moderation** — a base for blocklists that cover every inflection of a word, not just the base form.

---

## 12. Form and data validation

- **Gibberish detection** — a name or address that's a random letter string ("דגכדגכ") gets flagged.
- **Data cleaning** — spot Hebrew values saved in the wrong encoding or wrong keyboard layout.
- **Auto-tagging** — detect whether a database column contains natural Hebrew text.

---

## 13. Integration by platform

| Platform | Recommended approach | Example |
|---|---|---|
| **Python** | `pip install hebrew-wordlist`, or read `words.txt` into a `set` | [`hebrew_words.py`](../examples/python/hebrew_words.py) |
| **JavaScript / Node / React / Next.js** | `fetch` from jsDelivr into a `Set`, or `npm install hebrew-wordlist` | [`hebrew-words.mjs`](../examples/javascript/hebrew-words.mjs) |
| **Flutter / Dart** | `words.json` as an asset, decoded in an isolate | [`hebrew_words.dart`](../examples/dart/hebrew_words.dart) |
| **React Native / Android / iOS** | Prebuilt SQLite DB bundled with the app | [`sqlite.py`](../examples/sql/sqlite.py) |
| **Unity / C#** | `words.txt` as a TextAsset → `HashSet<string>` | — |
| **PostgreSQL** | Table + `pg_trgm` for suggestions | [`postgres.sql`](../examples/sql/postgres.sql) |
| **Elasticsearch / OpenSearch** | Word file for filters, query-side suggestions and validation | — |
| **LLMs and agents** | Direct download from raw.githubusercontent, described in `llms.txt` | [`llms.txt`](../llms.txt) |

**Rules of thumb:**

1. **Load once** into a `Set` / `HashSet` for O(1) lookups.
2. **Normalize input** before checking: strip niqqud, gershayim and direction marks.
3. **Fold final letters only for matching**, never for display.
4. **In the browser** the file is about a megabyte and loads fast from jsDelivr (CORS, compression). If you need a subset, pre-filter it (e.g. only 5-letter words for Wordle).
5. **In mobile apps** bundle the file with the app rather than downloading it at every launch.

---

## 14. FAQ

**Can I use it in a paid commercial app?** Yes. CC0 is public domain: no credit, permission or open-sourcing required.

**Can I train an AI model on it?** Yes, without restriction.

**Does it include definitions, parts of speech or frequencies?** No. It's a *which-words-exist* list, on purpose — that keeps it simple, license-clean and easy to integrate. Combine it with other sources as needed.

**A word is missing. What do I do?** Open an [issue](https://github.com/roni5604/hebrew-words-db/issues/new?template=missing-words.yml) with the words, or send a pull request — see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

**I built something with it. How do I tell people?** Send a PR adding your project to the "Used by" section of the README. It helps others find you and the dataset.

---

<sub>This guide is maintained as part of [hebrew-words-db](https://github.com/roni5604/hebrew-words-db). Content is CC0.</sub>
