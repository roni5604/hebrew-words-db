"""Build a ready-to-ship SQLite database of Hebrew words (for mobile/desktop apps).

    python3 sqlite.py hebrew_words.db

Bundle the .db file with an Android / iOS / React Native / Flutter / Electron
app and query it offline. Includes a `key` column with final letters folded,
handy for word games where ם and מ are the same tile.
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from hebrew_words import fold_finals, words  # noqa: E402

path = sys.argv[1] if len(sys.argv) > 1 else "hebrew_words.db"
Path(path).unlink(missing_ok=True)
db = sqlite3.connect(path)
db.execute("CREATE TABLE words (word TEXT PRIMARY KEY, key TEXT NOT NULL, length INT NOT NULL) WITHOUT ROWID")
db.executemany("INSERT INTO words VALUES (?, ?, ?)", ((w, fold_finals(w), len(w)) for w in words()))
db.execute("CREATE INDEX words_key ON words(key)")
db.execute("CREATE INDEX words_length ON words(length)")
db.commit()
n = db.execute("SELECT count(*) FROM words").fetchone()[0]
print(f"{path}: {n} words, {Path(path).stat().st_size // 1024} KB")
