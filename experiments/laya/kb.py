"""Knowledge base: convert the v0 seed to the section contract, load and validate sections.

Usage:
  uv run python kb.py convert   # data/knowledge/raw/conocimiento.v0.json -> data/knowledge/sections/*.json
  uv run python kb.py validate  # schema + cross-section rules from docs/knowledge-contract.md
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/knowledge/raw/conocimiento.v0.json"
SECTIONS_DIR = (
    ROOT / "data/knowledge/phase1/sections"
)  # seed v0; data/knowledge/sections belongs to Phase 2
SCHEMA = ROOT / "docs/schemas/knowledge-section.schema.json"
CONVERTED_AT = "2026-11-21"

# v0 label -> (section, entry id suffix, kind). Phase 1 mapping from docs/plan-knowledge-system.md.
MAPPING: dict[str, tuple[str, str, str]] = {
    "cómo llegar desde Manizales": ("access", "from_manizales", "procedure"),
    "cómo entrar en vehículo": ("access", "by_vehicle", "procedure"),
    "el acceso desde Murillo": ("access", "from_murillo", "procedure"),
    "dónde queda Valle de las Tumbas": ("access", "valle_tumbas_location", "fact"),
    "los cuatro sectores del parque": ("access", "sectors", "fact"),
    "el sector Santa Isabel": ("access", "sector_santa_isabel", "fact"),
    "el sector Nevado del Tolima": ("access", "sector_tolima", "fact"),
    "cómo reservar": ("booking_fees", "how_to_book", "procedure"),
    "cuánto cuesta la entrada": ("booking_fees", "entry_fee", "fact"),
    "si necesitas guía": ("booking_fees", "guide_required", "rule"),
    "la edad para ingresar": ("booking_fees", "minimum_age", "rule"),
    "el seguro de accidentes": ("booking_fees", "accident_insurance", "rule"),
    "los horarios de ingreso": ("hours_status", "entry_hours", "fact"),
    "si el parque está abierto": ("hours_status", "is_open", "fact"),
    "los cierres por conservación": ("hours_status", "conservation_closures", "fact"),
    "qué se puede visitar": ("activities", "what_to_visit", "explanation"),
    "si se puede subir al cráter": ("activities", "climb_crater", "rule"),
    "acampar en el parque": ("activities", "camping", "rule"),
    "la fotografía en el parque": ("activities", "photography", "rule"),
    "si se puede ver la cumbre": ("activities", "see_summit", "explanation"),
    "qué ropa y equipo llevar": ("preparation", "clothing_gear", "procedure"),
    "la actividad del volcán": ("weather_volcano", "volcano_activity", "safety"),
    "qué debes cuidar durante la visita": ("rules", "visitor_care", "rule"),
    "si puedes llevar mascotas": ("rules", "pets", "rule"),
    "las aves del parque": ("fauna", "birds", "explanation"),
    "los mamíferos del parque": ("fauna", "mammals", "explanation"),
    "los ecosistemas del parque": ("flora_ecosystems", "ecosystems", "explanation"),
    "la nieve y los glaciares": ("flora_ecosystems", "snow_glaciers", "explanation"),
    "la Laguna del Otún": ("flora_ecosystems", "laguna_otun", "explanation"),
    "los frailejones": ("flora_ecosystems", "frailejones", "explanation"),
    "el agua del parque": ("flora_ecosystems", "water", "explanation"),
    "qué es el superpáramo": ("flora_ecosystems", "superparamo", "explanation"),
    "qué son los humedales altoandinos": ("flora_ecosystems", "wetlands", "explanation"),
    "qué es el páramo": ("flora_ecosystems", "paramo", "explanation"),
    "los nevados del parque": ("geography", "peaks", "fact"),
    "qué es el Nevado del Ruiz": ("geography", "nevado_ruiz", "explanation"),
    "la altura del Ruiz": ("geography", "ruiz_height", "fact"),
    "el nombre del cráter": ("geography", "crater_name", "fact"),
    "los departamentos que comparten el parque": ("geography", "departments", "fact"),
    "la extensión y la creación del parque": ("geography", "area_creation", "fact"),
    "la diferencia entre el parque y el volcán": ("geography", "park_vs_volcano", "explanation"),
    "la erupción de 1985 y Armero": ("history_culture", "armero_1985", "explanation"),
    "qué es un lahar": ("history_culture", "lahar", "explanation"),
    "el nombre Kumanday": ("history_culture", "kumanday", "explanation"),
}

# Seed examples that belong to a different entry (found by the validator).
DROP_EXAMPLES = {("los ecosistemas del parque", "qué es un páramo")}

# Section metadata (order follows docs/knowledge-contract.md).
SECTIONS: dict[str, dict] = {
    "weather_volcano": {
        "order": 3,
        "title": "Clima y volcán",
        "profile": "safety",
        "description": "Actividad volcánica del Nevado del Ruiz, alertas, clima y condiciones del día para la visita.",
        "bank": [
            "¿Quieres saber la actividad actual del volcán o cómo afecta tu visita?",
            "¿Te interesa el clima del día o el estado del volcán?",
        ],
        "fallback": "No tengo ese dato del clima o del volcán, pero puedo contarte cómo se vigila el Ruiz.",
    },
    "access": {
        "order": 4,
        "title": "Cómo llegar y accesos",
        "profile": "procedure",
        "description": "Rutas, vías, sectores y puntos de entrada al parque, y cómo llegar desde cada ciudad.",
        "bank": [
            "¿Desde qué ciudad sales?",
            "¿A qué sector vas: Brisas, Santa Isabel, Laguna del Otún o Tolima?",
        ],
        "fallback": "No tengo esa ruta exacta, pero puedo contarte cómo llegar desde Manizales o Murillo.",
    },
    "booking_fees": {
        "order": 5,
        "title": "Reservas, tarifas y requisitos",
        "profile": "lookup",
        "description": "Cómo reservar, cuánto cuesta la entrada, guía obligatorio, edad mínima y seguro de accidentes.",
        "bank": [
            "¿Quieres saber cómo reservar o cuánto cuesta?",
            "¿Preguntas por los requisitos para entrar, como guía o seguro?",
        ],
        "fallback": "No tengo ese dato de reservas, pero puedo contarte cómo reservar y qué requisitos hay.",
    },
    "hours_status": {
        "order": 6,
        "title": "Horarios y apertura",
        "profile": "lookup",
        "description": "Horarios de ingreso, si el parque está abierto y cierres temporales por conservación.",
        "bank": [
            "¿Quieres el horario de ingreso o saber si está abierto?",
            "¿Para qué sector y qué fecha?",
        ],
        "fallback": "No tengo ese horario, pero puedo contarte el horario de ingreso por Brisas.",
    },
    "preparation": {
        "order": 7,
        "title": "Preparación y equipo",
        "profile": "procedure",
        "description": "Qué ropa, calzado y equipo llevar a la alta montaña.",
        "bank": ["¿Preguntas por ropa, equipo o comida?", "¿Vas con niños o en grupo?"],
        "fallback": "No tengo ese detalle, pero puedo decirte qué ropa y equipo llevar.",
    },
    "activities": {
        "order": 8,
        "title": "Qué hacer en el parque",
        "profile": "explain",
        "description": "Qué visitar, recorridos, subir al cráter, acampar, tomar fotos y ver la cumbre.",
        "bank": [
            "¿Quieres saber qué visitar o si una actividad está permitida?",
            "¿En qué sector estás pensando?",
        ],
        "fallback": "No tengo esa actividad, pero puedo contarte qué se puede visitar en el parque.",
    },
    "rules": {
        "order": 9,
        "title": "Normas para el visitante",
        "profile": "rules",
        "description": "Normas del parque para el visitante: mascotas, residuos, senderos y cuidado de la naturaleza.",
        "bank": [
            "¿Preguntas si algo está permitido o cómo cuidar el parque?",
            "¿Qué quieres llevar o hacer?",
        ],
        "fallback": "No tengo esa norma, pero puedo contarte qué cuidar durante la visita.",
    },
    "fauna": {
        "order": 11,
        "title": "Fauna",
        "profile": "explain",
        "description": "Animales del parque: aves y mamíferos de alta montaña.",
        "bank": ["¿Te interesan las aves o los mamíferos?", "¿Buscas una especie en particular?"],
        "fallback": "No tengo esa especie, pero puedo contarte sobre las aves y mamíferos del parque.",
    },
    "flora_ecosystems": {
        "order": 12,
        "title": "Flora y ecosistemas",
        "profile": "explain",
        "description": "Páramo, superpáramo, frailejones, humedales, glaciares, lagunas y el agua del parque.",
        "bank": [
            "¿Te interesa un ecosistema, como el páramo, o una planta, como el frailejón?",
            "¿Preguntas por el agua, los glaciares o las lagunas?",
        ],
        "fallback": "No tengo ese tema, pero puedo contarte sobre el páramo y los frailejones.",
    },
    "geography": {
        "order": 13,
        "title": "Geografía y volcanes",
        "profile": "explain",
        "description": "Nevados y volcanes del parque, alturas, cráter, departamentos, extensión y creación.",
        "bank": [
            "¿Preguntas por un nevado en particular o por el parque en general?",
            "¿Quieres datos como altura y extensión, o una explicación?",
        ],
        "fallback": "No tengo ese dato, pero puedo contarte sobre el Nevado del Ruiz y los nevados del parque.",
    },
    "history_culture": {
        "order": 14,
        "title": "Historia y cultura",
        "profile": "explain",
        "description": "Historia del volcán y del parque: Armero 1985, lahares y el nombre Kumanday.",
        "bank": [
            "¿Te interesa la tragedia de Armero o el origen de los nombres?",
            "¿Quieres la historia del volcán o del parque?",
        ],
        "fallback": "No tengo esa historia, pero puedo contarte sobre la erupción de 1985 y Armero.",
    },
}


def convert() -> None:
    raw = json.loads(RAW.read_text())
    labels = {e["label"] for e in raw}
    if labels != set(MAPPING):
        sys.exit(f"mapping mismatch: missing={labels - set(MAPPING)} extra={set(MAPPING) - labels}")
    out: dict[str, list[dict]] = {s: [] for s in SECTIONS}
    for e in raw:
        section, suffix, kind = MAPPING[e["label"]]
        answer = {"short": e["reply"]}
        for src, dst in (
            ("variants", "variants"),
            ("steps", "steps"),
            ("detail", "detail"),
            ("reflection", "reflection"),
        ):
            if e.get(src):
                answer[dst] = e[src]
        entry = {
            "id": f"{section}.{suffix}",
            "label": e["label"],
            "kind": kind,
            "audience": "visitor",
            "lang": "es",
            "examples": [
                x for x in dict.fromkeys(e["examples"]) if (e["label"], x) not in DROP_EXAMPLES
            ],
            "answer": answer,
            "sources": [{**e["source"], "retrieved_at": CONVERTED_AT}],
        }
        if re.search(r"\d", e["reply"]):
            entry["last_verified"] = CONVERTED_AT
        out[section].append(entry)
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    for sid, meta in SECTIONS.items():
        doc = {
            "contract_version": 1,
            "id": sid,
            "order": meta["order"],
            "title": meta["title"],
            "description": meta["description"],
            "retrieval": {"profile": meta["profile"], "top_k": 2},
            "clarification": {
                "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
                "bank": meta["bank"],
                "fallback": meta["fallback"],
            },
            "featured": [e["id"] for e in out[sid][:3]],
            "entries": out[sid],
        }
        (SECTIONS_DIR / f"{sid}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
        )
    print(f"wrote {len(SECTIONS)} sections, {sum(map(len, out.values()))} entries")


@dataclass(frozen=True)
class Entry:
    id: str
    section: str
    label: str
    examples: tuple[str, ...]
    answer: str
    tags: tuple[str, ...]


def load_sections(directory: Path = SECTIONS_DIR) -> tuple[dict[str, dict], list[Entry]]:
    sections = {}
    entries = []
    for path in sorted(directory.glob("*.json")):
        doc = json.loads(path.read_text())
        sections[doc["id"]] = doc
        for e in doc["entries"]:
            if e["audience"] != "visitor":
                continue
            entries.append(
                Entry(
                    e["id"],
                    doc["id"],
                    e["label"],
                    tuple(e["examples"]),
                    e["answer"]["short"],
                    tuple(e.get("tags", [])),
                )
            )
    return sections, entries


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def validate(directory: Path = SECTIONS_DIR) -> list[str]:
    schema = json.loads(SCHEMA.read_text())
    validator = jsonschema.Draft202012Validator(schema)
    errors: list[str] = []
    docs = {}
    for path in sorted(directory.glob("*.json")):
        doc = json.loads(path.read_text())
        docs[path.name] = doc
        errors += [
            f"{path.name}: {'/'.join(map(str, e.path))}: {e.message}"
            for e in validator.iter_errors(doc)
        ]
    if errors:
        return errors
    ids: dict[str, str] = {}
    example_owner: dict[str, str] = {}
    for name, doc in docs.items():
        if name != f"{doc['id']}.json":
            errors.append(f"{name}: file name must be {doc['id']}.json")
        slot_q = doc["clarification"].get("slot_questions", {})
        for e in doc["entries"]:
            if not e["id"].startswith(doc["id"] + "."):
                errors.append(f"{e['id']}: id must start with section id {doc['id']}")
            if e["id"] in ids:
                errors.append(f"{e['id']}: duplicate id (also in {ids[e['id']]})")
            ids[e["id"]] = doc["id"]
            for ex in e["examples"]:
                key = _norm(ex)
                if key in example_owner and example_owner[key] != e["id"]:
                    errors.append(f"{e['id']}: example {ex!r} also in {example_owner[key]}")
                example_owner.setdefault(key, e["id"])
            for need in e.get("needs", []):
                if need not in slot_q:
                    errors.append(f"{e['id']}: needs {need!r} but {doc['id']} has no slot question")
            if re.search(r"\d", e["answer"]["short"]) and "last_verified" not in e:
                errors.append(f"{e['id']}: answer has digits but no last_verified")
    for doc in docs.values():
        for ref in doc.get("featured", []):
            if ref not in ids:
                errors.append(f"{doc['id']}: featured {ref} does not exist")
        for e in doc["entries"]:
            for ref in e.get("related", []):
                if ref not in ids:
                    errors.append(f"{e['id']}: related {ref} does not exist")
    return errors


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if cmd == "convert":
        convert()
    elif cmd == "validate":
        target = Path(sys.argv[2]) if len(sys.argv) > 2 else SECTIONS_DIR
        errs = validate(target)
        print("\n".join(errs) if errs else "OK: 0 errors")
        sys.exit(1 if errs else 0)
    else:
        sys.exit(__doc__)
