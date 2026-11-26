"""Run llama-server on an Android phone over adb, with the same interface as LlamaServer.

The binary is a static NDK build of the same llama.cpp commit as the container image, pushed
with the GGUF files to PHONE_DIR (writable by the adb `shell` user, no root, no app). The
server is pinned to the big cores with `taskset` and reached through `adb forward`.

There is no cgroup on the phone: memory comes from /proc/<pid>/status (RSS, high-water mark),
CPU time from /proc/<pid>/stat, temperatures from the thermal HAL via `dumpsys`. Fields the
phone cannot provide (OOM events, CFS throttling, memory limit) stay None; they are never
guessed.
"""

from __future__ import annotations

import re
import shlex
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any

import httpx

from nevados_bench.runner.probe import CgroupSnapshot, EffectiveLimits
from nevados_bench.runner.server import ServerSpec, ServerStartError, parse_startup_log

PHONE_DIR = "/data/local/tmp/nevados"
PHONE_PORT = 8080
CLK_TCK = 100  # Android/Linux arm64 USER_HZ

Runner = Callable[..., subprocess.CompletedProcess[str]]


def cpu_mask(cpus: list[int]) -> str:
    """[4, 5, 6, 7] -> 'f0' (hex affinity mask for `taskset`)."""
    return format(sum(1 << c for c in cpus), "x")


class Adb:
    """Thin adb wrapper; `runner` is injectable so tests never touch a device."""

    def __init__(self, serial: str | None = None, runner: Runner = subprocess.run) -> None:
        self.serial = serial
        self.runner = runner

    def _base(self) -> list[str]:
        return ["adb", *(["-s", self.serial] if self.serial else [])]

    def run(self, *args: str, timeout: float = 60.0) -> subprocess.CompletedProcess[str]:
        return self.runner(
            [*self._base(), *args], capture_output=True, text=True, check=False, timeout=timeout
        )

    def shell(self, command: str, *, timeout: float = 60.0) -> subprocess.CompletedProcess[str]:
        return self.run("shell", command, timeout=timeout)


# ----------------------------------------------------------------------------- parsers


def parse_proc_status(text: str) -> dict[str, int]:
    """'VmRSS:   3680 kB' lines -> {'VmRSS': 3768320} in bytes."""
    out: dict[str, int] = {}
    for line in text.splitlines():
        m = re.match(r"(\w+):\s+(\d+)\s+kB", line)
        if m:
            out[m.group(1)] = int(m.group(2)) * 1024
    return out


def parse_proc_stat(text: str) -> dict[str, int]:
    """majflt, utime, stime from /proc/<pid>/stat (comm may contain spaces and parens)."""
    tail = text.rsplit(")", 1)[-1].split()
    # tail[0] is field 3 (state): field n is tail[n - 3].
    try:
        return {"majflt": int(tail[9]), "utime": int(tail[11]), "stime": int(tail[12])}
    except (IndexError, ValueError):
        return {}


_HAL_TEMP_RE = re.compile(r"Temperature\{mValue=([-\d.]+), mType=\d+, mName=(\w+)")


def parse_thermal(text: str) -> dict[str, Any]:
    """Live HAL temperatures (not the cached ones) and the throttling status from dumpsys."""
    out: dict[str, Any] = {}
    status = re.search(r"Thermal Status: (\d+)", text)
    if status:
        out["thermal_status"] = int(status.group(1))
    _, sep, live = text.partition("Current temperatures from HAL:")
    if sep:
        for value, name in _HAL_TEMP_RE.findall(live.split("Current cooling devices", 1)[0]):
            out.setdefault(name.lower(), float(value))
    return out


def parse_battery(text: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in ("level", "temperature", "voltage"):
        m = re.search(rf"^\s*{key}: (-?\d+)", text, re.MULTILINE)
        if m:
            out[key] = int(m.group(1))
    if "temperature" in out:
        out["temperature"] = out["temperature"] / 10.0  # tenths of a degree
    plugged = [
        kind for kind in ("AC", "USB", "Wireless") if re.search(rf"{kind} powered: true", text)
    ]
    out["powered"] = plugged
    return out


# ----------------------------------------------------------------------------- probes


class PhoneProbe:
    """Per-process memory and CPU snapshot; duck-types CgroupProbe for run_request."""

    def __init__(self, adb: Adb, pid: int | None, cpus: list[int]) -> None:
        self.adb = adb
        self.pid = pid
        self.cpus = cpus

    def snapshot(self) -> CgroupSnapshot:
        empty = CgroupSnapshot(None, None, None, None, None, None, None, None, None)
        if not self.pid:
            return empty
        proc = self.adb.shell(f"cat /proc/{self.pid}/status; echo @@; cat /proc/{self.pid}/stat")
        if proc.returncode != 0:
            return empty
        status_text, _, stat_text = proc.stdout.partition("@@")
        status = parse_proc_status(status_text)
        stat = parse_proc_stat(stat_text)
        cpu = (stat["utime"] + stat["stime"]) * 1_000_000 // CLK_TCK if "utime" in stat else None
        return CgroupSnapshot(
            memory_current=status.get("VmRSS"),
            memory_peak=status.get("VmHWM"),
            anon=status.get("RssAnon"),
            file=status.get("RssFile"),
            pgmajfault=stat.get("majflt"),
            oom=None,
            oom_kill=None,
            cpu_usage_usec=cpu,
            nr_throttled=None,
        )

    def effective_limits(self) -> EffectiveLimits:
        return EffectiveLimits(memory_max=None, memory_swap_max=None, cpus=self.cpus, cpu_max=None)


class PhoneHostProbe:
    """Mean frequency of the pinned cores and CPU temperature; one adb call per sample.

    run_request asks for frequency then temperature back to back, so a sample is reused
    for `max_age_s` to halve the adb round trips around each request.
    """

    def __init__(self, adb: Adb, cpus: list[int], *, max_age_s: float = 1.0) -> None:
        self.adb = adb
        self.cpus = cpus
        self.max_age_s = max_age_s
        self._sample: dict[str, Any] = {}
        self._at = -1e9

    def sample(self) -> dict[str, Any]:
        if time.monotonic() - self._at <= self.max_age_s:
            return self._sample
        freq_files = " ".join(
            f"/sys/devices/system/cpu/cpu{c}/cpufreq/scaling_cur_freq" for c in self.cpus
        )
        proc = self.adb.shell(f"cat {freq_files}; echo @@; dumpsys thermalservice")
        sample: dict[str, Any] = {}
        if proc.returncode == 0:
            freq_text, _, thermal_text = proc.stdout.partition("@@")
            khz = [int(v) for v in freq_text.split() if v.isdigit()]
            if khz:
                sample["freq_mhz"] = sum(khz) / len(khz) / 1000.0
            sample.update(parse_thermal(thermal_text))
        self._sample, self._at = sample, time.monotonic()
        return sample

    def freq_mhz(self) -> float | None:
        return self.sample().get("freq_mhz")

    def temp_c(self) -> float | None:
        return self.sample().get("cpu")


def device_state(adb: Adb) -> dict[str, Any]:
    """Battery and thermal state for meta.json (start and end of each launch)."""
    proc = adb.shell("dumpsys battery; echo @@; dumpsys thermalservice")
    if proc.returncode != 0:
        return {"error": proc.stderr.strip()[-200:]}
    battery_text, _, thermal_text = proc.stdout.partition("@@")
    return {"battery": parse_battery(battery_text), "thermal": parse_thermal(thermal_text)}


def device_info(adb: Adb) -> dict[str, Any]:
    props = {
        "soc": "ro.soc.model",
        "model": "ro.product.model",
        "android": "ro.build.version.release",
    }
    out: dict[str, Any] = {}
    for key, prop in props.items():
        proc = adb.shell(f"getprop {prop}")
        out[key] = proc.stdout.strip() if proc.returncode == 0 else None
    return out


# ----------------------------------------------------------------------------- server


@dataclass
class PhoneServer:
    """Context manager: start llama-server on the phone, wait healthy, always kill on exit."""

    spec: ServerSpec
    adb: Adb = field(default_factory=Adb)
    cpus: list[int] = field(default_factory=lambda: [4, 5, 6, 7])
    health_timeout_s: float = 300.0
    log_tail_lines: int = 40
    container_id: str | None = None  # LlamaServer compatibility; always None here
    pid: int | None = None
    load_ms: float | None = None
    startup_log: str = ""
    startup_info: dict[str, Any] = field(default_factory=dict)
    props: dict[str, Any] = field(default_factory=dict)
    oom_killed: bool | None = None  # Android's low-memory killer is not observable via adb

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.spec.effective_port}"

    @property
    def log_path(self) -> str:
        return f"{PHONE_DIR}/server-{self.spec.model.id}.log"

    @property
    def llama_build(self) -> str | None:
        return self.props.get("build_info") or self.startup_info.get("llama_build")

    def argv(self) -> list[str]:
        args = self.spec.server_args(
            models_dir=PHONE_DIR, slot_dir=PHONE_DIR, host="127.0.0.1", port=PHONE_PORT
        )
        return ["taskset", cpu_mask(self.cpus), f"{PHONE_DIR}/llama-server", *args]

    def __enter__(self) -> PhoneServer:
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
        gguf = f"{PHONE_DIR}/{self.spec.gguf_filename}"
        if self.adb.shell(f"test -f {shlex.quote(gguf)}").returncode != 0:
            raise ServerStartError(f"{gguf} is not on the phone; adb push it first")
        self.adb.shell("pkill -f nevados/llama-server")  # stale server from a crashed run
        port = self.spec.effective_port
        forward = self.adb.run("forward", f"tcp:{port}", f"tcp:{PHONE_PORT}")
        if forward.returncode != 0:
            raise ServerStartError(f"adb forward failed: {forward.stderr.strip()}")
        t0 = time.monotonic()
        launch = (
            f"setsid nohup {shlex.join(self.argv())} > {self.log_path} 2>&1 < /dev/null & echo $!"
        )
        proc = self.adb.shell(launch)
        try:
            self.pid = int(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError) as exc:
            raise ServerStartError(f"could not read server pid: {proc.stdout!r}") from exc
        self._wait_healthy(t0)
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
                        f"phone server not healthy after {self.health_timeout_s}s",
                        log_tail=self.logs(tail=self.log_tail_lines),
                    )
                try:
                    if http.get(f"{self.base_url}/health").status_code == 200:
                        return
                except httpx.TransportError:
                    pass
                if elapsed >= next_check:
                    next_check = elapsed + 1.0
                    if not self.is_running():
                        raise ServerStartError(
                            "phone server exited early",
                            log_tail=self.logs(tail=self.log_tail_lines),
                        )
                time.sleep(0.1)

    def is_running(self) -> bool:
        return bool(self.pid) and self.adb.shell(f"kill -0 {self.pid}").returncode == 0

    def logs(self, tail: int | None = None) -> str:
        cmd = f"tail -n {tail} {self.log_path}" if tail else f"cat {self.log_path}"
        return self.adb.shell(cmd).stdout

    def chat_handlers(self) -> list[str]:
        return parse_startup_log(self.logs())["chat_handlers"]

    def stop(self) -> None:
        if self.pid:
            self.adb.shell(f"kill {self.pid}")
            for _ in range(50):
                if not self.is_running():
                    break
                time.sleep(0.1)
            else:
                self.adb.shell(f"kill -9 {self.pid}")
        self.adb.run("forward", "--remove", f"tcp:{self.spec.effective_port}")
