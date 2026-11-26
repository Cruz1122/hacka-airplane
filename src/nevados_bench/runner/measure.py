"""One measured request: probe snapshots around the call plus derived fields."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from nevados_bench.runner.probe import CgroupProbe, CgroupSnapshot, HostProbe
from nevados_bench.schemas import Completion, LLMBackend, PromptRequest, RequestRecord


def _delta(after: int | None, before: int | None) -> int | None:
    return after - before if after is not None and before is not None else None


def _mean(*values: float | None) -> float | None:
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None


def derive(completion: Completion) -> dict[str, Any]:
    c = completion
    prompt_total = (
        c.cache_n + c.prompt_n if c.cache_n is not None and c.prompt_n is not None else None
    )
    overhead = (
        c.total_ms - c.prompt_ms - c.predicted_ms
        if None not in (c.total_ms, c.prompt_ms, c.predicted_ms)
        else None
    )
    return {
        "prompt_tokens_total": prompt_total,
        "overhead_ms": overhead,
        "truncated": c.finish_reason == "length",
    }


def run_request(
    backend: LLMBackend,
    probe: CgroupProbe | None,
    host_probe: HostProbe | None,
    request: PromptRequest,
    record_template: dict[str, Any],
) -> RequestRecord:
    """Execute `request` and return a RequestRecord.

    `record_template` holds identity fields (run_id, batch, suite, case_id, model_id, ...).
    Sampling, seed, tools_n and ts are filled from the request unless the template sets
    them. memory.peak is the cgroup's lifetime peak (resetting it needs write access).
    Host frequency/temperature are the mean of the before/after samples.
    """
    ts = datetime.now(UTC).isoformat()
    freq0 = host_probe.freq_mhz() if host_probe else None
    temp0 = host_probe.temp_c() if host_probe else None
    before: CgroupSnapshot | None = probe.snapshot() if probe else None
    completion = backend.complete(request)
    after: CgroupSnapshot | None = probe.snapshot() if probe else None
    freq1 = host_probe.freq_mhz() if host_probe else None
    temp1 = host_probe.temp_c() if host_probe else None

    reasoning_tokens: int | None = 0
    if completion.reasoning_content:
        count = getattr(backend, "count_reasoning_tokens", None)
        try:
            reasoning_tokens = count(completion) if callable(count) else None
        except Exception:  # count is best-effort metadata; the server may be gone (OOM)
            reasoning_tokens = None

    sampling = {"temperature": request.temperature, "top_p": request.top_p, "top_k": request.top_k}
    fields: dict[str, Any] = {
        "ts": ts,
        "seed": request.seed,
        "sampling": {k: v for k, v in sampling.items() if v is not None},
        "tools_n": len(request.tools or []),
    }
    fields.update(record_template)
    fields.update(derive(completion))
    fields.update(
        completion=completion,
        reasoning_tokens=reasoning_tokens,
        host_freq_mhz=_mean(freq0, freq1),
        host_temp_c=_mean(temp0, temp1),
    )
    if after is not None:
        fields.update(
            mem_current=after.memory_current,
            mem_peak=after.memory_peak,
            mem_anon=after.anon,
            mem_file=after.file,
            pgmajfault_delta=_delta(after.pgmajfault, before.pgmajfault if before else None),
            oom_events=_delta(after.oom_kill, before.oom_kill if before else None),
            cpu_usage_usec_delta=_delta(
                after.cpu_usage_usec, before.cpu_usage_usec if before else None
            ),
            nr_throttled=_delta(after.nr_throttled, before.nr_throttled if before else None),
        )
    return RequestRecord.model_validate(fields)
