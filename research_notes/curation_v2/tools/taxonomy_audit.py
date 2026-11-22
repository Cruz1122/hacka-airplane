#!/usr/bin/env python3
"""Audit section IDs, references, clarification slots, and example ownership."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SECTIONS = ROOT / "research_notes/curation_v2/snapshots/sections_before"
ID_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return " ".join(text.split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sections", type=Path, default=DEFAULT_SECTIONS,
                        help="Directory containing one JSON file per section")
    args = parser.parse_args()

    sections = {}
    errors = defaultdict(list)
    for path in sorted(args.sections.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors["unreadable_sections"].append({"file": path.name, "error": str(exc)})
            continue
        sections[path.stem] = data
        if data.get("id") != path.stem:
            errors["section_id_mismatch"].append({"file": path.name, "id": data.get("id")})

    entries = {}
    locations = defaultdict(list)
    examples = defaultdict(list)
    for section_id, section in sections.items():
        for entry in section.get("entries", []):
            eid = entry.get("id", "")
            locations[eid].append(section_id)
            if not ID_RE.fullmatch(eid) or not eid.startswith(section_id + "."):
                errors["invalid_entry_ids"].append({"id": eid, "section": section_id})
            entries.setdefault(eid, entry)
            for example in entry.get("examples", []):
                examples[norm(example)].append({"id": eid, "section": section_id,
                                                "text": example})

    for eid, owners in locations.items():
        if len(owners) > 1:
            errors["duplicate_ids"].append({"id": eid, "sections": owners})
    for text, owners in examples.items():
        owner_ids = sorted({owner["id"] for owner in owners})
        if len(owner_ids) > 1:
            errors["duplicate_examples"].append({"text": text, "entries": owner_ids})

    related_count = featured_count = hard_negative_count = need_count = 0
    section_stats = {}
    for section_id, section in sections.items():
        section_stats[section_id] = {
            "entry_count": len(section.get("entries", [])),
            "featured_count": len(section.get("featured", [])),
            "featured_ids": section.get("featured", []),
        }
        if len(section.get("featured", [])) > 5:
            errors["featured_over_limit"].append({
                "section": section_id,
                "count": len(section["featured"]),
                "limit": 5,
            })
        for eid in section.get("featured", []):
            featured_count += 1
            if eid not in entries:
                errors["unresolved_featured"].append({"section": section_id, "id": eid})
            if not eid.startswith(section_id + "."):
                errors["foreign_featured"].append({"section": section_id, "id": eid})
        for entry in section.get("entries", []):
            eid = entry.get("id", "")
            for target in entry.get("related", []):
                related_count += 1
                if target not in entries:
                    errors["unresolved_related"].append({"id": eid, "target": target})
            for negative in entry.get("hard_negatives", []):
                hard_negative_count += 1
                match = [owner for owner in examples.get(norm(negative), [])
                         if owner["id"] != eid]
                if not match:
                    errors["unmatched_hard_negatives"].append({"id": eid, "text": negative})
            for need in entry.get("needs", []):
                need_count += 1
                if need not in section.get("clarification", {}).get("slot_questions", {}):
                    errors["needs_without_slot_question"].append({"id": eid, "need": need})

    report = {
        "sections_dir": str(args.sections.resolve()),
        "section_count": len(sections),
        "entry_count": sum(len(s.get("entries", [])) for s in sections.values()),
        "global_unique_entry_ids": len(locations),
        "structural_counts": {
            "related_references": related_count,
            "featured_references": featured_count,
            "hard_negatives": hard_negative_count,
            "needs": need_count,
        },
        "sections": section_stats,
        "errors": dict(errors),
        "error_count": sum(map(len, errors.values())),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
