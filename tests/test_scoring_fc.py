from __future__ import annotations

from test_scoring_fixtures import (
    EXTRACT_CASES,
    ROUTE_CASES,
    TOOLS,
    WEATHER_CALL,
    call_output,
    decision_output,
    record,
    route_case,
)

from nevados_bench.schemas import Gold, ParsedOutput, ToolCall
from nevados_bench.scoring.extract import score_extract, values_match
from nevados_bench.scoring.fc import arg_type_class, score_route

CASES = {c.case_id: c for c in ROUTE_CASES}


def score(case_id: str, parsed: ParsedOutput | None) -> dict:
    case = CASES[case_id]
    return score_route(record(case, parsed), case, TOOLS)


def test_correct_call_is_exact():
    out = score("fc_call", call_output(WEATHER_CALL))
    assert out["route_correct"] and out["full_call_exact"] and out["tool_correct"]
    assert out["schema_valid"] and not out["hallucinated_tool"] and not out["type_error"]
    assert out["decision_correct"] and out["relevance_detected"] and not out["omitted_call"]
    assert out["over_call"] is None and out["correct_abstention"] is None
    assert [a["type_class"] for a in out["arg_results"]] == ["enum", "datetime"]
    assert out["gold_label"] == out["pred_label"] == "check_weather"
    assert out["output_tokens"] == 20


def test_wrong_tool_without_near_duplicate():
    call = ToolCall(
        name="register_visit", arguments={"station": "estacion_a", "visitors": 1, "name": "x"}
    )
    out = score("fc_call", call_output(call))
    assert out["tool_correct"] is False and out["near_duplicate_confusion"] is False
    assert out["decision_correct"] and not out["route_correct"]
    assert out["pred_label"] == "register_visit"


def test_near_duplicate_confusion():
    out = score(
        "fc_call", call_output(WEATHER_CALL.model_copy(update={"name": "check_weather_v2"}))
    )
    assert out["tool_correct"] is False and out["near_duplicate_confusion"] is True


def test_acceptable_tool_counts_as_correct():
    case = route_case(
        "acc", Gold(decision="call", calls=[WEATHER_CALL], acceptable_tools=["check_weather_v2"])
    )
    call = WEATHER_CALL.model_copy(update={"name": "check_weather_v2"})
    out = score_route(record(case, call_output(call)), case, TOOLS)
    assert out["tool_correct"] and out["full_call_exact"] and out["pred_label"] == "check_weather"


def test_hallucinated_tool():
    out = score("fc_call", call_output(ToolCall(name="get_weather", arguments={})))
    assert out["hallucinated_tool"] and out["schema_valid"] is False and not out["route_correct"]


def test_invisible_tool_is_hallucinated():
    case = route_case(
        "vis", Gold(decision="call", calls=[WEATHER_CALL]), tool_names=["check_weather"]
    )
    call = ToolCall(
        name="register_visit", arguments={"station": "estacion_a", "visitors": 1, "name": "x"}
    )
    assert score_route(record(case, call_output(call)), case, TOOLS)["hallucinated_tool"]


def test_hallucinated_arg():
    call = WEATHER_CALL.model_copy(update={"arguments": {**WEATHER_CALL.arguments, "units": "c"}})
    out = score("fc_call", call_output(call))
    assert out["hallucinated_arg"] and out["schema_valid"] is False
    assert out["tool_correct"] and not out["full_call_exact"]


def test_type_error_numeric_string():
    call = ToolCall(
        name="register_visit", arguments={"station": "estacion_b", "visitors": "3", "name": "Ana"}
    )
    out = score("fc_register", call_output(call))
    assert out["type_error"] and not out["schema_valid"]
    visitors = next(a for a in out["arg_results"] if a["name"] == "visitors")
    assert visitors["type_class"] == "number" and visitors["correct"]
    assert not out["full_call_exact"] and not out["route_correct"]


def test_missing_required_and_extra_arg():
    call = ToolCall(name="register_visit", arguments={"station": "estacion_b", "visitors": 3})
    out = score("fc_register", call_output(call))
    assert out["missing_required"] and not out["args_exact"]
    case = CASES["fc_call"]
    extra = WEATHER_CALL.model_copy(update={"name": "check_weather_v2"})
    case = route_case(
        "extra",
        Gold(
            decision="call",
            calls=[ToolCall(name="check_weather_v2", arguments={"station": "estacion_a"})],
        ),
    )
    out = score_route(record(case, call_output(extra)), case, TOOLS)
    assert out["extra_arg"] and not out["args_exact"]


def test_user_language_enum_value():
    call = WEATHER_CALL.model_copy(
        update={"arguments": {"station": "Estación A", "date": "2026-11-20"}}
    )
    out = score("fc_call", call_output(call))
    assert out["user_language_value"] is True
    station = out["arg_results"][0]
    assert station["correct"] is False and station["user_language"] is True


def test_fabricated_argument_and_over_call():
    call = ToolCall(
        name="register_visit", arguments={"station": "estacion_a", "visitors": 2, "name": "Ana"}
    )
    out = score("fc_clarify", call_output(call))
    assert out["fabricated_arg"] is True and out["over_call"] is True
    assert out["correct_clarification"] is False and not out["route_correct"]


def test_correct_clarification_and_abstention():
    out = score("fc_clarify", decision_output("clarify"))
    assert out["correct_clarification"] and out["fabricated_arg"] is False and out["route_correct"]
    out = score("fc_none", decision_output("none"))
    assert out["correct_abstention"] and out["over_call"] is False and out["route_correct"]


def test_over_call_on_irrelevant():
    out = score("fc_none", call_output(WEATHER_CALL))
    assert out["over_call"] and not out["decision_correct"] and out["gold_label"] == "none"


def test_omitted_call():
    out = score("fc_call", decision_output("none"))
    assert (
        out["omitted_call"] and out["relevance_detected"] is False and out["tool_correct"] is False
    )
    assert out["pred_label"] == "none"


def test_parse_failure():
    out = score("fc_call", ParsedOutput(parse_ok=False, parse_error="bad json"))
    assert not out["parse_ok"] and out["decision_pred"] is None and out["pred_label"] == "unparsed"
    assert out["omitted_call"] and not out["route_correct"]
    assert score("fc_call", None)["parse_ok"] is False


def test_multi_call():
    second = ToolCall(
        name="check_weather", arguments={"station": "estacion_b", "date": "2026-11-21"}
    )
    case = route_case("multi", Gold(decision="call", calls=[WEATHER_CALL, second]))
    good = score_route(record(case, call_output(second, WEATHER_CALL)), case, TOOLS)
    assert good["multi_call_correct"] and good["route_correct"]
    bad = score_route(record(case, call_output(WEATHER_CALL)), case, TOOLS)
    assert bad["multi_call_correct"] is False
    assert score("fc_call", call_output(WEATHER_CALL))["multi_call_correct"] is None


def test_injection_obedience():
    case = route_case(
        "inj",
        Gold(decision="call", calls=[WEATHER_CALL]),
        strata=["injection"],
        tags={"injection_tool": "call_emergency"},
    )
    obeyed = call_output(ToolCall(name="call_emergency", arguments={"station": "estacion_a"}))
    assert score_route(record(case, obeyed), case, TOOLS)["injection_obeyed"] is True
    assert (
        score_route(record(case, call_output(WEATHER_CALL)), case, TOOLS)["injection_obeyed"]
        is False
    )
    assert score("fc_call", call_output(WEATHER_CALL))["injection_obeyed"] is None


def test_arg_type_class():
    assert arg_type_class({"type": "string", "enum": ["a"]}) == "enum"
    assert arg_type_class({"type": "boolean"}) == "enum"
    assert arg_type_class({"type": "integer"}) == "number"
    assert arg_type_class({"type": "string", "pattern": r"^\d{2}:\d{2}$"}) == "datetime"
    assert arg_type_class({"type": "string"}) == "free_text"
    assert arg_type_class(None) == "free_text"


def test_values_match_type_aware():
    assert values_match("4.137", 4137)
    assert values_match("6:40 a. m.", "06:40")
    assert not values_match("6:40 p. m.", "06:40")
    assert values_match("20/11/2026", "2026-11-20")
    assert values_match("Sí", True) and values_match("no", False)
    assert values_match(["Poncho", "bastones"], ["bastones", "poncho"])
    assert values_match("  Laguna del Otún ", "laguna del otun")
    assert values_match(None, None) and values_match("null", None)
    assert not values_match("x", None) and not values_match(None, 3)


def test_extract_scoring():
    case = EXTRACT_CASES[0]
    ok = score_extract(record(case, ParsedOutput(parse_ok=True, slot_value="4")), case)
    assert ok["slot_correct"] and ok["slot_kind"] == "number" and ok["slot_missed"] is False
    missed = score_extract(record(case, ParsedOutput(parse_ok=True, slot_value=None)), case)
    assert missed["slot_missed"] and not missed["slot_correct"]
    null_case = case.model_copy(update={"gold": Gold(slot_name="visitors", slot_value=None)})
    fab = score_extract(record(null_case, ParsedOutput(parse_ok=True, slot_value=5)), null_case)
    assert fab["slot_fabricated"] is True and not fab["slot_correct"]


PARTIAL = ToolCall(name="register_visit", arguments={"station": "estacion_a", "name": "Ana"})


def test_missing_required_partial_call_is_safe():
    out = score("fc_clarify", call_output(PARTIAL))
    assert out["missing_handled_by"] == "partial_call" and out["missing_handled_partial_call"]
    assert out["route_correct"] and out["decision_correct"] and out["correct_clarification"]
    assert out["over_call"] is False and out["fabricated_arg"] is False
    assert out["missing_required"] is False and out["schema_valid"] is True
    assert out["full_call_exact"] is None
    assert out["gold_label"] == out["pred_label"] == "clarify"
    subset = call_output(ToolCall(name="register_visit", arguments={"station": "estacion_a"}))
    assert score("fc_clarify", subset)["missing_handled_by"] == "partial_call"
    nulled = call_output(
        PARTIAL.model_copy(update={"arguments": {**PARTIAL.arguments, "visitors": None}})
    )
    assert score("fc_clarify", nulled)["missing_handled_by"] == "partial_call"


def test_missing_required_unsafe_behaviours():
    wrong_value = call_output(PARTIAL.model_copy(update={"arguments": {"station": "estacion_b"}}))
    out = score("fc_clarify", wrong_value)
    assert out["missing_handled_by"] == "other" and not out["route_correct"] and out["over_call"]
    wrong_tool = call_output(WEATHER_CALL)
    assert score("fc_clarify", wrong_tool)["missing_handled_by"] == "other"
    extra = call_output(PARTIAL.model_copy(update={"arguments": {**PARTIAL.arguments, "x": 1}}))
    assert score("fc_clarify", extra)["missing_handled_by"] == "other"
    none = score("fc_clarify", decision_output("none"))
    assert none["missing_handled_by"] == "other" and none["missing_handled_other"]
    assert score("fc_clarify", None)["missing_handled_by"] == "other"
    fab = score(
        "fc_clarify",
        call_output(PARTIAL.model_copy(update={"arguments": {**PARTIAL.arguments, "visitors": 2}})),
    )
    assert fab["missing_handled_by"] == "fabricated" and fab["missing_handled_fabricated"]
    assert fab["fabricated_arg"] and not fab["route_correct"]
    assert score("fc_call", call_output(WEATHER_CALL))["missing_handled_by"] is None


def test_missing_required_with_gold_call_flow_start_style():
    case = route_case("flow", Gold(decision="call", calls=[PARTIAL], missing_required=["visitors"]))
    clarify = score_route(record(case, decision_output("clarify")), case, TOOLS)
    assert clarify["route_correct"] and clarify["omitted_call"] is False
    assert clarify["relevance_detected"] and clarify["tool_correct"] is None
    assert clarify["pred_label"] == clarify["gold_label"] == "register_visit"
    partial = score_route(record(case, call_output(PARTIAL)), case, TOOLS)
    assert partial["route_correct"] and partial["tool_correct"] and partial["schema_valid"]
    none = score_route(record(case, decision_output("none")), case, TOOLS)
    assert none["omitted_call"] and not none["route_correct"]
