"""Verify the evidence of booking_fees before the coordinator runs.

Two checks, both must pass:

1. Quote check (original): every quote in evidence/quotes.md appears verbatim in
   its raw file (whitespace-normalized, accents and OCR errors included). The
   quote text must be copied from the raw file, never corrected by hand.
2. Entry check (round 2): every entry in entries.json names its supporting quotes
   in `quotes`; each id must exist in quotes.md; and every number written in
   `answer.short`, `answer.variants` or `answer.detail` must appear in the raw
   files behind those quotes. This mirrors the coordinator, which greps numbers
   and legal citations in raw files and removes entries that fail.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "evidence"
QUOTES = EVIDENCE / "quotes.md"
ENTRIES = HERE / "entries.json"

BLOCK = re.compile(r"^### (Q\d+)\b")
FILE = re.compile(r"^- Archivo: (.+)$")
CITE = re.compile(r"^- Cita: «(.+)»$")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def normalize(text):
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())


def parse(path):
    items, current, archivo = [], None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        block = BLOCK.match(line)
        if block:
            current, archivo = block.group(1), None
            continue
        if current is None:
            continue
        found = FILE.match(line)
        if found:
            archivo = found.group(1).strip()
            continue
        cited = CITE.match(line)
        if cited:
            items.append((current, archivo, cited.group(1)))
    return items


def load_raw(archivo, cache):
    if archivo not in cache:
        source = EVIDENCE / archivo
        cache[archivo] = normalize(source.read_bytes().decode("utf-8", errors="replace"))
    return cache[archivo]


def check_quotes(items, cache):
    failures = []
    for qid, archivo, quote in items:
        if archivo is None:
            failures.append((qid, "sin archivo", quote))
            continue
        if not (EVIDENCE / archivo).exists():
            failures.append((qid, f"archivo inexistente: {archivo}", quote))
            continue
        if normalize(quote) not in load_raw(archivo, cache):
            failures.append((qid, archivo, quote))
    for qid, where, quote in failures:
        print(f"FAIL {qid} [{where}]: {quote}")
    print(f"Quotes checked: {len(items)}; failed: {len(failures)}")
    return failures


def check_entries(items, cache):
    if not ENTRIES.exists():
        print("Entries check skipped: entries.json not found")
        return []
    by_quote = {qid: archivo for qid, archivo, _ in items}
    failures, checked = [], 0
    for entry in json.loads(ENTRIES.read_text(encoding="utf-8")):
        checked += 1
        eid = entry["id"]
        quotes = entry.get("quotes") or []
        if not quotes:
            failures.append((eid, "sin citas en entries.json"))
            continue
        missing = [q for q in quotes if q not in by_quote]
        if missing:
            failures.append((eid, f"citas inexistentes: {', '.join(missing)}"))
            continue
        archivos = {by_quote[q] for q in quotes if by_quote[q]}
        raw = " ".join(load_raw(a, cache) for a in archivos if (EVIDENCE / a).exists())
        answer = entry["answer"]
        texts = [answer.get("short", ""), *answer.get("variants", []), answer.get("detail", "")]
        for text in texts:
            for token in NUMBER.findall(text):
                if token.rstrip(".,") not in raw:
                    failures.append((eid, f"cifra «{token}» no aparece en las citas {sorted(quotes)}"))
    for eid, reason in failures:
        print(f"FAIL entry {eid}: {reason}")
    print(f"Entries checked: {checked}; failed: {len(failures)}")
    return failures


def main():
    items = parse(QUOTES)
    cache = {}
    quote_failures = check_quotes(items, cache)
    entry_failures = check_entries(items, cache)
    return 1 if quote_failures or entry_failures or not items else 0


if __name__ == "__main__":
    sys.exit(main())
