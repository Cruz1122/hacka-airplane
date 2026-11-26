"""Typed loaders for config/models.yaml, config/profiles.yaml and the lock files."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_YAML = CONFIG_DIR / "models.yaml"
PROFILES_YAML = CONFIG_DIR / "profiles.yaml"
MODELS_LOCK = CONFIG_DIR / "models.lock.yaml"
IMAGE_LOCK = CONFIG_DIR / "image.lock.yaml"

Thinking = Literal["none", "off_by_default", "on_by_default", "always"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ModelConfig(_Strict):
    id: str
    repo: str
    file: str  # exact filename or glob resolved against the repo listing
    license: str
    quant: str = "Q4_K_M"
    deployable: bool = True
    thinking: Thinking = "none"
    grounded_qa: bool = True
    sampling: dict[str, Any] = Field(default_factory=dict)


class HardwareProfile(_Strict):
    cpuset: str
    threads: int = Field(gt=0)
    memory: str  # docker memory string, e.g. "4g"


class ServerConfig(_Strict):
    image: str
    ctx_size: int = Field(gt=0)
    parallel: int = 1
    cache_ram_mib: int = 0
    reasoning: Literal["on", "off", "auto"] = "off"
    port: int = 8080


class ProfilesConfig(_Strict):
    profiles: dict[str, HardwareProfile]
    server: ServerConfig


class ModelLock(_Strict):
    id: str
    repo: str
    filename: str
    size_bytes: int
    sha256: str


class ImageLock(_Strict):
    image: str  # the tag that was resolved
    ref: str  # repo@sha256:... usable by `docker run`
    digest: str  # sha256:...
    version: str | None = None
    revision: str | None = None
    created: str | None = None


def _read_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _write_yaml_atomic(path: Path, data: Any) -> None:
    """Write YAML via a temp file + rename so a crash never leaves a half-written lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=True)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def load_models(path: Path = MODELS_YAML) -> list[ModelConfig]:
    """Load the model registry, applying the top-level `defaults` to every entry."""
    raw = _read_yaml(path) or {}
    defaults = raw.get("defaults") or {}
    models = [ModelConfig.model_validate({**defaults, **entry}) for entry in raw.get("models", [])]
    ids = [m.id for m in models]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ValueError(f"duplicate model ids in {path}: {dupes}")
    return models


def get_model(model_id: str, path: Path = MODELS_YAML) -> ModelConfig:
    for model in load_models(path):
        if model.id == model_id:
            return model
    raise KeyError(f"unknown model id {model_id!r} in {path}")


def load_profiles(path: Path = PROFILES_YAML) -> ProfilesConfig:
    return ProfilesConfig.model_validate(_read_yaml(path))


def load_models_lock(path: Path = MODELS_LOCK) -> dict[str, ModelLock]:
    """Return locks keyed by model id; a missing file is an empty lock."""
    if not path.exists():
        return {}
    raw = _read_yaml(path) or {}
    return {e["id"]: ModelLock.model_validate(e) for e in raw.get("models", [])}


def upsert_model_lock(entry: ModelLock, path: Path = MODELS_LOCK) -> None:
    locks = load_models_lock(path)
    locks[entry.id] = entry
    ordered = [locks[k].model_dump() for k in sorted(locks)]
    _write_yaml_atomic(path, {"models": ordered})


def load_image_lock(path: Path = IMAGE_LOCK) -> ImageLock | None:
    if not path.exists():
        return None
    return ImageLock.model_validate(_read_yaml(path))


def save_image_lock(lock: ImageLock, path: Path = IMAGE_LOCK) -> None:
    _write_yaml_atomic(path, lock.model_dump())
