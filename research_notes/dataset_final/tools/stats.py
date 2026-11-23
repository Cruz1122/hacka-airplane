"""Dataset statistics for QUALITY_REPORT.md (reads the built package, writes work/stats.json).

    cd experiments/laya && uv run python ../../research_notes/dataset_final/tools/stats.py [--recall]
--recall also computes e5 retrieval Recall@1/3/5 on the held-out splits, before vs after corpus.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dataset import ROOT, W  # noqa: E402

PKG = W / "out/LOS_NEVADOS_LAYA_FINAL_DATASET"
SPLITS = {
    "train": "train/train.jsonl", "checkpoint_selection": "validation/checkpoint_selection.jsonl",
    "calibration": "validation/calibration.jsonl", "unseen_topics": "validation/unseen_topics.jsonl",
    "adversarial": "evaluation/adversarial.jsonl", "final_test": "evaluation/final_test_SEALED.jsonl",
    "retrospective_READ_ONLY": "evaluation/retrospective_test_blind_READ_ONLY.jsonl",
}
NONE = "ninguna de estas opciones"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recall", action="store_true")
    a = ap.parse_args()
    meta = {m["row_id"]: m for m in jl(PKG / "train/metadata.jsonl")}
    out = {}
    for s, rel in SPLITS.items():
        rows = jl(PKG / rel)
        tr = [meta[r["meta"]["row_id"]] if s == "train" else r["meta"] for r in rows]
        pos = Counter()
        for r in rows:
            t = r["expected"].get("topic")
            if t and t != NONE:
                pos[r["questions"]["topic"]["criteria"].index(t) + 1] += 1
        sec = Counter((m.get("canonical_id") or "none.").split(".")[0] for m in tr)
        out[s] = {
            "rows": len(rows),
            "outcome": dict(Counter(m["outcome"] for m in tr)),
            "none_cause": dict(Counter(m.get("none_cause") for m in tr if m["outcome"] == "candidate_none")),
            "target_position": dict(sorted(pos.items())),
            "pool_size": dict(sorted(Counter(len(r["meta"]["pool"]) for r in rows).items())),
            "flat_fill_rows": sum("flat_fill" in m["pool_source"] for m in tr),
            "provenance": dict(Counter(m.get("provenance") for m in tr)),
            "review_status": dict(Counter(m.get("review_status") for m in tr)),
            "scenario": dict(Counter(m.get("scenario") for m in tr).most_common(20)),
            "sections": dict(sorted(sec.items())),
            "distinct_canonical_faqs": len({m.get("canonical_id") for m in tr if m.get("canonical_id")}),
            "verified_hard_negatives_rows": sum(bool(m.get("verified_hard_negatives_in_pool")) for m in tr),
            "rows_with_judged_distinct_pair": sum(any(str(v) == "judged:distinct" for v in (m.get("pair_status") or {}).values()) for m in tr),
        }
    if a.recall:
        out["retrieval_recall"] = recall()
    (W / "work/stats.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({s: {k: v[k] for k in ("rows", "outcome", "target_position")} for s, v in out.items() if s in SPLITS},
                     ensure_ascii=False))
    if a.recall:
        print(json.dumps(out["retrieval_recall"], ensure_ascii=False))


def recall() -> dict:
    """Recall@k of the app retrieval on authored held-out rows + retrospective, before vs after corpus."""
    import importlib.util  # noqa: PLC0415

    from build_dataset import Index, load_embed  # noqa: PLC0415
    import build_dataset as bd  # noqa: PLC0415

    embed = load_embed()
    rows = []
    for s in ("checkpoint_selection", "calibration", "final_test", "adversarial", "retrospective_READ_ONLY"):
        for r in jl(PKG / SPLITS[s]):
            acc = set(r["meta"].get("acceptable_ids") or [])
            if acc and r["meta"].get("outcome") in ("positive", "candidate_none", "multi_positive"):
                rows.append((s, r["state"], acc))
    vecs = embed([q for _, q, _ in rows])
    res = {}
    for label, sec_dir in (("after_final_phase", ROOT / "data/knowledge/sections"),
                           ("before_final_phase", W / "snapshots/sections_before_final"),
                           ("before_curation_v2", ROOT / "research_notes/curation_v2/snapshots/sections_before")):
        if not sec_dir.exists():
            continue
        bd.SECTIONS = sec_dir
        ix = Index(embed)
        hits = defaultdict(lambda: Counter())
        for (s, _, acc), v in zip(rows, vecs, strict=True):
            pool = [ix.ids[n] for n in ix.retrieve(v)["pool"]]
            known = acc & set(ix.ids)
            if not known:
                continue
            h = hits[s]
            h["n"] += 1
            for k in (1, 3, 5):
                h[f"r@{k}"] += bool(known & set(pool[:k]))
        res[label] = {s: {k: round(v / h["n"], 4) if k != "n" else v for k, v in h.items()} for s, h in hits.items()}
    bd.SECTIONS = ROOT / "data/knowledge/sections"
    return res


if __name__ == "__main__":
    main()
