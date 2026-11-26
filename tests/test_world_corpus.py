import re
from collections import Counter

import pytest

from nevados_bench.values import contains_named_value, extract_values
from nevados_bench.world import STATION_IDS, load_world

NUMERIC = re.compile(r"^(\d+|\d{2}:\d{2})$")
REAL_PLACE_NAMES = ["nevados", "otun", "cocora", "brisas", "cisne", "olleta", "santa isabel"]


@pytest.fixture(scope="module")
def world():
    return load_world()


def test_load_world_is_cached(world):
    assert load_world() is world


def test_counts(world):
    assert len(world.stations) == 4
    assert 110 <= len(world.passages) <= 130
    assert sum(p.safety for p in world.passages.values()) >= 24
    assert 12 <= sum(bool(p.prior_values) for p in world.passages.values()) <= 20


def test_station_ids_are_snake_case_and_fictional(world):
    for sid, station in world.stations.items():
        assert re.fullmatch(r"[a-z]+(_[a-z]+)*", sid)
        lowered = station.name.lower()
        assert not any(real in lowered for real in REAL_PLACE_NAMES)


def test_passage_ids_are_citable(world):
    for pid, passage in world.passages.items():
        assert pid == passage.id
        assert re.fullmatch(r"[A-Z0-9_-]+", pid)


def test_every_passage_states_one_to_three_values(world):
    for passage in world.passages.values():
        assert 1 <= len(passage.values) <= 3, passage.id


def test_values_are_machine_detectable(world):
    for passage in world.passages.values():
        numeric = {v for v in passage.values if NUMERIC.match(v)}
        # Exact equality: the text states no number that is not a declared trap value.
        assert extract_values(passage.text) == numeric, passage.id
        for value in passage.values:
            if not NUMERIC.match(value):
                assert contains_named_value(passage.text, value), (passage.id, value)


def test_numeric_values_are_globally_unique(world):
    counts = Counter(v for p in world.passages.values() for v in p.values if NUMERIC.match(v))
    assert [v for v, n in counts.items() if n > 1] == []


def test_priors_never_collide_with_corpus_values(world):
    corpus_values = {v for p in world.passages.values() for v in p.values}
    for passage in world.passages.values():
        for prior in passage.prior_values:
            assert prior not in corpus_values, (passage.id, prior)
            assert prior not in passage.values


def test_counterfactuals_are_mostly_safety(world):
    cf = [p for p in world.passages.values() if p.prior_values]
    assert sum(p.safety for p in cf) > len(cf) / 2


def test_same_field_exists_for_every_station(world):
    fields_by_station = {
        sid: {p.field for p in world.passages.values() if p.station == sid} for sid in STATION_IDS
    }
    common = set.intersection(*fields_by_station.values())
    assert len(common) >= 20
    assert "emergency_phone" in common


def test_station_passages_name_their_station(world):
    for passage in world.passages.values():
        if passage.station:
            assert world.station_name(passage.station) in passage.text


def test_gazetteer_has_one_entry_per_value_and_passage(world):
    expected = {(v, p.id) for p in world.passages.values() for v in p.values}
    got = [(e.value, e.passage_id) for e in world.gazetteer]
    assert len(got) == len(set(got))
    assert set(got) == expected
    for entry in world.gazetteer:
        passage = world.passages[entry.passage_id]
        assert (entry.station, entry.field) == (passage.station, passage.field)


def test_filler_has_no_digits_and_disjoint_ids(world):
    assert len(world.filler) >= 100
    assert not set(world.filler) & set(world.passages)
    for passage in world.filler.values():
        assert not re.search(r"\d", passage.text)
        assert passage.values == []


def test_trails_resolve_to_passages(world):
    assert len(world.trails) == 12
    for trail_id, trail in world.trails.items():
        passage = world.passages[world.trail_passage_id(trail_id)]
        assert passage.station == trail.station
        assert str(trail.length_m) in passage.values


def test_injection_passages_are_never_selected_implicitly(world):
    from nevados_bench.fsm.prompts import build_request
    from nevados_bench.schemas import Case, Gold, ToolCall
    from nevados_bench.world.corpus import INJECTION_FIELD

    injected = {pid for pid, p in world.passages.items() if p.field == INJECTION_FIELD}
    assert injected
    assert world.passage_ids_for(None, INJECTION_FIELD) == []
    assert not injected & set(world.filler)
    # No tool result ever returns an injection passage.
    for name in world.base_tools:
        spec = world.tools[name].parameters
        for station in STATION_IDS:
            args = {
                "station": station,
                "trail_id": world.stations[station].trails[0].id,
                "date": "2026-12-03",
                "visitor_type": "nacional",
                "group_size": 2,
                "people_count": 1,
                "emergency_type": "lesion",
                "item": "drones",
                "target_altitude_m": 4000,
            }
            call = ToolCall(name=name, arguments={k: args[k] for k in spec["required"]})
            assert not injected & set(world.execute_tool(call)["passage_ids"])
    # Padding at the largest level never pulls them in.
    case = Case(
        case_id="c",
        suite="t",
        call_type="answer",
        fsm_state="ROUTER",
        user_message="?",
        passage_ids=["EST-A-03"],
        context_level="8k",
        gold=Gold(),
    )
    system = build_request(case, world, "native").messages[0]["content"]
    assert not any(f"[{pid}]" in system for pid in injected)
    # Their marker values stay in the gazetteer, tagged with the injection field.
    markers = {e.passage_id for e in world.gazetteer if e.field == INJECTION_FIELD}
    assert markers == injected
