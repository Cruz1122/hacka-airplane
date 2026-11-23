"""Run a Laya checkpoint over one or more splits and write predictions (one line per row).

    python scripts/predict.py CKPT_DIR validation/checkpoint_selection.jsonl [more.jsonl ...] --out preds.jsonl [--device cuda]
"""
from __future__ import annotations

import argparse
import json

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PKG, jl  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ckpt")
    ap.add_argument("splits", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args()
    import laya  # noqa: PLC0415

    agent = laya.load(a.ckpt, device=a.device, vegaml=False)
    with open(a.out, "w", encoding="utf-8") as f:
        for rel in a.splits:
            for r in jl(PKG / rel):
                ans = agent.system_one(r["state"], r["questions"])["answers"]["topic"]
                f.write(json.dumps({"file": rel, "row_id": r["meta"]["row_id"], "choice": ans["choice"],
                                    "probabilities": ans.get("probabilities")}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
