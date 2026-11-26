from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest
from test_scoring_fixtures import (
    ANSWER_CASES,
    EXTRACT_CASES,
    ROUTE_CASES,
    FakeWorld,
    completion,
    make_dialogue,
    oracle_output,
    record,
    wrong_output,
)

from nevados_bench.report.aggregate import aggregate_run
from nevados_bench.report.markdown import ranked, write_report

ALL_CASES = ROUTE_CASES + EXTRACT_CASES + ANSWER_CASES


def write_suites(suites: Path) -> None:
    suites.mkdir()
    by_suite: dict[str, list[str]] = {}
    for case in ALL_CASES:
        by_suite.setdefault(case.suite, []).append(case.model_dump_json())
    for suite, lines in by_suite.items():
        (suites / f"{suite}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (suites / "dialogues.jsonl").write_text(
        make_dialogue().model_dump_json() + "\n", encoding="utf-8"
    )
    never_run = ALL_CASES[0].model_copy(update={"suite": "fc_tools_sweep", "case_id": "sweep_0"})
    (suites / "fc_tools_sweep.jsonl").write_text(
        never_run.model_dump_json() + "\n", encoding="utf-8"
    )


def write_model(run: Path, batch: str, model_id: str, output_fn, reps: int = 1, **kw) -> Path:
    model_dir = run / batch / model_id
    model_dir.mkdir(parents=True)
    lines = []
    for rep in range(reps):
        for i, case in enumerate(ALL_CASES):
            rec = record(
                case,
                output_fn(case),
                model_id=model_id,
                batch=batch,
                rep=rep,
                ts=f"2026-11-14T00:{rep:02d}:{i:02d}Z",
                **kw,
            )
            lines.append(rec.model_dump_json())
    path = model_dir / "requests.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def value(rows, model, metric, suite=None, dim="all", sv="all", fc_mode="uniform"):
    hits = [
        r
        for r in rows
        if r["model_id"] == model
        and r["metric"] == metric
        and r["slice_dim"] == dim
        and r["slice_value"] == sv
        and (suite is None or r["suite"] == suite)
        and r["fc_mode"] == fc_mode
    ]
    assert hits, (model, metric, suite, dim, sv)
    return float(hits[0]["value"])


@pytest.fixture
def run_dir(tmp_path: Path) -> tuple[Path, Path]:
    suites = tmp_path / "suites"
    write_suites(suites)
    run = tmp_path / "results" / "run1"
    write_model(run, "B2", "oracle", oracle_output, reps=5)
    wrong_path = write_model(run, "B2", "wrong", wrong_output, mem_peak=6 * 1024**3)
    # Crash mid-write: truncated trailing line must be skipped, not fatal.
    with wrong_path.open("a", encoding="utf-8") as handle:
        handle.write('{"run_id": "run1", "batch": "B2", "sui')
    return run, suites


def test_oracle_scores_100_and_wrong_scores_0(run_dir):
    run, suites = run_dir
    aggregate_run(run, suites, FakeWorld())
    metrics = run / "metrics"
    fc = read(metrics / "fc_rates.csv")
    assert value(fc, "oracle", "route_correct", "fc_core") == 1.0
    assert value(fc, "wrong", "route_correct", "fc_core") == 0.0
    assert value(fc, "oracle", "pass_hat_5", "fc_core", "arm", "default") == 1.0
    assert value(fc, "wrong", "over_call", "fc_core") == 1.0
    assert value(fc, "wrong", "fabricated_arg", "fc_core") == 1.0
    assert value(fc, "oracle", "arg_correct", "fc_core", "arg_type", "enum") == 1.0
    ex = read(metrics / "extract_rates.csv")
    assert value(ex, "oracle", "slot_correct") == 1.0 and value(ex, "wrong", "slot_correct") == 0.0
    gr = read(metrics / "grounding_rates.csv")
    assert value(gr, "oracle", "grounded_correct") == 1.0
    assert value(gr, "wrong", "grounded_correct") == 0.0
    assert value(gr, "wrong", "safety_fabrication", dim="safety", sv="True") == 1.0
    assert value(gr, "oracle", "outcome_faithful", dim="question_type", sv="schedule") == 0.5

    gates = {(g["model_id"], g["gate"]): g["status"] for g in read(metrics / "gates.csv")}
    assert gates[("oracle", "safety_critical_fabrication")] == "pass"
    assert gates[("wrong", "safety_critical_fabrication")] == "fail"
    assert gates[("oracle", "memory_peak_le_profile_limit")] == "pass"
    assert gates[("wrong", "memory_peak_le_profile_limit")] == "fail"
    assert gates[("oracle", "parse_ok_uniform_ge_99pct")] == "pass"

    per_tool = {(r["model_id"], r["tool"]): r for r in read(metrics / "fc_per_tool.csv")}
    assert float(per_tool[("oracle", "check_weather")]["f1"]) == 1.0
    confusion = read(metrics / "fc_confusion.csv")
    assert any(
        r["model_id"] == "wrong"
        and r["gold_label"] == "none"
        and r["pred_label"] == "register_visit"
        for r in confusion
    )
    mcnemar = read(metrics / "mcnemar.csv")
    assert {r["suite"] for r in mcnemar} >= {"fc_core", "grounded_qa"}
    pareto = read(metrics / "pareto.csv")
    assert {r["model_id"] for r in pareto if r["pareto"] == "true"} >= {"oracle"}

    info = json.loads((metrics / "run_info.json").read_text())
    assert len(info["invalid_record_lines"]) == 1
    coverage = {(r["model_id"], r["suite"]): r for r in read(metrics / "coverage.csv")}
    assert coverage[("oracle", "fc_core")]["coverage"] == "1"

    scored = [json.loads(line) for line in (run / "scored.jsonl").read_text().splitlines()]
    assert len(scored) == 5 * len(ALL_CASES) + len(ALL_CASES)
    for name in (
        "latency.csv",
        "tps.csv",
        "resources.csv",
        "deltas.csv",
        "dialogue_rates.csv",
        "dialogue_detail.csv",
    ):
        assert (metrics / name).is_file()


def test_report_and_idempotence(run_dir):
    run, suites = run_dir
    aggregate_run(run, suites, FakeWorld())
    write_report(run)
    first = {p.name: p.read_bytes() for p in (run / "metrics").iterdir()}
    first["REPORT.md"] = (run / "REPORT.md").read_bytes()
    first["scored.jsonl"] = (run / "scored.jsonl").read_bytes()
    aggregate_run(run, suites, FakeWorld())
    write_report(run)
    second = {p.name: p.read_bytes() for p in (run / "metrics").iterdir()}
    second["REPORT.md"] = (run / "REPORT.md").read_bytes()
    second["scored.jsonl"] = (run / "scored.jsonl").read_bytes()
    assert first == second

    report = (run / "REPORT.md").read_text(encoding="utf-8")
    for heading in (
        "## Batches",
        "### Batch B2",
        "## Hard gates",
        "## Leaderboards",
        "## Pareto",
        "## Coverage",
        "## Not run / not verified",
    ):
        assert heading in report
    assert "Suite `fc_tools_sweep`: defined but no records." in report
    assert "Suite `dialogues`: defined but no records." in report
    assert "FAIL" in report and "PASS" in report
    assert "1 malformed record lines skipped" in report


def test_partial_data_and_empty_run(tmp_path):
    suites = tmp_path / "suites"
    write_suites(suites)
    run = tmp_path / "results" / "empty"
    run.mkdir(parents=True)
    aggregate_run(run, suites, FakeWorld())
    write_report(run)
    report = (run / "REPORT.md").read_text(encoding="utf-8")
    assert "_No batch has produced records yet._" in report
    # A second batch arrives later for only one model: earlier output is simply extended.
    write_model(run, "B5", "oracle", oracle_output)
    aggregate_run(run, suites, FakeWorld())
    write_report(run)
    assert "### Batch B5" in (run / "REPORT.md").read_text(encoding="utf-8")
    # Missing suites directory: records are kept but nothing is scored.
    other = tmp_path / "results" / "nosuites"
    write_model(other, "B2", "oracle", oracle_output)
    aggregate_run(other, tmp_path / "missing", FakeWorld())
    info = json.loads((other / "metrics" / "run_info.json").read_text())
    assert info["scored"] == 0 and info["records_without_case"] == len(ALL_CASES)


def test_ranked_labels_ties_inside_ci():
    rows = [
        {"model_id": "a", "value": "0.9", "ci_low": "0.8", "ci_high": "0.95"},
        {"model_id": "b", "value": "0.85", "ci_low": "0.75", "ci_high": "0.9"},
        {"model_id": "c", "value": "0.3", "ci_low": "0.2", "ci_high": "0.4"},
    ]
    assert [rank for rank, _ in ranked(rows, higher_is_better=True)] == ["1", "=1", "3"]
    assert [r["model_id"] for _, r in ranked(rows, higher_is_better=False)] == ["c", "b", "a"]


def write_records(run: Path, launch: str, records, meta: dict | None = None) -> None:
    model_dir = run / launch
    model_dir.mkdir(parents=True, exist_ok=True)
    if records:
        lines = [r.model_dump_json() for r in records]
        (model_dir / "requests.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if meta is not None:
        (model_dir / "meta.json").write_text(json.dumps(meta), encoding="utf-8")


def test_arms_launches_and_free_run(tmp_path):

    suites = tmp_path / "suites"
    write_suites(suites)
    run = tmp_path / "results" / "run2"
    route = [c for c in ALL_CASES if c.call_type == "route"]
    answers = [c for c in ALL_CASES if c.call_type == "answer"]
    meta = {
        "model_id": "oracle",
        "quant": "Q4_K_M",
        "profile": "phone-tight",
        "load_ms": 1200.0,
        "gguf_size_bytes": 1000,
        "mem_limit": 4 * 1024**3,
    }
    write_records(
        run,
        "B2/oracle",
        [record(c, oracle_output(c), model_id="oracle") for c in ALL_CASES],
        {**meta, "records_written": len(ALL_CASES)},
    )
    b3 = [
        record(c, oracle_output(c), model_id="oracle", batch="B3", arm="passk", rep=rep)
        for c in route
        for rep in range(5)
    ]
    # Prefix arms answer wrongly: they must not leak into grounding rates.
    b3 += [
        record(
            c,
            wrong_output(c),
            model_id="oracle",
            batch="B3",
            arm=arm,
            completion=completion(cache_n=900 if arm == "prefix_stable" else 0),
        )
        for c in answers
        for arm in ("prefix_stable", "prefix_dynamic")
    ]
    write_records(run, "B3/oracle", b3, meta)
    write_records(run, "B2/wrong", [record(c, wrong_output(c), model_id="wrong") for c in route])
    write_records(
        run,
        "B3/wrong",
        [record(c, oracle_output(c), model_id="wrong", batch="B3", arm="retry") for c in route],
    )
    write_records(
        run,
        "B1/broken",
        [],
        {
            "model_id": "broken",
            "quant": "Q4_K_M",
            "profile": "phone-tight",
            "start_error": "unknown arch",
        },
    )
    free = [r.model_copy(update={"batch": "B4"}) for r in _free_run_records()]
    write_records(run, "B4/oracle", free, meta)

    aggregate_run(run, suites, FakeWorld())
    write_report(run)
    metrics = run / "metrics"
    fc = read(metrics / "fc_rates.csv")
    overall = [
        r
        for r in fc
        if r["model_id"] == "oracle"
        and r["metric"] == "route_correct"
        and r["slice_dim"] == "all"
        and r["suite"] == "fc_core"
    ]
    assert overall[0]["n"] == str(len(route))
    assert value(fc, "oracle", "pass_hat_5", "fc_core", "arm", "passk") == 1.0
    assert value(fc, "wrong", "retry_recovery", "fc_core", "arm", "retry") == 1.0
    assert value(fc, "wrong", "accuracy_with_one_retry", "fc_core", "arm", "retry") == 1.0
    assert value(fc, "wrong", "route_correct", "fc_core") == 0.0
    assert value(fc, "oracle", "missing_handled_clarify", "fc_core") == 1.0

    gr = read(metrics / "grounding_rates.csv")
    assert value(gr, "oracle", "grounded_correct") == 1.0
    assert not [r for r in gr if r["slice_value"].startswith("prefix_")]
    lat = read(metrics / "latency.csv")
    assert any(r["metric"] == "ttft_ms_delta_stable_minus_dynamic" for r in lat)

    gates = {(g["model_id"], g["gate"]): g["status"] for g in read(metrics / "gates.csv")}
    assert gates[("broken", "launch_ok")] == "fail"
    assert gates[("oracle", "launch_ok")] == "pass"
    coverage = {(r["model_id"], r["suite"], r["batch"]): r for r in read(metrics / "coverage.csv")}
    free_cov = coverage[("oracle", "dialogues:free_run", "B4")]
    assert free_cov["cases_run"] == "1" and free_cov["cases_defined"] == "1"
    assert free_cov["records"] == "2"  # the code-only step is not a request
    dl = read(metrics / "dialogue_rates.csv")
    assert value(dl, "oracle", "dialogue_success", dim="arm", sv="free_run") == 1.0
    info = json.loads((metrics / "run_info.json").read_text())
    assert info["records_without_case"] == 0
    report = (run / "REPORT.md").read_text(encoding="utf-8")
    assert (
        "Launch `B1/broken` (broken|Q4_K_M|phone-tight) failed: start_error: unknown arch."
        in report
    )
    assert "broken / Q4_K_M / phone-tight" in report


def _free_run_records():
    from test_scoring_dialogue import REGISTER

    from nevados_bench.schemas import Completion, ParsedOutput

    def rec(turn, step, parsed, kind="llm", **kw):
        return record(
            None,
            parsed,
            suite="dialogues",
            case_id=f"d1:t{turn}:s{step}",
            arm="free_run",
            model_id="oracle",
            call_type="route" if kind == "llm" else None,
            tags={"dialogue_id": "d1", "turn_index": turn, "step_index": step, "kind": kind},
            completion=completion() if kind == "llm" else Completion(),
            ts=f"2026-11-14T01:00:{turn:02d}.{step}Z",
            **kw,
        )

    partial = REGISTER.model_copy(update={"arguments": {"station": "estacion_a", "name": "Ana"}})
    return [
        rec(
            0,
            0,
            ParsedOutput(parse_ok=True, decision="call", calls=[partial]),
            path=["ROUTER", "SLOT_FILLING"],
        ),
        rec(0, 1, ParsedOutput(parse_ok=True, slot_value=4), path=["SLOT_FILLING", "CONFIRM"]),
        rec(
            1,
            0,
            None,
            kind="code",
            path=["CONFIRM", "EXECUTE", "ANSWER"],
            executed_call=REGISTER.model_dump(),
        ),
    ]
