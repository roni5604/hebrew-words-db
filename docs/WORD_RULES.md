# Word-writing rules (for contributors and AI agents)

These rules keep `hebrew-words-db` consistent. Every word in a `raw/*_raw.txt`
file must follow them.

## What a "word" is here

- A real Modern Hebrew **surface form** that a fluent speaker would recognize
  as correctly spelled, written **without niqqud**.
- Inflected forms are welcome and wanted: noun plurals, construct (סמיכות)
  forms, possessive-suffix forms, full verb conjugations, adjective
  gender/number forms, prepositions with pronoun suffixes.
- Infinitives with ל are lexical and included (לשמור, להיות).

## What is NOT included

- **Clitic prefixes glued to a word**: no ו/ה/ב/כ/ל/מ/ש + word
  (not והבית, בבית, שהלך, מהעיר). Users peel these themselves; adding them
  would multiply the list by 50 without adding vocabulary.
  (Exception: when the letter is part of the word itself: לחם, מים, בית, שולחן.)
- Proper names of people, brands, companies.
- Definitions, niqqud, geresh/gershayim (loanwords are written without the
  geresh: ג'ינס → גינס, צ'יפס → ציפס), punctuation, Latin letters, digits.
- Multi-word expressions (one token per line only).
- Anything you are not sure is a real, correctly spelled word. **When in
  doubt, leave it out.** Quality beats quantity.

## Spelling

- **Ktiv male** (full spelling, the standard for unvocalized Hebrew, per the
  Academy of the Hebrew Language rules): ו for o/u (שומר, כותבת, תוכנית), י for
  i where the rules require it (שיר, דיבור), doubled ו/י for consonantal
  vav/yod in the middle of a word (תקווה, מצוות, עכשיו, ריאיון / ראיון).
- If two spellings are both in wide current use (תכנית / תוכנית,
  אמא / אימא), both may be listed.
- Final letters ך ם ן ף ץ only at the end of a word.

## Workflow

1. Write candidates (one per line) to a scratch file.
2. Check which already exist and keep only new, valid ones:

   ```bash
   python3 scripts/new_words.py candidates.txt -o raw/<batch>_raw.txt --header "Batch: <topic>"
   ```

   Quick membership check: `python3 scripts/new_words.py --check מילה מילה2`
3. Run `python3 scripts/build.py` to rebuild `data/`.
