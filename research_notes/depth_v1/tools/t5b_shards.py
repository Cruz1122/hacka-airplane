"""T5b L0 paraphrase shards (10 entries each) from fact_inventory.json + natural_replies.json.

usage: python3 t5b_shards.py            -> shards/T5b_000..NNN.json (never rewrites an existing file)
       python3 t5b_shards.py --pilot    -> shards/T5b_P00.json (10 mixed entries for the pilot)
"""

from __future__ import annotations

import json
import sys

from common import DEPTH, SECTION_ORDER, app, emergency_ids, entries, exempt
from check_facts import nums
from check_replies import strip_markers

PER = 10


def row(e: dict, inv: dict, nat: dict, emer: set) -> dict:
    facts = inv[e["id"]]
    comp = [{"fid": f["fid"], "text": f["text"]} for f in facts if f["class"] == "complement"]
    keyf = [{"fid": f["fid"], "text": f["text"]} for f in facts if f["class"] == "key"]
    l0 = nat.get(e["id"], "")
    keyn = set().union(*[nums(f["text"]) for f in keyf])
    compn = set().union(*[nums(f["text"]) for f in comp])
    req = sorted((nums(strip_markers(l0)) - (compn - keyn)) | keyn)
    return {
        "entry_id": e["id"], "kind": e.get("kind"), "section": e["section"],
        "emergency": e["id"] in emer, "label": e.get("label") or e.get("title"),
        "canonical_L0": l0, "key_facts": keyf, "complements": comp,
        "max_atoms": len(comp) // 2 if len(comp) >= 2 else len(comp),
        "numbers_required": req,
    }


def main() -> None:
    E, inv, nat, emer = entries(), app("fact_inventory.json"), app("natural_replies.json"), emergency_ids()
    todo = [e for s in SECTION_ORDER for e in E.values() if e["section"] == s and not exempt(e)]
    out = DEPTH / "shards"
    if "--pilot" in sys.argv:
        pick, want = [], [
            lambda e: e.get("kind") == "safety" and e["id"] not in emer,
            lambda e: e["id"] in emer,
            lambda e: e["id"] in emer and e.get("kind") != "safety",
            lambda e: e.get("kind") == "rule",
            lambda e: not any(f["class"] == "complement" for f in inv[e["id"]]) and e.get("kind") == "fact",
            lambda e: sum(f["class"] == "complement" for f in inv[e["id"]]) >= 6,
            lambda e: sum(f["class"] == "complement" for f in inv[e["id"]]) >= 6 and e.get("kind") == "procedure",
            lambda e: sum(f["class"] == "complement" for f in inv[e["id"]]) in (2, 3),
            lambda e: e["section"] == "booking_fees",
            lambda e: e.get("kind") == "explanation",
        ]
        for w in want:
            pick.append(next(e for e in todo if w(e) and e not in pick))
        (out / "T5b_P00.json").write_text(json.dumps(
            {"shard": "T5b_P00", "per_entry": 10, "entries": [row(e, inv, nat, emer) for e in pick]},
            ensure_ascii=False, indent=1))
        print("pilot", [e["id"] for e in pick])
        return
    made = []
    for k in range(0, len(todo), PER):
        name = f"T5b_{k // PER:03d}"
        p = out / f"{name}.json"
        if p.exists():
            continue
        p.write_text(json.dumps({"shard": name, "per_entry": 10,
                                 "entries": [row(e, inv, nat, emer) for e in todo[k:k + PER]]},
                                ensure_ascii=False, indent=1))
        made.append(name)
    print("made", len(made), made[:3], "...", made[-1:] if made else "")


if __name__ == "__main__":
    main()
