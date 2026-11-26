"""T5 write shards: 25 entries each, with the inputs R2.2 needs. Seeded, so reruns are identical.

Per entry: id, section, kind, label, L0, 3 current examples, related entries (id, label, L0 cut),
5 unrelated entries from other sections (id, label) for topic switches.

usage: python3 t5_shards.py   -> shards/T5_NNN.json
"""

from __future__ import annotations

import json
import random

from common import DEPTH, app, entries

PER = 25


def cut(t: str, n: int = 220) -> str:
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[: n].rsplit(" ", 1)[0] + "…"


def main() -> None:
    E, nat = entries(), app("natural_replies.json")
    ids = list(E)
    rnd = random.Random(20261124)
    rows = []
    for eid in ids:
        e = E[eid]
        rel = [r for r in (e.get("related") or []) if r in E][:4]
        others = [x for x in ids if E[x]["section"] != e["section"] and E[x]["section"] != "conversation"]
        rows.append({
            "entry_id": eid, "section": e["section"], "kind": e.get("kind"), "label": e["label"],
            "L0": cut(nat.get(eid, (e.get("answer") or {}).get("short", "")), 400),
            "examples": (e.get("examples") or [])[:3],
            "related": [{"id": r, "label": E[r]["label"], "L0": cut(nat.get(r, ""))} for r in rel],
            "unrelated": [{"id": x, "label": E[x]["label"]} for x in rnd.sample(others, 5)],
        })
    out = DEPTH / "shards"
    for i in range(0, len(rows), PER):
        (out / f"T5_{i // PER:03d}.json").write_text(json.dumps(
            {"shard": f"T5_{i // PER:03d}", "entries": rows[i: i + PER]}, ensure_ascii=False, indent=0))
    print("entries", len(rows), "shards", (len(rows) + PER - 1) // PER,
          "no related", sum(1 for r in rows if not r["related"]))


if __name__ == "__main__":
    main()
