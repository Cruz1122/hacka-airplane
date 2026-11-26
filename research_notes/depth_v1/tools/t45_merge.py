"""Apply T4/T5 reviews to proposals. Script rules only; the reviewer's verdict decides, except:

- T5 `drop` whose note says a turn copies an example, when the copy is ONLY in an intermediate turn
  (not the last, labelled turn): kept. The copied turn is context with a correct label; the
  conversation still adds a new last-turn pair (DECISION_LOG 12).
- `fix` rows are never applied by script: they go to arb_queue/<shard>.jsonl for Luna arbitration;
  their arbitration result (arb_out/<shard>.jsonl) is merged when present.

usage: python3 t45_merge.py T4_000 [T5_000 ...]   -> resolved/<shard>.jsonl, arb_queue/<shard>.jsonl
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter

from common import DEPTH, entries, fold, read_jsonl

COPY_NOTE = re.compile(r"verbatim|example|ejemplo|copia|copies", re.I)


def k(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(t)))


def merge(shard: str) -> None:
    E = entries()
    t5 = shard.startswith("T5_")
    idk = "conv_id" if t5 else "vid"
    props = read_jsonl(DEPTH / f"proposals/{shard}.jsonl")
    revs = {r[idk]: r for r in read_jsonl(DEPTH / f"reviews/{shard}.jsonl")}
    redo = DEPTH / f"reviews/{shard}f.jsonl"  # re-review of rows a reviewer misjudged (DECISION_LOG 13)
    if redo.exists():
        revs.update({r[idk]: r for r in read_jsonl(redo)})
    arbp = DEPTH / f"arb_out/{shard}.jsonl"
    arbs = {r[idk]: r for r in read_jsonl(arbp)} if arbp.exists() else {}
    ex = {eid: {k(x) for x in (e.get("examples") or [])} for eid, e in E.items()}
    keep, queue, why = [], [], Counter()
    for p in props:
        r = revs.get(p[idk])
        if not r:
            why["no review"] += 1
            continue
        v = r.get("verdict")
        if v == "fix":
            a = arbs.get(p[idk])
            if not a:
                queue.append({"row": p, "review": r})
                why["fix -> queue"] += 1
                continue
            v = a.get("verdict")
            if v == "ok" and t5 and a.get("turn_fixes"):
                for f in a["turn_fixes"]:
                    if f.get("entry_id") in E and 0 <= f.get("i", -1) < len(p["turns"]) - 1:
                        p["turns"][f["i"]]["entry_id"] = f["entry_id"]
            if v == "ok" and not t5 and a.get("entry_id") in E:
                p["entry_id"] = a["entry_id"]
            why[f"arbitrated:{v}"] += 1
        if v == "drop" and t5 and COPY_NOTE.search(r.get("note") or ""):
            hits = [i for i, t in enumerate(p["turns"])
                    if k(t["text"]) in ex.get(t["entry_id"], set()) | ex.get(p["entry_id"], set())]
            if hits and max(hits) < len(p["turns"]) - 1:
                v = "ok"
                why["kept: intermediate example copy"] += 1
        if v == "ok":
            keep.append({**p, "by_review": r.get("verdict")})
            why["ok"] += 1
        else:
            why[str(v)] += 1
    (DEPTH / "resolved").mkdir(exist_ok=True)
    (DEPTH / f"resolved/{shard}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in keep))
    q = DEPTH / f"arb_queue/{shard}.jsonl"
    q.parent.mkdir(exist_ok=True)
    q.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in queue))
    per = Counter(x["entry_id"] for x in keep)
    print(shard, dict(why), "entries", len(per), "min/entry", min(per.values()) if per else 0)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        merge(s)
