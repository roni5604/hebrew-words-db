#!/usr/bin/env python3
"""Remove reviewer-rejected words from a raw batch file.

    python3 scripts/apply_rejects.py raw/v2_topic_raw.txt rejects1.txt [rejects2.txt ...]

Comment lines and the header are kept; only rejected words are dropped.
"""

import sys
from pathlib import Path

raw = Path(sys.argv[1])
rejects = set()
for p in sys.argv[2:]:
    rejects |= {l.strip() for l in Path(p).read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.startswith("#")}
lines = raw.read_text(encoding="utf-8").splitlines()
kept = [l for l in lines if l.startswith("#") or l.strip() not in rejects]
removed = len(lines) - len(kept)
raw.write_text("\n".join(kept) + "\n", encoding="utf-8")
missing = len(rejects) - removed
print(f"{raw.name}: removed {removed} rejected words"
      + (f" ({missing} rejects were not in the file)" if missing else ""))
