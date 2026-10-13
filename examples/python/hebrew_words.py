"""Tiny shared helper for the examples: load the word list + Hebrew text utilities.

Uses the local repo copy (../../data/words.txt) when run inside the repo,
otherwise downloads it once from GitHub. Standard library only.
"""

from __future__ import annotations

import re
import urllib.request
from functools import lru_cache
from pathlib import Path

URL = "https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.txt"
LOCAL = Path(__file__).resolve().parents[2] / "data" / "words.txt"

# Final (sofit) letters -> regular form. Use for MATCHING only (games,
# keyboards, Scrabble tiles); keep the original spelling for display.
FINAL_TO_REGULAR = str.maketrans("ךםןףץ", "כמנפצ")
REGULAR_TO_FINAL = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}

# Niqqud + cantillation marks (U+0591-U+05C7) and geresh/gershayim/quotes.
_MARKS = re.compile(r"[֑-ׇ'\"׳״‎‏]")

# Common one-letter clitic prefixes (and, the, in, like, to, from, that).
PREFIX_LETTERS = "והבכלמש"


@lru_cache(maxsize=1)
def words() -> list[str]:
    if LOCAL.exists():
        text = LOCAL.read_text(encoding="utf-8")
    else:
        text = urllib.request.urlopen(URL).read().decode("utf-8")
    return text.split()


@lru_cache(maxsize=1)
def word_set() -> frozenset[str]:
    return frozenset(words())


def clean(text: str) -> str:
    """Strip niqqud, cantillation, geresh and direction marks."""
    return _MARKS.sub("", text).strip()


def fold_finals(word: str) -> str:
    """ספרים -> ספרימ  (matching key: every letter in its regular form)."""
    return word.translate(FINAL_TO_REGULAR)


def unfold_finals(word: str) -> str:
    """ספרימ -> ספרים  (restore the final form of the last letter for display)."""
    if word and word[-1] in REGULAR_TO_FINAL:
        return word[:-1] + REGULAR_TO_FINAL[word[-1]]
    return word


def is_word(token: str, strip_prefixes: bool = True) -> bool:
    """True if the token is a known word, optionally after peeling up to three
    clitic prefixes (e.g. ומהבית -> מהבית -> הבית -> בית)."""
    token = clean(token)
    ws = word_set()
    if token in ws:
        return True
    if strip_prefixes:
        for _ in range(3):
            if len(token) > 2 and token[0] in PREFIX_LETTERS:
                token = token[1:]
                if token in ws:
                    return True
            else:
                break
    return False
