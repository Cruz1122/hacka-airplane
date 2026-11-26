"""Cached ft4 GGUF embeddings (phone model) for the depth_v1 checks. Run inside the nlu venv:
cd experiments/nlu && uv run python ../../research_notes/depth_v1/tools/<script>.py

Cache: inputs/emb_cache.npz (texts + float16 vectors). Texts are whitespace-normalised.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from common import DEPTH, ROOT

sys.path.insert(0, str(ROOT / "experiments/laya"))
from export_knowledge import embed_gguf  # noqa: E402

GGUF = ROOT / "models/knowledge/e5-nlu-ft4-f16.gguf"
BIN = Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding"
CACHE = DEPTH / "inputs/emb_cache.npz"


def norm(t: str) -> str:
    return " ".join(t.split())


def embed(texts: list[str]) -> np.ndarray:
    """Vectors (float32, L2-normalised) for texts, embedding only those not cached yet."""
    texts = [norm(t) for t in texts]
    known: dict[str, np.ndarray] = {}
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=False)
        known = dict(zip(z["texts"].tolist(), z["vecs"], strict=True))
    todo = sorted({t for t in texts if t not in known})
    if todo:
        for t, v in zip(todo, embed_gguf(todo, GGUF, BIN), strict=True):
            known[t] = v.astype(np.float16)
        ks = sorted(known)
        np.savez(CACHE, texts=np.asarray(ks), vecs=np.stack([known[k] for k in ks]))
    return np.stack([known[t].astype(np.float32) for t in texts]) if texts else np.zeros((0, 768), np.float32)
