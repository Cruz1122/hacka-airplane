"""Lifecycle of one llama-server container pinned to a hardware profile.

Exactly one benchmark container runs at a time (see plan: concurrent containers would
compete for cores, L3 and memory bandwidth and invalidate latency numbers).
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import Any

import httpx

from nevados_bench.config import HardwareProfile, ImageLock, ModelConfig, ServerConfig

CONTAINER_PORT = 8080
CONTAINER_MODELS_DIR = "/models"
# `POST /slots/0?action=erase` is rejected (501) unless --slot-save-path points to an
# existing directory; /tmp exists in the image and nothing is ever saved there.
CONTAINER_SLOT_DIR = "/tmp"
# Verbosity 4 adds the build line and chat-template init lines at ~15 lines/request.
# Verbosity 5 also logs the per-request chat handler ("using differential autoparser",
# ...) but logs grammar state per token, which perturbs latency: use it only in smoke runs.
DEFAULT_LOG_VERBOSITY = 4
HANDLER_LOG_VERBOSITY = 5

_BUILD_RE = re.compile(r"\bbuild (\d+) \(([0-9a-f]+)\)")
_THINKING_RE = re.compile(r"chat template, thinking = (\d+)")
_HANDLER_RE = re.compile(r"common_chat_templates_apply_jinja: using (.+?)\s*$", re.MULTILINE)


class ServerStartError(RuntimeError):
    """The server did not become healthy. `oom_killed` marks a result, not a harness bug."""

    def __init__(
        self,
        message: str,
        *,
        oom_killed: bool = False,
        exit_code: int | None = None,
        log_tail: str = "",
    ) -> None:
        super().__init__(f"{message}\n--- last log lines ---\n{log_tail}" if log_tail else message)
        self.oom_killed = oom_killed
        self.exit_code = exit_code
        self.log_tail = log_tail


@dataclass(frozen=True)
class ServerSpec:
    """Everything needed to build the `docker run` argv; pure data, easy to test."""

    model: ModelConfig
    gguf_filename: str
    profile_name: str
    profile: HardwareProfile
    server: ServerConfig
    models_dir: Path
    image_lock: ImageLock | None = None
    threads: int | None = None  # override profile threads (thread sweep)
    ctx_size: int | None = None  # override server ctx_size
    thinking: bool = False  # thinking arm requested
    host_port: int | None = None
    log_verbosity: int = DEFAULT_LOG_VERBOSITY
    extra_args: tuple[str, ...] = ()

    @property
    def container_name(self) -> str:
        return f"nevados-bench-{self.model.id}"

    @property
    def effective_threads(self) -> int:
        return self.threads if self.threads is not None else self.profile.threads

    @property
    def effective_ctx(self) -> int:
        return self.ctx_size if self.ctx_size is not None else self.server.ctx_size

    @property
    def effective_port(self) -> int:
        return self.host_port if self.host_port is not None else self.server.port

    @property
    def image_ref(self) -> str:
        return self.image_lock.ref if self.image_lock is not None else self.server.image

    @property
    def reasoning(self) -> str:
        if self.thinking:
            return "on"
        if self.model.thinking == "always":
            return "auto"  # no switch exists; let the template behave as shipped
        return self.server.reasoning

    def server_args(
        self,
        *,
        models_dir: str = CONTAINER_MODELS_DIR,
        slot_dir: str = CONTAINER_SLOT_DIR,
        host: str = "0.0.0.0",
        port: int = CONTAINER_PORT,
    ) -> list[str]:
        """llama-server flags. Defaults target the container; the phone runner overrides paths."""
        threads = str(self.effective_threads)
        return [
            "-m", f"{models_dir}/{self.gguf_filename}",
            "-c", str(self.effective_ctx),
            "-t", threads,
            "-tb", threads,
            "-np", str(self.server.parallel),
            "--cache-ram", str(self.server.cache_ram_mib),
            "-ctk", "f16",
            "-ctv", "f16",
            "--metrics",
            "--slot-save-path", slot_dir,
            "--host", host,
            "--port", str(port),
            "--reasoning", self.reasoning,
            "-lv", str(self.log_verbosity),
            *self.extra_args,
        ]  # fmt: skip

    def docker_argv(self) -> list[str]:
        mem = self.profile.memory
        return [
            "docker", "run", "-d",
            "--name", self.container_name,
            "--label", "nevados-bench=1",
            "--cpuset-cpus", self.profile.cpuset,
            "--memory", mem,
            "--memory-swap", mem,  # equal to --memory: no swap
            "-v", f"{self.models_dir.resolve()}:{CONTAINER_MODELS_DIR}:ro",
            "-p", f"127.0.0.1:{self.effective_port}:{CONTAINER_PORT}",
            self.image_ref,
            *self.server_args(),
        ]  # fmt: skip


def parse_startup_log(log: str) -> dict[str, Any]:
    build = _BUILD_RE.search(log)
    thinking = _THINKING_RE.search(log)
    return {
        "llama_build": f"b{build.group(1)}-{build.group(2)}" if build else None,
        "template_thinking": int(thinking.group(1)) if thinking else None,
        "chat_handlers": sorted(set(_HANDLER_RE.findall(log))),
    }


def _docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["docker", *args], capture_output=True, text=True, check=False)
    if check and proc.returncode != 0:
        raise RuntimeError(f"docker {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc


def _parse_docker_time(value: str) -> float | None:
    # Docker prints RFC 3339 with nanoseconds; Python parses at most microseconds.
    m = re.match(r"(.+?)(?:\.(\d+))?(Z|[+-]\d\d:\d\d)$", value)
    if not m:
        return None
    frac = (m.group(2) or "0")[:6].ljust(6, "0")
    tz = "+00:00" if m.group(3) == "Z" else m.group(3)
    try:
        return datetime.fromisoformat(f"{m.group(1)}.{frac}{tz}").timestamp()
    except ValueError:
        return None


@dataclass
class LlamaServer:
    """Context manager: start container, wait healthy, always stop + remove on exit."""

    spec: ServerSpec
    health_timeout_s: float = 300.0
    log_tail_lines: int = 40
    container_id: str | None = None
    pid: int | None = None
    load_ms: float | None = None
    startup_log: str = ""
    startup_info: dict[str, Any] = field(default_factory=dict)
    props: dict[str, Any] = field(default_factory=dict)
    exit_state: dict[str, Any] = field(default_factory=dict)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.spec.effective_port}"

    @property
    def llama_build(self) -> str | None:
        return self.props.get("build_info") or self.startup_info.get("llama_build")

    def __enter__(self) -> LlamaServer:
        try:
            self.start()
        except BaseException:
            self.stop()
            raise
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.stop()

    def start(self) -> None:
        name = self.spec.container_name
        _docker("rm", "-f", name, check=False)  # stale container from a crashed run
        t0_wall = time.time()
        t0 = time.monotonic()
        self.container_id = _docker(*self.spec.docker_argv()[1:]).stdout.strip()
        state = self.inspect_state()
        self.pid = state.get("Pid") or None
        started = _parse_docker_time(state.get("StartedAt", ""))
        self._wait_healthy(t0)
        healthy_wall = time.time()
        # Prefer the daemon's StartedAt (excludes `docker run` client/create overhead).
        if started is not None and t0_wall <= started <= healthy_wall:
            self.load_ms = (healthy_wall - started) * 1000.0
        else:
            self.load_ms = (time.monotonic() - t0) * 1000.0
        self.startup_log = self.logs()
        self.startup_info = parse_startup_log(self.startup_log)
        self.props = httpx.get(f"{self.base_url}/props", timeout=10.0).json()

    def _wait_healthy(self, t0: float) -> None:
        next_check = 0.0
        with httpx.Client(timeout=2.0) as http:
            while True:
                elapsed = time.monotonic() - t0
                if elapsed > self.health_timeout_s:
                    raise ServerStartError(
                        f"{self.spec.container_name}: not healthy after {self.health_timeout_s}s",
                        log_tail=self.logs(tail=self.log_tail_lines),
                    )
                try:
                    if http.get(f"{self.base_url}/health").status_code == 200:
                        return
                except httpx.TransportError:
                    pass
                if elapsed >= next_check:
                    next_check = elapsed + 1.0
                    state = self.inspect_state()
                    if state and not state.get("Running", False):
                        raise ServerStartError(
                            f"{self.spec.container_name} exited early "
                            f"(exit {state.get('ExitCode')}, oom_killed={state.get('OOMKilled')})",
                            oom_killed=bool(state.get("OOMKilled")),
                            exit_code=state.get("ExitCode"),
                            log_tail=self.logs(tail=self.log_tail_lines),
                        )
                time.sleep(0.05)

    def inspect_state(self) -> dict[str, Any]:
        ref = self.container_id or self.spec.container_name
        proc = _docker("inspect", "--format", "{{json .State}}", ref, check=False)
        if proc.returncode != 0:
            return {}
        return json.loads(proc.stdout)

    @property
    def oom_killed(self) -> bool:
        """True if the container was OOM-killed (checked live, or from the state at stop)."""
        state = self.exit_state or self.inspect_state()
        return bool(state.get("OOMKilled"))

    def is_running(self) -> bool:
        return bool(self.inspect_state().get("Running"))

    def logs(self, tail: int | None = None) -> str:
        ref = self.container_id or self.spec.container_name
        args = ["logs", *(["--tail", str(tail)] if tail else []), ref]
        proc = _docker(*args, check=False)
        return proc.stdout + proc.stderr  # llama-server logs to stderr

    def chat_handlers(self) -> list[str]:
        """Chat handlers llama.cpp chose so far; only logged at HANDLER_LOG_VERBOSITY."""
        return parse_startup_log(self.logs())["chat_handlers"]

    def stop(self) -> None:
        state = self.inspect_state()
        if state:
            self.exit_state = state
        _docker("rm", "-f", self.container_id or self.spec.container_name, check=False)
