"""Hebrew spellchecker with "did you mean" suggestions (stdlib only).

    python3 spellcheck.py "שלומ עולמ, אני כותב מחשב חדשה"

Checks each token (after peeling clitic prefixes like ו/ה/ב/ל) and suggests
the closest known words by edit distance, treating final/regular letter
pairs (ם/מ, ן/נ ...) as identical.
"""

from __future__ import annotations

import sys
from collections import defaultdict

from hebrew_words import clean, fold_finals, is_word, words

ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"


def edits1(w: str) -> set[str]:
    splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits if b for c in ALPHABET]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def build_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for w in words():
        index[fold_finals(w)].append(w)
    return index


INDEX = build_index()


def suggest(token: str, limit: int = 5) -> list[str]:
    key = fold_finals(clean(token))
    if key in INDEX:  # only the final letter form was wrong (שלומ -> שלום)
        return INDEX[key][:limit]
    out: list[str] = []
    for cand in sorted(edits1(key)):
        out.extend(INDEX.get(cand, []))
        if len(out) >= limit:
            break
    return out[:limit]


def check(text: str) -> list[tuple[str, list[str]]]:
    tokens = [t.strip(".,!?;:()[]") for t in text.split()]
    return [(t, suggest(t)) for t in tokens if t and not is_word(t)]


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "שלומ עולמ, אני כותב בספר חדשש"
    for word, sugg in check(text):
        print(f"✗ {word} → {', '.join(sugg) or '(no suggestion)'}")
