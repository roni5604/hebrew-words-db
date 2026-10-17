#!/usr/bin/env python3
"""Check candidate words against the dataset before adding them.

    python3 scripts/check_new.py candidates.txt [more.txt ...]
    python3 scripts/check_new.py candidates.txt --write-new out_raw.txt

Normalizes each line exactly like scripts/build.py (strips geresh/gershayim
and edge punctuation, skips blank and # lines), then reports:
  * invalid  - not plain Hebrew letters / final letter in the middle / length
  * existing - already in data/words.txt (or in raw/staging/*.txt if --staging)
  * new      - would actually grow the dataset
With --write-new, writes only the new, valid, deduplicated words (sorted) to
the given file, so no work is ever duplicated.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build import _strip_geresh, is_valid_word  # noqa: E402


def load_existing(include_staging: bool, exclude: set[Path]) -> set[str]:
    words = set((ROOT / "data" / "words.txt").read_text(encoding="utf-8").split())
    if include_staging:
        for p in (ROOT / "raw" / "staging").glob("*.txt"):
            if p.resolve() in exclude:
                continue
            words.update(p.read_text(encoding="utf-8").split())
    return words


def normalize(line: str) -> str:
    line = line.strip()
    if not line or line.startswith("#"):
        return ""
    return _strip_geresh(line).strip(".,;:!? ")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--write-new", metavar="OUT")
    ap.add_argument("--staging", action="store_true",
                    help="also treat words already in raw/staging/*.txt as existing")
    ap.add_argument("--show", type=int, default=15, help="examples to print")
    args = ap.parse_args()

    out = Path(args.write_new).resolve() if args.write_new else None
    existing = load_existing(args.staging, {out} if out else set())

    seen: set[str] = set()
    invalid: list[str] = []
    dup: list[str] = []
    new: list[str] = []
    for f in args.files:
        for raw in Path(f).read_text(encoding="utf-8").splitlines():
            w = normalize(raw)
            if not w or w in seen:
                continue
            seen.add(w)
            if not is_valid_word(w):
                invalid.append(w)
            elif w in existing:
                dup.append(w)
            else:
                new.append(w)

    print(f"candidates: {len(seen)}  new: {len(new)}  already-existing: {len(dup)}  invalid: {len(invalid)}")
    if invalid:
        print("invalid examples:", " ".join(invalid[: args.show]))
    if new:
        print("new examples:", " ".join(new[: args.show]))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        prev = set(out.read_text(encoding="utf-8").split()) if out.exists() else set()
        merged = sorted(prev | set(new))
        out.write_text("\n".join(merged) + "\n", encoding="utf-8")
        print(f"wrote {len(merged)} words to {out} (+{len(merged) - len(prev)})")


if __name__ == "__main__":
    main()
