"""Sweep the off-topic floor T and the follow-up weight w on a blind set, phone-faithfully.

Same replay as gguf_eval.py (engine.ts): cue/short-and-below gate, concat context, fused turns chain
their context text (last 60 words), T judges standalone turns only. The gate does not depend on T or
w, so every query text is embedded once and the grid is pure numpy. Reads the CURRENT exported
assets (index.json, index.f32.bin, policy.json) for k, max_words, below and cue.

--mask-leaks also scores with every index row whose folded key is a blind_v4 turn removed
(all_rows.jsonl: dev and sealed texts; v4_sealed is never opened), so leaked rows cannot inflate it.

usage (laya venv): uv run python ../nlu/sweep_v4.py --gguf ../../models/knowledge/e5-nlu-ft5-f16.gguf \
    --blind ../../research_notes/depth_v1/blind_v4/v4_dev --mask-leaks
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

from build_payload import V4, key, read_jsonl  # noqa: E402
from export_knowledge import ASSETS, embed_gguf  # noqa: E402
from export_nlu import entry_scores, fuse, load  # noqa: E402
from gate_sweep import load_v2  # noqa: E402
from kb import app_texts  # noqa: E402

ROOT = HERE.parents[1]
OFF = "conversation.off_topic_question"
W_GRID = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
T_GRID = np.round(np.arange(0.30, 0.951, 0.01), 2)
norm = lambda t: " ".join(t.split())  # noqa: E731


def index_texts() -> list[str]:
    """The exported row texts in export_nlu order (to find leaked rows)."""
    _, entries = load()
    extra = app_texts(conv=True)
    out = []
    for e in entries:
        for t in [e["label"], *e.get("examples", []), *extra.get(e["id"], [])]:
            t = norm(t)
            if t:
                out.append(t)
    return out


def replay(rows, score, f):
    """Per row: list of (standalone scores, fused?, context text or None) per turn; returns texts needed."""
    plans, need = [], set()
    for r in rows:
        prev_text, steps = None, []
        for t in r["turns"]:
            s = score(t)
            short = len(t.split()) <= f["max_words"]
            gate = bool(re.match(f["cue"], t, re.I)) or (short and s.max() < f["below"])
            ctx = f"{prev_text} {t}" if prev_text is not None and gate else None
            if ctx:
                need.add(norm(ctx))
            steps.append((t, ctx))
            prev_text = " ".join(ctx.split()[-60:]) if ctx else t
        plans.append(steps)
    return plans, need


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gguf", type=Path, required=True)
    ap.add_argument("--llama-embedding", type=Path,
                    default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding")
    ap.add_argument("--blind", type=Path, required=True)
    ap.add_argument("--mask-leaks", action="store_true")
    a = ap.parse_args()

    catalog = json.loads((ASSETS / "catalog.json").read_text())
    policy = json.loads((ASSETS / "policy.json").read_text())
    m = json.loads((ASSETS / "index.json").read_text())
    if m["embedder"]["file"] != a.gguf.name:
        raise SystemExit(f"assets were exported with {m['embedder']['file']}, not {a.gguf.name}")
    vec = np.fromfile(ROOT / "models/knowledge" / m["vectors"]["file"], dtype="<f4").reshape(m["rows"], m["dims"])
    tv, owner = vec[: m["text_rows"]], np.asarray(m["row_entry"])
    ids = [e["id"] for e in catalog]
    k, f = policy["score_topk"], policy["followup"]
    rows = load_v2(a.blind)

    variants = {"all rows": np.ones(len(tv), bool)}
    if a.mask_leaks:
        texts = index_texts()
        if len(texts) != len(tv):
            raise SystemExit(f"index text order mismatch: {len(texts)} vs {len(tv)}")
        banned = {key(t) for r in read_jsonl(V4 / "all_rows.jsonl") for t in r["turns"]}
        keep = np.array([key(t) not in banned for t in texts])
        variants["leaks masked"] = keep
        print(f"index rows whose key is a blind_v4 turn: {int((~keep).sum())} of {len(tv)}")

    turns = sorted({norm(t) for r in rows for t in r["turns"]})
    qv = dict(zip(turns, embed_gguf(turns, a.gguf, a.llama_embedding), strict=True))
    for name, keep in variants.items():
        tvk, ok_owner = tv[keep], owner[keep]
        memo: dict[str, np.ndarray] = {}

        def score(t: str, tvk=tvk, ok_owner=ok_owner, memo=memo) -> np.ndarray:
            t = norm(t)
            if t not in memo:
                memo[t] = entry_scores((tvk @ qv[t]).astype(np.float32), ok_owner, len(ids), k)
            return memo[t]

        plans, need = replay(rows, score, f)
        missing = sorted(need - qv.keys())
        if missing:
            qv.update(zip(missing, embed_gguf(missing, a.gguf, a.llama_embedding), strict=True))
        # Final (scores, fused) per row for each w; T applies afterwards.
        best = None
        table = {}
        for w in W_GRID:
            finals = []
            for steps in plans:
                for t, ctx in steps:
                    s = score(t)
                    if ctx:
                        s = fuse(s, score(ctx), w)
                finals.append((s, ctx is not None))
            for T in T_GRID:
                by = defaultdict(lambda: [0, 0])
                for r, (s, fused) in zip(rows, finals, strict=True):
                    top = int(np.argmax(s))
                    pid = ids[top] if s[top] >= T or fused else None
                    acc = r["acceptable"]
                    ok = (pid in acc or (pid is None and OFF in acc)) if acc else pid is None
                    by[r["style"]][0] += ok
                    by[r["style"]][1] += 1
                tot = sum(v[0] for v in by.values()) / len(rows)
                table[(w, float(T))] = tot
                if best is None or tot > best[0]:
                    best = (tot, w, float(T), {s: round(v[0] / v[1], 3) for s, v in sorted(by.items())})
        print(f"\n[{name}] n={len(rows)} k={k} max_words={f['max_words']} below={f['below']}")
        print(f"best acc {best[0]:.3f} at w={best[1]} T={best[2]:.2f}")
        for s, v in best[3].items():
            print(f"  {s:12s} {v:.3f}")
        # Flatness check: how much the neighbourhood of the optimum moves.
        print("  acc by w at best T:", {w: round(table[(w, best[2])], 3) for w in W_GRID})
        print("  acc by T at best w:", {T: round(table[(best[1], T)], 3) for T in (0.4, 0.5, 0.6, 0.7, 0.8, best[2])})


if __name__ == "__main__":
    main()
