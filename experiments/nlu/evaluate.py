"""Blind-set accuracy of a retrieval configuration (top-1 answer or abstain).

Correct = the predicted entry is in the labelled `acceptable` set; for rows with no acceptable
entry (off-topic or not covered), abstaining is correct. Follow-up turns are embedded with the
conversation context (see `followup_vectors`).

usage: python evaluate.py --model PATH_OR_HF_ID [--split dev|test|all] [--aug] [--mode top3]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from kb import ROOT, Embedder, app_texts, load_entries

W = ROOT / "experiments/nlu/work"


def load_blind() -> list[dict]:
    rows = {json.loads(l)["qid"]: json.loads(l) for l in open(W / "queries_raw.jsonl") if l.strip()}
    for f in sorted(W.glob("labels_[0-9]*.jsonl")):
        for l in f.read_text().splitlines():
            if l.strip():
                lab = json.loads(l)
                if lab["qid"] in rows:
                    rows[lab["qid"]].update(lab)
    # Hub answers judged acceptable in a second, hub-only pass (labels_hub_*.jsonl).
    for f in sorted(W.glob("labels_hub_*.jsonl")):
        for l in f.read_text().splitlines():
            if l.strip():
                lab = json.loads(l)
                r = rows.get(lab["qid"])
                if r is not None and "acceptable" in r and lab["hubs"]:
                    r["acceptable"] = [*r["acceptable"], *lab["hubs"]]
    out = [r for r in rows.values() if "acceptable" in r]
    for r in out:  # fixed split: half of every style goes to test, by qid hash
        r["split"] = "test" if int(hashlib.sha256(r["qid"].encode()).hexdigest(), 16) % 2 else "dev"
    return out



class Index:
    def __init__(self, emb: Embedder, entries, aug: dict[str, list[str]] | None, banned: set[str]):
        texts, owner = [], []
        for i, e in enumerate(entries):
            for t in [e.label, *e.examples, *(aug.get(e.id, []) if aug else [])]:
                if t.strip().lower() in banned:
                    continue
                texts.append(t)
                owner.append(i)
        self.entries, self.owner, self.emb = entries, np.array(owner), emb
        self.V = emb.encode(texts)
        self.groups = [np.flatnonzero(self.owner == i) for i in range(len(entries))]

    def scores(self, Q: np.ndarray, mode: str) -> np.ndarray:
        sim = Q @ self.V.T
        out = np.full((len(Q), len(self.entries)), -1.0, dtype=np.float32)
        k = 1 if mode == "max" else int(mode[3:])
        for e, g in enumerate(self.groups):
            if len(g):
                s = np.sort(sim[:, g], 1)[:, ::-1][:, :k]
                out[:, e] = s.mean(1)
        return out


def followup_vectors(emb: Embedder, rows: list[dict], strategy: str, w: float) -> np.ndarray:
    last = emb.encode([r["turns"][-1] for r in rows])
    if strategy == "last":
        return last
    ctx = emb.encode([" ".join(r["turns"]) for r in rows])
    if strategy == "concat":
        return ctx
    prev = emb.encode([r["turns"][-2] if len(r["turns"]) > 1 else r["turns"][-1] for r in rows])
    mix = last + w * prev
    return mix / np.linalg.norm(mix, axis=1, keepdims=True)


def evaluate(rows, idx: Index, mode: str, T: float, strategy: str, w: float) -> dict:
    single = [r for r in rows if len(r["turns"]) == 1]
    multi = [r for r in rows if len(r["turns"]) > 1]
    preds = {}
    for group, strat in ((single, "last"), (multi, strategy)):
        if not group:
            continue
        if strat == "fuse":
            # Entry-level fusion: relevant to the new message AND to what came before.
            s_last = idx.scores(idx.emb.encode([r["turns"][-1] for r in group]), mode)
            s_prev = idx.scores(idx.emb.encode([" ".join(r["turns"][:-1]) for r in group]), mode)
            S = (s_last + w * s_prev) / (1 + w)
        else:
            S = idx.scores(followup_vectors(idx.emb, group, strat, w), mode)
        for r, s in zip(group, S):
            top = int(s.argmax())
            preds[r["qid"]] = (idx.entries[top].id, float(s[top]))
    by = defaultdict(lambda: [0, 0])
    detail = []
    for r in rows:
        pid, sc = preds[r["qid"]]
        answer = pid if sc >= T else None
        acc = set(r["acceptable"])
        ok = (answer in acc) if acc else (answer is None)
        by[r["style"]][0] += ok
        by[r["style"]][1] += 1
        detail.append({"qid": r["qid"], "turns": r["turns"], "pred": pid, "score": round(sc, 4),
                       "abstain": answer is None, "acceptable": r["acceptable"], "ok": ok})
    tot = sum(v[0] for v in by.values()), sum(v[1] for v in by.values())
    return {"acc": tot[0] / tot[1], "n": tot[1], "by_style": {k: round(v[0] / v[1], 3) for k, v in sorted(by.items())},
            "detail": detail}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--aug", action="store_true")
    ap.add_argument("--mode", default="top3")
    ap.add_argument("--strategy", default="mix")
    ap.add_argument("--w", type=float, default=0.5)
    ap.add_argument("--dump", type=Path)
    ap.add_argument("--hubs", action="store_true")
    ap.add_argument("--strip", action="store_true", help="strip chat fillers (kb.clean) before embedding")
    ap.add_argument("--conv", action="store_true")
    a = ap.parse_args()

    rows = load_blind()
    if a.split != "all":
        rows = [r for r in rows if r["split"] == a.split]
    banned = {t.strip().lower() for r in load_blind() for t in r["turns"]}
    entries = load_entries(hubs=a.hubs)
    emb = Embedder(a.model, strip_fillers=a.strip)
    extra = app_texts(conv=a.conv) if a.aug else None
    idx = Index(emb, entries, extra, banned)
    print(f"model={a.model} split={a.split} n={len(rows)} rows={len(idx.V)} mode={a.mode} strategy={a.strategy}")
    best = None
    for T in np.arange(0.70, 0.96, 0.01):
        res = evaluate(rows, idx, a.mode, float(T), a.strategy, a.w)
        if best is None or res["acc"] > best[1]["acc"]:
            best = (float(T), res)
    T, res = best
    print(f"best T={T:.2f} acc={res['acc']:.3f} by_style={res['by_style']}")
    if a.dump:
        a.dump.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in res["detail"]) + "\n")


if __name__ == "__main__":
    main()
