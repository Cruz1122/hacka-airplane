"""Validates the conversation section against the attached schema snapshot and contract rules.

Run: python3 -I validate_section.py
Exit code 0 only when every check passes.
"""
import json
import re
import sys
from pathlib import Path

import jsonschema

BASE = Path("/home/cruz1122/dev/hacka-airplane/research_notes/Conocimiento turístico de Los Nevados")
SCHEMA = BASE / "inputs" / "knowledge-section.schema.json"
SECTION = Path("/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/conversation.json")
ENGLISH_MARKERS = re.compile(
    r"\b(what|where|how|can|do|does|are|is this|i'm|i |you|your|who|tell|thank|hello|hi there|bye|good|need|way|book|call|reminder|stupid|useless|got|forget|never|see you|me\?|where am)\b",
    re.I,
)

errors, warnings = [], []
data = json.loads(SECTION.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
    errors.append(f"schema: {'/'.join(map(str, err.path))}: {err.message}")

entries = data["entries"]
ids = [e["id"] for e in entries]
id_set = set(ids)
if len(ids) != len(id_set):
    errors.append("duplicate entry ids")

all_examples = {}
for e in entries:
    eid = e["id"]
    if not eid.startswith(data["id"] + "."):
        errors.append(f"{eid}: id does not start with section id")
    ex = e["examples"]
    if len(ex) < 12:
        errors.append(f"{eid}: only {len(ex)} examples (need >= 12)")
    if len(set(ex)) != len(ex):
        errors.append(f"{eid}: duplicate examples inside entry")
    for x in ex:
        if x in all_examples and all_examples[x] != eid:
            errors.append(f"example repeated across entries: {x!r} in {all_examples[x]} and {eid}")
        all_examples[x] = eid
    words = len(e["label"].split())
    if not 3 <= words <= 8:
        errors.append(f"{eid}: label has {words} words: {e['label']!r}")
    negs = e.get("hard_negatives", [])
    if not 2 <= len(negs) <= 4:
        errors.append(f"{eid}: {len(negs)} hard_negatives (need 2-4)")
    for n in negs:
        if n in ex:
            errors.append(f"{eid}: hard negative equals one of its own examples: {n!r}")
    for r in e.get("related", []):
        if r not in id_set:
            errors.append(f"{eid}: related id does not resolve: {r}")
    if not 1 <= len(e.get("related", [])) <= 3:
        errors.append(f"{eid}: related count {len(e.get('related', []))} not in 1-3")
    if any(ch.isdigit() for ch in e["answer"]["short"]):
        errors.append(f"{eid}: answer.short contains digits; add last_verified and official source first")
    if e.get("last_verified") is None and any(ch.isdigit() for ch in " ".join(e["answer"].get("variants", []))):
        errors.append(f"{eid}: variant contains digits without last_verified")
    en = [x for x in ex if ENGLISH_MARKERS.search(x)]
    if not 1 <= len(en) <= 4:
        warnings.append(f"{eid}: {len(en)} English-looking examples (check 1-2 natural English questions): {en}")
    if e["kind"] == "action":
        errors.append(f"{eid}: unexpected action kind")
    if e["audience"] != "visitor":
        errors.append(f"{eid}: audience must be visitor")

for f in data["featured"]:
    if f not in id_set:
        errors.append(f"featured id does not resolve: {f}")
if not 3 <= len(data["featured"]) <= 5:
    errors.append(f"featured count {len(data['featured'])} not in 3-5")

bank = data["clarification"]["bank"]
if not 4 <= len(bank) <= 8:
    errors.append(f"clarification.bank has {len(bank)} questions (need 4-8)")

print(f"entries={len(entries)} examples={sum(len(e['examples']) for e in entries)}")
print(f"errors={len(errors)} warnings={len(warnings)}")
for m in errors:
    print("ERROR", m)
for m in warnings:
    print("WARN", m)
sys.exit(1 if errors else 0)
