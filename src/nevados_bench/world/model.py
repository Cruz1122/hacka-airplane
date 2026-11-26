"""World container, argument validation and deterministic mock tool execution."""

from __future__ import annotations

import datetime as dt
import functools
import string
from dataclasses import dataclass, field
from typing import Any

from jsonschema import Draft202012Validator

from nevados_bench.schemas import GazetteerEntry, Passage, ToolCall, ToolSpec
from nevados_bench.world.corpus import (
    INJECTION_FIELD,
    STATIONS,
    TRAILS,
    Station,
    Trail,
    build_filler,
    build_passages,
    stable_hash,
)
from nevados_bench.world.tools import build_tools

# Park-wide passages returned by tools, keyed by field.
_PARK = {
    "rescue_line": "PAR-02",
    "police_contact": "PAR-03",
    "fire_brigade": "PAR-04",
    "lightning_protocol": "PAR-05",
    "hypothermia_protocol": "PAR-06",
    "sunscreen": "PAR-07",
    "max_visitor_altitude": "PAR-08",
    "acclimatization": "PAR-09",
    "insurance": "PAR-10",
    "drones": "PAR-11",
    "pets": "PAR-12",
    "camping": "PAR-13",
    "guide_requirement": "PAR-17",
    "lost_person_protocol": "PAR-21",
}
_ITEM_RULES = {
    "drones": ("PAR-11", False),
    "mascotas": ("PAR-12", False),
    "carpas": ("PAR-13", True),
    "bebidas_alcoholicas": ("PAR-22", False),
}
_FEE_FIELD = {
    "nacional": "entry_fee_national",
    "extranjero": "entry_fee_foreign",
    "reducida": "entry_fee_reduced",
}
_TRAIL_STATUS = ["abierto", "abierto con precaución", "cerrado temporalmente"]
_FORECAST = ["despejado en la mañana", "nublado con lloviznas", "niebla densa", "granizo aislado"]


@dataclass(frozen=True)
class World:
    stations: dict[str, Station]
    trails: dict[str, Trail]
    passages: dict[str, Passage]
    filler: dict[str, Passage]  # digit-free padding passages, never gold
    gazetteer: list[GazetteerEntry]
    tools: dict[str, ToolSpec]
    _by_field: dict[tuple[str | None, str], list[str]] = field(repr=False)

    # ------------------------------------------------------------------ lookups

    @property
    def base_tools(self) -> list[str]:
        return [n for n, t in self.tools.items() if t.near_duplicate_of is None]

    @property
    def clone_tools(self) -> list[str]:
        return [n for n, t in self.tools.items() if t.near_duplicate_of is not None]

    def get_passage(self, passage_id: str) -> Passage:
        """Corpus or filler passage by ID."""
        if passage_id in self.passages:
            return self.passages[passage_id]
        if passage_id in self.filler:
            return self.filler[passage_id]
        raise KeyError(f"unknown passage id: {passage_id}")

    def passage_ids_for(self, station: str | None, field_name: str) -> list[str]:
        return list(self._by_field.get((station, field_name), []))

    def trail_passage_id(self, trail_id: str) -> str:
        trail = self.trails[trail_id]
        for pid in self.passage_ids_for(trail.station, "trail"):
            if trail.name in self.passages[pid].text:
                return pid
        raise KeyError(f"no passage for trail {trail_id}")

    def station_name(self, station_id: str) -> str:
        return self.stations[station_id].name

    def slot_schema(self, slot_name: str) -> dict[str, Any]:
        """JSON Schema of a tool argument, looked up across all tools (first match)."""
        for tool in self.tools.values():
            prop = tool.parameters.get("properties", {}).get(slot_name)
            if prop is not None:
                return prop
        raise KeyError(f"unknown slot: {slot_name}")

    # --------------------------------------------------------------- validation

    def validate_value(self, slot_name: str, value: Any) -> list[str]:
        """Errors for a single argument value (empty when valid)."""
        schema = self.slot_schema(slot_name)
        errors = [e.message for e in Draft202012Validator(schema).iter_errors(value)]
        if not errors and slot_name == "date" and not _is_iso_date(value):
            errors.append(f"{value!r} is not an ISO date (YYYY-MM-DD)")
        return errors

    def validate_arguments(self, tool_name: str, arguments: Any) -> list[str]:
        """Errors for a full tool call: schema, unknown arguments and ISO dates."""
        if tool_name not in self.tools:
            return [f"unknown tool: {tool_name}"]
        schema = self.tools[tool_name].parameters
        if not isinstance(arguments, dict):
            return ["arguments must be an object"]
        errors = [e.message for e in Draft202012Validator(schema).iter_errors(arguments)]
        known = schema.get("properties", {})
        errors += [f"unexpected argument: {k}" for k in arguments if k not in known]
        if "date" in arguments and "date" in known and not _is_iso_date(arguments["date"]):
            errors.append(f"{arguments['date']!r} is not an ISO date (YYYY-MM-DD)")
        return errors

    def missing_required(self, tool_name: str, arguments: dict[str, Any]) -> list[str]:
        required = self.tools[tool_name].parameters.get("required", [])
        return [name for name in required if name not in arguments]

    # ---------------------------------------------------------------- execution

    def execute_tool(self, call: ToolCall) -> dict[str, Any]:
        """Deterministic mock result. Facts come only from corpus passages (by ID);
        ``data`` carries derived non-numeric facts (availability, status, codes)."""
        errors = self.validate_arguments(call.name, call.arguments)
        if errors:
            return {"ok": False, "tool": call.name, "error": "; ".join(errors)}
        spec = self.tools[call.name]
        if spec.near_duplicate_of is not None:
            return {"ok": True, "tool": call.name, "passage_ids": [], "data": {}}
        args = call.arguments
        station = args.get("station")
        key = f"{call.name}|{sorted(args.items())}"
        data: dict[str, Any] = {}

        def st(*fields: str) -> list[str]:
            return [pid for f in fields for pid in self.passage_ids_for(station, f)]

        def park(*fields: str) -> list[str]:
            return [_PARK[f] for f in fields]

        match call.name:
            case "get_opening_hours":
                pids = st("opening_hours", "last_entry")
            case "get_station_altitude":
                pids = st("altitude_m")
            case "get_station_services":
                pids = st("services")
            case "get_transport_options":
                pids = st("transport")
            case "get_entry_fee":
                pids = st(_FEE_FIELD[args["visitor_type"]])
            case "get_entry_requirements":
                pids = st("minimum_age") + park("insurance", "guide_requirement")
            case "check_daily_capacity":
                pids = st("daily_capacity")
                data["cupos_disponibles"] = stable_hash(key) % 4 != 0
            case "list_trails":
                pids = st("trail")
                data["senderos"] = [t.id for t in self.stations[station].trails]
            case "get_trail_details":
                pids = [self.trail_passage_id(args["trail_id"])]
            case "get_trail_conditions":
                pids = [self.trail_passage_id(args["trail_id"])]
                data["estado"] = _TRAIL_STATUS[stable_hash(key) % len(_TRAIL_STATUS)]
            case "get_required_gear":
                pids = st("required_gear") + park("sunscreen")
            case "get_weather_forecast":
                pids = st("weather_window")
                data["pronostico"] = _FORECAST[stable_hash(key) % len(_FORECAST)]
            case "get_weather_window":
                pids = st("weather_window")
            case "get_park_rules":
                pids = st("max_group_size", "prohibition") + park("drones", "pets", "camping")
            case "check_item_allowed":
                pid, allowed = _ITEM_RULES[args["item"]]
                pids = [pid]
                data["permitido"] = allowed
            case "get_flora_fauna_info":
                pids = st("flora_fauna")
            case "list_protected_species":
                pids = st("wildlife_distance")
            case "get_altitude_sickness_protocol":
                pids = st("altitude_sickness_protocol", "oxygen_point")
            case "get_acclimatization_advice":
                pids = park("acclimatization", "max_visitor_altitude")
                limit = int(self.passages["PAR-08"].values[0])
                data["altitud_permitida"] = args["target_altitude_m"] <= limit
            case "find_nearest_shelter":
                pids = st("storm_shelter") + park("lightning_protocol")
            case "get_emergency_contacts":
                pids = st("emergency_phone", "radio_channel") + park(
                    "rescue_line", "police_contact", "fire_brigade"
                )
            case "get_emergency_procedure":
                pids = self._procedure_passages(args["emergency_type"], station)
            case "report_emergency":
                pids = st("emergency_phone", "emergency_procedure")
                data["codigo_reporte"] = _letter_code("EMG", key)
            case "register_visit":
                pids = st("daily_capacity")
                data["codigo_registro"] = _letter_code("REG", key)
            case _:  # pragma: no cover - every base tool is handled above
                raise AssertionError(f"unhandled tool {call.name}")
        return {"ok": True, "tool": call.name, "passage_ids": pids, "data": data}

    def _procedure_passages(self, emergency_type: str, station: str) -> list[str]:
        mapping = {
            "mal_de_altura": self.passage_ids_for(station, "altitude_sickness_protocol"),
            "hipotermia": [_PARK["hypothermia_protocol"]],
            "lesion": self.passage_ids_for(station, "emergency_procedure"),
            "persona_perdida": [_PARK["lost_person_protocol"]],
            "tormenta_electrica": [
                _PARK["lightning_protocol"],
                *self.passage_ids_for(station, "storm_shelter"),
            ],
            "incendio": [_PARK["fire_brigade"]],
        }
        return mapping[emergency_type]


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _letter_code(prefix: str, key: str) -> str:
    # Letters only: a confirmation code must never look like a corpus number.
    h = stable_hash(key)
    letters = []
    for _ in range(6):
        h, r = divmod(h, 26)
        letters.append(string.ascii_uppercase[r])
    return f"{prefix}-{''.join(letters)}"


@functools.cache
def load_world() -> World:
    passages = build_passages()
    by_field: dict[tuple[str | None, str], list[str]] = {}
    for pid, passage in passages.items():
        # Injection passages are opt-in only (grounded_qa injection cases): never indexed by
        # field, so no tool result or field lookup can surface them implicitly.
        if passage.field != INJECTION_FIELD:
            by_field.setdefault((passage.station, passage.field), []).append(pid)
    # Injection markers stay in the gazetteer on purpose: field "prompt_injection" lets the
    # scorer classify a marker in an answer as obedience to the injection.
    gazetteer = [
        GazetteerEntry(value=value, passage_id=p.id, station=p.station, field=p.field)
        for p in passages.values()
        for value in p.values
    ]
    return World(
        stations=STATIONS,
        trails=TRAILS,
        passages=passages,
        filler=build_filler(),
        gazetteer=gazetteer,
        tools=build_tools(),
        _by_field=by_field,
    )


def execute_tool(call: ToolCall) -> dict[str, Any]:
    """Module-level convenience over ``load_world().execute_tool``."""
    return load_world().execute_tool(call)
