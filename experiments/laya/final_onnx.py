"""E11: ship-format check for the final Laya checkpoint (run_rlcd6).

ONNX fp32 export, int8 on Gather only (E10 winner), then CPU predictions on a split compared row by
row with the Colab GPU predictions, plus latency.

  uv run python final_onnx.py <model_dir> <split.jsonl> <colab_predictions.jsonl> <out.json>
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from onnx_exp import export

torch.set_num_threads(4)


def main(model: str, split: str, colab: str, out: str) -> None:
    import laya
    from laya.onnx_agent import ONNXAgent
    from onnxruntime.quantization import QuantType, quantize_dynamic

    art = Path(model) / "onnx"
    art.mkdir(exist_ok=True)
    fp32, g8 = art / "laya_final.onnx", art / "laya_final.gather_int8.onnx"
    if not fp32.exists():
        export(laya.load(model, device="cpu", vegaml=False), fp32)
    if not g8.exists():
        quantize_dynamic(str(fp32), str(g8), weight_type=QuantType.QInt8, op_types_to_quantize=["Gather"])
    rows = [json.loads(x) for x in Path(split).read_text().splitlines()]
    ref = {p["row_id"]: p for p in map(json.loads, Path(colab).read_text().splitlines())}
    agent = ONNXAgent(model, onnx_path=str(g8))
    agent.system_one(rows[0]["state"], rows[0]["questions"])
    same, diffs, lat = 0, [], []
    for r in rows:
        t0 = time.perf_counter()
        a = agent.system_one(r["state"], r["questions"])["answers"]["topic"]
        lat.append(time.perf_counter() - t0)
        p = ref[r["meta"]["row_id"]]
        same += a["choice"] == p["choice"]
        diffs.append(max(abs(a["probabilities"][k] - p["probabilities"][k]) for k in p["probabilities"]))
    rep = {
        "rows": len(rows),
        "gather_int8_mb": round(g8.stat().st_size / 1e6, 1),
        "same_choice_as_colab": round(same / len(rows), 4),
        "max_prob_diff_p50": round(float(np.median(diffs)), 4),
        "max_prob_diff_p95": round(float(np.percentile(diffs, 95)), 4),
        "p50_ms": round(1000 * float(np.median(lat)), 1),
        "p95_ms": round(1000 * float(np.percentile(lat, 95)), 1),
        "note": "latency measured while review subagents ran; treat as upper bound",
    }
    Path(out).write_text(json.dumps(rep, indent=2))
    print(json.dumps(rep))


if __name__ == "__main__":
    main(*sys.argv[1:5])
