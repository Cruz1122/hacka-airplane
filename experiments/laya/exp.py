"""Phase 1 experiments E1-E6: embedding retrieval (flat vs gateway) and Laya as System 1.

  uv run python exp.py embed            # E1-E3 for every embedding model -> results/p1-laya/retrieval.json
  uv run python exp.py laya MODEL       # E4-E6 with the given embedding model -> results/p1-laya/laya_MODEL.json

Pool = candidate entries handed to System 1 (E3 soft gateway, top_k per section).
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
import torch
from kb import ROOT, Entry, load_sections

EVAL = ROOT / "data/knowledge/phase1/eval"
OUT = ROOT / "results/p1-laya"
torch.set_num_threads(4)

EMBEDDERS = {
    "e5-small": ("intfloat/multilingual-e5-small", "query: ", "query: "),
    "e5-base": ("intfloat/multilingual-e5-base", "query: ", "query: "),
    "minilm": ("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "", ""),
    "gemma": (
        "google/embeddinggemma-300m",
        "task: search result | query: ",
        "task: search result | query: ",
    ),
}

GATE_DELTA = 0.05  # sections within this similarity of the best one are opened
MAX_GATES = 5
TOP_K = 2


def load_eval(name: str) -> list[dict]:
    return [json.loads(line) for line in (EVAL / f"{name}.jsonl").read_text().splitlines()]


@dataclass
class Index:
    vecs: np.ndarray  # (n, d) normalized
    owner: list[int]  # entry index per vector
    is_example: list[tuple[int, int] | None]  # (entry, example idx) for example vectors
    entries: list[Entry]


class Embedder:
    def __init__(self, key: str):
        from sentence_transformers import SentenceTransformer

        name, self.qp, self.dp = EMBEDDERS[key]
        self.model = SentenceTransformer(name, device="cpu")

    def __call__(self, texts: list[str], query: bool) -> np.ndarray:
        p = self.qp if query else self.dp
        v = self.model.encode([p + t for t in texts], batch_size=64, normalize_embeddings=True)
        return np.asarray(v, dtype=np.float32)


def build_index(emb: Embedder, entries: list[Entry]) -> Index:
    texts, owner, ex = [], [], []
    for i, e in enumerate(entries):
        texts.append(e.label)
        owner.append(i)
        ex.append(None)
        for j, x in enumerate(e.examples):
            texts.append(x)
            owner.append(i)
            ex.append((i, j))
    return Index(emb(texts, query=False), owner, ex, entries)


def entry_scores(index: Index, q: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    sims = index.vecs @ q
    if mask is not None:
        sims = np.where(mask, sims, -1.0)
    out = np.full(len(index.entries), -1.0, dtype=np.float32)
    np.maximum.at(out, np.asarray(index.owner), sims)
    return out


def gateway(index: Index, scores: np.ndarray) -> list[tuple[str, float]]:
    """Section score = best entry score in the section. Returns open sections, best first."""
    by_sec: dict[str, float] = defaultdict(lambda: -1.0)
    for e, s in zip(index.entries, scores, strict=True):
        by_sec[e.section] = max(by_sec[e.section], float(s))
    ranked = sorted(by_sec.items(), key=lambda kv: -kv[1])
    top = ranked[0][1]
    return [kv for kv in ranked if kv[1] >= top - GATE_DELTA][:MAX_GATES]


def pool(index: Index, scores: np.ndarray, gates: list[tuple[str, float]]) -> list[int]:
    cands = []
    for sec, _ in gates:
        idx = [i for i, e in enumerate(index.entries) if e.section == sec]
        idx.sort(key=lambda i: -scores[i])
        cands += idx[:TOP_K]
    return sorted(cands, key=lambda i: -scores[i])


def queries(index: Index) -> dict[str, list[tuple[str, list[str], int | None]]]:
    """(text, expected ids, held-out vector index or None) per eval set."""
    sets: dict[str, list] = {}
    loo = []
    for vi, ex in enumerate(index.is_example):
        if ex is None:
            continue
        e = index.entries[ex[0]]
        loo.append((e.examples[ex[1]], [e.id], vi))
    sets["loo"] = loo
    for name in ("paraphrase", "out_of_scope", "near_miss", "multi_intent"):
        sets[name] = [(r["q"], r["expected"], None) for r in load_eval(name)]
    return sets


def retrieval(key: str) -> dict:
    _, entries = load_sections()
    emb = Embedder(key)
    t0 = time.perf_counter()
    index = build_index(emb, entries)
    build_s = time.perf_counter() - t0
    sets = queries(index)
    ids = [e.id for e in entries]
    # "Spider" gateway: one vector per section = normalized mean of its vectors + its description.
    sections, _ = load_sections()
    sec_names = sorted({e.section for e in entries})
    desc = emb([sections[n]["description"] for n in sec_names], query=False)
    cents = []
    for k, n in enumerate(sec_names):
        rows_n = [vi for vi, o in enumerate(index.owner) if entries[o].section == n]
        c = index.vecs[rows_n].mean(axis=0) + desc[k]
        cents.append(c / np.linalg.norm(c))
    cents = np.stack(cents)
    report: dict = {
        "model": EMBEDDERS[key][0],
        "vectors": len(index.owner),
        "index_build_s": round(build_s, 2),
    }
    lat = []
    rows = []
    for name, qs in sets.items():
        texts = [q for q, _, _ in qs]
        t0 = time.perf_counter()
        qv = emb(texts, query=True)
        lat.append((time.perf_counter() - t0) / len(texts))
        for (text, exp, held), v in zip(qs, qv, strict=True):
            mask = None
            if held is not None:
                mask = np.ones(len(index.owner), dtype=bool)
                mask[held] = False
            s = entry_scores(index, v, mask)
            order = np.argsort(-s)
            gates = gateway(index, s)
            hard_sec = gates[0][0]
            hard = max(
                (i for i, e in enumerate(entries) if e.section == hard_sec), key=lambda i: s[i]
            )
            p = pool(index, s, gates)
            cs = np.argsort(-(cents @ v))
            cen_hard_sec = sec_names[cs[0]]
            cen_hard = max(
                (i for i, e in enumerate(entries) if e.section == cen_hard_sec), key=lambda i: s[i]
            )
            cen3 = {sec_names[i] for i in cs[:3]}
            cen_pool = sorted(
                (i for i, e in enumerate(entries) if e.section in cen3), key=lambda i: -s[i]
            )[:5]
            rows.append(
                {
                    "set": name,
                    "q": text,
                    "expected": exp,
                    "flat_top": ids[order[0]],
                    "flat_top5": [ids[i] for i in order[:5]],
                    "s1": float(s[order[0]]),
                    "s2": float(s[order[1]]),
                    "hard_gate": ids[hard],
                    "gates": [g for g, _ in gates],
                    "pool": [ids[i] for i in p],
                    "pool_scores": [float(s[i]) for i in p],
                    "cen_hard": ids[cen_hard],
                    "cen_pool": [ids[i] for i in cen_pool],
                    "cen_top_section_ok": any(
                        by == cen_hard_sec for by in [x.split(".")[0] for x in exp]
                    ),
                }
            )
    report["embed_ms_per_query"] = round(1000 * float(np.mean(lat)), 2)
    report["metrics"] = summarize(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"rows_{key}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    )
    return report


def summarize(rows: list[dict]) -> dict:
    m: dict = {}
    for name in ("loo", "paraphrase"):
        rs = [r for r in rows if r["set"] == name]
        n = len(rs)
        m[name] = {
            "n": n,
            "E1_flat_top1": ci(sum(r["flat_top"] in r["expected"] for r in rs), n),
            "E1_flat_recall5": ci(
                sum(bool(set(r["flat_top5"]) & set(r["expected"])) for r in rs), n
            ),
            "E2_hard_gate_top1": ci(sum(r["hard_gate"] in r["expected"] for r in rs), n),
            "E2b_centroid_gate_section_acc": ci(sum(r["cen_top_section_ok"] for r in rs), n),
            "E2b_centroid_hard_top1": ci(sum(r["cen_hard"] in r["expected"] for r in rs), n),
            "E3b_centroid_top3_pool5_recall": ci(
                sum(bool(set(r["cen_pool"]) & set(r["expected"])) for r in rs), n
            ),
            "E3_pool_recall": ci(sum(bool(set(r["pool"]) & set(r["expected"])) for r in rs), n),
            "E3_pool_size_mean": round(float(np.mean([len(r["pool"]) for r in rs])), 2),
            "E3_gates_mean": round(float(np.mean([len(r["gates"]) for r in rs])), 2),
        }
    mi = [r for r in rows if r["set"] == "multi_intent"]
    m["multi_intent"] = {
        "n": len(mi),
        "both_in_flat_top5": sum(set(r["expected"]) <= set(r["flat_top5"]) for r in mi),
        "both_in_pool": sum(set(r["expected"]) <= set(r["pool"]) for r in mi),
    }
    m["abstention_emb"] = abstention(rows, conf=lambda r: r["s1"], pick=lambda r: r["flat_top"])
    m["abstention_emb_margin"] = abstention(
        rows, conf=lambda r: r["s1"] - r["s2"], pick=lambda r: r["flat_top"]
    )
    return m


def ci(k: int, n: int) -> dict:
    """Wilson 95 % interval."""
    if n == 0:
        return {"rate": None}
    p, z = k / n, 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "rate": round(p, 4), "lo": round(c - h, 4), "hi": round(c + h, 4)}


def abstention(rows: list[dict], conf, pick, max_wrong: float = 0.03) -> dict:
    """In-domain = paraphrase; out = out_of_scope + near_miss.

    Answering an out-of-domain question or picking the wrong entry counts as wrong. Reports AUROC
    (in vs out by confidence) and the coverage at <= 3 % wrong answers, with the threshold chosen by
    2-fold cross-validation (fit on one half, measured on the other, averaged).
    """
    ind = [r for r in rows if r["set"] == "paraphrase"]
    out = [r for r in rows if r["set"] in ("out_of_scope", "near_miss")]
    ci_, co = [conf(r) for r in ind], [conf(r) for r in out]
    auroc = float(np.mean([(a > b) + 0.5 * (a == b) for a in ci_ for b in co]))
    items = [(conf(r), pick(r) in r["expected"], True) for r in ind] + [
        (conf(r), False, False) for r in out
    ]
    rng = random.Random(7)
    rng.shuffle(items)
    halves = [items[::2], items[1::2]]

    def stats(xs, t):
        ans = [x for x in xs if x[0] >= t]
        wrong = sum(not ok for _, ok, _ in ans)
        n_in = sum(isin for *_, isin in xs)
        correct = sum(ok for _, ok, _ in ans)
        return wrong / max(1, len(xs)), correct / max(1, n_in)

    def fit(xs):
        best = math.inf
        for t in sorted({x[0] for x in xs}):
            if stats(xs, t)[0] <= max_wrong:
                return t
        return best

    res = []
    for a, b in ((0, 1), (1, 0)):
        t = fit(halves[a])
        res.append((*stats(halves[b], t), t))
    return {
        "auroc_in_vs_out": round(auroc, 4),
        "cv_wrong_rate": round(float(np.mean([r[0] for r in res])), 4),
        "cv_correct_coverage": round(float(np.mean([r[1] for r in res])), 4),
        "thresholds": [round(r[2], 4) for r in res],
    }


# ---------------------------------------------------------------- Laya (System 1)

LAYA_ID = "telepatia-ai/laya-pt-es-nli"
NLI_CRITERIA = {
    "contradiction": "el estado hace falsa la hipótesis",
    "entailment": "el estado confirma la hipótesis",
    "neutral": "el estado no confirma ni contradice la hipótesis",
}


def nli_question(hyp: str) -> dict:
    return {
        "type": "choice",
        "instructions": f"¿Cuál es la relación lógica entre el estado y la hipótesis: {hyp}",
        "criteria": NLI_CRITERIA,
    }


def load_laya():
    import laya

    return laya.load(LAYA_ID, device="cpu", vegaml=False)


def p_entail(res: dict, qid: str) -> float:
    return float(res["answers"][qid]["probabilities"]["entailment"])


def laya_run(key: str, limit: int | None = None) -> dict:
    _, entries = load_sections()
    by_id = {e.id: e for e in entries}
    rows = [json.loads(x) for x in (OUT / f"rows_{key}.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["set"] != "loo"]
    if limit:
        rows = rows[:limit]
    agent = load_laya()
    agent.system_one("hola", {"w": nli_question("El visitante saluda.")})  # warm-up
    lat_label, lat_choice = [], []
    for r in rows:
        cands = r["pool"]
        # E4a: hypothesis from the entry label.
        qs = {
            f"c{i}": nli_question(f"El visitante pregunta sobre {by_id[c].label}.")
            for i, c in enumerate(cands)
        }
        t0 = time.perf_counter()
        res = agent.system_one(r["q"], qs)
        lat_label.append(time.perf_counter() - t0)
        r["laya_label"] = [p_entail(res, f"c{i}") for i in range(len(cands))]
        # E4b: hypothesis from the closest example of each candidate (paraphrase test).
        best_ex = []
        for c in cands:
            best_ex.append(
                by_id[c].examples[0] if not by_id[c].examples else _closest(r["q"], by_id[c])
            )
        qs = {f"c{i}": nli_question(f"El visitante pregunta: {x}") for i, x in enumerate(best_ex)}
        res = agent.system_one(r["q"], qs)
        r["laya_example"] = [p_entail(res, f"c{i}") for i in range(len(cands))]
        # E5: one choice question over labels plus "none".
        crit = {c: by_id[c].label for c in cands}
        crit["none"] = "ninguno de estos temas"
        t0 = time.perf_counter()
        res = agent.system_one(
            r["q"],
            {
                "topic": {
                    "type": "choice",
                    "instructions": "¿Sobre qué tema pregunta el visitante?",
                    "criteria": crit,
                }
            },
        )
        lat_choice.append(time.perf_counter() - t0)
        probs = res["answers"]["topic"]["probabilities"]
        r["laya_choice"] = [float(probs[c]) for c in cands]
        r["laya_choice_none"] = float(probs["none"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"laya_rows_{key}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    )
    rep = {
        "embedder": key,
        "laya": LAYA_ID,
        "pool_max": max(len(r["pool"]) for r in rows),
        "latency_ms": {
            "nli_label_pool_p50": pct(lat_label, 50),
            "nli_label_pool_p95": pct(lat_label, 95),
            "choice_p50": pct(lat_choice, 50),
            "choice_p95": pct(lat_choice, 95),
        },
        "metrics": laya_summary(rows),
    }
    return rep


_EMB_CACHE: dict = {}


def _closest(q: str, e: Entry) -> str:
    """Pick the example of e most similar to q with the small e5 model (cheap, cached)."""
    if "emb" not in _EMB_CACHE:
        _EMB_CACHE["emb"] = Embedder("e5-small")
    emb = _EMB_CACHE["emb"]
    key = e.id
    if key not in _EMB_CACHE:
        _EMB_CACHE[key] = emb(list(e.examples), query=False)
    qv = emb([q], query=True)[0]
    return e.examples[int(np.argmax(_EMB_CACHE[key] @ qv))]


def pct(xs: list[float], p: int) -> float:
    return round(1000 * float(np.percentile(xs, p)), 1)


def laya_summary(rows: list[dict]) -> dict:
    out: dict = {}
    variants = {
        "E3_emb_only": (lambda r: r["pool_scores"], lambda r: r["pool_scores"][0]),
        "E4a_nli_label": (lambda r: r["laya_label"], None),
        "E4b_nli_example": (lambda r: r["laya_example"], None),
        "E5_choice": (lambda r: r["laya_choice"], None),
        "E4a+emb": (
            lambda r: [a + b for a, b in zip(r["laya_label"], r["pool_scores"], strict=True)],
            None,
        ),
        "E4b+emb": (
            lambda r: [a + b for a, b in zip(r["laya_example"], r["pool_scores"], strict=True)],
            None,
        ),
    }
    para = [r for r in rows if r["set"] == "paraphrase"]
    for name, (score, _) in variants.items():
        picks = lambda r, score=score: r["pool"][int(np.argmax(score(r)))]  # noqa: E731
        top1 = ci(sum(picks(r) in r["expected"] for r in para), len(para))
        tagged = [dict(r, _pick=picks(r), _conf=float(max(score(r)))) for r in rows]
        ab = abstention(tagged, conf=lambda r: r["_conf"], pick=lambda r: r["_pick"])
        mi = [r for r in rows if r["set"] == "multi_intent"]
        both_top2 = sum(
            set(r["expected"]) <= {r["pool"][i] for i in np.argsort(score(r))[::-1][:2]} for r in mi
        )
        out[name] = {
            "paraphrase_top1": top1,
            "abstention": ab,
            "multi_intent_both_top2": f"{both_top2}/{len(mi)}",
        }
    # E6: Laya choice with an explicit "none" option as the abstention signal.
    tagged = [
        dict(r, _pick=r["pool"][int(np.argmax(r["laya_choice"]))], _conf=1 - r["laya_choice_none"])
        for r in rows
    ]
    out["E6_choice_none_gate"] = {
        "abstention": abstention(tagged, conf=lambda r: r["_conf"], pick=lambda r: r["_pick"])
    }
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True)
    if cmd == "embed":
        keys = sys.argv[2:] or list(EMBEDDERS)
        allrep = {}
        for k in keys:
            try:
                allrep[k] = retrieval(k)
                print(k, json.dumps(allrep[k]["metrics"]["paraphrase"]), flush=True)
            except Exception as exc:  # gated or missing model: record and continue
                allrep[k] = {"error": f"{type(exc).__name__}: {exc}"[:400]}
                print(k, "ERROR", allrep[k]["error"], flush=True)
        (OUT / "retrieval.json").write_text(json.dumps(allrep, ensure_ascii=False, indent=2))
    elif cmd == "laya":
        key = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
        rep = laya_run(key, limit)
        (OUT / f"laya_{key}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2))
        print(json.dumps(rep, ensure_ascii=False, indent=1))
