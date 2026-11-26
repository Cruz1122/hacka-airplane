"""Verify every quote in evidence/quotes.md occurs in its raw file.

Whitespace is collapsed. Accents and case stay as published.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUOTES = HERE / "evidence" / "quotes.md"
EVIDENCE = HERE / "evidence"


def normalize(text: str) -> str:
    return " ".join(text.split())


def parse(markdown: str) -> list[dict[str, str]]:
    blocks = []
    current: dict[str, str] | None = None
    for line in markdown.splitlines():
        if line.startswith("## "):
            if current:
                blocks.append(current)
            current = {"id": line[3:].strip()}
            continue
        if current is None or not line.strip():
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if key in {"url", "retrieved", "file", "quote"}:
            current[key] = value.strip()
    if current:
        blocks.append(current)
    return blocks


def main() -> None:
    blocks = parse(QUOTES.read_text(encoding="utf-8"))
    if not blocks:
        raise SystemExit("quotes.md has no entries")
    failures = []
    for block in blocks:
        missing = [key for key in ("id", "url", "retrieved", "file", "quote") if not block.get(key)]
        if missing:
            failures.append(f"{block.get('id', '?')}: missing {missing}")
            continue
        path = EVIDENCE / block["file"]
        if not path.is_file():
            failures.append(f"{block['id']}: raw file not found: {path.name}")
            continue
        haystack = normalize(path.read_text(encoding="utf-8", errors="replace"))
        needle = normalize(block["quote"])
        if needle not in haystack:
            failures.append(f"{block['id']}: quote not in {block['file']}: {needle[:120]}")
    if failures:
        print(f"FAILED {len(failures)}")
        for item in failures:
            print(item)
        raise SystemExit(1)
    print(f"OK {len(blocks)} quotes")


if __name__ == "__main__":
    main()
