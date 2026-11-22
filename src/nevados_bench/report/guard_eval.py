"""Offline effect of the code guards: re-score recorded outputs as if guarded.

The guards are pure post-processing of the model output, so their effect on a finished run
needs no model calls: each grounded answer goes through `guard_answer` and each single-turn
route (B2) through `guard_route`; the record is rewritten with the guarded output and the
unchanged scorer runs again. Writes `metrics/guard_eval.csv` (answers, per model),
`metrics/guard_route_eval.csv` (routes, per model) and `metrics/guard_rejections.jsonl`.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from nevados_bench.guards import detect_station, guard_answer, guard_route
from nevados_bench.report.aggregate import load_catalog, load_run
from nevados_bench.schemas import Case, RequestRecord
from nevados_bench.scoring.fc import is_injection_case, score_route
from nevados_bench.scoring.grounding import answer_text, score_answer
from nevados_bench.scoring.stats import wilson_interval
from nevados_bench.world import World


def guarded_record(record: RequestRecord, text: str) -> RequestRecord:
    completion = record.completion.model_copy(update={"content": text})
    update: dict[str, Any] = {"completion": completion}
    if record.parsed is not None:
        update["parsed"] = record.parsed.model_copy(update={"answer_text": text})
    return record.model_copy(update=update)


def evaluate(
    records: list[RequestRecord], cases: dict[tuple[str, str], Case], world: World
) -> list[dict]:
    """One row per answer record: baseline flags, guarded flags and the guard decision."""
    names = {sid: s.name for sid, s in world.stations.items()}
    rows: list[dict[str, Any]] = []
    for record in records:
        case = cases.get((record.suite, record.case_id))
        if case is None or (record.call_type or case.call_type) != "answer":
            continue
        shown = {pid: world.passages[pid] for pid in case.passage_ids if pid in world.passages}
        safety = bool(case.tags.get("safety"))
        result = guard_answer(
            answer_text(record),
            user_message=case.user_message,
            shown=shown,
            target_station=detect_station(case.user_message, names),
            gazetteer=world.gazetteer,
            safety=safety,
        )
        before = score_answer(record, case, world.passages, world.gazetteer)
        after = (
            before
            if result.passed
            else score_answer(
                guarded_record(record, result.text), case, world.passages, world.gazetteer
            )
        )
        rows.append(
            {
                "model_id": record.model_id,
                "batch": record.batch,
                "case_id": record.case_id,
                "rep": record.rep,
                "arm": record.arm,
                "safety": safety,
                "answerable": before["answerable"],
                "passed": result.passed,
                "reasons": list(result.reasons),
                "before": before,
                "after": after,
                "text": answer_text(record),
            }
        )
    return rows


def _rate(rows: list[dict], side: str, flag: str) -> tuple[int, int]:
    vals = [r[side][flag] for r in rows if r[side][flag] is not None]
    return sum(bool(v) for v in vals), len(vals)


def summarize(rows: list[dict]) -> list[dict[str, Any]]:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_model[r["model_id"]].append(r)
    out = []
    for model, group in sorted(by_model.items()):
        row: dict[str, Any] = {"model_id": model, "n": len(group)}
        for flag in (
            "grounded_correct",
            "faithful",
            "correct_abstention",
            "hallucinated",
            "false_abstention",
            "safety_fabrication",
        ):
            for side in ("before", "after"):
                k, n = _rate(group, side, flag)
                lo, hi = wilson_interval(k, n)
                row[f"{flag}_{side}"] = k
                row[f"{flag}_{side}_n"] = n
                row[f"{flag}_{side}_rate"] = round(k / n, 4) if n else None
                row[f"{flag}_{side}_ci"] = (
                    f"[{lo:.3f}, {hi:.3f}]" if lo is not None and hi is not None else ""
                )
        rejected = [r for r in group if not r["passed"]]
        row["rejected"] = len(rejected)
        row["rejected_was_correct"] = sum(r["before"]["grounded_correct"] for r in rejected)
        reasons = Counter(reason for r in rejected for reason in r["reasons"])
        row["reasons"] = json.dumps(dict(reasons.most_common()), ensure_ascii=False)
        out.append(row)
    return out


def evaluate_routes(
    records: list[RequestRecord], cases: dict[tuple[str, str], Case], world: World
) -> list[dict[str, Any]]:
    """Routes before and after `guard_route` (no device station).

    B2 is single-turn fc_core, the suite the guard rules were tuned on. B4 dialogue route
    steps (teacher-forced history or state summary) were not looked at while tuning, so
    they are the held-out check.
    """
    rows: list[dict[str, Any]] = []
    for record in records:
        case = cases.get((record.suite, record.case_id))
        if record.batch not in ("B2", "B4") or case is None or case.call_type != "route":
            continue
        # Same rule as the driver: only user turns ground arguments.
        context = [
            m.get("content") or ""
            for m in case.history
            if isinstance(m, dict) and m.get("role") == "user"
        ]
        if case.state_summary:
            context.append(case.state_summary)
        parsed = record.parsed
        before = score_route(record, case, world.tools)
        if parsed is None or not parsed.parse_ok:
            after, result = before, None
        else:
            result = guard_route(
                parsed.decision,
                parsed.calls,
                user_text=case.user_message,
                context_texts=context,
                world=world,
            )
            new = parsed.model_copy(
                update={"decision": result.decision, "calls": list(result.calls)}
            )
            after = score_route(record.model_copy(update={"parsed": new}), case, world.tools)
        injected = is_injection_case(case) and bool(before.get("injection_obeyed"))
        rows.append(
            {
                "model_id": record.model_id,
                "fc_mode": record.fc_mode,
                "set": f"{record.batch}:{record.arm}",
                "case_id": record.case_id,
                "before": before,
                "after": after,
                "changed": result is not None
                and (result.decision != parsed.decision or result.missing != ()),
                "missing": list(result.missing) if result else [],
                "injection_obeyed": injected,
                # Still obeyed after the guard and not stopped by the confirmation step.
                "injection_executes": injected
                and bool(after.get("injection_obeyed"))
                and not (result is not None and result.needs_confirmation),
            }
        )
    return rows


def summarize_routes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        by_key[(r["model_id"], r["fc_mode"] or "", r["set"])].append(r)
    out = []
    for (model, mode, subset), group in sorted(by_key.items()):
        row: dict[str, Any] = {"model_id": model, "fc_mode": mode, "set": subset, "n": len(group)}
        for flag in ("correct", "fabricated_arg", "correct_clarification", "over_call"):
            for side in ("before", "after"):
                k, n = _rate(group, side, flag)
                row[f"{flag}_{side}"] = k
                row[f"{flag}_{side}_n"] = n
                row[f"{flag}_{side}_rate"] = round(k / n, 4) if n else None
        row["changed"] = sum(r["changed"] for r in group)
        row["changed_was_correct"] = sum(
            bool(r["before"]["correct"]) and not r["after"]["correct"] for r in group
        )
        row["injection_obeyed"] = sum(r["injection_obeyed"] for r in group)
        row["injection_executes_after"] = sum(r["injection_executes"] for r in group)
        out.append(row)
    return out


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_guard_eval(
    run_dir: Path, suites_dir: Path, world: World
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    catalog = load_catalog(suites_dir)
    records = load_run(run_dir).records
    rows = evaluate(records, catalog.cases, world)
    summary = summarize(rows)
    route_summary = summarize_routes(evaluate_routes(records, catalog.cases, world))
    metrics = run_dir / "metrics"
    metrics.mkdir(parents=True, exist_ok=True)
    _write_csv(metrics / "guard_eval.csv", summary)
    _write_csv(metrics / "guard_route_eval.csv", route_summary)
    with (metrics / "guard_rejections.jsonl").open("w", encoding="utf-8") as handle:
        for r in rows:
            if not r["passed"]:
                slim = {k: v for k, v in r.items() if k not in ("before", "after")}
                slim["outcome_before"] = r["before"]["outcome"]
                slim["outcome_after"] = r["after"]["outcome"]
                handle.write(json.dumps(slim, ensure_ascii=False) + "\n")
    return summary, route_summary
