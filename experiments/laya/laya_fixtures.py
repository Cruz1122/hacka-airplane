"""Spec for the future TypeScript Laya port: inputs, tensors and outputs of the shipping ONNX.

  uv run python laya_fixtures.py <model_dir> <onnx> <eval.jsonl> [n_rows]

Writes mobile/src/core/knowledge/laya/__fixtures__/laya_io.json. Per row: the state and question
exactly as the app builds them, the internal question form, the state token ids, the encoded
sequence and marker positions, the ONNX logits, and the final probabilities from ONNXAgent. A TS
port must reproduce `seq`/`markers` from (state, question) and then the probabilities.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from laya.onnx_agent import ONNXAgent, _collate_items_numpy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "mobile/src/core/knowledge/laya/__fixtures__/laya_io.json"


def main(model: str, onnx: str, split: str, n: int = 40) -> None:
    agent = ONNXAgent(model, onnx_path=onnx)
    rows = [json.loads(x) for x in Path(split).read_text().splitlines() if x][:n]
    max_len = agent.cfg.get("max_len", 512)
    head_max_len = agent.cfg.get("head_max_len", 192)
    out = []
    for r in rows:
        q = r["questions"]
        ids = list(q)
        internal = {k: agent._to_internal(q[k]) for k in ids}
        items = agent._encode_state(r["state"], ids, internal, max_len, head_max_len)
        feed = _collate_items_numpy([items], agent.tok.pad_token_id)
        logits, act = agent.session.run(["logits", "act_logits"], feed)
        res = agent.system_one(r["state"], q)["answers"]["topic"]
        out.append({
            "row_id": r["meta"]["row_id"], "state": r["state"], "questions": q,
            "internal": internal, "seq": items[0]["ids"], "markers": items[0]["markers"],
            "qtype": items[0]["qtype"],
            "logits": np.round(logits[0], 6).tolist(), "act_logits": np.round(act[0], 6).tolist(),
            "choice": res["choice"], "probabilities": res["probabilities"],
        })
    tok = agent.tok
    probe = ["pa' los nevados, ¿por dónde es la entrada?", "ninguna de estas opciones",
             "Laguna del Otún", "¿Qué tema contesta la pregunta del visitante?", "ÁÉÍÓÚ ñ ü 123 km/h"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "model_bytes": Path(model).joinpath("model.safetensors").stat().st_size,
        "onnx": Path(onnx).name, "max_len": max_len, "head_max_len": head_max_len,
        "pad_id": tok.pad_token_id, "mask_token": tok.mask_token,
        "special": {k: getattr(tok, k, None) for k in ("cls_token", "sep_token", "bos_token", "eos_token")},
        "temperature": agent.cfg.get("temperature"),
        "tokenizer_probe": [{"text": t, "ids": tok(t, add_special_tokens=False)["input_ids"]} for t in probe],
        "rows": out,
    }, ensure_ascii=False))
    print(OUT, len(out), "rows", OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], *(int(x) for x in sys.argv[4:5]))
