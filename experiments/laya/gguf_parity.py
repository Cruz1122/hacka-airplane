"""E12: e5-base GGUF (llama.cpp) vs sentence-transformers on the Phase 3 retrieval contract.

  uv run python gguf_parity.py ../../models/knowledge/e5-base-q8_0.gguf [more.gguf ...]

For each backend, index and queries both come from that backend (as on the phone). Eval rows: the
six final-dataset validation/evaluation splits, retrieved with the fit-time self mask.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from export_knowledge import ROOT, Index, embed_gguf, embed_st

DS = ROOT / "models/laya_final_rlcd6_raw/ds/LOS_NEVADOS_COLAB_FINAL/LOS_NEVADOS_LAYA_FINAL_DATASET"
SPLITS = ["validation/calibration", "validation/checkpoint_selection", "validation/unseen_topics",
          "evaluation/adversarial", "evaluation/final_test_SEALED",
          "evaluation/retrospective_test_blind_READ_ONLY"]
BIN = Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding"


def run(ix: Index, rows: list[dict], vec: np.ndarray) -> list[dict]:
    ix.set_vectors(vec[: len(ix.texts) + len(ix.desc)])
    qv = vec[len(ix.texts) + len(ix.desc) :]
    return [ix.retrieve(v, ix.mask_for(r["state"])) for r, v in zip(rows, qv, strict=True)]


def main(ggufs: list[str]) -> None:
    ix = Index()
    rows = [json.loads(x) for s in SPLITS for x in (DS / f"{s}.jsonl").read_text().splitlines() if x]
    texts = ix.texts + ix.desc + [r["state"] for r in rows]
    T = json.loads((ROOT / "mobile/assets/data/knowledge/policy.json").read_text())["T"]
    t0 = time.time()
    ref_v = embed_st(texts)
    ref = run(ix, rows, ref_v)
    report = {"rows": len(rows), "T": T, "st_seconds": round(time.time() - t0, 1)}
    for g in ggufs:
        t0 = time.time()
        v = embed_gguf(texts, Path(g), BIN)
        secs = round(time.time() - t0, 1)
        res = run(ix, rows, v)
        vcos = np.sum(v * ref_v, axis=1)
        d = np.array([a["cos"][0] - b["cos"][0] for a, b in zip(res, ref, strict=True)])
        flips = sum((a["cos"][0] >= T) != (b["cos"][0] >= T) for a, b in zip(res, ref, strict=True))
        top3 = sum(a["pool"][:3] != b["pool"][:3] for a, b in zip(res, ref, strict=True))
        top1 = sum(a["pool"][0] != b["pool"][0] for a, b in zip(res, ref, strict=True))
        report[Path(g).name] = {
            "seconds": secs, "vector_cos_vs_st_min": round(float(vcos.min()), 5),
            "vector_cos_vs_st_p01": round(float(np.percentile(vcos, 1)), 5),
            "cos0_mean_signed_delta": round(float(d.mean()), 5),
            "cos0_abs_delta_p99": round(float(np.percentile(np.abs(d), 99)), 5),
            "menu_abstain_flips": flips, "flip_rate": round(flips / len(rows), 4),
            "top1_changed": top1, "top3_changed": top3,
        }
        print(Path(g).name, json.dumps(report[Path(g).name]), flush=True)
    out = ROOT / "results/p3-final/e12_gguf_parity.json"
    out.write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
