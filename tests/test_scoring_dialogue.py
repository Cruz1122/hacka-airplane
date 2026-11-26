from __future__ import annotations

from test_scoring_fixtures import (
    GAZETTEER,
    PARTIAL_REGISTER,
    PASSAGES,
    TOOLS,
    call_output,
    completion,
    decision_output,
    make_dialogue,
    oracle_output,
    record,
)

from nevados_bench.report.aggregate import score_record
from nevados_bench.schemas import Completion, ParsedOutput, ToolCall
from nevados_bench.scoring.dialogue import (
    annotate_premature,
    dialogue_metric_rows,
    free_run_outcomes,
    premature_flags,
    teacher_forced_outcomes,
)
from nevados_bench.scoring.grounding import index_gazetteer

DIALOGUE = make_dialogue()
DIALOGUES = {"d1": DIALOGUE}
STEPS = {
    case.case_id: (t, s, case)
    for t, turn in enumerate(DIALOGUE.turns)
    for s, case in enumerate(turn.steps)
}
REGISTER = ToolCall(
    name="register_visit", arguments={"station": "estacion_a", "visitors": 4, "name": "Ana"}
)


def step_row(case_id: str, parsed: ParsedOutput, arm: str = "state_summary", rep: int = 0, **kw):
    turn, step, case = STEPS[case_id]
    tags = {"dialogue_id": "d1", "turn_index": turn, "step_index": step, "depth": 3, **case.tags}
    case = case.model_copy(update={"tags": tags})
    rec = record(case, parsed, arm=arm, rep=rep, fc_mode="uniform", **kw)
    return score_record(rec, case, TOOLS, PASSAGES, index_gazetteer(GAZETTEER))


def free_step(turn: int, step: int, parsed: ParsedOutput | None, rep: int = 0, *, kind="llm", **kw):
    """Free-run record: no gold case, identity as emitted by the orchestrator."""
    rec = record(
        None,
        parsed,
        suite="dialogues",
        case_id=f"d1:t{turn}:s{step}",
        arm="free_run",
        rep=rep,
        call_type="route" if kind == "llm" else None,
        tags={
            "dialogue_id": "d1",
            "turn_index": turn,
            "step_index": step,
            "depth": 3,
            "kind": kind,
        },
        completion=completion() if kind == "llm" else Completion(),
        ts=f"2026-11-14T00:00:{turn:02d}.{step}Z",
        **kw,
    )
    return score_record(rec, None, TOOLS, PASSAGES, index_gazetteer(GAZETTEER))


def free_run(rows: list[dict]) -> dict[int, dict]:
    annotate_premature(rows, TOOLS)
    return {o["rep"]: o for o in free_run_outcomes(rows, DIALOGUES, TOOLS)}


def confirmed_run(rep: int = 0, executed: ToolCall = REGISTER) -> list[dict]:
    return [
        free_step(0, 0, call_output(PARTIAL_REGISTER), rep, path=["ROUTER", "SLOT_FILLING"]),
        free_step(
            0, 1, ParsedOutput(parse_ok=True, slot_value=4), rep, path=["SLOT_FILLING", "CONFIRM"]
        ),
        free_step(
            1,
            0,
            None,
            rep,
            kind="code",
            path=["CONFIRM", "EXECUTE", "ANSWER"],
            executed_call=executed.model_dump(),
        ),
    ]


def test_premature_flags_follow_the_executed_path():
    def rows(*paths_and_calls):
        return [{"path": p, "executed_call": c} for p, c in paths_and_calls]

    ex = REGISTER.model_dump()
    ok = rows(
        (["ROUTER", "SLOT_FILLING"], None),
        (["SLOT_FILLING", "CONFIRM"], None),
        (["CONFIRM", "EXECUTE", "ANSWER"], ex),
    )
    assert premature_flags(ok, TOOLS) == [False, False, False]
    # Correction from CONFIRM back to SLOT_FILLING voids the earlier confirmation.
    voided = rows(
        (["SLOT_FILLING", "CONFIRM"], None),
        (["CONFIRM", "SLOT_FILLING"], None),
        (["SLOT_FILLING", "EXECUTE", "ANSWER"], ex),
    )
    assert premature_flags(voided, TOOLS) == [False, False, True]
    direct = rows((["ROUTER", "EXECUTE", "ANSWER"], ex))
    assert premature_flags(direct, TOOLS) == [True]
    info = rows((["ROUTER", "ANSWER"], {"name": "check_weather", "arguments": {}}))
    assert premature_flags(info, TOOLS) == [False]


def test_predicted_flow_tool_call_is_not_an_execution():
    # Teacher forcing: the gold behaviour at ROUTER is a flow-start call to register_visit.
    row = step_row("d1_t0_s0", call_output(PARTIAL_REGISTER))
    assert row["correct"] and row["missing_handled_by"] == "partial_call"
    annotate_premature([row], TOOLS)
    assert row["premature_execution"] is None


def test_teacher_forced_success_first_error_and_composition():
    good = [step_row(cid, oracle_output(STEPS[cid][2])) for cid in STEPS]
    assert all(r["correct"] and r["transition_correct"] for r in good)
    bad = [
        step_row("d1_t0_s0", oracle_output(STEPS["d1_t0_s0"][2]), rep=1),
        step_row("d1_t0_s1", oracle_output(STEPS["d1_t0_s1"][2]), rep=1),
        step_row("d1_t1_s0", decision_output("none"), rep=1),
    ]
    outcomes = {o["rep"]: o for o in teacher_forced_outcomes(good + bad, DIALOGUES)}
    assert outcomes[0]["success"] and outcomes[0]["first_error_turn"] is None
    assert not outcomes[1]["success"] and outcomes[1]["first_error_turn"] == 1
    # route accuracy 3/4, extract 2/2 -> product 0.75 * 1 * 0.75
    assert outcomes[0]["expected_success"] == 0.5625
    partial = teacher_forced_outcomes(good[:1], DIALOGUES)[0]
    assert not partial["complete"] and not partial["success"]


def test_clarify_is_also_safe_at_flow_start():
    row = step_row("d1_t0_s0", decision_output("clarify"))
    assert row["correct"] and row["missing_handled_by"] == "clarify"
    fabricated = step_row("d1_t0_s0", call_output(REGISTER))
    assert not fabricated["correct"] and fabricated["missing_handled_by"] == "fabricated"


def test_transition_uses_predicted_state_when_recorded():
    row = step_row("d1_t0_s0", decision_output("clarify"), next_state="ROUTER")
    assert row["correct"] and row["transition_correct"] is False


def test_free_run_success_against_expected_executions():
    out = free_run(confirmed_run())[0]
    assert out["success"] and out["side_effects_ok"] and not out["premature_execution"]
    assert out["missing_execution"] is False and out["extra_execution"] is False


def test_free_run_wrong_args_missing_extra_and_premature():
    wrong = REGISTER.model_copy(update={"arguments": {**REGISTER.arguments, "visitors": 5}})
    rows = confirmed_run(rep=0, executed=wrong)
    rows += confirmed_run(rep=1)[:2]  # never executed
    rows += [
        *confirmed_run(rep=2),
        free_step(
            2,
            0,
            None,
            2,
            kind="code",
            path=["CONFIRM", "EXECUTE", "ANSWER"],
            executed_call=REGISTER.model_dump(),
        ),
    ]
    rows += [
        free_step(
            0,
            0,
            call_output(REGISTER),
            3,
            kind="code",
            path=["ROUTER", "EXECUTE", "ANSWER"],
            executed_call=REGISTER.model_dump(),
        )
    ]
    out = free_run(rows)
    assert out[0]["wrong_args_execution"] and not out[0]["success"]
    assert out[1]["missing_execution"] and not out[1]["success"]
    assert out[2]["extra_execution"] and not out[2]["success"]
    assert out[3]["premature_execution"] and not out[3]["success"]
    flagged = [r for r in rows if r["rep"] == 3]
    assert flagged[0]["premature_execution"] is True


def test_free_run_loop_ignores_code_steps():
    rows = [
        free_step(i, 0, decision_output("clarify"), path=["ROUTER", "CLARIFY"]) for i in range(3)
    ]
    out = free_run(rows)[0]
    assert out["loop"] and out["repeats"] == 2 and not out["success"]
    codes = [free_step(i, 0, None, 1, kind="code", path=["CONFIRM", "ROUTER"]) for i in range(3)]
    assert not free_run(codes)[1]["loop"]


def test_dialogue_metric_rows_include_summary_delta_and_free_run():
    rows = []
    for arm in ("state_summary", "history_full"):
        for cid in STEPS:
            parsed = oracle_output(STEPS[cid][2])
            if arm == "history_full" and cid == "d1_t1_s0":
                parsed = decision_output("none")
            rows.append(step_row(cid, parsed, arm=arm))
    rows += confirmed_run()
    annotate_premature(rows, TOOLS)
    metrics, detail = dialogue_metric_rows(rows, DIALOGUES, TOOLS)
    by = {(m["metric"], m["slice_dim"], m["slice_value"]): m for m in metrics}
    assert by[("dialogue_success", "arm", "state_summary")]["value"] == 1.0
    assert by[("dialogue_success", "arm", "history_full")]["value"] == 0.0
    assert by[("dialogue_success", "arm", "free_run")]["value"] == 1.0
    assert by[("missing_execution", "arm", "free_run")]["value"] == 0.0
    assert by[("premature_execution", "arm", "free_run")]["value"] == 0.0
    assert ("premature_execution", "arm", "state_summary") not in by
    delta = by[("dialogue_success_delta_summary_minus_full", "depth", "3")]
    assert delta["value"] == 1.0 and delta["n"] == 1
    assert ("step_accuracy", "arm×phenomenon", "state_summary|correction") in by
    assert ("step_accuracy", "arm×side_effect_pending", "state_summary|True") in by
    assert ("extract_accuracy", "arm×turn_index", "state_summary|0") in by
    assert {d["arm"] for d in detail} == {"state_summary", "history_full", "free_run"}
