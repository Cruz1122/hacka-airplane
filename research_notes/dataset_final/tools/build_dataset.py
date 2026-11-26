"""Build the final Laya choice dataset (train / validation / evaluation) from the curated corpus.

    cd experiments/laya
    uv run python ../../research_notes/dataset_final/tools/build_dataset.py pools   # pools + pairs_todo
    uv run python ../../research_notes/dataset_final/tools/build_dataset.py build   # all splits -> out/

Retrieval contract (the same one the app must run at inference):
  e5-base ("query: " prefix on every text) over label + examples of visitor entries; gateway keeps
  up to MAX_SECTIONS sections whose score (max cosine over the section description and its texts)
  is within DELTA of the best; each section contributes its `retrieval.top_k` best entries; the pool
  is the K best of those by entry score (max cosine over its texts). If the pool has fewer than
  MIN_POOL entries it is filled from the flat ranking (`pool_source = flat_fill`).

A corpus example used as a training query is masked out of both the gateway and the entry scores
(otherwise its owner FAQ always comes first at cosine 1.0). Unseen-topic FAQs are removed from the
index while training rows are built, so they never appear as training candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
W = ROOT / "research_notes/dataset_final"
SECTIONS = ROOT / "data/knowledge/sections"
ROUTE = ROOT / "research_notes/curation_v2/tools/route_check.py"
AUDIT = ROOT / "research_notes/curation_v2/audit/label_audit.jsonl"
EVAL_V2 = ROOT / "data/knowledge/eval_v2"
HISTORICAL = ROOT / "data/knowledge/laya_ft/eval.jsonl"

NONE = "ninguna de estas opciones"
INSTR = "¿Qué tema contesta la pregunta del visitante?"
SEED = 20261126
K, MIN_POOL, MAX_SECTIONS, DELTA = 5, 3, 5, 0.05
LEAK_COS = 0.93
UNSEEN_FRAC = 0.08
UNSEEN_EXCLUDE_SECTIONS = {"actions", "conversation"}  # never withhold emergency/chat intents from training
UNSEEN_EXCLUDE_KINDS = {"safety", "action"}  # nor any safety protocol (CPR, lost person, 123/119 lines...)
VERDICTS = {"distinct", "also_answers", "query_dependent", "mislabeled"}
UNSEEN_PER_FAQ = 4


def norm(text: str) -> str:
    t = unicodedata.normalize("NFD", text.casefold()).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^\w\s]", " ", t).split())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bucket(key: str, salt: str = "") -> float:
    return int(hashlib.sha256(f"{SEED}:{salt}:{key}".encode()).hexdigest()[:12], 16) / 16**12


def load_embed():
    spec = importlib.util.spec_from_file_location("route_check_final", ROUTE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.embed


def jl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []


def wjl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows))


class Index:
    def __init__(self, embed):
        self.embed = embed
        self.sections, self.entries = {}, []
        for p in sorted(SECTIONS.glob("*.json")):
            s = json.loads(p.read_text())
            self.sections[s.get("id", p.stem)] = s
            for e in s["entries"]:
                if e.get("audience", "visitor") == "visitor":
                    self.entries.append({**e, "section": s.get("id", p.stem)})
        self.ids = [e["id"] for e in self.entries]
        self.pos = {i: n for n, i in enumerate(self.ids)}
        texts, owner, ex_ref = [], [], []
        for n, e in enumerate(self.entries):
            texts.append(e["label"]); owner.append(n); ex_ref.append(None)
            for j, x in enumerate(e.get("examples", [])):
                texts.append(x); owner.append(n); ex_ref.append(j)
        self.texts, self.owner, self.ex_ref = texts, np.asarray(owner), ex_ref
        self.sec_names = list(self.sections)
        self.text_sec = np.asarray([self.sec_names.index(self.entries[o]["section"]) for o in owner])
        self.entry_sec = np.asarray([self.sec_names.index(e["section"]) for e in self.entries])
        vec = embed(texts + [self.sections[s].get("description", "") for s in self.sec_names])
        self.tv, self.dv = vec[: len(texts)], vec[len(texts):]
        self.top_k = [int(self.sections[s].get("retrieval", {}).get("top_k", 2)) for s in self.sec_names]
        self.example_pos = {(o, j): t for t, (o, j) in enumerate(zip(owner, ex_ref)) if j is not None}
        self.norm_text = [norm(x) for x in texts]

    def self_mask(self, n: int, t: int) -> list[int]:
        """The query text plus every text of the same FAQ that is identical after normalization."""
        return [u for u in np.flatnonzero(self.owner == n) if u == t or self.norm_text[u] == self.norm_text[t]]

    def retrieve(self, q: np.ndarray, mask_text: int | None = None, excluded: np.ndarray | None = None) -> dict:
        sims = self.tv @ q
        if mask_text is not None:  # an int or a list: the query text and identical texts of its owner
            sims[mask_text] = -1.0
        if excluded is not None:
            sims[excluded[self.owner]] = -1.0
        scores = np.full(len(self.entries), -1.0, dtype=np.float32)
        np.maximum.at(scores, self.owner, sims)
        sec = self.dv @ q
        np.maximum.at(sec, self.text_sec, sims)
        order = sorted(range(len(self.sec_names)), key=lambda s: (-sec[s], self.sec_names[s]))
        top = sec[order[0]]
        gates = [s for s in order if sec[s] >= top - DELTA][:MAX_SECTIONS]
        pool = []
        for s in gates:
            members = [n for n in np.flatnonzero(self.entry_sec == s) if scores[n] > -1.0]
            pool += sorted(members, key=lambda n: (-scores[n], self.ids[n]))[: self.top_k[s]]
        pool = sorted(pool, key=lambda n: (-scores[n], self.ids[n]))[:K]
        source = {n: "gateway" for n in pool}
        if len(pool) < MIN_POOL:
            for n in np.argsort(-scores, kind="stable"):
                if len(pool) >= MIN_POOL:
                    break
                if n not in source and scores[n] > -1.0:
                    pool.append(int(n)); source[int(n)] = "flat_fill"
            pool = sorted(pool, key=lambda n: (-scores[n], self.ids[n]))
        flat_rank = {int(n): r + 1 for r, n in enumerate(np.argsort(-scores, kind="stable")[:50])}
        return {"pool": [int(n) for n in pool], "cos": [round(float(scores[n]), 6) for n in pool],
                "pool_source": [source[n] for n in pool], "gates": [self.sec_names[s] for s in gates],
                "gate_scores": [round(float(sec[s]), 6) for s in gates], "flat_rank": flat_rank}


def options(ix: Index, pool: list[int]) -> list[str]:
    used, out = set(), []
    for n in pool:
        t = ix.entries[n]["label"]
        if t in used or t == NONE:
            t = f"{t} ({ix.entries[n]['section']})"
        used.add(t); out.append(t)
    return out


def unseen_ids(ix: Index) -> list[str]:
    eligible = sorted(e["id"] for e in ix.entries if e["section"] not in UNSEEN_EXCLUDE_SECTIONS
                      and e.get("kind") not in UNSEEN_EXCLUDE_KINDS
                      and len(e.get("examples", [])) >= 8)
    by_sec = defaultdict(list)
    for i in eligible:
        by_sec[i.split(".")[0]].append(i)
    rng, held = random.Random(SEED), []
    for s in sorted(by_sec):  # stratified by section
        held += rng.sample(by_sec[s], max(1, round(UNSEEN_FRAC * len(by_sec[s]))))
    return sorted(held)


# --------------------------------------------------------------------------------------- judgments
def load_pair_judgments() -> dict[tuple[str, str], dict]:
    """(gold, other) -> {verdict: distinct|also_answers|query_dependent, by, note}."""
    res = {}
    for p in sorted((W / "judgments").glob("pairs.*.jsonl")):
        for r in jl(p):
            if r.get("verdict") not in VERDICTS:
                raise ValueError(f"{p.name}: bad verdict {r.get('verdict')!r} for {r.get('a')}|{r.get('b')}")
            res[(r["a"], r["b"])] = {**r, "file": p.name}
    for p in sorted((W / "judgments").glob("pairs_arbitration*.jsonl")):  # arbitration overrides
        for r in jl(p):
            if r.get("verdict") not in VERDICTS:
                raise ValueError(f"{p.name}: bad verdict {r.get('verdict')!r} for {r.get('a')}|{r.get('b')}")
            res[(r["a"], r["b"])] = {**r, "file": p.name}
    return res


def load_audit() -> dict[str, dict]:
    res = {}
    for r in jl(AUDIT):
        res[norm(r["question"])] = r
    return res


def load_authored() -> tuple[list[dict], list[dict]]:
    """Authored rows after independent verification; returns (kept, excluded)."""
    ver = {}
    for p in sorted((W / "judgments").glob("authored_verify.*.jsonl")):
        for r in jl(p):
            ver[r["qid"]] = {**r, "file": p.name}
    for p in sorted((W / "judgments").glob("authored_arbitration*.jsonl")):
        for r in jl(p):
            ver[r["qid"]] = {**r, "file": p.name}
    kept, excluded = [], []
    for p in sorted((W / "authored").glob("*.jsonl")):
        for r in jl(p):
            v = ver.get(r["qid"])
            if v is None:
                excluded.append({"qid": r["qid"], "q": r["q"], "reason": "not_verified"}); continue
            if v["verdict"] == "drop":
                excluded.append({"qid": r["qid"], "q": r["q"], "reason": "verifier_drop", "note": v.get("note", "")}); continue
            row = dict(r)
            row["review"] = {"verdict": v["verdict"], "by": v.get("by", v["file"]), "note": v.get("note", "")}
            if v["verdict"] == "fix":
                row["label_before"] = {k: r.get(k) for k in ("case", "gold", "acceptable")}
                for k in ("case", "gold", "acceptable"):
                    if k in v:
                        row[k] = v[k]
            if "near_ids_ok" in v:
                row["near_ids"] = v["near_ids_ok"]
            kept.append(row)
    return kept, excluded


# --------------------------------------------------------------------------------------- rows
def make_row(ix: Index, q: str, ret: dict, acceptable: set[str], doubt: set[str], trace: dict) -> dict:
    pool_ids = [ix.ids[n] for n in ret["pool"]]
    opts = options(ix, ret["pool"])
    hits = [i for i, c in enumerate(pool_ids) if c in acceptable]
    if len(hits) == 1:
        target, outcome = opts[hits[0]], "positive"
    elif not hits:
        target, outcome = NONE, "candidate_none"
    else:
        target, outcome = None, "multi_positive"
    gold = trace.get("canonical_id")
    if outcome == "candidate_none":
        cause = "true_out_of_scope" if not acceptable else "retrieval_miss"
    else:
        cause = None
    meta = {
        "row_id": trace["row_id"], "kind": trace["example_type"], "k": len(pool_ids),
        "pool": pool_ids, "gold": sorted(acceptable),
    }
    trace = {
        **trace, "query": q, "acceptable_ids": sorted(acceptable), "candidate_ids": pool_ids,
        "candidate_positions": {c: i + 1 for i, c in enumerate(pool_ids)},
        "candidate_cosines": ret["cos"], "pool_source": ret["pool_source"],
        "gate_sections": ret["gates"], "gate_scores": ret["gate_scores"],
        "gold_flat_rank": ret["flat_rank"].get(ix.pos[gold]) if gold in ix.pos else None,
        "target_position": hits[0] + 1 if len(hits) == 1 else None,
        "outcome": outcome, "none_cause": cause,
        "doubt_ids_in_pool": sorted(set(pool_ids) & doubt),
    }
    return {"state": q,
            "questions": {"topic": {"type": "choice", "instructions": INSTR, "criteria": [*opts, NONE]}},
            "expected": {"topic": target} if target is not None else {}, "meta": meta, "_trace": trace}


def pools(args) -> None:
    embed = load_embed()
    ix = Index(embed)
    held = set(unseen_ids(ix))
    excl = np.asarray([i in held for i in ix.ids])
    out = []
    for n, e in enumerate(ix.entries):
        if e["id"] in held:
            continue
        for j, x in enumerate(e.get("examples", [])):
            t = ix.example_pos[(n, j)]
            r = ix.retrieve(ix.tv[t], mask_text=ix.self_mask(n, t), excluded=excl)
            out.append({"gold": e["id"], "q": x, "pool": [ix.ids[m] for m in r["pool"]], "cos": r["cos"],
                        "src": r["pool_source"], "gates": r["gates"]})
    wjl(W / "work/train_pools.jsonl", out)
    # Pairs that decide a label: every other candidate in a none-target row (if it answers, "none"
    # is false supervision) and every candidate ranked above gold (the hard negative Laya must reject).
    pairs = defaultdict(lambda: {"rows": 0, "none_rows": 0, "above_gold": 0, "samples": []})
    for r in out:
        g = r["gold"]
        gpos = r["pool"].index(g) if g in r["pool"] else None
        for p, c in enumerate(r["pool"]):
            if c == g or (gpos is not None and p > gpos):
                continue
            d = pairs[(g, c)]
            d["rows"] += 1
            d["none_rows"] += gpos is None
            d["above_gold"] += gpos is not None
            if len(d["samples"]) < 3:
                d["samples"].append(r["q"])
    todo = sorted(({"a": a, "b": b, **v} for (a, b), v in pairs.items()), key=lambda x: (-x["rows"], x["a"], x["b"]))
    wjl(W / "work/pairs_todo.jsonl", todo)
    pool_len = Counter(len(r["pool"]) for r in out)
    fill = sum("flat_fill" in r["src"] for r in out)
    none = sum(r["gold"] not in r["pool"] for r in out)
    rows_cov = np.cumsum([t["rows"] for t in todo])
    print(json.dumps({"held": len(held), "rows": len(out), "pool_len": dict(pool_len), "flat_fill_rows": fill,
                      "none_target_rows": none, "pairs": len(todo),
                      "rows_covered_by_top": {n: int(rows_cov[min(n, len(todo)) - 1]) for n in (300, 600, 900, 1200, 1800, 2400)},
                      "pair_row_total": int(rows_cov[-1])}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("pools", "build"))
    a = ap.parse_args()
    if a.cmd == "pools":
        pools(a)
    else:
        from build_splits import build  # noqa: E402  (second half lives in its own module)
        build(a)
