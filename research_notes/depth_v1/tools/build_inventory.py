"""T3.0 integration: resolved/T30_*.jsonl -> data/knowledge/app/fact_inventory.json (R7.1).

Script only. Rows come from check_facts.py --write, so support and purges are already checked;
this re-asserts the forced-key rule per entry and the coverage goal (every non-exempt entry).

usage: python3 build_inventory.py [--check]   (--check: report only, write nothing)
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter

from common import APP, DEPTH, emergency_ids, entries, exempt, read_jsonl

SHARD = re.compile(r"^T30_\d{3}x?$")  # skips pilot / k8 experiment files


def main() -> int:
    E = entries()
    emerg = emergency_ids()
    inv: dict[str, list] = {}
    for p in sorted((DEPTH / "resolved").glob("T30_*.jsonl")):
        if not SHARD.match(p.stem):
            continue
        for r in read_jsonl(p):
            if r["entry_id"] in E and r.get("facts"):
                inv[r["entry_id"]] = r["facts"]  # later files (e.g. 041x top-up) win
    errors = []
    for eid, facts in inv.items():
        e = E[eid]
        fids = [f["fid"] for f in facts]
        if len(set(fids)) != len(fids):
            errors.append(f"{eid}: duplicate fid")
        if not any(f["class"] == "key" for f in facts):
            errors.append(f"{eid}: no key fact")
        if (e.get("kind") in ("safety", "rule", "action") or eid in emerg) and any(f["class"] != "key" for f in facts):
            errors.append(f"{eid}: forced-key entry has a complement")
    missing = sorted(eid for eid, e in E.items() if not exempt(e) and eid not in inv)
    cls = Counter(f["class"] for fs in inv.values() for f in fs)
    zero = sum(1 for fs in inv.values() if not any(f["class"] == "complement" for f in fs))
    print(json.dumps({"entries": len(inv), "non_exempt_missing": missing, "facts": dict(cls),
                      "entries_without_complement": zero, "errors": errors[:20], "n_errors": len(errors)},
                     ensure_ascii=False))
    if errors or missing:
        return 1
    if "--check" not in sys.argv:
        out = {eid: inv[eid] for eid in sorted(inv)}
        (APP / "fact_inventory.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        print("wrote", APP / "fact_inventory.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
