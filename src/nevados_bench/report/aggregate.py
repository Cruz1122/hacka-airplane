"""Aggregation of a run directory into scored.jsonl and tidy metric CSVs.

Input layout:  <run_dir>/<batch>/<launch_dir>/requests.jsonl and/or meta.json
               (a launch that failed to start may have only meta.json)
World: any object exposing `.tools`, `.passages` (mappings by name/id or iterables) and
`.gazetteer` (iterable of GazetteerEntry or mapping value -> entries).

Output layout: <run_dir>/scored.jsonl, <run_dir>/metrics/*.csv, <run_dir>/metrics/run_info.json

Works on partial data (missing batches, suites or models are simply absent) and is
idempotent: outputs are fully rewritten and ordered deterministically. A truncated or
malformed JSONL line (e.g. a crash mid-write) is skipped and listed in run_info.json.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from nevados_bench.schemas import (
    CONTEXT_LEVEL_TOKENS,
    Case,
    Dialogue,
    GazetteerEntry,
    Passage,
    RequestRecord,
    ToolSpec,
)
from nevados_bench.scoring import dialogue as dlg
from nevados_bench.scoring.extract import score_extract
from nevados_bench.scoring.fc import call_signature, score_route
from nevados_bench.scoring.grounding import index_gazetteer, score_answer
from nevados_bench.scoring.latency import (
    LAUNCH_FAILURE_FIELDS,
    is_warmup,
    latency_metric_rows,
    launch_failed,
    resource_metric_rows,
    tps_metric_rows,
)
from nevados_bench.scoring.stats import (
    mcnemar_paired,
    ols,
    paired_delta,
    percentile,
    stable_seed,
    wilson_interval,
)
from nevados_bench.scoring.tidy import (
    ALL,
    ANY,
    COLUMNS,
    ModelKey,
    compact,
    mean_row,
    metric_row,
    model_key,
    rate_row,
)
from nevados_bench.values import normalize_text

DIALOGUES_FILE = "dialogues.jsonl"
UNSCORED_SUITES = frozenset({"speed"})
# Arms that repeat or re-ask cases already counted by a primary arm. They appear only in
# the `arm` slice (and in their dedicated metrics) so overall rates do not double count.
SECONDARY_ARMS = frozenset(
    {
        "retry",
        "passk",
        "prefix_stable",
        "prefix_dynamic",
        "warmup",
        "free_run",
        "free_run_guarded",
        "free_run_extractive",
    }
)
# Cache-effect arms: feed latency.csv only, excluded from grounding rates entirely.
CACHE_ARMS = frozenset({"prefix_stable", "prefix_dynamic"})
PASS_K = 5
GIB = 1024**3
# Docker `--memory` values of config/profiles.yaml ("4g" = 4 GiB). A record may override
# with an extra `mem_limit` field (bytes).
PROFILE_MEMORY_LIMIT_BYTES = {"phone-tight": 4 * GIB, "phone-nominal": 5 * GIB}
PARSE_OK_GATE = 0.99
PARETO_LEVELS = frozenset({"1k", "2k"})

FC_FLAGS = (
    "parse_ok",
    "schema_valid",
    "hallucinated_tool",
    "hallucinated_arg",
    "type_error",
    "extra_arg",
    "missing_required",
    "tool_correct",
    "near_duplicate_confusion",
    "args_exact",
    "user_language_value",
    "fabricated_arg",
    "full_call_exact",
    "decision_correct",
    "over_call",
    "omitted_call",
    "relevance_detected",
    "correct_abstention",
    "correct_clarification",
    "multi_call_correct",
    "injection_obeyed",
    "route_correct",
    "missing_handled_clarify",
    "missing_handled_partial_call",
    "missing_handled_fabricated",
    "missing_handled_other",
)
FC_SLICES = (
    "stratum",
    "tools_n",
    "context_level",
    "gold_position",
    "distractors_n",
    "arm",
    "near_duplicate",
    "injection",
    "fsm_state",
)
EXTRACT_FLAGS = ("parse_ok", "slot_correct", "slot_fabricated", "slot_missed")
EXTRACT_SLICES = ("stratum", "arm", "slot_kind", "fsm_state", "context_level")
GROUNDING_FLAGS = (
    "grounded_correct",
    "faithful",
    "fabrication",
    "contamination",
    "prior_override",
    "hallucinated",
    "correct_abstention",
    "false_abstention",
    "lure_taken",
    "non_responsive",
    "answered_unanswerable",
    "citation_correct",
    "has_citation",
    "cited_not_shown",
    "language_ok",
    "rule_adherence",
    "injection_obeyed",
    "degenerate",
    "degenerate_empty",
    "degenerate_max_tokens",
    "degenerate_loop",
    "safety_fabrication",
    "abstained_with_extra_value",
)
GROUNDING_SLICES = (
    "context_level",
    "gold_position",
    "distractors_n",
    "question_type",
    "safety",
    "answerable",
    "closed_book",
    "arm",
    "stratum",
)
GROUNDING_OUTCOMES = (
    "faithful",
    "false_abstention",
    "prior_override",
    "contamination",
    "fabrication",
    "partial",
    "non_responsive",
    "lure_taken",
    "correct_abstention",
    "answered_unanswerable",
)


@dataclass
class Catalog:
    cases: dict[tuple[str, str], Case] = field(default_factory=dict)
    dialogues: dict[str, Dialogue] = field(default_factory=dict)
    defined: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    invalid_lines: list[str] = field(default_factory=list)

    def find(self, suite: str, case_id: str) -> Case | None:
        return self.cases.get((suite, case_id))


@dataclass
class RunData:
    records: list[RequestRecord] = field(default_factory=list)
    launches: list[dict[str, Any]] = field(default_factory=list)
    invalid_lines: list[str] = field(default_factory=list)


# ----------------------------------------------------------------------------- loading


def _index(items: Mapping[str, Any] | Iterable[Any], attr: str) -> dict[str, Any]:
    if isinstance(items, Mapping):
        return dict(items)
    return {getattr(item, attr): item for item in items}


def _with_step_tags(case: Case, dialogue: Dialogue, turn_index: int, step_index: int) -> Case:
    tags = {
        "dialogue_id": dialogue.dialogue_id,
        "turn_index": turn_index,
        "step_index": step_index,
        "depth": dialogue.depth,
        **case.tags,
    }
    tags.setdefault("phenomena", list(dialogue.phenomena))
    return case.model_copy(update={"tags": tags})


def load_catalog(suites_dir: Path) -> Catalog:
    """All cases in suites_dir/*.jsonl; dialogue step cases are flattened and tagged."""
    catalog = Catalog()
    if not suites_dir.is_dir():
        return catalog
    for path in sorted(suites_dir.glob("*.jsonl")):
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if "turns" in data and "dialogue_id" in data:
                        dialogue = Dialogue.model_validate(data)
                        catalog.dialogues[dialogue.dialogue_id] = dialogue
                        for t_idx, turn in enumerate(dialogue.turns):
                            for s_idx, step in enumerate(turn.steps):
                                case = _with_step_tags(step, dialogue, t_idx, s_idx)
                                catalog.cases[(case.suite, case.case_id)] = case
                                catalog.defined[case.suite].add(case.case_id)
                    else:
                        case = Case.model_validate(data)
                        catalog.cases[(case.suite, case.case_id)] = case
                        catalog.defined[case.suite].add(case.case_id)
                except (json.JSONDecodeError, ValidationError) as exc:
                    catalog.invalid_lines.append(f"{path.name}:{lineno}: {type(exc).__name__}")
    return catalog


def load_run(run_dir: Path) -> RunData:
    data = RunData()
    for path in sorted(run_dir.glob("*/*/requests.jsonl")):
        rel = path.relative_to(run_dir)
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    data.records.append(RequestRecord.model_validate_json(line))
                except ValidationError as exc:
                    data.invalid_lines.append(f"{rel}:{lineno}: {exc.error_count()} errors")
    for meta_path in sorted(run_dir.glob("*/*/meta.json")):
        rel = meta_path.parent.relative_to(run_dir)
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data.invalid_lines.append(f"{rel}/meta.json: invalid JSON")
            continue
        if not all(meta.get(k) for k in ("model_id", "quant", "profile")):
            data.invalid_lines.append(f"{rel}/meta.json: missing model_id/quant/profile")
            continue
        data.launches.append({**meta, "launch": rel.as_posix(), "batch": rel.parts[0]})
    data.records.sort(key=_record_order)
    return data


def _record_order(r: RequestRecord) -> tuple[Any, ...]:
    return (
        r.batch,
        r.model_id,
        r.quant,
        r.profile,
        r.fc_mode or "",
        r.suite,
        r.case_id,
        r.rep,
        r.arm,
        r.ts,
    )


# ----------------------------------------------------------------------------- scoring


def _output_signature(record: RequestRecord) -> str:
    parsed = record.parsed
    if parsed is None or not parsed.parse_ok:
        return "unparsed:" + normalize_text(record.completion.content)
    calls = sorted(call_signature(c) for c in parsed.calls)
    slot = json.dumps(parsed.slot_value, sort_keys=True, ensure_ascii=False, default=str)
    return f"{parsed.decision}|{calls}|{slot}|{normalize_text(parsed.answer_text or '')}"


def score_record(
    record: RequestRecord,
    case: Case | None,
    tools: dict[str, ToolSpec],
    passages: dict[str, Passage],
    gazetteer: dict[str, list[GazetteerEntry]],
) -> dict[str, Any]:
    """One scored.jsonl row: identity, analysis dimensions and the scorer's flags."""
    tags = {**(case.tags if case else {}), **record.tags}
    call_type = record.call_type or (case.call_type if case else None)
    row: dict[str, Any] = {
        "run_id": record.run_id,
        "batch": record.batch,
        "suite": record.suite,
        "case_id": record.case_id,
        "rep": record.rep,
        "arm": record.arm,
        "model_id": record.model_id,
        "quant": record.quant,
        "profile": record.profile,
        "fc_mode": record.fc_mode or "",
        "threads": record.threads,
        "call_type": call_type,
        "fsm_state": record.fsm_state or (case.fsm_state if case else None),
        "context_level": record.context_level or (case.context_level if case else None),
        "tools_n": record.tools_n or (len(case.tool_names) if case else 0) or tags.get("tools_n"),
        "strata": list(record.strata or (case.strata if case else [])),
        "ts": record.ts,
        "tags": tags,
        "case_found": case is not None,
        "executed_call": dlg.executed_call(record),
        "path": dlg.fsm_path(record),
        "scored": False,
        "correct": None,
        "output_signature": _output_signature(record),
        "pred_calls": [c.model_dump() for c in record.parsed.calls]
        if record.parsed and record.parsed.parse_ok
        else [],
    }
    # Set for free-run rows by dlg.annotate_premature (needs the whole dialogue).
    row["premature_execution"] = None
    if case is None or record.suite in UNSCORED_SUITES or call_type is None:
        return row
    if call_type == "route":
        flags = score_route(record, case, tools)
    elif call_type == "extract":
        flags = score_extract(record, case)
    else:
        flags = score_answer(record, case, passages, gazetteer)
    row.update(flags)
    row["scored"] = True
    row["transition_correct"] = dlg.transition_correct(record, case, row["correct"])
    return row


# ----------------------------------------------------------------------------- slicing


def _dim(row: dict[str, Any], name: str) -> list[Any]:
    """Slice values of a row for a dimension (strata explode to one value each)."""
    if name == "stratum":
        return list(row.get("strata") or []) or ["none"]
    value = row[name] if name in row and name not in ("tags",) else row.get("tags", {}).get(name)
    if value is None:
        return []
    return [value]


def _sliced(
    rows: list[dict[str, Any]], dims: Iterable[str]
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if "arm" in dims:
            out[("arm", str(row.get("arm")))].append(row)
        if row.get("arm") in SECONDARY_ARMS:
            continue
        out[(ALL, ALL)].append(row)
        for dim in dims:
            if dim == "arm":
                continue
            for value in _dim(row, dim):
                out[(dim, str(value))].append(row)
    return out


def _group(rows: Iterable[dict[str, Any]], fn: Any) -> dict[Any, list[dict[str, Any]]]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[fn(row)].append(row)
    return dict(sorted(groups.items(), key=lambda kv: str(kv[0])))


def is_primary(row: dict[str, Any]) -> bool:
    return row.get("arm") not in SECONDARY_ARMS


def _key_suite(row: dict[str, Any]) -> tuple[ModelKey, str]:
    return (model_key(row), row["suite"])


def _rate_table(
    rows: list[dict[str, Any]], flags: Iterable[str], dims: Iterable[str]
) -> list[dict[str, Any] | None]:
    out: list[dict[str, Any] | None] = []
    flags = tuple(flags)
    for (key, suite), grows in _group(rows, _key_suite).items():
        for (dim, value), srows in sorted(_sliced(grows, dims).items()):
            for flag in flags:
                out.append(rate_row(key, suite, dim, value, flag, (r.get(flag) for r in srows)))
            out.append(
                mean_row(
                    key, suite, dim, value, "output_tokens", (r.get("output_tokens") for r in srows)
                )
            )
        out.extend(_pass_k_rows(key, suite, grows))
        out.extend(_retry_rows(key, suite, grows))
    return out


def _pass_k_rows(
    key: ModelKey, suite: str, rows: list[dict[str, Any]]
) -> list[dict[str, Any] | None]:
    """pass^k: per case and arm, reps 0..k-1 all present and all correct."""
    reps: dict[tuple[str, str], dict[int, bool]] = defaultdict(dict)
    for r in rows:
        if r.get("correct") is not None:
            reps[(r["arm"], r["case_id"])][r["rep"]] = bool(r["correct"])
    by_arm: dict[str, list[bool]] = defaultdict(list)
    for (arm, _), outcomes in sorted(reps.items()):
        if all(i in outcomes for i in range(PASS_K)):
            by_arm[arm].append(all(outcomes[i] for i in range(PASS_K)))
    return [
        rate_row(key, suite, "arm", arm, f"pass_hat_{PASS_K}", vals)
        for arm, vals in sorted(by_arm.items())
    ]


def _retry_rows(
    key: ModelKey, suite: str, rows: list[dict[str, Any]]
) -> list[dict[str, Any] | None]:
    """Retry arm: a single retry with the error message after a failed first attempt."""
    retries = {
        (r["case_id"], r["rep"]): r
        for r in rows
        if r["arm"] == "retry" and r.get("correct") is not None
    }
    if not retries:
        return []
    firsts = {
        (r["case_id"], r["rep"]): r
        for r in rows
        if r["arm"] == "default" and r.get("correct") is not None
    }
    combined = []
    for pair, first in sorted(firsts.items()):
        retry = retries.get(pair)
        combined.append(bool(first["correct"]) or bool(retry and retry["correct"]))
    return [
        rate_row(
            key, suite, "arm", "retry", "retry_recovery", (r["correct"] for r in retries.values())
        ),
        rate_row(key, suite, "arm", "retry", "accuracy_with_one_retry", combined),
    ]


def fc_rows(route: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = _rate_table(route, FC_FLAGS, FC_SLICES)
    for (key, suite), grows in _group(route, _key_suite).items():
        by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in grows:
            for arg in row.get("arg_results") or []:
                by_type[arg["type_class"]].append(arg)
        for type_class, args in sorted(by_type.items()):
            out.append(
                rate_row(
                    key, suite, "arg_type", type_class, "arg_correct", (a["correct"] for a in args)
                )
            )
            out.append(
                rate_row(
                    key,
                    suite,
                    "arg_type",
                    type_class,
                    "arg_user_language",
                    (a["user_language"] for a in args),
                )
            )
        for dim, xfn in (
            ("tools_n", lambda r: r.get("tools_n")),
            ("context_level", lambda r: _level_tokens(r.get("context_level"))),
        ):
            pairs = [
                (float(xfn(r)), float(bool(r["route_correct"])))
                for r in grows
                if xfn(r) is not None
            ]
            fit = ols([p[0] for p in pairs], [p[1] for p in pairs])
            if fit:
                scale = 1000.0 if dim == "context_level" else 1.0
                unit = "per_1k_tokens" if dim == "context_level" else "per_tool"
                out.append(
                    metric_row(
                        key,
                        suite,
                        f"{dim}_regression",
                        ALL,
                        f"route_correct_slope_{unit}",
                        len(pairs),
                        fit["slope"] * scale,
                    )
                )
    return compact(out)


def _level_tokens(level: Any) -> int | None:
    return CONTEXT_LEVEL_TOKENS.get(str(level)) if level is not None else None


def grounding_rows(answer: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = _rate_table(answer, GROUNDING_FLAGS, GROUNDING_SLICES)
    for (key, suite), grows in _group(answer, _key_suite).items():
        for (dim, value), srows in sorted(_sliced(grows, GROUNDING_SLICES).items()):
            for outcome in GROUNDING_OUTCOMES:
                out.append(
                    rate_row(
                        key,
                        suite,
                        dim,
                        value,
                        f"outcome_{outcome}",
                        (r["outcome"] == outcome for r in srows),
                    )
                )
            for metric in ("answer_chars", "answer_words"):
                out.append(mean_row(key, suite, dim, value, metric, (r.get(metric) for r in srows)))
    return compact(out)


def per_tool_rows(route: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per-label precision/recall/F1 (labels: tool names, 'none', 'clarify', 'unparsed')."""
    out = []
    for (key, suite), grows in _group(route, _key_suite).items():
        labels = sorted({r["gold_label"] for r in grows} | {r["pred_label"] for r in grows})
        for label in labels:
            tp = sum(1 for r in grows if r["gold_label"] == label and r["pred_label"] == label)
            fp = sum(1 for r in grows if r["gold_label"] != label and r["pred_label"] == label)
            fn = sum(1 for r in grows if r["gold_label"] == label and r["pred_label"] != label)
            precision = tp / (tp + fp) if tp + fp else None
            recall = tp / (tp + fn) if tp + fn else None
            f1 = (
                2 * precision * recall / (precision + recall)
                if precision is not None and recall is not None and precision + recall
                else (0.0 if precision is not None and recall is not None else None)
            )
            out.append(
                {
                    **_key_cols(key),
                    "suite": suite,
                    "tool": label,
                    "support": tp + fn,
                    "tp": tp,
                    "fp": fp,
                    "fn": fn,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "low_n": tp + fn < 30,
                }
            )
    return out


def confusion_rows(route: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for (key, suite), grows in _group(route, _key_suite).items():
        counts: dict[tuple[str, str], int] = defaultdict(int)
        for r in grows:
            counts[(r["gold_label"], r["pred_label"])] += 1
        for (gold, pred), count in sorted(counts.items()):
            out.append(
                {
                    **_key_cols(key),
                    "suite": suite,
                    "gold_label": gold,
                    "pred_label": pred,
                    "count": count,
                }
            )
    return out


def _key_cols(key: ModelKey) -> dict[str, str]:
    return dict(zip(("model_id", "quant", "profile", "fc_mode"), key, strict=True))


def mcnemar_rows(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pairwise exact McNemar between models on the same (case, rep, arm), per suite x fc_mode."""
    table: dict[tuple[str, str], dict[tuple[str, str, str], dict[tuple[Any, ...], bool]]] = (
        defaultdict(lambda: defaultdict(dict))
    )
    for r in scored:
        if r.get("correct") is None:
            continue
        system = (r["model_id"], r["quant"], r["profile"])
        table[(r["suite"], r["fc_mode"])][system][(r["case_id"], r["rep"], r["arm"])] = bool(
            r["correct"]
        )
    out = []
    for (suite, fc_mode), systems in sorted(table.items()):
        names = sorted(systems)
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                shared = sorted(set(systems[a]) & set(systems[b]), key=str)
                if not shared:
                    continue
                test = mcnemar_paired(
                    [systems[a][k] for k in shared], [systems[b][k] for k in shared]
                )
                acc_a = (test["both"] + test["a_only"]) / test["n"]
                acc_b = (test["both"] + test["b_only"]) / test["n"]
                verdict = "tie"
                if test["p_value"] < 0.05:
                    verdict = "a_better" if test["a_only"] > test["b_only"] else "b_better"
                out.append(
                    {
                        "suite": suite,
                        "fc_mode": fc_mode,
                        "metric": "correct",
                        "model_a": a[0],
                        "quant_a": a[1],
                        "profile_a": a[2],
                        "model_b": b[0],
                        "quant_b": b[1],
                        "profile_b": b[2],
                        "n_pairs": test["n"],
                        "acc_a": acc_a,
                        "acc_b": acc_b,
                        "a_only": test["a_only"],
                        "b_only": test["b_only"],
                        "p_value": test["p_value"],
                        "verdict": verdict,
                        "low_n": test["n"] < 30,
                    }
                )
    return out


def _paired_delta_rows(
    scored: list[dict[str, Any]],
    label: str,
    side: Any,
    group_key: Any,
    out_key: Any,
    metrics: Iterable[str],
) -> list[dict[str, Any] | None]:
    """Generic paired delta: rows split into side 'a'/'b' by `side`, paired on case/rep/arm."""
    tables: dict[tuple[Any, ...], dict[str, dict[str, dict[tuple[Any, ...], float]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict))
    )
    for r in scored:
        s = side(r)
        if s is None:
            continue
        for metric in metrics:
            if r.get(metric) is not None:
                tables[group_key(r)][metric][s][(r["case_id"], r["rep"], r["arm"])] = float(
                    bool(r[metric])
                )
    out: list[dict[str, Any] | None] = []
    for gkey, per_metric in sorted(tables.items(), key=lambda kv: str(kv[0])):
        for metric, sides in sorted(per_metric.items()):
            shared = sorted(set(sides["a"]) & set(sides["b"]), key=str)
            if not shared:
                continue
            delta, lo, hi = paired_delta(
                [sides["a"][k] for k in shared],
                [sides["b"][k] for k in shared],
                seed=stable_seed(label, gkey, metric),
            )
            key, suite = out_key(gkey)
            out.append(
                metric_row(
                    key, suite, "comparison", label, f"{metric}_delta", len(shared), delta, lo, hi
                )
            )
    return out


def delta_rows(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    route = [r for r in scored if r.get("scored") and r["call_type"] == "route"]
    quality = [r for r in scored if r.get("correct") is not None]
    out: list[dict[str, Any] | None] = []
    mode_metrics = ("route_correct", "parse_ok", "tool_correct", "full_call_exact")
    for label, a_mode, b_mode in (
        ("native-uniform", "native", "uniform"),
        ("grammar_on-grammar_off", "uniform", "uniform_free"),
    ):
        out.extend(
            _paired_delta_rows(
                route,
                label,
                lambda r, a=a_mode, b=b_mode: (
                    "a" if r["fc_mode"] == a else "b" if r["fc_mode"] == b else None
                ),
                lambda r: (r["model_id"], r["quant"], r["profile"], r["suite"]),
                lambda g, lab=label: ((g[0], g[1], g[2], lab), g[3]),
                mode_metrics,
            )
        )
    out.extend(
        _paired_delta_rows(
            quality,
            "Q8_0-Q4_K_M",
            lambda r: "a" if r["quant"] == "Q8_0" else "b" if r["quant"] == "Q4_K_M" else None,
            lambda r: (r["model_id"], r["profile"], r["fc_mode"], r["suite"]),
            lambda g: ((g[0], "Q8_0-Q4_K_M", g[1], g[2]), g[3]),
            ("correct",),
        )
    )
    return compact(out)


def quant_speed_rows(tps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Q8_0 minus Q4_K_M for median decode / cold prefill tok/s at each context level."""
    medians: dict[tuple[Any, ...], float] = {}
    for row in tps:
        if (
            row["metric"] in ("decode_tps_p50", "prefill_tps_cold_p50")
            and row["slice_dim"] == "context_level"
        ):
            medians[
                (
                    row["model_id"],
                    row["quant"],
                    row["profile"],
                    row["fc_mode"],
                    row["slice_value"],
                    row["metric"],
                )
            ] = row["value"]
    out = []
    for (model, quant, profile, fc_mode, level, metric), value in sorted(medians.items()):
        if quant != "Q8_0":
            continue
        base = medians.get((model, "Q4_K_M", profile, fc_mode, level, metric))
        if base is not None and value is not None:
            out.append(
                metric_row(
                    (model, "Q8_0-Q4_K_M", profile, fc_mode),
                    ANY,
                    "context_level",
                    level,
                    f"{metric}_delta",
                    1,
                    value - base,
                )
            )
    return out


# ----------------------------------------------------------------------------- run-level tables


def coverage_rows(records: list[RequestRecord], catalog: Catalog) -> list[dict[str, Any]]:
    """Cases run / defined per batch x model x suite; free-run counts dialogues instead
    (suite `dialogues:free_run`). Code-only steps are not counted as records."""
    ran: dict[tuple[str, str, str, str, str, str], set[str]] = defaultdict(set)
    counts: dict[tuple[str, str, str, str, str, str], int] = defaultdict(int)
    for r in records:
        if r.tags.get("kind") == "code":
            continue
        free = str(r.arm).startswith(dlg.FREE_RUN)
        suite = f"{r.suite}:{r.arm}" if free else r.suite
        k = (r.batch, r.model_id, r.quant, r.profile, r.fc_mode or "", suite)
        ran[k].add(str(r.tags.get("dialogue_id")) if free else r.case_id)
        counts[k] += 1
    out = []
    for k, case_ids in sorted(ran.items()):
        if f":{dlg.FREE_RUN}" in k[5]:
            defined = set(catalog.dialogues)
        else:
            defined = catalog.defined.get(k[5], set())
        run_defined = len(case_ids & defined)
        out.append(
            {
                "batch": k[0],
                "model_id": k[1],
                "quant": k[2],
                "profile": k[3],
                "fc_mode": k[4],
                "suite": k[5],
                "cases_defined": len(defined),
                "cases_run": run_defined,
                "cases_unknown": len(case_ids - defined),
                "records": counts[k],
                "coverage": run_defined / len(defined) if defined else None,
            }
        )
    return out


def gate_rows(
    records: list[RequestRecord],
    scored: list[dict[str, Any]],
    launches: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Hard gates per system (model x quant x profile); systems come from records and from
    launch meta.json files, so a model that never started still appears (as a failure)."""
    launches = launches or []
    systems = sorted(
        {(r.model_id, r.quant, r.profile) for r in records}
        | {(str(m["model_id"]), str(m["quant"]), str(m["profile"])) for m in launches}
    )
    out = []
    for model_id, quant, profile in systems:
        metas = [
            m
            for m in launches
            if (m["model_id"], m["quant"], m["profile"]) == (model_id, quant, profile)
        ]
        failed = [m for m in metas if launch_failed(m)]
        if metas:
            out.append(
                {
                    "model_id": model_id,
                    "quant": quant,
                    "profile": profile,
                    "gate": "launch_ok",
                    "value": len(failed),
                    "threshold": "== 0 failed launches",
                    "n": len(metas),
                    "status": "fail" if failed else "pass",
                }
            )
        mine = [
            r
            for r in scored
            if (r["model_id"], r["quant"], r["profile"]) == (model_id, quant, profile)
        ]
        base = {"model_id": model_id, "quant": quant, "profile": profile}
        safety = [r["safety_fabrication"] for r in mine if r.get("safety_fabrication") is not None]
        count = sum(bool(v) for v in safety)
        out.append(
            {
                **base,
                "gate": "safety_critical_fabrication",
                "value": count,
                "threshold": "== 0",
                "n": len(safety),
                "status": "not_run" if not safety else "pass" if count == 0 else "fail",
            }
        )
        recs = [
            r for r in records if (r.model_id, r.quant, r.profile) == (model_id, quant, profile)
        ]
        peaks = [r.mem_peak for r in recs if r.mem_peak is not None]
        limits = [m.get("mem_limit") for m in metas] + [
            (r.model_extra or {}).get("mem_limit") for r in recs
        ]
        limit = next((int(v) for v in limits if v), PROFILE_MEMORY_LIMIT_BYTES.get(profile))
        if any(m.get("oom_killed") for m in metas):
            status, value = "fail", max(peaks) if peaks else None
        elif not peaks:
            status, value = "not_run", None
        elif limit is None:
            status, value = "not_verified", max(peaks)
        else:
            status, value = ("pass" if max(peaks) <= limit else "fail"), max(peaks)
        out.append(
            {
                **base,
                "gate": "memory_peak_le_profile_limit",
                "value": value,
                "threshold": f"<= {limit}" if limit else "unknown",
                "n": len(peaks),
                "status": status,
            }
        )
        parse = [
            r["parse_ok"]
            for r in mine
            if r["fc_mode"] == "uniform"
            and r.get("call_type") in ("route", "extract")
            and r.get("scored")
            and is_primary(r)
        ]
        rate = sum(parse) / len(parse) if parse else None
        lo, _ = wilson_interval(sum(parse), len(parse)) if parse else (None, None)
        out.append(
            {
                **base,
                "gate": "parse_ok_uniform_ge_99pct",
                "value": rate,
                "threshold": f">= {PARSE_OK_GATE}",
                "n": len(parse),
                "ci_low": lo,
                "status": "not_run"
                if rate is None
                else "pass"
                if rate >= PARSE_OK_GATE
                else "fail",
            }
        )
    return out


def pareto_rows(records: list[RequestRecord], scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Route accuracy vs median route latency at the realistic 1k-2k context levels."""
    acc: dict[ModelKey, list[bool]] = defaultdict(list)
    for r in scored:
        if (
            r.get("call_type") == "route"
            and r.get("scored")
            and is_primary(r)
            and r.get("context_level") in PARETO_LEVELS
        ):
            acc[model_key(r)].append(bool(r["route_correct"]))
    lat: dict[ModelKey, list[float]] = defaultdict(list)
    for r in records:
        if (
            r.call_type == "route"
            and r.context_level in PARETO_LEVELS
            and r.arm not in SECONDARY_ARMS
            and not is_warmup(r)
            and r.completion.total_ms is not None
            and not r.completion.http_error
        ):
            lat[model_key(r)].append(r.completion.total_ms)
    points = []
    for key in sorted(set(acc) & set(lat)):
        k, n = sum(acc[key]), len(acc[key])
        lo, hi = wilson_interval(k, n)
        points.append(
            {
                **_key_cols(key),
                "accuracy": k / n,
                "acc_n": n,
                "acc_ci_low": lo,
                "acc_ci_high": hi,
                "latency_p50_ms": percentile(lat[key], 50),
                "lat_n": len(lat[key]),
            }
        )
    for p in points:
        p["pareto"] = not any(
            q is not p
            and q["accuracy"] >= p["accuracy"]
            and q["latency_p50_ms"] <= p["latency_p50_ms"]
            and (q["accuracy"] > p["accuracy"] or q["latency_p50_ms"] < p["latency_p50_ms"])
            for q in points
        )
    return points


# ----------------------------------------------------------------------------- writing


def _fmt(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6g}"
    if isinstance(value, list | dict):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


def write_csv(path: Path, rows: list[dict[str, Any]], columns: Iterable[str] | None = None) -> None:
    cols = list(columns) if columns else (list(rows[0]) if rows else [])
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _fmt(row.get(c)) for c in cols})
    tmp.replace(path)


PER_TOOL_COLUMNS = (
    "model_id",
    "quant",
    "profile",
    "fc_mode",
    "suite",
    "tool",
    "support",
    "tp",
    "fp",
    "fn",
    "precision",
    "recall",
    "f1",
    "low_n",
)
CONFUSION_COLUMNS = (
    "model_id",
    "quant",
    "profile",
    "fc_mode",
    "suite",
    "gold_label",
    "pred_label",
    "count",
)
MCNEMAR_COLUMNS = (
    "suite",
    "fc_mode",
    "metric",
    "model_a",
    "quant_a",
    "profile_a",
    "model_b",
    "quant_b",
    "profile_b",
    "n_pairs",
    "acc_a",
    "acc_b",
    "a_only",
    "b_only",
    "p_value",
    "verdict",
    "low_n",
)
COVERAGE_COLUMNS = (
    "batch",
    "model_id",
    "quant",
    "profile",
    "fc_mode",
    "suite",
    "cases_defined",
    "cases_run",
    "cases_unknown",
    "records",
    "coverage",
)
GATE_COLUMNS = (
    "model_id",
    "quant",
    "profile",
    "gate",
    "value",
    "threshold",
    "n",
    "ci_low",
    "status",
)
PARETO_COLUMNS = (
    "model_id",
    "quant",
    "profile",
    "fc_mode",
    "accuracy",
    "acc_n",
    "acc_ci_low",
    "acc_ci_high",
    "latency_p50_ms",
    "lat_n",
    "pareto",
)
DIALOGUE_DETAIL_COLUMNS = (
    "model_id",
    "quant",
    "profile",
    "fc_mode",
    "arm",
    "rep",
    "dialogue_id",
    "depth",
    "steps_expected",
    "steps_run",
    "complete",
    "success",
    "first_error_turn",
    "expected_success",
    "premature_execution",
    "repeats",
    "loop",
    "side_effects_ok",
    "executions",
    "missing_execution",
    "extra_execution",
    "wrong_tool_execution",
    "wrong_args_execution",
)


def _metric_sort(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: tuple(str(r.get(c, "")) for c in COLUMNS[:8]))


def aggregate_run(run_dir: Path | str, suites_dir: Path | str, world: Any) -> None:
    """Score every request under run_dir and write scored.jsonl plus metrics/*.csv."""
    run_dir, suites_dir = Path(run_dir), Path(suites_dir)
    tools: dict[str, ToolSpec] = _index(world.tools, "name")
    passages: dict[str, Passage] = _index(world.passages, "id")
    gazetteer = index_gazetteer(world.gazetteer)
    catalog = load_catalog(suites_dir)
    run = load_run(run_dir)

    scored = []
    missing_cases = 0
    for record in run.records:
        case = catalog.find(record.suite, record.case_id)
        free_run = str(record.arm).startswith(dlg.FREE_RUN) or record.suite == dlg.FREE_RUN
        if case is None and record.suite not in UNSCORED_SUITES and not free_run:
            missing_cases += 1
        scored.append(score_record(record, case, tools, passages, gazetteer))
    dlg.annotate_premature(scored, tools)

    tmp = run_dir / "scored.jsonl.tmp"
    with tmp.open("w", encoding="utf-8") as handle:
        for row in scored:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False, default=str) + "\n")
    tmp.replace(run_dir / "scored.jsonl")

    route = [r for r in scored if r["scored"] and r["call_type"] == "route"]
    extract = [r for r in scored if r["scored"] and r["call_type"] == "extract"]
    answer = [
        r
        for r in scored
        if r["scored"] and r["call_type"] == "answer" and r["arm"] not in CACHE_ARMS
    ]
    dialogue_rows, dialogue_detail = dlg.dialogue_metric_rows(
        [r for r in scored if r["scored"] or dlg.is_free_run(r)], catalog.dialogues, tools
    )
    tps = tps_metric_rows(run.records)

    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    tidy_tables = {
        "fc_rates.csv": fc_rows(route),
        "extract_rates.csv": compact(_rate_table(extract, EXTRACT_FLAGS, EXTRACT_SLICES)),
        "grounding_rates.csv": grounding_rows(answer),
        "dialogue_rates.csv": dialogue_rows,
        "latency.csv": latency_metric_rows(run.records),
        "tps.csv": tps,
        "resources.csv": resource_metric_rows(run.records, run.launches),
        "deltas.csv": delta_rows(scored) + quant_speed_rows(tps),
    }
    for name, rows in tidy_tables.items():
        write_csv(metrics_dir / name, _metric_sort(rows), COLUMNS)
    primary_route = [r for r in route if is_primary(r)]
    write_csv(metrics_dir / "fc_per_tool.csv", per_tool_rows(primary_route), PER_TOOL_COLUMNS)
    write_csv(metrics_dir / "fc_confusion.csv", confusion_rows(primary_route), CONFUSION_COLUMNS)
    write_csv(metrics_dir / "mcnemar.csv", mcnemar_rows(scored), MCNEMAR_COLUMNS)
    write_csv(metrics_dir / "coverage.csv", coverage_rows(run.records, catalog), COVERAGE_COLUMNS)
    write_csv(metrics_dir / "gates.csv", gate_rows(run.records, scored, run.launches), GATE_COLUMNS)
    write_csv(metrics_dir / "pareto.csv", pareto_rows(run.records, scored), PARETO_COLUMNS)
    write_csv(metrics_dir / "dialogue_detail.csv", dialogue_detail, DIALOGUE_DETAIL_COLUMNS)

    info = {
        "records": len(run.records),
        "scored": sum(1 for r in scored if r["scored"]),
        "records_without_case": missing_cases,
        "invalid_record_lines": run.invalid_lines,
        "invalid_case_lines": catalog.invalid_lines,
        "suites_defined": {s: len(ids) for s, ids in sorted(catalog.defined.items())},
        "suites_run": sorted({r.suite for r in run.records}),
        "batches": sorted({r.batch for r in run.records}),
        "models": sorted({f"{r.model_id}|{r.quant}|{r.profile}" for r in run.records}),
        "run_ids": sorted({r.run_id for r in run.records}),
        "launches": [
            {
                "launch": m["launch"],
                "model": f"{m['model_id']}|{m['quant']}|{m['profile']}",
                "failed": launch_failed(m),
                "failure": next((f"{k}: {m[k]}" for k in LAUNCH_FAILURE_FIELDS if m.get(k)), None),
                "records_written": m.get("records_written"),
                "cases_skipped_budget": m.get("cases_skipped_budget"),
            }
            for m in run.launches
        ],
    }
    (metrics_dir / "run_info.json").write_text(
        json.dumps(info, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
