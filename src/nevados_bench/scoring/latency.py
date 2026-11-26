"""Latency (§1), throughput (§2) and resource (§6) metrics from raw request records.

Conventions:
- Warm-up requests (`arm == "warmup"` or `tags.warmup`) and requests with an HTTP error
  are excluded from distributions; they still count for first-request latency and
  timeouts respectively. Code-only free-run steps (`tags.kind == "code"`) are not model
  requests and are ignored everywhere (latency, TPS, timeouts, resources).
- Cache arm: `arm` when it is "cold"/"warm", otherwise "cold" if `cache_n == 0`, "warm" if
  `cache_n > 0`, else "unknown".
- Prefill tok/s = `prompt_tps` (or prompt_n / prompt_ms); decode tok/s = `predicted_tps`
  (or predicted_n / predicted_ms). Prefill speed is reported on cold requests only.
- Output-length bucket: `tags.output_len`, else `sampling.max_tokens` when it is one of
  16/64/256, else predicted_n bucketed (<=32 -> 16, <=128 -> 64, else 256).
- User turn = records sharing (arm, rep, tags.dialogue_id, tags.turn_index); its
  end-to-end latency is the sum of `total_ms` of its calls. Requests without a
  dialogue id are each their own turn for the request-level SLO.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

from nevados_bench.schemas import RequestRecord
from nevados_bench.scoring.stats import mean, ols, paired_delta, percentile, stable_seed, stdev
from nevados_bench.scoring.tidy import (
    ANY,
    ModelKey,
    compact,
    describe_rows,
    mean_row,
    metric_row,
    model_key,
    rate_row,
)

SLO_SECONDS = (2, 5, 10)
OUTPUT_BUCKETS = (16, 64, 256)
SUSTAINED_ARM = "sustained"
SUSTAINED_WINDOW = 5
PREFIX_ARMS = ("prefix_stable", "prefix_dynamic")
GIB = 1024**3


def is_warmup(record: RequestRecord) -> bool:
    return record.arm == "warmup" or bool(record.tags.get("warmup"))


def is_code_step(record: RequestRecord) -> bool:
    """Code-only FSM step (free run): empty Completion, not a model request."""
    return record.tags.get("kind") == "code"


def cache_arm(record: RequestRecord) -> str:
    if record.arm in ("cold", "warm"):
        return record.arm
    cache_n = record.completion.cache_n
    if cache_n is None:
        return "unknown"
    return "cold" if cache_n == 0 else "warm"


def prefill_tps(record: RequestRecord) -> float | None:
    c = record.completion
    if c.prompt_tps is not None:
        return c.prompt_tps
    if c.prompt_n and c.prompt_ms:
        return c.prompt_n / c.prompt_ms * 1000
    return None


def decode_tps(record: RequestRecord) -> float | None:
    c = record.completion
    if c.predicted_tps is not None:
        return c.predicted_tps
    if c.predicted_n and c.predicted_ms:
        return c.predicted_n / c.predicted_ms * 1000
    return None


def prompt_tokens(record: RequestRecord) -> int | None:
    if record.prompt_tokens_total is not None:
        return record.prompt_tokens_total
    c = record.completion
    if c.prompt_n is None:
        return None
    return (c.cache_n or 0) + c.prompt_n


def output_bucket(record: RequestRecord) -> int | None:
    tagged = record.tags.get("output_len")
    if tagged is not None:
        return int(tagged)
    max_tokens = record.sampling.get("max_tokens")
    if max_tokens in OUTPUT_BUCKETS:
        return int(max_tokens)
    n = record.completion.predicted_n
    if n is None:
        return None
    return 16 if n <= 32 else 64 if n <= 128 else 256


def _usable(records: Iterable[RequestRecord]) -> list[RequestRecord]:
    return [
        r
        for r in records
        if not is_warmup(r) and not is_code_step(r) and not r.completion.http_error
    ]


def _by_key(records: Iterable[RequestRecord]) -> dict[ModelKey, list[RequestRecord]]:
    groups: dict[ModelKey, list[RequestRecord]] = defaultdict(list)
    for record in records:
        groups[model_key(record)].append(record)
    return dict(sorted(groups.items()))


def _turn_groups(records: Iterable[RequestRecord]) -> dict[tuple[Any, ...], list[RequestRecord]]:
    turns: dict[tuple[Any, ...], list[RequestRecord]] = defaultdict(list)
    for r in records:
        dialogue_id = r.tags.get("dialogue_id")
        if dialogue_id is None:
            continue
        turns[(r.arm, r.rep, dialogue_id, r.tags.get("turn_index"))].append(r)
    return turns


def latency_metric_rows(records: Iterable[RequestRecord]) -> list[dict[str, Any]]:
    """Rows for latency.csv."""
    all_records = list(records)
    out: list[dict[str, Any] | None] = []
    for key, recs in _by_key(r for r in all_records if not is_code_step(r)).items():
        out.extend(_first_request_rows(key, recs))
        usable = _usable(recs)
        cells: dict[str, list[RequestRecord]] = defaultdict(list)
        for r in usable:
            cells[f"{r.context_level}|{cache_arm(r)}|{r.call_type}"].append(r)
            cells[f"{ANY}|{ANY}|{r.call_type}"].append(r)
        for cell, crecs in sorted(cells.items()):
            dim = "context_level×cache×call_type"
            for metric in ("ttft_ms", "ttfc_ms", "total_ms"):
                vals = [getattr(r.completion, metric) for r in crecs]
                out.extend(
                    describe_rows(key, ANY, dim, cell, metric, [v for v in vals if v is not None])
                )
            out.extend(_share_rows(key, dim, cell, crecs))
            totals = [r.completion.total_ms for r in crecs if r.completion.total_ms is not None]
            p50, p95 = percentile(totals, 50), percentile(totals, 95)
            if p50:
                out.append(
                    metric_row(key, ANY, dim, cell, "tail_ratio_p95_p50", len(totals), p95 / p50)
                )
            for seconds in SLO_SECONDS:
                out.append(
                    rate_row(
                        key,
                        ANY,
                        dim,
                        cell,
                        f"request_slo_{seconds}s",
                        (t <= seconds * 1000 for t in totals),
                    )
                )
        out.append(
            rate_row(key, ANY, "all", "all", "timeout_rate", (r.completion.timeout for r in recs))
        )
        out.append(
            metric_row(
                key,
                ANY,
                "all",
                "all",
                "timeouts",
                len(recs),
                float(sum(r.completion.timeout for r in recs)),
            )
        )
        out.extend(_regression_rows(key, usable))
        out.extend(_turn_rows(key, usable))
        out.extend(_cache_rows(key, usable))
    return compact(out)


def _first_request_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    by_batch: dict[str, list[RequestRecord]] = defaultdict(list)
    for r in recs:
        by_batch[r.batch].append(r)
    rows: list[dict[str, Any] | None] = []
    for batch, brecs in sorted(by_batch.items()):
        first = min(brecs, key=lambda r: r.ts)
        if first.completion.total_ms is not None:
            rows.append(
                metric_row(
                    key, ANY, "batch", batch, "first_request_total_ms", 1, first.completion.total_ms
                )
            )
    return rows


def _share_rows(
    key: ModelKey, dim: str, cell: str, recs: list[RequestRecord]
) -> list[dict[str, Any] | None]:
    timed = [
        r
        for r in recs
        if r.completion.total_ms
        and r.completion.prompt_ms is not None
        and r.completion.predicted_ms is not None
    ]
    if not timed:
        return []
    total = sum(r.completion.total_ms or 0.0 for r in timed)
    prefill = sum(r.completion.prompt_ms or 0.0 for r in timed)
    decode = sum(r.completion.predicted_ms or 0.0 for r in timed)
    n = len(timed)
    return [
        metric_row(key, ANY, dim, cell, "prefill_share", n, prefill / total),
        metric_row(key, ANY, dim, cell, "decode_share", n, decode / total),
        metric_row(
            key, ANY, dim, cell, "overhead_share", n, max(0.0, total - prefill - decode) / total
        ),
    ]


def _regression_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    by_type: dict[str, list[RequestRecord]] = defaultdict(list)
    for r in recs:
        by_type[str(r.call_type)].append(r)
        by_type[ANY].append(r)
    for call_type, trecs in sorted(by_type.items()):
        fits = {
            "total_ms_vs_prompt_tokens": [(prompt_tokens(r), r.completion.total_ms) for r in trecs],
            "prompt_ms_vs_prompt_tokens_cold": [
                (prompt_tokens(r), r.completion.prompt_ms) for r in trecs if cache_arm(r) == "cold"
            ],
            "total_ms_vs_tools_n": [(r.tools_n, r.completion.total_ms) for r in trecs],
        }
        for name, pairs in fits.items():
            pairs = [(float(x), float(y)) for x, y in pairs if x is not None and y is not None]
            fit = ols([p[0] for p in pairs], [p[1] for p in pairs])
            if fit is None:
                continue
            per_1k = 1000.0 if "prompt_tokens" in name else 1.0
            unit = "slope_ms_per_1k_tokens" if per_1k == 1000.0 else "slope_ms_per_tool"
            n = len(pairs)
            rows.append(
                metric_row(
                    key, ANY, "call_type", call_type, f"{name}_{unit}", n, fit["slope"] * per_1k
                )
            )
            rows.append(
                metric_row(
                    key, ANY, "call_type", call_type, f"{name}_intercept_ms", n, fit["intercept"]
                )
            )
            rows.append(metric_row(key, ANY, "call_type", call_type, f"{name}_r2", n, fit["r2"]))
    return rows


def _turn_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    turns = _turn_groups(recs)
    by_arm: dict[str, list[float]] = defaultdict(list)
    reprocessed: dict[str, list[float]] = defaultdict(list)
    dialogues: dict[tuple[Any, ...], float] = defaultdict(float)
    for (arm, rep, dialogue_id, _), trecs in turns.items():
        if any(r.completion.total_ms is None for r in trecs):
            continue
        total = sum(r.completion.total_ms or 0.0 for r in trecs)
        by_arm[arm].append(total)
        reprocessed[arm].append(float(sum(r.completion.prompt_n or 0 for r in trecs)))
        dialogues[(arm, rep, dialogue_id)] += total
    for arm, totals in sorted(by_arm.items()):
        rows.extend(describe_rows(key, ANY, "arm", arm, "turn_e2e_ms", totals))
        for seconds in SLO_SECONDS:
            rows.append(
                rate_row(
                    key,
                    ANY,
                    "arm",
                    arm,
                    f"turn_slo_{seconds}s",
                    (t <= seconds * 1000 for t in totals),
                )
            )
        rows.append(mean_row(key, ANY, "arm", arm, "reprocessed_tokens_per_turn", reprocessed[arm]))
        dial = [v for (a, _, _), v in sorted(dialogues.items(), key=str) if a == arm]
        rows.extend(describe_rows(key, ANY, "arm", arm, "dialogue_e2e_ms", dial))
    return rows


def _cache_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    groups: dict[str, list[float]] = defaultdict(list)
    for r in recs:
        c = r.completion
        if c.cache_n is None or c.prompt_n is None or (c.cache_n + c.prompt_n) == 0:
            continue
        ratio = c.cache_n / (c.cache_n + c.prompt_n)
        groups[f"{r.arm}|{r.call_type}"].append(ratio)
        groups[f"{ANY}|{r.call_type}"].append(ratio)
    for cell, ratios in sorted(groups.items()):
        rows.append(mean_row(key, ANY, "arm×call_type", cell, "cache_hit_ratio", ratios))
    stable, dynamic = PREFIX_ARMS
    paired: dict[str, dict[tuple[Any, ...], RequestRecord]] = defaultdict(dict)
    for r in recs:
        if r.arm in PREFIX_ARMS:
            paired[r.arm][(r.case_id, r.rep)] = r
    shared = sorted(set(paired[stable]) & set(paired[dynamic]), key=str)
    for metric in ("ttft_ms", "prompt_n"):
        pairs = [
            (
                getattr(paired[stable][k].completion, metric),
                getattr(paired[dynamic][k].completion, metric),
            )
            for k in shared
        ]
        pairs = [(float(a), float(b)) for a, b in pairs if a is not None and b is not None]
        if pairs:
            delta, lo, hi = paired_delta(
                [p[0] for p in pairs],
                [p[1] for p in pairs],
                seed=stable_seed(*key, "prefix", metric),
            )
            rows.append(
                metric_row(
                    key,
                    ANY,
                    "arm_pair",
                    f"{stable}-{dynamic}",
                    f"{metric}_delta_stable_minus_dynamic",
                    len(pairs),
                    delta,
                    lo,
                    hi,
                )
            )
    return rows


def tps_metric_rows(records: Iterable[RequestRecord]) -> list[dict[str, Any]]:
    """Rows for tps.csv."""
    out: list[dict[str, Any] | None] = []
    for key, recs in _by_key(_usable(records)).items():
        cold = [r for r in recs if cache_arm(r) == "cold"]
        for level, lrecs in sorted(_group(cold, lambda r: r.context_level).items()):
            out.extend(
                describe_rows(
                    key, ANY, "context_level", level, "prefill_tps_cold", _vals(lrecs, prefill_tps)
                )
            )
        for level, lrecs in sorted(_group(recs, lambda r: r.context_level).items()):
            out.extend(
                describe_rows(
                    key, ANY, "context_level", level, "decode_tps", _vals(lrecs, decode_tps)
                )
            )
        for bucket, brecs in sorted(_group(recs, output_bucket).items()):
            out.extend(
                describe_rows(
                    key, ANY, "output_len", bucket, "decode_tps", _vals(brecs, decode_tps)
                )
            )
        thread_medians: dict[str, dict[int, float]] = defaultdict(dict)
        for threads, trecs in sorted(_group(recs, lambda r: r.threads).items()):
            for metric, fn, src in (
                ("decode_tps", decode_tps, trecs),
                ("prefill_tps_cold", prefill_tps, [r for r in trecs if cache_arm(r) == "cold"]),
            ):
                vals = _vals(src, fn)
                out.extend(describe_rows(key, ANY, "threads", threads, metric, vals))
                med = percentile(vals, 50)
                if med is not None:
                    thread_medians[metric][int(threads)] = med
        for metric, medians in thread_medians.items():
            if len(medians) < 2:
                continue
            base_t = min(medians)
            for threads, med in sorted(medians.items()):
                eff = med / (medians[base_t] * threads / base_t)
                out.append(
                    metric_row(key, ANY, "threads", threads, f"{metric}_scaling_efficiency", 1, eff)
                )
        out.extend(_sustained_rows(key, recs))
        effective = [
            r.completion.predicted_n / r.completion.total_ms * 1000
            for r in recs
            if r.completion.predicted_n is not None and r.completion.total_ms
        ]
        out.extend(describe_rows(key, ANY, "all", "all", "effective_e2e_tps", effective))
        answers = [
            float(r.completion.predicted_n)
            for r in recs
            if r.call_type == "answer" and r.completion.predicted_n is not None
        ]
        out.extend(describe_rows(key, ANY, "call_type", "answer", "tokens_per_answer", answers))
        peaks = [r.mem_peak for r in recs if r.mem_peak]
        decode_med = percentile(_vals(recs, decode_tps), 50)
        if peaks and decode_med is not None:
            out.append(
                metric_row(
                    key,
                    ANY,
                    "all",
                    "all",
                    "decode_tps_per_gib_peak",
                    len(recs),
                    decode_med / (max(peaks) / GIB),
                )
            )
        out.extend(_rep_cv_rows(key, recs))
    return compact(out)


def _group(recs: Iterable[RequestRecord], fn: Any) -> dict[Any, list[RequestRecord]]:
    groups: dict[Any, list[RequestRecord]] = defaultdict(list)
    for r in recs:
        value = fn(r)
        if value is not None:
            groups[value].append(r)
    return groups


def _vals(recs: Iterable[RequestRecord], fn: Any) -> list[float]:
    return [float(v) for v in (fn(r) for r in recs) if v is not None]


def _sustained_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    sustained = sorted(
        (r for r in recs if r.arm == SUSTAINED_ARM and decode_tps(r) is not None),
        key=lambda r: (r.rep, r.tags.get("turn_index", 0), r.ts),
    )
    if len(sustained) < 2 * SUSTAINED_WINDOW:
        return []
    first = mean(_vals(sustained[:SUSTAINED_WINDOW], decode_tps))
    last = mean(_vals(sustained[-SUSTAINED_WINDOW:], decode_tps))
    if not first or last is None:
        return []
    n = len(sustained)
    return [
        metric_row(key, ANY, "arm", SUSTAINED_ARM, "decode_tps_first5_mean", n, first),
        metric_row(key, ANY, "arm", SUSTAINED_ARM, "decode_tps_last5_mean", n, last),
        metric_row(
            key, ANY, "arm", SUSTAINED_ARM, "decode_tps_drift_pct", n, (last - first) / first * 100
        ),
    ]


def _rep_cv_rows(key: ModelKey, recs: list[RequestRecord]) -> list[dict[str, Any] | None]:
    groups = _group(
        recs, lambda r: (r.suite, r.case_id, r.arm, r.context_level, str(r.tags.get("turn_index")))
    )
    rows: list[dict[str, Any] | None] = []
    for metric, fn in (("decode_tps", decode_tps), ("total_ms", lambda r: r.completion.total_ms)):
        cvs = []
        for grecs in groups.values():
            vals = _vals(grecs, fn)
            sd, mu = stdev(vals), mean(vals)
            if sd is not None and mu:
                cvs.append(sd / mu)
        rows.append(mean_row(key, ANY, "all", "all", f"{metric}_rep_cv_mean", cvs))
    return rows


LAUNCH_FAILURE_FIELDS = ("start_error", "oom_killed", "died")


def launch_failed(meta: Mapping[str, Any]) -> bool:
    return any(meta.get(field) for field in LAUNCH_FAILURE_FIELDS)


def resource_metric_rows(
    records: Iterable[RequestRecord],
    launches: Iterable[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Rows for resources.csv, pooled over fc modes (resources do not depend on them).

    `launches` are the per-launch `meta.json` dicts (with a `launch` key naming the
    launch directory). `load_ms` / `gguf_size_bytes` are read from them, else from record
    extra fields. Code-only steps are ignored.
    """
    groups: dict[ModelKey, list[RequestRecord]] = defaultdict(list)
    for r in records:
        if not is_code_step(r):
            groups[(r.model_id, r.quant, r.profile, ANY)].append(r)
    by_key: dict[ModelKey, list[Mapping[str, Any]]] = defaultdict(list)
    for meta in launches or []:
        key = (str(meta.get("model_id")), str(meta.get("quant")), str(meta.get("profile")), ANY)
        by_key[key].append(meta)
        groups.setdefault(key, [])
    out: list[dict[str, Any] | None] = []
    for key, recs in sorted(groups.items()):
        metas = sorted(by_key.get(key, []), key=lambda m: str(m.get("launch")))
        loads = {
            str(m.get("launch")): m.get("load_ms") for m in metas if m.get("load_ms") is not None
        }
        sizes = [m.get("gguf_size_bytes") for m in metas if m.get("gguf_size_bytes") is not None]
        for r in recs:
            extra = r.model_extra or {}
            if not metas and extra.get("load_ms") is not None:
                loads.setdefault("records", extra["load_ms"])
            if extra.get("gguf_size_bytes") is not None:
                sizes.append(extra["gguf_size_bytes"])
        for launch, load in sorted(loads.items()):
            out.append(metric_row(key, ANY, "launch", launch, "load_ms", 1, float(load)))
        out.append(mean_row(key, ANY, "all", "all", "load_ms", loads.values()))
        if sizes:
            out.append(metric_row(key, ANY, "all", "all", "gguf_size_bytes", 1, float(max(sizes))))
        if metas:
            out.append(
                rate_row(
                    key, ANY, "all", "all", "launch_failure_rate", (launch_failed(m) for m in metas)
                )
            )
            for m in metas:
                out.append(
                    metric_row(
                        key,
                        ANY,
                        "launch",
                        m.get("launch"),
                        "launch_failed",
                        1,
                        float(launch_failed(m)),
                    )
                )
        for field in ("mem_peak", "mem_anon", "mem_file", "oom_events"):
            vals = [getattr(r, field) for r in recs if getattr(r, field) is not None]
            if vals:
                out.append(
                    metric_row(key, ANY, "all", "all", f"{field}_max", len(vals), float(max(vals)))
                )
        faults = [r.pgmajfault_delta for r in recs if r.pgmajfault_delta is not None]
        if faults:
            out.append(
                metric_row(
                    key, ANY, "all", "all", "pgmajfault_sum", len(faults), float(sum(faults))
                )
            )
        for ctx, crecs in sorted(_group(recs, lambda r: r.ctx_size).items()):
            peaks = [r.mem_peak for r in crecs if r.mem_peak is not None]
            if peaks:
                out.append(
                    metric_row(
                        key, ANY, "ctx_size", ctx, "mem_peak_max", len(peaks), float(max(peaks))
                    )
                )
        out.append(metric_row(key, ANY, "all", "all", "requests", len(recs), float(len(recs))))
    return compact(out)
