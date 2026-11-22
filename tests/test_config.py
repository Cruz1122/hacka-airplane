from __future__ import annotations

from pathlib import Path

import pytest

from nevados_bench.config import (
    ImageLock,
    ModelLock,
    get_model,
    load_image_lock,
    load_models,
    load_models_lock,
    load_profiles,
    save_image_lock,
    upsert_model_lock,
)


def test_real_models_yaml_applies_defaults() -> None:
    models = load_models()
    assert len(models) == 25
    granite = get_model("granite4-350m")
    assert granite.quant == "Q4_K_M" and granite.deployable and granite.thinking == "none"
    assert granite.grounded_qa and granite.sampling == {}
    assert get_model("xlam2-1b").deployable is False
    assert get_model("lfm2.5-2.6b").thinking == "always"
    assert get_model("functiongemma-270m").grounded_qa is False
    assert get_model("qwen3-0.6b").sampling["top_k"] == 20
    with pytest.raises(KeyError):
        get_model("nope")


def test_real_profiles_yaml() -> None:
    cfg = load_profiles()
    assert cfg.profiles["phone-tight"].cpuset == "0-2"
    assert cfg.profiles["phone-tight"].threads == 3
    assert cfg.profiles["phone-nominal"].memory == "5g"
    assert cfg.server.cache_ram_mib == 0 and cfg.server.parallel == 1
    assert cfg.server.reasoning == "off"


def test_duplicate_ids_rejected(tmp_path: Path) -> None:
    p = tmp_path / "m.yaml"
    entry = "{id: a, repo: r, file: f, license: l}"
    p.write_text(f"models:\n  - {entry}\n  - {entry}\n")
    with pytest.raises(ValueError, match="duplicate"):
        load_models(p)


def test_lock_roundtrip(tmp_path: Path) -> None:
    lock = tmp_path / "models.lock.yaml"
    assert load_models_lock(lock) == {}
    a = ModelLock(id="b", repo="r", filename="b.gguf", size_bytes=1, sha256="x")
    upsert_model_lock(a, lock)
    upsert_model_lock(a.model_copy(update={"id": "a"}), lock)
    upsert_model_lock(a.model_copy(update={"sha256": "y"}), lock)
    locks = load_models_lock(lock)
    assert list(locks) == ["a", "b"] and locks["b"].sha256 == "y"

    img = tmp_path / "image.lock.yaml"
    assert load_image_lock(img) is None
    il = ImageLock(image="i:server", ref="i@sha256:1", digest="sha256:1", version="b1")
    save_image_lock(il, img)
    assert load_image_lock(img) == il
