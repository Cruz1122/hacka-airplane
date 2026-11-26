#!/usr/bin/env python3
"""Build and validate the geography knowledge section.

Sources are the pages read on 2026-11-21. Visitor text is editorial,
not a quotation and not an endorsement of the offline app by those agencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path("/home/cruz1122/dev/hacka-airplane")
SCHEMA = ROOT / "research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json"
OUT = ROOT / "data/knowledge/sections/geography.json"
DATE = "2026-11-21"

PNN = {
    "label": "Parques Nacionales Naturales de Colombia",
    "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
    "retrieved_at": DATE,
}
SGC_SHEET = {
    "label": "Servicio Geológico Colombiano, hoja informativa del Nevado del Ruiz, septiembre de 2024",
    "url": "https://www2.sgc.gov.co/Temas-destacados/Documents/Hoja-informativa-volcan-Nevado-de-Ruiz-SGC.pdf",
    "retrieved_at": DATE,
}
SGC_RANK = {
    "label": "Servicio Geológico Colombiano, los 10 volcanes más altos de Colombia, 9 de agosto de 2024",
    "url": "https://www2.sgc.gov.co/Noticias/Paginas/Los-10-volcanes-mas-altos-de-Colombia.aspx",
    "retrieved_at": DATE,
}
SGC_BULLETIN = {
    "label": "Servicio Geológico Colombiano, boletín de actividad del segmento volcánico norte, 2023",
    "url": "https://www2.sgc.gov.co/Publicaciones/Informes%20tcnicos/Informe_de_actividad_volcanica_segmento_norte_2023.pdf",
    "retrieved_at": DATE,
}
SGC_CRATER = {
    "label": "Servicio Geológico Colombiano, geomorfología del cráter Arenas, 31 de enero de 2020",
    "url": "https://www2.sgc.gov.co/Noticias/Paginas/El-Nuevo-Domo-de-Lava-del-Volcan-Nevado-del-Ruiz-y-la-Geomorfologia-Actual-del-Crater-Arenas-2020.aspx",
    "retrieved_at": DATE,
}
IDEAM_RUIZ = {
    "label": "IDEAM, glaciar Nevado del Ruiz",
    "url": "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-ruiz",
    "retrieved_at": DATE,
}
IDEAM_SANTA = {
    "label": "IDEAM, glaciar Nevado Santa Isabel",
    "url": "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-santa-isabel",
    "retrieved_at": DATE,
}
IDEAM_TOLIMA = {
    "label": "IDEAM, glaciar Nevado del Tolima",
    "url": "https://www.ideam.gov.co/nuestra-entidad/ecosistemas-e-informacion-ambiental/glaciares/nevado-del-tolima",
    "retrieved_at": DATE,
}
RAMSAR = {
    "label": "Ficha Ramsar del complejo Laguna del Otún, 17 de julio de 2006",
    "url": "https://rsis.ramsar.org/RISapp/files/RISrep/CO1781RIS.pdf",
    "retrieved_at": DATE,
}
CARDER = {
    "label": "CARDER, nota sobre Los Nevados, 14 de julio de 2026",
    "url": "https://www.carder.gov.co/pnn-los-nevados-un-patrimonio-natural-que-garantiza-el-agua-y-la-vida-de-risaralda/",
    "retrieved_at": DATE,
}
TOLIMA_GOV = {
    "label": "Gobernación del Tolima, turismo de Anzoátegui",
    "url": "https://tolima.gov.co/tolima/informacion-general/turismo/1996-municipio-de-anzoategui",
    "retrieved_at": DATE,
}


def entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    negatives: list[str],
    short: str,
    variants: list[str],
    sources: list[dict],
    related: list[str],
    tags: list[str],
    entities: dict | None = None,
    detail: str | None = None,
    reflection: str | None = None,
) -> dict:
    item = {
        "id": entry_id,
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": negatives,
        "needs": [],
        "answer": {"short": short, "variants": variants, "detail": detail, "reflection": reflection},
        "sources": sources,
        "last_verified": DATE,
        "valid_until": None,
        "related": related,
        "tags": tags,
    }
    if entities:
        item["entities"] = entities
    return item


def build() -> dict:
    from entries_a import ENTRIES_A
    from entries_b import ENTRIES_B

    entries = ENTRIES_A + ENTRIES_B
    assign_negatives(entries)
    return {
        "contract_version": 1,
        "id": "geography",
        "order": 13,
        "title": "Geografía del parque",
        "description": "Nevados, paramillos, alturas, lagunas, ríos, departamentos, municipios, sectores y la diferencia entre el área protegida y el volcán.",
        "retrieval": {
            "profile": "explain",
            "bm25_weight": 0.25,
            "top_k": 3,
            "min_score": None,
            "entity_filters": ["landform", "sector"],
        },
        "clarification": {
            "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
            "bank": [
                "¿Preguntas por el parque completo o por una cumbre en particular?",
                "¿Cuál te interesa: Ruiz, Santa Isabel, Tolima, Quindío o Cisne?",
                "¿Buscas una laguna: Otún, Verde o del Encanto?",
                "¿Hablas de un sector de visita o de la montaña que le da nombre?",
                "¿Quieres la ubicación, la altura o la diferencia entre el parque y el volcán?",
                "¿La duda es el departamento, el municipio o la cordillera?",
                "¿Preguntas por el cráter Arenas del Ruiz o por el cráter del Tolima?",
            ],
            "slot_questions": {
                "landform": "¿Preguntas por un nevado, una laguna, un río, un cráter o por el parque completo?",
                "sector": "¿Te interesa Brisas-Kumanday, Cisne-Poleka Kasue, la Laguna del Otún o Quindío-Dulima?",
            },
            "fallback": "Puedo ubicarte los nevados, las lagunas, los sectores y los departamentos del parque. Dime cuál de esos lugares tienes en mente.",
        },
        "featured": [
            "geography.main_peaks",
            "geography.ruiz_height",
            "geography.park_versus_volcano",
            "geography.laguna_otun",
            "geography.four_sectors",
        ],
        "entries": entries,
    }


def word_count(label: str) -> int:
    return len(label.split())


def sentence_count(text: str) -> int:
    cleaned = re.sub(r"(?<=\d)\.(?=\d)", "", text)
    parts = [p for p in re.split(r"[.!?]+", cleaned) if p.strip()]
    return len(parts)


def pick_example(by_id: dict[str, dict], entry_id: str, fragment: str) -> str:
    examples = by_id[entry_id]["examples"]
    hits = [example for example in examples if fragment.casefold() in example.casefold()]
    if len(hits) != 1:
        raise SystemExit(f"{entry_id} :: {fragment!r} -> {hits}")
    return hits[0]


# Each negative is an example of another entry that a visitor could confuse with this one.
NEGATIVE_MAP: dict[str, list[tuple[str, str]]] = {
    "geography.main_peaks": [
        ("geography.park_versus_volcano", "es lo mismo el parque"),
        ("geography.ruiz_height", "a qué altura está la cima del Ruiz"),
        ("geography.four_sectors", "qué sectores hay"),
    ],
    "geography.ruiz_identity": [
        ("geography.ruiz_height", "cuánto mide el Nevado del Ruiz"),
        ("geography.arenas_crater", "cómo se llama el cráter principal"),
        ("geography.ruiz_age", "en qué año geológico"),
    ],
    "geography.ruiz_height": [
        ("geography.tolima_height", "a qué altura está el Nevado del Tolima"),
        ("geography.santa_isabel_height", "altura de Santa Isabel"),
        ("geography.highest_in_park", "cumbre más alta dentro del parque"),
    ],
    "geography.ruiz_where": [
        ("geography.manizales_outside", "Manizales queda dentro del parque"),
        ("geography.ruiz_faults", "por qué hay un volcán en esas fallas"),
        ("geography.villamaria_caldas", "Villamaría sí entra"),
    ],
    "geography.arenas_crater": [
        ("geography.tolima_crater", "el Tolima también tiene cráter"),
        ("geography.olleta_pirana", "qué es el volcán La Olleta"),
        ("geography.ruiz_height", "altura del Ruiz"),
    ],
    "geography.park_area": [
        ("geography.risaralda_share", "qué porcentaje del parque"),
        ("geography.municipalities", "qué municipios toca"),
        ("geography.departments", "en qué departamentos está"),
    ],
    "geography.departments": [
        ("geography.municipalities", "lista de municipios"),
        ("geography.manizales_outside", "ciudad de Manizales es parte"),
        ("geography.salento_quindio", "el parque llega hasta Salento"),
    ],
    "geography.cordillera_central": [
        ("geography.andes_occidentales_office", "por qué la ficha dice Andes Occidentales"),
        ("geography.watersheds", "hacia cada vertiente"),
        ("geography.departments", "departamentos de Los Nevados"),
    ],
    "geography.andes_occidentales_office": [
        ("geography.cordillera_central", "en qué cordillera está"),
        ("geography.departments", "Caldas Risaralda Quindío y Tolima"),
        ("geography.main_peaks", "Parque Los Nevados en el mapa"),
    ],
    "geography.municipalities": [
        ("geography.departments", "en qué departamentos está"),
        ("geography.ibague_highlands", "Ibagué ciudad queda dentro"),
        ("geography.salento_quindio", "Armenia está dentro"),
    ],
    "geography.manizales_outside": [
        ("geography.ruiz_where", "dónde queda el Ruiz"),
        ("geography.villamaria_caldas", "municipio caldense es Villamaría"),
        ("geography.murillo_ruiz", "Murillo está del lado del Ruiz"),
    ],
    "geography.park_versus_volcano": [
        ("geography.main_peaks", "qué nevados hay"),
        ("geography.park_area", "cuántas hectáreas tiene"),
        ("geography.four_sectors", "cuatro sectores del parque"),
    ],
    "geography.four_sectors": [
        ("geography.sector_brisas_kumanday", "qué es el sector Brisas"),
        ("geography.sector_cisne_poleka", "qué es el sector del Cisne"),
        ("geography.sector_laguna_otun", "sector Otún dónde queda"),
    ],
    "geography.sector_brisas_kumanday": [
        ("geography.valle_tumbas", "el silencio son el mismo"),
        ("geography.ruiz_height", "msnm del Nevado del Ruiz"),
        ("geography.four_sectors", "brisas cisne otun"),
    ],
    "geography.sector_cisne_poleka": [
        ("geography.paramillo_cisne", "qué es el Paramillo del Cisne"),
        ("geography.laguna_verde", "dónde queda la Laguna Verde"),
        ("geography.four_sectors", "nombres de las zonas de visita"),
    ],
    "geography.sector_laguna_otun": [
        ("geography.laguna_otun", "qué es la laguna del Otún"),
        ("geography.rio_otun", "de dónde nace el río Otún"),
        ("geography.pereira_santa_rosa", "Pereira está dentro del parque"),
    ],
    "geography.sector_quindio_dulima": [
        ("geography.tolima_volcano", "qué es el Nevado del Tolima"),
        ("geography.salento_quindio", "municipio quindiano del área"),
        ("geography.ibague_highlands", "municipio de Ibagué sí está"),
    ],
    "geography.valle_tumbas": [
        ("geography.sector_brisas_kumanday", "Brisas-Kumanday dónde queda"),
        ("geography.arenas_crater", "cráter Arenas"),
        ("geography.laguna_otun", "laguna más grande del parque"),
    ],
    "geography.laguna_otun": [
        ("geography.laguna_otun_formation", "cómo se formó la Laguna del Otún"),
        ("geography.rio_otun", "el Otún sale de la laguna"),
        ("geography.laguna_verde", "dónde queda la Laguna Verde"),
    ],
    "geography.laguna_otun_formation": [
        ("geography.laguna_otun", "qué es la laguna del Otún"),
        ("geography.rio_otun", "a qué altura nace el río"),
        ("geography.santa_isabel", "qué es Santa Isabel"),
    ],
    "geography.laguna_verde": [
        ("geography.glacier_summits", "qué cumbres todavía tienen nieve"),
        ("geography.sector_cisne_poleka", "Cisne-Poleka Kasue qué montañas"),
        ("geography.laguna_encanto", "dónde queda la Laguna del Encanto"),
    ],
    "geography.laguna_encanto": [
        ("geography.sector_quindio_dulima", "qué es el sector del Tolima"),
        ("geography.tolima_height", "altura del Tolima"),
        ("geography.laguna_otun", "laguna grande de los nevados"),
    ],
    "geography.santa_isabel": [
        ("geography.santa_isabel_height", "altura de Santa Isabel"),
        ("geography.sector_cisne_poleka", "mira hacia Poleka Kasue"),
        ("geography.paramillo_cisne", "Cisne es un nevado o un paramillo"),
    ],
    "geography.santa_isabel_height": [
        ("geography.ruiz_height", "cuánto mide el Nevado del Ruiz"),
        ("geography.tolima_height", "cuánto mide la cumbre del Tolima"),
        ("geography.santa_isabel", "tres cumbres norte centro y sur"),
    ],
    "geography.tolima_volcano": [
        ("geography.tolima_height", "5215 es la cima"),
        ("geography.sector_quindio_dulima", "Quindío-Dulima a qué volcán"),
        ("geography.tolima_crater", "cómo es el cráter del Tolima"),
    ],
    "geography.tolima_height": [
        ("geography.ruiz_height", "a qué altura está la cima del Ruiz"),
        ("geography.highest_in_park", "el Ruiz le gana al Tolima"),
        ("geography.tolima_volcano", "una sola cumbre, no tres"),
    ],
    "geography.paramillo_quindio": [
        ("geography.paramillo_santa_rosa", "a qué altura está Santa Rosa"),
        ("geography.salento_quindio", "cumbre del Quindío"),
        ("geography.glacier_summits", "paramillos no entran"),
    ],
    "geography.paramillo_cisne": [
        ("geography.sector_cisne_poleka", "el cisne es el sector o la montaña"),
        ("geography.santa_isabel", "conjunto de domos"),
        ("geography.main_peaks", "nevados y los paramillos"),
    ],
    "geography.paramillo_santa_rosa": [
        ("geography.paramillo_quindio", "junto con Santa Rosa"),
        ("geography.laguna_otun", "páramo de Santa Rosa"),
        ("geography.pereira_santa_rosa", "Santa Rosa de Cabal también entra"),
    ],
    "geography.olleta_pirana": [
        ("geography.arenas_crater", "qué es Arenas en la cima"),
        ("geography.ruiz_identity", "cráter y glaciar ese volcán"),
        ("geography.volcanic_centers", "la olleta no esta activa"),
    ],
    "geography.glacier_summits": [
        ("geography.laguna_verde", "laguna verde es un glaciar"),
        ("geography.santa_isabel", "tres nevados del parque"),
        ("geography.paramillo_quindio", "todavía es un nevado con hielo"),
    ],
    "geography.highest_in_park": [
        ("geography.ruiz_versus_huila", "volcán más alto de Colombia"),
        ("geography.ruiz_height", "cinco mil metros"),
        ("geography.tolima_height", "cinco mil doscientos"),
    ],
    "geography.ruiz_versus_huila": [
        ("geography.highest_in_park", "punto más alto de Los Nevados"),
        ("geography.ruiz_height", "qué tan alto es ese volcán"),
        ("geography.tolima_volcano", "cono en el sur del parque"),
    ],
    "geography.watersheds": [
        ("geography.rio_otun", "de dónde nace el río Otún"),
        ("geography.rio_chinchina", "de dónde sale el río Chinchiná"),
        ("geography.cordillera_central", "entre el Cauca y el Magdalena"),
    ],
    "geography.rio_otun": [
        ("geography.laguna_otun", "visitar el Otún"),
        ("geography.laguna_otun_formation", "origen glacial"),
        ("geography.watersheds", "baja al Cauca o al Magdalena"),
    ],
    "geography.rio_chinchina": [
        ("geography.rio_otun", "cae a la cuenca del Cauca"),
        ("geography.watersheds", "Azufrado y Recio"),
        ("geography.villamaria_caldas", "lado caldense del Ruiz"),
    ],
    "geography.ruiz_age": [
        ("geography.ruiz_identity", "es un estratovolcán"),
        ("geography.geoheritage", "patrimonio geológico internacional"),
        ("geography.volcanic_centers", "estratovolcán activo del complejo"),
    ],
    "geography.volcanic_centers": [
        ("geography.olleta_pirana", "cráteres parásitos"),
        ("geography.ruiz_identity", "estratovolcan activo"),
        ("geography.ruiz_faults", "mapa de amenaza de esta semana"),
    ],
    "geography.geoheritage": [
        ("geography.ruiz_identity", "ficha corta del Nevado del Ruiz"),
        ("geography.arenas_crater", "asomarme al cráter"),
        ("geography.ruiz_age", "erupción de 1985"),
    ],
    "geography.ruiz_faults": [
        ("geography.ruiz_where", "volcán está en la cordillera Central"),
        ("geography.volcanic_centers", "color de alerta de hoy"),
        ("geography.ruiz_identity", "historia de Armero"),
    ],
    "geography.summit_line": [
        ("geography.main_peaks", "cuáles son las cumbres del parque"),
        ("geography.ruiz_where", "sureste de Manizales"),
        ("geography.tolima_volcano", "4 grados 39 norte"),
    ],
    "geography.risaralda_share": [
        ("geography.park_area", "61.388 es la cifra"),
        ("geography.pereira_santa_rosa", "municipios risaraldenses"),
        ("geography.laguna_otun", "Pereira y Santa Rosa"),
    ],
    "geography.salento_quindio": [
        ("geography.sector_quindio_dulima", "salento ibague y anzoategui"),
        ("geography.paramillo_quindio", "Tolima Quindío y Risaralda se tocan"),
        ("geography.municipalities", "Salento Herveo Casabianca"),
    ],
    "geography.villamaria_caldas": [
        ("geography.manizales_outside", "Manizales o de Villamaría"),
        ("geography.ruiz_where", "Villamaría Murillo y Casabianca"),
        ("geography.murillo_ruiz", "no es Villamaría"),
    ],
    "geography.tolima_municipalities": [
        ("geography.municipalities", "diez o once municipios"),
        ("geography.murillo_ruiz", "municipio de Murillo entra"),
        ("geography.ibague_highlands", "Ibagué está en la lista de diez"),
    ],
    "geography.pereira_santa_rosa": [
        ("geography.sector_laguna_otun", "referencia municipal de ese lado"),
        ("geography.risaralda_share", "Pereira y Santa Rosa"),
        ("geography.ucumari_buffer", "El Cedral está en Ucumarí"),
    ],
    "geography.ibague_highlands": [
        ("geography.tolima_volcano", "ibague y anzoategui"),
        ("geography.sector_quindio_dulima", "salento ibague y anzoategui"),
        ("geography.tolima_height", "metros de Dulima"),
    ],
    "geography.murillo_ruiz": [
        ("geography.ruiz_where", "kilometros de manizales"),
        ("geography.villamaria_caldas", "glaciar del Ruiz pasa por Villamaría"),
        ("geography.sector_brisas_kumanday", "sector del volcán Nevado del Ruiz"),
    ],
    "geography.ucumari_buffer": [
        ("geography.laguna_otun", "humedal Ramsar"),
        ("geography.rio_otun", "el Otún sale de la laguna"),
        ("geography.pereira_santa_rosa", "ciudad de Pereira es la laguna"),
    ],
    "geography.tolima_crater": [
        ("geography.arenas_crater", "nombre del crater del ruiz"),
        ("geography.tolima_volcano", "forma cónica del volcán"),
        ("geography.tolima_height", "cota de la única cumbre"),
    ],
}


def assign_negatives(entries: list[dict]) -> None:
    by_id = {item["id"]: item for item in entries}
    missing = set(by_id) - set(NEGATIVE_MAP)
    extra = set(NEGATIVE_MAP) - set(by_id)
    if missing or extra:
        raise SystemExit(f"negative map mismatch missing={sorted(missing)} extra={sorted(extra)}")
    for item in entries:
        chosen = []
        for other_id, fragment in NEGATIVE_MAP[item["id"]]:
            example = pick_example(by_id, other_id, fragment)
            if example in item["examples"]:
                raise SystemExit(f"{item['id']} negative is its own example: {example}")
            chosen.append(example)
        if len(set(chosen)) != len(chosen):
            raise SystemExit(f"repeated negative in {item['id']}: {chosen}")
        item["hard_negatives"] = chosen


def validate(section: dict) -> list[str]:
    import jsonschema

    errors: list[str] = []
    schema = json.loads(SCHEMA.read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(section), key=lambda item: list(item.path)):
        errors.append(f"schema: {list(err.path)}: {err.message}")

    if section["id"] != "geography" or section["order"] != 13:
        errors.append("section id or order mismatch")
    if section["retrieval"]["profile"] != "explain":
        errors.append("profile must be explain")
    filters = set(section["retrieval"]["entity_filters"])
    slots = set(section["clarification"]["slot_questions"])
    if filters != slots:
        errors.append(f"slot_questions {slots} do not match filters {filters}")
    bank = section["clarification"]["bank"]
    if not 4 <= len(bank) <= 8:
        errors.append("clarification bank must have 4 to 8 questions")
    if "{label_a}" not in section["clarification"]["between_entries"] or "{label_b}" not in section["clarification"]["between_entries"]:
        errors.append("between_entries template missing labels")

    ids = [item["id"] for item in section["entries"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate entry ids")
    featured = section["featured"]
    if not 1 <= len(featured) <= 5:
        errors.append("featured count out of range")
    for featured_id in featured:
        if featured_id not in ids:
            errors.append(f"featured missing: {featured_id}")

    seen_examples: dict[str, str] = {}
    labels: list[str] = []
    for item in section["entries"]:
        if not item["id"].startswith("geography."):
            errors.append(f"bad id {item['id']}")
        labels.append(item["label"])
        count = word_count(item["label"])
        if not 3 <= count <= 8:
            errors.append(f"{item['id']} label has {count} words: {item['label']}")
        if len(item["examples"]) < 12:
            errors.append(f"{item['id']} has {len(item['examples'])} examples")
        if len(set(item["examples"])) != len(item["examples"]):
            errors.append(f"{item['id']} has duplicate examples")
        negatives = item.get("hard_negatives") or []
        if not 2 <= len(negatives) <= 4:
            errors.append(f"{item['id']} has {len(negatives)} hard negatives")
        related = item.get("related") or []
        if not 1 <= len(related) <= 3:
            errors.append(f"{item['id']} has {len(related)} related")
        for rel in related:
            if rel not in ids:
                errors.append(f"{item['id']} related missing: {rel}")
            if rel == item["id"]:
                errors.append(f"{item['id']} related to itself")
        needs = item.get("needs") or []
        for need in needs:
            if need not in section["clarification"]["slot_questions"]:
                errors.append(f"{item['id']} need without slot: {need}")
        variants = item["answer"].get("variants") or []
        if not 1 <= len(variants) <= 2:
            errors.append(f"{item['id']} variants {len(variants)}")
        if sentence_count(item["answer"]["short"]) > 3:
            errors.append(f"{item['id']} short has {sentence_count(item['answer']['short'])} sentences")
        if len(item["answer"]["short"]) < 10:
            errors.append(f"{item['id']} short too small")
        if re.search(r"\d", item["answer"]["short"]) and "last_verified" not in item:
            errors.append(f"{item['id']} number without last_verified")
        for example in item["examples"]:
            key = example.casefold().strip()
            if key in seen_examples:
                errors.append(f"duplicate example between {seen_examples[key]} and {item['id']}: {example}")
            else:
                seen_examples[key] = item["id"]
            if example.startswith("geography.") or example.lower().startswith("ejemplo"):
                errors.append(f"artificial example in {item['id']}: {example}")

    example_owner = {example: owner for owner, example in ((owner, ex) for owner, ex in seen_examples.items())}
    # rebuild exact map
    exact_owner: dict[str, str] = {}
    for item in section["entries"]:
        for example in item["examples"]:
            exact_owner[example] = item["id"]
    for item in section["entries"]:
        for negative in item.get("hard_negatives") or []:
            owner = exact_owner.get(negative)
            if owner is None:
                errors.append(f"{item['id']} negative is not an example: {negative}")
            elif owner == item["id"]:
                errors.append(f"{item['id']} negative points to itself: {negative}")
        for negative in item.get("hard_negatives") or []:
            if negative in item["examples"]:
                errors.append(f"{item['id']} negative duplicates its own example")

    if len(set(labels)) != len(labels):
        errors.append("duplicate labels")
    return errors


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    section = build()
    errors = validate(section)
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n")
    example_count = sum(len(item["examples"]) for item in section["entries"])
    print(f"entries={len(section['entries'])} examples={example_count} errors={len(errors)}")
    for err in errors:
        print(err)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: geography now builds from geography/source/geography.v1.json via coordination/build_from_snapshot.py geography; rerunning this script would revert reviewed corrections.")
    raise SystemExit(main())
