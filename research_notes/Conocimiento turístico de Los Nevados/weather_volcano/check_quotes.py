"""Verify weather_volcano quotes and that every entry id is covered.

Each `Archivo: `path`` line sets the raw file (relative to the notes root) for the
quotes that follow it. Every «...» quote must occur in that file after collapsing
whitespace. Every entry id in the generated section JSON must appear in quotes.md.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parents[1]
QUOTES = HERE / "evidence" / "quotes.md"
SECTION = ROOT / "data" / "knowledge" / "sections" / "weather_volcano.json"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")


def normalize(text):
    text = unicodedata.normalize("NFC", text)
    # SharePoint inserts zero-width spaces inside words. They are not part of the sentence.
    for invisible in ("\u00a0", "\u200b", "\u200c", "\u200d", "\ufeff"):
        text = text.replace(invisible, " " if invisible == "\u00a0" else "")
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
    if not SECTION.is_file():
        failures.append((0, "", "", "section json missing; run the generator first"))
    else:
        body = QUOTES.read_text(encoding="utf-8")
        for item in json.loads(SECTION.read_text(encoding="utf-8"))["entries"]:
            if item["id"] not in body:
                failures.append((0, "quotes.md", item["id"], "entry id not covered"))
    for number, archivo, quote, reason in failures:
        print(f"FAIL line {number} [{archivo}] {reason}: «{quote}»")
    print(f"quotes checked: {checked}; failures: {len(failures)}")
    return 1 if failures or checked == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
