"""Verify that every quote in access/evidence/quotes.md appears verbatim in its raw file.

Each `Archivo: `path`` line sets the raw file (relative to the notes root) for the quotes
that follow it. Every «...» quote on later lines must occur in that file after collapsing
whitespace. Every entry id produced by the snapshot overlay must be named in quotes.md.
Exit status 1 when any quote is missing, has no file, or an entry has no citation.
"""

import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
QUOTES = HERE / "evidence" / "quotes.md"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")
ENTRY_ID = re.compile(r"access\.[a-z0-9_]+")


def normalize(text):
    text = unicodedata.normalize("NFC", text).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text)


def covered_ids():
    data = json.loads((HERE / "source" / "access.v1.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("access_overlay", HERE / "source" / "overlay.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = module.apply(data)
    return {entry["id"] for entry in data["entries"]}


def main():
    current = None
    checked, failures = 0, []
    corpus = {}
    text = QUOTES.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
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
            haystack = corpus.get(current)
            if haystack is None:
                failures.append((number, current, quote, "raw file missing"))
            elif normalize(quote) not in haystack:
                failures.append((number, current, quote, "not found verbatim"))
    named = set(ENTRY_ID.findall(text))
    missing = sorted(covered_ids() - named)
    for entry_id in missing:
        failures.append((0, "", entry_id, "entry id not covered"))
    for number, archivo, quote, reason in failures:
        print(f"FAIL line {number} [{archivo}] {reason}: «{quote}»")
    print(f"quotes checked: {checked}; failures: {len(failures)}")
    return 1 if failures or checked == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
