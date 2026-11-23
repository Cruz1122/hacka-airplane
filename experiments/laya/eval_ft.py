"""Gate the fine-tuned Laya on the artifact that ships: ONNX int8 on CPU, Phase 2 eval pools.

  uv run python eval_ft.py /path/to/laya_ft_ckpt_A     # unzipped checkpoint from the Colab notebook

The e5-base baseline is computed on the same rows (pool order = e5 rank, meta.cos = cosine).
Rule (docs/history/plan-knowledge-system.md): versus the BEST embedding-only setup, +5 points top-1, or
+10 points answered at <= 3 % wrong; and int8 p50 <= 400 ms on the laptop CPU with k = 5.
fp32 ONNX runs on the same rows so a miss can be blamed on the model or on quantization.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from exp import OUT
from ft_data import FT, NONE, coverage_at
from onnx_exp import export

torch.set_num_threads(4)


def run(agent, rows: list[dict], k: int) -> tuple[list[dict], list[float]]:
    preds, lat = [], []
    for r in rows:
        q = json.loads(json.dumps(r["questions"]))
        options = q["topic"]["criteria"][:-1][:k]
        q["topic"]["criteria"] = [*options, NONE]
        pool = r["meta"]["pool"][: len(options)]
        cos = r["meta"]["cos"][: len(options)]
        gold = set(r["meta"]["gold"])
        t0 = time.perf_counter()
        a = agent.system_one(r["state"], q)["answers"]["topic"]
        lat.append(time.perf_counter() - t0)
        probs = a["probabilities"]
        p = [float(probs[o]) for o in options]
        best = int(np.argmax(p))
        comb = [x + c for x, c in zip(p, cos, strict=True)]
        bc = int(np.argmax(comb))
        preds.append(
            {
                "kind": r["meta"]["kind"],
                "heldout": r["meta"]["heldout_gold"],
                "gold_in_pool": bool(set(pool) & gold),
                "says_none": a["choice"] == NONE,
                "p_none": float(probs[NONE]),
                "laya_pick": pool[best],
                "laya_ok": pool[best] in gold,
                "laya_conf": p[best] * (a["choice"] != NONE),
                "comb_pick": pool[bc],
                "comb_ok": pool[bc] in gold,
                "comb_conf": comb[bc] * (a["choice"] != NONE),
                "e5_ok": pool[0] in gold,
                "e5_cos": cos[0],
                "e5_margin": cos[0] - cos[1] if len(cos) > 1 else cos[0],
            }
        )
    return preds, lat


def score(preds: list[dict], ok: str, conf: str) -> dict:
    para = [p for p in preds if p["kind"] == "paraphrase"]
    held = [p for p in para if p["heldout"]]
    items = [(p[conf], p[ok], p["kind"] == "paraphrase") for p in preds]
    return {
        "top1": round(sum(p[ok] for p in para) / len(para), 4),
        "top1_heldout_entries": round(sum(p[ok] for p in held) / max(1, len(held)), 4),
        "abstention": coverage_at(items),
    }


def metrics(preds: list[dict], lat: list[float]) -> dict:
    ood = [p for p in preds if p["kind"] != "paraphrase"]
    return {
        "e5_cos": score(preds, "e5_ok", "e5_cos"),
        "e5_margin": score(preds, "e5_ok", "e5_margin"),
        "laya": score(preds, "laya_ok", "laya_conf"),
        "laya+cos": score(preds, "comb_ok", "comb_conf"),
        "ood_says_none": round(sum(p["says_none"] for p in ood) / max(1, len(ood)), 4),
        "p50_ms": round(1000 * float(np.median(lat)), 1),
        "p95_ms": round(1000 * float(np.percentile(lat, 95)), 1),
    }


def main(ckpt: str, limit: int | None = None) -> None:
    import laya
    from laya.onnx_agent import ONNXAgent
    from onnxruntime.quantization import QuantType, quantize_dynamic

    rows = [json.loads(x) for x in (FT / "eval.jsonl").read_text().splitlines()]
    if limit:  # smoke only: keep both in-domain and out-of-domain rows
        para = [r for r in rows if r["meta"]["kind"] == "paraphrase"]
        rows = para[:limit] + [r for r in rows if r["meta"]["kind"] != "paraphrase"][:limit]
    art = Path(ckpt) / "onnx"
    art.mkdir(exist_ok=True)
    fp32, int8 = art / "laya_ft.onnx", art / "laya_ft.int8.onnx"
    if not fp32.exists():
        export(laya.load(ckpt, device="cpu", vegaml=False), fp32)
    if not int8.exists():
        quantize_dynamic(str(fp32), str(int8), weight_type=QuantType.QInt8)
    name = Path(ckpt).name
    report: dict = {"ckpt": ckpt, "int8_mb": round(int8.stat().st_size / 1e6, 1)}
    for tag, path in (("int8", int8), ("fp32", fp32)):
        agent = ONNXAgent(ckpt, onnx_path=str(path))
        agent.system_one(rows[0]["state"], rows[0]["questions"])  # warm-up
        for k in (5, 3) if tag == "int8" else (5,):
            preds, lat = run(agent, rows, k)
            report[f"{tag}_k{k}"] = metrics(preds, lat)
            (OUT / f"laya_ft_preds_{name}_{tag}_k{k}.jsonl").write_text(
                "".join(json.dumps(p, ensure_ascii=False) + "\n" for p in preds)
            )
            print(tag, k, json.dumps(report[f"{tag}_k{k}"]), flush=True)
    (OUT / f"laya_ft_gate_{name}.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
