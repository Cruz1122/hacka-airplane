#!/usr/bin/env python3
"""Verify that every verbatim quote in evidence/quotes.md appears in the
referenced raw file under evidence/raw/.

Accent-, case- and whitespace-insensitive substring match so PDF/HTML
line-wrap differences do not cause false negatives, while any fabricated
or paraphrased quote fails immediately.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
QUOTES_MD = HERE / "evidence" / "quotes.md"
REPO_NOTES = HERE.parent


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main() -> int:
    text = QUOTES_MD.read_text(encoding="utf-8")
    current_file: pathlib.Path | None = None
    cache: dict[pathlib.Path, str] = {}
    checked = 0
    failed = 0

    for lineno, line in enumerate(text.splitlines(), 1):
        m_file = re.match(r"^\s*Archivo:\s*`([^`]+)`", line)
        if m_file:
            current_file = REPO_NOTES / m_file.group(1)
            if not current_file.exists():
                print(f"MISSING RAW FILE (line {lineno}): {current_file}")
                return 2
            if current_file not in cache:
                cache[current_file] = norm(
                    current_file.read_text(encoding="utf-8", errors="ignore")
                )
            continue

        for m_q in re.finditer(r"«([^»]+)»", line):
            quote = m_q.group(1)
            if current_file is None:
                print(f"QUOTE WITHOUT FILE (line {lineno}): {quote[:60]}")
                failed += 1
                continue
            checked += 1
            nq = norm(quote)
            if nq not in cache[current_file]:
                print(
                    f"FAIL line {lineno} in {current_file.name}:\n  quote: {quote}\n  norm : {nq}"
                )
                failed += 1

    print(f"Checked {checked} quotes across {len(cache)} raw files; failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
