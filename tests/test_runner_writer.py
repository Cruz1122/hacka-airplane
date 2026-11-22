from __future__ import annotations

from pathlib import Path

import pytest

from nevados_bench.runner.writer import RecordWriter, done_keys
from nevados_bench.schemas import Completion, RequestRecord


def rec(
    case_id: str, rep: int = 0, arm: str = "default", fc_mode: str | None = None
) -> RequestRecord:
    return RequestRecord(
        run_id="r",
        batch="B0",
        suite="s",
        case_id=case_id,
        rep=rep,
        arm=arm,
        model_id="m",
        gguf_file="m.gguf",
        quant="Q4_K_M",
        profile="phone-tight",
        threads=3,
        ctx_size=12288,
        fc_mode=fc_mode,  # type: ignore[arg-type]
        ts="2026-11-14T00:00:00+00:00",
        completion=Completion(content="x"),
    )


def test_append_and_done_keys(tmp_path: Path) -> None:
    path = tmp_path / "a" / "requests.jsonl"
    with RecordWriter(path) as w:
        w.append(rec("c1"))
        w.append(rec("c1", rep=1, arm="warm", fc_mode="native"))
    assert done_keys(path) == {("c1", 0, "default", None), ("c1", 1, "warm", "native")}
    assert len(path.read_text().splitlines()) == 2


def test_truncated_last_line_tolerated_and_repaired(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    with RecordWriter(path) as w:
        w.append(rec("c1"))
    full = rec("c2").model_dump_json()
    with path.open("a") as fh:
        fh.write(full[: len(full) // 2])  # crash mid-write
    assert done_keys(path) == {("c1", 0, "default", None)}
    with RecordWriter(path) as w:
        w.append(rec("c2"))
    assert done_keys(path) == {("c1", 0, "default", None), ("c2", 0, "default", None)}
    assert len(path.read_text().splitlines()) == 2


def test_truncated_only_line(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    path.write_text('{"case_id": "c')
    assert done_keys(path) == set()
    with RecordWriter(path) as w:
        w.append(rec("c1"))
    assert done_keys(path) == {("c1", 0, "default", None)}


def test_corrupt_middle_line_raises(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    path.write_text("garbage\n" + rec("c1").model_dump_json() + "\n")
    with pytest.raises(ValueError, match="corrupt"):
        done_keys(path)


def test_missing_file(tmp_path: Path) -> None:
    assert done_keys(tmp_path / "none.jsonl") == set()
