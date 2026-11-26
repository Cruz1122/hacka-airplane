"""blind_v4 label units + ft4 top-10 candidates (phone index), sharded for the labelers.

A unit is one turn to label. single -> its turn. multi -> every turn (context = earlier turns).
cont_pos / cont_neg -> turn 0 (entry) and turn 1 (is_continuation; entry if it is not one).
Candidates: top-10 entries of the turn alone, plus top-10 of "<prev> <turn>" for later turns.

usage (nlu venv): cd experiments/nlu && uv run python ../../research_notes/depth_v1/tools/v4_candidates.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments/laya"))
sys.path.insert(0, str(ROOT / "experiments/nlu"))
from export_knowledge import ASSETS, embed_gguf  # noqa: E402
from export_nlu import entry_scores  # noqa: E402

V4 = ROOT / "research_notes/depth_v1/blind_v4"
GGUF = ROOT / "models/knowledge/e5-nlu-ft4-f16.gguf"
BIN = Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding"
PER_SHARD = 100


def main() -> None:
    rows = []
    for p in sorted((V4 / "raw").glob("w*.jsonl")):
        for l in p.read_text().splitlines():
            if l.strip():
                rows.append(json.loads(l))
    (V4 / "all_rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    units = []
    for r in rows:
        t = [" ".join(x.split()) for x in r["turns"]]
        if r["type"] == "single":
            units.append({"uid": f"{r['qid']}:0", "qid": r["qid"], "type": r["type"], "turn": 0, "turns": t[:1]})
        else:
            for i in range(len(t)):
                units.append({"uid": f"{r['qid']}:{i}", "qid": r["qid"], "type": r["type"], "turn": i, "turns": t[: i + 1]})
    texts = sorted({u["turns"][-1] for u in units} | {f"{u['turns'][-2]} {u['turns'][-1]}" for u in units if u["turn"] > 0})
    vec = dict(zip(texts, embed_gguf(texts, GGUF, BIN), strict=True))
    cat = json.loads((ASSETS / "catalog.json").read_text())
    m = json.loads((ASSETS / "index.json").read_text())
    iv = np.fromfile(ROOT / "models/knowledge" / m["vectors"]["file"], dtype="<f4").reshape(m["rows"], m["dims"])
    tv, owner = iv[: m["text_rows"]], np.asarray(m["row_entry"])
    ids = [e["id"] for e in cat]
    info = {e["id"]: {"id": e["id"], "label": e["label"], "short": (e.get("short") or "")[:110]} for e in cat}
    k = json.loads((ASSETS / "policy.json").read_text())["score_topk"]

    def top(text: str) -> list[str]:
        s = entry_scores((tv @ vec[text]).astype(np.float32), owner, len(ids), k)
        return [ids[i] for i in np.argsort(-s)[:10]]

    for u in units:
        c = top(u["turns"][-1])
        if u["turn"] > 0:
            c += [x for x in top(f"{u['turns'][-2]} {u['turns'][-1]}") if x not in c]
        u["candidates"] = [info[x] for x in c]
    out = V4 / "label_shards"
    out.mkdir(exist_ok=True)
    n = 0
    for i in range(0, len(units), PER_SHARD):
        (out / f"L{n:02d}.json").write_text(json.dumps({"shard": f"L{n:02d}", "units": units[i : i + PER_SHARD]}, ensure_ascii=False, indent=0))
        n += 1
    print(f"rows {len(rows)} units {len(units)} shards {n}")


if __name__ == "__main__":
    main()
