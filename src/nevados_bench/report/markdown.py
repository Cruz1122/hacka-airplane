"""REPORT.md rendering from the CSVs written by `aggregate_run`.

The report contains no timestamps so that re-running it on the same data is a no-op.
Ranking rule: rows are sorted by value; a row whose confidence interval overlaps the CI
of the current rank group's leader is shown as a tie ("=k") instead of a new rank.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MCNEMAR_LIMIT = 50


@dataclass(frozen=True)
class Board:
    title: str
    file: str
    metric: str
    slice_dim: str
    slice_value: str | None  # None: one table per slice value
    higher_is_better: bool
    percent: bool = True


BOARDS = (
    Board(
        "Function calling: full route correctness",
        "fc_rates.csv",
        "route_correct",
        "all",
        "all",
        True,
    ),
    Board("Function calling: tool selection", "fc_rates.csv", "tool_correct", "all", "all", True),
    Board("Function calling: parse ok", "fc_rates.csv", "parse_ok", "all", "all", True),
    Board("Slot extraction", "extract_rates.csv", "slot_correct", "all", "all", True),
    Board(
        "Grounding: correct (faithful or correct abstention)",
        "grounding_rates.csv",
        "grounded_correct",
        "all",
        "all",
        True,
    ),
    Board(
        "Grounding: hallucination (any unsupported value)",
        "grounding_rates.csv",
        "hallucinated",
        "all",
        "all",
        False,
    ),
    Board(
        "Grounding: safety-critical fabrication",
        "grounding_rates.csv",
        "safety_fabrication",
        "all",
        "all",
        False,
    ),
    Board("Dialogue success by arm", "dialogue_rates.csv", "dialogue_success", "arm", None, True),
    Board(
        "Dialogue step accuracy by arm", "dialogue_rates.csv", "step_accuracy", "arm", None, True
    ),
    Board(
        "Latency: route total ms p50",
        "latency.csv",
        "total_ms_p50",
        "context_level×cache×call_type",
        "*|*|route",
        False,
        False,
    ),
    Board(
        "Latency: answer TTFT ms p50",
        "latency.csv",
        "ttft_ms_p50",
        "context_level×cache×call_type",
        "*|*|answer",
        False,
        False,
    ),
    Board(
        "Throughput: effective end-to-end tok/s p50",
        "tps.csv",
        "effective_e2e_tps_p50",
        "all",
        "all",
        True,
        False,
    ),
    Board(
        "Throughput: cold prefill tok/s p50 by context level",
        "tps.csv",
        "prefill_tps_cold_p50",
        "context_level",
        None,
        True,
        False,
    ),
    Board(
        "Resources: peak memory (bytes)",
        "resources.csv",
        "mem_peak_max",
        "all",
        "all",
        False,
        False,
    ),
)

EXPECTED_FAMILIES = {
    "latency.csv": (
        "first_request_total_ms",
        "turn_e2e_ms_p50",
        "dialogue_e2e_ms_p50",
        "ttft_ms_delta_stable_minus_dynamic",
        "total_ms_vs_prompt_tokens_slope_ms_per_1k_tokens",
    ),
    "tps.csv": ("decode_tps_scaling_efficiency", "decode_tps_drift_pct", "decode_tps_per_gib_peak"),
    "resources.csv": ("load_ms", "gguf_size_bytes", "mem_peak_max"),
    "fc_rates.csv": ("pass_hat_5", "retry_recovery", "injection_obeyed", "multi_call_correct"),
    "deltas.csv": ("route_correct_delta", "correct_delta"),
    "dialogue_rates.csv": (
        "dialogue_success_delta_summary_minus_full",
        "dialogue_premature_execution",
    ),
    "grounding_rates.csv": ("citation_correct", "injection_obeyed", "safety_fabrication"),
}

ALWAYS_UNVERIFIED = (
    "Laptop x86 numbers are an ordinal proxy; absolute phone latency needs the B6 adb anchor.",
    "Thermal throttling and energy are out of scope (only measurable on the real phone).",
    "Hallucination scorer validity requires the manual audit of 50 sampled answers (plan, Risks).",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _num(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _fmt(value: float | None, percent: bool) -> str:
    if value is None:
        return "—"
    if percent:
        return f"{100 * value:.1f} %"
    return f"{value:,.1f}" if abs(value) < 1e6 else f"{value:,.0f}"


def _model(row: dict[str, str]) -> str:
    parts = [row.get("model_id", ""), row.get("quant", ""), row.get("profile", "")]
    mode = row.get("fc_mode", "")
    if mode and mode != "*":
        parts.append(mode)
    return " / ".join(p for p in parts if p)


def _overlap(a: dict[str, str], b: dict[str, str]) -> bool:
    lo_a, hi_a, lo_b, hi_b = (
        _num(a.get("ci_low")),
        _num(a.get("ci_high")),
        _num(b.get("ci_low")),
        _num(b.get("ci_high")),
    )
    if None in (lo_a, hi_a, lo_b, hi_b):
        return _num(a.get("value")) == _num(b.get("value"))
    return lo_a <= hi_b and lo_b <= hi_a  # type: ignore[operator]


def ranked(rows: list[dict[str, str]], higher_is_better: bool) -> list[tuple[str, dict[str, str]]]:
    """Rows sorted by value with rank labels; CI overlap with the group leader is a tie."""
    valid = [r for r in rows if _num(r.get("value")) is not None]
    valid.sort(
        key=lambda r: (
            -(_num(r["value"]) or 0) if higher_is_better else (_num(r["value"]) or 0),
            _model(r),
        )
    )
    out = []
    leader: dict[str, str] | None = None
    rank = 0
    for position, row in enumerate(valid, 1):
        if leader is not None and _overlap(leader, row):
            out.append((f"={rank}", row))
            continue
        rank, leader = position, row
        out.append((str(rank), row))
    return out


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return lines


def _board_lines(board: Board, rows: list[dict[str, str]]) -> list[str]:
    selected = [
        r for r in rows if r["metric"] == board.metric and r["slice_dim"] == board.slice_dim
    ]
    if board.slice_value is not None:
        selected = [r for r in selected if r["slice_value"] == board.slice_value]
    if not selected:
        return [f"### {board.title}", "", "_No data._", ""]
    lines = [f"### {board.title}", ""]
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in selected:
        groups[(r["suite"], r["slice_value"])].append(r)
    for (suite, value), grows in sorted(groups.items()):
        caption = f"suite `{suite}`" + (
            f", {board.slice_dim} = `{value}`" if board.slice_value is None else ""
        )
        body = []
        for rank, r in ranked(grows, board.higher_is_better):
            ci = (
                f"[{_fmt(_num(r['ci_low']), board.percent)}, "
                f"{_fmt(_num(r['ci_high']), board.percent)}]"
                if r.get("ci_low")
                else "—"
            )
            body.append(
                [
                    rank,
                    _model(r),
                    _fmt(_num(r["value"]), board.percent),
                    ci,
                    r["n"],
                    "yes" if r.get("low_n") == "true" else "",
                ]
            )
        lines += [f"{caption} — {'higher' if board.higher_is_better else 'lower'} is better", ""]
        lines += [*_table(["rank", "model", "value", "95 % CI", "n", "n<30"], body), ""]
    return lines


def write_report(run_dir: Path | str) -> Path:
    """Render <run_dir>/REPORT.md from <run_dir>/metrics/*; returns the report path."""
    run_dir = Path(run_dir)
    metrics = run_dir / "metrics"
    info_path = metrics / "run_info.json"
    info: dict[str, Any] = (
        json.loads(info_path.read_text(encoding="utf-8")) if info_path.is_file() else {}
    )
    coverage = _read_csv(metrics / "coverage.csv")
    gates = _read_csv(metrics / "gates.csv")
    pareto = _read_csv(metrics / "pareto.csv")
    mcnemar = _read_csv(metrics / "mcnemar.csv")
    tables = {
        name: _read_csv(metrics / name)
        for name in {b.file for b in BOARDS} | set(EXPECTED_FAMILIES)
    }

    run_ids = ", ".join(info.get("run_ids", [])) or run_dir.name
    lines = [
        f"# Benchmark report — {run_ids}",
        "",
        f"Records: {info.get('records', 0)} · scored: {info.get('scored', 0)} · "
        f"batches: {', '.join(info.get('batches', [])) or 'none'} · "
        f"models: {len(info.get('models', []))}",
        "",
        "Rates carry Wilson 95 % CIs, latency percentiles a seeded bootstrap CI. "
        "Rank `=k` means the difference to rank k is inside the CI (a tie). "
        "Cells with n<30 are flagged.",
        "",
        "## Batches",
        "",
    ]
    by_batch: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in coverage:
        by_batch[row["batch"]].append(row)
    if not by_batch:
        lines += ["_No batch has produced records yet._", ""]
    for batch, rows in sorted(by_batch.items()):
        lines += [f"### Batch {batch}", ""]
        body = [
            [
                _model(r),
                r["suite"],
                f"{r['cases_run']}/{r['cases_defined']}",
                _fmt(_num(r["coverage"]), True),
                r["records"],
            ]
            for r in rows
        ]
        lines += [*_table(["model", "suite", "cases run/defined", "coverage", "records"], body), ""]

    lines += ["## Hard gates", ""]
    lines += _gate_lines(gates)
    lines += ["## Leaderboards", ""]
    for board in BOARDS:
        lines += _board_lines(board, tables.get(board.file, []))
    lines += ["## Pareto: accuracy vs latency (route calls, context 1k–2k)", ""]
    if pareto:
        body = [
            [
                _model(r),
                _fmt(_num(r["accuracy"]), True),
                f"[{_fmt(_num(r['acc_ci_low']), True)}, {_fmt(_num(r['acc_ci_high']), True)}]",
                r["acc_n"],
                _fmt(_num(r["latency_p50_ms"]), False),
                "yes" if r["pareto"] == "true" else "",
            ]
            for r in sorted(
                pareto, key=lambda r: (r["pareto"] != "true", -(_num(r["accuracy"]) or 0))
            )
        ]
        lines += [
            *_table(["model", "accuracy", "95 % CI", "n", "latency p50 ms", "frontier"], body),
            "",
        ]
    else:
        lines += ["_No route records at 1k–2k context._", ""]
    lines += ["## Pairwise significance (exact McNemar, p < 0.05)", ""]
    significant = [r for r in mcnemar if r["verdict"] != "tie"]
    if significant:
        body = [
            [
                r["suite"],
                r["fc_mode"],
                f"{r['model_a']}/{r['quant_a']}/{r['profile_a']}",
                f"{r['model_b']}/{r['quant_b']}/{r['profile_b']}",
                r["n_pairs"],
                _fmt(_num(r["acc_a"]), True),
                _fmt(_num(r["acc_b"]), True),
                f"{float(r['p_value']):.3g}",
                r["verdict"],
            ]
            for r in significant[:MCNEMAR_LIMIT]
        ]
        lines += _table(
            ["suite", "fc_mode", "a", "b", "pairs", "acc a", "acc b", "p", "verdict"], body
        )
        if len(significant) > MCNEMAR_LIMIT:
            lines.append(f"\n_{len(significant) - MCNEMAR_LIMIT} more in metrics/mcnemar.csv._")
        lines.append("")
    else:
        lines += [
            f"_No significant pairwise difference ({len(mcnemar)} pairs tested); all are ties._",
            "",
        ]
    lines += ["## Coverage", ""]
    pooled: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in coverage:
        pooled[(_model(row), row["suite"])].append(row)
    if pooled:
        body = [
            [m, s, str(max(int(r["cases_run"]) for r in rs)), rs[0]["cases_defined"]]
            for (m, s), rs in sorted(pooled.items())
        ]
        lines += [
            *_table(["model", "suite", "cases run (max over batches)", "cases defined"], body),
            "",
        ]
    else:
        lines += ["_No coverage data._", ""]
    lines += ["## Not run / not verified", ""]
    lines += [f"- {item}" for item in _not_run(info, coverage, gates, tables)] + [""]
    path = run_dir / "REPORT.md"
    tmp = path.with_suffix(".tmp")
    tmp.write_text("\n".join(lines), encoding="utf-8")
    tmp.replace(path)
    return path


def _gate_lines(gates: list[dict[str, str]]) -> list[str]:
    if not gates:
        return ["_No gate could be evaluated._", ""]
    names = sorted({g["gate"] for g in gates})
    systems: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for g in gates:
        systems[_model(g)][g["gate"]] = g
    body = []
    for system, by_gate in sorted(systems.items()):
        cells = []
        for name in names:
            g = by_gate.get(name)
            if g is None:
                cells.append("not run")
                continue
            value = g["value"]
            if name == "parse_ok_uniform_ge_99pct":
                value = _fmt(_num(value), True)
            elif name == "memory_peak_le_profile_limit" and _num(value) is not None:
                value = f"{(_num(value) or 0) / 1024**3:.2f} GiB"
            cells.append(f"{g['status'].upper()} ({value or '—'}, n={g['n']})")
        verdict = "PASS" if all(by_gate.get(n, {}).get("status") == "pass" for n in names) else "—"
        body.append([system, *cells, verdict])
    return [*_table(["model", *names, "all gates"], body), ""]


def _not_run(
    info: dict[str, Any],
    coverage: list[dict[str, str]],
    gates: list[dict[str, str]],
    tables: dict[str, list[dict[str, str]]],
) -> list[str]:
    items = []
    run_suites = set(info.get("suites_run", []))
    for suite in sorted(set(info.get("suites_defined", {})) - run_suites):
        items.append(f"Suite `{suite}`: defined but no records.")
    for row in coverage:
        cov = _num(row.get("coverage"))
        if cov is not None and cov < 1:
            items.append(
                f"Batch {row['batch']}, {_model(row)}, suite `{row['suite']}`: "
                f"coverage {_fmt(cov, True)} ({row['cases_run']}/{row['cases_defined']})."
            )
    for g in gates:
        if g["status"] in ("not_run", "not_verified"):
            items.append(f"Gate `{g['gate']}` for {_model(g)}: {g['status'].replace('_', ' ')}.")
    for name, families in EXPECTED_FAMILIES.items():
        present = {r["metric"] for r in tables.get(name, [])}
        for family in families:
            if not any(m == family or m.startswith(family) for m in present):
                items.append(f"`{name}` has no `{family}` rows (arm or field not recorded yet).")
    for launch in info.get("launches", []):
        if launch.get("failed"):
            items.append(
                f"Launch `{launch['launch']}` ({launch['model']}) failed: {launch['failure']}."
            )
        if launch.get("cases_skipped_budget"):
            items.append(
                f"Launch `{launch['launch']}`: {launch['cases_skipped_budget']} cases skipped "
                "(time budget)."
            )
    if info.get("invalid_record_lines"):
        items.append(
            f"{len(info['invalid_record_lines'])} malformed record lines skipped "
            "(see run_info.json)."
        )
    if info.get("invalid_case_lines"):
        items.append(
            f"{len(info['invalid_case_lines'])} malformed case lines skipped (see run_info.json)."
        )
    if info.get("records_without_case"):
        items.append(
            f"{info['records_without_case']} records reference a case not in the suites (unscored)."
        )
    items.extend(ALWAYS_UNVERIFIED)
    return items
