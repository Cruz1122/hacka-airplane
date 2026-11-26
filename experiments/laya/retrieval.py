"""Shared e5-base retrieval for curation-v2 evaluation and training rows."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ROUTE_CHECK = ROOT / "research_notes/curation_v2/tools/route_check.py"
MODEL = "intfloat/multilingual-e5-base"
DELTA = 0.05
MAX_SECTIONS = 5


@dataclass
class Candidate:
    id: str
    section: str
    label: str
    score: float
    rank: int = 0


class Retriever:
    def __init__(self, sections_dir: str | Path, *, embedder=None):
        self.sections_dir = Path(sections_dir)
        self.sections: dict[str, dict] = {}
        self.entries: list[dict] = []
        for path in sorted(self.sections_dir.glob("*.json")):
            section = json.loads(path.read_text())
            name = section.get("id", path.stem)
            self.sections[name] = section
            for entry in section.get("entries", []):
                if entry.get("audience", "visitor") == "visitor":
                    self.entries.append({**entry, "section": name})
        if embedder is None:
            spec = importlib.util.spec_from_file_location("route_check_v2", ROUTE_CHECK)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            embedder = mod.embed
        self.embed = embedder
        self.ids = [e["id"] for e in self.entries]
        self.id_pos = {eid: i for i, eid in enumerate(self.ids)}
        self.entry_vecs: list[np.ndarray] = []
        self.section_vecs: dict[str, np.ndarray] = {}
        self._index()

    def _index(self):
        texts, owners, sections = [], [], []
        for i, e in enumerate(self.entries):
            texts.extend([e["label"], *e.get("examples", [])])
            owners.extend([i] * (1 + len(e.get("examples", []))))
            sections.extend([e["section"]] * (1 + len(e.get("examples", []))))
        descs = {s: data.get("description", "") for s, data in self.sections.items()}
        all_texts = texts + [descs[s] for s in self.sections]
        vectors = self.embed(all_texts)
        self.text_vectors = vectors[:len(texts)]
        self.owners = np.asarray(owners, dtype=np.int32)
        self.section_vectors = {s: [] for s in self.sections}
        for v, s in zip(vectors[len(texts):], self.sections, strict=True):
            self.section_vectors[s].append(v)
        # Labels/examples plus description all contribute to gateway section score.
        for v, s in zip(self.text_vectors, sections, strict=True):
            self.section_vectors[s].append(v)
        self.section_vecs = {s: np.stack(vs) for s, vs in self.section_vectors.items() if vs}

    def score(self, query_vector: np.ndarray, mask_vector: int | None = None) -> np.ndarray:
        sims = self.text_vectors @ query_vector
        if mask_vector is not None:
            sims[mask_vector] = -1.0
        scores = np.full(len(self.entries), -1.0, dtype=np.float32)
        np.maximum.at(scores, self.owners, sims)
        return scores

    def retrieve(self, query_vector: np.ndarray, *, mode="gateway", k=5, mask_vector=None,
                 tau_gate=-1.0, delta=DELTA) -> dict:
        scores = self.score(query_vector, mask_vector)
        if mode == "flat":
            pool_idx = np.argsort(-scores, kind="stable")[:k].tolist()
            gates = []
        elif mode == "gateway":
            section_scores = {
                s: float(np.max(vecs @ query_vector)) for s, vecs in self.section_vecs.items()
            }
            ranked_sections = sorted(section_scores.items(), key=lambda x: (-x[1], x[0]))
            top = ranked_sections[0][1] if ranked_sections else -1.0
            gates = [(s, sc) for s, sc in ranked_sections
                     if sc >= max(tau_gate, top - delta)][:MAX_SECTIONS]
            by_section = {s: [] for s, _ in gates}
            for i, entry in enumerate(self.entries):
                if entry["section"] in by_section:
                    by_section[entry["section"]].append(i)
            pool_idx = []
            for section, _ in gates:
                limit = int(self.sections[section].get("retrieval", {}).get("top_k", 2))
                pool_idx.extend(sorted(by_section[section], key=lambda i: (-scores[i], self.ids[i]))[:limit])
            pool_idx = sorted(pool_idx, key=lambda i: (-scores[i], self.ids[i]))[:k]
        else:
            raise ValueError(f"unknown retrieval mode: {mode}")
        candidates = [Candidate(self.ids[i], self.entries[i]["section"],
                                self.entries[i]["label"], float(scores[i])) for i in pool_idx]
        for rank, candidate in enumerate(candidates, 1):
            candidate.rank = rank
        return {"candidates": candidates, "gates": gates, "scores": scores}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sections_dir", type=Path)
    ap.add_argument("query")
    ap.add_argument("--mode", choices=("flat", "gateway"), default="gateway")
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()
    retriever = Retriever(args.sections_dir)
    qv = retriever.embed([args.query])[0]
    result = retriever.retrieve(qv, mode=args.mode, k=args.k)
    print(json.dumps({"sections": result["gates"], "pool": [c.__dict__ for c in result["candidates"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
