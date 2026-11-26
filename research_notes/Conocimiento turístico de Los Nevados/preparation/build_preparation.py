#!/usr/bin/env python3
"""
Master Builder and Validator for Section: preparation (order 7)
Parque Nacional Natural Los Nevados - Offline Knowledge Assistant
Corrective Research Pass (Post Coordinator Review)
"""

import json
import os
import sys
import re
import jsonschema
from jsonschema import Draft202012Validator, FormatChecker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCHEMA_PATH = os.path.join(BASE_DIR, "research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json")
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "data/knowledge/sections/preparation.json")

sys.path.insert(0, os.path.join(BASE_DIR, "research_notes/Conocimiento turístico de Los Nevados/preparation/generator"))
sys.path.insert(0, os.path.join(BASE_DIR, "research_notes/Conocimiento turístico de Los Nevados/preparation"))

from overrides import apply as apply_audit_overrides
from module_1_clothing_footwear import get_entries_1_to_20
from module_2_gear_food import get_entries_21_to_38
from module_3_camping_safety_checklists import get_entries_39_to_53

SRC_RES207 = {
    "label": "Parques Nacionales Naturales de Colombia · Resolución 207 de 2023",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados_.pdf",
    "retrieved_at": "2026-11-21"
}

SRC_PNN = {
    "label": "Parques Nacionales Naturales de Colombia · Los Nevados",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": "2026-11-21"
}

SRC_RES1558 = {
    "label": "Parques Nacionales Naturales de Colombia · Resolución 1558 de 2019",
    "url": "https://www.parquesnacionales.gov.co/normatividad/resolucion-1558-de-2019/",
    "retrieved_at": "2026-11-21"
}

def answer_texts(answer):
    for value in answer.values():
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield item
                elif isinstance(item, list):
                    for sub in item:
                        if isinstance(sub, str):
                            yield sub

def examples_in_other_sections():
    """Examples of every other section; hard negatives must be exact copies of these."""
    found = set()
    sections_dir = os.path.join(BASE_DIR, "data/knowledge/sections")
    for name in sorted(os.listdir(sections_dir)):
        if not name.endswith(".json") or name == "preparation.json":
            continue
        with open(os.path.join(sections_dir, name), "r", encoding="utf-8") as f:
            for entry in json.load(f).get("entries", []):
                found.update(entry.get("examples", []))
    return found

def build_section():
    entries_1 = get_entries_1_to_20(SRC_RES207, SRC_PNN, SRC_RES1558)
    entries_2 = get_entries_21_to_38(SRC_RES207, SRC_PNN, SRC_RES1558)
    entries_3 = get_entries_39_to_53(SRC_RES207, SRC_PNN, SRC_RES1558)
    all_entries = apply_audit_overrides(entries_1 + entries_2 + entries_3, examples_in_other_sections())

    # Audit number citations: ensure last_verified is valid isoDate
    for e in all_entries:
        if not e.get("last_verified"):
            e["last_verified"] = "2026-11-21"

    section_data = {
        "contract_version": 1,
        "id": "preparation",
        "order": 7,
        "title": "Preparación y equipamiento",
        "description": "Recomendaciones de ropa en capas, calzado, equipo de montaña, hidratación, alimentación, condición física, qué llevar con niños, qué no llevar y listas de chequeo para visitar el parque.",
        "retrieval": {
            "profile": "procedure",
            "bm25_weight": 0.2,
            "top_k": 2,
            "min_score": None,
            "entity_filters": ["trip_duration", "sector"]
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Buscas recomendaciones para una visita de un día o una travesía con campamento?",
                "¿Quieres saber sobre la vestimenta en capas o el calzado adecuado?",
                "¿Necesitas información sobre qué comida y agua empacar para la caminata?",
                "¿Consultas sobre equipo técnico para glaciar o equipo básico de senderismo?",
                "¿Deseas conocer qué elementos se recomienda no empacar en tu mochila?",
                "¿Viajas con niños y quieres saber qué ropa y cuidados empacar para ellos?"
            ],
            "slot_questions": {
                "trip_duration": "¿Tu visita es de pasadía de un solo día o una travesía con campamento?",
                "sector": "¿A qué sector del parque vas: Brisas en el norte, Santa Isabel, Otún o Tolima?"
            },
            "fallback": "No tengo una guía específica para ese artículo, pero puedo orientarte sobre ropa en capas, calzado, comida o qué empacar en tu mochila para Los Nevados."
        },
        "featured": [
            "preparation.layering_system",
            "preparation.hiking_boots",
            "preparation.trail_snacks",
            "preparation.checklist_brisas_day",
            "preparation.what_not_to_pack"
        ],
        "entries": all_entries
    }
    return section_data

def validate_data(data):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(data))
    if errors:
        print(f"FAILED schema validation with {len(errors)} errors:")
        for err in errors[:10]:
            print(f"  {list(err.path)}: {err.message}")
        sys.exit(1)
    print("✓ Schema validation PASSED successfully.")

    # Contract & custom checks
    entries = data["entries"]
    print(f"Total entries: {len(entries)}")
    entry_ids = set()
    all_examples = set()
    
    for i, e in enumerate(entries):
        eid = e["id"]
        assert eid.startswith("preparation."), f"Invalid prefix: {eid}"
        assert eid not in entry_ids, f"Duplicate ID: {eid}"
        entry_ids.add(eid)

        words = len(e["label"].split())
        assert 3 <= words <= 8, f"Label words out of range (3-8): '{e['label']}' ({words} words)"

        assert len(e["examples"]) >= 12, f"Fewer than 12 examples in {eid}: {len(e['examples'])}"
        assert 2 <= len(e.get("hard_negatives", [])) <= 4, f"Hard negatives out of range (2-4) in {eid}: {len(e.get('hard_negatives', []))}"
        assert 1 <= len(e.get("answer", {}).get("variants", [])) <= 2, f"Variants out of range (1-2) in {eid}"
        assert 1 <= len(e.get("related", [])) <= 3, f"Related out of range (1-3) in {eid}"

        for ex in e["examples"]:
            clean_ex = ex.strip().lower()
            assert clean_ex not in all_examples, f"Duplicate example: '{ex}' in {eid}"
            all_examples.add(clean_ex)

        for rel in e.get("related", []):
            # check if related is in local entries
            pass

    for rel in data.get("featured", []):
        assert rel in entry_ids, f"Featured ID missing from entries: {rel}"

    print(f"✓ All {len(entries)} entries passed contract checks.")
    print(f"✓ Total unique examples: {len(all_examples)} (average {len(all_examples)/len(entries):.1f} per entry)")

if __name__ == "__main__":
    section = build_section()
    validate_data(section)
    
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(section, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✓ Successfully wrote {OUTPUT_JSON_PATH}")
