"""Check how a proposal changes e5 routing, before anyone applies it.

    uv run --project experiments/laya python research_notes/curation_v2/tools/route_check.py \
        --proposal P.json [--out report.json]

Builds the candidate corpus in memory with the add-park-knowledge tool (nothing is written), embeds
labels + examples with multilingual-e5-base (cached in .cache/e5base.sqlite, one process at a time
under .cache/e5.lock) and reports, over the flat index of visitor entries:
  - touched_loo: for every example of an added/updated entry, the leave-one-out rank of its own
    entry (own vector masked) and the closest foreign entry when own is not rank 1;
  - removed: every example that the proposal removes (edited away or deleted entry) and whether it
    still reaches its entry, or the delete's replace_with, in the top 3 of the new corpus.
A removed core phrasing that no longer routes is the Phase 2 swap regression; fix it before review.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / ".cache"
KTOOL = ROOT / ".claude/skills/add-park-knowledge/scripts/knowledge.py"
MODEL = "intfloat/multilingual-e5-base"
PREFIX = "query: "  # e5 is used with the query prefix for both questions and examples here


def load_ktool():
    spec = importlib.util.spec_from_file_location("knowledge", KTOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def embed(texts: list[str]) -> np.ndarray:
    """Normalized e5-base vectors, cached by text hash; serialized across processes."""
    CACHE.mkdir(exist_ok=True)
    with open(CACHE / "e5.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        db = sqlite3.connect(CACHE / "e5base.sqlite")
        db.execute("create table if not exists v (h text primary key, b blob)")
        keys = [hashlib.sha1((PREFIX + t).encode()).hexdigest() for t in texts]
        have = {}
        uniq = list(dict.fromkeys(keys))
        for i in range(0, len(uniq), 900):
            chunk = uniq[i:i + 900]
            q = f"select h, b from v where h in ({','.join('?' * len(chunk))})"
            have.update(db.execute(q, chunk).fetchall())
        missing = [(k, t) for k, t in dict(zip(keys, texts)).items() if k not in have]
        if missing:
            from sentence_transformers import SentenceTransformer

            m = SentenceTransformer(MODEL, device="cpu")
            vecs = m.encode([PREFIX + t for _, t in missing], batch_size=64,
                            normalize_embeddings=True)
            rows = [(k, np.asarray(v, np.float32).tobytes()) for (k, _), v in zip(missing, vecs)]
            db.executemany("insert or replace into v values (?, ?)", rows)
            db.commit()
            have.update(rows)
        db.close()
    return np.stack([np.frombuffer(have[k], np.float32) for k in keys])


def flat_index(sections: dict) -> tuple[list[str], np.ndarray, np.ndarray, list[str]]:
    ids, owner, texts = [], [], []
    for s in sections.values():
        for e in s["entries"]:
            if e["audience"] != "visitor":
                continue
            ids.append(e["id"])
            for t in (e["label"], *e["examples"]):
                owner.append(len(ids) - 1)
                texts.append(t)
    return ids, np.asarray(owner), embed(texts), texts


def ranks(ids, owner, vecs, qv, mask_row=None):
    sims = vecs @ qv
    if mask_row is not None:
        sims[mask_row] = -1.0
    best = np.full(len(ids), -1.0, np.float32)
    np.maximum.at(best, owner, sims)
    order = np.argsort(-best)
    return order, best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposal", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    kt = load_ktool()
    proposal = json.loads(Path(a.proposal).read_text())
    ops, writes, *_ = kt.build(ROOT, proposal)
    before = {p.stem: json.loads(p.read_text()) for p in (ROOT / kt.SECTIONS).glob("*.json")}
    after = dict(before)
    for name, data in writes.items():
        if name.startswith(str(kt.SECTIONS)):
            after[Path(name).stem] = json.loads(data)
    ids, owner, vecs, texts = flat_index(after)
    pos = {eid: i for i, eid in enumerate(ids)}
    before_entries = {e["id"]: e for s in before.values() for e in s["entries"]}
    touched, removed = [], []
    for rec in ops:
        op = kt.record_op(rec)
        eid = kt.record_id(rec)
        if op != "delete" and eid in pos:
            i = pos[eid]
            rows = np.nonzero(owner == i)[0][1:]  # skip the label vector
            for r in rows:
                order, best = ranks(ids, owner, vecs, vecs[r], mask_row=r)
                rank = int(np.nonzero(order == i)[0][0]) + 1
                item = {"id": eid, "example": texts[r], "rank": rank}
                if rank > 1:
                    item.update(top1=ids[order[0]], top1_cos=round(float(best[order[0]]), 4),
                                own_cos=round(float(best[i]), 4))
                touched.append(item)
        old = before_entries.get(eid)
        if old is None:
            continue
        new_ex = set(rec["entry"]["examples"]) if op != "delete" else set()
        gone = [x for x in old["examples"] if x not in new_ex]
        target = rec.get("replace_with") if op == "delete" else eid
        if gone:
            qv = embed(gone)
            for x, v in zip(gone, qv):
                order, best = ranks(ids, owner, vecs, v)
                top3 = [ids[j] for j in order[:3]]
                removed.append({"id": eid, "example": x, "target": target,
                                "ok_top3": target in top3, "top3": top3})
    n_t = len(touched)
    rep = {
        "proposal": a.proposal,
        "ops": kt.op_counts(ops),
        "touched_examples": n_t,
        "touched_loo_top1": round(sum(t["rank"] == 1 for t in touched) / n_t, 4) if n_t else None,
        "touched_confusions": [t for t in touched if t["rank"] > 1],
        "removed_examples": len(removed),
        "removed_not_routing": [r for r in removed if not r["ok_top3"]],
    }
    text = json.dumps(rep, indent=1, ensure_ascii=False)
    if a.out:
        Path(a.out).write_text(text)
    summary = {k: v for k, v in rep.items() if not isinstance(v, list)}
    summary["n_touched_confusions"] = len(rep["touched_confusions"])
    summary["n_removed_not_routing"] = len(rep["removed_not_routing"])
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
