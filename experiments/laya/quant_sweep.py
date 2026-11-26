"""E10: int8 quantization variants for the fine-tuned Laya; same gate rows as eval_ft.py.

uv run python quant_sweep.py ../../models/laya_ft_A
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import onnx
from eval_ft import metrics, run
from exp import OUT
from ft_data import FT


def main(ckpt: str) -> None:
    from laya.onnx_agent import ONNXAgent
    from onnxruntime.quantization import QuantType, quantize_dynamic

    art = Path(ckpt) / "onnx"
    fp32 = art / "laya_ft.onnx"
    model = onnx.load(str(fp32), load_external_data=False)
    # Decision-head nodes: everything after the encoder (names do not start with the encoder prefix).
    head = [n.name for n in model.graph.node if n.op_type == "MatMul" and "encoder" not in n.name]
    variants = {
        "per_channel": {"per_channel": True},
        "matmul_per_channel": {"per_channel": True, "op_types_to_quantize": ["MatMul"]},
        "per_channel_head_fp32": {"per_channel": True, "nodes_to_exclude": head},
        "gather_only": {"op_types_to_quantize": ["Gather"]},
    }
    rows = [json.loads(x) for x in (FT / "eval.jsonl").read_text().splitlines()]
    report = {"head_matmul_nodes": len(head)}
    for name, kw in variants.items():
        path = art / f"laya_ft.{name}.onnx"
        if not path.exists():
            quantize_dynamic(str(fp32), str(path), weight_type=QuantType.QInt8, **kw)
        agent = ONNXAgent(ckpt, onnx_path=str(path))
        agent.system_one(rows[0]["state"], rows[0]["questions"])
        preds, lat = run(agent, rows, 5)
        m = metrics(preds, lat)
        report[name] = {"mb": round(path.stat().st_size / 1e6, 1), **m}
        print(
            name,
            report[name]["mb"],
            "MB",
            "p50",
            m["p50_ms"],
            "laya",
            m["laya"]["top1"],
            "laya+cos",
            m["laya+cos"]["top1"],
            "cov",
            m["laya+cos"]["abstention"]["cv_correct_coverage"],
            flush=True,
        )
    (OUT / f"quant_sweep_{Path(ckpt).name}.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
