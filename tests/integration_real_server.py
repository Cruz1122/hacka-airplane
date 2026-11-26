"""Real llama-server integration check (needs Docker, the pulled image and granite4-350m).

Not collected by pytest (file name does not match test_*.py). Run:

    uv run python tests/integration_real_server.py

Downloads granite4-350m (~237 MB) only if missing. Exits non-zero on any failed check.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

import jsonschema

from nevados_bench.config import MODELS_DIR, get_model, load_profiles
from nevados_bench.runner.client import LlamaClient
from nevados_bench.runner.fetch import lock_image, resolve_and_download
from nevados_bench.runner.measure import run_request
from nevados_bench.runner.probe import CgroupProbe, HostProbe, parse_cpuset
from nevados_bench.runner.server import LlamaServer, ServerSpec
from nevados_bench.runner.speed import run_speed_protocol
from nevados_bench.schemas import PromptRequest

MODEL_ID = "granite4-350m"
PROFILE = "phone-tight"
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}
ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string", "enum": ["get_weather", "none", "clarify"]},
        "args": {"type": "object", "properties": {"city": {"type": "string"}}},
    },
    "required": ["tool", "args"],
}

failures: list[str] = []


def check(ok: bool, label: str, detail: Any = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {label} {detail}")
    if not ok:
        failures.append(label)


def mem_bytes(spec: str) -> int:
    units = {"k": 1024, "m": 1024**2, "g": 1024**3}
    return int(spec[:-1]) * units[spec[-1].lower()]


def main() -> int:
    cfg = load_profiles()
    profile = cfg.profiles[PROFILE]
    image = lock_image(cfg.server.image)
    print(f"image {image.ref} version={image.version}")
    model = get_model(MODEL_ID)
    lock = resolve_and_download(model, MODELS_DIR)
    print(f"model {lock.filename} sha256={lock.sha256[:12]}")
    spec = ServerSpec(
        model=model,
        gguf_filename=lock.filename,
        profile_name=PROFILE,
        profile=profile,
        server=cfg.server,
        models_dir=MODELS_DIR,
        image_lock=image,
    )
    print(" ".join(spec.docker_argv()))
    template = {
        "run_id": "integration",
        "batch": "B0",
        "suite": "integration",
        "case_id": "x",
        "model_id": model.id,
        "gguf_file": lock.filename,
        "gguf_sha256": lock.sha256,
        "quant": model.quant,
        "image_digest": image.digest,
        "profile": PROFILE,
        "threads": profile.threads,
        "ctx_size": spec.effective_ctx,
    }
    with LlamaServer(spec) as server, LlamaClient(server.base_url, timeout_s=120) as client:
        assert server.container_id
        print(f"load_ms={server.load_ms:.0f} build={server.llama_build} info={server.startup_info}")
        template["llama_build"] = server.llama_build
        probe = CgroupProbe.for_container(server.container_id, pid=server.pid)
        print(f"cgroup {probe.cgroup_dir}")
        lim = probe.effective_limits()
        check(lim.memory_max == mem_bytes(profile.memory), "memory.max", lim.memory_max)
        check(lim.memory_swap_max == 0, "memory.swap.max", lim.memory_swap_max)
        check(lim.cpus == parse_cpuset(profile.cpuset), "cpuset.cpus.effective", lim.cpus)
        check((lim.cpu_max or "").startswith("max"), "no CFS quota", lim.cpu_max)
        host = HostProbe(parse_cpuset(profile.cpuset))
        print(f"host freq={host.freq_mhz()} MHz temp={host.temp_c()} C")

        msgs = [{"role": "user", "content": "Describe el páramo andino en dos frases."}]
        client.erase_slot()
        cold = run_request(
            client,
            probe,
            host,
            PromptRequest(messages=msgs, max_tokens=32, cache_prompt=False),
            {**template, "case_id": "cold", "arm": "cold"},
        )
        warm = run_request(
            client,
            probe,
            host,
            PromptRequest(messages=msgs, max_tokens=32, cache_prompt=True),
            {**template, "case_id": "cold", "arm": "warm"},
        )
        for r in (cold, warm):
            c = r.completion
            print(
                f"{r.arm}: cache_n={c.cache_n} prompt_n={c.prompt_n} prompt_ms={c.prompt_ms} "
                f"ttft={c.ttft_ms:.1f} total={c.total_ms:.1f} predicted_n={c.predicted_n} "
                f"tps={c.predicted_tps} overhead={r.overhead_ms} mem_cur={r.mem_current} "
                f"peak={r.mem_peak} cpu_us={r.cpu_usage_usec_delta} freq={r.host_freq_mhz} "
                f"temp={r.host_temp_c}"
            )
        cc = cold.completion
        check(cc.cache_n == 0, "cold cache_n == 0", cc.cache_n)
        check((warm.completion.cache_n or 0) > 0, "warm cache_n > 0", warm.completion.cache_n)
        templated = client.count_prompt_tokens(msgs)
        check(
            abs(templated - (cold.prompt_tokens_total or 0)) <= 2,
            "apply-template+tokenize ~ prompt tokens",
            f"{templated} vs {cold.prompt_tokens_total}",
        )
        # TTFT must include prefill and stay within a modest client/HTTP overhead of it.
        ttft_gap = (cc.ttft_ms or 0) - (cc.prompt_ms or 0)
        check(0 <= ttft_gap < 150, "ttft_ms consistent with prompt_ms", f"gap={ttft_gap:.1f} ms")

        # tool_choice=auto depends on model quality (granite-350m at temperature 0 often
        # answers in prose), so it is informational; "required" makes llama.cpp constrain
        # the output to a call and deterministically exercises the parse path.
        for choice in ("auto", "required"):
            tool = client.complete(
                PromptRequest(
                    messages=[{"role": "user", "content": "What is the weather in Paris?"}],
                    tools=[WEATHER_TOOL],
                    tool_choice=choice,  # type: ignore[arg-type]
                    max_tokens=64,
                )
            )
            print(
                f"tool[{choice}]: {tool.tool_calls} finish={tool.finish_reason} "
                f"content={tool.content[:80]!r} err={tool.http_error}"
            )
        ok = bool(tool.tool_calls) and tool.tool_calls[0]["name"] == "get_weather"
        if ok:
            args = json.loads(tool.tool_calls[0]["arguments"])
            ok = isinstance(args, dict) and "city" in args
        check(ok, "native tool call parsed", tool.finish_reason)

        js = client.complete(
            PromptRequest(
                messages=[{"role": "user", "content": "Route: what is the weather in Paris?"}],
                json_schema=ROUTE_SCHEMA,
                tool_choice="none",
                max_tokens=64,
            )
        )
        print(f"json_schema: {js.content!r} err={js.http_error}")
        try:
            jsonschema.validate(json.loads(js.content), ROUTE_SCHEMA)
            check(True, "json_schema output valid")
        except (json.JSONDecodeError, jsonschema.ValidationError) as exc:
            check(False, "json_schema output valid", exc)

        speed = run_speed_protocol(
            client,
            probe,
            host,
            lambda i: "El páramo es un ecosistema de alta montaña con frailejones. " * 60,
            template,
            threads=profile.threads,
            levels=("0.5k",),
            output_lengths=(16,),
            reps=1,
            sustained_n=2,
        )
        for r in speed:
            c = r.completion
            print(
                f"speed {r.case_id} {r.arm}: cache_n={c.cache_n} prompt_n={c.prompt_n} "
                f"predicted_n={c.predicted_n} ttft={c.ttft_ms:.1f} prompt_tps={c.prompt_tps} "
                f"decode_tps={c.predicted_tps} tags={r.tags}"
            )
        dec = [r for r in speed if r.arm == "decode"]
        check(
            all(r.completion.predicted_n == 16 for r in dec),
            "ignore_eos forces length",
            [r.completion.predicted_n for r in dec],
        )
        check(not server.oom_killed, "not oom_killed")
        name = spec.container_name

    gone = subprocess.run(["docker", "inspect", name], capture_output=True).returncode != 0
    check(gone, "container removed after exit", name)
    print("FAILED: " + ", ".join(failures) if failures else "ALL PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
