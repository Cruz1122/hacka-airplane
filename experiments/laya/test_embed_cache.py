"""The export's embedding cache: a re-export embeds only texts the model has not seen.

Run: cd experiments/laya && uv run --with pytest pytest -q test_embed_cache.py
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def ek(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "export_knowledge_under_test", ROOT / "experiments/laya/export_knowledge.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "EMBED_CACHE", tmp_path / "cache")
    calls: list[list[str]] = []

    def fake_run(texts, gguf, binary):
        calls.append(list(texts))
        return np.array([[len(t), 1.0] for t in texts], dtype=np.float32)

    monkeypatch.setattr(mod, "_run_llama_embedding", fake_run)
    mod.calls = calls
    return mod


def test_second_export_embeds_only_new_texts(ek, tmp_path):
    gguf = tmp_path / "model.gguf"
    gguf.write_bytes(b"model-a")
    first = ek.embed_gguf(["uno", "dos", "uno"], gguf, Path("bin"))
    assert ek.calls == [["uno", "dos"]]
    assert first.tolist() == [[3, 1], [3, 1], [3, 1]]

    second = ek.embed_gguf(["dos", "tres palabras"], gguf, Path("bin"))
    assert ek.calls[1] == ["tres palabras"]
    assert second.tolist() == [[3, 1], [13, 1]]


def test_another_model_never_reuses_vectors(ek, tmp_path):
    a, b = tmp_path / "a.gguf", tmp_path / "b.gguf"
    a.write_bytes(b"model-a")
    b.write_bytes(b"model-b")
    ek.embed_gguf(["uno"], a, Path("bin"))
    ek.embed_gguf(["uno"], b, Path("bin"))
    assert ek.calls == [["uno"], ["uno"]]
