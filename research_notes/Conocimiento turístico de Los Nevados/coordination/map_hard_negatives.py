"""Map every invented hard negative to a real example of another entry (contract rule 3).

A hard negative must be an existing example of a different entry. For each one that is not, pick
the real example of another entry most similar to the entry's own examples (multilingual-e5-base
cosine to the entry centroid), preferring owners not already used by that entry: a hard negative is
a query that looks like this entry but belongs elsewhere. Many invented texts were unrelated
filler, so they only feed the near-miss list, not the choice.
Run on a corpus built WITHOUT hard_negative_map.json (move it aside, run coordinator_fixes.py).
Invented texts with no close real example (cosine < NEAR_MISS) are saved to near_miss_candidates.json
as uncovered on-topic questions for the Phase 2 near-miss evaluation set. Writes hard_negative_map.json
({entry_id: {invented: real}}), which coordinator_fixes.py applies, and hard_negative_review.json
(lowest similarities first) for the coordinator's manual check.

Run (needs sentence-transformers): cd experiments/laya && uv run python <this file>
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
SECTIONS = HERE.parents[2] / "data/knowledge/sections"
OUT = HERE / "hard_negative_map.json"
REVIEW = HERE / "hard_negative_review.json"
NEAR_MISS_OUT = HERE / "near_miss_candidates.json"
NEAR_MISS = 0.88


def main():
    entries = [e for f in sorted(SECTIONS.glob("*.json")) for e in json.loads(f.read_text(encoding="utf-8"))["entries"]]
    owner = {}
    for e in entries:
        for x in e["examples"]:
            owner.setdefault(x, e["id"])
    pool = list(owner)
    pool_owner = np.array([owner[x] for x in pool])
    invented = sorted({(e["id"], h) for e in entries for h in e.get("hard_negatives", []) if owner.get(h, e["id"]) == e["id"]})
    model = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu")
    enc = lambda xs: model.encode([f"query: {x}" for x in xs], batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    pool_vec = enc(pool)
    inv_vec = enc([h for _, h in invented])
    by_id = {e["id"]: e for e in entries}
    centroid = {}
    for e in entries:
        idx = [i for i, x in enumerate(pool) if owner[x] == e["id"]]
        c = pool_vec[idx].mean(axis=0)
        centroid[e["id"]] = c / np.linalg.norm(c)
    mapping, review, near_miss = {}, [], []
    for (eid, text), vec in zip(invented, inv_vec):
        entry = by_id[eid]
        taken = {h for h in entry["hard_negatives"] if owner.get(h, eid) != eid} | set(mapping.get(eid, {}).values())
        to_text = pool_vec @ vec
        if to_text[pool_owner != eid].max() < NEAR_MISS:
            near_miss.append({"from_entry": eid, "q": text})
        scores = pool_vec @ centroid[eid]
        scores[pool_owner == eid] = -9  # never an example of the entry itself
        used = {owner[h] for h in taken if h in owner}
        ranked = [i for i in np.argsort(-scores)[:200] if pool[i] not in taken]
        i = next((j for j in ranked if pool_owner[j] not in used), ranked[0])
        mapping.setdefault(eid, {})[text] = pool[i]
        review.append({"id": eid, "invented": text, "real": pool[i], "real_owner": str(pool_owner[i]), "cosine": round(float(to_text[i]), 3),
                       "to_entry": round(float(pool_vec[i] @ centroid[eid]), 3)})
    review.sort(key=lambda r: r["cosine"])
    OUT.write_text(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    NEAR_MISS_OUT.write_text(json.dumps(near_miss, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cos = np.array([r["cosine"] for r in review])
    print(f"mapped {len(review)} invented hard negatives; cosine min {cos.min():.3f} p10 {np.percentile(cos,10):.3f} median {np.median(cos):.3f}; near-miss candidates {len(near_miss)}")


if __name__ == "__main__":
    main()
