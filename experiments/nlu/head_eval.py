"""Linear head over frozen e5 vectors (multinomial logistic regression), scored on the blind set.

On the phone this is one more MatMul + bias after the embedding, so it fits the ONNX scorer.
Compares, on the same split: dense top-k retrieval, the head alone, and a blend of both.

usage: python head_eval.py [--model M] [--split dev] [--C 20] [--hubs]
"""

from __future__ import annotations

import argparse

import numpy as np
from sklearn.linear_model import LogisticRegression

from evaluate import Index, load_blind
from kb import Embedder, app_texts, load_entries


def accuracy(rows, pred_ids, conf, T) -> float:
    ok = 0
    for r, p, c in zip(rows, pred_ids, conf):
        ans = p if c >= T else None
        acc = r["acceptable"]
        ok += (ans in acc) if acc else ans is None
    return ok / len(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--C", type=float, nargs="+", default=[5, 20, 50])
    ap.add_argument("--w", type=float, default=0.5, help="follow-up fusion weight")
    ap.add_argument("--hubs", action="store_true")
    ap.add_argument("--strip", action="store_true", help="strip chat fillers (kb.clean) before embedding")
    a = ap.parse_args()

    blind = load_blind()
    rows = [r for r in blind if r["split"] == a.split]
    banned = {t.strip().lower() for r in blind for t in r["turns"]}
    entries = load_entries(hubs=a.hubs)
    emb = Embedder(a.model, strip_fillers=a.strip)
    idx = Index(emb, entries, app_texts(conv=True), banned)
    X, y = idx.V, idx.owner

    last = emb.encode([r["turns"][-1] for r in rows])
    prev = emb.encode([" ".join(r["turns"][:-1]) if len(r["turns"]) > 1 else r["turns"][-1] for r in rows])
    multi = np.array([len(r["turns"]) > 1 for r in rows])

    def fuse(s_last, s_prev):
        out = s_last.copy()
        out[multi] = (s_last[multi] + a.w * s_prev[multi]) / (1 + a.w)
        return out

    dense = fuse(idx.scores(last, "top3"), idx.scores(prev, "top3"))
    Ts = np.arange(0.0, 0.96, 0.01)

    def report(name, S):
        top = S.argmax(1)
        ids = [entries[t].id for t in top]
        conf = S.max(1)
        best = max((accuracy(rows, ids, conf, T), T) for T in Ts)
        print(f"{name:28s} acc@T0={accuracy(rows, ids, conf, -1e9):.3f} best={best[0]:.3f} (T={best[1]:.2f})", flush=True)

    print(f"split={a.split} n={len(rows)} train_rows={len(X)} classes={len(entries)}", flush=True)
    report("dense top3", dense)
    for C in a.C:
        clf = LogisticRegression(C=C, max_iter=300, n_jobs=-1)
        clf.fit(X, y)
        full = np.zeros((len(rows), len(entries)), dtype=np.float32)
        P = fuse(clf.predict_proba(last), clf.predict_proba(prev))
        full[:, clf.classes_] = P
        report(f"head C={C}", full)
        # Blend: retrieval cosine plus the head's probability (both in [0, 1]).
        for lam in (0.3, 0.6):
            report(f"dense + {lam}*head C={C}", dense + lam * full)


if __name__ == "__main__":
    main()
