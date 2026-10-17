#!/usr/bin/env python3
"""Find which candidate words are NEW (not yet in the dataset), so contributors
don't waste effort on duplicates.

    # Which of these are missing?
    python3 scripts/new_words.py --check יש אין פער שלום

    # Filter a candidate file (one word per line, # comments allowed) and
    # write only valid, not-yet-included words to a raw batch file:
    python3 scripts/new_words.py candidates.txt -o raw/batch_topic_raw.txt \
        --header "Batch: topic description"

Checks against data/words.txt AND every existing raw/*_raw*.txt file (so
words waiting in another unbuilt batch also count as existing). Applies the
same normalization and validation as scripts/build.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build import _strip_geresh, is_valid_word  # noqa: E402

NIQQUD = re.compile(r"[֑-ׇ‎‏]")


def normalize(word: str) -> str:
    word = NIQQUD.sub("", word.strip())
    return _strip_geresh(word).strip(".,;:!? -")


def known_words(exclude: Path | None = None) -> set[str]:
    words = set((ROOT / "data" / "words.txt").read_text(encoding="utf-8").split())
    for p in (ROOT / "raw").glob("*_raw*.txt"):
        if exclude and p.resolve() == exclude.resolve():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                words.add(normalize(line))
    return words


def read_candidates(paths: list[str]) -> list[str]:
    out = []
    for p in paths:
        text = sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.split("#", 1)[0]
            for tok in line.replace(",", " ").split():
                out.append(tok)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="candidate files ('-' for stdin)")
    ap.add_argument("--check", nargs="+", metavar="WORD", help="print which of these words are missing")
    ap.add_argument("-o", "--output", help="write new valid words here (a raw/*_raw.txt file)")
    ap.add_argument("--header", default="", help="comment header for the output file")
    args = ap.parse_args()

    out_path = Path(args.output) if args.output else None
    known = known_words(exclude=out_path)

    if args.check:
        missing = [w for w in (normalize(x) for x in args.check) if w and w not in known]
        print(" ".join(missing) if missing else "(all already in the dataset)")
        return

    seen: set[str] = set()
    new, dup, invalid = [], 0, []
    for raw in read_candidates(args.files):
        w = normalize(raw)
        if not w or w in seen:
            continue
        seen.add(w)
        if not is_valid_word(w):
            invalid.append(raw)
        elif w in known:
            dup += 1
        else:
            new.append(w)

    print(f"candidates: {len(seen)}  new: {len(new)}  already present: {dup}  invalid: {len(invalid)}",
          file=sys.stderr)
    if invalid:
        print("invalid (not written):", " ".join(invalid[:40]), file=sys.stderr)

    if out_path:
        header = "".join(f"# {h}\n" for h in args.header.splitlines() if h) if args.header else ""
        header += ("# Source: compiled from general knowledge of Modern Hebrew (AI-assisted),\n"
                   "# filtered against the existing dataset by scripts/new_words.py.\n"
                   "# License: CC0 1.0 (public domain), see LICENSE.\n\n")
        existing = []
        if out_path.exists():
            existing = [l for l in out_path.read_text(encoding="utf-8").splitlines()
                        if l.strip() and not l.startswith("#")]
            header = "".join(l + "\n" for l in out_path.read_text(encoding="utf-8").splitlines()
                             if l.startswith("#")) + "\n"
        merged = sorted(set(existing) | set(new))
        out_path.write_text(header + "\n".join(merged) + "\n", encoding="utf-8")
        print(f"wrote {len(merged)} words to {out_path}", file=sys.stderr)
    else:
        print("\n".join(new))


if __name__ == "__main__":
    main()
