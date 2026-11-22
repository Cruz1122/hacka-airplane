"""Append-only, crash-safe JSONL writer for RequestRecord, with resume support."""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import TracebackType
from typing import IO, Any

from nevados_bench.schemas import RequestRecord

RecordKey = tuple[str, int, str, str | None]  # (case_id, rep, arm, fc_mode)


def record_key(record: RequestRecord | dict[str, Any]) -> RecordKey:
    data = record.model_dump() if isinstance(record, RequestRecord) else record
    return (data["case_id"], data.get("rep", 0), data.get("arm", "default"), data.get("fc_mode"))


def _drop_partial_tail(path: Path) -> None:
    """Truncate a last line without newline (crash mid-write) so appends stay line-aligned.

    The partial record is lost, which is safe: it is absent from done_keys and re-runs.
    """
    with path.open("rb+") as fh:
        fh.seek(0, os.SEEK_END)
        size = fh.tell()
        if size == 0:
            return
        fh.seek(size - 1)
        if fh.read(1) == b"\n":
            return
        pos = size
        step = 1 << 16
        while pos > 0:
            start = max(0, pos - step)
            fh.seek(start)
            block = fh.read(pos - start)
            idx = block.rfind(b"\n")
            if idx != -1:
                fh.truncate(start + idx + 1)
                return
            pos = start
        fh.truncate(0)


def done_keys(path: Path) -> set[RecordKey]:
    """Keys already written. Tolerates a truncated last line; corruption elsewhere raises."""
    if not path.exists():
        return set()
    lines = path.read_bytes().split(b"\n")
    keys: set[RecordKey] = set()
    last = len(lines) - 1
    for i, raw in enumerate(lines):
        if not raw.strip():
            continue
        try:
            keys.add(record_key(json.loads(raw)))
        except (json.JSONDecodeError, KeyError) as exc:
            if i == last:  # no trailing newline: crash mid-write
                continue
            raise ValueError(f"{path}:{i + 1}: corrupt record line") from exc
    return keys


class RecordWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._fh: IO[str] | None = None

    def __enter__(self) -> RecordWriter:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def open(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            _drop_partial_tail(self.path)
        self._fh = self.path.open("a", encoding="utf-8")

    def append(self, record: RequestRecord) -> None:
        if self._fh is None:
            self.open()
        assert self._fh is not None
        self._fh.write(record.model_dump_json() + "\n")
        self._fh.flush()
        os.fsync(self._fh.fileno())

    def close(self) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None
