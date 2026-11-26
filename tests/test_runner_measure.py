from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nevados_bench.runner.measure import run_request
from nevados_bench.runner.probe import CgroupProbe
from nevados_bench.runner.speed import ColdCacheError, run_speed_protocol
from nevados_bench.schemas import Completion, PromptRequest

TEMPLATE: dict[str, Any] = {
    "run_id": "r",
    "batch": "B1",
    "suite": "s",
    "case_id": "c",
    "model_id": "m",
    "gguf_file": "m.gguf",
    "quant": "Q4_K_M",
    "profile": "phone-tight",
    "threads": 3,
    "ctx_size": 12288,
}


class FakeBackend:
    def __init__(self, cg: Path | None = None) -> None:
        self.cg = cg
        self.requests: list[PromptRequest] = []
        self.erased = 0
        self.cached = False
        self.leaky = False  # simulate a server that reuses KV despite cache_prompt=false

    def complete(self, request: PromptRequest) -> Completion:
        self.requests.append(request)
        if self.cg is not None:
            (self.cg / "cpu.stat").write_text("usage_usec 1500\nnr_throttled 0\n")
            (self.cg / "memory.stat").write_text("anon 10\nfile 20\npgmajfault 7\n")
        cache_n = 30 if ((request.cache_prompt or self.leaky) and self.cached) else 0
        self.cached = True
        return Completion(
            content="x",
            reasoning_content="a b c",
            finish_reason="length",
            total_ms=100.0,
            cache_n=cache_n,
            prompt_n=10,
            prompt_ms=60.0,
            predicted_n=request.max_tokens,
            predicted_ms=30.0,
        )

    def count_reasoning_tokens(self, completion: Completion) -> int:
        return len(completion.reasoning_content.split())

    # speed-protocol client surface
    def count_prompt_tokens(self, messages: list[dict[str, Any]]) -> int:
        return 20 + sum(len(m["content"].split()) for m in messages)

    def erase_slot(self) -> None:
        self.erased += 1
        self.cached = False


def test_run_request_fills_deltas_and_derived(tmp_path: Path) -> None:
    cg = tmp_path
    (cg / "cpu.stat").write_text("usage_usec 1000\nnr_throttled 0\n")
    (cg / "memory.stat").write_text("anon 10\nfile 20\npgmajfault 2\n")
    (cg / "memory.current").write_text("500\n")
    (cg / "memory.peak").write_text("900\n")
    backend = FakeBackend(cg)
    req = PromptRequest(messages=[{"role": "user", "content": "hi"}], top_k=20, tools=[{}, {}])
    r = run_request(backend, CgroupProbe(cg), None, req, TEMPLATE)
    assert r.prompt_tokens_total == 10 and r.overhead_ms == 10.0 and r.truncated
    assert r.reasoning_tokens == 3
    assert r.cpu_usage_usec_delta == 500 and r.pgmajfault_delta == 5
    assert r.mem_current == 500 and r.mem_peak == 900 and r.oom_events is None
    assert r.sampling == {"temperature": 0.0, "top_k": 20} and r.tools_n == 2
    assert r.ts and r.host_freq_mhz is None


def test_run_request_without_probes() -> None:
    r = run_request(FakeBackend(), None, None, PromptRequest(messages=[]), TEMPLATE)
    assert r.mem_current is None and r.completion.content == "x"


def test_speed_protocol_shape() -> None:
    backend = FakeBackend()
    sink: list[Any] = []
    out = run_speed_protocol(
        backend,  # type: ignore[arg-type]
        None,
        None,
        lambda i: f"palabra{i} " * 50,
        TEMPLATE,
        threads=2,
        sink=sink.append,
        levels=("0.5k", "1k"),
        output_lengths=(16,),
        reps=2,
        sustained_n=3,
    )
    assert out == sink
    arms = [(r.case_id, r.arm) for r in out]
    assert arms.count(("speed:prefill:0.5k", "cold")) == 2  # warm-up discarded
    assert arms.count(("speed:prefill:1k", "warm")) == 2
    assert arms.count(("speed:decode:16", "decode")) == 2
    assert arms.count(("speed:sustained", "sustained")) == 3
    assert all(r.threads == 2 and r.suite == "speed" for r in out)
    assert all(r.completion.cache_n == 0 for r in out if r.arm == "cold")
    assert all(r.completion.cache_n for r in out if r.arm == "warm")
    tags = next(r.tags for r in out if r.case_id == "speed:prefill:0.5k")
    assert tags["measured_prompt_tokens"] <= 500
    assert backend.erased == 2 * 3  # per cold rep incl. warm-up
    assert all(r.extra_body == {"ignore_eos": True} for r in backend.requests)


def test_speed_protocol_rejects_warm_cold() -> None:
    backend = FakeBackend()
    backend.erase_slot = lambda: None  # type: ignore[method-assign]
    backend.cached = True
    backend.leaky = True
    with pytest.raises(ColdCacheError):
        run_speed_protocol(
            backend,  # type: ignore[arg-type]
            None,
            None,
            lambda i: "a " * 10,
            TEMPLATE,
            threads=3,
            levels=("0.5k",),
            output_lengths=(),
            sustained_n=0,
        )
