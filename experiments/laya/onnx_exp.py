"""E7: export Laya PT/ES NLI to ONNX (fp32 and dynamic int8); measure size, CPU latency, agreement.

uv run python onnx_exp.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch
from exp import LAYA_ID, OUT, load_laya, nli_question, p_entail
from kb import load_sections

ART = OUT / "onnx"
N_CANDS = 5


def export(agent, path: Path) -> None:
    model = agent.model.eval()
    L, k = 64, 3
    args = (
        torch.ones(N_CANDS, L, dtype=torch.long),
        torch.ones(N_CANDS, L, dtype=torch.long),
        torch.tensor([[10, 20, 30]] * N_CANDS, dtype=torch.long),
        torch.ones(N_CANDS, k, dtype=torch.bool),
        torch.zeros(N_CANDS, dtype=torch.long),
    )
    torch.onnx.export(
        model,
        args,
        str(path),
        dynamo=False,
        opset_version=17,
        input_names=["input_ids", "attention_mask", "marker_pos", "marker_mask", "qtype"],
        output_names=["logits", "act_logits"],
        dynamic_axes={
            "input_ids": {0: "n", 1: "L"},
            "attention_mask": {0: "n", 1: "L"},
            "marker_pos": {0: "n", 1: "k"},
            "marker_mask": {0: "n", 1: "k"},
            "qtype": {0: "n"},
            "logits": {0: "n"},
            "act_logits": {0: "n"},
        },
    )


def main() -> None:
    from laya.onnx_agent import ONNXAgent
    from onnxruntime.quantization import QuantType, quantize_dynamic

    ART.mkdir(parents=True, exist_ok=True)
    agent = load_laya()
    fp32 = ART / "laya_pt_es_nli.onnx"
    int8 = ART / "laya_pt_es_nli.int8.onnx"
    if not fp32.exists():
        export(agent, fp32)
    if not int8.exists():
        quantize_dynamic(str(fp32), str(int8), weight_type=QuantType.QInt8)

    _, entries = load_sections()
    by_id = {e.id: e for e in entries}
    rows = [json.loads(x) for x in (OUT / "laya_rows_e5-base.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["set"] == "paraphrase"]

    def qset(r):
        cands = r["pool"][:N_CANDS]
        return cands, {
            f"c{i}": nli_question(f"El visitante pregunta sobre {by_id[c].label}.")
            for i, c in enumerate(cands)
        }

    runners = {"torch": agent}
    for name, path in (("onnx_fp32", fp32), ("onnx_int8", int8)):
        runners[name] = ONNXAgent(LAYA_ID, onnx_path=str(path))
    report = {
        "n_candidates": N_CANDS,
        "threads_note": "onnxruntime default threads; torch 4 threads",
    }
    picks: dict[str, list[str]] = {}
    for name, ag in runners.items():
        cands, qs = qset(rows[0])
        ag.system_one(rows[0]["q"], qs)  # warm-up
        lat, pk, ok = [], [], 0
        for r in rows:
            cands, qs = qset(r)
            t0 = time.perf_counter()
            res = ag.system_one(r["q"], qs)
            lat.append(time.perf_counter() - t0)
            ps = [p_entail(res, f"c{i}") for i in range(len(cands))]
            # E4a+emb score on the first N_CANDS of the pool.
            comb = [a + b for a, b in zip(ps, r["pool_scores"][:N_CANDS], strict=True)]
            pick = cands[int(np.argmax(comb))]
            pk.append(pick)
            ok += pick in r["expected"]
        picks[name] = pk
        report[name] = {
            "p50_ms": round(1000 * float(np.percentile(lat, 50)), 1),
            "p95_ms": round(1000 * float(np.percentile(lat, 95)), 1),
            "paraphrase_top1_E4a+emb_top5pool": round(ok / len(rows), 4),
        }
        print(name, report[name], flush=True)
    for name in ("onnx_fp32", "onnx_int8"):
        report[name]["agreement_with_torch"] = round(
            float(np.mean([a == b for a, b in zip(picks[name], picks["torch"], strict=True)])), 4
        )
    report["size_mb"] = {p.name: round(p.stat().st_size / 1e6, 1) for p in ART.glob("*.onnx*")}
    (OUT / "onnx.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
