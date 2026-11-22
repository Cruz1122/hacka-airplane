"""Export train-side questions as single-choice Laya rows with the app retrieval pool."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from leak_check import compare, embedder, load_rows
from retrieval import ROOT, Retriever

NONE = "ninguna de estas opciones"
INSTRUCTIONS = "¿Qué tema contesta la pregunta del visitante?"
SEED = 20261122


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_audit(path: Path) -> dict[str, set[str]]:
    accepted: dict[str, set[str]] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        labels = set(record.get("acceptable_ids", []))
        for gold in record.get("canonical_gold", []):
            accepted.setdefault(gold, {gold}).update(labels)
    return accepted


def label_for(candidate, used: set[str]) -> str:
    label = candidate.label
    if label in used or label == NONE:
        label = f"{label} ({candidate.section})"
    used.add(label)
    return label


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sections_dir", type=Path)
    parser.add_argument("train_rows", type=Path, help="Train-only source JSONL, normally train_core.jsonl")
    parser.add_argument("--audit", type=Path, default=ROOT / "research_notes/curation_v2/audit/label_audit.jsonl")
    parser.add_argument("--test-blind", type=Path, required=True)
    parser.add_argument("--corpus-manifest", type=Path, default=ROOT / "research_notes/curation_v2/snapshots/sections_after.sha256.json")
    parser.add_argument("--out", type=Path, default=ROOT / "data/knowledge/laya_ft_v2")
    args = parser.parse_args()

    source_rows = load_rows([args.train_rows])
    audited_acceptables = load_audit(args.audit)
    retriever = Retriever(args.sections_dir)
    vectors = retriever.embed([row.get("state", row.get("q", "")) for row in source_rows])
    exported = []
    skipped_short_pool = 0
    audit_verified = 0
    for row, vector in zip(source_rows, vectors, strict=True):
        meta = row.get("meta", {})
        gold = set(meta.get("gold", []))
        acceptable = set().union(*(audited_acceptables.get(item, {item}) for item in gold)) if gold else set()
        if any(item in audited_acceptables for item in gold):
            audit_verified += 1
            label_origin = "verified"
        else:
            label_origin = "synthetic"
        retrieval = retriever.retrieve(vector, mode="gateway", k=5, tau_gate=-1.0, delta=0.05)
        candidates = retrieval["candidates"]
        if not 3 <= len(candidates) <= 5:
            skipped_short_pool += 1
            continue
        used: set[str] = set()
        options = [label_for(candidate, used) for candidate in candidates]
        target = next((option for option, candidate in zip(options, candidates, strict=True) if candidate.id in acceptable), NONE)
        exported.append({
            "state": row.get("state", row.get("q", "")),
            "questions": {"topic": {"type": "choice", "instructions": INSTRUCTIONS, "criteria": [*options, NONE]}},
            "expected": {"topic": target},
            "meta": {
                "format": "choice",
                "label_origin": label_origin,
                "acceptable_ids": sorted(acceptable),
                "gold_ids": sorted(gold),
                "candidate_ids": [candidate.id for candidate in candidates],
                "candidate_cosines": [round(candidate.score, 6) for candidate in candidates],
                "gate_sections": [section for section, _ in retrieval["gates"]],
                "kind": meta.get("kind", "unknown"),
            },
        })

    random.Random(SEED).shuffle(exported)
    dev_count = round(len(exported) * 0.05)
    dev_rows, train = exported[:dev_count], exported[dev_count:]
    args.out.mkdir(parents=True, exist_ok=True)
    train_path, dev_path = args.out / "train.jsonl", args.out / "dev.jsonl"
    train_path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in train))
    dev_path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in dev_rows))

    leak = compare(load_rows([args.test_blind]), [(str(index), row["state"]) for index, row in enumerate(exported)], "ft_v2", embedder())
    leak_path = args.out / "test_blind_leak_check.json"
    leak_path.write_text(json.dumps(leak, indent=2, ensure_ascii=False) + "\n")
    manifest = {
        "seed": SEED,
        "format": "single choice, 3-5 FAQ options plus 'ninguna de estas opciones'",
        "retrieval": {"embedding": "intfloat/multilingual-e5-base", "query_prefix": "query: ", "mode": "gateway", "k": 5, "delta": 0.05, "max_sections": 5, "tau_gate": -1.0},
        "input": {"path": str(args.train_rows), "sha256": sha256(args.train_rows), "rows": len(source_rows)},
        "audit": {"path": str(args.audit), "sha256": sha256(args.audit), "verified_rows_before_pool_filter": audit_verified},
        "corpus": {"path": str(args.corpus_manifest), "manifest_sha256": sha256(args.corpus_manifest)},
        "counts": {"train": len(train), "dev": len(dev_rows), "exported": len(exported), "skipped_pool_outside_3_to_5": skipped_short_pool},
        "label_origin_counts": {"verified": sum(row["meta"]["label_origin"] == "verified" for row in exported), "synthetic": sum(row["meta"]["label_origin"] == "synthetic" for row in exported)},
        "test_blind_leak_check": {"path": str(leak_path), "sha256": sha256(leak_path), "exact_count": leak["exact_count"], "cosine_ge_0_93_count": leak["cosine_ge_0_93_count"], "union_count": leak["union_count"]},
        "files_sha256": {train_path.name: sha256(train_path), dev_path.name: sha256(dev_path)},
        "training_note": "Export only; no model training was run.",
    }
    (args.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(manifest["counts"] | {"label_origin_counts": manifest["label_origin_counts"], "test_blind_leak_check": manifest["test_blind_leak_check"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
