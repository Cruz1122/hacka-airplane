"""Script checks on T3 layer rows (DECISION_LOG 26). Row (JSONL), one per layer text:
{"lid": "<entry_id>#L1a", "entry_id", "layer": 1|2, "kind": "why|how|specifics", "atoms": [fid], "text"}

Per row: entry in the shard set; layer <= layers_wanted; kind valid (layer 2 = specifics);
atoms non-empty complement fids; every number in the text is in its atoms, the key facts or L0;
every number of its atoms is in the text; 20-90 words; no emoji.
Per entry: texts of one layer share their atoms; two layers share no atom.

usage: python3 check_layers.py <rows.jsonl> [--write <clean.jsonl>]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from check_facts import nums
from common import app, read_jsonl

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
KINDS = {1: {"why", "how"}, 2: {"specifics"}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", type=Path)
    ap.add_argument("--write", type=Path)
    a = ap.parse_args()
    inv, nat = app("fact_inventory.json"), app("natural_replies.json")
    why, keep, bad_rows = Counter(), [], []
    for r in read_jsonl(a.rows):
        eid, text, atoms = r.get("entry_id"), r.get("text") or "", r.get("atoms") or []
        facts = inv.get(eid, [])
        comp = {f["fid"]: f["text"] for f in facts if f["class"] == "complement"}
        wanted = 1 if len(comp) < 4 else 2
        keyn = set().union(set(), *[nums(f["text"]) for f in facts if f["class"] == "key"])
        atomn = set().union(set(), *[nums(comp[x]) for x in atoms if x in comp])
        tn, nw = nums(text), len(text.split())
        bad = None
        if len(comp) < 2:
            bad = "entry has < 2 complements"
        elif r.get("layer") not in (1, 2) or r["layer"] > wanted:
            bad = "bad layer"
        elif r.get("kind") not in KINDS[r["layer"]]:
            bad = "bad kind"
        elif not atoms or any(x not in comp for x in atoms):
            bad = "atoms empty or not complement fids"
        elif atomn - tn:
            bad = f"missing number {sorted(atomn - tn)}"
        elif tn - (atomn | keyn | nums(nat.get(eid, ""))):
            bad = f"number outside its facts {sorted(tn - (atomn | keyn | nums(nat.get(eid, ''))))}"
        elif not 20 <= nw <= 90:
            bad = f"{nw} words"
        elif EMOJI.search(text):
            bad = "emoji"
        if bad:
            why[bad.split(" [")[0]] += 1
            bad_rows.append(f"{r.get('lid')}: {bad}")
            continue
        keep.append(r)
    # per entry: one atom set per layer, layers disjoint
    groups: dict[str, dict[int, list]] = defaultdict(lambda: defaultdict(list))
    for r in keep:
        groups[r["entry_id"]][r["layer"]].append(r)
    final = []
    for eid, layers in groups.items():
        sets = {}
        for layer, rows in layers.items():
            s = [frozenset(r["atoms"]) for r in rows]
            if len(set(s)) > 1:
                why["layer texts with different atoms"] += 1
                bad_rows.append(f"{eid} L{layer}: texts carry different atoms")
            sets[layer] = s[0]
        if len(sets) == 2 and sets[1] & sets[2]:
            why["layers share atoms"] += 1
            bad_rows.append(f"{eid}: layers share {sorted(sets[1] & sets[2])}")
            continue
        final += [r for rows in layers.values() for r in rows]
    if a.write:
        a.write.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final))
    for b in bad_rows:
        print("  ", b)
    print(json.dumps({"rows_kept": len(final), "rejected": dict(why), "entries": len(groups)}))


if __name__ == "__main__":
    main()
