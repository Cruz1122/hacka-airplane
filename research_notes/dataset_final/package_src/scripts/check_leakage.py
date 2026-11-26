"""Leakage between train and every held-out split: exact (normalized) and near-duplicate text.

    python scripts/check_leakage.py              # exact + character-trigram Jaccard >= 0.8 (stdlib)
    python scripts/check_leakage.py --semantic   # + e5-base cosine >= 0.93 (needs sentence-transformers)
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SPLITS, Report, jl, norm  # noqa: E402

JACCARD = 0.8
COS = 0.93


def grams(t: str) -> set[str]:
    t = f"  {t}  "
    return {t[i:i + 3] for i in range(len(t) - 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--semantic", action="store_true")
    a = ap.parse_args()
    rep = Report("check_leakage")
    train = [r["state"] for r in jl(__import__("_common").PKG / SPLITS["train"])]
    tn = {norm(t) for t in train}
    tg = [grams(norm(t)) for t in train]
    inv = defaultdict(set)
    for i, g in enumerate(tg):
        for x in g:
            inv[x].add(i)
    held = {s: [r["state"] for r in jl(__import__("_common").PKG / rel)] for s, rel in SPLITS.items() if s != "train"}
    for s, texts in held.items():
        exact = sum(norm(t) in tn for t in texts)
        near = 0
        for t in texts:
            g = grams(norm(t))
            cand = defaultdict(int)
            for x in g:
                for i in inv.get(x, ()):
                    cand[i] += 1
            if any(c / (len(g) + len(tg[i]) - c) >= JACCARD for i, c in cand.items()):
                near += 1
        rep.notes.append(f"{s}: {len(texts)} rows, exact {exact}, trigram-jaccard>={JACCARD} {near}")
        rep.check(exact == 0, f"{s}: {exact} exact duplicates of train")
        if not s.endswith("READ_ONLY"):
            rep.check(near == 0, f"{s}: {near} near-duplicates of train")
    if a.semantic:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        m = SentenceTransformer("intfloat/multilingual-e5-base")
        enc = lambda xs: m.encode(["query: " + x for x in xs], batch_size=64, normalize_embeddings=True)  # noqa: E731
        tv = enc(train)
        for s, texts in held.items():
            if not texts:
                continue
            hits = int(((enc(texts) @ tv.T).max(axis=1) >= COS).sum())
            rep.notes.append(f"{s}: e5 cosine>={COS} vs train: {hits}")
            rep.check(hits == 0, f"{s}: {hits} rows with e5 cosine >= {COS} to a train row")
    rep.done()


if __name__ == "__main__":
    main()
