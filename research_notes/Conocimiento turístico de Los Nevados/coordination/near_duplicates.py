"""Report example pairs of different entries with e5-base cosine >= 0.95 (contract rule 2).

Pairs listed in near_duplicates_reviewed.json (coordinator-reviewed as distinct intents) are kept in the
report with "reviewed": true; only unreviewed pairs need a decision. Writes near_duplicates.json. Run: cd experiments/laya && uv run python <this file>
"""

import json
from pathlib import Path

import unicodedata

import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
SECTIONS = HERE.parents[2] / "data/knowledge/sections"
THRESHOLD = 0.95


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.casefold().strip()) if unicodedata.category(c) != "Mn")


def key(a, b):
    return frozenset({(a[0], fold(a[1])), (b[0], fold(b[1]))})


def main():
    rows = [(e["id"], x) for f in sorted(SECTIONS.glob("*.json"))
            for e in json.loads(f.read_text(encoding="utf-8"))["entries"] for x in e["examples"]]
    model = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu")
    vec = model.encode([f"query: {x}" for _, x in rows], batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    ids = np.array([i for i, _ in rows])
    pairs = []
    for a in range(len(rows)):
        sims = vec[a + 1:] @ vec[a]
        for off in np.nonzero(sims >= THRESHOLD)[0]:
            b = a + 1 + off
            if ids[a] != ids[b]:
                pairs.append({"cosine": round(float(sims[off]), 3), "a": list(rows[a]), "b": list(rows[b])})
    reviewed_path = HERE / "near_duplicates_reviewed.json"
    reviewed = {key(r["a"], r["b"]) for r in json.loads(reviewed_path.read_text(encoding="utf-8"))} if reviewed_path.exists() else set()
    for p in pairs:
        p["reviewed"] = key(p["a"], p["b"]) in reviewed
    pairs.sort(key=lambda p: (p["reviewed"], -p["cosine"]))
    (HERE / "near_duplicates.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    open_pairs = sum(not p["reviewed"] for p in pairs)
    print(f"{len(rows)} examples, {len(pairs)} cross-entry pairs with cosine >= {THRESHOLD}, {open_pairs} unreviewed")


if __name__ == "__main__":
    main()
