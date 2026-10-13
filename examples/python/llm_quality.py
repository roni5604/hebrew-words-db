"""Cheap quality checks for Hebrew text from LLMs, OCR or speech-to-text.

    python3 llm_quality.py output.txt
    echo "שלום עולם ומחשבבב" | python3 llm_quality.py -

Reports the out-of-vocabulary (OOV) rate: the share of Hebrew tokens that are
not known words even after peeling clitic prefixes. A sudden jump in OOV rate
flags garbled OCR pages, hallucinated "words", broken transliteration or
tokenizer artifacts. Also usable as a filter for synthetic training data.

Optional: pass --tokenizer <hf-model> (needs `pip install transformers`) to
measure tokenizer fertility (tokens per Hebrew word) on the word list itself.
"""

from __future__ import annotations

import re
import sys

from hebrew_words import clean, is_word, words

HEBREW_TOKEN = re.compile(r"[א-ת֑-ׇ'\"]+")


def oov_report(text: str) -> dict:
    tokens = [clean(t) for t in HEBREW_TOKEN.findall(text)]
    tokens = [t for t in tokens if len(t) > 1]
    unknown = [t for t in tokens if not is_word(t)]
    return {
        "hebrew_tokens": len(tokens),
        "unknown": len(unknown),
        "oov_rate": round(len(unknown) / len(tokens), 3) if tokens else 0.0,
        "examples": sorted(set(unknown))[:15],
    }


def tokenizer_fertility(model: str, sample: int = 5000) -> float:
    from transformers import AutoTokenizer  # optional dependency

    tok = AutoTokenizer.from_pretrained(model)
    ws = words()[:: max(1, len(words()) // sample)]
    return sum(len(tok.tokenize(w)) for w in ws) / len(ws)


if __name__ == "__main__":
    if "--tokenizer" in sys.argv:
        model = sys.argv[sys.argv.index("--tokenizer") + 1]
        print(f"{model}: {tokenizer_fertility(model):.2f} tokens per Hebrew word")
        sys.exit()
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    print(oov_report(text))
