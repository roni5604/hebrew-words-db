#!/usr/bin/env python3
"""
Builds the final dictionary artifacts (data/words.txt, data/words.json,
data/by_letter/*.txt, data/stats.json) from every *_raw.txt file under
raw/.

Usage:
    python3 scripts/build.py
    python3 scripts/build.py --exclude "v2_pending_*"   # skip unreviewed batches

See CONTRIBUTING.md for how to add new words, and docs/SOURCES.md for
the methodology / licensing rationale behind this word list.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"
DATA_DIR = ROOT / "data"
BY_LETTER_DIR = DATA_DIR / "by_letter"

# Final (sofit) letters and their base form. We keep the CORRECT spelling
# (with final letters) in the canonical word list - this repo stores real,
# properly-spelled Hebrew words, not a game-normalized form.
FINAL_LETTERS = {"ך", "ם", "ן", "ף", "ץ"}
BASE_LETTERS = {"כ", "מ", "נ", "פ", "צ"}
HEBREW_LETTERS = BASE_LETTERS | FINAL_LETTERS | set("אבגדהוזחטילסעקרשת")

MIN_LEN = 1
MAX_LEN = 20


# Geresh/gershayim characters used to spell loanwords (ג'ינג'י, ז'קט) or
# abbreviations (חבל"ז). By decision of the repo owner, these words are kept
# but WITHOUT the geresh mark - e.g. "ג'וק" is stored as "גוק". This keeps
# the dictionary to plain, unaccented Hebrew letters only.
GERESH_CHARS = "'’\""


def _strip_geresh(word: str) -> str:
    for ch in GERESH_CHARS:
        word = word.replace(ch, "")
    return word


EXCLUDE: list[str] = []


def raw_files() -> list[Path]:
    files = sorted(RAW_DIR.glob("*_raw*.txt"))
    return [p for p in files if not any(p.match(pat) for pat in EXCLUDE)]


def iter_raw_lines():
    for path in raw_files():
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            stripped = _strip_geresh(stripped).strip(".,;:!? ")
            if not stripped:
                continue
            yield path.name, lineno, stripped


def is_valid_word(word: str) -> bool:
    if not (MIN_LEN <= len(word) <= MAX_LEN):
        return False
    if any(ch in FINAL_LETTERS for ch in word[:-1]):
        # A final letter must only appear as the LAST character of a word.
        return False
    return all(ch in HEBREW_LETTERS for ch in word)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--exclude", action="append", default=[],
                    help="glob of raw file names to skip (repeatable)")
    EXCLUDE.extend(ap.parse_args().exclude)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BY_LETTER_DIR.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    rejected: list[tuple[str, int, str]] = []

    for filename, lineno, word in iter_raw_lines():
        if is_valid_word(word):
            seen.add(word)
        else:
            rejected.append((filename, lineno, word))

    words = sorted(seen)

    (DATA_DIR / "words.txt").write_text(
        "\n".join(words) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "words.json").write_text(
        json.dumps(words, ensure_ascii=False, indent=None),
        encoding="utf-8",
    )
    # CSV with a header row: renders as a nice table in the Hugging Face /
    # Kaggle dataset viewers and loads directly with pandas.read_csv().
    (DATA_DIR / "words.csv").write_text(
        "word,length\n"
        + "".join(f"{w},{len(w)}\n" for w in words),
        encoding="utf-8",
    )

    # Split by first letter for easy browsing on GitHub.
    for existing in BY_LETTER_DIR.glob("*.txt"):
        existing.unlink()
    by_first_letter: dict[str, list[str]] = {}
    for word in words:
        by_first_letter.setdefault(word[0], []).append(word)
    for letter, letter_words in by_first_letter.items():
        (BY_LETTER_DIR / f"{letter}.txt").write_text(
            "\n".join(letter_words) + "\n", encoding="utf-8"
        )

    # Split by length (games: Wordle = 5 letters, crosswords, Boggle).
    by_length_dir = DATA_DIR / "by_length"
    by_length_dir.mkdir(parents=True, exist_ok=True)
    for existing in by_length_dir.glob("*.txt"):
        existing.unlink()
    by_len: dict[int, list[str]] = {}
    for word in words:
        by_len.setdefault(len(word), []).append(word)
    for n, len_words in by_len.items():
        (by_length_dir / f"{n:02d}.txt").write_text(
            "\n".join(len_words) + "\n", encoding="utf-8"
        )

    length_histogram = Counter(len(w) for w in words)
    stats = {
        "name": "hebrew-words-db",
        "description": "CC0 public-domain list of Hebrew words (incl. "
        "inflected forms). One word per line, no niqqud, no definitions.",
        "language": "he",
        "license": "CC0-1.0",
        "homepage": "https://github.com/roni5604/hebrew-words-db",
        "files": {
            "txt": "data/words.txt",
            "json": "data/words.json",
            "csv": "data/words.csv",
        },
        "total_words": len(words),
        "by_first_letter_count": {
            letter: len(letter_words)
            for letter, letter_words in sorted(by_first_letter.items())
        },
        "by_length_count": {
            str(length): count
            for length, count in sorted(length_histogram.items())
        },
        "raw_files_processed": sorted({p.name for p in raw_files()}),
        "rejected_line_count": len(rejected),
    }
    (DATA_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"✅ {len(words)} מילים ייחודיות נכתבו ל-{DATA_DIR / 'words.txt'}")
    print(f"✅ {len(by_first_letter)} קבצי אותיות נכתבו ל-{BY_LETTER_DIR}")
    if rejected:
        print(f"⚠️  {len(rejected)} שורות נדחו (לא עברית תקנית/אורך לא תקין):")
        for filename, lineno, word in rejected[:30]:
            print(f"   {filename}:{lineno}: {word!r}")
        if len(rejected) > 30:
            print(f"   ... ועוד {len(rejected) - 30} שורות נדחות")


if __name__ == "__main__":
    main()
