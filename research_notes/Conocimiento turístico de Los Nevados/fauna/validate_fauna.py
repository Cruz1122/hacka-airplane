"""Independent validator for data/knowledge/sections/fauna.json."""
import json
import re
from pathlib import Path
import jsonschema

BASE = Path("/home/cruz1122/dev/hacka-airplane")
SECTION_PATH = BASE / "data/knowledge/sections/fauna.json"
SCHEMA_PATH = BASE / "research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json"

section = json.loads(SECTION_PATH.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

# 1. JSON Schema validation
validator = jsonschema.Draft202012Validator(schema)
schema_errors = list(validator.iter_errors(section))
if schema_errors:
    print(f"FAILED: {len(schema_errors)} JSON schema errors found:")
    for err in schema_errors:
        print(f"  {list(err.path)}: {err.message}")
    raise SystemExit(1)
print("JSON Schema: VALID (Draft 2020-12)")

# 2. Section contract checks
problems = []
entries = section["entries"]
entry_ids = {e["id"] for e in entries}
all_examples = {}
labels = set()

if section["id"] != "fauna":
    problems.append(f"Section id must be 'fauna', got '{section['id']}'")
if section["order"] != 11:
    problems.append(f"Section order must be 11, got '{section['order']}'")
if section["retrieval"]["profile"] != "explain":
    problems.append(f"Retrieval profile must be 'explain', got '{section['retrieval']['profile']}'")

for e in entries:
    eid = e["id"]
    if not eid.startswith("fauna."):
        problems.append(f"{eid}: ID must start with 'fauna.'")
    words = e["label"].strip().split()
    if not (3 <= len(words) <= 8):
        problems.append(f"{eid}: label has {len(words)} words (must be 3-8): '{e['label']}'")
    if e["label"] in labels:
        problems.append(f"{eid}: duplicate label '{e['label']}'")
    labels.add(e["label"])

    if len(e["examples"]) < 12:
        problems.append(f"{eid}: fewer than 12 examples ({len(e['examples'])})")
    if not (2 <= len(e.get("hard_negatives", [])) <= 4):
        problems.append(f"{eid}: hard negatives count not in [2, 4]: {len(e.get('hard_negatives', []))}")

    for ex in e["examples"]:
        clean_ex = ex.strip().lower()
        if clean_ex in all_examples:
            problems.append(f"Duplicate example: '{ex}' in {all_examples[clean_ex]} and {eid}")
        all_examples[clean_ex] = eid

    for ref in e.get("related", []):
        if ref not in entry_ids:
            problems.append(f"{eid}: unresolved related id '{ref}'")

    for need in e.get("needs", []):
        if need not in section["clarification"].get("slot_questions", {}):
            problems.append(f"{eid}: missing slot question for need '{need}'")

    full_text = e["answer"]["short"] + " " + " ".join(e["answer"].get("variants", []))
    if re.search(r"\d", full_text):
        if not e.get("last_verified"):
            problems.append(f"{eid}: answer contains digits but lacks last_verified")

for feat in section.get("featured", []):
    if feat not in entry_ids:
        problems.append(f"Featured ID unresolved: '{feat}'")

for key in section["retrieval"].get("entity_filters", []):
    if key not in section["clarification"].get("slot_questions", {}):
        problems.append(f"Missing slot question for entity filter '{key}'")

if problems:
    print(f"FAILED: {len(problems)} contract problems:")
    for p in problems:
        print(f"  {p}")
    raise SystemExit(1)

print("Contract checks: VALID")
print(f"  Entries count: {len(entries)}")
print(f"  Total examples: {len(all_examples)}")
print(f"  Total hard negatives: {sum(len(e.get('hard_negatives', [])) for e in entries)}")
print("All checks successfully passed!")
