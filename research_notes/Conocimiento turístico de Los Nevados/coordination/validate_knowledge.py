"""Validate the delivered corpus without changing authored content."""

import json
import random
import re
import sys
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parent.parent
OFFICIAL = (
    "gov.co", "humboldt.org.co", "sibcolombia.net", "carder.gov.co",
    "corpocaldas.gov.co", "cortolima.gov.co",
    "cdc.gov", "medlineplus.gov", "who.int", "ramsar.org", "unesco.org",
    "iugs-geoheritage.org",
)


def normalized(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.findall(r"\w+", text))


def answer_texts(answer):
    for value in answer.values():
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield item
                elif isinstance(item, list):
                    yield from (text for text in item if isinstance(text, str))


def official(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith("." + domain) for domain in OFFICIAL)


def validate():
    assignments = json.loads((HERE / "assignments.json").read_text())
    schema = json.loads((NOTES / "inputs/knowledge-section.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors, warnings, sections, entries, samples = [], [], [], [], {}
    example_owners, normalized_owners = defaultdict(list), defaultdict(list)
    id_owners = defaultdict(list)
    for spec in assignments:
        section_id = spec["id"]
        path = ROOT / "data/knowledge/sections" / (section_id + ".json")
        if not path.exists():
            errors.append({"section": section_id, "rule": "missing_section"})
            continue
        try:
            data = json.loads(path.read_text())
        except (ValueError, OSError) as exc:
            errors.append({"section": section_id, "rule": "invalid_json", "detail": str(exc)})
            continue
        for issue in validator.iter_errors(data):
            errors.append({"section": section_id, "rule": "schema", "path": list(issue.path),
                           "detail": issue.message})
        for key in ("id", "order"):
            if data.get(key) != spec[key]:
                errors.append({"section": section_id, "rule": "section_" + key})
        if data.get("retrieval", {}).get("profile") != spec["profile"]:
            errors.append({"section": section_id, "rule": "profile"})
        clarification = data.get("clarification", {})
        slots = clarification.get("slot_questions", {})
        if not 4 <= len(clarification.get("bank", [])) <= 8:
            errors.append({"section": section_id, "rule": "clarification_count"})
        for entity in data.get("retrieval", {}).get("entity_filters", []):
            if entity not in slots:
                errors.append({"section": section_id, "rule": "entity_filter_slot", "entity": entity})
        current = data.get("entries", [])
        sections.append({"id": section_id, "target": spec["target"], "entries": len(current),
                         "examples": sum(len(e.get("examples", [])) for e in current)})
        samples[section_id] = [e["id"] for e in random.Random(20261121).sample(
            current, min(5, len(current)))]
        if not 3 <= len(data.get("featured", [])) <= 5:
            warnings.append({"section": section_id, "rule": "featured_count"})
        if not (NOTES / (section_id + ".research.md")).exists():
            errors.append({"section": section_id, "rule": "missing_research_log"})
        for entry in current:
            entry_id = entry.get("id", "")
            id_owners[entry_id].append(section_id)
            entries.append((section_id, entry, data))
            def fail(rule, **detail):
                errors.append({"id": entry_id, "rule": rule, **detail})
            if not entry_id.startswith(section_id + "."):
                fail("id_prefix")
            if not 3 <= len(entry.get("label", "").split()) <= 8:
                fail("label_words")
            if len(entry.get("examples", [])) < 12:
                fail("examples_minimum")
            if not 2 <= len(entry.get("hard_negatives", [])) <= 4:
                fail("hard_negatives_count")
            if not 1 <= len(entry.get("answer", {}).get("variants", [])) <= 2:
                fail("variants_count")
            if not 1 <= len(entry.get("related", [])) <= 3:
                fail("related_count")
            for need in entry.get("needs", []):
                if need not in slots:
                    fail("needs_slot", need=need)
            for example in entry.get("examples", []):
                example_owners[example].append(entry_id)
                normalized_owners[normalized(example)].append(entry_id)
            texts = list(answer_texts(entry.get("answer", {})))
            if any(re.search(r"\d", value) for value in texts):
                if not entry.get("last_verified"):
                    fail("number_last_verified")
                if not any(official(s.get("url", "")) for s in entry.get("sources", [])):
                    fail("number_official_source")
            if entry.get("kind") == "action" and entry.get("action") not in (
                    "register_visit", "report_emergency"):
                fail("unsupported_action")
            if any(re.search(r"desde este entorno|no pude consultar|norma que revis[eé]|HTTP [45]\d\d",
                             value, re.I) for value in texts):
                fail("research_environment_leak")
    for entry_id, owners in id_owners.items():
        if len(owners) > 1:
            errors.append({"id": entry_id, "rule": "duplicate_id", "owners": owners})
    for example, owners in example_owners.items():
        if len(owners) > 1:
            errors.append({"rule": "duplicate_example", "example": example, "owners": owners})
    for example, owners in normalized_owners.items():
        if len(set(owners)) > 1:
            warnings.append({"rule": "normalized_example_collision", "example": example,
                             "owners": sorted(set(owners))})
    for section_id, entry, data in entries:
        for related in entry.get("related", []):
            if related not in id_owners:
                errors.append({"id": entry["id"], "rule": "related_missing", "target": related})
        for negative in entry.get("hard_negatives", []):
            owners = example_owners.get(negative, [])
            if entry["id"] in owners or not owners:
                warnings.append({"id": entry["id"], "rule": "hard_negative_review", "text": negative})
    for section_id in {s for s, _, _ in entries}:
        data = next(d for s, _, d in entries if s == section_id)
        for featured in data.get("featured", []):
            if featured not in id_owners:
                errors.append({"section": section_id, "rule": "featured_missing", "target": featured})
    labels = [(s, e["id"], normalized(e.get("label", ""))) for s, e, _ in entries]
    for i, (section_a, id_a, label_a) in enumerate(labels):
        for section_b, id_b, label_b in labels[i + 1:]:
            ratio = SequenceMatcher(None, label_a, label_b).ratio()
            if ratio >= .88:
                warnings.append({"rule": "similar_labels", "ids": [id_a, id_b],
                                 "cross_section": section_a != section_b, "ratio": round(ratio, 3)})
    return {"sections": sections, "total_entries": len(entries),
            "total_examples": sum(s["examples"] for s in sections),
            "errors": errors, "warnings": warnings, "quality_samples": samples,
            "limitations": ["Semantic example similarity and citation entailment require manual review.",
                            "Numeric source checks confirm official domain presence, not evidence support.",
                            "Numbers written as words require manual review."]}


if __name__ == "__main__":
    assert normalized("¿Cómo estás?") == normalized("como estas")
    assert official("https://www.sgc.gov.co/a")
    assert not official("https://sgc.gov.co.example.com/a")
    assert list(answer_texts({"steps": [["one"], ["two"]], "detail": None})) == ["one", "two"]
    report = validate()
    (HERE / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("sections", "total_entries", "total_examples")},
                     ensure_ascii=False, indent=2))
    print(f"Errors: {len(report['errors'])}; review flags: {len(report['warnings'])}")
    sys.exit(bool(report["errors"]))
