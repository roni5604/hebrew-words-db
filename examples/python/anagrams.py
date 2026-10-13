"""Hebrew anagram solver and "words from these letters" finder (Scrabble/Boggle helper).

    python3 anagrams.py שלום          # exact anagrams
    python3 anagrams.py --from רכבתשלו # every word you can build from these tiles

Final letters are folded, so ם and מ are the same tile (as in Hebrew Scrabble,
which has no separate final-letter tiles).
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict

from hebrew_words import clean, fold_finals, words


def key(word: str) -> str:
    return "".join(sorted(fold_finals(word)))


ANAGRAMS: dict[str, list[str]] = defaultdict(list)
for _w in words():
    ANAGRAMS[key(_w)].append(_w)


def anagrams(word: str) -> list[str]:
    word = clean(word)
    return [w for w in ANAGRAMS.get(key(word), []) if w != word]


def from_tiles(tiles: str, min_len: int = 2) -> list[str]:
    have = Counter(fold_finals(clean(tiles)))
    out = [w for w in words()
           if len(w) >= min_len and not Counter(fold_finals(w)) - have]
    return sorted(out, key=lambda w: (-len(w), w))


if __name__ == "__main__":
    args = sys.argv[1:] or ["שלום"]
    if args[0] == "--from":
        print(" ".join(from_tiles(args[1] if len(args) > 1 else "רכבתשלו")[:60]))
    else:
        print(" ".join(anagrams(args[0])) or "(none)")
