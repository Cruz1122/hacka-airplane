"""Create a deterministic family-disjoint dev_gate/test_blind split."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = 20261122


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(paths: list[Path]) -> list[tuple[Path, dict]]:
    return [(path, json.loads(line)) for path in paths for line in path.read_text().splitlines() if line.strip()]


def counts(rows: list[dict], key: str) -> dict[str, int]:
    return dict(sorted(Counter(row.get(key, "unknown") for row in rows).items()))


def filter_verified(rows: list[tuple[Path, dict]], leaked_ids: set[str]):
    dropped = [item for item in rows if item[1].get("label_status") == "dropped"]
    verified = [item for item in rows if item[1].get("label_status") != "dropped"]
    leaked = [item for item in verified if item[1].get("qid") in leaked_ids]
    eligible = [item for item in verified if item[1].get("qid") not in leaked_ids]
    return eligible, dropped, leaked


def split(rows: list[tuple[Path, dict]], dev_fraction: float, seed: int):
    families = sorted({row["family"] for _, row in rows})
    random.Random(seed).shuffle(families)
    dev_count = max(1, round(len(families) * dev_fraction)) if families else 0
    dev_families = set(families[:dev_count])
    dev = [item for item in rows if item[1]["family"] in dev_families]
    test = [item for item in rows if item[1]["family"] not in dev_families]
    return dev, test


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rows", type=Path, help="Frozen verified.jsonl")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--dev-fraction", type=float, default=0.25)
    parser.add_argument("--leak-report", type=Path, required=True)
    parser.add_argument("--before-manifest", type=Path, default=ROOT / "research_notes/curation_v2/snapshots/sections_before.sha256.json")
    parser.add_argument("--after-manifest", type=Path, default=ROOT / "research_notes/curation_v2/snapshots/sections_after.sha256.json")
    args = parser.parse_args()

    raw = load_rows([args.rows])
    leak_data = json.loads(args.leak_report.read_text())
    leaked_ids = {item["qid"] for item in leak_data.get("flagged_union", [])}
    eligible, dropped, leaked = filter_verified(raw, leaked_ids)
    dev, test = split(eligible, args.dev_fraction, SEED)

    args.out.mkdir(parents=True, exist_ok=True)
    output_hashes = {}
    for name, subset in (("dev_gate", dev), ("test_blind", test)):
        output = args.out / f"{name}.jsonl"
        output.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for _, row in subset))
        output_hashes[output.name] = sha256(output)

    dev_families = {row["family"] for _, row in dev}
    test_families = {row["family"] for _, row in test}
    manifest = {
        "seed": SEED,
        "dev_fraction_of_families": args.dev_fraction,
        "input": {"path": str(args.rows), "sha256": sha256(args.rows), "line_count": len(raw)},
        "label_status_filter": {"excluded_status": "dropped", "excluded_qids": [row.get("qid") for _, row in dropped]},
        "leak_exclusion": {"report": str(args.leak_report), "report_sha256": sha256(args.leak_report), "excluded_qids": [row.get("qid") for _, row in leaked], "excluded_count": len(leaked)},
        "eligible_rows": len(eligible),
        "eligible_families": len(dev_families | test_families),
        "dev_gate": {"rows": len(dev), "families": sorted(dev_families), "by_case": counts([row for _, row in dev], "case"), "by_scenario": counts([row for _, row in dev], "scenario")},
        "test_blind": {"rows": len(test), "families": sorted(test_families), "by_case": counts([row for _, row in test], "case"), "by_scenario": counts([row for _, row in test], "scenario")},
        "family_disjoint": not bool(dev_families & test_families),
        "corpus_hashes": {
            "before": {"manifest_path": str(args.before_manifest), "manifest_sha256": sha256(args.before_manifest), "files": json.loads(args.before_manifest.read_text()).get("files", {})},
            "after": {"manifest_path": str(args.after_manifest), "manifest_sha256": sha256(args.after_manifest), "files": json.loads(args.after_manifest.read_text()).get("files", {})},
        },
        "outputs_sha256": output_hashes,
    }
    if not manifest["family_disjoint"]:
        raise RuntimeError("family split is not disjoint")
    (args.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"eligible_rows": len(eligible), "dropped_marker_rows": len(dropped), "leaked_rows_excluded": len(leaked), "dev_gate_rows": len(dev), "test_blind_rows": len(test), "family_disjoint": manifest["family_disjoint"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
