"""Report Phase 2 eval questions that are near-copies of training examples (e5-base cosine >= 0.95).

Rows tagged "near_copy": true are known near-copies kept for reference (each has a replacement row
"replaces_near_copy"); they are reported apart and excluded from the clean-subset count.
Writes eval_leakage.json. Run: cd experiments/laya && uv run python <this file>
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
THRESHOLD = 0.95


def main():
    examples = [(e["id"], x) for f in sorted((ROOT / "data/knowledge/sections").glob("*.json"))
                for e in json.loads(f.read_text(encoding="utf-8"))["entries"] for x in e["examples"]]
    rows = [(p.name, json.loads(line)) for p in sorted((ROOT / "data/knowledge/phase2/eval").glob("*.jsonl"))
            for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    model = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu")
    enc = lambda xs: model.encode([f"query: {x}" for x in xs], batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    ex_vec, q_vec = enc([x for _, x in examples]), enc([r["q"] for _, r in rows])
    hits = []
    for (name, row), vec in zip(rows, q_vec):
        sims = ex_vec @ vec
        i = int(sims.argmax())
        if sims[i] >= THRESHOLD:
            hits.append({"file": name, "q": row["q"], "expected": row["expected"], "near_copy": bool(row.get("near_copy")), "example": examples[i][1],
                         "example_owner": examples[i][0], "cosine": round(float(sims[i]), 3)})
    hits.sort(key=lambda h: -h["cosine"])
    (HERE / "eval_leakage.json").write_text(json.dumps(hits, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tagged = sum(h["near_copy"] for h in hits)
    print(f"{len(rows)} eval questions, {len(hits)} with an example at cosine >= {THRESHOLD} "
          f"({tagged} tagged near_copy, {len(hits) - tagged} in the clean subset)")


if __name__ == "__main__":
    main()
