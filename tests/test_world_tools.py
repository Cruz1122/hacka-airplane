import re

import pytest
from jsonschema import Draft202012Validator

from nevados_bench.fsm.states import STATES
from nevados_bench.schemas import ToolCall
from nevados_bench.world import execute_tool, load_world
from nevados_bench.world.tools import EMERGENCY_TYPES, ITEMS

ALLOWED_KEYS = {"type", "enum", "properties", "required", "description"}


@pytest.fixture(scope="module")
def world():
    return load_world()


def _keys(schema):
    keys = set(schema)
    for prop in schema.get("properties", {}).values():
        keys |= _keys(prop)
    return keys


def test_tool_counts(world):
    assert len(world.base_tools) == 24
    assert len(world.clone_tools) == 24
    base = [world.tools[n] for n in world.base_tools]
    assert sum(t.safety for t in base) >= 6
    assert [t.name for t in world.tools.values() if t.has_side_effects] == [
        "report_emergency",
        "register_visit",
    ]


def test_tool_names_and_schemas(world):
    for name, spec in world.tools.items():
        assert re.fullmatch(r"[a-z]+(_[a-z]+)*", name)
        Draft202012Validator.check_schema(spec.parameters)
        assert spec.parameters["type"] == "object"
        assert _keys(spec.parameters) <= ALLOWED_KEYS, name
        assert spec.fsm_states and set(spec.fsm_states) <= set(STATES)


def test_side_effect_tools_need_multiple_slots(world):
    for name in ("register_visit", "report_emergency"):
        assert len(world.tools[name].parameters["required"]) >= 3


def test_clones_point_to_base_tools(world):
    for name in world.clone_tools:
        spec = world.tools[name]
        assert spec.near_duplicate_of in world.base_tools
        assert not spec.has_side_effects
        assert spec.description != world.tools[spec.near_duplicate_of].description
    originals = [world.tools[n].near_duplicate_of for n in world.clone_tools]
    assert sorted(originals) == sorted(world.base_tools)


SAMPLE_ARGS = {
    "station": "laguna_espejo",
    "trail_id": "sendero_mirlo",
    "date": "2026-12-03",
    "visitor_type": "extranjero",
    "group_size": 4,
    "people_count": 2,
    "emergency_type": "mal_de_altura",
    "item": "drones",
    "target_altitude_m": 4500,
    "report_code": "EMG-ABCDEF",
}


@pytest.mark.parametrize("name", load_world().base_tools)
def test_execute_every_base_tool(world, name):
    required = world.tools[name].parameters["required"]
    call = ToolCall(name=name, arguments={k: SAMPLE_ARGS[k] for k in required})
    result = world.execute_tool(call)
    assert result["ok"], result
    assert result["passage_ids"]
    for pid in result["passage_ids"]:
        assert pid in world.passages
    # Deterministic.
    assert world.execute_tool(call) == result


def test_execute_rejects_invalid_arguments(world):
    bad = [
        ToolCall(name="get_entry_fee", arguments={"station": "laguna_espejo"}),
        ToolCall(name="get_opening_hours", arguments={"station": "nevado_ruiz"}),
        ToolCall(name="check_daily_capacity", arguments={"station": "valle_bruma", "date": "3/12"}),
        ToolCall(name="get_opening_hours", arguments={"station": "valle_bruma", "extra": 1}),
        ToolCall(name="does_not_exist", arguments={}),
    ]
    for call in bad:
        result = execute_tool(call)
        assert not result["ok"] and result["error"]


def test_execute_results_come_from_the_requested_station(world):
    result = execute_tool(
        ToolCall(name="get_station_altitude", arguments={"station": "valle_bruma"})
    )
    assert [world.passages[p].station for p in result["passage_ids"]] == ["valle_bruma"]


def test_emergency_procedure_covers_every_type(world):
    for etype in EMERGENCY_TYPES:
        args = {"emergency_type": etype, "station": "alto_cenizo"}
        assert execute_tool(ToolCall(name="get_emergency_procedure", arguments=args))["ok"]
    for item in ITEMS:
        assert execute_tool(ToolCall(name="check_item_allowed", arguments={"item": item}))["ok"]


def test_registration_code_has_no_digits(world):
    args = {k: SAMPLE_ARGS[k] for k in ("station", "date", "group_size", "visitor_type")}
    result = execute_tool(ToolCall(name="register_visit", arguments=args))
    assert re.fullmatch(r"REG-[A-Z]{6}", result["data"]["codigo_registro"])


def test_alcohol_rule_has_its_own_passage(world):
    result = execute_tool(
        ToolCall(name="check_item_allowed", arguments={"item": "bebidas_alcoholicas"})
    )
    assert result["passage_ids"] == ["PAR-22"] and result["data"]["permitido"] is False
    assert world.passages["PAR-22"].field == "alcohol"
