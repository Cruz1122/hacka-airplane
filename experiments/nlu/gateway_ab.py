"""A/B of the vector gateway on the shipped ft4 index: all gates open (shipped) vs soft and hard routing.

Replays gguf_eval.py's phone-faithful loop (top-3 mean, follow-up fusion, T) and adds retrieve.ts's
gateway: gate score = max row cosine of the CURRENT turn over the gate's text rows + description row;
open gates = score >= best - delta, at most max_sections; the answer is the best fused entry inside
the open gates. Same query vectors for every variant (one embedding pass).

usage (experiments/laya venv): uv run python ../nlu/gateway_ab.py --gguf ../../models/knowledge/e5-nlu-ft4-f16.gguf
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

NLU = Path(__file__).resolve().parent
sys.path.insert(0, str(NLU.parent / "laya"))
sys.path.insert(0, str(NLU))

from evaluate import load_blind  # noqa: E402
from export_knowledge import ASSETS, embed_gguf  # noqa: E402
from export_nlu import entry_scores, fuse  # noqa: E402
from gate_sweep import load_v2  # noqa: E402

ROOT = NLU.parents[1]
OFF = "conversation.off_topic_question"
# name: (delta, max_sections, gate source). Gate source of a follow-up turn:
#   turn  = the current turn's own section scores (what retrieve.ts does today)
#   fused = section scores fused with the context's like entry scores: (cur + w * ctx) / (1 + w)
#   union = the current turn's open gates plus the previous turn's open gates
VARIANTS = {
    "all open (shipped)": (2.0, 15, "turn"),
    "d.05 turn": (0.05, 5, "turn"),
    "d.05 fused": (0.05, 5, "fused"),
    "d.10 fused": (0.10, 5, "fused"),
    "d.05 union": (0.05, 5, "union"),
    "d.10 union": (0.10, 5, "union"),
    "hard fused": (0.0, 1, "fused"),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gguf", type=Path, required=True)
    ap.add_argument(
        "--llama-embedding",
        type=Path,
        default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding",
    )
    a = ap.parse_args()

    catalog = json.loads((ASSETS / "catalog.json").read_text())
    policy = json.loads((ASSETS / "policy.json").read_text())
    m = json.loads((ASSETS / "index.json").read_text())
    vec = np.fromfile(ROOT / "models/knowledge" / m["vectors"]["file"], dtype="<f4").reshape(
        m["rows"], m["dims"]
    )
    nt = m["text_rows"]
    owner = np.asarray(m["row_entry"])
    ent_sec = np.asarray(m["entry_section"])
    row_sec = ent_sec[owner]
    n_sec = len(m["section_rows"])
    ids = [e["id"] for e in catalog]
    k, T, f = policy["score_topk"], policy["T"], policy["followup"]

    sets = {
        "dev": [r for r in load_blind() if r["split"] == "dev"],
        "test": [r for r in load_blind() if r["split"] == "test"],
        "blind_v2": load_v2(NLU / "work/blind_v2"),
        "blind_v3 (sealed)": load_v2(NLU / "work/blind_v3"),
    }
    norm = lambda t: " ".join(t.split())  # noqa: E731
    texts = set()
    for rows in sets.values():
        for r in rows:
            texts |= {norm(t) for t in r["turns"]}
            texts |= {
                norm(" ".join(r["turns"][j : i + 1]))
                for i in range(1, len(r["turns"]))
                for j in range(i)
            }
    turns = sorted(texts)
    qv = dict(zip(turns, embed_gguf(turns, a.gguf, a.llama_embedding), strict=True))

    def sims(t: str) -> np.ndarray:
        return (vec @ qv[norm(t)]).astype(np.float32)

    def sec_scores(rs: np.ndarray) -> np.ndarray:
        sec = np.full(n_sec, -np.inf, dtype=np.float32)
        np.maximum.at(sec, row_sec, rs[:nt])
        return np.maximum(sec, rs[nt:])

    def open_gates(sec: np.ndarray, delta: float, max_sec: int) -> set[int]:
        order = sorted(range(n_sec), key=lambda s: (-sec[s], m["section_rows"][s]))
        floor = np.float32(sec[order[0]] - np.float32(delta))
        return set([s for s in order if sec[s] >= floor][:max_sec])

    print(f"gguf={a.gguf.name} score_topk={k} T={T} followup w={f['w']}")
    header = "set".ljust(20) + "n".rjust(5) + "".join(v[:22].rjust(24) for v in VARIANTS)
    print(header)
    for name, rows in sets.items():
        tally = defaultdict(lambda: [0, 0])  # variant -> [ok, strict_ok]
        fol = defaultdict(lambda: [0, 0])  # variant -> [ok, n] on multi-turn rows
        for r in rows:
            acc = r["acceptable"]
            sacc = [x for x in acc if not x.startswith("hub.")]
            for v, (delta, max_sec, src) in VARIANTS.items():
                prev, prev_text, prev_open = None, None, None
                fused = False
                for t in r["turns"]:
                    rs = sims(t)
                    s = entry_scores(rs[:nt], owner, len(ids), k)
                    sec = sec_scores(rs)
                    short = len(t.split()) <= f["max_words"]
                    gate = bool(re.match(f["cue"], t, re.I)) or (short and s.max() < f["below"])
                    fused = False
                    if prev is not None and gate:
                        crs = sims(f"{prev_text} {t}")
                        s = fuse(s, entry_scores(crs[:nt], owner, len(ids), k), f["w"])
                        if src == "fused":
                            sec = fuse(sec, sec_scores(crs), f["w"])
                        fused = True
                    opened = open_gates(sec, delta, max_sec)
                    if src == "union" and fused and prev_open is not None:
                        opened |= prev_open
                    prev, prev_open = s, opened
                    prev_text = " ".join(f"{prev_text} {t}".split()[-60:]) if fused else t
                mask = np.isin(ent_sec, list(opened))
                gs = np.where(mask & (s > -1), s, -np.inf)
                top = int(np.argmax(gs))
                pid = ids[top] if np.isfinite(gs[top]) and (gs[top] >= T or fused) else None
                ok = (pid in acc or (pid is None and OFF in acc)) if acc else pid is None
                sok = (pid in sacc or (pid is None and OFF in sacc)) if sacc else pid is None
                tally[v][0] += ok
                tally[v][1] += sok
                if len(r["turns"]) > 1:
                    fol[v][0] += ok
                    fol[v][1] += 1
        n = len(rows)
        print(
            name.ljust(20)
            + str(n).rjust(5)
            + "".join(
                f"{tally[v][0] / n:6.1%} (s {tally[v][1] / n:5.1%})".rjust(24) for v in VARIANTS
            )
        )
        nf = fol[next(iter(VARIANTS))][1]
        if nf:
            print(
                "  follow-ups".ljust(20)
                + str(nf).rjust(5)
                + "".join(f"{fol[v][0] / nf:6.1%}".rjust(24) for v in VARIANTS)
            )


if __name__ == "__main__":
    main()
