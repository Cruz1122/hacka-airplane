"""Quick lever comparison on a pseudo-dev set: the last 2 examples of every entry are held out of
the index and used as queries. In-distribution (same writers as the index), so it ranks ideas;
the blind set decides.

usage: python pseudo_dev.py --model intfloat/multilingual-e5-base
"""

from __future__ import annotations

import argparse

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from kb import Embedder, fold, load_entries


def entry_scores(sim: np.ndarray, owner: np.ndarray, n_entries: int, mode: str) -> np.ndarray:
    """sim: [Q, rows]; owner: row -> entry. Returns [Q, n_entries]."""
    out = np.full((sim.shape[0], n_entries), -1.0, dtype=np.float32)
    if mode == "max":
        for e in range(n_entries):
            out[:, e] = sim[:, owner == e].max(1)
    elif mode.startswith("top"):
        k = int(mode[3:])
        for e in range(n_entries):
            s = np.sort(sim[:, owner == e], 1)[:, ::-1][:, :k]
            out[:, e] = s.mean(1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--prefix", default="query: ")
    a = ap.parse_args()

    entries = load_entries()
    texts, owner, queries, gold = [], [], [], []
    short_rows = []
    for i, e in enumerate(entries):
        keep, held = e.examples[:-2], e.examples[-2:]
        for t in [e.label, *keep]:
            texts.append(t)
            owner.append(i)
        short_rows.append(e.short)
        queries += held
        gold += [i] * len(held)
    owner = np.array(owner)
    gold = np.array(gold)
    n = len(entries)

    emb = Embedder(a.model, prefix=a.prefix)
    V = emb.encode(texts)
    Q = emb.encode(queries)
    S = emb.encode(short_rows)
    sim = Q @ V.T
    sim_short = Q @ S.T

    def acc(scores: np.ndarray) -> str:
        top = scores.argmax(1)
        top3 = np.argsort(-scores, 1)[:, :3]
        return f"top1 {np.mean(top == gold):.3f}  top3 {np.mean((top3 == gold[:, None]).any(1)):.3f}"

    print(f"model={a.model} queries={len(queries)} rows={len(texts)} entries={n}")
    base = {m: entry_scores(sim, owner, n, m) for m in ("max", "top2", "top3")}
    for m, s in base.items():
        print(f"  dense {m:5s}: {acc(s)}")
    for w in (0.3, 0.5):
        print(f"  max + {w}*short : {acc(np.maximum(base['max'], 0) + w * sim_short)}")

    # Lexical channel: char n-grams on folded text, robust to typos and missing accents.
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=1)
    X = vec.fit_transform([fold(t) for t in texts])
    Xq = vec.transform([fold(q) for q in queries])
    lex = (Xq @ X.T).toarray().astype(np.float32)
    lex_e = entry_scores(lex, owner, n, "max")
    print(f"  lexical max   : {acc(lex_e)}")
    for w in (0.1, 0.2, 0.3):
        print(f"  dense max + {w}*lex: {acc(base['max'] + w * lex_e)}")


if __name__ == "__main__":
    main()
