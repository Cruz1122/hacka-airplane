#!/usr/bin/env python3
"""Verify every «...» quote in activities/evidence/quotes.md is a literal
substring of its referenced raw file under activities/evidence/raw/
(after whitespace normalization).

Usage: python3 "research_notes/Conocimiento turístico de Los Nevados/activities/check_quotes.py"
Exits 0 if all quotes match; non-zero otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
QUOTES_MD = HERE / "evidence" / "quotes.md"
SECTION_JSON = BASE.parents[1] / "data" / "knowledge" / "sections" / "activities.json"


def norm(s: str) -> str:
    s = s.replace("\u00a0", " ").replace("\u00ad", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def main() -> int:
    text = QUOTES_MD.read_text(encoding="utf-8")
    current_file: Path | None = None
    cache: dict[Path, str] = {}
    ok = 0
    bad = 0

    for lineno, line in enumerate(text.splitlines(), 1):
        m = re.search(r"Archivo(?:\s+de\s+texto)?:\s*`([^`]+)`", line)
        if m:
            current_file = BASE / m.group(1)
            continue
        for q in re.findall(r"«([^»]+)»", line):
            if current_file is None:
                print(f"L{lineno}: quote before any Archivo declaration: {q[:60]}")
                bad += 1
                continue
            if not current_file.exists():
                print(f"L{lineno}: missing raw file {current_file}")
                bad += 1
                continue
            if current_file not in cache:
                cache[current_file] = norm(
                    current_file.read_text(encoding="utf-8", errors="ignore")
                )
            nq = norm(q)
            if "[…]" in nq or "[...]" in nq:
                print(f"L{lineno}: ellipsis forbidden inside quote [{current_file.name}]: «{nq[:80]}»")
                bad += 1
                continue
            if nq in cache[current_file]:
                ok += 1
            else:
                print(f"L{lineno}: FAIL in {current_file.name}: «{nq[:100]}»")
                bad += 1

    missing: list[str] = []
    if SECTION_JSON.exists():
        entries = json.loads(SECTION_JSON.read_text(encoding="utf-8")).get("entries", [])
        missing = [entry["id"] for entry in entries if entry["id"] not in text]
        for entry_id in missing:
            print(f"NO QUOTE COVERAGE: {entry_id}")
    else:
        print(f"missing section json {SECTION_JSON}")
        missing = ["<section json>"]

    print(
        f"Checked {ok + bad} quotes across {len(cache)} raw files: {ok} OK, {bad} FAIL; "
        f"entries without a quote marker: {len(missing)}"
    )
    return 0 if bad == 0 and ok > 0 and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
