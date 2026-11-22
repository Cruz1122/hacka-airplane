"""Canonical value forms shared by the synthetic world (which states values) and the
scorers (which detect them in free model text).

Canonical forms:
- times        -> "HH:MM" 24h            ("6:40 a. m." -> "06:40", "6:15 pm" -> "18:15")
- quantities   -> digits only            ("4.137 m" -> "4137", "$38.500" -> "38500")
- named values -> normalize_text(value)  (lowercase, accents stripped, single spaces)

The corpus must avoid decimals and unit-convertible quantities so that a faithful
answer always contains the canonical form of the gold value.
"""

from __future__ import annotations

import re
import unicodedata

ABSTAIN_ES = "No tengo información oficial sobre eso."
ABSTAIN_EN = "I don't have official information about that."

_TIME_RE = re.compile(
    r"(?<!\d)(\d{1,2})\s*[:h]\s*(\d{2})(?!\d)\s*(a\.?\s?m\.?|p\.?\s?m\.?)?", re.IGNORECASE
)
_NUMBER_RE = re.compile(r"(?<![\w.,])\d{1,3}(?:[.,]\d{3})+(?!\d)|\d+")
# `[fuente: ID]` as instructed, or a bare bracketed passage id such as `[EST-C-15]`, which
# models often emit instead. Both must be removed before extracting values, otherwise the
# digits of the id are scored as a fabricated quantity.
_CITATION_RE = re.compile(
    r"\[\s*(?:fuente\s*:\s*([A-Za-z0-9_\-]+)|([A-Za-z]{2,}(?:-[A-Za-z0-9]+)*-\d+))\s*\]",
    re.IGNORECASE,
)
_ABSTAIN_PATTERNS = (
    "no tengo informacion oficial",
    "i don't have official information",
    "i do not have official information",
)


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace."""
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", stripped.replace("’", "'")).strip().lower()


def _canonical_time(hour: str, minute: str, meridiem: str | None) -> str | None:
    h, m = int(hour), int(minute)
    if meridiem:
        is_pm = meridiem.lower().startswith("p")
        if h == 12:
            h = 12 if is_pm else 0
        elif is_pm:
            h += 12
    if h > 23 or m > 59:
        return None
    return f"{h:02d}:{m:02d}"


def extract_times(text: str) -> set[str]:
    found = set()
    for match in _TIME_RE.finditer(text):
        canonical = _canonical_time(match.group(1), match.group(2), match.group(3))
        if canonical:
            found.add(canonical)
    return found


def extract_numbers(text: str) -> set[str]:
    """Digit-only quantities, with time expressions and citation IDs removed first."""
    cleaned = _CITATION_RE.sub(" ", text)
    cleaned = _TIME_RE.sub(" ", cleaned)
    return {re.sub(r"[.,]", "", match.group(0)) for match in _NUMBER_RE.finditer(cleaned)}


def extract_values(text: str) -> set[str]:
    """All canonical times and quantities mentioned in free text."""
    return extract_times(text) | extract_numbers(text)


def contains_named_value(text: str, value: str) -> bool:
    """Whole-phrase match of a named (non-numeric) canonical value in free text."""
    pattern = r"(?<!\w)" + re.escape(normalize_text(value)) + r"(?!\w)"
    return re.search(pattern, normalize_text(text)) is not None


def extract_citations(text: str) -> list[str]:
    return [(labelled or bare).upper() for labelled, bare in _CITATION_RE.findall(text)]


def is_abstention(text: str) -> bool:
    normalized = normalize_text(text)
    return any(pattern in normalized for pattern in _ABSTAIN_PATTERNS)
