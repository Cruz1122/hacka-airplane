from __future__ import annotations

import dataclasses
import subprocess
from pathlib import Path

from nevados_bench.config import get_model, load_profiles
from nevados_bench.runner.phone import (
    PHONE_DIR,
    Adb,
    PhoneHostProbe,
    PhoneProbe,
    PhoneServer,
    cpu_mask,
    parse_battery,
    parse_proc_stat,
    parse_proc_status,
    parse_thermal,
)
from nevados_bench.runner.server import ServerSpec

THERMAL = """\
Thermal Status: 1
Cached temperatures:
\tTemperature{mValue=67.07, mType=0, mName=CPU, mStatus=0}
HAL Ready: true
Current temperatures from HAL:
\tTemperature{mValue=47.206, mType=0, mName=CPU, mStatus=0}
\tTemperature{mValue=35.9, mType=2, mName=BATTERY, mStatus=0}
\tTemperature{mValue=38.869, mType=3, mName=SKIN, mStatus=0}
Current cooling devices from HAL:
\tCoolingDevice{mValue=0, mType=2, mName=CPU0}
"""

BATTERY = """\
Current Battery Service state:
  AC powered: false
  USB powered: true
  Wireless powered: false
  level: 79
  voltage: 4169
  temperature: 359
"""


class FakeAdb:
    """Records argv and answers from a table of (substring -> stdout, returncode)."""

    def __init__(self, answers: dict[str, tuple[str, int]]) -> None:
        self.answers = answers
        self.calls: list[list[str]] = []

    def __call__(self, argv: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        self.calls.append(argv)
        joined = " ".join(argv)
        for needle, (out, rc) in self.answers.items():
            if needle in joined:
                return subprocess.CompletedProcess(argv, rc, out, "")
        return subprocess.CompletedProcess(argv, 0, "", "")


def phone_spec() -> ServerSpec:
    cfg = load_profiles()
    return ServerSpec(
        model=get_model("gemma4-e2b"),
        gguf_filename="g.gguf",
        profile_name="phone-device",
        profile=cfg.profiles["phone-device"],
        server=cfg.server,
        models_dir=Path("/unused"),
        ctx_size=4096,
    )


def test_cpu_mask_big_cores() -> None:
    assert cpu_mask([4, 5, 6, 7]) == "f0"
    assert cpu_mask([0, 1, 2]) == "7"


def test_parse_proc_status_bytes() -> None:
    out = parse_proc_status("VmHWM:\t    3680 kB\nVmRSS:\t 2048 kB\nName:\tllama\n")
    assert out == {"VmHWM": 3680 * 1024, "VmRSS": 2048 * 1024}


def test_parse_proc_stat_comm_with_spaces_and_parens() -> None:
    # pid (comm) state ppid pgrp session tty tpgid flags minflt cminflt majflt cmajflt utime stime
    text = "123 (llama (x) srv) S 1 2 3 4 5 6 70 8 9 10 250 50 0 0"
    assert parse_proc_stat(text) == {"majflt": 9, "utime": 250, "stime": 50}
    assert parse_proc_stat("garbage") == {}


def test_parse_thermal_uses_live_hal_values_not_cache() -> None:
    out = parse_thermal(THERMAL)
    assert out == {"thermal_status": 1, "cpu": 47.206, "battery": 35.9, "skin": 38.869}


def test_parse_battery() -> None:
    out = parse_battery(BATTERY)
    assert out["level"] == 79 and out["temperature"] == 35.9 and out["powered"] == ["USB"]


def test_phone_probe_snapshot_maps_proc_fields() -> None:
    status = "VmHWM:\t 3000000 kB\nVmRSS:\t 2900000 kB\nRssAnon:\t 100 kB\nRssFile:\t 200 kB\n"
    stat = "77 (llama-server) S 1 2 3 4 5 6 70 8 12 10 300 100 0 0"
    fake = FakeAdb({"/proc/77/status": (f"{status}@@\n{stat}", 0)})
    snap = PhoneProbe(Adb(runner=fake), 77, [4, 5, 6, 7]).snapshot()
    assert snap.memory_peak == 3000000 * 1024
    assert snap.memory_current == 2900000 * 1024
    assert snap.anon == 100 * 1024 and snap.file == 200 * 1024
    assert snap.pgmajfault == 12
    assert snap.cpu_usage_usec == 400 * 10_000  # (utime + stime) ticks at 100 Hz
    assert snap.oom_kill is None and snap.nr_throttled is None  # not observable: not guessed


def test_phone_probe_without_pid_or_on_failure_is_empty() -> None:
    assert PhoneProbe(Adb(runner=FakeAdb({})), None, []).snapshot().memory_peak is None
    failing = FakeAdb({"/proc/": ("", 1)})
    assert PhoneProbe(Adb(runner=failing), 5, []).snapshot().memory_peak is None


def test_host_probe_one_adb_call_for_freq_and_temp() -> None:
    fake = FakeAdb({"scaling_cur_freq": (f"2500000\n2000000\n@@\n{THERMAL}", 0)})
    probe = PhoneHostProbe(Adb(runner=fake), [4, 5])
    assert probe.freq_mhz() == 2250.0
    assert probe.temp_c() == 47.206
    assert len(fake.calls) == 1


def test_phone_server_argv_pins_big_cores_and_phone_paths() -> None:
    server = PhoneServer(phone_spec(), adb=Adb(runner=FakeAdb({})), cpus=[4, 5, 6, 7])
    argv = server.argv()
    assert argv[:3] == ["taskset", "f0", f"{PHONE_DIR}/llama-server"]
    assert argv[argv.index("-m") + 1] == f"{PHONE_DIR}/g.gguf"
    assert argv[argv.index("-c") + 1] == "4096"
    assert argv[argv.index("-t") + 1] == "4"
    assert argv[argv.index("--host") + 1] == "127.0.0.1"
    assert argv[argv.index("--slot-save-path") + 1] == PHONE_DIR


def test_phone_server_missing_gguf_fails_before_launch() -> None:
    fake = FakeAdb({"test -f": ("", 1)})
    server = PhoneServer(phone_spec(), adb=Adb(runner=fake))
    try:
        server.start()
    except Exception as exc:  # ServerStartError
        assert "not on the phone" in str(exc)
    else:
        raise AssertionError("expected ServerStartError")
    assert not any("setsid" in " ".join(c) for c in fake.calls)


def test_container_server_args_unchanged_by_default() -> None:
    argv = phone_spec().server_args()
    assert argv[argv.index("-m") + 1] == "/models/g.gguf"
    assert argv[argv.index("--host") + 1] == "0.0.0.0"
    assert argv[argv.index("--port") + 1] == "8080"


def test_phone_server_argv_carries_cache_ram_override() -> None:
    spec = phone_spec()
    spec = dataclasses.replace(spec, server=spec.server.model_copy(update={"cache_ram_mib": 512}))
    argv = PhoneServer(spec, adb=Adb(runner=FakeAdb({})), cpus=[4, 5, 6, 7]).argv()
    assert argv[argv.index("--cache-ram") + 1] == "512"
