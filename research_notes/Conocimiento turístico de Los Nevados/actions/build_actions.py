"""Build and validate data/knowledge/sections/actions.json.

Usage (from the repository root):
    python3 -I "research_notes/Conocimiento turístico de Los Nevados/actions/build_actions.py"

Writes the section JSON, then validates it against the attached schema snapshot
and the contract rules that the schema cannot express. Exits non-zero on failure.

Facts are cited to the evidence saved under actions/evidence/ (see actions.research.md).
Editorial action text (what the app does) has no official source and is labelled as such.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
NOTES = REPO / "research_notes" / "Conocimiento turístico de Los Nevados"
SCHEMA = NOTES / "inputs" / "knowledge-section.schema.json"
OUT = REPO / "data" / "knowledge" / "sections" / "actions.json"

VERIFIED = "2026-11-21"
PNN_URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"
POLICIA_URL = (
    "https://www.policia.gov.co/noticia/"
    "policia-nacional-sensibiliza-comunidad-sobre-uso-las-lineas-emergencia-123-155"
)
SRC_PNN = {
    "label": "Parques Nacionales Naturales · ficha Los Nevados (reservas y registro de ingreso; no describe el registro de esta app)",
    "url": PNN_URL,
    "retrieved_at": VERIFIED,
}
SRC_PNN_GUIA = {
    "label": "Parques Nacionales Naturales · ficha Los Nevados (guías registrados: equipo médico de respuesta y radios; no describe esta app)",
    "url": PNN_URL,
    "retrieved_at": VERIFIED,
}
SRC_123 = {
    "label": "Policía Nacional · nota sobre la línea 123, publicada el 12 mar 2023 (no describe el reporte de esta app)",
    "url": POLICIA_URL,
    "retrieved_at": VERIFIED,
}

SLOT_QUESTIONS = {
    "sector": "¿En qué sector estás o vas a ir: Brisas, Cisne, Otún o Quindío–Dulima?",
    "date": "¿Para qué fecha quieres registrar la visita?",
    "group_size": "¿Cuántas personas integran el grupo?",
    "visitor_type": "¿El visitante es nacional o extranjero?",
    "emergency_type": "¿Qué tipo de emergencia es: lesión, persona perdida, mal de altura, hipotermia, tormenta eléctrica o incendio?",
    "people_count": "¿Cuántas personas están involucradas en la emergencia?",
}

EMERGENCY_NEEDS = ["sector", "people_count"]


def emergency_entry(
    entry_id: str,
    label: str,
    emergency_type: str | None,
    examples: list[str],
    hard_negatives: list[str],
    short: str,
    variant: str,
    steps: list[list[str]],
    related: list[str],
    tags: list[str],
) -> dict:
    """Build a report_emergency entry.

    emergency_type=None means the visitor has not said which kind of emergency it is, so the
    handoff must ask for it: emergency_type is then a need and no type is pinned in entities.
    """
    if emergency_type is None:
        entities: dict[str, list[str]] = {}
        needs = ["emergency_type", *EMERGENCY_NEEDS]
    else:
        entities = {"emergency_type": [emergency_type]}
        needs = list(EMERGENCY_NEEDS)
    return {
        "id": entry_id,
        "label": label,
        "kind": "action",
        "audience": "visitor",
        "lang": "es",
        "examples": examples,
        "hard_negatives": hard_negatives,
        "entities": entities,
        "needs": needs,
        "action": "report_emergency",
        "answer": {"short": short, "variants": [variant], "steps": steps},
        "sources": [SRC_123, SRC_PNN_GUIA],
        "last_verified": VERIFIED,
        "valid_until": None,
        "related": related,
        "tags": tags,
    }


ENTRIES: list[dict] = [
    {
        "id": "actions.register_planned_visit",
        "label": "registrar una visita para otra fecha",
        "kind": "action",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "quiero registrar mi visita para el sábado",
            "registrar un grupo para una fecha futura",
            "cómo dejo registrado mi grupo para otro día",
            "anotar a cuatro personas para el domingo",
            "registro de visita para el puente festivo",
            "necesito dejar registrada una visita",
            "registrar visita al Otún el mes que viene",
            "me ayudas a registrar la visita del fin de semana",
            "¿registrar la visita sirve como reserva?",
            "quiero registrar mi grupo con anticipación",
            "I want to register a visit for a future date",
            "register my group visit for next weekend",
            "reg visita pa el sabado pa seis personas",
            "ayúdame a registrar la visita de mañana",
        ],
        "hard_negatives": ["cómo reservo", "cuánto cuesta entrar", "a qué hora abren"],
        "entities": {
            "sector": ["brisas", "cisne", "otun", "quindio_dulima"],
            "visitor_type": ["nacional", "extranjero"],
        },
        "needs": ["sector", "date", "group_size", "visitor_type"],
        "action": "register_visit",
        "answer": {
            "short": (
                "Puedo preparar el registro de tu visita con sector, fecha, número de personas y tipo de visitante. "
                "Te muestro un resumen y no lo envío sin tu confirmación; sin conexión no puedo asegurar que quede guardado."
            ),
            "variants": [
                "Te ayudo a dejar lista la visita: dime el sector, la fecha, cuántas personas son y si son nacionales o extranjeros. "
                "Confirmas el resumen antes de cualquier envío, y sin conexión no puedo garantizar que quede guardado."
            ],
            "steps": [
                [
                    "Dime el sector, la fecha, el número de personas y el tipo de visitante.",
                    "Revisa el resumen que te muestro antes de confirmar.",
                ],
                [
                    "El registro de ingreso del parque se hace en el punto de registro del sector; esta acción no lo reemplaza.",
                    "En Brisas, para fines de semana y festivos, la ficha pide reservar con al menos un día de anticipación en reservasnevados.com. En los demás sectores la reserva es obligatoria y la gestiona tu agencia registrada.",
                ],
            ],
        },
        "sources": [SRC_PNN],
        "last_verified": VERIFIED,
        "valid_until": None,
        "related": ["actions.register_arrival_today", "actions.report_emergency_general"],
        "tags": ["registro", "visita", "grupo", "fecha"],
    },
    {
        "id": "actions.register_arrival_today",
        "label": "registrar mi llegada al sector hoy",
        "kind": "action",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "ya llegué a la entrada, quiero registrarme",
            "estoy en el punto de ingreso, cómo me registro",
            "llegamos hoy al sector, registro el grupo",
            "registrar llegada hoy",
            "ya estoy en Brisas, anoto a mi grupo",
            "me registro ahorita que llegué al parque",
            "ya llegué al control de Potosí, ¿me registro?",
            "acabo de llegar, hay que registrarnos",
            "toca registrarnos aquí en la entrada?",
            "ya llegue, como me registro",
            "llegué hoy sin reservar, ¿me puedo registrar?",
            "just arrived at the entrance, how do I register my group",
            "I just got to the park, need to register",
        ],
        "hard_negatives": ["a qué hora abren", "cuánto cuesta entrar", "necesito seguro para entrar"],
        "entities": {
            "sector": ["brisas", "cisne", "otun", "quindio_dulima"],
            "visitor_type": ["nacional", "extranjero"],
        },
        "needs": ["sector", "group_size", "visitor_type"],
        "action": "register_visit",
        "answer": {
            "short": (
                "Puedo preparar tu registro de llegada con el sector, cuántas personas van y el tipo de visitante. "
                "Te muestro el resumen y solo lo envío si confirmas; sin conexión no puedo garantizar que quede guardado. "
                "El registro oficial de ingreso se hace en el punto de registro del sector."
            ),
            "variants": [
                "Si ya estás en la entrada, dime el sector, cuántas personas son y el tipo de visitante. "
                "Confirma el resumen antes de enviarlo; el paso oficial sigue siendo el punto de registro del sector."
            ],
            "steps": [
                [
                    "Dime el sector en el que estás, el número de personas y el tipo de visitante.",
                    "Confirma el resumen que te muestro antes de que la app lo envíe.",
                ],
                [
                    "En el punto de registro del sector, sigue las indicaciones del personal para completar el ingreso.",
                ],
            ],
        },
        "sources": [SRC_PNN],
        "last_verified": VERIFIED,
        "valid_until": None,
        "related": ["actions.register_planned_visit", "actions.report_emergency_general"],
        "tags": ["llegada", "registro", "ingreso", "hoy"],
    },
    {
        "id": "actions.report_emergency_general",
        "label": "reportar una emergencia en el parque",
        "kind": "action",
        "audience": "visitor",
        "lang": "es",
        "examples": [
            "hay una emergencia",
            "quiero reportar una emergencia",
            "necesito ayuda urgente",
            "es una emergencia, ¿qué hago?",
            "cómo reporto una emergencia",
            "ayuda, emergencia aquí en el sendero",
            "socorro, necesitamos ayuda ya",
            "hay una situación de emergencia con mi grupo",
            "como reporto una emergencia en la montaña",
            "emergencia, mándame ayuda",
            "tengo una urgencia en el páramo",
            "I need to report an emergency",
            "emergency on the trail, how do I report it",
        ],
        "hard_negatives": ["qué hago si me pierdo", "qué es el mal de altura", "qué número llamar si me lastimo"],
        "entities": {},
        "needs": ["emergency_type", "sector", "people_count"],
        "action": "report_emergency",
        "answer": {
            "short": (
                "Si hay peligro inmediato, marca primero el 123 cuando tengas señal: es la línea única de emergencias del país y atiende las 24 horas. "
                "Luego puedo preparar tu reporte con el sector, el tipo de emergencia y cuántas personas están involucradas; no lo envío sin tu confirmación."
            ),
            "variants": [
                "Si la situación es urgente, marca primero el 123 cuando tengas señal; es la línea única de emergencias del país. "
                "Después dime el sector, el tipo de emergencia y cuántas personas están involucradas para preparar el reporte."
            ],
            "steps": [
                ["Si hay peligro inmediato, marca el 123 cuando tengas señal."],
                [
                    "Dime el tipo de emergencia, el sector y cuántas personas están involucradas para preparar el reporte.",
                ],
            ],
            "detail": (
                "La línea 123 atiende emergencias y seguridad. La Policía advierte que las llamadas de broma o sin motivo "
                "pueden impedir la atención de una emergencia real, así que úsala solo para una emergencia."
            ),
        },
        "sources": [SRC_123, SRC_PNN_GUIA],
        "last_verified": VERIFIED,
        "valid_until": None,
        "related": ["actions.report_injury", "actions.report_offline_emergency"],
        "tags": ["emergencia", "ayuda", "reporte", "urgencia"],
    },
    emergency_entry(
        entry_id="actions.report_injury",
        label="reportar una lesión o accidente",
        emergency_type="lesion",
        examples=[
            "se lastimó alguien del grupo",
            "se cayó y se lastimó la pierna",
            "reportar un accidente en el sendero",
            "mi amigo se torció el tobillo",
            "se fracturo la mano, no puede mover los dedos",
            "se cortó feo con una piedra",
            "se golpeó la cabeza al caer",
            "me caí y me duele mucho la rodilla",
            "reporte de lesión en la caminata",
            "compañero herido, no puede caminar",
            "one of my friends fell and hurt his leg",
            "a hiker got injured, can I report it?",
            "se pegó una caída feísima",
        ],
        hard_negatives=["primeros auxilios para un esguince", "qué hacer si te pierdes", "cuánto cuesta el seguro de accidentes"],
        short=(
            "Si la persona está herida o no puede caminar, marca primero el 123 cuando tengas señal. "
            "Puedo preparar un reporte de lesión con el sector, cuántas personas están involucradas y la referencia del sendero; lo envío solo si confirmas."
        ),
        variant=(
            "Si alguien se lastimó, marca el 123 cuando tengas señal. Después dime el sector, cuántas personas están involucradas "
            "y dónde ocurrió en el sendero, y confirma el reporte antes de enviarlo."
        ),
        steps=[
            [
                "Si hay una lesión grave, marca el 123 cuando tengas señal.",
                "Avisa a tu guía o agencia: según el parque, los guías registrados deben contar con equipo médico de respuesta y radios.",
            ],
            ["Dime el sector, cuántas personas están involucradas y la referencia del sendero para preparar el reporte."],
        ],
        related=["actions.report_emergency_general", "actions.report_lost_person"],
        tags=["lesión", "accidente", "herido", "caída"],
    ),
    emergency_entry(
        entry_id="actions.report_lost_person",
        label="reportar una persona perdida",
        emergency_type="persona_perdida",
        examples=[
            "se perdio mi amigo en el paramo",
            "no encuentro a mi grupo",
            "perdí de vista a mi hijo en el sendero",
            "una persona no volvió del recorrido",
            "persona desaparecida en la montaña",
            "mi compañero se separó del grupo y no aparece",
            "reportar persona extraviada",
            "se nos perdió un señor en la laguna",
            "alguien del grupo está perdido desde hace rato",
            "mi esposa se quedó atrás y no la veo",
            "se nos perdió la niña",
            "someone from my group is missing",
            "a person is lost on the trail, I need help",
        ],
        hard_negatives=["qué hago si me pierdo", "cómo leer el mapa del sendero", "qué debo llevar"],
        short=(
            "Si la persona está en peligro o no sabes dónde está, marca primero el 123 cuando tengas señal. "
            "Puedo preparar el reporte de persona perdida con el sector, cuántas personas faltan y la última referencia del recorrido; lo envío solo si confirmas."
        ),
        variant=(
            "Si alguien de tu grupo no aparece, pide ayuda ya: marca el 123 cuando tengas señal. Después dime el sector, "
            "cuántas personas faltan y la última referencia del recorrido que tuviste, y confirma el reporte antes de enviarlo."
        ),
        steps=[
            [
                "Si alguien no aparece, marca el 123 cuando tengas señal.",
                "Avisa a tu guía o agencia; según el parque, sus guías registrados deben contar con radios.",
            ],
            ["Dime el sector, cuántas personas faltan y la última referencia del recorrido para preparar el reporte."],
        ],
        related=["actions.report_injury", "actions.report_offline_emergency"],
        tags=["perdido", "desaparecido", "grupo", "búsqueda"],
    ),
    emergency_entry(
        entry_id="actions.report_altitude_sickness",
        label="reportar mal de altura de alguien",
        emergency_type="mal_de_altura",
        examples=[
            "mi compañera tiene mal de altura",
            "a alguien le dio soroche",
            "mi hermano está muy mareado por la altura",
            "se desmayó por la altura",
            "persona con dolor de cabeza fuerte en la cumbre",
            "le dio mal de montaña a mi amigo",
            "el soroche se puso grave",
            "mareo y vómito de un compañero por la altura",
            "reportar soroche",
            "tiene soroche y ya no habla bien",
            "altitude sickness, my friend is not well",
            "my friend has altitude sickness, how do I report it",
        ],
        hard_negatives=["qué es el mal de altura", "cómo se previene el soroche", "a qué altura es peligroso subir"],
        short=(
            "Si la persona está confundida, no responde o empeora, marca primero el 123 cuando tengas señal y no la dejes sola. "
            "Puedo preparar un reporte de mal de altura con el sector y cuántas personas están involucradas; lo envío solo si confirmas."
        ),
        variant=(
            "Si alguien del grupo tiene soroche y empeora, marca el 123 cuando tengas señal y avisa a tu guía. "
            "Dime el sector y cuántas personas están involucradas para preparar el reporte; no lo envío sin tu confirmación."
        ),
        steps=[
            [
                "Si hay confusión, pérdida de conocimiento o empeoramiento, marca el 123 cuando tengas señal.",
                "Avisa a tu guía, que según el parque debe contar con equipo médico de respuesta.",
            ],
            ["Para indicaciones de salud en altura, pregunta al asistente por ese tema."],
        ],
        related=["actions.report_emergency_general", "actions.report_hypothermia"],
        tags=["soroche", "mal de altura", "altura", "reporte"],
    ),
    emergency_entry(
        entry_id="actions.report_hypothermia",
        label="reportar hipotermia de una persona",
        emergency_type="hipotermia",
        examples=[
            "alguien tirita sin parar",
            "mi amigo está congelado y no habla bien",
            "compañero con hipotermia",
            "tiene frio y tirita mucho",
            "mi hermano está temblando y muy confundido",
            "se mojó con la lluvia y tiembla feo",
            "reporte de hipotermia en el páramo",
            "mi compañero se quedó sin fuerzas por el frío",
            "hay una persona con hipotermia en el sendero",
            "tiritando sin control, necesito ayuda",
            "someone is shivering uncontrollably and confused",
            "I think my friend has hypothermia, what do I report?",
        ],
        hard_negatives=["qué ropa llevar para el frío", "cómo se previene la hipotermia", "qué es la hipotermia"],
        short=(
            "Si la persona está confundida, no puede moverse o casi no habla, marca primero el 123 cuando tengas señal. "
            "Puedo preparar un reporte de hipotermia con el sector y cuántas personas están involucradas; lo envío solo si confirmas."
        ),
        variant=(
            "Si alguien tirita sin control o está confundido, marca el 123 cuando tengas señal. Dime el sector y cuántas personas "
            "están involucradas para preparar el reporte, que solo se envía con tu confirmación."
        ),
        steps=[
            [
                "Si la persona está confundida o no puede moverse, marca el 123 cuando tengas señal.",
                "Avisa a tu guía, que según el parque debe contar con equipo médico de respuesta.",
            ],
            ["Dime el sector y cuántas personas están involucradas para preparar el reporte."],
        ],
        related=["actions.report_altitude_sickness", "actions.report_storm"],
        tags=["hipotermia", "frío", "tiritar", "reporte"],
    ),
    emergency_entry(
        entry_id="actions.report_storm",
        label="reportar tormenta eléctrica cerca",
        emergency_type="tormenta_electrica",
        examples=[
            "hay tormenta electrica, ayuda",
            "caen rayos cerca del grupo",
            "nos cayó un rayo",
            "truenos y rayos en la cumbre",
            "tormenta con granizo y rayos en el páramo",
            "reportar tormenta con rayos",
            "hay rayos y no sabemos qué hacer",
            "se viene una tormenta eléctrica fuerte, avisa",
            "lightning storm near the lagoon, I need to report it",
            "lightning hit close to our group, what do I report",
            "está tronando muy duro y hay rayos",
            "rayo cayó cerca de la cabaña",
        ],
        hard_negatives=["pronóstico de lluvia para hoy", "qué hacer en una tormenta", "cómo llegar a la cabaña Potosí"],
        short=(
            "Si hay rayos cerca, sigue las indicaciones de tu guía o del personal del parque; si hay personas heridas, marca el 123 cuando tengas señal. "
            "Puedo preparar un reporte de tormenta eléctrica con el sector y cuántas personas están involucradas; lo envío solo si confirmas."
        ),
        variant=(
            "Con tormenta eléctrica, pide indicaciones a tu guía o al personal del parque. Si hay personas heridas, marca el 123 "
            "cuando tengas señal. Dime el sector y cuántas personas están involucradas para preparar el reporte."
        ),
        steps=[
            ["Si hay rayos cerca, sigue las indicaciones de tu guía o del personal del parque."],
            [
                "Si hay personas heridas, marca el 123 cuando tengas señal.",
                "Dime el sector y cuántas personas están involucradas para preparar el reporte.",
            ],
        ],
        related=["actions.report_fire", "actions.report_hypothermia"],
        tags=["tormenta", "rayos", "granizo", "reporte"],
    ),
    emergency_entry(
        entry_id="actions.report_fire",
        label="reportar un incendio en el sector",
        emergency_type="incendio",
        examples=[
            "hay fuego en el paramo",
            "se está quemando el pajonal",
            "incendio forestal cerca del sendero",
            "veo llamas en la montaña",
            "humo y fuego cerca de la laguna",
            "reportar candela en la montaña",
            "se prendió el monte, hay humo",
            "hay una quemada cerca del camino",
            "conato de incendio en el páramo",
            "there's a fire on the paramo",
            "wildfire near the trail, what do I do",
            "se ve fuego y mucho humo desde el sendero",
        ],
        hard_negatives=["qué está prohibido con fuego en el parque", "cómo cuidar el páramo", "qué es un pajonal"],
        short=(
            "Si ves fuego o mucho humo, aléjate de la zona y marca el 123 cuando tengas señal. "
            "Puedo preparar un reporte de incendio con el sector y cuántas personas están involucradas; lo envío solo si confirmas."
        ),
        variant=(
            "Si hay fuego en el páramo, aléjate y marca el 123 cuando tengas señal. Dime el sector y cuántas personas "
            "están involucradas para preparar el reporte; no lo envío sin tu confirmación."
        ),
        steps=[
            [
                "Aléjate del fuego y del humo, y marca el 123 cuando tengas señal.",
                "Si vas con guía, avísale: sus guías registrados deben contar con radios.",
            ],
            ["Dime el sector y cuántas personas están involucradas para preparar el reporte."],
        ],
        related=["actions.report_storm", "actions.report_emergency_general"],
        tags=["incendio", "fuego", "humo", "páramo"],
    ),
    emergency_entry(
        entry_id="actions.report_offline_emergency",
        label="reportar emergencia sin señal",
        emergency_type=None,
        examples=[
            "puedo reportar una emergencia sin señal",
            "reportar sin internet",
            "no tengo señal y hay emergencia",
            "se puede mandar la alerta sin datos",
            "la app sirve para emergencias sin conexion?",
            "sin señal, cómo aviso de una emergencia",
            "si no hay señal cómo pido ayuda",
            "reporto emergencia sin datos del celular",
            "emergencia y no tengo cobertura",
            "se puede reportar sin señal en el páramo",
            "can I report an emergency without signal",
            "no signal here, emergency, what do I do",
        ],
        hard_negatives=["dónde hay señal de celular", "qué hago si me pierdo", "cómo llegar a Brisas"],
        short=(
            "Sin señal no puedo garantizar que un reporte llegue al equipo de rescate ni que quede guardado. "
            "Si tienes señal, aunque sea poca, marca el 123 primero; si vas con guía, avísale de inmediato, porque según el parque debe contar con radios."
        ),
        variant=(
            "Si no hay señal, no te prometo que el reporte salga desde la app. Lo más seguro es conseguir señal para marcar el 123 "
            "o avisar a tu guía, que según el parque debe contar con radio y equipo médico de respuesta."
        ),
        steps=[
            [
                "Si tienes señal, marca el 123 primero.",
                "Si vas con guía o agencia, avísales de inmediato por radio o en persona.",
            ],
            [
                "Con señal, puedo preparar el reporte con el sector y cuántas personas están involucradas; revisa el resumen y confírmalo antes de enviarlo.",
            ],
        ],
        related=["actions.report_emergency_general", "actions.report_lost_person"],
        tags=["sin señal", "sin conexión", "offline", "emergencia"],
    ),
]

SECTION = {
    "contract_version": 1,
    "id": "actions",
    "order": 1,
    "title": "Registrar visita y reportar emergencia",
    "description": (
        "Acciones de la app: preparar el registro de una visita o un reporte de emergencia, siempre con tu confirmación. "
        "No garantiza envío ni guardado sin conexión; en una emergencia real, marca el 123 si tienes señal."
    ),
    "retrieval": {
        "profile": "safety",
        "bm25_weight": 0.3,
        "top_k": 2,
        "min_score": None,
        "entity_filters": ["sector", "date", "group_size", "visitor_type", "emergency_type", "people_count"],
    },
    "clarification": {
        "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
        "bank": [
            "¿Es una emergencia con peligro inmediato? Si lo es, marca primero el 123 cuando tengas señal.",
            "¿Quieres registrar una visita para otra fecha o estás llegando hoy?",
            "¿Qué tipo de emergencia es: lesión, persona perdida, mal de altura, hipotermia, tormenta eléctrica o incendio?",
            "¿Tienes señal en este momento o estás sin conexión?",
            "¿En qué sector estás: Brisas, Cisne, Otún o Quindío–Dulima?",
            "¿Cuántas personas están involucradas en la situación?",
        ],
        "slot_questions": SLOT_QUESTIONS,
        "fallback": (
            "Puedo ayudarte a registrar una visita o a preparar un reporte de emergencia. "
            "Si hay peligro inmediato, marca el 123 cuando tengas señal."
        ),
    },
    "featured": [
        "actions.report_emergency_general",
        "actions.report_offline_emergency",
        "actions.report_injury",
        "actions.register_planned_visit",
        "actions.report_lost_person",
    ],
    "entries": ENTRIES,
}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

_DIGIT = re.compile(r"\d")
# Phrases that would promise an outcome the offline assistant cannot guarantee.
_FORBIDDEN = [
    r"\bGPS\b",
    r"\bubicación exacta\b",
    r"\bya (quedó|quedo) (registrad|guardad|enviad)",
    r"\bse envió\b",
    r"\bse envio\b",
    r"\brescate (llegará|llegara|va en camino)\b",
    r"\btraduc",
    r"\bgener(a|ar) (texto|contenido)\b",
]


def _norm(text: str) -> str:
    """Accent-, case- and punctuation-insensitive key, so near-identical examples collide."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[^a-z0-9ñ ]+", " ", text).split())


# English markers for counting 1-2 English examples per entry. Words chosen so that no
# Spanish example matches them (e.g. "mi" is not "my", "reportar" is not "report").
_ENGLISH = re.compile(
    r"(\bI\b|\b(my|the|someone|there|need|how|can|what|just|near|with|without|signal|report|"
    r"fire|hiker|friend|trail|storm|lost|from|altitude|sickness|emergency|hypothermia|injured|"
    r"get|got|wildfire|missing|shivering|lightning|register|arrived|group|park|entrance|visit|"
    r"for|is|weekend|next|future|date|on)\b)"
)


def check_contract(section: dict) -> list[str]:
    errors: list[str] = []
    ids = [e["id"] for e in section["entries"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate entry ids")
    id_set = set(ids)
    seen_examples: dict[str, str] = {}
    entity_filters = set(section["retrieval"]["entity_filters"])
    slot_keys = set(section["clarification"].get("slot_questions", {}))

    for e in section["entries"]:
        eid = e["id"]
        if not eid.startswith(section["id"] + "."):
            errors.append(f"{eid}: id must start with section id")
        words = len(e["label"].split())
        if not 3 <= words <= 8:
            errors.append(f"{eid}: label has {words} words")
        if len(e["examples"]) < 12:
            errors.append(f"{eid}: only {len(e['examples'])} examples (min 12)")
        english = [x for x in e["examples"] if _ENGLISH.search(x)]
        if not 1 <= len(english) <= 2:
            errors.append(f"{eid}: {len(english)} English examples (need 1-2)")
        for ex in e["examples"]:
            key = _norm(ex)
            if key in seen_examples and seen_examples[key] != eid:
                errors.append(f"duplicate example '{ex}' in {eid} and {seen_examples[key]}")
            seen_examples.setdefault(key, eid)
        negs = e.get("hard_negatives", [])
        if not 2 <= len(negs) <= 4:
            errors.append(f"{eid}: {len(negs)} hard_negatives (need 2-4)")
        for ref in e.get("related", []):
            if ref not in id_set or ref == eid:
                errors.append(f"{eid}: related '{ref}' does not resolve to another entry")
        for need in e.get("needs", []):
            if need not in slot_keys:
                errors.append(f"{eid}: need '{need}' has no slot question")
        for ent in e.get("entities", {}):
            if ent not in entity_filters:
                errors.append(f"{eid}: entity '{ent}' not in retrieval.entity_filters")
        texts = [e["answer"]["short"], *e["answer"].get("variants", []), e["answer"].get("detail") or ""]
        texts += [t for level in e["answer"].get("steps", []) for t in level]
        if any(_DIGIT.search(t) for t in texts) and "last_verified" not in e:
            errors.append(f"{eid}: answer has digits but no last_verified")
        for t in texts:
            for pat in _FORBIDDEN:
                if re.search(pat, t, flags=re.IGNORECASE):
                    errors.append(f"{eid}: forbidden promise pattern {pat!r} in '{t[:60]}'")
        if e["kind"] == "action" and e.get("action") not in {"register_visit", "report_emergency"}:
            errors.append(f"{eid}: action must be register_visit or report_emergency")
        if not e["sources"]:
            errors.append(f"{eid}: no sources")

    for ref in section.get("featured", []):
        if ref not in id_set:
            errors.append(f"featured '{ref}' does not resolve")
    if not 3 <= len(section.get("featured", [])) <= 5:
        errors.append("featured must have 3-5 ids")
    bank = section["clarification"]["bank"]
    if not 4 <= len(bank) <= 8:
        errors.append(f"clarification.bank has {len(bank)} items (need 4-8)")
    for ent in entity_filters:
        if ent not in slot_keys:
            errors.append(f"entity_filter '{ent}' has no slot question")
    return errors


def check_schema(section: dict) -> list[str]:
    import jsonschema  # stdlib-adjacent dev dependency already present in this environment

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [f"schema: {'/'.join(map(str, err.path))}: {err.message}" for err in validator.iter_errors(section)]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(SECTION, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    errors = check_schema(SECTION) + check_contract(SECTION)
    counts = {e["id"]: len(e["examples"]) for e in SECTION["entries"]}
    print(f"entries={len(SECTION['entries'])} examples_total={sum(counts.values())}")
    for eid, n in counts.items():
        print(f"  {eid}: examples={n} hard_negatives={len(next(x for x in SECTION['entries'] if x['id'] == eid)['hard_negatives'])}")
    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print("  -", err)
        return 1
    print("VALIDATION OK: schema + contract rules")
    return 0


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: actions now builds from actions/source/actions.v1.json via coordination/build_from_snapshot.py actions; rerunning this script would revert reviewed corrections.")
    sys.exit(main())
