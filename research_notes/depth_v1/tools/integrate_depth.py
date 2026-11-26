"""Write data/knowledge/app/depth_replies.json: per entry the "sigue" layers (T3) and the walk (R4.2).

walk (Part B §5): the entry's `related` ids, then 2-hop related ids, each group ordered by e5 cosine
of label to label. Never `actions.*` or `kind: chat`; an emergency entry walks only to
`health_safety` and `actions` entries. At most WALK ids.

layers: resolved/T3L_*.final.jsonl rows {entry_id, layers: [{kind, texts: [{text, atoms}]}]}
(approved layer texts, written from the entry's own complement facts). Absent -> no layers.

Run inside the nlu venv (label embeddings):
  cd experiments/nlu && uv run python ../../research_notes/depth_v1/tools/integrate_depth.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from common import DEPTH, emergency_ids, entries, read_jsonl  # noqa: E402
from emb import embed  # noqa: E402

APP = DEPTH.parents[1] / "data/knowledge/app"
WALK = 6


def main() -> None:
    E, emer = entries(), emergency_ids()
    ids = sorted(E)
    vec = dict(zip(ids, embed([E[i]["label"] for i in ids]), strict=True))

    def allowed(src: str, dst: str) -> bool:
        if dst == src or dst not in E or E[dst].get("kind") == "chat":
            return False
        if src in emer:
            return E[dst]["section"] in ("health_safety", "actions")
        return not dst.startswith("actions.")

    def ranked(src: str, cands: list[str]) -> list[str]:
        return sorted(dict.fromkeys(c for c in cands if allowed(src, c)),
                      key=lambda c: -float(np.dot(vec[src], vec[c])))

    layers: dict[str, list] = {}
    for p in sorted((DEPTH / "resolved").glob("T3L_*.final.jsonl")):
        for r in read_jsonl(p):
            layers[r["entry_id"]] = r["layers"]

    out = {}
    for eid in ids:
        if E[eid].get("kind") == "chat":
            continue
        hop1 = ranked(eid, E[eid].get("related", []))
        hop2 = ranked(eid, [h for r in E[eid].get("related", []) if r in E for h in E[r].get("related", [])])
        walk = (hop1 + [h for h in hop2 if h not in hop1])[:WALK]
        if walk or eid in layers:
            out[eid] = {"layers": layers.get(eid, []), "walk": walk}
    # Hubs (hubs.json) answer broad questions with a short text (HUB batch); "sigue" walks into
    # their members, in hub order. Emergency hubs keep only health_safety/actions members.
    for h in json.loads((APP / "hubs.json").read_text()):
        walk = [m for m in h["members"] if m in E and E[m].get("kind") != "chat"][:WALK]
        if walk:
            out[h["id"]] = {"layers": [], "walk": walk}
    (APP / "depth_replies.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"entries": len(out), "with_walk": sum(bool(v["walk"]) for v in out.values()),
                      "with_layers": sum(bool(v["layers"]) for v in out.values()),
                      "non_chat": sum(E[e].get("kind") != "chat" for e in ids)}))


if __name__ == "__main__":
    main()
