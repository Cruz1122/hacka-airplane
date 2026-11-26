"""Build the second-review input for T5b shard S: the candidate texts (first-review ok, or fix
with an arbitrated ok, using fixed_text) of kind safety/rule and emergency entries.

usage: python3 t5b_second.py T5b_000   -> proposals/T5b_000_2.jsonl (prints the row count)
"""

from __future__ import annotations

import json
import sys

from common import DEPTH, app, emergency_ids, entries, read_jsonl
from t5b_merge import needs_second, opt


def build(s: str) -> int:
    E, emer = entries(), emergency_ids()
    inv, nat = app("fact_inventory.json"), app("natural_replies.json")

    def facts(eid: str) -> dict:
        # rows carry the entry facts so a reviewer never judges without them (DECISION_LOG 19)
        fs = inv.get(eid, [])
        return {"canonical_L0": nat.get(eid, ""),
                "key_facts": [f["text"] for f in fs if f["class"] == "key"],
                "complements": {f["fid"]: f["text"] for f in fs if f["class"] == "complement"}}
    rev = opt(DEPTH / f"reviews/{s}.jsonl")
    arb = opt(DEPTH / f"arb_out/{s}.jsonl")
    out = []
    for p in read_jsonl(DEPTH / f"proposals/{s}.jsonl"):
        e, r = E.get(p["entry_id"]), rev.get(p["pid"])
        if not e or not r or not needs_second(e, emer):
            continue
        if r.get("verdict") == "ok":
            out.append({**p, "emergency": p["entry_id"] in emer, "entry": facts(p["entry_id"])})
        elif r.get("verdict") == "fix" and arb.get(p["pid"], {}).get("verdict") == "ok":
            out.append({**p, "text": r.get("fixed_text") or p["text"], "emergency": p["entry_id"] in emer, "entry": facts(p["entry_id"])})
    (DEPTH / f"proposals/{s}_2.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    return len(out)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(a, build(a))
