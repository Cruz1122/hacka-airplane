"""FSM states, transition table, tools visible per state and slot-filling metadata.

The table follows the plan's state diagram. Edges the diagram leaves implicit but the
free-run driver needs are marked below (topic states reaching ANSWER, CLARIFY/OUT_OF_SCOPE
returning to ROUTER, cancelling from CONFIRM).
"""

from __future__ import annotations

import itertools

from nevados_bench.world import World

ROUTER = "ROUTER"
STATION_INFO = "STATION_INFO"
TRAILS = "TRAILS"
ENTRY_REQUIREMENTS = "ENTRY_REQUIREMENTS"
ALTITUDE_SAFETY = "ALTITUDE_SAFETY"
WEATHER_GEAR = "WEATHER_GEAR"
FLORA_FAUNA = "FLORA_FAUNA"
REGULATIONS = "REGULATIONS"
VISIT_REGISTRATION = "VISIT_REGISTRATION"
EMERGENCY = "EMERGENCY"
OUT_OF_SCOPE = "OUT_OF_SCOPE"
CLARIFY = "CLARIFY"
SLOT_FILLING = "SLOT_FILLING"
CONFIRM = "CONFIRM"
EXECUTE = "EXECUTE"
ANSWER = "ANSWER"

STATES: tuple[str, ...] = (
    ROUTER,
    STATION_INFO,
    TRAILS,
    ENTRY_REQUIREMENTS,
    ALTITUDE_SAFETY,
    WEATHER_GEAR,
    FLORA_FAUNA,
    REGULATIONS,
    VISIT_REGISTRATION,
    EMERGENCY,
    OUT_OF_SCOPE,
    CLARIFY,
    SLOT_FILLING,
    CONFIRM,
    EXECUTE,
    ANSWER,
)

TOPIC_STATES: tuple[str, ...] = (
    STATION_INFO,
    TRAILS,
    ENTRY_REQUIREMENTS,
    ALTITUDE_SAFETY,
    WEATHER_GEAR,
    FLORA_FAUNA,
    REGULATIONS,
    EMERGENCY,
)

TRANSITIONS: dict[str, frozenset[str]] = {
    ROUTER: frozenset({*TOPIC_STATES, VISIT_REGISTRATION, EMERGENCY, OUT_OF_SCOPE, CLARIFY}),
    # Implicit in the diagram: every topic state can answer (diagram draws only three).
    **{s: frozenset({ANSWER}) for s in TOPIC_STATES if s != EMERGENCY},
    VISIT_REGISTRATION: frozenset({SLOT_FILLING}),
    EMERGENCY: frozenset({SLOT_FILLING, ANSWER}),  # ANSWER: informational emergency tools
    SLOT_FILLING: frozenset({SLOT_FILLING, CONFIRM, ROUTER}),
    CONFIRM: frozenset({EXECUTE, SLOT_FILLING, ROUTER}),  # ROUTER: user cancels (implicit)
    EXECUTE: frozenset({ANSWER}),
    ANSWER: frozenset({ROUTER}),
    OUT_OF_SCOPE: frozenset({ROUTER}),  # implicit
    CLARIFY: frozenset({ROUTER}),  # implicit
}

# Side-effect flows: tool -> (intent state, ordered required slots).
FLOW_STATE: dict[str, str] = {
    "register_visit": VISIT_REGISTRATION,
    "report_emergency": EMERGENCY,
}
REQUIRED_SLOTS: dict[str, list[str]] = {
    "register_visit": ["station", "date", "group_size", "visitor_type"],
    "report_emergency": ["station", "emergency_type", "people_count"],
}

SLOT_LABELS: dict[str, str] = {
    "station": "estación",
    "date": "fecha (AAAA-MM-DD)",
    "group_size": "número de personas del grupo",
    "visitor_type": "tipo de visitante (nacional, extranjero o reducida)",
    "emergency_type": "tipo de emergencia",
    "people_count": "número de personas afectadas",
    "trail_id": "sendero",
    "item": "objeto o actividad",
    "target_altitude_m": "altitud objetivo en metros",
    "report_code": "código del reporte",
}

SLOT_QUESTIONS: dict[str, str] = {
    "station": "¿A qué estación te refieres?",
    "date": "¿Para qué fecha? Indícala como AAAA-MM-DD.",
    "group_size": "¿Cuántas personas van en el grupo?",
    "visitor_type": "¿Qué tipo de visitante son: nacional, extranjero o tarifa reducida?",
    "emergency_type": (
        "¿Qué tipo de emergencia es: mal de altura, hipotermia, lesión, persona perdida, "
        "tormenta eléctrica o incendio?"
    ),
    "people_count": "¿Cuántas personas están afectadas?",
    "trail_id": "¿De qué sendero hablas?",
    "item": "¿Qué objeto o actividad quieres consultar?",
    "target_altitude_m": "¿A qué altitud en metros piensas subir?",
    "report_code": "¿Cuál es el código del reporte?",
}

TOOL_LABELS: dict[str, str] = {
    "register_visit": "el registro de la visita",
    "report_emergency": "el reporte de emergencia",
}


def can_transition(src: str, dst: str) -> bool:
    return dst in TRANSITIONS.get(src, frozenset())


def check_path(path: list[str]) -> None:
    """Raise ValueError if consecutive states in ``path`` are not legal transitions."""
    for src, dst in itertools.pairwise(path):
        if not can_transition(src, dst):
            raise ValueError(f"illegal FSM transition {src} -> {dst}")


def tool_topic(world: World, tool_name: str) -> str:
    """Intent state a tool belongs to (its first non-ROUTER state)."""
    return next(s for s in world.tools[tool_name].fsm_states if s != ROUTER)


def visible_tools(world: World, state: str, *, include_clones: bool = False) -> list[str]:
    """Tools visible in ``state``, in catalogue order. ROUTER sees every base tool."""
    return [
        name
        for name, spec in world.tools.items()
        if state in spec.fsm_states and (include_clones or spec.near_duplicate_of is None)
    ]
