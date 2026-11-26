"""Phone-faithful blind accuracy: the exported assets + index.f32.bin + llama.cpp (GGUF) query vectors,
scored exactly as mobile/src/core/knowledge does (top-k mean, follow-up fusion gate, T).

Each conversation is replayed turn by turn like the chat: the previous turn's FINAL entry scores
are what a follow-up fuses with (engine.ts prevScores).

usage (laya venv): uv run python ../nlu/gguf_eval.py --gguf ../../models/knowledge/e5-nlu-ft1-f16.gguf [--split test]
Reports accuracy with hub credit (labels_hub_*) and strict (original labels only).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "laya"))
sys.path.insert(0, str(HERE))

from evaluate import load_blind  # noqa: E402
from gate_sweep import load_v2  # noqa: E402
from export_knowledge import ASSETS, embed_gguf  # noqa: E402
from export_nlu import entry_scores, fuse  # noqa: E402

ROOT = HERE.parents[1]
OFF = "conversation.off_topic_question"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gguf", type=Path, required=True)
    ap.add_argument("--llama-embedding", type=Path,
                    default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--dump", type=Path)
    ap.add_argument("--blind", type=Path, help="a fresh set dir (queries_*.jsonl + labels_*.jsonl) instead of work/")
    a = ap.parse_args()

    catalog = json.loads((ASSETS / "catalog.json").read_text())
    policy = json.loads((ASSETS / "policy.json").read_text())
    m = json.loads((ASSETS / "index.json").read_text())
    vec = np.fromfile(ROOT / "models/knowledge" / m["vectors"]["file"], dtype="<f4").reshape(m["rows"], m["dims"])
    tv, owner = vec[: m["text_rows"]], np.asarray(m["row_entry"])
    ids = [e["id"] for e in catalog]
    k, T, f = policy["score_topk"], policy["T"], policy["followup"]

    blind = load_v2(a.blind) if a.blind else load_blind()
    rows = blind if a.blind else [r for r in blind if args_split(r, a.split)]
    strict_acc = {r["qid"]: [x for x in r["acceptable"] if not x.startswith("hub.")] for r in blind}
    norm = lambda t: " ".join(t.split())  # noqa: E731
    texts = {norm(t) for r in rows for t in r["turns"]}
    if f and f.get("mode") == "concat":  # engine.ts embeds "<previous user text> <this text>"
        texts |= {norm(" ".join(r["turns"][j:i + 1])) for r in rows for i in range(1, len(r["turns"])) for j in range(i)}
    turns = sorted(texts)
    qv = dict(zip(turns, embed_gguf(turns, a.gguf, a.llama_embedding), strict=True))

    by = defaultdict(lambda: [0, 0, 0])
    dump = []
    for r in rows:
        prev, prev_text = None, None
        score = lambda t: entry_scores((tv @ qv[norm(t)]).astype(np.float32), owner, len(ids), k)  # noqa: E731
        fused = False
        for t in r["turns"]:
            fused = False
            s = score(t)
            short = len(t.split()) <= f["max_words"] if f else False
            if f and f.get("cue"):
                gate = bool(re.match(f["cue"], t, re.I)) or (short and s.max() < f["below"])
            else:
                gate = bool(f) and (short or s.max() < f["below"])
            if prev is not None and gate:
                ctx = score(f"{prev_text} {t}") if f.get("mode") == "concat" else prev
                s = fuse(s, ctx, f["w"])
                fused = True
            # engine.ts: a fused turn chains its context text (last 60 words)
            prev, prev_text = s, (" ".join(f"{prev_text} {t}".split()[-60:]) if fused else t)
        top = int(np.argmax(s))
        pid = ids[top] if s[top] >= T or fused else None  # engine.ts: T judges standalone turns only
        acc, sacc = r["acceptable"], strict_acc[r["qid"]]
        # Abstaining ("not in the park guide") is the right answer to an off-topic question too.
        ok = (pid in acc or (pid is None and OFF in acc)) if acc else pid is None
        sok = (pid in sacc or (pid is None and OFF in sacc)) if sacc else pid is None
        b = by[r["style"]]
        b[0] += ok
        b[1] += sok
        b[2] += 1
        dump.append({"qid": r["qid"], "turns": r["turns"], "pred": pid, "score": round(float(s[top]), 4),
                     "acceptable": acc, "ok": ok, "strict_ok": sok})
    n = sum(v[2] for v in by.values())
    print(f"split={a.split} n={n} gguf={a.gguf.name} k={k} T={T} followup={f}")
    print(f"acc (hub credit) {sum(v[0] for v in by.values()) / n:.3f}   strict {sum(v[1] for v in by.values()) / n:.3f}")
    print({s: round(v[0] / v[2], 3) for s, v in sorted(by.items())})
    if a.dump:
        a.dump.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in dump) + "\n")


def args_split(r: dict, split: str) -> bool:
    return split == "all" or r["split"] == split


if __name__ == "__main__":
    main()
