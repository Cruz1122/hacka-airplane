"""Search raw text files with whitespace normalized, printing context snippets.

Usage: python3 -I find_text.py <regex> <file> [<file> ...] [--ctx N] [--max M]
Line breaks and NBSP are collapsed first, so a phrase split across lines still matches.
"""

import re
import sys
import unicodedata
from pathlib import Path


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text)


def main(argv):
    ctx, maxhits, args = 150, 6, []
    i = 0
    while i < len(argv):
        if argv[i] == "--ctx":
            ctx = int(argv[i + 1]); i += 2; continue
        if argv[i] == "--max":
            maxhits = int(argv[i + 1]); i += 2; continue
        args.append(argv[i]); i += 1
    pattern, files = re.compile(args[0], re.IGNORECASE), args[1:]
    for name in files:
        text = normalize(Path(name).read_text(encoding="utf-8", errors="replace"))
        hits = list(pattern.finditer(text))
        if not hits:
            continue
        print(f"== {Path(name).name}: {len(hits)} hit(s)")
        for m in hits[:maxhits]:
            s, e = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
            print("   ...", text[s:e], "...")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
