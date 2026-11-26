"""Build data/knowledge/sections/booking_fees.json from booking_fees/entries.json.

Source of truth: entries.json (authored, quotes in evidence/quotes.md). This
script adds the section metadata, expands related ids, derives hard negatives
from related entries, checks the contract rules that the coordinator validator
also checks, and writes the section. Run check_quotes.py before building.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE / "entries.json"
DEST = ROOT / "data/knowledge/sections/booking_fees.json"
SECTION = "booking_fees"
TODAY = "2026-11-21"
OFFICIAL_SUFFIX = "gov.co"

META = {
    "contract_version": 1,
    "id": SECTION,
    "order": 5,
    "title": "Reservas, tarifas y requisitos de ingreso",
    "description": "Información sobre reservas por sector, tarifas de ingreso, pagos, edad, seguro obligatorio y guías registrados para visitar Los Nevados.",
    "retrieval": {
        "profile": "lookup",
        "bm25_weight": 0.25,
        "top_k": 2,
        "min_score": None,
        "entity_filters": ["sector", "visitor_category"],
    },
    "clarification": {
        "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
        "bank": [
            "¿Qué sector o atractivo quieres visitar?",
            "¿Buscas reservar, revisar una tarifa o confirmar un requisito?",
            "¿Viajas con menores o necesitas confirmar una edad permitida?",
            "¿Quieres consultar el seguro, la guianza o la inducción?",
            "¿Tienes ya un operador registrado para tu recorrido?",
        ],
        "slot_questions": {
            "sector": "¿A qué sector o atractivo del parque vas?",
            "visitor_category": "¿Qué categoría de visitante quieres consultar?",
            "age": "¿Qué edad tiene la persona y qué atractivo planea visitar?",
        },
        "fallback": "Puedo orientarte sobre reservas, tarifas, edades, seguro, guías e inducción; dime qué sector o requisito quieres revisar.",
    },
    "featured": [
        "booking_fees.reservation_requirements",
        "booking_fees.sector_entry_fee_difference",
        "booking_fees.guide_required",
        "booking_fees.age_minimum_by_attraction",
        "booking_fees.accident_insurance_requirement",
    ],
}


def full_id(short):
    return f"{SECTION}.{short}" if not short.startswith(f"{SECTION}.") else short


def has_official_source(entry):
    # Numeric answers need an official government host, mirroring validate_knowledge.py.
    return any(
        (urlparse(s["url"]).hostname or "").endswith(OFFICIAL_SUFFIX) for s in entry["sources"]
    )


def build():
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in raw}
    errors = []
    entries = []
    for src in raw:
        own = set(src["examples"])
        related = [full_id(r) for r in src.get("related_short", [])]
        for rel in related:
            if rel not in by_id:
                errors.append(f"{src['id']}: related missing {rel}")
        if not 1 <= len(related) <= 3:
            errors.append(f"{src['id']}: related count {len(related)}")
        # Hard negatives: first examples of related entries that are not this entry's own examples.
        negatives = []
        for rel in related:
            for example in by_id[rel]["examples"]:
                if example not in own and example not in negatives:
                    negatives.append(example)
                    break
            if len(negatives) == 4:
                break
        answer = dict(src["answer"])
        out = {
            "id": src["id"],
            "label": src["label"],
            "kind": src["kind"],
            "audience": src["audience"],
            "lang": src["lang"],
            "examples": src["examples"],
            "hard_negatives": negatives[:2],
            "needs": [],
            "answer": answer,
            "sources": src["sources"],
            "last_verified": TODAY,
            "valid_until": src.get("valid_until"),
            "related": related,
            "tags": src.get("tags", []),
        }
        entries.append(out)
        if not 3 <= len(src["label"].split()) <= 8:
            errors.append(f"{src['id']}: label word count")
        if len(src["examples"]) < 12:
            errors.append(f"{src['id']}: examples < 12")
        if len(answer["short"]) > 320:
            errors.append(f"{src['id']}: answer.short > 320 chars")
        if re.search(r"\d", answer["short"] + answer.get("detail", "")) and not has_official_source(src):
            errors.append(f"{src['id']}: numeric answer without gov.co source")
        if len(out["hard_negatives"]) < 2:
            errors.append(f"{src['id']}: hard_negatives < 2")
    for feat in META["featured"]:
        if feat not in by_id:
            errors.append(f"featured missing {feat}")
    ids = [e["id"] for e in entries]
    if len(set(ids)) != len(ids):
        errors.append("duplicate entry ids")
    if errors:
        for error in errors:
            print("ERROR", error, file=sys.stderr)
        return 1
    data = dict(META)
    data["entries"] = entries
    DEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    examples = sum(len(e["examples"]) for e in entries)
    print(f"Wrote {DEST}: {len(entries)} entries, {examples} examples")
    return 0


if __name__ == "__main__":
    sys.exit(build())
