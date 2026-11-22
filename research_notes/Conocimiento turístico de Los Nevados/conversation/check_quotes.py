"""Verify that every quote in conversation/evidence/quotes.md appears verbatim in its raw file.

Each `Archivo: `path``  line sets the raw file (relative to the notes root) for the quotes
that follow it. Every «...» quote on later lines must occur in that file after collapsing
whitespace (line breaks, NBSP). Exit status 1 when any quote is missing or has no file.
"""

import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
QUOTES = HERE / "evidence" / "quotes.md"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")


def normalize(text):
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text)


def main():
    current = None
    checked, failures = 0, []
    corpus = {}
    for number, line in enumerate(QUOTES.read_text(encoding="utf-8").splitlines(), 1):
        match = ARCHIVO.search(line)
        if match:
            current = match.group(1)
            if current not in corpus:
                path = NOTES / current
                if not path.is_file():
                    failures.append((number, current, "", "raw file does not exist"))
                    corpus[current] = None
                else:
                    try:
                        corpus[current] = normalize(path.read_text(encoding="utf-8", errors="strict"))
                    except UnicodeDecodeError:
                        corpus[current] = normalize(path.read_text(encoding="cp1252", errors="replace"))
        for quote in QUOTE.findall(line):
            checked += 1
            if current is None:
                failures.append((number, "", quote, "quote before any Archivo line"))
                continue
            text = corpus.get(current)
            if text is None:
                failures.append((number, current, quote, "raw file missing"))
            elif normalize(quote) not in text:
                failures.append((number, current, quote, "not found verbatim"))
    for number, archivo, quote, reason in failures:
        print(f"FAIL line {number} [{archivo}] {reason}: «{quote}»")
    print(f"quotes checked: {checked}; failures: {len(failures)}")
    return 1 if failures or checked == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
