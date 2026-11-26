from __future__ import annotations

import hashlib
from pathlib import Path

import httpx
import pytest

from nevados_bench.config import ModelConfig, load_models_lock
from nevados_bench.runner.fetch import FetchError, resolve_and_download, resolve_file

BLOB = b"GGUF" + bytes(range(256)) * 40
SHA = hashlib.sha256(BLOB).hexdigest()
REPO = "org/model-GGUF"


def listing(sha: str = SHA) -> list[dict[str, object]]:
    return [
        {"type": "file", "path": "README.md", "size": 10},
        {
            "type": "file",
            "path": "m-Q4_K_M.gguf",
            "size": len(BLOB),
            "lfs": {"oid": sha, "size": len(BLOB)},
        },
        {"type": "file", "path": "mmproj-m-Q4_K_M.gguf", "size": 5},
        {"type": "file", "path": "m-Q8_0.gguf", "size": 5},
    ]


def transport(calls: list[httpx.Request], sha: str = SHA) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if "/api/models/" in request.url.path:
            return httpx.Response(200, json=listing(sha))
        rng = request.headers.get("Range")
        if rng:
            start = int(rng.split("=")[1].rstrip("-"))
            return httpx.Response(206, content=BLOB[start:])
        return httpx.Response(200, content=BLOB)

    return httpx.MockTransport(handler)


def cfg(file: str = "*Q4_K_M.gguf") -> ModelConfig:
    return ModelConfig(id="m", repo=REPO, file=file, license="apache-2.0")


def test_resolve_file_rules() -> None:
    assert resolve_file(listing(), "*Q4_K_M.gguf", REPO)["path"] == "m-Q4_K_M.gguf"
    assert resolve_file(listing(), "m-Q8_0.gguf", REPO)["path"] == "m-Q8_0.gguf"
    with pytest.raises(FetchError, match="matched 0"):
        resolve_file(listing(), "*Q5*", REPO)
    with pytest.raises(FetchError, match="matched 2"):
        resolve_file(listing(), "m-*.gguf", REPO)


def test_download_resume_and_idempotent(tmp_path: Path) -> None:
    models = tmp_path / "models"
    models.mkdir()
    lock = tmp_path / "lock.yaml"
    (models / "m-Q4_K_M.gguf.part").write_bytes(BLOB[:1000])  # interrupted earlier
    calls: list[httpx.Request] = []
    with httpx.Client(transport=transport(calls)) as client:
        entry = resolve_and_download(cfg(), models, lock_path=lock, client=client)
        assert entry.sha256 == SHA and entry.size_bytes == len(BLOB)
        assert (models / "m-Q4_K_M.gguf").read_bytes() == BLOB
        assert not (models / "m-Q4_K_M.gguf.part").exists()
        assert calls[1].headers["Range"] == "bytes=1000-"
        assert load_models_lock(lock)["m"].filename == "m-Q4_K_M.gguf"

        calls.clear()
        again = resolve_and_download(cfg(), models, lock_path=lock, client=client)
        assert again == entry
        assert len(calls) == 1  # listing only, no download


def test_sha_mismatch(tmp_path: Path) -> None:
    calls: list[httpx.Request] = []
    with (
        httpx.Client(transport=transport(calls, sha="0" * 64)) as client,
        pytest.raises(FetchError, match="sha256"),
    ):
        resolve_and_download(cfg(), tmp_path, lock_path=tmp_path / "l.yaml", client=client)
    assert not (tmp_path / "l.yaml").exists()
