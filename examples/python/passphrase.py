"""Hebrew passphrase generator (Diceware-style) + password blocklist builder.

    python3 passphrase.py            # e.g. "כיסא-ענן-מגדל-שוקולד"
    python3 passphrase.py --blocklist blocklist.txt

Passphrases use `secrets` (cryptographically secure). The pool follows the
selection rules proposed for a Hebrew BIP39 list: 4-8 letters, no clitic
prefix letter at the start, and unique by the first 4 letters.

The blocklist contains every word BOTH in Hebrew and as it would be typed on
an English keyboard (שלום -> akuo), because attackers try both forms.
"""

from __future__ import annotations

import math
import secrets
import sys

from hebrew_words import PREFIX_LETTERS, words
from wrong_layout import HE_TO_EN


def pool() -> list[str]:
    seen: set[str] = set()
    out = []
    for w in words():
        if 4 <= len(w) <= 8 and w[0] not in PREFIX_LETTERS and w[:4] not in seen:
            seen.add(w[:4])
            out.append(w)
    return out


def passphrase(n_words: int = 4, sep: str = "-") -> tuple[str, float]:
    p = pool()
    phrase = sep.join(secrets.choice(p) for _ in range(n_words))
    return phrase, n_words * math.log2(len(p))


def blocklist() -> list[str]:
    out = set()
    for w in words():
        if len(w) >= 4:
            out.add(w)
            out.add(w.translate(HE_TO_EN))
    return sorted(out)


if __name__ == "__main__":
    if "--blocklist" in sys.argv:
        path = sys.argv[-1] if sys.argv[-1] != "--blocklist" else "blocklist.txt"
        open(path, "w", encoding="utf-8").write("\n".join(blocklist()) + "\n")
        print("wrote", path)
    else:
        phrase, bits = passphrase()
        print(phrase, f"(~{bits:.0f} bits of entropy, pool of {len(pool())} words)")
