#!/usr/bin/env python3
"""Expand compact noun/adjective SPEC lines into all inflected forms.

One shared, reviewed generator, so contributors (human or AI) describe a
lemma once and never hand-roll suffix logic. Lessons from review rounds are
built in: nouns keep both nuns before -נו (שולחננו), bound stems are given
explicitly (ילדה -> ילדת-), plural possessives follow the plural type
(-ים -> -יו/-יהם, -ות -> -ותיו/-ותיהם), final letters are fixed
automatically, and nothing is invented for flags you didn't set.

    python3 scripts/paradigm.py specs.txt > candidates.txt
    python3 scripts/new_words.py candidates.txt -o raw/<batch>_raw.txt

SPEC FORMAT (one lemma per line, fields separated by "|", # = comment):

  N | lemma | plural | sg-stem | pl-stem | flags
      Noun. Every field after lemma may be empty ("-" or blank).
      plural   e.g. ילדים / ילדות / עיניים (write it in full)
      sg-stem  bound singular stem used for construct + possessives:
               ילד- (ילדי, ילדו), ילדת- (ילדתו), שולחנ- (שולחנו), ביתי? no:
               write it WITHOUT the trailing hyphen: ילד, ילדת, שולחנ, בית
               empty = no construct-singular/singular possessives.
      pl-stem  bound plural stem WITHOUT the ending:
               for -ים plurals give the stem before -י: ילד  (-> ילדי, ילדיו)
               for -ות plurals give the stem incl. -ות: ילדות (-> ילדותי, ילדותיו)
               empty = no construct-plural/plural possessives.
      flags    comma list:
               nosgposs  construct sg only, no singular possessives
               noplposs  construct pl only, no plural possessives
               poss3     possessives only in 3rd person (ו ה ם ן / יו יה יהם יהן)
               dual      plural is a dual (עיניים): pl-stem = עינ (-> עיני, עיניו)

      CAUTION — irregular singular possessives: masculine nouns ending in -ה
      (מקרה, שדה, מחנה) take -הו/-ך/-נו (מקרהו), not stem+suffix. For these
      leave sg-stem EMPTY and list the few real forms on a W line.
      Loanwords in -יה/-ציה: construct -יית only if really used; usually
      leave sg-stem empty.

  A | masc | fem | masc-pl | fem-pl | flags
      Adjective/participle. Write all four forms in full.
      flags: cpl  also emit masculine construct plural (גדולי)
             cfs  also emit feminine construct singular (given as fem with
                  final ה->ת, e.g. גדולה -> גדולת)

  W | word word word ...
      Plain extra words (adverbs, invariable words, irregular forms).

Examples:
  N | ילד | ילדים | ילד | ילד |
  N | ילדה | ילדות | ילדת | ילדות |
  N | שולחן | שולחנות | שולחנ | שולחנות |
  N | עין | עיניים | עינ | עינ | dual
  N | אחריות | - | אחריות | - |
  A | גדול | גדולה | גדולים | גדולות | cpl
  W | אולי לעולם פתאום
"""

from __future__ import annotations

import sys

FINAL = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}
UNFINAL = {v: k for k, v in FINAL.items()}

SG_SUFFIXES = ["י", "ך", "ו", "ה", "נו", "כם", "כן", "ם", "ן"]
SG_SUFFIXES_3 = ["ו", "ה", "ם", "ן"]
PL_SUFFIXES = ["יי", "יך", "ייך", "יו", "יה", "ינו", "יכם", "יכן", "יהם", "יהן"]
PL_SUFFIXES_3 = ["יו", "יה", "יהם", "יהן"]


def stem(s: str) -> str:
    """Normalize a bound stem: strip hyphens, turn a final letter into its base form."""
    s = s.strip().rstrip("-")
    if s and s[-1] in UNFINAL:
        s = s[:-1] + UNFINAL[s[-1]]
    return s


def fin(word: str) -> str:
    """Apply final-letter form to the last letter only."""
    if not word:
        return word
    body = "".join(UNFINAL.get(c, c) for c in word[:-1])
    last = FINAL.get(word[-1], word[-1])
    return body + last


def noun(fields: list[str]) -> list[str]:
    lemma, plural, sg, pl, flags = (fields + [""] * 5)[:5]
    flags = {f.strip() for f in flags.split(",") if f.strip()}
    out = [lemma]
    if plural and plural != "-":
        out.append(plural)
    sg = "" if sg in ("", "-") else stem(sg)
    pl = "" if pl in ("", "-") else stem(pl)
    poss3 = "poss3" in flags
    if sg:
        out.append(fin(sg))  # construct singular (= stem with final letter)
        if "nosgposs" not in flags:
            for suf in (SG_SUFFIXES_3 if poss3 else SG_SUFFIXES):
                out.append(fin(sg + suf))
    if pl:
        if pl.endswith("ות"):
            out.append(pl)  # construct plural of -ות plurals = same form
            base = pl
        else:
            out.append(pl + "י")  # construct plural / dual: ילדי, עיני
            base = pl
        if "noplposs" not in flags:
            for suf in (PL_SUFFIXES_3 if poss3 else PL_SUFFIXES):
                # stem ending in a consonantal yod (ביטוי, ציווי): the suffix's
                # first yod is written once: ביטוי+יי -> ביטויי, +ייך -> ביטוייך
                if base.endswith("י") and suf.startswith("יי"):
                    suf = suf[1:]
                out.append(fin(base + suf))
    return out


def adjective(fields: list[str]) -> list[str]:
    m, f, mp, fp, flags = (fields + [""] * 5)[:5]
    flags = {x.strip() for x in flags.split(",") if x.strip()}
    out = [x for x in (m, f, mp, fp) if x and x != "-"]
    if "cpl" in flags and mp.endswith("ים"):
        out.append(mp[:-1])  # גדולים -> גדולי
    if "cfs" in flags and f.endswith("ה"):
        out.append(f[:-1] + "ת")
    return out


def expand(line: str) -> list[str]:
    line = line.split("#", 1)[0].strip()
    if not line:
        return []
    parts = [p.strip() for p in line.split("|")]
    kind, rest = parts[0].upper(), parts[1:]
    if kind == "N":
        return noun(rest)
    if kind == "A":
        return adjective(rest)
    if kind == "W":
        return " ".join(rest).split()
    raise ValueError(f"unknown spec type {kind!r} in line: {line}")


def main() -> None:
    errors = 0
    for path in sys.argv[1:] or ["-"]:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        for n, line in enumerate(text.splitlines(), 1):
            try:
                for w in expand(line):
                    print(w)
            except Exception as e:  # report and continue
                errors += 1
                print(f"{path}:{n}: {e}", file=sys.stderr)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
