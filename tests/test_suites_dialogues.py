import datetime as dt
import json
import re
from collections import Counter

import pytest

from nevados_bench.fsm import prompts
from nevados_bench.fsm import states as S
from nevados_bench.fsm.driver import is_affirmative, is_cancel, is_plain_negative, run_dialogue
from nevados_bench.schemas import Completion, PromptRequest
from nevados_bench.suites import dialogues as DL
from nevados_bench.values import extract_values, normalize_text
from nevados_bench.world import load_world


@pytest.fixture(scope="module")
def world():
    return load_world()


@pytest.fixture(scope="module")
def traces(world):
    return DL.simulate(world)


@pytest.fixture(scope="module")
def dialogues(world):
    return DL.generate_dialogues(world)


def _steps(dialogues):
    return [s for d in dialogues for t in d.turns for s in t.steps]


def test_counts_and_depths(dialogues):
    assert len(dialogues) == 36
    assert Counter(d.depth for d in dialogues) == {3: 12, 6: 12, 12: 12}
    for d in dialogues:
        assert len(d.turns) == d.depth
    assert len({d.dialogue_id for d in dialogues}) == 36


def test_phenomena_coverage(dialogues):
    counts = Counter(p for d in dialogues for p in d.phenomena)
    for phenomenon in DL.PHENOMENA:
        assert counts[phenomenon] >= 8, phenomenon
    assert set(counts) == set(DL.PHENOMENA)
    # Both side-effect flows are exercised.
    tools = {c.name for s in _steps(dialogues) for c in s.gold.calls}
    assert {"register_visit", "report_emergency"} <= tools


def test_step_ids_suite_and_tags(dialogues):
    steps = _steps(dialogues)
    ids = [s.case_id for s in steps]
    assert len(ids) == len(set(ids))
    required = {
        "dialogue_id", "turn_index", "step_index", "depth", "phenomenon", "history_turns",
        "safety", "side_effect_pending", "gold_path",
    }  # fmt: skip
    for d in dialogues:
        for t_index, turn in enumerate(d.turns):
            for s_index, step in enumerate(turn.steps):
                assert step.suite == "dialogues"
                assert re.fullmatch(r"dlg-\d{2}-t\d{2}-s\d", step.case_id)
                assert step.case_id == f"{d.dialogue_id}-t{t_index:02d}-s{s_index}"
                assert required <= set(step.tags)
                assert step.tags["dialogue_id"] == d.dialogue_id
                assert step.tags["depth"] == d.depth
                assert step.tags["phenomenon"] in DL.PHENOMENA
                assert step.state_summary
                assert len(step.history) == 2 * t_index
                assert step.user_message == turn.user_message


def test_transitions_are_legal(dialogues):
    for step in _steps(dialogues):
        assert step.gold.next_state is not None
        assert S.can_transition(step.fsm_state, step.gold.next_state), step.case_id
        path = step.tags["gold_path"]
        S.check_path(path)
        assert path[0] == step.fsm_state and path[1] == step.gold.next_state


def test_gold_values_are_valid(world, dialogues):
    for step in _steps(dialogues):
        if step.call_type == "extract":
            assert step.slot_name == step.gold.slot_name
            if step.gold.slot_value is not None:
                assert not world.validate_value(step.slot_name, step.gold.slot_value)
                if step.slot_name == "date":
                    assert dt.date.fromisoformat(step.gold.slot_value).weekday() != 1
        elif step.call_type == "route":
            assert step.gold.decision == "call" and len(step.gold.calls) == 1
            call = step.gold.calls[0]
            assert call.name in step.tool_names
            if call.name in S.FLOW_STATE:
                for name, value in call.arguments.items():
                    assert not world.validate_value(name, value)
                assert step.tags["side_effect_pending"]
                assert step.gold.missing_required == world.missing_required(
                    call.name, call.arguments
                )
            else:
                assert not world.validate_arguments(call.name, call.arguments)
        else:
            assert step.passage_ids and step.gold.answerable
            assert step.gold.gold_passage_id in step.passage_ids
            shown = {v for p in step.passage_ids for v in world.passages[p].values}
            assert set(step.gold.gold_values) <= shown


def test_side_effect_pending_only_inside_flows(dialogues):
    for step in _steps(dialogues):
        if step.tags["side_effect_pending"]:
            assert "Trámite en curso: ninguno" not in step.state_summary or any(
                c.name in S.FLOW_STATE for c in step.gold.calls
            )


def test_driver_keywords_match_script(traces):
    for trace in traces:
        script = DL.SCRIPTS[int(trace.dialogue.dialogue_id[-2:]) - 1]
        for state, turn in zip(trace.turn_states, script, strict=True):
            msg = turn.message
            if isinstance(turn, DL.Cancel):
                assert is_cancel(msg) or (state == S.CONFIRM and is_plain_negative(msg)), msg
            elif state == S.SLOT_FILLING:
                assert not is_cancel(msg), msg
            elif state == S.CONFIRM:
                if isinstance(turn, DL.Confirm):
                    assert is_affirmative(msg), msg
                else:
                    assert not (is_affirmative(msg) or is_cancel(msg) or is_plain_negative(msg))


def test_extract_null_when_pending_slot_not_given(dialogues):
    for step in _steps(dialogues):
        if step.call_type == "extract" and step.gold.slot_value is None:
            assert step.tags["phenomenon"] in {"correction", "intent_switch"}


def test_state_summary_and_history_each_resolve_stations(world, dialogues):
    for step in _steps(dialogues):
        if step.call_type != "route":
            continue
        station = step.gold.calls[0].arguments.get("station")
        if not station:
            continue
        name = normalize_text(world.station_name(station).removeprefix("Estación "))
        if name in normalize_text(step.user_message):
            continue
        assert station in step.state_summary, step.case_id
        history = normalize_text(" ".join(m["content"] for m in step.history))
        assert name in history, step.case_id


def test_build_request_works_for_every_step(world, dialogues):
    for step in _steps(dialogues):
        for mode in ("native", "uniform"):
            request = prompts.build_request(step, world, mode)
            assert request.messages[-1]["role"] == "user"
        # Both arms: blanking one of the two sources still builds.
        prompts.build_request(step.model_copy(update={"history": []}), world, "native")
        prompts.build_request(step.model_copy(update={"state_summary": None}), world, "native")


def test_answer_replies_are_faithful(world, traces):
    for trace in traces:
        for turn, reply in zip(trace.dialogue.turns, trace.replies, strict=True):
            answers = [s for s in turn.steps if s.call_type == "answer"]
            if answers:
                numeric = {v for v in answers[0].gold.gold_values if v[0].isdigit()}
                assert numeric <= extract_values(reply)


def test_generation_is_deterministic(world, dialogues):
    again = DL.generate_dialogues(world)
    assert [d.model_dump() for d in again] == [d.model_dump() for d in dialogues]


# ----------------------------------------------------------------------------- free run


class OracleBackend:
    """Replays the gold output of each teacher-forced step, in order."""

    def __init__(self, dialogue):
        self.outputs = [s for t in dialogue.turns for s in t.steps]
        self.requests: list[PromptRequest] = []

    def complete(self, request: PromptRequest) -> Completion:
        self.requests.append(request)
        step = self.outputs.pop(0)
        if step.call_type == "route":
            call = step.gold.calls[0]
            return Completion(
                tool_calls=[{"name": call.name, "arguments": json.dumps(call.arguments)}]
            )
        if step.call_type == "extract":
            return Completion(content=json.dumps({"value": step.gold.slot_value}))
        return Completion(content=self._answers.pop(0))

    _answers: list[str]


@pytest.mark.parametrize("dialogue_id", [f"dlg-{n:02d}" for n in range(1, 37)])
def test_driver_replays_gold(world, traces, dialogue_id):
    trace = next(t for t in traces if t.dialogue.dialogue_id == dialogue_id)
    backend = OracleBackend(trace.dialogue)
    backend._answers = [
        reply
        for turn, reply in zip(trace.dialogue.turns, trace.replies, strict=True)
        if any(s.call_type == "answer" for s in turn.steps)
    ]
    steps = run_dialogue(trace.dialogue, backend, world, "native")
    assert backend.outputs == [] and backend._answers == []
    llm = [s for s in steps if s.kind == "llm"]
    gold = [s for t in trace.dialogue.turns for s in t.steps]
    assert len(llm) == len(gold)
    for got, want in zip(llm, gold, strict=True):
        assert got.call_type == want.call_type
        assert got.path[-1] == want.tags["gold_path"][-1], want.case_id
    # Same assistant replies turn by turn and same executed side effects.
    replies = {}
    for s in steps:
        if s.assistant_message is not None:
            replies[s.turn_index] = s.assistant_message
    assert [replies[i] for i in range(len(trace.replies))] == trace.replies
    executed = [
        s.executed_call
        for s in steps
        if s.executed_call is not None and world.tools[s.executed_call.name].has_side_effects
    ]
    assert executed == trace.executions == trace.dialogue.expected_executions
    assert steps[-1].state_after == trace.final_state


def test_expected_executions(world, dialogues):
    total = 0
    for d in dialogues:
        total += len(d.expected_executions)
        for call in d.expected_executions:
            assert world.tools[call.name].has_side_effects
            assert not world.validate_arguments(call.name, call.arguments)
            assert not world.missing_required(call.name, call.arguments)
    assert total == 17
