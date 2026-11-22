"""Every figure quoted in reports/r2/informe.tex, computed from results/ (no model calls).

Usage: uv run python reports/r2/numbers.py > reports/r2/numbers.txt
Turn latency = wall time of all model calls a visitor turn triggers (code steps cost ~0).
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "results"
MODELS = ("gemma4-e2b", "qwen3-1.7b", "granite4-micro", "qwen3-0.6b")


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def q(values: list[float], p: float) -> float | None:
    """Nearest-rank percentile."""
    if not values:
        return None
    s = sorted(values)
    return s[max(0, math.ceil(p * len(s)) - 1)]


def fmt(v: float | None, scale: float = 1.0, nd: int = 1) -> str:
    return "n/a" if v is None else f"{v / scale:.{nd}f}"


def section(title: str) -> None:
    print(f"\n## {title}")


def speed() -> None:
    section("B6 phone speed (ctx 4096, 4 threads on cpu4-7)")
    for model in MODELS:
        recs = load(ROOT / f"r2-phone/B6/{model}@c4k/requests.jsonl")
        meta_path = ROOT / f"r2-phone/B6/{model}@c4k/meta.json"
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        by = defaultdict(list)
        for r in recs:
            by[(r["arm"], r.get("context_level"))].append(r["completion"])
        dec = [c["predicted_tps"] for c in by[("decode", None)] if c.get("predicted_tps")]
        line = [f"{model}: decode tok/s p50 {fmt(q(dec, 0.5))}"]
        for level in ("0.5k", "1k", "2k"):
            cold = by[("cold", level)]
            warm = by[("warm", level)]
            pre = [c["prompt_tps"] for c in cold if c.get("prompt_tps")]
            ttft_c = [c["ttft_ms"] for c in cold if c.get("ttft_ms")]
            ttft_w = [c["ttft_ms"] for c in warm if c.get("ttft_ms")]
            line.append(
                f"{level}: prefill {fmt(q(pre, 0.5), nd=0)} tok/s, TTFT cold "
                f"{fmt(q(ttft_c, 0.5), 1000, 2)} s warm {fmt(q(ttft_w, 0.5), 1000, 2)} s"
            )
        sus = [r for r in recs if r["arm"] == "sustained"]
        if sus:
            tps = [r["completion"].get("predicted_tps") or 0 for r in sus]
            first, last = sum(tps[:5]) / 5, sum(tps[-5:]) / 5
            temps = [r.get("host_temp_c") for r in sus if r.get("host_temp_c")]
            freqs = [r.get("host_freq_mhz") for r in sus if r.get("host_freq_mhz")]
            line.append(
                f"sustained 30: decode first5 {first:.2f} last5 {last:.2f} tok/s "
                f"({(last / first - 1) * 100:+.0f} %), cpu {min(temps):.0f}-{max(temps):.0f} C, "
                f"freq {min(freqs):.0f}-{max(freqs):.0f} MHz"
            )
        peak = max((r.get("mem_peak") or 0 for r in recs), default=0)
        line.append(f"VmHWM peak {peak / 2**30:.2f} GiB")
        end = (meta.get("device_state_end") or {}).get("thermal") or {}
        line.append(f"end thermal_status {end.get('thermal_status')} skin {end.get('skin')}")
        print("\n  ".join(line))


def route_latency() -> None:
    section("Route call latency on the phone (B2 fc_core, uniform, 240 cases)")
    runs = [(m, "r2-phone", "chat") for m in MODELS]
    runs.append(("gemma4-e2b", "r2-phone-raw", "completion"))
    for model, run, endpoint in runs:
        recs = load(ROOT / f"{run}/B2/{model}/requests.jsonl")
        cs = [r["completion"] for r in recs]
        tot = [c["total_ms"] for c in cs if c.get("total_ms")]
        out = [c["predicted_n"] for c in cs if c.get("predicted_n") is not None]
        dec = [c["predicted_ms"] for c in cs if c.get("predicted_ms") is not None]
        print(
            f"{model} [{endpoint}] n={len(tot)} total p50 {fmt(q(tot, 0.5), 1000, 2)} s "
            f"p95 {fmt(q(tot, 0.95), 1000, 2)} s; output tokens p50 {q(out, 0.5)}; "
            f"decode p50 {fmt(q(dec, 0.5), 1000, 2)} s"
        )


def turns(run: str, batch: str, model: str) -> dict:
    """Per visitor turn: summed model-call time and number of calls."""
    recs = load(ROOT / f"{run}/{batch}/{model}/requests.jsonl")
    per_turn: dict[tuple, list[float]] = defaultdict(list)
    for r in recs:
        key = (r["arm"], r["tags"]["dialogue_id"], r["tags"]["turn_index"])
        per_turn[key].append(r["completion"].get("total_ms") or 0.0)
    out = defaultdict(lambda: {"ms": [], "calls": []})
    for (arm, _, _), ms in per_turn.items():
        out[arm]["ms"].append(sum(ms))
        out[arm]["calls"].append(sum(1 for m in ms if m > 0))
    dialogues = defaultdict(set)
    for r in recs:
        dialogues[r["arm"]].add(r["tags"]["dialogue_id"])
    return {arm: {**v, "dialogues": len(dialogues[arm])} for arm, v in out.items()}


def turn_latency() -> None:
    section("Per-turn latency (sum of model calls per visitor turn)")
    for run, batch, models in (
        ("r2-phone-raw", "B8", ("gemma4-e2b",)),  # no host-RAM cache (stopped at 19 dialogues)
        ("r2-phone-deploy", "B8", MODELS),  # deployment config: /completion + --cache-ram 512
        ("r2-laptop-v2", "B7", ("gemma4-e2b",)),
        ("r2-laptop-v2", "B8", ("gemma4-e2b",)),
    ):
        for model in models:
            for arm, v in sorted(turns(run, batch, model).items()):
                ms = v["ms"]
                share5 = sum(1 for x in ms if x <= 5000) / len(ms) * 100 if ms else 0
                print(
                    f"{run}/{batch} {model} {arm}: dialogues {v['dialogues']} turns {len(ms)} "
                    f"p50 {fmt(q(ms, 0.5), 1000, 2)} s p90 {fmt(q(ms, 0.9), 1000, 2)} s "
                    f"p95 {fmt(q(ms, 0.95), 1000, 2)} s "
                    f"max {fmt(max(ms, default=None), 1000, 1)} s; "
                    f"<=5 s {share5:.0f} %; calls/turn mean "
                    f"{sum(v['calls']) / max(1, len(v['calls'])):.2f}"
                )


def call_latency() -> None:
    section("Model-call latency by call type inside B8 on the phone")
    runs = [("r2-phone-raw", "gemma4-e2b")] + [("r2-phone-deploy", m) for m in MODELS]
    for run, model in runs:
        recs = load(ROOT / f"{run}/B8/{model}/requests.jsonl")
        by = defaultdict(list)
        for r in recs:
            if r["tags"]["kind"] == "llm" and r["completion"].get("total_ms"):
                by[r["call_type"]].append(r["completion"]["total_ms"])
        parts = [
            f"{ct} n={len(v)} p50 {fmt(q(v, 0.5), 1000, 2)} s p95 {fmt(q(v, 0.95), 1000, 2)} s"
            for ct, v in sorted(by.items())
        ]
        print(f"{run} {model}: " + ("; ".join(parts) if parts else "no data"))


def main() -> None:
    speed()
    route_latency()
    call_latency()
    turn_latency()


if __name__ == "__main__":
    main()
