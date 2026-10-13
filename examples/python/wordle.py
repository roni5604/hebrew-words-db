"""Hebrew Wordle helper: build answer/guess lists and play in the terminal.

    python3 wordle.py          # play one round
    python3 wordle.py --lists  # write guesses.txt / answers.txt

Hebrew-specific choices (the same ones the popular Hebrew Wordle clones made):
* Letters are compared in their regular form, so the keyboard has 22 keys
  and ם counts as מ. Words are shown with the correct final letter.
* ALL 5-letter words are accepted as guesses, but answers are drawn only
  from words that don't start with a clitic prefix letter, because answers
  like "והבית" feel unfair to players.
"""

from __future__ import annotations

import random
import sys

from hebrew_words import PREFIX_LETTERS, clean, fold_finals, words

LENGTH = 5


def guess_list() -> list[str]:
    return [w for w in words() if len(w) == LENGTH]


def answer_list() -> list[str]:
    return [w for w in guess_list() if w[0] not in PREFIX_LETTERS]


def score(guess: str, answer: str) -> str:
    """🟩 right place, 🟨 elsewhere in the word, ⬜ not in the word."""
    g, a = fold_finals(guess), fold_finals(answer)
    result = ["⬜"] * LENGTH
    remaining = list(a)
    for i, ch in enumerate(g):
        if a[i] == ch:
            result[i] = "🟩"
            remaining.remove(ch)
    for i, ch in enumerate(g):
        if result[i] == "⬜" and ch in remaining:
            result[i] = "🟨"
            remaining.remove(ch)
    return "".join(result)


def play() -> None:
    valid = {fold_finals(w) for w in guess_list()}
    answer = random.choice(answer_list())
    for turn in range(1, 7):
        guess = clean(input(f"ניחוש {turn}/6: "))
        if len(guess) != LENGTH or fold_finals(guess) not in valid:
            print("מילה לא מוכרת או לא באורך 5")
            continue
        print(guess, score(guess, answer))
        if fold_finals(guess) == fold_finals(answer):
            print("🎉 כל הכבוד!")
            return
    print("המילה הייתה:", answer)


if __name__ == "__main__":
    if "--lists" in sys.argv:
        open("guesses.txt", "w", encoding="utf-8").write("\n".join(guess_list()) + "\n")
        open("answers.txt", "w", encoding="utf-8").write("\n".join(answer_list()) + "\n")
        print(len(guess_list()), "guesses,", len(answer_list()), "answers")
    else:
        play()
