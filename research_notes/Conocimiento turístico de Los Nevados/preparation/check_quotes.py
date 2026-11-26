"""Verify the evidence of the `preparation` section against its raw files.

Checks, in order:
1. Every entry of data/knowledge/sections/preparation.json has exactly one block in
   preparation/evidence/quotes.md, and no block refers to an id that is not published.
2. Every «quote» in a block occurs verbatim in the raw file named by the nearest `Archivo:` line
   (whitespace and NBSP normalized).
3. Every digit token in an answer (short, variants, detail) occurs in the raw files that the
   entry's block cites.
4. Every answer.short is at most 320 characters.
5. No block is marked «Consejo general»: every entry must cite a raw file that states its advice.

Exit status 1 when any check fails. Paths are resolved from this file, not from the cwd.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
BASE = NOTES.parent.parent
QUOTES = HERE / "evidence" / "quotes.md"
SECTION = BASE / "data" / "knowledge" / "sections" / "preparation.json"

BLOCK = re.compile(r"^###\s+`([^`]+)`")
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")
GENERAL = "Consejo general"  # forbidden marker: a general-advice block is a false attribution
DIGITS = re.compile(r"\d+(?:[.,]\d+)*")
SHORT_LIMIT = 320


def normalize(text):
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text)


def load_raw(relative):
    path = NOTES / relative
    if not path.is_file():
        return None
    try:
        return normalize(path.read_text(encoding="utf-8", errors="strict"))
    except UnicodeDecodeError:
        return normalize(path.read_text(encoding="cp1252", errors="replace"))


def parse_blocks():
    blocks, current = {}, None
    for number, line in enumerate(QUOTES.read_text(encoding="utf-8").splitlines(), 1):
        header = BLOCK.match(line)
        if header:
            entry_id = header.group(1)
            if entry_id in blocks:
                raise SystemExit(f"duplicate block for {entry_id} at line {number}")
            current = blocks[entry_id] = {"line": number, "files": [], "quotes": [], "file": None}
            continue
        if current is None:
            continue
        match = ARCHIVO.search(line)
        if match:
            current["file"] = match.group(1)
            if current["file"] not in current["files"]:
                current["files"].append(current["file"])
        for quote in QUOTE.findall(line):
            current["quotes"].append((number, current["file"], quote))
    return blocks


def answer_texts(answer):
    yield answer.get("short", "")
    for variant in answer.get("variants") or []:
        yield variant
    if answer.get("detail"):
        yield answer["detail"]
    if answer.get("reflection"):
        yield answer["reflection"]


def main():
    failures = []
    entries = json.loads(SECTION.read_text(encoding="utf-8"))["entries"]
    published = {e["id"]: e for e in entries}
    blocks = parse_blocks()
    corpus = {}

    for entry_id in published:
        if entry_id not in blocks:
            failures.append(f"{entry_id}: no block in quotes.md")
    for entry_id in blocks:
        if entry_id not in published:
            failures.append(f"{entry_id}: block in quotes.md for an id that is not published")

    checked_quotes = 0
    for entry_id, block in blocks.items():
        for number, archivo, quote in block["quotes"]:
            checked_quotes += 1
            if archivo is None:
                failures.append(f"line {number} {entry_id}: quote before any Archivo line")
                continue
            if archivo not in corpus:
                corpus[archivo] = load_raw(archivo)
            text = corpus[archivo]
            if text is None:
                failures.append(f"line {number} {entry_id}: raw file missing: {archivo}")
            elif normalize(quote) not in text:
                failures.append(f"line {number} {entry_id} [{archivo}]: not found verbatim: «{quote}»")

        if entry_id not in published:
            continue
        entry = published[entry_id]
        short = entry["answer"].get("short", "")
        if len(short) > SHORT_LIMIT:
            failures.append(f"{entry_id}: answer.short has {len(short)} characters (limit {SHORT_LIMIT})")

        tokens = set()
        for text in answer_texts(entry["answer"]):
            tokens.update(DIGITS.findall(text))
        if not block["quotes"]:
            failures.append(f"{entry_id}: block has no quotes")
            continue
        for archivo in block["files"]:
            if archivo not in corpus:
                corpus[archivo] = load_raw(archivo)
        cited = " ".join(corpus[f] or "" for f in block["files"])
        for token in sorted(tokens):
            if token not in cited:
                failures.append(f"{entry_id}: digit «{token}» not found in cited files {block['files']}")

    if GENERAL in QUOTES.read_text(encoding="utf-8"):
        failures.append(f"quotes.md still contains the forbidden marker «{GENERAL}»")

    for failure in failures:
        print(f"FAIL {failure}")
    print(f"entries: {len(published)}; blocks: {len(blocks)}; quotes checked: {checked_quotes}; failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
