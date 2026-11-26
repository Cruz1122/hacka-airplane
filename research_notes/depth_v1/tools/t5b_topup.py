"""T5b step 5: top-up shards for entries below goal after merge + arbitration.

For each given shard S, runs the same selection as check_replies on resolved/S.jsonl and collects
the entries below goal. Writes shards/T5b_U<nn>.json (10 entries each): the T5b shard row plus
`approved` (texts already kept, which the new ones must differ from) and `need`. Also writes
resolved/T5b_U<nn>.base.jsonl, the approved rows, for the writer's self-check:

  python3 check_replies.py proposals/T5b_U<nn>.jsonl --base resolved/T5b_U<nn>.base.jsonl

usage: python3 t5b_topup.py T5b_000 T5b_001 ...   (prints the shard names it made)
"""

from __future__ import annotations

import json
import subprocess
import sys

from common import DEPTH, app, emergency_ids, entries, read_jsonl
from t5b_shards import row

PER, GOAL = 10, 8


def main() -> None:
    E, inv, nat, emer = entries(), app("fact_inventory.json"), app("natural_replies.json"), emergency_ids()
    todo = []
    for s in sys.argv[1:]:
        # after a first top-up round, t5b_final.py writes S.all.jsonl (parent + approved top-ups)
        res = DEPTH / f"resolved/{s}.all.jsonl"
        if not res.exists():
            res = DEPTH / f"resolved/{s}.jsonl"
        clean = DEPTH / f"resolved/{s}.clean.jsonl"
        subprocess.run([sys.executable, "check_replies.py", str(res), "--write", str(clean), "--quiet"],
                       check=True, cwd=DEPTH / "tools", stdout=subprocess.DEVNULL)
        low = json.loads(clean.with_suffix(".low.json").read_text())
        kept = read_jsonl(clean)
        for eid, v in low.items():
            appr = [r for r in kept if r["entry_id"] == eid]
            todo.append((eid, appr, max(GOAL - v["kept"], 0) + 3))
        # an entry whose every row was dropped is absent from the check report: it needs a full set
        seen = {r["entry_id"] for r in kept} | set(low)
        for e in json.loads((DEPTH / f"shards/{s}.json").read_text())["entries"]:
            if e["entry_id"] not in seen:
                todo.append((e["entry_id"], [], GOAL + 3))
    existing = sorted(p.stem for p in (DEPTH / "shards").glob("T5b_U*.json"))
    n = len(existing)
    made = []
    for k in range(0, len(todo), PER):
        name = f"T5b_U{n + k // PER:02d}"
        chunk = todo[k:k + PER]
        rows = []
        for eid, appr, need in chunk:
            rows.append({**row(E[eid] | {"id": eid}, inv, nat, emer), "need": need,
                         "approved": [{"pid": r["pid"], "structure": r["structure"], "atoms": r.get("atoms", []),
                                       "text": r["text"]} for r in appr]})
        (DEPTH / f"shards/{name}.json").write_text(json.dumps(
            {"shard": name, "entries": rows}, ensure_ascii=False, indent=1))
        (DEPTH / f"resolved/{name}.base.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for _, appr, _ in chunk for r in appr))
        made.append((name, len(chunk), sum(x[2] for x in chunk)))
    print("made", made)


if __name__ == "__main__":
    main()
