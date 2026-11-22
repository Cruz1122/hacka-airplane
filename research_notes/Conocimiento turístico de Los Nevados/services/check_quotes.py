"""Verify the evidence behind every services entry.

Checks, in order:
1. Every «...» quote in evidence/quotes.md appears verbatim (whitespace-normalized) in the raw file
   named by the most recent `Archivo: `path`` line of its entry block. Paths are relative to the notes root.
2. Every entry of data/knowledge/sections/services.json (run after coordination/coordinator_fixes.py)
   has a `## services.<id>` block, and every block names an existing entry.
3. Each block has at least one raw file and either one quote or an explicit `- Sin dato:` line
   (an entry with no official figure states the search it made).
4. Every number (2+ digits) in an entry's `short` or `variants` appears in that entry's raw files.
   Numbers are written the way the raw file writes them (for example 4100, not 4.100).

Exit status 1 on any failure. The last line is the summary.
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
SECTION = ROOT / "data/knowledge/sections/services.json"
ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")
HEADING = re.compile(r"^##\s+(services\.\S+)\s*$")
SIN_DATO = re.compile(r"^-\s*Sin dato:")
NUMBER = re.compile(r"\d[\d.,]*")


def normalize(text):
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text)


def fold(text):
    text = unicodedata.normalize("NFKD", normalize(text).casefold())
    return "".join(c for c in text if not unicodedata.combining(c))


def numbers(text):
    found = set()
    for match in NUMBER.finditer(text):
        token = match.group(0).rstrip(".,")
        if len(re.sub(r"[.,]", "", token)) >= 2:
            found.add(token)
    return found


def read_raw(path):
    try:
        return normalize(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return normalize(path.read_text(encoding="cp1252", errors="replace"))


def parse_blocks(failures):
    blocks = {}
    current = None
    current_file = None
    for number, line in enumerate(QUOTES.read_text(encoding="utf-8").splitlines(), 1):
        heading = HEADING.match(line)
        if heading:
            current = heading.group(1)
            current_file = None
            if current in blocks:
                failures.append(f"line {number}: duplicate block {current}")
            blocks[current] = {"files": [], "quotes": [], "sin_dato": False, "texts": {}}
            continue
        if current is None:
            continue
        block = blocks[current]
        if SIN_DATO.match(line):
            block["sin_dato"] = True
        for match in ARCHIVO.finditer(line):
            current_file = match.group(1)
            if current_file not in block["files"]:
                block["files"].append(current_file)
                path = NOTES / current_file
                if not path.is_file():
                    failures.append(f"line {number} [{current}]: raw file does not exist: {current_file}")
                    block["texts"][current_file] = None
                else:
                    block["texts"][current_file] = read_raw(path)
        for quote in QUOTE.findall(line):
            if current_file is None:
                failures.append(f"line {number} [{current}]: quote before any Archivo line: «{quote}»")
                continue
            block["quotes"].append((number, current_file, quote))
            text = block["texts"].get(current_file)
            if text is None:
                failures.append(f"line {number} [{current}]: raw file missing for quote: «{quote}»")
            elif normalize(quote) not in text:
                failures.append(f"line {number} [{current}] {current_file}: not found verbatim: «{quote}»")
    return blocks


def main():
    failures = []
    blocks = parse_blocks(failures)
    entries = json.loads(SECTION.read_text(encoding="utf-8"))["entries"]
    ids = [entry["id"] for entry in entries]
    checked_quotes = sum(len(block["quotes"]) for block in blocks.values())
    checked_numbers = 0

    for entry_id in ids:
        block = blocks.get(entry_id)
        if block is None:
            failures.append(f"{entry_id}: no block in quotes.md")
            continue
        if not block["files"]:
            failures.append(f"{entry_id}: block names no raw file")
        if not block["quotes"] and not block["sin_dato"]:
            failures.append(f"{entry_id}: no quote and no `- Sin dato:` line")
        entry = next(e for e in entries if e["id"] == entry_id)
        answer_text = " ".join([entry["answer"]["short"], *entry["answer"].get("variants", [])])
        corpus = fold(" ".join(text for text in block["texts"].values() if text))
        for token in sorted(numbers(answer_text)):
            checked_numbers += 1
            if fold(token) not in corpus:
                failures.append(f"{entry_id}: number «{token}» in answer not found in its raw files")

    for block_id in blocks:
        if block_id not in ids:
            failures.append(f"{block_id}: block without an entry in services.json")

    for failure in failures:
        print(f"FAIL {failure}")
    print(
        f"quotes checked: {checked_quotes}; entries covered: {len(ids) - sum(1 for i in ids if i not in blocks)}/{len(ids)}; "
        f"numbers checked: {checked_numbers}; failures: {len(failures)}"
    )
    return 1 if failures or checked_quotes == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
