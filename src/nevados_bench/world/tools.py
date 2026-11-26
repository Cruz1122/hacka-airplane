"""Tool catalogue: 24 base tools plus 24 near-duplicate clones that are never the gold answer.

Arguments are canonical (station/trail ids as enums, ISO dates, integers). Parameter schemas
use only simple JSON Schema constructs so every runtime grammar converter can handle them.
"""

from __future__ import annotations

from typing import Any

from nevados_bench.schemas import ToolSpec
from nevados_bench.world.corpus import STATION_IDS, TRAIL_IDS

VISITOR_TYPES = ["nacional", "extranjero", "reducida"]
EMERGENCY_TYPES = [
    "mal_de_altura",
    "hipotermia",
    "lesion",
    "persona_perdida",
    "tormenta_electrica",
    "incendio",
]
ITEMS = ["drones", "mascotas", "carpas", "bebidas_alcoholicas"]

_P: dict[str, dict[str, Any]] = {
    "station": {
        "type": "string",
        "enum": STATION_IDS,
        "description": "Identificador de la estación.",
    },
    "trail_id": {
        "type": "string",
        "enum": TRAIL_IDS,
        "description": "Identificador del sendero.",
    },
    "date": {"type": "string", "description": "Fecha en formato AAAA-MM-DD."},
    "visitor_type": {
        "type": "string",
        "enum": VISITOR_TYPES,
        "description": "Tipo de visitante o tarifa.",
    },
    "group_size": {"type": "integer", "description": "Número de personas del grupo."},
    "people_count": {"type": "integer", "description": "Número de personas afectadas."},
    "emergency_type": {
        "type": "string",
        "enum": EMERGENCY_TYPES,
        "description": "Tipo de emergencia.",
    },
    "item": {"type": "string", "enum": ITEMS, "description": "Objeto o actividad a consultar."},
    "target_altitude_m": {
        "type": "integer",
        "description": "Altitud objetivo en metros sobre el nivel del mar.",
    },
    "report_code": {"type": "string", "description": "Código del reporte de emergencia."},
}


def params(*required: str, optional: tuple[str, ...] = ()) -> dict[str, Any]:
    names = [*required, *optional]
    return {
        "type": "object",
        "properties": {name: dict(_P[name]) for name in names},
        "required": list(required),
    }


# (name, description, parameters, topic state, safety, side effects)
_BASE: list[tuple[str, str, dict[str, Any], str, bool, bool]] = [
    (
        "get_opening_hours",
        "Consulta el horario de apertura, cierre y último ingreso de una estación.",
        params("station"),
        "STATION_INFO",
        False,
        False,
    ),
    (
        "get_station_altitude",
        "Consulta la altitud en metros a la que está ubicada una estación.",
        params("station"),
        "STATION_INFO",
        False,
        False,
    ),
    (
        "get_station_services",
        "Consulta los servicios de una estación: cafetería, baños y parqueadero.",
        params("station"),
        "STATION_INFO",
        False,
        False,
    ),
    (
        "get_transport_options",
        "Consulta el bus rural hacia una estación: hora de salida y duración del trayecto.",
        params("station"),
        "STATION_INFO",
        False,
        False,
    ),
    (
        "get_entry_fee",
        "Consulta la tarifa de ingreso de una estación según el tipo de visitante.",
        params("station", "visitor_type"),
        "ENTRY_REQUIREMENTS",
        False,
        False,
    ),
    (
        "get_entry_requirements",
        "Consulta los requisitos de ingreso: edad mínima, seguro obligatorio y guía.",
        params("station"),
        "ENTRY_REQUIREMENTS",
        False,
        False,
    ),
    (
        "check_daily_capacity",
        "Consulta el aforo diario de una estación y si quedan cupos para una fecha.",
        params("station", "date"),
        "ENTRY_REQUIREMENTS",
        False,
        False,
    ),
    (
        "list_trails",
        "Lista los senderos que parten de una estación.",
        params("station"),
        "TRAILS",
        False,
        False,
    ),
    (
        "get_trail_details",
        "Consulta la longitud, la duración y la dificultad de un sendero.",
        params("trail_id"),
        "TRAILS",
        False,
        False,
    ),
    (
        "get_trail_conditions",
        "Consulta el estado de un sendero (abierto o cerrado) para una fecha.",
        params("trail_id", "date"),
        "TRAILS",
        False,
        False,
    ),
    (
        "get_required_gear",
        "Consulta el equipo obligatorio para ingresar a los senderos de una estación.",
        params("station"),
        "WEATHER_GEAR",
        False,
        False,
    ),
    (
        "get_weather_forecast",
        "Consulta el pronóstico del clima de una estación para una fecha concreta.",
        params("station", "date"),
        "WEATHER_GEAR",
        False,
        False,
    ),
    (
        "get_weather_window",
        "Consulta la franja horaria habitual de clima estable en una estación.",
        params("station"),
        "WEATHER_GEAR",
        False,
        False,
    ),
    (
        "get_park_rules",
        "Consulta las normas de una estación: tamaño máximo de grupo y prohibiciones.",
        params("station"),
        "REGULATIONS",
        False,
        False,
    ),
    (
        "check_item_allowed",
        "Consulta si un objeto o actividad está permitido en el parque.",
        params("item"),
        "REGULATIONS",
        False,
        False,
    ),
    (
        "get_flora_fauna_info",
        "Consulta las aves registradas y la especie emblemática de una estación.",
        params("station"),
        "FLORA_FAUNA",
        False,
        False,
    ),
    (
        "list_protected_species",
        "Consulta las normas de observación de mamíferos protegidos en una estación.",
        params("station"),
        "FLORA_FAUNA",
        False,
        False,
    ),
    (
        "get_altitude_sickness_protocol",
        "Consulta el protocolo ante mal de altura y el puesto de oxígeno de una estación.",
        params("station"),
        "ALTITUDE_SAFETY",
        True,
        False,
    ),
    (
        "get_acclimatization_advice",
        "Consulta las reglas de aclimatación y si una altitud objetivo está permitida.",
        params("target_altitude_m"),
        "ALTITUDE_SAFETY",
        True,
        False,
    ),
    (
        "find_nearest_shelter",
        "Consulta el refugio contra tormentas eléctricas más cercano a una estación.",
        params("station"),
        "ALTITUDE_SAFETY",
        True,
        False,
    ),
    (
        "get_emergency_contacts",
        "Consulta las líneas de emergencia, rescate y el canal de radio de una estación.",
        params("station"),
        "EMERGENCY",
        True,
        False,
    ),
    (
        "get_emergency_procedure",
        "Consulta qué hacer ante un tipo de emergencia en una estación.",
        params("emergency_type", "station"),
        "EMERGENCY",
        True,
        False,
    ),
    (
        "report_emergency",
        "Envía un reporte de emergencia al equipo de rescate. Requiere confirmación.",
        params("station", "emergency_type", "people_count", optional=("trail_id",)),
        "EMERGENCY",
        True,
        True,
    ),
    (
        "register_visit",
        "Registra una visita a una estación para una fecha y un grupo. Requiere confirmación.",
        params("station", "date", "group_size", "visitor_type"),
        "VISIT_REGISTRATION",
        False,
        True,
    ),
]

# (clone name, original, description, parameters or None to reuse the original's)
_CLONES: list[tuple[str, str, str, dict[str, Any] | None]] = [
    (
        "get_holiday_schedule",
        "get_opening_hours",
        "Consulta el calendario de eventos especiales que una estación programa en festivos.",
        None,
    ),
    (
        "get_peak_elevation",
        "get_station_altitude",
        "Consulta la altura de la cumbre nevada que se ve desde una estación.",
        None,
    ),
    (
        "list_souvenir_shop_items",
        "get_station_services",
        "Lista los recuerdos y artesanías a la venta en la tienda de una estación.",
        None,
    ),
    (
        "get_taxi_contacts",
        "get_transport_options",
        "Lista los contactos de taxis privados que llevan turistas hasta una estación.",
        None,
    ),
    (
        "get_annual_pass_price",
        "get_entry_fee",
        "Consulta el precio del pase anual para visitantes frecuentes de una estación.",
        None,
    ),
    (
        "get_volunteer_requirements",
        "get_entry_requirements",
        "Consulta los requisitos para inscribirse como voluntario del parque en una estación.",
        None,
    ),
    (
        "check_parking_availability",
        "check_daily_capacity",
        "Consulta si quedan cupos de parqueadero para vehículos en una estación y fecha.",
        None,
    ),
    (
        "list_cycling_routes",
        "list_trails",
        "Lista las rutas para bicicleta de montaña en los alrededores de una estación.",
        None,
    ),
    (
        "get_trail_map",
        "get_trail_details",
        "Devuelve el enlace al mapa descargable de un sendero.",
        None,
    ),
    (
        "get_trail_reviews",
        "get_trail_conditions",
        "Muestra las opiniones de otros visitantes sobre un sendero.",
        params("trail_id"),
    ),
    (
        "get_gear_rental_prices",
        "get_required_gear",
        "Consulta las tarifas de alquiler de equipo de montaña en una estación.",
        None,
    ),
    (
        "get_historical_weather",
        "get_weather_forecast",
        "Consulta estadísticas climáticas de años anteriores para una estación.",
        params("station"),
    ),
    (
        "get_sunrise_time",
        "get_weather_window",
        "Consulta la hora de salida del sol en una estación para una fecha.",
        params("station", "date"),
    ),
    (
        "get_photography_rules",
        "get_park_rules",
        "Consulta las normas para fotografía comercial y filmaciones profesionales.",
        None,
    ),
    (
        "check_lost_and_found",
        "check_item_allowed",
        "Busca un objeto entregado en la oficina de objetos perdidos del parque.",
        None,
    ),
    (
        "get_birdwatching_tours",
        "get_flora_fauna_info",
        "Lista los operadores de tours guiados de avistamiento de aves de una estación.",
        None,
    ),
    (
        "list_invasive_species",
        "list_protected_species",
        "Lista las especies invasoras que el parque está erradicando cerca de una estación.",
        None,
    ),
    (
        "get_altitude_training_plan",
        "get_altitude_sickness_protocol",
        "Sugiere un plan de entrenamiento físico previo para deportistas de alta montaña.",
        None,
    ),
    (
        "get_altitude_records",
        "get_acclimatization_advice",
        "Consulta las altitudes récord alcanzadas por expediciones históricas en el parque.",
        params("station"),
    ),
    (
        "find_nearest_restaurant",
        "find_nearest_shelter",
        "Consulta el restaurante más cercano a una estación.",
        None,
    ),
    (
        "get_tourism_office_contacts",
        "get_emergency_contacts",
        "Consulta los contactos de la oficina de turismo para trámites administrativos.",
        None,
    ),
    (
        "get_first_aid_course_info",
        "get_emergency_procedure",
        "Informa sobre los cursos de primeros auxilios que ofrece el parque en una estación.",
        params("station"),
    ),
    (
        "get_emergency_report_status",
        "report_emergency",
        "Consulta el estado de un reporte de emergencia ya enviado a partir de su código.",
        params("report_code"),
    ),
    (
        "estimate_visit_cost",
        "register_visit",
        "Calcula el costo estimado de una visita sin registrarla.",
        params("station", "group_size", "visitor_type"),
    ),
]

# Flow states where side-effect tools stay visible (code-driven slot filling and confirm).
_FLOW_EXTRA_STATES = ["SLOT_FILLING", "CONFIRM"]


def build_tools() -> dict[str, ToolSpec]:
    tools: dict[str, ToolSpec] = {}
    for name, description, parameters, topic, safety, side_effects in _BASE:
        states = ["ROUTER", topic, *(_FLOW_EXTRA_STATES if side_effects else [])]
        tools[name] = ToolSpec(
            name=name,
            description=description,
            parameters=parameters,
            has_side_effects=side_effects,
            safety=safety,
            fsm_states=states,
        )
    for name, original, description, parameters in _CLONES:
        base = tools[original]
        tools[name] = ToolSpec(
            name=name,
            description=description,
            parameters=parameters if parameters is not None else base.parameters,
            has_side_effects=False,
            safety=False,
            near_duplicate_of=original,
            fsm_states=[s for s in base.fsm_states if s not in _FLOW_EXTRA_STATES],
        )
    return tools
