"""Merge blind_v4 labels_a + labels_b; route disagreements to arbitration; assemble the final set.

Script rules (never model judgment):
- cont_pos/cont_neg turn 1: a null is_continuation means false (labelers left it unset on negatives).
- exact agreement -> accepted.
- sets differ only by hub.* ids -> union accepted (hub credit is a separate metric; strict drops hubs).
- anything else (disputed ids, out_of_scope or is_continuation disagreement) -> arbitration.

usage: python3 t2_merge.py arb     -> blind_v4/arb_shards/A##.json + blind_v4/agreed.jsonl
       python3 t2_merge.py final   -> blind_v4/gold.jsonl (agreed + blind_v4/arb/A##.jsonl)
"""

from __future__ import annotations

import json
import sys
from collections import Counter

from common import DEPTH

V4 = DEPTH / "blind_v4"
PER_ARB = 90


def load(p):
    out = {}
    if p.exists():
        for l in p.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                out[r["uid"]] = r
    return out


def shards():
    return sorted(p for p in (V4 / "label_shards").glob("L??.json"))


def labels(kind: str) -> dict:
    out = {}
    for p in sorted((V4 / f"labels_{kind}").glob("L*.jsonl")):
        out.update(load(p))
    return out


def norm(u: dict, r: dict) -> dict:
    cont = r.get("is_continuation")
    if u["type"] in ("cont_pos", "cont_neg") and u["turn"] == 1:
        cont = bool(cont)
    else:
        cont = None
    ids = [] if cont else sorted(set(r.get("acceptable_ids") or []))
    return {"acceptable_ids": ids, "out_of_scope": bool(r.get("out_of_scope")), "is_continuation": cont}


def arb() -> None:
    A, B = labels("a"), labels("b")
    agreed, disputes, why, catalog = [], [], Counter(), {}
    for p in shards():
        d = json.loads(p.read_text())
        catalog.update(d["catalog"])
        for u in d["units"]:
            a, b = A.get(u["uid"]), B.get(u["uid"])
            if not a or not b:
                why["missing"] += 1
                continue
            na, nb = norm(u, a), norm(u, b)
            sa, sb = set(na["acceptable_ids"]), set(nb["acceptable_ids"])
            base = {"uid": u["uid"], "qid": u["qid"], "type": u["type"], "turn": u["turn"], "turns": u["turns"]}
            if na == nb:
                why["agree"] += 1
                agreed.append({**base, **na, "how": "agree"})
            elif na["is_continuation"] == nb["is_continuation"] and na["out_of_scope"] == nb["out_of_scope"] \
                    and sa & sb and all(x.startswith("hub.") for x in sa ^ sb):
                why["hub_union"] += 1
                agreed.append({**base, **na, "acceptable_ids": sorted(sa | sb), "how": "hub_union"})
            else:
                why["dispute"] += 1
                disputes.append({**base, "candidates": u["candidates"], "both": sorted(sa & sb),
                                 "disputed": sorted(sa ^ sb), "A": na, "B": nb})
    (V4 / "agreed.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in agreed))
    out = V4 / "arb_shards"
    out.mkdir(exist_ok=True)
    for i in range(0, len(disputes), PER_ARB):
        part = disputes[i: i + PER_ARB]
        ids = {c for u in part for c in u["candidates"]}
        (out / f"A{i // PER_ARB:02d}.json").write_text(json.dumps(
            {"shard": f"A{i // PER_ARB:02d}", "units": part, "catalog": {k: v for k, v in catalog.items() if k in ids}},
            ensure_ascii=False, indent=0))
    print(dict(why), "arb shards", (len(disputes) + PER_ARB - 1) // PER_ARB)


def final() -> None:
    rows = [json.loads(l) for l in (V4 / "agreed.jsonl").read_text().splitlines()]
    arbs = {}
    for p in sorted((V4 / "arb").glob("A*.jsonl")):
        arbs.update(load(p))
    missing, seen = 0, set()
    for p in sorted((V4 / "arb_shards").glob("A*.json")):
        for u in json.loads(p.read_text())["units"]:
            if u["uid"] in seen:  # A02x-style top-up shards repeat units of their parent shard
                continue
            seen.add(u["uid"])
            r = arbs.get(u["uid"])
            if not r:
                missing += 1
                continue
            ok = set(u["candidates"])
            ids = sorted(x for x in (r.get("acceptable_ids") or []) if x in ok)
            cont = r.get("is_continuation") if u["type"] in ("cont_pos", "cont_neg") and u["turn"] == 1 else None
            rows.append({k: u[k] for k in ("uid", "qid", "type", "turn", "turns")} | {
                "acceptable_ids": [] if cont else ids, "out_of_scope": bool(r.get("out_of_scope")),
                "is_continuation": cont, "how": "arbitrated"})
    rows.sort(key=lambda r: r["uid"])
    (V4 / "gold.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print("gold", len(rows), Counter(r["how"] for r in rows), "arb missing", missing)


if __name__ == "__main__":
    {"arb": arb, "final": final}[sys.argv[1]]()
