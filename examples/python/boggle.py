"""Hebrew Boggle solver: find every word on a 4x4 board with a prefix trie.

    python3 boggle.py "שלומ ביתר אהבה כלבנ"

This is the core of a Hebrew Boggle game such as WordboxGame ("מצא ת׳מילה").
Tiles use regular letters; words are matched with final letters folded.
"""

from __future__ import annotations

import sys

from hebrew_words import fold_finals, words

END = "$"


def build_trie(min_len: int = 3) -> dict:
    root: dict = {}
    for w in words():
        if len(w) < min_len:
            continue
        node = root
        for ch in fold_finals(w):
            node = node.setdefault(ch, {})
        node[END] = w
    return root


def solve(board: list[str], trie: dict) -> list[str]:
    n, m = len(board), len(board[0])
    found: set[str] = set()

    def dfs(r: int, c: int, node: dict, seen: set) -> None:
        ch = board[r][c]
        if ch not in node:
            return
        node = node[ch]
        if END in node:
            found.add(node[END])
        seen.add((r, c))
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < m and (rr, cc) not in seen:
                    dfs(rr, cc, node, seen)
        seen.discard((r, c))

    for r in range(n):
        for c in range(m):
            dfs(r, c, trie, set())
    return sorted(found, key=lambda w: (-len(w), w))


if __name__ == "__main__":
    rows = (sys.argv[1] if len(sys.argv) > 1 else "שלומ ביתר אהבה כלבנ").split()
    board = [fold_finals(r) for r in rows]
    result = solve(board, build_trie())
    print(len(result), "words:", " ".join(result[:40]))
