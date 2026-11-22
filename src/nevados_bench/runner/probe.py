"""Read-only cgroup v2 and host probes. Missing or unreadable files yield None, never raise."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

CGROUP_ROOT = Path("/sys/fs/cgroup")
SYS_ROOT = Path("/sys")
PROC_ROOT = Path("/proc")


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except OSError:
        return None


def _read_int(path: Path) -> int | None:
    text = _read(path)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _read_kv(path: Path) -> dict[str, int]:
    """Parse flat-keyed cgroup files (memory.stat, memory.events, cpu.stat)."""
    text = _read(path)
    out: dict[str, int] = {}
    for line in (text or "").splitlines():
        parts = line.split()
        if len(parts) == 2:
            try:
                out[parts[0]] = int(parts[1])
            except ValueError:
                continue
    return out


def parse_cpuset(spec: str) -> list[int]:
    """'0-2,5' -> [0, 1, 2, 5]."""
    cpus: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            cpus.extend(range(int(lo), int(hi) + 1))
        else:
            cpus.append(int(part))
    return cpus


@dataclass(frozen=True)
class CgroupSnapshot:
    memory_current: int | None
    memory_peak: int | None
    anon: int | None
    file: int | None
    pgmajfault: int | None
    oom: int | None
    oom_kill: int | None
    cpu_usage_usec: int | None
    nr_throttled: int | None


@dataclass(frozen=True)
class EffectiveLimits:
    memory_max: int | None  # None also when the file says "max" (unlimited)
    memory_swap_max: int | None
    cpus: list[int] | None
    cpu_max: str | None  # "max 100000" means no CFS quota


def find_container_cgroup(
    container_id: str,
    *,
    pid: int | None = None,
    cgroup_root: Path = CGROUP_ROOT,
    proc_root: Path = PROC_ROOT,
) -> Path | None:
    """Locate the container's cgroup dir: /proc/<pid>/cgroup, known layouts, then a search."""
    if pid:
        text = _read(proc_root / str(pid) / "cgroup")
        for line in (text or "").splitlines():
            if line.startswith("0::"):
                candidate = cgroup_root / line[3:].lstrip("/")
                if candidate.is_dir():
                    return candidate
    for candidate in (
        cgroup_root / "system.slice" / f"docker-{container_id}.scope",  # systemd driver
        cgroup_root / "docker" / container_id,  # cgroupfs driver
    ):
        if candidate.is_dir():
            return candidate
    try:
        for candidate in cgroup_root.rglob(f"*{container_id}*"):
            if candidate.is_dir() and (candidate / "memory.current").exists():
                return candidate
    except OSError:
        return None
    return None


class CgroupProbe:
    def __init__(self, cgroup_dir: Path | None) -> None:
        self.cgroup_dir = cgroup_dir

    @classmethod
    def for_container(
        cls, container_id: str, *, pid: int | None = None, cgroup_root: Path = CGROUP_ROOT
    ) -> CgroupProbe:
        return cls(find_container_cgroup(container_id, pid=pid, cgroup_root=cgroup_root))

    def _path(self, name: str) -> Path:
        assert self.cgroup_dir is not None
        return self.cgroup_dir / name

    def snapshot(self) -> CgroupSnapshot:
        if self.cgroup_dir is None:
            return CgroupSnapshot(None, None, None, None, None, None, None, None, None)
        stat = _read_kv(self._path("memory.stat"))
        events = _read_kv(self._path("memory.events"))
        cpu = _read_kv(self._path("cpu.stat"))
        return CgroupSnapshot(
            memory_current=_read_int(self._path("memory.current")),
            memory_peak=_read_int(self._path("memory.peak")),
            anon=stat.get("anon"),
            file=stat.get("file"),
            pgmajfault=stat.get("pgmajfault"),
            oom=events.get("oom"),
            oom_kill=events.get("oom_kill"),
            cpu_usage_usec=cpu.get("usage_usec"),
            nr_throttled=cpu.get("nr_throttled"),
        )

    def effective_limits(self) -> EffectiveLimits:
        if self.cgroup_dir is None:
            return EffectiveLimits(None, None, None, None)
        cpus = _read(self._path("cpuset.cpus.effective"))
        try:
            cpu_list = parse_cpuset(cpus) if cpus else None
        except ValueError:
            cpu_list = None
        return EffectiveLimits(
            memory_max=_read_int(self._path("memory.max")),
            memory_swap_max=_read_int(self._path("memory.swap.max")),
            cpus=cpu_list,
            cpu_max=_read(self._path("cpu.max")),
        )


class HostProbe:
    """Mean current frequency of the profile's CPUs and package temperature."""

    def __init__(self, cpus: list[int], *, sys_root: Path = SYS_ROOT) -> None:
        self.cpus = cpus
        self.sys_root = sys_root

    def freq_mhz(self) -> float | None:
        values = [
            _read_int(self.sys_root / f"devices/system/cpu/cpu{n}/cpufreq/scaling_cur_freq")
            for n in self.cpus
        ]
        khz = [v for v in values if v is not None]
        return sum(khz) / len(khz) / 1000.0 if khz else None

    def temp_c(self) -> float | None:
        hwmon = self.sys_root / "class/hwmon"
        try:
            hwmons = sorted(hwmon.iterdir()) if hwmon.is_dir() else []
        except OSError:
            hwmons = []
        for dev in hwmons:
            if _read(dev / "name") not in ("coretemp", "k10temp", "zenpower"):
                continue
            # Prefer the input labelled as package (Intel) or Tctl (AMD); else temp1.
            chosen = dev / "temp1_input"
            for label in sorted(dev.glob("temp*_label")):
                text = (_read(label) or "").lower()
                if text.startswith(("package", "tctl")):
                    chosen = label.with_name(label.name.replace("_label", "_input"))
                    break
            milli = _read_int(chosen)
            if milli is not None:
                return milli / 1000.0
        thermal = self.sys_root / "class/thermal"
        try:
            zones = sorted(thermal.glob("thermal_zone*")) if thermal.is_dir() else []
        except OSError:
            zones = []
        for zone in zones:
            if _read(zone / "type") == "x86_pkg_temp":
                milli = _read_int(zone / "temp")
                if milli is not None:
                    return milli / 1000.0
        return None
