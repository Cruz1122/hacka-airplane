"""Build the Colab payload for colab_train.py: {"pools": [{id, texts}], "blind": [...]}.

pools: per entry (hubs included) its label, examples and kb.app_texts(conv=True) rows, deduplicated.
Every text whose folded key is a turn of research_notes/depth_v1/blind_v4/all_rows.jsonl is dropped
(all_rows holds dev and sealed texts, written before the split, so v4_sealed is never opened).
blind: v4_dev queries_v4 + labels_v4, split "dev".

usage (nlu venv): uv run python build_payload.py --out work/payload_ft5.json
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

from kb import ROOT, app_texts, load_entries

V4 = ROOT / "research_notes/depth_v1/blind_v4"


def key(text: str) -> str:
    """Same key as depth_v1/tools/integrate_train.py: accent-folded a-z0-9 words."""
    t = unicodedata.normalize("NFD", text.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " ".join(re.findall(r"[a-z0-9]+", t))


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--no-variants", action="store_true", help="leave train_variants.json out of the pools")
    a = ap.parse_args()

    banned = {key(t) for r in read_jsonl(V4 / "all_rows.jsonl") for t in r["turns"]}
    extra = app_texts(conv=True, variants=not a.no_variants)
    entries = load_entries(hubs=True)
    ids = {e.id for e in entries}
    orphans = sorted(set(extra) - ids)
    if orphans:
        raise SystemExit(f"app_texts ids with no entry: {orphans[:10]} ({len(orphans)})")

    pools, dropped = [], 0
    for e in entries:
        seen, texts = set(), []
        # Exact-string dedup only: accent/punctuation variants of one question are kept on purpose,
        # they teach robustness to badly written queries. The folded key is only the leak test.
        for t in [e.label, *e.examples, *extra.get(e.id, [])]:
            t = t.strip()
            if not t or t in seen:
                continue
            seen.add(t)
            if key(t) in banned:
                dropped += 1
                continue
            texts.append(t)
        pools.append({"id": e.id, "texts": texts})

    lab = {r["qid"]: r["acceptable"] for r in read_jsonl(V4 / "v4_dev/labels_v4.jsonl")}
    blind = [{"qid": r["qid"], "turns": r["turns"], "style": r["style"], "acceptable": lab[r["qid"]],
              "split": "dev"} for r in read_jsonl(V4 / "v4_dev/queries_v4.jsonl") if r["qid"] in lab]

    a.out.write_text(json.dumps({"pools": pools, "blind": blind}, ensure_ascii=False))
    n = sum(len(p["texts"]) for p in pools)
    print(f"pools {len(pools)} texts {n} (dropped as blind leak {dropped}; pools <2 texts "
          f"{sum(len(p['texts']) < 2 for p in pools)}) blind {len(blind)} -> {a.out} "
          f"{a.out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
