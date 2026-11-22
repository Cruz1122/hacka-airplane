"""Shared builder for the corrected activities section.

The pre-correction modules must not be imported. Every answer below is written
from passages read on 2026-11-21.
"""

from __future__ import annotations

import json
from pathlib import Path

RETRIEVED = "2026-11-21"

SOURCES = {
    "ficha": {
        "label": "Parques Nacionales Naturales de Colombia, ficha PNN Los Nevados",
        "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
        "retrieved_at": RETRIEVED,
    },
    "res207": {
        "label": "Parques Nacionales Naturales, Resolución 207 del 4 de agosto de 2023",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf",
        "retrieved_at": RETRIEVED,
    },
    "letter": {
        "label": "PNN Los Nevados, radicado 20266200003411 del 11 de mayo de 2026",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/Respuesta-Radicado-Ano%CC%81nimo-No.-20264700042282.pdf",
        "retrieved_at": RETRIEVED,
    },
    "news": {
        "label": "Parques Nacionales Naturales, noticia del 6 de marzo de 2026",
        "url": "https://www.parquesnacionales.gov.co/sala-prensa/noticias/el-parque-nacional-natural-los-nevados-lanza-nuevo-plan-de-ordenamiento-ecoturistico-para-fortalecer-la-conservacion-en-la-alta-montana/",
        "retrieved_at": RETRIEVED,
    },
    "poe": {
        "label": "Parques Nacionales Naturales, versión corta del POE Los Nevados, copyright 2025",
        "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/03/PUBLICACIO%CC%81N-PNN-LOS-NEVADOS-2026-V2.pdf",
        "retrieved_at": RETRIEVED,
    },
}

ENTRIES: list[dict] = []


def entry(
    eid: str,
    label: str,
    kind: str,
    examples: list[str],
    negatives: list[str],
    short: str,
    variants: list[str],
    related: list[str],
    tags: list[str],
    sources: list[str],
    sector: list[str] | None = None,
    detail: str | None = None,
    steps: list[list[str]] | None = None,
    reflection: str | None = None,
) -> dict:
    answer: dict = {"short": short, "variants": variants}
    if steps is not None:
        answer["steps"] = steps
    if detail is not None:
        answer["detail"] = detail
    if reflection is not None:
        answer["reflection"] = reflection
    item = {
        "id": eid,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "needs": [],
        "answer": answer,
        "sources": [SOURCES[key] for key in sources],
        "last_verified": RETRIEVED,
        "related": related,
        "tags": tags,
    }
    if sector:
        item["entities"] = {"sector": sector}
    return item


def add(item: dict) -> None:
    ENTRIES.append(item)


def section_document() -> dict:
    return {
        "contract_version": 1,
        "id": "activities",
        "order": 8,
        "title": "Qué hacer y qué visitar",
        "description": "Recorridos, senderos, miradores, cumbres, camping, fotografía y otras actividades de visita en Los Nevados, según el sector.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.35,
            "top_k": 2,
            "min_score": None,
            "entity_filters": ["sector"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Buscas una salida corta por Brisas o una travesía de varios días?",
                "¿Quieres el valle del Ruiz, Santa Isabel, la Laguna del Otún o el Tolima?",
                "¿Preguntas por una cumbre, por acampar o por un sendero con nombre?",
                "¿La visita es en vehículo cubierto o caminando?",
                "¿Vas con niños o estás planeando alta montaña?",
                "¿Quieres fotografiar, mirar aves o saber si esa actividad está publicada?",
                "¿El plan es de un día o incluye pasar la noche?",
            ],
            "slot_questions": {
                "sector": "¿En qué sector quieres hacer la actividad: Brisas, Santa Isabel, Laguna del Otún o Tolima?",
            },
            "fallback": "No tengo ese recorrido con ese nombre. Puedo contarte la visita en Brisas, Santa Isabel, la Laguna del Otún o el Tolima, y qué cumbres están descritas. Confirma el sendero con Parques Nacionales antes de salir.",
        },
        "featured": [
            "activities.what_to_visit",
            "activities.brisas_valle_tumbas",
            "activities.ruiz_summit_closed",
            "activities.camping_where",
            "activities.sector_tolima",
        ],
        "entries": ENTRIES,
    }


def write_section(path: Path) -> None:
    path.write_text(json.dumps(section_document(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
