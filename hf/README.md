---
language:
- he
license: cc0-1.0
pretty_name: Hebrew Words (CC0 Hebrew word list)
size_categories:
- 100K<n<1M
tags:
- hebrew
- wordlist
- word-list
- lexicon
- vocabulary
- dictionary
- spellcheck
- word-games
- public-domain
configs:
- config_name: default
  data_files:
  - split: train
    path: data/words.csv
---

# Hebrew Words — public-domain Hebrew word list · מאגר מילים בעברית

**167,000+ Modern Hebrew words** — including noun plurals, verb conjugations and adjective forms — released under **CC0 1.0 (public domain)**. No niqqud, no definitions, just words.

This is a mirror of [github.com/roni5604/hebrew-words-db](https://github.com/roni5604/hebrew-words-db), synced automatically on every update. Issues and contributions go to GitHub.

## Load it

```python
from datasets import load_dataset
ds = load_dataset("roni5604/hebrew-words", split="train")
words = set(ds["word"])
print(len(words), "שלום" in words)
```

Or without `datasets`:

```python
import pandas as pd
df = pd.read_csv("hf://datasets/roni5604/hebrew-words/data/words.csv")
```

## Fields

| Column | Type | Description |
|---|---|---|
| `word` | string | A Hebrew word (letters U+05D0–U+05EA only, no niqqud) |
| `length` | int | Number of letters |

Plain-text (`data/words.txt`) and JSON (`data/words.json`) versions are included in the repo too.

## Why

Nearly every other comprehensive Hebrew word list is AGPL (Hspell, hebrew_wordlists), non-commercial (DICTA, CC BY-NC) or share-alike (Wiktionary). This dataset is CC0, so it can be used in commercial products, closed-source apps and model training with no attribution requirement.

## Uses

Spellcheck and autocomplete, Hebrew word games (Wordle, Boggle, Scrabble, crosswords), vocabulary coverage tests for LLMs and tokenizers, filtering non-words in generated text, education apps.

## Limitations

- A *which-words-exist* list: no definitions, part-of-speech tags, frequencies or proper names.
- Not exhaustive — Hebrew morphology yields millions of valid forms. Coverage focuses on common Modern Hebrew and regular inflections, and grows over time.
- Compiled with AI assistance and validated by script; occasional errors are possible. Please report them on GitHub.
- Loanwords are stored without geresh (ג'וק → גוק).

## Citation

```bibtex
@misc{michaeli_hebrew_words_db,
  author       = {Michaeli, Roni},
  title        = {hebrew-words-db: A public-domain list of Hebrew words},
  year         = {2026},
  howpublished = {\url{https://github.com/roni5604/hebrew-words-db}},
  doi          = {10.5281/zenodo.23442852},
  note         = {CC0-1.0}
}
```
