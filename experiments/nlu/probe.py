"""Linear probe / centroid vs kNN on frozen embeddings (pseudo-dev split of pseudo_dev.py)."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from kb import Embedder, load_entries

entries = load_entries()
texts, owner, queries, gold = [], [], [], []
for i, e in enumerate(entries):
    for t in [e.label, *e.examples[:-2]]:
        texts.append(t); owner.append(i)
    queries += e.examples[-2:]; gold += [i] * len(e.examples[-2:])
owner, gold = np.array(owner), np.array(gold)
emb = Embedder("intfloat/multilingual-e5-base")
V, Q = emb.encode(texts), emb.encode(queries)
n = len(entries)
C = np.stack([V[owner == e].mean(0) for e in range(n)]); C /= np.linalg.norm(C, axis=1, keepdims=True)
print("centroid top1", np.mean((Q @ C.T).argmax(1) == gold))
for c in (1, 10, 50):
    lr = LogisticRegression(C=c, max_iter=300, n_jobs=8).fit(V, owner)
    print(f"logreg C={c} top1", np.mean(lr.predict(Q) == gold))
