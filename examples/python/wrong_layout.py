"""Fix text typed with the wrong keyboard layout ("akuo" -> "שלום").

    python3 wrong_layout.py "akuo nv akunl"

Maps each character through the standard Israeli keyboard layout (SI-1452)
and accepts the conversion only when most resulting tokens are real Hebrew
words - the word list is what makes this reliable instead of guessy.
Useful for search boxes, chat apps and form inputs.
"""

from __future__ import annotations

import sys

from hebrew_words import is_word

EN = "qwertyuiopasdfghjkl;'zxcvbnm,./"
HE = "/'קראטוןםפשדגכעיחלךף,זסבהנמצתץ."
EN_TO_HE = str.maketrans(EN, HE)
HE_TO_EN = str.maketrans(HE, EN)


def to_hebrew(text: str) -> str:
    return text.lower().translate(EN_TO_HE)


def fix(text: str, threshold: float = 0.6) -> str | None:
    """Return the Hebrew conversion if it looks right, else None."""
    converted = to_hebrew(text)
    tokens = [t.strip(".,/'") for t in converted.split()]
    tokens = [t for t in tokens if t]
    if not tokens:
        return None
    hits = sum(is_word(t) for t in tokens)
    return converted if hits / len(tokens) >= threshold else None


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "akuo nv akunl"
    print(fix(text) or "(looks like real English - left as is)")
