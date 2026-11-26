"""Apply T5b reviews to L0 paraphrase proposals. Script rules only.

Inputs per shard S:
  proposals/S.jsonl        writer rows
  reviews/S.jsonl          first review (Luna): verdict ok|fix|drop, fixed_text for fix
  reviews/S_2.jsonl        second review (fresh Luna) for kind safety/rule and emergency entries
                           (R6.6 / T5b step 2): must also be ok; carries emergency_ok
  arb_out/S.jsonl          arbitration of fixes: {pid, verdict ok|drop}; ok -> fixed_text is used
Outputs:
  resolved/S.jsonl         approved rows (then run check_replies.py on it)
  arb_queue/S.jsonl        fixes without arbitration
  second_queue/S.json      entry ids still waiting for the second review

usage: python3 t5b_merge.py T5b_000 [T5b_001 ...]
"""

from __future__ import annotations

import json
import sys
from collections import Counter

from common import DEPTH, app, emergency_ids, entries, read_jsonl


def opt(path):
    return {r["pid"]: r for r in read_jsonl(path)} if path.exists() else {}


def needs_second(e: dict, emer: set) -> bool:
    return e.get("kind") in ("safety", "rule") or e["id"] in emer


def merge(s: str) -> None:
    E, emer = entries(), emergency_ids()
    props = read_jsonl(DEPTH / f"proposals/{s}.jsonl")
    rev = opt(DEPTH / f"reviews/{s}.jsonl")
    rev2 = opt(DEPTH / f"reviews/{s}_2.jsonl")
    arb = opt(DEPTH / f"arb_out/{s}.jsonl")
    inv, nat = app("fact_inventory.json"), app("natural_replies.json")
    keep, queue, waiting, why = [], [], set(), Counter()
    for p in props:
        r = rev.get(p["pid"])
        if not r:
            why["no review"] += 1
            continue
        row, v = dict(p), r.get("verdict")
        if v == "fix":
            a = arb.get(p["pid"])
            if not a:
                # the arbiter judges fixed_text against the entry's facts, so the queue row carries them
                facts = inv.get(p["entry_id"], [])
                queue.append({"row": p, "review": r, "entry": {
                    "canonical_L0": nat.get(p["entry_id"], ""),
                    "key_facts": [f["text"] for f in facts if f["class"] == "key"],
                    "complements": {f["fid"]: f["text"] for f in facts if f["class"] == "complement"}}})
                why["fix -> queue"] += 1
                continue
            v = a.get("verdict")
            if v == "ok":
                row["text"] = r.get("fixed_text") or p["text"]
                row["fixed"] = True
        if v != "ok":
            why[str(v)] += 1
            continue
        e = E.get(p["entry_id"])
        if e and needs_second(e, emer):
            r2 = rev2.get(p["pid"])
            if not r2:
                waiting.add(p["entry_id"])
                why["waiting second review"] += 1
                continue
            if r2.get("verdict") != "ok":
                why["second review " + str(r2.get("verdict"))] += 1
                continue
            if p["entry_id"] in emer:
                row["emergency_ok"] = bool(r2.get("emergency_ok"))
        keep.append(row)
        why["ok"] += 1
    for d, rows in (("resolved", keep), ("arb_queue", queue)):
        (DEPTH / d).mkdir(exist_ok=True)
        (DEPTH / f"{d}/{s}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    (DEPTH / "second_queue").mkdir(exist_ok=True)
    (DEPTH / f"second_queue/{s}.json").write_text(json.dumps(sorted(waiting)))
    print(s, dict(why))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        merge(a)
