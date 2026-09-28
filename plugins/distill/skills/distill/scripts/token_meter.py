#!/usr/bin/env python3
"""Estimate tokens in texts and compare savings.

Usage:
  token_meter.py before.txt after.txt   # compare two files (after vs before)
  token_meter.py --text "some reply"    # count one string
  token_meter.py a.md b.md c.md         # table for 3+ files (first = baseline)
  cat reply.txt | token_meter.py -      # read stdin

Uses tiktoken (cl100k_base) as a proxy tokenizer if installed; otherwise a
regex heuristic that tracks BPE counts within ~10% for English prose and code.
"""

import math
import re
import sys

try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")

    def count(text):
        return len(_ENC.encode(text))

    METHOD = "tiktoken cl100k_base"
except Exception:
    _PIECE = re.compile(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]|\s+")

    def count(text):
        n = 0
        for p in _PIECE.findall(text):
            if p.isspace():
                n += p.count("\n") // 2  # blank lines cost a little
            elif p.isalpha():
                n += 1 if len(p) <= 6 else math.ceil(len(p) / 5)
            elif p.isdigit():
                n += math.ceil(len(p) / 3)
            else:
                n += 1
        return n

    METHOD = "heuristic (install tiktoken for exact counts)"


def read(src):
    if src == "-":
        return sys.stdin.read()
    with open(src, encoding="utf-8", errors="replace") as f:
        return f.read()


def stats(text):
    return count(text), len(text.split()), len(text)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--text":
        t, w, c = stats(" ".join(argv[1:]))
        print(f"tokens={t} words={w} chars={c}  [{METHOD}]")
        return 0

    rows = [(p, *stats(read(p))) for p in argv]
    base = rows[0][1] or 1
    width = max(len(r[0]) for r in rows)
    print(f"{'file'.ljust(width)}  tokens  words   chars  vs_first")
    for p, t, w, c in rows:
        delta = "baseline" if p == rows[0][0] else f"{(base - t) / base:+.0%} saved"
        print(f"{p.ljust(width)}  {t:6}  {w:5}  {c:6}  {delta}")
    if len(rows) == 2:
        t0, t1 = rows[0][1], rows[1][1]
        ratio = t0 / t1 if t1 else float("inf")
        print(f"\nsaved {t0 - t1} tokens ({(t0 - t1) / (t0 or 1):.0%}), {ratio:.1f}x smaller")
    print(f"[{METHOD}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
