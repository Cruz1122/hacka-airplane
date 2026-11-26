#!/usr/bin/env python3
"""Check label proposals in findings/labels.json against the corpus before apply.

Usage (from any directory):
    python3 research_notes/curation_v2/tools/label_check.py [--proposals PATH]

Exits 0 when "fail" is empty, 1 otherwise. Prints one JSON object.

Checks:
  - keys, ids, and current_label match the snapshot exactly
  - proposed_label differs from current_label and has 3-8 words
  - no exact or accent-folded duplicate among all labels after applying every
    proposal (so the result is unique across the whole corpus)
  - contrast_with ids exist and do not contain the entry itself
  - near duplicates (difflib ratio >= 0.85) are reported as "warn_near" for review
  - every confusable pair with a_examples_to_b + b_examples_to_a >= 4 is counted
    as relabelled (one endpoint in the proposals) or kept (neither endpoint)
"""

from __future__ import annotations

import argparse
import csv
import difflib
import glob
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CURATION = ROOT / "research_notes" / "curation_v2"
SNAPSHOTS = CURATION / "snapshots" / "sections_before"
PAIRS = CURATION / "audit" / "inventory_before" / "confusable_pairs.csv"
DEFAULT_PROPOSALS = CURATION / "findings" / "labels.json"

KEYS = {"id", "current_label", "proposed_label", "contrast_with", "reason"}
NEAR_THRESHOLD = 0.85
MIN_WORDS, MAX_WORDS = 3, 8
PAIR_MIN = 4


def fold(text: str) -> str:
    """Lowercase, strip accents and punctuation, collapse whitespace."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    no_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    no_punct = re.sub(r"[^\w\s]", " ", no_accents)
    return " ".join(no_punct.split())


def load_corpus() -> dict[str, str]:
    labels: dict[str, str] = {}
    for path in sorted(glob.glob(str(SNAPSHOTS / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for entry in data["entries"]:
            if entry["id"] in labels:
                raise SystemExit(f"duplicate entry id in snapshots: {entry['id']}")
            labels[entry["id"]] = entry["label"]
    return labels


def qualifying_pairs() -> tuple[set[frozenset[str]], int]:
    pairs: dict[frozenset[str], int] = {}
    with PAIRS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = frozenset((row["a"], row["b"]))
            total = int(row["a_examples_to_b"]) + int(row["b_examples_to_a"])
            pairs[key] = total  # both directions carry the same totals
    qualifying = {key for key, total in pairs.items() if total >= PAIR_MIN}
    return qualifying, len(pairs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposals", type=Path, default=DEFAULT_PROPOSALS)
    args = parser.parse_args()

    corpus = load_corpus()
    proposals = json.loads(args.proposals.read_text(encoding="utf-8"))
    fail: list[str] = []
    warn_near: list[dict] = []

    seen_ids: set[str] = set()
    for index, item in enumerate(proposals):
        where = f"#{index} {item.get('id', '?')}"
        if set(item) != KEYS:
            fail.append(f"{where}: keys {sorted(item)} != {sorted(KEYS)}")
            continue
        entry_id = item["id"]
        if entry_id in seen_ids:
            fail.append(f"{where}: duplicate id in proposals")
        seen_ids.add(entry_id)
        if entry_id not in corpus:
            fail.append(f"{where}: id not in snapshots/sections_before")
            continue
        if item["current_label"] != corpus[entry_id]:
            fail.append(f"{where}: current_label does not match snapshot")
        proposed = item["proposed_label"].strip()
        if proposed == item["current_label"]:
            fail.append(f"{where}: proposed_label equals current_label")
        words = len(proposed.split())
        if not MIN_WORDS <= words <= MAX_WORDS:
            fail.append(f"{where}: {words} words, expected {MIN_WORDS}-{MAX_WORDS}")
        contrast = item["contrast_with"]
        if not contrast:
            fail.append(f"{where}: contrast_with is empty")
        for other in contrast:
            if other not in corpus:
                fail.append(f"{where}: contrast_with unknown id {other}")
            if other == entry_id:
                fail.append(f"{where}: contrast_with contains itself")
        if not item["reason"].strip():
            fail.append(f"{where}: empty reason")

    # Corpus after applying every proposal: labels must be unique.
    after = dict(corpus)
    for item in proposals:
        if item.get("id") in after:
            after[item["id"]] = item["proposed_label"].strip()
    by_folded: dict[str, list[str]] = {}
    for entry_id, label in after.items():
        by_folded.setdefault(fold(label), []).append(entry_id)
    for folded, ids in by_folded.items():
        if len(ids) > 1:
            fail.append(f"duplicate after apply ({folded!r}): {', '.join(sorted(ids))}")

    changed = {item["id"] for item in proposals if item.get("id") in corpus}
    for item in proposals:
        if item.get("id") not in corpus:
            continue
        proposed = fold(item["proposed_label"])
        for other_id, other_label in after.items():
            if other_id == item["id"]:
                continue
            ratio = difflib.SequenceMatcher(None, proposed, fold(other_label)).ratio()
            if ratio >= NEAR_THRESHOLD:
                warn_near.append({
                    "id": item["id"],
                    "proposed": item["proposed_label"],
                    "other_id": other_id,
                    "other_label": other_label,
                    "ratio": round(ratio, 2),
                })

    qualifying, total_pairs = qualifying_pairs()
    relabelled = [pair for pair in qualifying if pair & changed]
    kept = [pair for pair in qualifying if not pair & changed]
    missing_contrast = []
    for item in proposals:
        if item.get("id") not in corpus:
            continue
        for pair in qualifying:
            if item["id"] in pair:
                partner = next(iter(pair - {item["id"]}))
                if partner not in item["contrast_with"] and partner not in changed:
                    missing_contrast.append(f"{item['id']} <-> {partner}")

    result = {
        "proposals": len(proposals),
        "pairs_total_unordered": total_pairs,
        "pairs_qualifying": len(qualifying),
        "pairs_relabelled": len(relabelled),
        "pairs_kept": len(kept),
        "warn_near": warn_near,
        "warn_contrast_partner_not_listed": missing_contrast,
        "fail": fail,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
