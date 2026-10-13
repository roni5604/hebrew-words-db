"""Rough Hebrew rhyme finder (חרוזים) by shared word endings.

    python3 rhymes.py אהבה

Hebrew written without niqqud doesn't show vowels, so this is approximate:
it groups words that share their last N letters (final letters folded).
Good enough for songwriting helpers, kids' poetry games and greeting-card
generators; refine with a niqqud tool if you need exact pronunciation.
"""

from __future__ import annotations

import sys

from hebrew_words import clean, fold_finals, words


def rhymes(word: str, n: int = 3, limit: int = 40) -> list[str]:
    word = clean(word)
    end = fold_finals(word)[-n:]
    out = [w for w in words() if w != word and fold_finals(w).endswith(end)]
    return sorted(out, key=lambda w: (abs(len(w) - len(word)), w))[:limit]


if __name__ == "__main__":
    w = sys.argv[1] if len(sys.argv) > 1 else "אהבה"
    print(" ".join(rhymes(w)))
