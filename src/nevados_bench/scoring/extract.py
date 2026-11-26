"""Slot-extraction scoring and the type-aware value comparison shared with fc.py.

Comparison rules (catalog §3 "acierto por tipo" and §4 "acierto de extracción"):
- booleans: true/false, si/sí/yes/no and their string forms;
- numbers: int/float or numeric strings, Spanish thousands separators allowed ("4.137");
- times: any expression `values.extract_times` understands, compared as "HH:MM";
- dates: ISO "YYYY-MM-DD", "DD/MM/YYYY" or "DD-MM-YYYY", compared as ISO;
- lists: order-insensitive multiset of normalised items;
- null gold: prediction must be null, empty or "null"/"none";
- free text: `normalize_text`, punctuation dropped, "_" and "-" treated as spaces.
"""

from __future__ import annotations

import re
from typing import Any

from nevados_bench.schemas import Case, RequestRecord
from nevados_bench.values import extract_numbers, extract_times, normalize_text

_TIME_ONLY = re.compile(r"^\d{2}:\d{2}$")
_ISO_DATE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
_DMY_DATE = re.compile(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$")
_THOUSANDS = re.compile(r"^-?\d{1,3}(?:[.,]\d{3})+$")
_DECIMAL = re.compile(r"^-?\d+(?:[.,]\d+)?$")
_PUNCT = re.compile(r"[^\w\s:]")
_TRUE = {"true", "si", "yes", "verdadero", "1"}
_FALSE = {"false", "no", "falso", "0"}
_NULLS = {"", "null", "none", "n/a"}


def value_kind(gold: Any) -> str:
    """Comparison kind inferred from a gold value."""
    if gold is None:
        return "null"
    if isinstance(gold, bool):
        return "boolean"
    if isinstance(gold, int | float):
        return "number"
    if isinstance(gold, list | tuple):
        return "list"
    if isinstance(gold, str):
        if _TIME_ONLY.match(gold):
            return "time"
        if _ISO_DATE.match(gold):
            return "date"
    return "text"


def canonical_text(value: Any) -> str:
    text = normalize_text(str(value)).replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", _PUNCT.sub(" ", text)).strip()


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        # The corpus has no decimals (see values.py), so "4.137" is a thousands separator.
        if _THOUSANDS.match(stripped):
            return float(re.sub(r"[.,]", "", stripped))
        if _DECIMAL.match(stripped):
            return float(stripped.replace(",", "."))
        numbers = extract_numbers(stripped)
        if len(numbers) == 1:
            return float(next(iter(numbers)))
    return None


def _date(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if match := _ISO_DATE.match(text):
        y, m, d = match.groups()
    elif match := _DMY_DATE.match(text):
        d, m, y = match.groups()
    else:
        return None
    return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"


def is_null(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in _NULLS)


def values_match(pred: Any, gold: Any) -> bool:
    """Type-aware, normalised equality of a predicted value against the gold value."""
    kind = value_kind(gold)
    if kind == "null":
        return is_null(pred)
    if is_null(pred):
        return False
    if kind == "boolean":
        if isinstance(pred, bool):
            return pred == gold
        token = canonical_text(pred)
        return (token in _TRUE) if gold else (token in _FALSE)
    if kind == "number":
        number = _number(pred)
        return number is not None and abs(number - float(gold)) < 1e-9
    if kind == "time":
        times = extract_times(str(pred))
        return times == {gold}
    if kind == "date":
        return _date(pred) == _date(gold)
    if kind == "list":
        if not isinstance(pred, list | tuple):
            return False
        return sorted(canonical_text(v) for v in pred) == sorted(canonical_text(v) for v in gold)
    return canonical_text(pred) == canonical_text(gold)


def score_extract(record: RequestRecord, case: Case) -> dict[str, Any]:
    """Per-request flags for an `extract` call (one slot)."""
    parsed = record.parsed
    parse_ok = bool(parsed and parsed.parse_ok)
    pred = parsed.slot_value if parsed else None
    gold = case.gold.slot_value
    correct = parse_ok and values_match(pred, gold)
    return {
        "parse_ok": parse_ok,
        "slot_name": case.gold.slot_name or case.slot_name,
        "slot_kind": value_kind(gold),
        "slot_correct": correct,
        # Model supplied a value the user never gave (gold is null).
        "slot_fabricated": (parse_ok and not is_null(pred)) if gold is None else None,
        # Model returned null although the user gave the value.
        "slot_missed": (not parse_ok or is_null(pred)) if gold is not None else None,
        "output_tokens": record.completion.predicted_n,
        "correct": correct,
    }
