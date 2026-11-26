"""Pack authored rows with the FAQs a verifier must read: gold, acceptable, near_ids and the real top-5 pool.

    cd experiments/laya && uv run python ../../research_notes/dataset_final/tools/verify_digest.py
Writes work/verify_shard.<VERIFIER>.jsonl (rows grouped so no verifier checks its own model's rows).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dataset import W, Index, jl, load_embed  # noqa: E402

CUT = 170
# verifier -> authored files (cross-model: Gemini rows -> Grok/Haiku/Luna, Grok rows -> Gemini/Haiku)
PLAN = {
    "V-X1": ["G4"], "V-X2": ["G5"], "V-X3": ["G6"],
    "V-G4": ["X4"], "V-H2": ["X1"], "V-G5": ["X2"], "V-G6": ["X3"],
}


def short(view, i):
    s = view[i]["short"]
    return s if len(s) <= CUT else s[: CUT - 1] + "…"


def main() -> None:
    view = {json.loads(x)["id"]: json.loads(x) for x in (W / "inputs/kb_view.jsonl").read_text().splitlines()}
    ix = Index(load_embed())
    for verifier, authors in PLAN.items():
        rows = [r for a in authors for r in jl(W / f"authored/{a}.jsonl")]
        vecs = ix.embed([r["q"] for r in rows]) if rows else []
        out = []
        for r, v in zip(rows, vecs):
            pool = [ix.ids[n] for n in ix.retrieve(v)["pool"]]
            ids = list(dict.fromkeys([*(r.get("acceptable") or []), *([r["gold"]] if r.get("gold") else []),
                                      *(r.get("near_ids") or []), *pool]))
            out.append({"qid": r["qid"], "q": r["q"], "case": r["case"], "scenario": r["scenario"],
                        "gold": r.get("gold"), "acceptable": r.get("acceptable") or [], "near_ids": r.get("near_ids") or [],
                        "why": r.get("why", ""), "retrieved_pool": pool,
                        "faqs": {i: {"label": view[i]["label"], "short": short(view, i)} for i in ids if i in view},
                        "unknown_ids": [i for i in ids if i not in view]})
        p = W / f"work/verify_shard.{verifier}.jsonl"
        p.write_text("".join(json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "\n" for o in out))
        print(verifier, len(out), p.stat().st_size)


if __name__ == "__main__":
    main()
