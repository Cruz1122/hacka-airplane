"""Report exact and e5-cosine overlap between questions and text sources."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ROUTE = ROOT / "research_notes/curation_v2/tools/route_check.py"
THRESHOLD = 0.93


def norm(text: str) -> str:
    ascii_text = unicodedata.normalize("NFD", text.casefold()).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", ascii_text).strip()


def row_paths(path: Path) -> list[Path]:
    return sorted(path.glob("*.jsonl")) if path.is_dir() else [path]


def load_rows(paths: list[Path]) -> list[dict]:
    return [json.loads(line) for path in paths for line in path.read_text().splitlines() if line.strip()]


def corpus_examples(directory: Path) -> list[tuple[str, str]]:
    values = []
    for path in sorted(directory.glob("*.json")):
        section = json.loads(path.read_text())
        for entry in section.get("entries", []):
            values.extend((entry["id"], value) for value in entry.get("examples", []) if value)
    return values


def training_texts(paths: list[Path]) -> list[tuple[str, str]]:
    values = []
    for path in paths:
        for index, row in enumerate(load_rows([path])):
            owner = row.get("qid", row.get("meta", {}).get("entry_id", f"{path.name}:{index + 1}"))
            for text in [row.get("q", row.get("state", "")), *row.get("meta", {}).get("examples", [])]:
                if text:
                    values.append((str(owner), text))
    return values


def embedder():
    spec = importlib.util.spec_from_file_location("route_check_leak_v2", ROUTE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.embed


def compare(rows: list[dict], references: list[tuple[str, str]], source: str, encode) -> dict:
    queries = [row.get("q", row.get("state", "")) for row in rows]
    usable = [(i, query) for i, query in enumerate(queries) if query]
    normalized_refs: dict[str, str] = {}
    for owner, text in references:
        normalized_refs.setdefault(norm(text), owner)
    exact = {index: normalized_refs[norm(query)] for index, query in usable if norm(query) in normalized_refs}
    if usable and references:
        query_vectors = encode([query for _, query in usable])
        ref_vectors = encode([text for _, text in references])
        similarities = query_vectors @ ref_vectors.T
        best_positions = np.argmax(similarities, axis=1)
        best_values = similarities[np.arange(len(usable)), best_positions]
        cosine = {
            index: {"score": float(score), "owner": references[int(position)][0]}
            for (index, _), score, position in zip(usable, best_values, best_positions, strict=True)
            if float(score) >= THRESHOLD
        }
    else:
        cosine = {}
    flagged = sorted(set(exact) | set(cosine))
    rows_by_index = []
    for index in flagged:
        rows_by_index.append({
            "qid": rows[index].get("qid", f"row-{index + 1}"),
            "exact": index in exact,
            "cosine": round(cosine[index]["score"], 6) if index in cosine else None,
            "exact_owner": exact.get(index),
            "cosine_owner": cosine.get(index, {}).get("owner"),
        })
    return {
        "source": source,
        "reference_texts": len(references),
        "exact_count": len(exact),
        "cosine_ge_0_93_count": len(cosine),
        "union_count": len(flagged),
        "flagged": rows_by_index,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rows", type=Path, help="JSONL file or directory of JSONL files")
    parser.add_argument("--sections-before", type=Path)
    parser.add_argument("--sections-after", type=Path)
    parser.add_argument("--sections-dir", type=Path, help="Compatibility alias for one corpus")
    parser.add_argument("--train", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = load_rows(row_paths(args.rows))
    dropped = [row for row in rows if row.get("label_status") == "dropped"]
    rows = [row for row in rows if row.get("label_status") != "dropped"]
    sources = []
    if args.sections_dir:
        sources.append(("corpus", corpus_examples(args.sections_dir)))
    if args.sections_before:
        sources.append(("corpus_before", corpus_examples(args.sections_before)))
    if args.sections_after:
        sources.append(("corpus_after", corpus_examples(args.sections_after)))
    if args.train:
        sources.append(("training", training_texts(args.train)))
    if not sources:
        parser.error("supply --sections-dir, --sections-before, --sections-after, or --train")

    encode = embedder()
    by_source = [compare(rows, refs, name, encode) for name, refs in sources]
    all_flagged = {}
    for report in by_source:
        for item in report["flagged"]:
            all_flagged.setdefault(item["qid"], {})[report["source"]] = item
    report = {
        "input_rows_including_dropped": len(rows) + len(dropped),
        "dropped_by_label_status": [row.get("qid") for row in dropped],
        "rows_compared": len(rows),
        "threshold": THRESHOLD,
        "normalization": "casefold, NFD accent removal, ASCII, collapsed whitespace",
        "sources": by_source,
        "flagged_union_count": len(all_flagged),
        "flagged_union": [{"qid": qid, "matches": matches} for qid, matches in sorted(all_flagged.items())],
        "input_sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in row_paths(args.rows)},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"rows_compared": len(rows), "dropped": len(dropped), "flagged_union_count": len(all_flagged), "sources": [{k: v for k, v in source.items() if k != "flagged"} for source in by_source]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
