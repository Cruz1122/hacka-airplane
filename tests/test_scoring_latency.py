from __future__ import annotations

import pytest
from test_scoring_fixtures import completion, record

from nevados_bench.schemas import Completion
from nevados_bench.scoring.latency import (
    cache_arm,
    latency_metric_rows,
    output_bucket,
    resource_metric_rows,
    tps_metric_rows,
)


def by_metric(rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    return {(r["metric"], r["slice_dim"], r["slice_value"]): r for r in rows}


def speed_records() -> list:
    recs = []
    for i, tokens in enumerate((500, 1000, 2000, 4000)):
        total = 100 + tokens * 0.5  # 500 ms per 1k tokens + 100 ms intercept
        recs.append(
            record(
                None,
                arm="cold",
                case_id=f"s{i}",
                context_level=["0.5k", "1k", "2k", "4k"][i],
                prompt_tokens_total=tokens,
                tools_n=i,
                completion=completion(
                    cache_n=0,
                    prompt_n=tokens,
                    total_ms=total,
                    prompt_ms=total * 0.6,
                    predicted_ms=total * 0.3,
                    ttft_ms=total * 0.6,
                ),
                ts=f"2026-11-14T00:00:0{i + 1}Z",
            )
        )
    return recs


def test_cache_arm_and_output_bucket():
    assert cache_arm(record(None, arm="warm")) == "warm"
    assert cache_arm(record(None, completion=completion(cache_n=10))) == "warm"
    assert cache_arm(record(None, completion=completion(cache_n=None))) == "unknown"
    assert output_bucket(record(None, tags={"output_len": 64})) == 64
    assert output_bucket(record(None, completion=completion(predicted_n=200))) == 256


def test_latency_distribution_regression_shares_and_slo():
    warmup = record(
        None,
        arm="warmup",
        case_id="w",
        ts="2026-11-14T00:00:00Z",
        completion=completion(total_ms=9999.0),
    )
    rows = by_metric(latency_metric_rows([warmup, *speed_records()]))
    first = rows[("first_request_total_ms", "batch", "B2")]
    assert first["value"] == 9999.0
    p50 = rows[("total_ms_p50", "context_level×cache×call_type", "*|*|answer")]
    assert p50["n"] == 4 and p50["value"] == pytest.approx(850.0)
    assert p50["ci_low"] is not None and p50["low_n"] is True
    slope = rows[("total_ms_vs_prompt_tokens_slope_ms_per_1k_tokens", "call_type", "*")]
    assert slope["value"] == pytest.approx(500.0)
    assert rows[("total_ms_vs_prompt_tokens_intercept_ms", "call_type", "*")][
        "value"
    ] == pytest.approx(100)
    share = rows[("prefill_share", "context_level×cache×call_type", "*|*|answer")]
    assert share["value"] == pytest.approx(0.6)
    overhead = rows[("overhead_share", "context_level×cache×call_type", "*|*|answer")]
    assert overhead["value"] == pytest.approx(0.1)
    slo = rows[("request_slo_2s", "context_level×cache×call_type", "*|*|answer")]
    assert slo["value"] == 0.75  # 2100 ms misses the 2 s SLO
    assert rows[("timeouts", "all", "all")]["value"] == 0


def test_turn_and_dialogue_end_to_end():
    recs = []
    for turn, totals in enumerate(((1500.0, 1000.0), (4000.0,))):
        for step, total in enumerate(totals):
            recs.append(
                record(
                    None,
                    arm="history_full",
                    case_id=f"t{turn}s{step}",
                    tags={"dialogue_id": "d1", "turn_index": turn},
                    completion=completion(total_ms=total, prompt_n=100),
                )
            )
    rows = by_metric(latency_metric_rows(recs))
    assert rows[("turn_e2e_ms_max", "arm", "history_full")]["value"] == 4000.0
    assert rows[("turn_slo_2s", "arm", "history_full")]["value"] == 0.0
    assert rows[("turn_slo_5s", "arm", "history_full")]["value"] == 1.0
    assert rows[("dialogue_e2e_ms_mean", "arm", "history_full")]["value"] == 6500.0
    assert rows[("reprocessed_tokens_per_turn", "arm", "history_full")]["value"] == 150.0


def test_cache_ratio_and_prefix_delta():
    recs = [
        record(
            None,
            arm="prefix_stable",
            case_id="c",
            completion=completion(cache_n=900, prompt_n=100, ttft_ms=50.0),
        ),
        record(
            None,
            arm="prefix_dynamic",
            case_id="c",
            completion=completion(cache_n=0, prompt_n=1000, ttft_ms=500.0),
        ),
    ]
    rows = by_metric(latency_metric_rows(recs))
    assert rows[("cache_hit_ratio", "arm×call_type", "prefix_stable|answer")]["value"] == 0.9
    delta = rows[("ttft_ms_delta_stable_minus_dynamic", "arm_pair", "prefix_stable-prefix_dynamic")]
    assert delta["value"] == -450.0


def test_tps_threads_sustained_and_memory():
    recs = []
    for threads, tps in ((1, 10.0), (2, 18.0), (4, 30.0)):
        recs.append(
            record(
                None,
                threads=threads,
                case_id=f"t{threads}",
                completion=completion(predicted_tps=tps),
            )
        )
    for i in range(10):
        recs.append(
            record(
                None,
                arm="sustained",
                case_id="sus",
                tags={"turn_index": i},
                completion=completion(predicted_tps=20.0 if i < 5 else 18.0),
            )
        )
    rows = by_metric(tps_metric_rows(recs))
    assert rows[("decode_tps_scaling_efficiency", "threads", "2")]["value"] == pytest.approx(0.9)
    assert rows[("decode_tps_scaling_efficiency", "threads", "4")]["value"] == pytest.approx(0.75)
    assert rows[("decode_tps_drift_pct", "arm", "sustained")]["value"] == pytest.approx(-10.0)
    assert ("prefill_tps_cold_p50", "context_level", "1k") in rows
    assert ("decode_tps_p50", "output_len", "16") in rows
    eff = rows[("effective_e2e_tps_p50", "all", "all")]
    assert eff["value"] == pytest.approx(20.0)
    assert rows[("decode_tps_per_gib_peak", "all", "all")]["value"] == pytest.approx(
        9.0
    )  # median 18 tok/s over 2 GiB


def test_code_only_steps_are_ignored():
    code = record(
        None,
        arm="free_run",
        case_id="d1:t1:s0",
        tags={"kind": "code"},
        completion=Completion(),
        ts="2026-11-13T00:00:00Z",
        mem_peak=None,
    )
    base = speed_records()
    with_code = by_metric(latency_metric_rows([code, *base]))
    without = by_metric(latency_metric_rows(base))
    assert with_code == without
    assert with_code[("timeouts", "all", "all")]["n"] == 4
    assert by_metric(tps_metric_rows([code, *base])) == by_metric(tps_metric_rows(base))
    res = by_metric(resource_metric_rows([code, *base]))
    assert res[("requests", "all", "all")]["value"] == 4


def test_resources():
    recs = [
        record(
            None,
            mem_peak=3 * 1024**3,
            mem_anon=100,
            mem_file=200,
            pgmajfault_delta=4,
            oom_events=0,
            ctx_size=4096,
        ),
        record(None, mem_peak=1024**3, pgmajfault_delta=1, ctx_size=8192),
    ]
    launches = [
        {
            "model_id": "model-x",
            "quant": "Q4_K_M",
            "profile": "phone-tight",
            "launch": "B1/model-x",
            "load_ms": 1500.0,
            "gguf_size_bytes": 10,
        },
        {
            "model_id": "model-x",
            "quant": "Q4_K_M",
            "profile": "phone-tight",
            "launch": "B1/model-x@t1",
            "load_ms": 2500.0,
            "gguf_size_bytes": 10,
        },
        {
            "model_id": "model-y",
            "quant": "Q4_K_M",
            "profile": "phone-tight",
            "launch": "B1/model-y",
            "start_error": "unknown architecture",
        },
    ]
    rows = resource_metric_rows(recs, launches)
    x = by_metric([r for r in rows if r["model_id"] == "model-x"])
    assert x[("mem_peak_max", "all", "all")]["value"] == 3 * 1024**3
    assert x[("mem_peak_max", "ctx_size", "8192")]["value"] == 1024**3
    assert x[("pgmajfault_sum", "all", "all")]["value"] == 5
    assert x[("load_ms", "launch", "B1/model-x@t1")]["value"] == 2500.0
    assert x[("load_ms", "all", "all")]["value"] == 2000.0
    assert x[("gguf_size_bytes", "all", "all")]["value"] == 10
    assert x[("oom_events_max", "all", "all")]["value"] == 0
    assert x[("launch_failure_rate", "all", "all")]["value"] == 0.0
    y = by_metric([r for r in rows if r["model_id"] == "model-y"])
    assert y[("launch_failure_rate", "all", "all")]["value"] == 1.0
    assert y[("requests", "all", "all")]["value"] == 0
