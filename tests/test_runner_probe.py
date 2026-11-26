from __future__ import annotations

from pathlib import Path

from nevados_bench.runner.probe import (
    CgroupProbe,
    HostProbe,
    find_container_cgroup,
    parse_cpuset,
)

CID = "abc123"


def make_cgroup(root: Path) -> Path:
    d = root / "system.slice" / f"docker-{CID}.scope"
    d.mkdir(parents=True)
    (d / "memory.current").write_text("1000\n")
    (d / "memory.peak").write_text("2000\n")
    (d / "memory.stat").write_text("anon 300\nfile 700\npgmajfault 5\nbogus x\n")
    (d / "memory.events").write_text("low 0\nhigh 0\nmax 1\noom 2\noom_kill 1\n")
    (d / "cpu.stat").write_text("usage_usec 123456\nnr_periods 0\nnr_throttled 0\n")
    (d / "memory.max").write_text("4294967296\n")
    (d / "memory.swap.max").write_text("0\n")
    (d / "cpuset.cpus.effective").write_text("0-2\n")
    (d / "cpu.max").write_text("max 100000\n")
    return d


def test_parse_cpuset() -> None:
    assert parse_cpuset("0-2,5") == [0, 1, 2, 5]
    assert parse_cpuset("3") == [3]


def test_snapshot_and_limits(tmp_path: Path) -> None:
    make_cgroup(tmp_path)
    probe = CgroupProbe.for_container(CID, cgroup_root=tmp_path)
    s = probe.snapshot()
    assert (s.memory_current, s.memory_peak, s.anon, s.file, s.pgmajfault) == (
        1000,
        2000,
        300,
        700,
        5,
    )
    assert (s.oom, s.oom_kill, s.cpu_usage_usec, s.nr_throttled) == (2, 1, 123456, 0)
    lim = probe.effective_limits()
    assert lim.memory_max == 4 * 1024**3
    assert lim.memory_swap_max == 0
    assert lim.cpus == [0, 1, 2]
    assert lim.cpu_max == "max 100000"


def test_missing_files_yield_none(tmp_path: Path) -> None:
    d = make_cgroup(tmp_path)
    (d / "memory.peak").unlink()
    (d / "memory.stat").unlink()
    (d / "memory.max").write_text("max\n")
    probe = CgroupProbe(d)
    s = probe.snapshot()
    assert s.memory_peak is None and s.anon is None and s.memory_current == 1000
    assert probe.effective_limits().memory_max is None
    empty = CgroupProbe(None)
    assert empty.snapshot().memory_current is None
    assert empty.effective_limits().cpus is None


def test_discovery_via_proc_and_fallback(tmp_path: Path) -> None:
    cg = tmp_path / "cg"
    nested = cg / "custom" / f"x-{CID}"
    nested.mkdir(parents=True)
    (nested / "memory.current").write_text("1\n")
    proc = tmp_path / "proc" / "42"
    proc.mkdir(parents=True)
    (proc / "cgroup").write_text(f"0::/custom/x-{CID}\n")
    assert find_container_cgroup(CID, pid=42, cgroup_root=cg, proc_root=tmp_path / "proc") == nested
    assert find_container_cgroup(CID, cgroup_root=cg) == nested  # rglob fallback
    assert find_container_cgroup("nope", cgroup_root=cg) is None


def test_host_probe(tmp_path: Path) -> None:
    for n, khz in ((0, 1000000), (1, 3000000)):
        f = tmp_path / f"devices/system/cpu/cpu{n}/cpufreq/scaling_cur_freq"
        f.parent.mkdir(parents=True)
        f.write_text(f"{khz}\n")
    hw = tmp_path / "class/hwmon/hwmon3"
    hw.mkdir(parents=True)
    (hw / "name").write_text("coretemp\n")
    (hw / "temp1_label").write_text("Core 0\n")
    (hw / "temp1_input").write_text("40000\n")
    (hw / "temp2_label").write_text("Package id 0\n")
    (hw / "temp2_input").write_text("55500\n")
    probe = HostProbe([0, 1, 2], sys_root=tmp_path)  # cpu2 missing -> ignored
    assert probe.freq_mhz() == 2000.0
    assert probe.temp_c() == 55.5


def test_host_probe_thermal_zone_and_missing(tmp_path: Path) -> None:
    assert HostProbe([0], sys_root=tmp_path).freq_mhz() is None
    assert HostProbe([0], sys_root=tmp_path).temp_c() is None
    z = tmp_path / "class/thermal/thermal_zone1"
    z.mkdir(parents=True)
    (z / "type").write_text("x86_pkg_temp\n")
    (z / "temp").write_text("61000\n")
    assert HostProbe([0], sys_root=tmp_path).temp_c() == 61.0
