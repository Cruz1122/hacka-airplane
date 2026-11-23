"""Phase 3 prep: e5-base baseline on the Phase 2 corpus and Laya fine-tune data (listwise choice).

  uv run python ft_data.py baseline   # e5-base on data/knowledge/phase2/eval -> results/p1-laya/p2_baseline.json
  uv run python ft_data.py build      # training rows + eval pools -> data/knowledge/laya_ft/

Reads data/knowledge/sections (Phase 2 output) and never writes there.
"""

from __future__ import annotations

import json
import random
import sys
import zipfile

import numpy as np
from exp import OUT, Embedder, Index, ci
from kb import ROOT, Entry, load_sections

SECTIONS = ROOT / "data/knowledge/sections"
EVAL2 = ROOT / "data/knowledge/phase2/eval"
FT = ROOT / "data/knowledge/laya_ft"
NONE = "ninguna de estas opciones"
INSTR = "¿Qué tema contesta la pregunta del visitante?"
HOLDOUT_FRAC = 0.10
SEED = 20261122


def load_eval2() -> list[dict]:
    rows = []
    for p in sorted(EVAL2.glob("*.jsonl")):
        kind = p.stem.split(".")[0]
        for line in p.read_text().splitlines():
            r = json.loads(line)
            if r.get("near_copy"):
                continue
            rows.append({"set": kind, "q": r["q"], "expected": r["expected"]})
    return rows


def build_index(emb: Embedder, entries: list[Entry]) -> Index:
    """Example vectors only (labels are included too), with owner and example position."""
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


def entry_scores(index: Index, sims: np.ndarray) -> np.ndarray:
    out = np.full(len(index.entries), -1.0, dtype=np.float32)
    np.maximum.at(out, np.asarray(index.owner), sims)
    return out


def coverage_at(items: list[tuple[float, bool, bool]], max_wrong: float = 0.03) -> dict:
    """items = (confidence, answered_correctly, in_domain). 2-fold CV threshold, OOD reported apart."""
    rng = random.Random(7)
    items = items[:]
    rng.shuffle(items)
    halves = [items[::2], items[1::2]]

    def stats(xs, t):
        ans = [x for x in xs if x[0] >= t]
        wrong = sum(not ok for _, ok, _ in ans)
        n_in = sum(1 for *_, i in xs if i)
        n_out = sum(1 for *_, i in xs if not i)
        ood_ans = sum(1 for c, _, i in xs if not i and c >= t)
        return (
            wrong / max(1, len(xs)),
            sum(ok for _, ok, _ in ans) / max(1, n_in),
            ood_ans / max(1, n_out),
        )

    def fit(xs):
        for t in sorted({x[0] for x in xs}):
            if stats(xs, t)[0] <= max_wrong:
                return t
        return float("inf")

    res = []
    for a, b in ((0, 1), (1, 0)):
        t = fit(halves[a])
        res.append((*stats(halves[b], t), t))
    ind = [c for c, _, i in items if i]
    out = [c for c, _, i in items if not i]
    auroc = float(np.mean([(a > b) + 0.5 * (a == b) for a in ind for b in out])) if out else None
    return {
        "auroc_in_vs_out": None if auroc is None else round(auroc, 4),
        "cv_wrong_rate": round(float(np.mean([r[0] for r in res])), 4),
        "cv_correct_coverage": round(float(np.mean([r[1] for r in res])), 4),
        "cv_ood_answered_rate": round(float(np.mean([r[2] for r in res])), 4),
        "thresholds": [round(r[3], 4) for r in res],
    }


def baseline() -> dict:
    _, entries = load_sections(SECTIONS)
    emb = Embedder("e5-base")
    index = build_index(emb, entries)
    ids = [e.id for e in entries]
    rows = load_eval2()
    qv = emb([r["q"] for r in rows], query=True)
    para = []
    items = []
    for r, v in zip(rows, qv, strict=True):
        s = entry_scores(index, index.vecs @ v)
        order = np.argsort(-s)
        top = [ids[i] for i in order[:5]]
        r["top5"], r["s1"], r["s2"] = top, float(s[order[0]]), float(s[order[1]])
        ok = top[0] in r["expected"]
        if r["set"] == "paraphrase":
            para.append(r)
        items.append((r["s1"], ok, r["set"] == "paraphrase"))
    n = len(para)
    rep = {
        "corpus": {"entries": len(entries), "examples": sum(len(e.examples) for e in entries)},
        "eval": {
            k: sum(r["set"] == k for r in rows) for k in ("paraphrase", "near_miss", "out_of_scope")
        },
        "top1": ci(sum(r["top5"][0] in r["expected"] for r in para), n),
        "recall3": ci(sum(bool(set(r["top5"][:3]) & set(r["expected"])) for r in para), n),
        "recall5": ci(sum(bool(set(r["top5"]) & set(r["expected"])) for r in para), n),
        "abstention_cos": coverage_at(items),
        "abstention_margin": coverage_at(
            [(r["s1"] - r["s2"], it[1], it[2]) for r, it in zip(rows, items, strict=True)]
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "p2_baseline.json").write_text(json.dumps(rep, indent=2))
    (OUT / "p2_baseline_rows.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    )
    return rep


def option_texts(cands: list[Entry]) -> list[str]:
    """Unique option text per candidate: the label, disambiguated by section title on collision."""
    seen: dict[str, int] = {}
    out = []
    for e in cands:
        t = e.label
        if t in seen or t == NONE:
            t = f"{e.label} ({e.section})"
        seen[t] = 1
        out.append(t)
    return out


def make_row(q: str, cands: list[Entry], gold: set[str], meta: dict) -> dict:
    texts = option_texts(cands)
    crit = [*texts, NONE]
    hit = [t for t, e in zip(texts, cands, strict=True) if e.id in gold]
    expected = hit[0] if hit else NONE
    return {
        "state": q,
        "questions": {"topic": {"type": "choice", "instructions": INSTR, "criteria": crit}},
        "expected": {"topic": expected},
        "meta": {**meta, "pool": [e.id for e in cands], "gold": sorted(gold)},
    }


def build() -> dict:
    _, entries = load_sections(SECTIONS)
    rng = random.Random(SEED)
    held = set(rng.sample([e.id for e in entries], round(HOLDOUT_FRAC * len(entries))))
    emb = Embedder("e5-base")
    index = build_index(emb, entries)
    owner = np.asarray(index.owner)
    train_entries = np.asarray([e.id not in held for e in entries])
    rows = []
    for vi, ex in enumerate(index.is_example):
        if ex is None:
            continue
        e = entries[ex[0]]
        if e.id in held:
            continue
        sims = index.vecs @ index.vecs[vi]
        sims[
            vi
        ] = -1.0  # mask the query's own vector, otherwise gold is always rank 1 at cosine 1.0
        # Held-out entries never appear in training pools.
        sims = np.where(train_entries[owner], sims, -1.0)
        s = entry_scores(index, sims)
        order = [i for i in np.argsort(-s) if train_entries[i]]
        k = rng.choice((3, 4, 5))
        q = e.examples[ex[1]]
        rows.append(
            make_row(q, [entries[i] for i in order[:k]], {e.id}, {"kind": "natural", "k": k})
        )
        # No extra "gold removed" rows: pools already miss gold ~28 % of the time naturally, and adding
        # more pushed the "none" target to 42 %, which teaches over-abstention.
    rng.shuffle(rows)
    # Eval pools: Phase 2 eval with pools from the full index (k = 5 and k = 3 are prefixes).
    ev = load_eval2()
    qv = emb([r["q"] for r in ev], query=True)
    eval_rows = []
    for r, v in zip(ev, qv, strict=True):
        s = entry_scores(index, index.vecs @ v)
        order = list(np.argsort(-s)[:5])
        cands = [entries[i] for i in order]
        row = make_row(r["q"], cands, set(r["expected"]), {"kind": r["set"], "k": 5})
        row["meta"]["cos"] = [float(s[i]) for i in order]
        row["meta"]["heldout_gold"] = bool(set(r["expected"]) & held)
        eval_rows.append(row)
    FT.mkdir(parents=True, exist_ok=True)
    # Dev slice of training rows for choosing epochs / base; never choose on the Phase 2 eval.
    dev, rows = rows[:450], rows[450:]
    (FT / "dev.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in dev))
    (FT / "train.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    (FT / "eval.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in eval_rows)
    )
    (FT / "heldout_entries.json").write_text(json.dumps(sorted(held), indent=1))
    stats = {
        "train_rows": len(rows),
        "dev_rows": len(dev),
        "train_none_target": sum(r["expected"]["topic"] == NONE for r in rows),
        "eval_rows": len(eval_rows),
        "eval_heldout_gold": sum(r["meta"]["heldout_gold"] for r in eval_rows),
        "heldout_entries": len(held),
        "max_options": max(len(r["questions"]["topic"]["criteria"]) for r in rows),
        "longest_option_chars": max(
            len(c) for r in rows for c in r["questions"]["topic"]["criteria"]
        ),
    }
    (FT / "stats.json").write_text(json.dumps(stats, indent=2))
    with zipfile.ZipFile(FT / "laya_ft.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in (
            "train.jsonl",
            "dev.jsonl",
            "eval.jsonl",
            "heldout_entries.json",
            "stats.json",
        ):
            z.write(FT / name, name)
    return stats


if __name__ == "__main__":
    cmd = sys.argv[1]
    print(json.dumps(baseline() if cmd == "baseline" else build(), indent=1, ensure_ascii=False))
