#!/usr/bin/env python3
"""Refresh the word count everywhere it is written in prose, after build.py.

    python3 scripts/build.py && python3 scripts/update_counts.py

Rounds the total DOWN to the nearest thousand for "N,000+" / "Nk+" phrases,
writes the exact number where an exact number is shown, updates the
Hugging Face size category, and regenerates docs/social-preview.png
(needs Pillow; skipped if unavailable).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "README.md", "llms.txt", "docs/llms.txt", "hf/README.md", "docs/index.html",
    "docs/USE_CASES.md", "docs/USE_CASES.en.md", "CITATION.cff",
    "packages/python/README.md", "packages/python/pyproject.toml",
    "packages/npm/README.md", "packages/npm/package.json",
]


def main() -> None:
    total = json.loads((ROOT / "data" / "stats.json").read_text(encoding="utf-8"))["total_words"]
    k = total // 1000
    subs = [
        (re.compile(r"\b\d{2,3},000\+"), f"{k:,},000+".replace(",000,000", ",000")),
        (re.compile(r"\b\d{2,3}k\+"), f"{k}k+"),
        (re.compile(r"\b\d{2,3}000\+"), f"{k}000+"),
        (re.compile(r"more than \d{2,3},000 "), f"more than {k},000 "),
        (re.compile(r"(?<=# )\d{5,7}(?= True)"), str(total)),
        (re.compile(r"(?<=<b class=\"count\" id=\"count\">)[\d,]+\+?"), f"{k},000+"),
    ]
    size_cat = "10K<n<100K" if total < 100_000 else "100K<n<1M"
    changed = []
    for rel in FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        new = s
        for pat, rep in subs:
            new = pat.sub(rep, new)
        if rel == "hf/README.md":
            new = re.sub(r"- (10K<n<100K|100K<n<1M)", f"- {size_cat}", new)
        if new != s:
            p.write_text(new, encoding="utf-8")
            changed.append(rel)
    print(f"total={total} -> '{k},000+'; updated: {', '.join(changed) or 'nothing'}")
    try:
        make_social_preview(total)
        print("regenerated docs/social-preview.png")
    except ImportError:
        print("Pillow not installed; social preview not regenerated")


def make_social_preview(total: int) -> None:
    import random

    from PIL import Image, ImageDraw, ImageFont, features

    raqm = features.check("raqm")
    W, H = 1280, 640
    img = Image.new("RGB", (W, H), "#0b1a4a")
    d = ImageDraw.Draw(img)
    words = (ROOT / "data" / "words.txt").read_text(encoding="utf-8").split()
    font_dir = "/usr/share/fonts/truetype/dejavu/"
    small = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 22)
    heb = (lambda s: s) if raqm else (lambda s: s[::-1])
    rnd = random.Random(3)
    for y in range(10, H, 34):
        x = W - 10
        while x > 0:
            w = heb(rnd.choice(words))
            tw = d.textlength(w, font=small)
            d.text((x - tw, y), w, font=small, fill="#16286a")
            x -= tw + 24
    d.rounded_rectangle((90, 120, 1190, 520), radius=36, fill="#0b1a4a", outline="#2c4bb8", width=3)
    big = ImageFont.truetype(font_dir + "DejaVuSans-Bold.ttf", 96)
    mid = ImageFont.truetype(font_dir + "DejaVuSans-Bold.ttf", 54)
    en = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 40)

    def ctext(y, s, f, fill):
        d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill)

    ctext(160, heb("מאגר מילים בעברית"), big, "#ffffff")
    ctext(290, f"{total:,} Hebrew words · CC0", mid, "#8fb0ff")
    ctext(380, "hebrew-words-db · TXT / JSON / CSV", en, "#c9d4f5")
    ctext(440, "public domain · free for any use", en, "#c9d4f5")
    img.save(ROOT / "docs" / "social-preview.png", optimize=True)


if __name__ == "__main__":
    main()
