"""Write the depth_v1 training pools next to the original app files.

Reads resolved/T4_*.clean.jsonl and resolved/T5_*.clean.jsonl. Does not edit sections, aug_queries
or followup_convs. Drops a text whose folded key is already in blind_v4/all_rows.jsonl.

  python3 integrate_train.py
  -> data/knowledge/app/train_variants.json   {entry_id: [text]}
  -> data/knowledge/app/train_convs.json      {target_id: [[{text, entry_id}, ...]]}
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from common import DEPTH, entries, fold  # noqa: E402

ROOT = DEPTH.parents[1]
APP = ROOT / "data/knowledge/app"
RESOLVED = DEPTH / "resolved"
BLIND = DEPTH / "blind_v4/all_rows.jsonl"


def key(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(text)))


def blind_keys() -> set[str]:
    out: set[str] = set()
    for line in BLIND.read_text().splitlines():
        if line.strip():
            for turn in json.loads(line)["turns"]:
                out.add(key(turn))
    return out


def main() -> None:
    known = set(entries())
    banned = blind_keys()
    variants: dict[str, list[str]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)
    skipped = {"unknown": 0, "blind": 0, "dup": 0, "empty": 0}

    def take(eid: str, text: str) -> bool:
        text = " ".join(text.split())
        if not text:
            skipped["empty"] += 1
            return False
        if eid not in known:
            skipped["unknown"] += 1
            return False
        k = key(text)
        if k in banned:
            skipped["blind"] += 1
            return False
        if k in seen[eid]:
            skipped["dup"] += 1
            return False
        seen[eid].add(k)
        return True

    for path in sorted(RESOLVED.glob("T4_*.clean.jsonl")):
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if take(row["entry_id"], row["text"]):
                variants[row["entry_id"]].append(" ".join(row["text"].split()))

    convs: dict[str, list[list[dict]]] = defaultdict(list)
    conv_rows = 0
    for path in sorted(RESOLVED.glob("T5_*.clean.jsonl")):
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            turns = []
            for turn in row["turns"]:
                text = " ".join(turn["text"].split())
                if take(turn["entry_id"], text):
                    turns.append({"text": text, "entry_id": turn["entry_id"]})
            if turns and row["entry_id"] in known:
                convs[row["entry_id"]].append(turns)
                conv_rows += 1

    APP.mkdir(parents=True, exist_ok=True)
    (APP / "train_variants.json").write_text(json.dumps(variants, ensure_ascii=False))
    (APP / "train_convs.json").write_text(json.dumps(convs, ensure_ascii=False))
    print(json.dumps({
        "variant_entries": len(variants),
        "variant_texts": sum(map(len, variants.values())),
        "conv_entries": len(convs),
        "conversations": conv_rows,
        "skipped": skipped,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
