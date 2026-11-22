"""Model download (Hugging Face, anonymous) and image pinning.

No token handling on purpose: every repo in the registry is public, and credential
files must never be read by this tool.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import httpx

from nevados_bench.config import (
    IMAGE_LOCK,
    MODELS_LOCK,
    ImageLock,
    ModelConfig,
    ModelLock,
    load_models_lock,
    save_image_lock,
    upsert_model_lock,
)

HF_BASE = "https://huggingface.co"
_CHUNK = 1 << 20


class FetchError(RuntimeError):
    pass


def list_repo_files(client: httpx.Client, repo: str) -> list[dict[str, Any]]:
    resp = client.get(f"{HF_BASE}/api/models/{repo}/tree/main")
    if resp.status_code != 200:
        raise FetchError(f"listing {repo} failed: HTTP {resp.status_code}: {resp.text[:300]}")
    return [e for e in resp.json() if e.get("type") == "file"]


def resolve_file(entries: list[dict[str, Any]], pattern: str, repo: str) -> dict[str, Any]:
    """Pick exactly one repo entry matching `pattern` (exact name or glob), ignoring mmproj."""
    candidates = [e for e in entries if "mmproj" not in e["path"].lower()]
    exact = [e for e in candidates if e["path"] == pattern]
    matches = exact or [e for e in candidates if fnmatch.fnmatchcase(e["path"], pattern)]
    if len(matches) != 1:
        names = [e["path"] for e in matches]
        raise FetchError(
            f"{repo}: pattern {pattern!r} matched {len(matches)} files (need exactly 1): {names}"
        )
    return matches[0]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while block := fh.read(_CHUNK):
            digest.update(block)
    return digest.hexdigest()


def _download(client: httpx.Client, url: str, dest: Path, expected_size: int | None) -> None:
    """Stream `url` into `dest`, resuming from `dest.part` with an HTTP Range request."""
    part = dest.with_name(dest.name + ".part")
    offset = part.stat().st_size if part.exists() else 0
    if expected_size is not None and offset > expected_size:
        part.unlink()
        offset = 0
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    with client.stream("GET", url, headers=headers) as resp:
        if resp.status_code == 416 and expected_size is not None and offset == expected_size:
            pass  # .part already complete
        elif resp.status_code in (200, 206):
            mode = "ab" if resp.status_code == 206 else "wb"  # 200 = server ignored Range
            with part.open(mode) as fh:
                for block in resp.iter_bytes(_CHUNK):
                    fh.write(block)
        else:
            resp.read()
            raise FetchError(f"download {url} failed: HTTP {resp.status_code}: {resp.text[:300]}")
    size = part.stat().st_size
    if expected_size is not None and size != expected_size:
        raise FetchError(
            f"{dest.name}: got {size} bytes, expected {expected_size}; rerun to resume"
        )
    part.replace(dest)


def resolve_and_download(
    model_cfg: ModelConfig,
    models_dir: Path,
    *,
    lock_path: Path = MODELS_LOCK,
    client: httpx.Client | None = None,
) -> ModelLock:
    """Resolve, download (resumable) and sha256-verify one model; upsert its lock entry.

    Idempotent: an already-present file whose size matches and whose lock entry exists
    is not re-hashed.
    """
    own_client = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=httpx.Timeout(60.0))
    try:
        entry = resolve_file(
            list_repo_files(client, model_cfg.repo), model_cfg.file, model_cfg.repo
        )
        filename = Path(entry["path"]).name
        size = entry.get("lfs", {}).get("size") or entry.get("size")
        remote_sha = (entry.get("lfs") or {}).get("oid")
        models_dir.mkdir(parents=True, exist_ok=True)
        dest = models_dir / filename

        existing = load_models_lock(lock_path).get(model_cfg.id)
        if (
            existing is not None
            and existing.filename == filename
            and dest.exists()
            and dest.stat().st_size == existing.size_bytes
            and (remote_sha is None or remote_sha == existing.sha256)
        ):
            return existing

        if not (dest.exists() and size is not None and dest.stat().st_size == size):
            url = f"{HF_BASE}/{model_cfg.repo}/resolve/main/{entry['path']}"
            _download(client, url, dest, size)

        sha = sha256_file(dest)
        if remote_sha and sha != remote_sha:
            bad = dest.with_name(dest.name + ".corrupt")
            dest.replace(bad)
            raise FetchError(f"{filename}: sha256 {sha} != LFS oid {remote_sha}; moved to {bad}")
        lock = ModelLock(
            id=model_cfg.id,
            repo=model_cfg.repo,
            filename=filename,
            size_bytes=dest.stat().st_size,
            sha256=sha,
        )
        upsert_model_lock(lock, lock_path)
        return lock
    finally:
        if own_client:
            client.close()


def lock_image(image: str, *, lock_path: Path = IMAGE_LOCK) -> ImageLock:
    """Pin a locally pulled image to its repo digest and record its build labels."""
    proc = subprocess.run(
        ["docker", "image", "inspect", image], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise FetchError(f"docker image inspect {image} failed: {proc.stderr.strip()}")
    info = json.loads(proc.stdout)[0]
    repo = image.rsplit(":", 1)[0] if ":" in image.rsplit("/", 1)[-1] else image
    digests = [d for d in info.get("RepoDigests") or [] if d.startswith(repo + "@")]
    if not digests:
        raise FetchError(f"{image} has no repo digest (locally built?): {info.get('RepoDigests')}")
    ref = digests[0]
    labels = (info.get("Config") or {}).get("Labels") or {}
    lock = ImageLock(
        image=image,
        ref=ref,
        digest=ref.split("@", 1)[1],
        version=labels.get("org.opencontainers.image.version"),
        revision=labels.get("org.opencontainers.image.revision"),
        created=labels.get("org.opencontainers.image.created"),
    )
    save_image_lock(lock, lock_path)
    return lock
