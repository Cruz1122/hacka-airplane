"""Render captured requests into raw prompt/completion text with the target model's template.

The prompt text comes from llama-server's /apply-template for the same GGUF the phone
runs, so training sees byte-for-byte what /completion receives in deployment (Qwen3 with
reasoning off appends an empty think block). Split: dialogues are kept whole in one side.

Usage:
  docker run ... llama-server -m Qwen3-0.6B-Q4_K_M.gguf --reasoning off --port 8082
  uv run python -m nevados_bench.finetune.render --in data/finetune/examples.jsonl \
      --template-url http://127.0.0.1:8082 --out data/finetune
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import httpx

EOT = "<|im_end|>"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", type=Path, required=True)
    ap.add_argument("--template-url", default="http://127.0.0.1:8082")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dev-share", type=float, default=0.04)
    args = ap.parse_args()
    rows = [json.loads(line) for line in args.inp.read_text().splitlines() if line.strip()]
    args.out.mkdir(parents=True, exist_ok=True)
    train = (args.out / "train.jsonl").open("w")
    dev = (args.out / "dev.jsonl").open("w")
    counts = {"train": 0, "dev": 0}
    with httpx.Client(base_url=args.template_url, timeout=30.0) as client:
        for i, row in enumerate(rows):
            resp = client.post("/apply-template", json={"messages": row["messages"]})
            resp.raise_for_status()
            key = row.get("dialogue_id") or f"single-{i}"
            bucket = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 10_000
            side = "dev" if bucket < args.dev_share * 10_000 else "train"
            rec = {
                "prompt": resp.json()["prompt"],
                "completion": row["target"] + EOT,
                "call_type": row["call_type"],
                "source": row.get("source"),
            }
            (dev if side == "dev" else train).write(json.dumps(rec, ensure_ascii=False) + "\n")
            counts[side] += 1
    train.close()
    dev.close()
    print(counts)


if __name__ == "__main__":
    main()
