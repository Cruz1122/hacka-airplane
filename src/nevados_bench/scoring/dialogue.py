"""FSM and dialogue scoring (catalog §4).

Works on *scored rows* (the dicts written to scored.jsonl), so per-step correctness is
always the one computed by fc / extract / grounding.

Arms:
- teacher forcing: every arm except `free_run` (the orchestrator uses `state_summary`
  and `history_full`). Each record is one step case evaluated from the gold state. A
  predicted call to a flow tool (e.g. `register_visit` at ROUTER or SLOT_FILLING) opens
  or corrects slot filling; it is never an execution, so premature execution does not
  apply to teacher-forced records (`tags.side_effect_pending` is only a slice).
- free run (`arm == "free_run"`, or `suite == "free_run"`): the FSM is driven by the
  model's own outputs. Records (`case_id == "<dialogue_id>:t<turn>:s<step>"`, no gold
  case) are grouped by `tags.dialogue_id` and ordered by `tags.turn_index`,
  `tags.step_index`, then `ts`. Code-only steps (`tags.kind == "code"`) carry the
  executions but are ignored for loop detection.

Definitions:
- transition correct: predicted next state (record field `next_state` or
  `tags.pred_next_state`) equals `gold.next_state`; without a predicted state the step's
  own correctness is used (under teacher forcing the FSM transition is a deterministic
  function of the step output).
- dialogue success (teacher forcing): every step case of the dialogue was run and is
  correct. Incomplete dialogues are excluded.
- expected success (composition of errors): product over the dialogue's steps of the
  model's accuracy on that step's call type within the same arm.
- premature execution (free run only): a side-effect tool was executed (record field
  `executed_call`, set only on the step where the driver executed it) and the dialogue's
  state sequence did not pass through CONFIRM since the flow (re)entered SLOT_FILLING.
  The sequence is the concatenation of each step's `path` (first = state before; falls
  back to `fsm_state`). Steps without an execution are not premature.
- free-run success: the ordered list of executed side-effect calls equals
  `Dialogue.expected_executions` exactly (same tools, same arguments, same order, none
  missing, none extra), no premature execution and no loop. Mismatches are reported as
  `missing_execution` (fewer executions than expected), `extra_execution` (more),
  `wrong_tool_execution` and `wrong_args_execution` (position-wise, same tool but
  different arguments).
- repeat: two consecutive steps with identical state and output; loop: three or more.
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Any

from nevados_bench.schemas import Case, Dialogue, RequestRecord, ToolCall, ToolSpec
from nevados_bench.scoring.extract import values_match
from nevados_bench.scoring.stats import mean, paired_delta, stable_seed
from nevados_bench.scoring.tidy import ModelKey, compact, mean_row, metric_row, model_key, rate_row

CONFIRM = "CONFIRM"
SLOT_FILLING = "SLOT_FILLING"
EXECUTE = "EXECUTE"
FREE_RUN = "free_run"
SUMMARY_ARM = "state_summary"
FULL_ARM = "history_full"
SUITE = "dialogues"


def transition_correct(record: RequestRecord, case: Case, step_correct: bool | None) -> bool | None:
    if case.gold.next_state is None:
        return None
    extra = record.model_extra or {}
    predicted = extra.get("next_state") or record.tags.get("pred_next_state")
    if predicted is not None:
        return str(predicted) == case.gold.next_state
    return step_correct


def executed_call(record: RequestRecord) -> dict[str, Any] | None:
    """The tool call the FSM executed for this step, if the runner recorded one."""
    extra = record.model_extra or {}
    call = extra.get("executed_call", record.tags.get("executed_call"))
    if isinstance(call, ToolCall):
        return call.model_dump()
    return call if isinstance(call, dict) else None


def fsm_path(record: RequestRecord) -> list[str] | None:
    extra = record.model_extra or {}
    path = extra.get("path", record.tags.get("path"))
    return [str(p) for p in path] if isinstance(path, list | tuple) else None


def is_side_effect(call: dict[str, Any] | None, tools: dict[str, ToolSpec]) -> bool:
    """Executed calls to tools unknown to the world are kept (they cannot be judged safe)."""
    if not call:
        return False
    spec = tools.get(str(call.get("name")))
    return spec is None or spec.has_side_effects


def premature_flags(rows: list[dict[str, Any]], tools: dict[str, ToolSpec]) -> list[bool]:
    """Per ordered free-run step: True when it executes a side effect without a CONFIRM
    since the flow last entered SLOT_FILLING (see module docstring)."""
    confirmed = False
    flags = []
    for row in rows:
        path = row.get("path") or [row.get("fsm_state") or ""]
        call = row.get("executed_call")
        executes = is_side_effect(call, tools)
        flag = False
        evaluated = False
        for state in path:
            if state == SLOT_FILLING:
                confirmed = False
            elif state == CONFIRM:
                confirmed = True
            elif state == EXECUTE and executes and not evaluated:
                flag, evaluated = not confirmed, True
        if executes:
            if not evaluated:
                flag = not confirmed
            confirmed = False  # the flow is over once executed
        flags.append(flag)
    return flags


def is_free_run(row: dict[str, Any]) -> bool:
    """`free_run` and its variants (`free_run_guarded`, ...), each scored as its own arm."""
    return str(row.get("arm") or "").startswith(FREE_RUN) or row.get("suite") == FREE_RUN


def dialogue_steps(dialogue: Dialogue) -> list[tuple[int, int, Case]]:
    return [
        (turn_index, step_index, case)
        for turn_index, turn in enumerate(dialogue.turns)
        for step_index, case in enumerate(turn.steps)
    ]


def _step_order(row: dict[str, Any]) -> tuple[Any, ...]:
    tags = row.get("tags", {})
    return (tags.get("turn_index", 0), tags.get("step_index", 0), row.get("ts", ""))


def teacher_forced_outcomes(
    rows: list[dict[str, Any]], dialogues: dict[str, Dialogue]
) -> list[dict[str, Any]]:
    """One outcome per model key x arm x rep x dialogue (teacher-forced arms only)."""
    by_group: dict[tuple[Any, ...], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if is_free_run(row):
            continue
        dialogue_id = row.get("tags", {}).get("dialogue_id")
        if dialogue_id not in dialogues:
            continue
        group = (model_key(row), row.get("arm"), row.get("rep", 0), dialogue_id)
        by_group[group][row["case_id"]] = row
    accuracy = _call_type_accuracy(rows)
    outcomes = []
    for (key, arm, rep, dialogue_id), seen in sorted(by_group.items(), key=lambda kv: str(kv[0])):
        dialogue = dialogues[dialogue_id]
        steps = dialogue_steps(dialogue)
        complete = all(case.case_id in seen for _, _, case in steps)
        errors = [
            turn
            for turn, _, case in steps
            if case.case_id in seen and not seen[case.case_id]["correct"]
        ]
        expected = 1.0
        for _, _, case in steps:
            expected *= accuracy.get((key, arm, case.call_type), 0.0)
        outcomes.append(
            {
                "key": key,
                "arm": arm,
                "rep": rep,
                "dialogue_id": dialogue_id,
                "depth": dialogue.depth,
                "phenomena": list(dialogue.phenomena),
                "steps_expected": len(steps),
                "steps_run": sum(1 for _, _, case in steps if case.case_id in seen),
                "complete": complete,
                "success": (complete and not errors),
                "first_error_turn": min(errors) if errors else None,
                "expected_success": expected,
            }
        )
    return outcomes


def _call_type_accuracy(rows: list[dict[str, Any]]) -> dict[tuple[Any, ...], float]:
    buckets: dict[tuple[Any, ...], list[bool]] = defaultdict(list)
    for row in rows:
        if not is_free_run(row) and row.get("correct") is not None:
            buckets[(model_key(row), row.get("arm"), row.get("call_type"))].append(
                bool(row["correct"])
            )
    return {k: sum(v) / len(v) for k, v in buckets.items()}


def _call_matches(pred: dict[str, Any], gold: ToolCall) -> bool:
    if pred.get("name") != gold.name:
        return False
    args = pred.get("arguments", {})
    return set(args) == set(gold.arguments) and all(
        values_match(args[name], value) for name, value in gold.arguments.items()
    )


def _free_run_groups(rows: list[dict[str, Any]]) -> dict[tuple[Any, ...], list[dict[str, Any]]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if is_free_run(row):
            dialogue_id = row.get("tags", {}).get("dialogue_id")
            arm = str(row.get("arm") or FREE_RUN)
            groups[(model_key(row), arm, row.get("rep", 0), dialogue_id)].append(row)
    for group in groups.values():
        group.sort(key=_step_order)
    return dict(sorted(groups.items(), key=lambda kv: str(kv[0])))


def annotate_premature(rows: list[dict[str, Any]], tools: dict[str, ToolSpec]) -> None:
    """Set `premature_execution` on free-run rows (in place); None on every other row."""
    for row in rows:
        row["premature_execution"] = None
    for group in _free_run_groups(rows).values():
        for row, flag in zip(group, premature_flags(group, tools), strict=True):
            row["premature_execution"] = flag


def free_run_outcomes(
    rows: list[dict[str, Any]], dialogues: dict[str, Dialogue], tools: dict[str, ToolSpec]
) -> list[dict[str, Any]]:
    """One outcome per model key x rep x dialogue for `free_run` records."""
    outcomes = []
    for (key, arm, rep, dialogue_id), group in _free_run_groups(rows).items():
        llm = [r for r in group if r.get("tags", {}).get("kind") != "code"]
        signatures = [(r.get("fsm_state"), r.get("output_signature")) for r in llm]
        run = longest = 1
        repeats = 0
        for prev, cur in itertools.pairwise(signatures):
            if cur == prev:
                repeats += 1
                run += 1
                longest = max(longest, run)
            else:
                run = 1
        premature = any(premature_flags(group, tools))
        executed = [
            r["executed_call"] for r in group if is_side_effect(r.get("executed_call"), tools)
        ]
        dialogue = dialogues.get(dialogue_id)
        loop = longest >= 3
        out = {
            "key": key,
            "arm": arm,
            "rep": rep,
            "dialogue_id": dialogue_id,
            "depth": dialogue.depth if dialogue else None,
            "steps_run": len(group),
            "executions": len(executed),
            "premature_execution": premature,
            "repeats": repeats,
            "repeat": repeats > 0,
            "loop": loop,
            "side_effects_ok": None,
            "missing_execution": None,
            "extra_execution": None,
            "wrong_tool_execution": None,
            "wrong_args_execution": None,
            "success": None,
        }
        if dialogue is not None:
            expected = dialogue.expected_executions
            pairs = list(zip(executed, expected, strict=False))
            wrong_tool = any(p.get("name") != g.name for p, g in pairs)
            wrong_args = any(p.get("name") == g.name and not _call_matches(p, g) for p, g in pairs)
            effects_ok = len(executed) == len(expected) and all(
                _call_matches(p, g) for p, g in pairs
            )
            out.update(
                side_effects_ok=effects_ok,
                missing_execution=len(executed) < len(expected),
                extra_execution=len(executed) > len(expected),
                wrong_tool_execution=wrong_tool,
                wrong_args_execution=wrong_args,
                success=bool(effects_ok and not premature and not loop),
            )
        outcomes.append(out)
    return outcomes


def _phenomena(row: dict[str, Any]) -> list[str]:
    value = row.get("tags", {}).get("phenomenon", row.get("phenomena"))
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def dialogue_metric_rows(
    rows: list[dict[str, Any]], dialogues: dict[str, Dialogue], tools: dict[str, ToolSpec]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """(tidy metric rows for dialogue_rates.csv, per-dialogue detail rows)."""
    steps = [r for r in rows if r.get("tags", {}).get("dialogue_id") is not None]
    out: list[dict[str, Any] | None] = []
    by_key: dict[ModelKey, list[dict[str, Any]]] = defaultdict(list)
    for row in steps:
        by_key[model_key(row)].append(row)
    tf = teacher_forced_outcomes(steps, dialogues)
    fr = free_run_outcomes(steps, dialogues, tools)
    for key, key_rows in sorted(by_key.items()):
        slices: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in key_rows:
            arm = str(row.get("arm"))
            tags = row.get("tags", {})
            slices[("arm", arm)].append(row)
            slices[("arm×depth", f"{arm}|{tags.get('depth')}")].append(row)
            slices[("arm×turn_index", f"{arm}|{tags.get('turn_index')}")].append(row)
            slices[("arm×fsm_state", f"{arm}|{row.get('fsm_state')}")].append(row)
            if tags.get("side_effect_pending") is not None:
                pending = tags["side_effect_pending"]
                slices[("arm×side_effect_pending", f"{arm}|{pending}")].append(row)
            for phen in _phenomena(row):
                slices[("arm×phenomenon", f"{arm}|{phen}")].append(row)
        for (dim, value), srows in sorted(slices.items()):
            out.append(
                rate_row(key, SUITE, dim, value, "step_accuracy", (r.get("correct") for r in srows))
            )
            out.append(
                rate_row(
                    key,
                    SUITE,
                    dim,
                    value,
                    "transition_accuracy",
                    (r.get("transition_correct") for r in srows),
                )
            )
            out.append(
                rate_row(
                    key,
                    SUITE,
                    dim,
                    value,
                    "extract_accuracy",
                    (r.get("correct") for r in srows if r.get("call_type") == "extract"),
                )
            )
            out.append(
                rate_row(
                    key,
                    SUITE,
                    dim,
                    value,
                    "premature_execution",
                    (r.get("premature_execution") for r in srows if is_free_run(r)),
                )
            )
        out.extend(_outcome_rows(key, [o for o in tf if o["key"] == key]))
        out.extend(_free_run_rows(key, [o for o in fr if o["key"] == key]))
        out.extend(_summary_delta_rows(key, key_rows, [o for o in tf if o["key"] == key]))
    detail = [
        {**_key_dict(o["key"]), **{k: v for k, v in o.items() if k != "key"}} for o in tf + fr
    ]
    return compact(out), detail


def _key_dict(key: ModelKey) -> dict[str, str]:
    return dict(zip(("model_id", "quant", "profile", "fc_mode"), key, strict=True))


def _outcome_rows(key: ModelKey, outcomes: list[dict[str, Any]]) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for o in outcomes:
        if not o["complete"]:
            continue
        groups[("arm", o["arm"])].append(o)
        groups[("arm×depth", f"{o['arm']}|{o['depth']}")].append(o)
        for phen in o["phenomena"]:
            groups[("arm×phenomenon", f"{o['arm']}|{phen}")].append(o)
    for (dim, value), group in sorted(groups.items()):
        rows.append(
            rate_row(key, SUITE, dim, value, "dialogue_success", (o["success"] for o in group))
        )
        expected = [o["expected_success"] for o in group]
        rows.append(mean_row(key, SUITE, dim, value, "dialogue_success_expected_product", expected))
        observed = mean([1.0 if o["success"] else 0.0 for o in group])
        exp = mean(expected)
        if observed is not None and exp is not None:
            rows.append(
                metric_row(
                    key,
                    SUITE,
                    dim,
                    value,
                    "composition_gap_observed_minus_product",
                    len(group),
                    observed - exp,
                )
            )
        rows.append(
            mean_row(
                key,
                SUITE,
                dim,
                value,
                "first_error_turn",
                (o["first_error_turn"] for o in group if o["first_error_turn"] is not None),
            )
        )
    return rows


def _free_run_rows(key: ModelKey, outcomes: list[dict[str, Any]]) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for o in outcomes:
        groups[("arm", o["arm"])].append(o)
        groups[("arm×depth", f"{o['arm']}|{o['depth']}")].append(o)
    for (dim, value), group in sorted(groups.items()):
        rows.append(
            rate_row(key, SUITE, dim, value, "dialogue_success", (o["success"] for o in group))
        )
        for flag in (
            "missing_execution",
            "extra_execution",
            "wrong_tool_execution",
            "wrong_args_execution",
            "side_effects_ok",
        ):
            rows.append(rate_row(key, SUITE, dim, value, flag, (o[flag] for o in group)))
        rows.append(
            rate_row(
                key,
                SUITE,
                dim,
                value,
                "dialogue_premature_execution",
                (o["premature_execution"] for o in group),
            )
        )
        rows.append(rate_row(key, SUITE, dim, value, "dialogue_loop", (o["loop"] for o in group)))
        rows.append(
            rate_row(key, SUITE, dim, value, "dialogue_repeat", (o["repeat"] for o in group))
        )
        rows.append(
            mean_row(key, SUITE, dim, value, "repeats_per_dialogue", (o["repeats"] for o in group))
        )
    return rows


def _summary_delta_rows(
    key: ModelKey, rows: list[dict[str, Any]], outcomes: list[dict[str, Any]]
) -> list[dict[str, Any] | None]:
    """state_summary minus history_full by depth, paired on (case, rep) / (dialogue, rep)."""
    out: list[dict[str, Any] | None] = []
    steps: dict[str, dict[tuple[Any, ...], dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row.get("arm") in (SUMMARY_ARM, FULL_ARM) and row.get("correct") is not None:
            steps[row["arm"]][(row["case_id"], row.get("rep", 0))] = row
    dials: dict[str, dict[tuple[Any, ...], dict[str, Any]]] = defaultdict(dict)
    for o in outcomes:
        if o["arm"] in (SUMMARY_ARM, FULL_ARM) and o["complete"]:
            dials[o["arm"]][(o["dialogue_id"], o["rep"])] = o
    for metric, table, depth_of, value_of in (
        ("step_accuracy", steps, lambda r: r.get("tags", {}).get("depth"), lambda r: r["correct"]),
        ("dialogue_success", dials, lambda o: o["depth"], lambda o: o["success"]),
    ):
        shared = sorted(set(table[SUMMARY_ARM]) & set(table[FULL_ARM]), key=str)
        by_depth: dict[Any, list[tuple[float, float]]] = defaultdict(list)
        for pair in shared:
            a, b = table[SUMMARY_ARM][pair], table[FULL_ARM][pair]
            by_depth[depth_of(a)].append((float(bool(value_of(a))), float(bool(value_of(b)))))
        for depth, pairs in sorted(by_depth.items(), key=lambda kv: str(kv[0])):
            delta, lo, hi = paired_delta(
                [p[0] for p in pairs], [p[1] for p in pairs], seed=stable_seed(*key, metric, depth)
            )
            out.append(
                metric_row(
                    key,
                    SUITE,
                    "depth",
                    depth,
                    f"{metric}_delta_summary_minus_full",
                    len(pairs),
                    delta,
                    lo,
                    hi,
                )
            )
    return out
