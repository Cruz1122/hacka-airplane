"""Write the corrected history_culture section. Run from this directory."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from corrected_culture import CULTURE
from corrected_round2 import ROUND2
from corrected_eruptions import ERUPTIONS
from corrected_names import NAMES

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data/knowledge/sections/history_culture.json"

ENTRIES = NAMES + ERUPTIONS + CULTURE + ROUND2

SECTION = {
    "contract_version": 1,
    "id": "history_culture",
    "order": 14,
    "title": "Historia y cultura",
    "description": "Nombres indígenas, creación del parque, erupciones históricas, memoria de Armero y la cultura campesina y cafetera ligada a Los Nevados.",
    "retrieval": {
        "profile": "explain",
        "bm25_weight": 0.35,
        "top_k": 3,
        "min_score": None,
        "entity_filters": ["volcano"],
    },
    "clarification": {
        "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
        "bank": [
            "¿Preguntas por la tragedia de 1985, por una erupción más antigua o por el nombre de un nevado?",
            "¿Hablas del Ruiz, de Santa Isabel, del Tolima o del parque en general?",
            "¿Quieres saber cuándo se creó el parque o qué pasó en Armero?",
            "¿Buscas el significado de Kumanday, de Poleka Kasue o de Dulima?",
            "¿La pregunta es sobre la historia de 1985 o sobre el estado del volcán hoy?",
            "¿Te interesa el paisaje cafetero, las casas de El Bosque o las comunidades del páramo?",
            "¿Preguntas por la ley de Armero o por la sentencia que declaró sujeto de derechos al parque?",
        ],
        "slot_questions": {
            "volcano": "¿Sobre cuál nevado preguntas: el Ruiz, Santa Isabel o el Tolima?",
        },
        "fallback": "Puedo contarte los nombres indígenas, la creación del parque o qué pasó en Armero. El estado del volcán de esta semana se mira en el Servicio Geológico Colombiano.",
    },
    "featured": [
        "history_culture.armero_1985",
        "history_culture.what_is_a_lahar",
        "history_culture.kumanday_name",
        "history_culture.park_creation_1974",
        "history_culture.coffee_landscape",
    ],
    "entries": ENTRIES,
}


def sentences(text: str) -> int:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([p for p in parts if p])


def main() -> int:
    ids = [e["id"] for e in ENTRIES]
    problems = []
    if len(ids) != len(set(ids)):
        problems.append("duplicate ids")
    examples = []
    for e in ENTRIES:
        examples.extend(e["examples"])
        if not 3 <= len(e["label"].split()) <= 8:
            problems.append(f"label {e['id']} {e['label']!r}")
        if len(e["examples"]) < 12:
            problems.append(f"examples {e['id']}")
        if len(set(e["examples"])) != len(e["examples"]):
            problems.append(f"dup ex {e['id']}")
        if not 2 <= len(e["hard_negatives"]) <= 4:
            problems.append(f"hn {e['id']}")
        if not 1 <= len(e["answer"]["variants"]) <= 2:
            problems.append(f"variants {e['id']}")
        if not 1 <= len(e["related"]) <= 3:
            problems.append(f"related {e['id']}")
        if sentences(e["answer"]["short"]) > 3:
            problems.append(f"short sentences {e['id']} {sentences(e['answer']['short'])}")
        for rel in e["related"]:
            if rel not in ids:
                problems.append(f"missing related {e['id']} -> {rel}")
        for feat in SECTION["featured"]:
            if feat not in ids:
                problems.append(f"missing featured {feat}")
    if len(examples) != len(set(examples)):
        from collections import Counter
        for text, n in Counter(examples).items():
            if n > 1:
                problems.append(f"dup example {text!r}")
    if problems:
        print("\n".join(problems))
        return 1
    OUT.write_text(json.dumps(SECTION, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"entries={len(ENTRIES)} examples={len(examples)} path={OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
