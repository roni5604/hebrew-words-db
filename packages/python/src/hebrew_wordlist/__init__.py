"""The largest public-domain (CC0) list of Hebrew words.

    >>> import hebrew_wordlist as hw
    >>> len(hw.words()) > 60000
    True
    >>> hw.is_word("שלום")
    True

Data: https://github.com/roni5604/hebrew-words-db (CC0-1.0).
"""

from __future__ import annotations

import random as _random
from functools import lru_cache
from importlib.resources import files
from typing import FrozenSet, List, Optional

__all__ = ["words", "word_set", "is_word", "starting_with", "of_length", "random_words"]


@lru_cache(maxsize=1)
def words() -> List[str]:
    """All words, sorted, as a list of str."""
    text = files(__name__).joinpath("words.txt").read_text(encoding="utf-8")
    return text.split()


@lru_cache(maxsize=1)
def word_set() -> FrozenSet[str]:
    """All words as a frozenset, for fast membership tests."""
    return frozenset(words())


def is_word(word: str) -> bool:
    """True if `word` (no niqqud) is in the list."""
    return word.strip() in word_set()


def starting_with(prefix: str) -> List[str]:
    """Words that start with `prefix`."""
    return [w for w in words() if w.startswith(prefix)]


def of_length(n: int) -> List[str]:
    """Words with exactly `n` letters (e.g. 5 for a Hebrew Wordle)."""
    return [w for w in words() if len(w) == n]


def random_words(k: int = 1, seed: Optional[int] = None) -> List[str]:
    """`k` random words."""
    return _random.Random(seed).sample(words(), k)
