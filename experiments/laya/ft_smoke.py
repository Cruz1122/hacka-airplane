"""Local smoke of the full Laya fine-tune chain on a tiny slice (CPU), before spending Colab time.

dry_run -> finetune (100 rows, 1 epoch) -> laya.load(output) -> 6-option predict ->
ONNX export -> int8 -> ONNXAgent predict (same pick as torch?).

  uv run python ft_smoke.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from exp import LAYA_ID
from kb import ROOT

FT = ROOT / "data/knowledge/laya_ft"


def main() -> None:
    import laya
    from laya.onnx_agent import ONNXAgent
    from laya.train import TrainConfig, dry_run, finetune, resolve_checkpoint_dir
    from onnx_exp import export
    from onnxruntime.quantization import QuantType, quantize_dynamic

    work = Path(tempfile.mkdtemp(prefix="laya_smoke_"))
    rows = FT.joinpath("train.jsonl").read_text().splitlines()[:100]
    small = work / "train_small.jsonl"
    small.write_text("\n".join(rows) + "\n")
    base = resolve_checkpoint_dir(LAYA_ID)
    cfg = TrainConfig(
        epochs=1,
        micro_batch=4,
        grad_accum=1,
        shuffle_options=("choice",),
        calib_max=20,
        log_every=5,
    )
    print("dry_run:", json.dumps(dry_run(str(small), base, cfg), default=str)[:800])
    out = work / "ckpt"
    summary = finetune(str(small), base, str(out), cfg, device="cpu")
    print("finetune summary keys:", sorted(summary)[:20])
    agent = laya.load(str(out), device="cpu", vegaml=False)
    r = json.loads(rows[0])
    res = agent.system_one(r["state"], r["questions"])
    print("torch answer:", res["answers"]["topic"]["choice"], "| expected:", r["expected"]["topic"])
    six = next(
        json.loads(x) for x in rows if len(json.loads(x)["questions"]["topic"]["criteria"]) == 6
    )
    t6 = agent.system_one(six["state"], six["questions"])["answers"]["topic"]
    fp32, int8 = work / "m.onnx", work / "m.int8.onnx"
    export(agent, fp32)
    quantize_dynamic(str(fp32), str(int8), weight_type=QuantType.QInt8)
    for path in (fp32, int8):
        oa = ONNXAgent(str(out), onnx_path=str(path))
        o6 = oa.system_one(six["state"], six["questions"])["answers"]["topic"]
        print(
            path.name,
            "6-option pick:",
            o6["choice"],
            "| torch:",
            t6["choice"],
            "| max prob diff:",
            round(
                max(
                    abs(o6["probabilities"][k] - t6["probabilities"][k])
                    for k in t6["probabilities"]
                ),
                4,
            ),
        )
    print("work dir:", work)


if __name__ == "__main__":
    main()
