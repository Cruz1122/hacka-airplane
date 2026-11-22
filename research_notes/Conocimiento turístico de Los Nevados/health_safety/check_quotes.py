"""Verify that every QUOTE in evidence/quotes.md appears verbatim (whitespace-normalized) in its raw file."""

from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUOTES_MD = HERE / "evidence" / "quotes.md"
RAW_DIR = HERE / "evidence" / "raw"


def norm_ws(text: str) -> str:
    return " ".join(text.split())


def raw_variants(raw_path: Path) -> list[str]:
    content = raw_path.read_text(encoding="utf-8", errors="ignore")
    variants = [norm_ws(content), norm_ws(unescape(content))]
    stripped = re.sub(r"<[^>]+>", " ", content)
    variants.append(norm_ws(stripped))
    variants.append(norm_ws(unescape(stripped)))
    return variants


def main() -> int:
    if not QUOTES_MD.exists():
        print(f"ERROR: missing {QUOTES_MD}", file=sys.stderr)
        return 1

    lines = QUOTES_MD.read_text(encoding="utf-8").splitlines()
    current_raw: Path | None = None
    checked = 0
    failures = 0

    for line_no, line in enumerate(lines, 1):
        raw_match = re.search(r"\*\*Raw file:\*\*\s*`([^`]+)`", line)
        if raw_match:
            current_raw = RAW_DIR / raw_match.group(1)
            continue

        quote_match = re.search(r"QUOTE:\s*`([^`]+)`", line)
        if quote_match:
            quote = norm_ws(quote_match.group(1))
            checked += 1
            if current_raw is None or not current_raw.exists():
                print(f"FAIL line {line_no}: raw file missing ({current_raw}) for quote: {quote!r}")
                failures += 1
                continue
            haystacks = raw_variants(current_raw)
            if not any(quote in h or norm_ws(unescape(quote)) in h for h in haystacks):
                print(f"FAIL line {line_no} in {current_raw.name}: quote not found verbatim: {quote!r}")
                failures += 1

    if checked == 0:
        print("FAIL: 0 quotes found in quotes.md")
        return 1

    if failures:
        print(f"check_quotes FAILED: {failures}/{checked} quotes missing from raw files.")
        return 1

    print(f"check_quotes OK: {checked}/{checked} verbatim quotes verified across raw files in {RAW_DIR.name}/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
