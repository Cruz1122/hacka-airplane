"""Verify the geography evidence record in evidence/quotes.md.

quotes.md is split into blocks by `## ` headings. Each block names one raw file with an
`Archivo:` line. Checks, all must pass:
1. Every «quote» in a block, tagged or not, occurs verbatim in that block's raw file
   (whitespace, NBSP and typographic apostrophes/quotes normalized).
2. Every tag `- [id, id] ...` names an entry of data/knowledge/sections/geography.json.
3. Every entry of that section is cited by at least one tagged quote.
4. Every number in an entry's answer (short, variants, detail, steps) occurs among the
   numbers of that entry's own tagged quotes. Numbers are compared after removing '.' and ','
   and leading zeros, so "61.388,24" matches "61388,24" and "1,8" matches "1.8".

Usage: python3 geography/check_quotes.py   (after build_from_snapshot.py and coordinator_fixes.py)
Exit status 1 on any failure.
"""

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parent.parent
QUOTES = HERE / "evidence" / "quotes.md"
SECTION = ROOT / "data" / "knowledge" / "sections" / "geography.json"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
TAGGED = re.compile(r"^- \[([^\]]+)\]\s*(.*)$")
QUOTE = re.compile(r"«([^»]+)»")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def normalize(text):
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    for old, new in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text)


def canonical_number(token):
    return token.replace(".", "").replace(",", "").lstrip("0") or "0"


def numbers_of(text):
    return {canonical_number(token) for token in NUMBER.findall(text)}


def answer_strings(answer):
    if isinstance(answer, str):
        yield answer
    elif isinstance(answer, dict):
        for value in answer.values():
            yield from answer_strings(value)
    elif isinstance(answer, list):
        for item in answer:
            yield from answer_strings(item)


def read_raw(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252", errors="replace")


def main():
    failures = []
    blocks, block = [], None  # lines before the first "## " heading are preamble, not evidence
    for line in QUOTES.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if block:
                blocks.append(block)
            block = [line]
        elif block is not None:
            block.append(line)
    if block:
        blocks.append(block)

    cited_quotes = defaultdict(int)
    entry_numbers = defaultdict(set)
    checked = 0
    for lines in blocks:
        archivos = [m.group(1) for line in lines for m in [ARCHIVO.search(line)] if m]
        if not archivos:
            if any(QUOTE.search(line) for line in lines):
                failures.append(f"block without Archivo line: {lines[0]}")
            continue
        raw_path = NOTES / archivos[0]
        if not raw_path.is_file():
            failures.append(f"raw file missing: {archivos[0]}")
            continue
        raw = normalize(read_raw(raw_path))
        for number, line in enumerate(lines, 1):
            tagged = TAGGED.match(line)
            ids = [i.strip() for i in tagged.group(1).split(",") if i.strip()] if tagged else []
            for quote in QUOTE.findall(line):
                checked += 1
                if normalize(quote) not in raw:
                    failures.append(f"not found verbatim in {archivos[0]}: «{quote}»")
                for entry_id in ids:
                    cited_quotes[entry_id] += 1
                    entry_numbers[entry_id] |= numbers_of(quote)

    section = json.loads(SECTION.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in section["entries"]}
    for entry_id in sorted(set(cited_quotes) - set(entries)):
        failures.append(f"tag names an id that is not in geography.json: {entry_id}")

    uncited = [entry_id for entry_id in entries if cited_quotes[entry_id] == 0]
    unsupported = []
    for entry_id, entry in entries.items():
        for text in answer_strings(entry["answer"]):
            for token in NUMBER.findall(text):
                if canonical_number(token) not in entry_numbers[entry_id]:
                    unsupported.append((entry_id, token))
    for entry_id in uncited:
        failures.append(f"entry without any tagged quote: {entry_id}")
    for entry_id, token in unsupported:
        failures.append(f"number not in the entry's own quotes: {entry_id}: {token}")

    for failure in failures:
        print(f"FAIL {failure}")
    print(f"quotes checked: {checked}; entries: {len(entries)}; uncited: {len(uncited)}; "
          f"unsupported numbers: {len(unsupported)}; failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
