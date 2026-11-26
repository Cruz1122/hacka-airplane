#!/usr/bin/env python3
"""Verify that every quote in evidence/quotes.md is a whitespace-normalized substring of its raw file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent / "evidence"
QUOTES = EVIDENCE / "quotes.md"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_quotes(text: str) -> list[dict[str, str]]:
    blocks = re.split(r"(?m)^### ", text)[1:]
    parsed = []
    for block in blocks:
        lines = block.splitlines()
        title = lines[0].strip()
        fields: dict[str, str] = {"title": title}
        quote_lines: list[str] = []
        in_quote = False
        for line in lines[1:]:
            if line.startswith("quote:"):
                in_quote = True
                quote_lines.append(line.split(":", 1)[1].strip())
                continue
            if in_quote:
                if line.startswith(" ") or line.startswith("\t"):
                    quote_lines.append(line.strip())
                    continue
                in_quote = False
            if ":" in line and not in_quote:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        fields["quote"] = " ".join(part for part in quote_lines if part)
        parsed.append(fields)
    return parsed


def main() -> int:
    records = parse_quotes(QUOTES.read_text(encoding="utf-8"))
    if not records:
        print("No quotes found")
        return 1
    failures = 0
    for record in records:
        rel = record.get("file", "")
        quote = record.get("quote", "")
        path = EVIDENCE / rel
        if not rel or not quote or not path.is_file():
            print(f"FAIL {record.get('title')}: missing file or quote ({rel})")
            failures += 1
            continue
        blob = normalize(path.read_text(encoding="utf-8", errors="replace"))
        if normalize(quote) not in blob:
            print(f"FAIL {record.get('title')}: quote not in {rel}")
            print(f"  {quote[:180]}")
            failures += 1
    print(f"Quotes: {len(records)}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
