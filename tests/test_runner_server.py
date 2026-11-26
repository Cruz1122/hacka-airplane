from __future__ import annotations

from pathlib import Path

from nevados_bench.config import ImageLock, get_model, load_profiles
from nevados_bench.runner.server import ServerSpec, _parse_docker_time, parse_startup_log

LOCK = ImageLock(image="ghcr.io/x:server", ref="ghcr.io/x@sha256:abc", digest="sha256:abc")


def spec(profile: str, **kw: object) -> ServerSpec:
    cfg = load_profiles()
    return ServerSpec(
        model=kw.pop("model", get_model("granite4-350m")),  # type: ignore[arg-type]
        gguf_filename="g.gguf",
        profile_name=profile,
        profile=cfg.profiles[profile],
        server=cfg.server,
        models_dir=Path("/data/models"),
        **kw,  # type: ignore[arg-type]
    )


def flag(argv: list[str], name: str) -> str:
    return argv[argv.index(name) + 1]


def test_phone_tight_argv() -> None:
    s = spec("phone-tight", image_lock=LOCK)
    argv = s.docker_argv()
    assert argv[:3] == ["docker", "run", "-d"]
    assert flag(argv, "--name") == "nevados-bench-granite4-350m"
    assert flag(argv, "--cpuset-cpus") == "0-2"
    assert flag(argv, "--memory") == "4g" and flag(argv, "--memory-swap") == "4g"
    assert flag(argv, "-v") == "/data/models:/models:ro"
    assert flag(argv, "-p") == "127.0.0.1:8080:8080"
    image_at = argv.index("ghcr.io/x@sha256:abc")
    server = argv[image_at + 1 :]
    assert flag(server, "-m") == "/models/g.gguf"
    assert flag(server, "-c") == "12288"
    assert flag(server, "-t") == "3" and flag(server, "-tb") == "3"
    assert flag(server, "-np") == "1" and flag(server, "--cache-ram") == "0"
    assert flag(server, "--host") == "0.0.0.0" and flag(server, "--reasoning") == "off"
    assert "--metrics" in server and flag(server, "--slot-save-path") == "/tmp"
    assert "--cpus" not in argv and "--cpu-quota" not in argv  # no CFS quota


def test_phone_nominal_overrides_and_unpinned_image() -> None:
    s = spec("phone-nominal", threads=1, ctx_size=4096, host_port=18080)
    argv = s.docker_argv()
    assert flag(argv, "--cpuset-cpus") == "0-3"
    assert flag(argv, "--memory") == "5g" and flag(argv, "--memory-swap") == "5g"
    assert flag(argv, "-p") == "127.0.0.1:18080:8080"
    assert "ghcr.io/ggml-org/llama.cpp:server" in argv
    assert flag(argv, "-t") == "1" and flag(argv, "-tb") == "1" and flag(argv, "-c") == "4096"


def test_reasoning_modes() -> None:
    assert spec("phone-tight", thinking=True).reasoning == "on"
    assert spec("phone-tight", model=get_model("lfm2.5-2.6b")).reasoning == "auto"
    assert spec("phone-tight", model=get_model("qwen3-0.6b")).reasoning == "off"


def test_parse_startup_log() -> None:
    log = (
        "0.00.021 I cmn  common_param: common_params_print_info: build 12375 (9d25e0014) "
        "with GNU 15.2.0 for Linux x86_64\n"
        "0.00.558 I srv          init: init: chat template, thinking = 0\n"
        "0.01.172 D common_chat_templates_apply_jinja: using differential autoparser\n"
        "0.02.172 D common_chat_templates_apply_jinja: using differential autoparser\n"
    )
    info = parse_startup_log(log)
    assert info == {
        "llama_build": "b12375-9d25e0014",
        "template_thinking": 0,
        "chat_handlers": ["differential autoparser"],
    }
    assert parse_startup_log("")["llama_build"] is None


def test_parse_docker_time() -> None:
    t = _parse_docker_time("2026-11-14T22:01:02.123456789Z")
    assert t is not None and abs(t % 60 - 2.123456) < 1e-5
    assert _parse_docker_time("garbage") is None
