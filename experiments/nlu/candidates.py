"""Top-15 e5 candidates per blind query (labeling hints only; labelers also get the full catalog)."""
import json
import numpy as np
from kb import Embedder, load_entries, ROOT

W = ROOT / "experiments/nlu/work"
entries = load_entries()
texts, owner = [], []
for i, e in enumerate(entries):
    for t in [e.label, *e.examples]:
        texts.append(t); owner.append(i)
owner = np.array(owner)
emb = Embedder("intfloat/multilingual-e5-base")
V = emb.encode(texts)
rows = [json.loads(l) for l in open(W / "queries_raw.jsonl")]
qs = [" ".join(r["turns"]) for r in rows]  # conversations: whole context as the hint query
Q = emb.encode(qs)
sim = Q @ V.T
best = np.full((len(qs), len(entries)), -1.0)
np.maximum.at(best.T, owner, sim.T) if False else None
for e in range(len(entries)):
    best[:, e] = sim[:, owner == e].max(1)
with open(W / "queries_with_candidates.jsonl", "w") as f:
    for r, s in zip(rows, best):
        top = np.argsort(-s)[:15]
        r["candidates"] = [entries[i].id for i in top]
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("ok", len(rows))
