from collections import Counter, defaultdict

import pytest

from nevados_bench.fsm.prompts import build_request, estimate_request_tokens
from nevados_bench.suites import fc
from nevados_bench.world import load_world

COMMON_TAGS = {"tools_n", "decision", "gold_tool", "safety"}


@pytest.fixture(scope="module")
def world():
    return load_world()


@pytest.fixture(scope="module")
def core(world):
    return fc.generate_fc_core(world)


@pytest.fixture(scope="module")
def tools_sweep(world):
    return fc.generate_fc_tools_sweep(world)


@pytest.fixture(scope="module")
def ctx_sweep(world):
    return fc.generate_fc_ctx_sweep(world)


@pytest.fixture(scope="module")
def smoke(world):
    return fc.generate_smoke(world)


@pytest.fixture(scope="module")
def all_cases(core, tools_sweep, ctx_sweep, smoke):
    return [*core, *tools_sweep, *ctx_sweep, *smoke]


# ----------------------------------------------------------------------------- composition


def test_core_composition(world, core):
    assert len(core) == 240
    assert Counter(c.gold.decision for c in core) == {"call": 144, "none": 56, "clarify": 40}
    assert {c.suite for c in core} == {"fc_core"}
    assert {c.call_type for c in core} == {"route"}
    assert {c.fsm_state for c in core} == {"ROUTER"}
    calls = [c for c in core if c.gold.decision == "call"]
    assert Counter(c.tags["gold_tool"] for c in calls) == dict.fromkeys(world.base_tools, 6)
    assert 8 <= sum(c.tags["multi_call"] for c in calls) <= 12
    for c in core:
        assert c.tags["multi_call"] == (len(c.gold.calls) > 1)


def test_core_strata(core):
    strata = Counter(s for c in core for s in c.strata)
    assert set(strata) == set(fc.STRATA)
    assert min(strata.values()) >= 20
    per_tool = defaultdict(set)
    for c in core:
        if c.gold.decision == "call":
            per_tool[c.tags["gold_tool"]].add(c.strata[0])
    assert all(len(s) >= 4 for s in per_tool.values())
    for c in core:
        expected = {"english": "en", "code_switch": "mixed"}.get(c.strata[0], "es")
        if not (c.strata == ["injection"] and c.language == "en"):
            assert c.language == expected


def test_injection_cases(world, core):
    injection = [c for c in core if c.tags["injection"]]
    assert sum(c.gold.decision == "none" for c in injection) == 12
    for c in injection:
        assert c.strata == ["injection"]
        tool = c.tags["injection_tool"]
        assert tool in world.tools
        assert tool in c.tool_names
        assert tool not in {call.name for call in c.gold.calls}


def test_core_tool_lists(world, core):
    for c in core:
        assert len(c.tool_names) == 8 == c.tags["tools_n"]
        assert len(set(c.tool_names)) == 8
        assert all(world.tools[t].near_duplicate_of is None for t in c.tool_names)
        gold = c.tags["gold_tool"]
        if gold is not None:
            assert fc.SIBLING[gold] in c.tool_names
    calls = [c for c in core if c.tags["gold_tool"]]
    for decision in ("call", "clarify"):
        labels = {c.tags["gold_position"] for c in calls if c.gold.decision == decision}
        assert labels == {"first", "middle", "last"}


def test_smoke(core, smoke):
    assert len(smoke) == 12
    assert Counter(c.gold.decision for c in smoke) == {"call": 6, "none": 3, "clarify": 3}
    by_id = {c.case_id: c for c in core}
    for c in smoke:
        assert c.suite == "smoke"
        assert c.strata == ["direct"]
        source = by_id[c.tags["source_case_id"]]
        assert source.user_message == c.user_message
        assert source.gold == c.gold


def test_tools_sweep(world, tools_sweep):
    assert len(tools_sweep) == 300
    bases = defaultdict(list)
    for c in tools_sweep:
        bases[c.tags["base_query_id"]].append(c)
    assert len(bases) == 60
    first = [cases[0] for cases in bases.values()]
    assert Counter(c.gold.decision for c in first) == {"call": 40, "none": 10, "clarify": 10}
    for cases in bases.values():
        assert sorted(c.tags["tools_n"] for c in cases) == list(fc.TOOL_COUNTS)
        assert len({c.user_message for c in cases}) == 1
        assert (
            len({c.tags["gold_position"] for c in cases}) >= 2 or cases[0].tags["gold_tool"] is None
        )
    for c in tools_sweep:
        n = c.tags["tools_n"]
        assert len(c.tool_names) == n == len(set(c.tool_names))
        gold = c.tags["gold_tool"]
        clones = [t for t in c.tool_names if world.tools[t].near_duplicate_of]
        if n < 48:
            assert not clones
        if gold is None:
            assert c.tags["gold_tool_position"] == "absent"
            continue
        assert gold in c.tool_names
        assert c.tags["gold_tool_position"] == fc._position_label(c.tool_names.index(gold), n)
        assert (fc.SIBLING[gold] in c.tool_names) == (n >= 6)
        has_clone = any(world.tools[t].near_duplicate_of == gold for t in c.tool_names)
        assert c.tags["near_duplicate"] == has_clone
    assert {c.tags["gold_tool_position"] for c in tools_sweep} == {
        "first",
        "middle",
        "last",
        "absent",
    }
    for c in tools_sweep:
        assert c.tags["near_duplicate"] == (
            c.tags["tools_n"] == 48 and c.tags["gold_tool"] is not None
        )
    for n in fc.TOOL_COUNTS:
        labels = {c.tags["gold_position"] for c in tools_sweep if c.tags["tools_n"] == n}
        assert labels == {"first", "middle", "last", "absent"}, n


# ----------------------------------------------------------------------------- shared lists


def _list_ids(cases):
    by_id = defaultdict(set)
    for c in cases:
        by_id[c.tags["tool_list_id"]].add(tuple(c.tool_names))
    assert all(len(v) == 1 for v in by_id.values())  # one id per ordered list
    return set(by_id)


def test_tool_list_id_matches_list(all_cases):
    assert all(c.tags["tool_list_id"] == fc.tool_list_id(c.tool_names) for c in all_cases)
    lists = {tuple(c.tool_names) for c in all_cases}
    assert len({fc.tool_list_id(list(t)) for t in lists}) == len(lists)


def test_shared_list_caps(core, tools_sweep, ctx_sweep, smoke):
    assert len(_list_ids(core)) <= 16
    assert len(_list_ids(ctx_sweep)) <= 8
    assert _list_ids(smoke) <= _list_ids(core)
    caps = {48: 3, 24: 3, 12: 6}
    for n, cap in caps.items():
        assert len(_list_ids([c for c in tools_sweep if c.tags["tools_n"] == n])) <= cap
    # Each shared list is reused by many cases.
    core_use = Counter(c.tags["tool_list_id"] for c in core)
    assert min(core_use.values()) >= 5


def test_full_and_base_sweep_lists(world, tools_sweep):
    for c in tools_sweep:
        n = c.tags["tools_n"]
        if n == 48:
            assert set(c.tool_names) == set(world.tools)
        if n == 24:
            assert set(c.tool_names) == set(world.base_tools)


def test_ctx_sweep(ctx_sweep):
    assert len(ctx_sweep) == 300
    bases = defaultdict(list)
    for c in ctx_sweep:
        bases[c.tags["base_query_id"]].append(c)
    assert len(bases) == 60
    for cases in bases.values():
        assert [c.context_level for c in cases] == list(fc.CONTEXT_LEVELS)
        assert len({tuple(c.tool_names) for c in cases}) == 1
        assert len(cases[0].tool_names) == 8
        assert not any(c.passage_ids for c in cases)


@pytest.mark.parametrize("mode", ["native", "uniform"])
def test_ctx_tokens_increase_with_level(world, ctx_sweep, mode):
    bases = defaultdict(list)
    for c in ctx_sweep:
        bases[c.tags["base_query_id"]].append(c)
    for cases in bases.values():
        tokens = [estimate_request_tokens(build_request(c, world, mode)) for c in cases]
        assert tokens == sorted(tokens), tokens
        assert tokens[-1] > tokens[0]
        assert tokens[1:] == sorted(set(tokens[1:])), tokens


# ----------------------------------------------------------------------------- gold labels


def test_gold_calls_validate(world, all_cases):
    for c in all_cases:
        if c.gold.decision == "call":
            assert c.gold.calls
            for call in c.gold.calls:
                assert world.validate_arguments(call.name, call.arguments) == [], c.case_id
                assert call.name in c.tool_names
            assert c.tags["gold_tool"] == c.gold.calls[0].name
            for name in c.gold.acceptable_tools:
                assert name in world.tools


def test_clarify_misses_required_args(world, all_cases):
    for c in [c for c in all_cases if c.gold.decision == "clarify"]:
        assert len(c.gold.calls) == 1
        call = c.gold.calls[0]
        assert call.name in c.tool_names
        assert c.gold.missing_required
        assert world.missing_required(call.name, call.arguments) == c.gold.missing_required
        for name, value in call.arguments.items():
            assert world.validate_value(name, value) == [], c.case_id


def test_none_cases_have_no_matching_tool(core):
    queries = {q.key: q for q in fc.core_queries()}
    by_text = {q.text: q for q in queries.values()}
    for c in core:
        if c.gold.decision != "none":
            continue
        assert not c.gold.calls and c.tags["gold_tool"] is None
        q = by_text[c.user_message]
        assert not set(q.avoid) & set(c.tool_names), c.case_id


def test_none_avoid_lists_cover_obvious_matches(world, core):
    # Keyword guard on top of the authored avoid lists: no visible tool for a topic the
    # out-of-domain question names explicitly.
    keyword_tools = {
        "horario": "get_opening_hours",
        "open": "get_opening_hours",
        "clima": "get_weather_forecast",
        "weather": "get_weather_forecast",
        "entrada": "get_entry_fee",
        "entrance": "get_entry_fee",
        "senderos": "list_trails",
    }
    for c in core:
        if c.gold.decision != "none" or c.tags["injection"]:
            continue
        text = c.user_message.lower()
        for word, tool in keyword_tools.items():
            if word in text:
                assert tool not in c.tool_names, (c.case_id, word)


def test_relative_dates_resolve_from_reference_date():
    from nevados_bench.fsm.prompts import REFERENCE_DATE

    assert REFERENCE_DATE.startswith(fc.TODAY)
    assert "jueves" in REFERENCE_DATE


# ----------------------------------------------------------------------------- invariants


def test_common_tags(all_cases, world):
    for c in all_cases:
        assert set(c.tags) >= COMMON_TAGS, c.case_id
        assert c.tags["decision"] == c.gold.decision
        assert c.tags["tools_n"] == len(c.tool_names)
        gold = c.tags["gold_tool"]
        assert c.tags["safety"] == bool(gold and world.tools[gold].safety)
        assert c.tags["gold_position"] == c.tags["gold_tool_position"]


def test_ids_unique_and_stable(world, all_cases):
    ids = [c.case_id for c in all_cases]
    assert len(ids) == len(set(ids))
    again = [
        *fc.generate_fc_core(world),
        *fc.generate_fc_tools_sweep(world),
        *fc.generate_fc_ctx_sweep(world),
        *fc.generate_smoke(world),
    ]
    assert [c.model_dump() for c in again] == [c.model_dump() for c in all_cases]
    assert ids[0] == "fc_core-0001"
    assert "tools_sweep-q017-n24" in ids


def test_priority_round_robin(core, tools_sweep):
    for suite in (core, tools_sweep):
        assert sorted(c.priority for c in suite) == list(range(len(suite)))
    head = sorted(core, key=lambda c: c.priority)[:27]
    assert {c.strata[0] for c in head} == set(fc.STRATA)
    assert {c.gold.decision for c in head} == {"call", "none", "clarify"}
    sweep_head = sorted(tools_sweep, key=lambda c: c.priority)[:30]
    assert {c.gold.decision for c in sweep_head} == {"call", "none", "clarify"}


def test_display_names_not_ids(world, core):
    ids = [*world.stations, *world.trails]
    for c in core:
        if c.tags["injection"]:
            continue  # attackers may spell canonical ids on purpose
        assert not any(i in c.user_message for i in ids), c.case_id


@pytest.mark.parametrize("mode", ["native", "uniform"])
def test_build_request_succeeds(world, all_cases, mode):
    for c in all_cases:
        request = build_request(c, world, mode)
        assert request.messages[-1]["content"] == c.user_message
        if mode == "native":
            assert [t["function"]["name"] for t in request.tools] == c.tool_names
        else:
            assert request.json_schema is not None
