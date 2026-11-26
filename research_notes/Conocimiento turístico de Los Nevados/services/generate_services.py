"""Rebuild the curated services knowledge section from reviewed evidence.

The script is idempotent. It starts from the current section file, applies
CORRECTIONS by entry id, and upserts NEW_ENTRIES by id. Existing entries keep
their position, and new entries are appended after them.

Run: python3 generate_services.py
Evidence for every source lives in services/evidence/ (see quotes-2026-11-21.md).
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "data/knowledge/sections/services.json"
SECTIONS = ROOT / "data/knowledge/sections"
DATE = "2026-11-21"

PNN_PAGE = (
    "https://www.parquesnacionales.gov.co/nuestros-parques/"
    "parque-nacional-natural-los-nevados/"
)
INFORME_2024 = (
    "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/12/"
    "Informe-de-necesidades-de-asistencia-PNN-Los-Nevados-2024.docx"
)
ANEXO_2023 = (
    "https://parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf"
)
FOLLETO_2024 = "https://www.parquesnacionales.gov.co/wp-content/uploads/2024/07/nevados.pdf"
RADICADO_2026 = (
    "https://www.parquesnacionales.gov.co/wp-content/uploads/2026/05/"
    "Respuesta-Radicado-No.-20266200001002.pdf"
)
MINCIT_RNT = (
    "https://www.mincit.gov.co/minturismo/analisis-sectorial-y-promocion/"
    "registro-nacional-de-turismo/que-es-el-registro-nacional-de-turismo"
)
MINCIT_RENOVACION_2026 = (
    "https://www.mincit.gov.co/prensa/noticias/turismo/"
    "mincit-invita-renovar-registro-nacional-de-turismo"
)
VILLAMARIA_RENDICION_2025 = (
    "https://villamaria-caldas.gov.co/Participa/Documents/"
    "INFORME%20RENDICION%20%20DE%20CUENTAS%20DICIEMBRE%202025%20.pdf"
)


def source(label: str, url: str) -> dict[str, str]:
    return {"label": label, "url": url, "retrieved_at": DATE}


SRC_PNN = source("Parques Nacionales Naturales · Los Nevados (ficha oficial)", PNN_PAGE)
SRC_INFORME = source("PNN Los Nevados · Informe de necesidades de asistencia 2024", INFORME_2024)
SRC_ANEXO = source("PNN Los Nevados · Anexo de reglamentación ecoturística (2023)", ANEXO_2023)
SRC_FOLLETO = source("PNN Los Nevados · Folleto de gestión del ejercicio (2024)", FOLLETO_2024)


def entry(
    entry_id: str,
    label: str,
    kind: str,
    examples: list[str],
    hard_negatives: list[str],
    entities: dict[str, list[str]],
    short: str,
    variants: list[str],
    detail: str | None,
    sources: list[dict[str, str]],
    related: list[str],
    tags: list[str],
    steps: list[list[str]] | None = None,
) -> dict:
    answer: dict = {"short": short, "variants": variants}
    if steps is not None:
        answer["steps"] = steps
    answer["detail"] = detail
    answer["reflection"] = None
    return {
        "id": f"services.{entry_id}",
        "label": label,
        "kind": kind,
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "entities": entities,
        "answer": answer,
        "sources": sources,
        "last_verified": DATE,
        "valid_until": None,
        "related": related,
        "tags": tags,
    }


# Corrections to the existing 21 entries. Each key is an entry id; each value
# replaces the fields listed and appends any extra sources (deduplicated by URL).
CORRECTIONS: dict[str, dict] = {
    "services.porter_luggage": {
        "detail": (
            "Conflicto sin resolver: el anexo de PNN de 2023 prohíbe el porteo en las zonas "
            "de camping temporales de Calvito y Arenales, mientras el informe 2024 registra "
            "porteo en la ruta Los Chilcos–Arenales cumbre. Confirma el tramo con el prestador. "
            "La publicación 2026 de PNN (p. 31) incluye a los porteadores como categoría de "
            "prestador regulada."
        ),
        "add_sources": [SRC_ANEXO],
    },
    "services.guide_radios": {
        "detail": (
            "PNN describe estas condiciones como medidas de seguridad ante la actividad volcánica "
            "o las emergencias de montaña. El anexo de 2023 exige al guía autorizado botiquín, "
            "radio portable y certificado de primeros auxilios de 20 horas. La frecuencia no "
            "aparece en las fuentes revisadas; no la incluyo."
        ),
        "add_sources": [SRC_ANEXO],
    },
    "services.drinking_water": {
        "detail": (
            "Ninguna fuente revisada menciona fuentes ni puntos de agua potable. El anexo de 2023 "
            "exige que el guía lleve filtro para el agua en el equipo mínimo; eso no es un punto "
            "de agua en el parque. La recomendación de hidratación es de PNN; no hay datos de "
            "calidad del agua."
        ),
        "add_sources": [SRC_ANEXO],
    },
    "services.phone_signal": {
        "detail": (
            "El informe 2024 lista como necesidad implementar comunicaciones para la gestión del "
            "riesgo en algunos sectores. El folleto de PNN de 2024 cita \"Radiocomunicaciones\" y "
            "\"Conectividad\" entre sus aciertos, sin decir dónde ni con qué cobertura. La "
            "publicación 2026 de PNN incluye adquirir equipos de radiocomunicaciones como acción "
            "futura. Ninguna fuente revisada describe cobertura celular actual."
        ),
        "add_sources": [SRC_FOLLETO],
    },
}


NEW_ENTRIES: list[dict] = [
    entry(
        "interpretive_guiding",
        "guianza interpretativa en los senderos",
        "fact",
        [
            "guianza interpretativa",
            "hay guia que me explique el paramo",
            "dan guianza ambiental en los senderos",
            "me explican la naturaleza con un guia interprete",
            "hay recorridos guiados con educacion ambiental",
            "en el Cisne dan guianza para el sendero?",
            "guia que cuente del paramo y la fauna",
            "toca contratar guia para el sendero de interpretacion?",
            "sendero de interpretacion ambiental con guia",
            "en el Otun hay guia interprete?",
            "quien explica las plantas del paramo en el recorrido",
            "guia para entender el ecosistema del nevado",
            "do they offer guided interpretation tours",
            "is there an environmental interpretation guide",
        ],
        [
            "cómo sé si el guía está autorizado",
            "necesito contratar un guía para visitar",
        ],
        {"sector": ["brisas", "cisne", "otun", "quindio_dulima"]},
        (
            "La guianza interpretativa la ofrecen guías y operadores registrados en varios senderos, "
            "según el informe 2024 de PNN. Pide el servicio al operador antes de subir; en el sendero "
            "del Ruiz está restringida por la actividad volcánica."
        ),
        [
            "Según PNN (informe 2024), hay guianza interpretativa en senderos del Ruiz, Cisne, Otún, "
            "Chilcos–Arenales y Juntas. Confirma con el operador, porque depende de la actividad volcánica."
        ],
        (
            "El informe 2024 lista la guianza por sendero, no por sector. El anexo de 2023 exige que el "
            "guía esté registrado en la base de datos de PNN, tenga tarjeta profesional del Ministerio "
            "de Comercio y lleve botiquín y radio. No tengo tarifas verificadas aquí: los valores de "
            "interpretación y guianza aparecen en la ficha de PNN y pueden cambiar."
        ),
        [SRC_PNN, SRC_INFORME, SRC_ANEXO],
        ["services.guide_radios", "services.first_aid_points", "services.porter_luggage"],
        ["guianza", "interpretación", "guías", "educación ambiental"],
    ),
    entry(
        "town_lodging_rnt",
        "alojamiento en pueblos cercanos y RNT",
        "procedure",
        [
            "hostal en Murillo",
            "donde me quedo en Villamaria antes de subir",
            "hotel en Santa Rosa de Cabal para el parque",
            "hay hospedaje en El Cedral?",
            "como se si el hostal esta registrado",
            "el hotel tiene RNT?",
            "como verifico que la cabana este legal",
            "donde busco hospedajes en Murillo",
            "quedarme en Santa Rosa antes de ir al nevado",
            "posada en Villamaria para la madrugada",
            "hay casas para dormir en Murillo?",
            "que es el registro nacional de turismo",
            "where can I stay in Murillo before the trip",
            "is the hostel in Santa Rosa registered",
        ],
        [
            "hay hospedaje en El Bosque",
            "hay alojamiento en Brisas",
        ],
        {},
        (
            "Para dormir en Murillo, Villamaría o Santa Rosa de Cabal, elige un alojamiento con Registro "
            "Nacional de Turismo (RNT) vigente y pide su número. El RNT se renueva cada año, entre el 1 "
            "de enero y el 31 de marzo."
        ),
        [
            "Antes de reservar en Murillo, Villamaría o Santa Rosa, pide el número de RNT del alojamiento. "
            "Ese registro es obligatorio para operar y se renueva cada año."
        ],
        (
            "No encontré un listado oficial de alojamientos por municipio, así que no nombro negocios. "
            "En Villamaría, la Oficina de Turismo (turismo@villamaria-caldas.gov.co, según su informe de "
            "gestión de diciembre de 2025) puede orientarte. Para Murillo y Santa Rosa de Cabal no tengo un "
            "contacto oficial de turismo verificado; pregunta en su alcaldía. Precios y disponibilidad no "
            "están verificados."
        ),
        [
            source("MinCIT · Qué es el Registro Nacional de Turismo", MINCIT_RNT),
            source("MinCIT · Llamado a renovar el RNT 2026 (11-02-2026)", MINCIT_RENOVACION_2026),
            source("Alcaldía de Villamaría · Informe de rendición de cuentas (dic. 2025)", VILLAMARIA_RENDICION_2025),
        ],
        ["services.otun_lodging", "services.tolima_lodging", "services.cisne_visitor_center"],
        ["alojamiento", "RNT", "Murillo", "Villamaría", "Santa Rosa"],
        steps=[
            ["Pide al alojamiento su número de RNT antes de reservar."],
            ["Confírmalo en el RUES o pregunta en la cámara de comercio de la ciudad."],
        ],
    ),
    entry(
        "lost_items",
        "objetos perdidos: a quién avisar",
        "procedure",
        [
            "perdi un objeto en el parque",
            "se me perdio el celular en el sendero",
            "donde reclamo algo que se me perdio",
            "encontre un morral en el paramo, que hago",
            "hay oficina de objetos perdidos",
            "perdi las llaves cerca de la laguna",
            "a quien le aviso si se me pierde algo",
            "se me quedo la camara en la cabana",
            "deje una chaqueta en el centro de Brisas",
            "hay donde entreguen objetos encontrados",
            "donde dejan lo que encuentran en el sendero",
            "lost and found at the park",
            "I lost my glasses on the trail",
        ],
        [
            "perdí de vista a mi hijo en el sendero",
            "hay botiquín en las cabañas",
        ],
        {},
        (
            "No tengo confirmado un servicio de objetos perdidos en el parque. Escribe al correo del Parque "
            "Nacional, nevados@parquesnacionales.gov.co, y describe el objeto y el sector donde lo perdiste."
        ),
        [
            "No tengo confirmado un procedimiento de objetos perdidos. Escribe a nevados@parquesnacionales.gov.co "
            "con la descripción del objeto y el sector donde lo perdiste."
        ],
        (
            "Ninguna fuente revisada describe un procedimiento, un punto de entrega ni un horario para objetos "
            "perdidos. El correo es el general del área protegida: aparece en el anexo de PNN de 2023 y en una "
            "respuesta oficial de mayo de 2026. No es un canal específico para objetos."
        ),
        [
            SRC_ANEXO,
            source("PNN Los Nevados · Respuesta a derecho de petición (18-05-2026)", RADICADO_2026),
        ],
        ["services.official_sites", "services.brisas_visitor_center"],
        ["objetos perdidos", "correo", "contacto"],
        steps=[
            ["Escribe a nevados@parquesnacionales.gov.co."],
            ["Incluye qué objeto es y en qué sector lo perdiste."],
        ],
    ),
]


def normalize(text: str) -> str:
    """Compare examples the way the knowledge validator does: case and accent insensitive."""
    decomposed = unicodedata.normalize("NFKD", text.strip().lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def load_other_examples() -> dict[str, list[str]]:
    """Map normalized example -> ids in every other section file."""
    pool: dict[str, list[str]] = {}
    for path in sorted(SECTIONS.glob("*.json")):
        if path.resolve() == OUTPUT.resolve():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for other in data.get("entries", []):
            for example in other.get("examples", []):
                pool.setdefault(normalize(example), []).append(other["id"])
    return pool


def apply_corrections(entries: list[dict]) -> None:
    for item in entries:
        patch = CORRECTIONS.get(item["id"])
        if patch is None:
            continue
        if "detail" in patch:
            item["answer"]["detail"] = patch["detail"]
        known = {source_item["url"] for source_item in item["sources"]}
        for extra in patch.get("add_sources", []):
            if extra["url"] not in known:
                item["sources"].append(extra)
                known.add(extra["url"])


def upsert(entries: list[dict], new_items: list[dict]) -> list[dict]:
    index = {item["id"]: position for position, item in enumerate(entries)}
    for new_item in new_items:
        if new_item["id"] in index:
            entries[index[new_item["id"]]] = new_item
        else:
            entries.append(new_item)
            index[new_item["id"]] = len(entries) - 1
    return entries


def check(entries: list[dict]) -> None:
    """Fail fast on the contract rules this generator is responsible for."""
    ids = [item["id"] for item in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate entry ids in services")
    own_pool: dict[str, list[str]] = {}
    for item in entries:
        for example in item["examples"]:
            own_pool.setdefault(normalize(example), []).append(item["id"])
    other_pool = load_other_examples()
    for item in entries:
        if len(item["examples"]) < 12:
            raise ValueError(f"{item['id']} has fewer than 12 examples")
        if len({normalize(x) for x in item["examples"]}) != len(item["examples"]):
            raise ValueError(f"{item['id']} repeats an example internally")
        words = len(item["label"].split())
        if not 3 <= words <= 8:
            raise ValueError(f"{item['id']} label has {words} words")
        if not 2 <= len(item.get("hard_negatives", [])) <= 4:
            raise ValueError(f"{item['id']} needs 2-4 hard negatives")
        for example in item["examples"]:
            key = normalize(example)
            if key in other_pool:
                raise ValueError(f"{item['id']} example duplicates another section: {example}")
            if len(own_pool[key]) > 1:
                raise ValueError(f"example appears in several services entries: {example}")
        for negative in item.get("hard_negatives", []):
            key = normalize(negative)
            owners = own_pool.get(key, []) + other_pool.get(key, [])
            if not any(owner != item["id"] for owner in owners):
                raise ValueError(f"{item['id']} hard negative is not another entry's example: {negative}")
        for related in item.get("related", []):
            if related not in ids:
                raise ValueError(f"{item['id']} related does not resolve: {related}")
        if not 1 <= len(item.get("related", [])) <= 3:
            raise ValueError(f"{item['id']} needs 1-3 related ids")


def main() -> None:
    section = json.loads(OUTPUT.read_text(encoding="utf-8"))
    entries = section["entries"]
    apply_corrections(entries)
    entries = upsert(entries, NEW_ENTRIES)
    section["entries"] = entries
    check(entries)
    OUTPUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(entries)} entries, "
          f"{sum(len(item['examples']) for item in entries)} examples")


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: services now builds from services/source/services.v1.json via coordination/build_from_snapshot.py services; rerunning this script would revert reviewed corrections.")
    main()
