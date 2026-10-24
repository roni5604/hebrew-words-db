# hebrew-wordlist

The largest public-domain (CC0) list of Hebrew words — 178,000+ words including plurals, verb conjugations and adjective forms. Zero dependencies. Data from [github.com/roni5604/hebrew-words-db](https://github.com/roni5604/hebrew-words-db).

```bash
pip install hebrew-wordlist
```

```python
import hebrew_wordlist as hw

hw.is_word("שלום")        # True
len(hw.words())            # 178000+
hw.of_length(5)[:3]        # five-letter words, e.g. for a Hebrew Wordle
hw.starting_with("מח")     # prefix search
hw.random_words(3, seed=1)
```

Word data: CC0-1.0 (public domain). Code: MIT.
