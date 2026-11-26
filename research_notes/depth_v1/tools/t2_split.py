"""Split blind_v4/gold.jsonl into v4_dev (40 %) and v4_sealed (60 %) by conversation hash, and write
the dev set in gguf_eval --blind format. All turns of one conversation (qid) land on the same side.

v4_sealed is written once, its sha256 recorded, and never opened again in this mission.
Continuation turns (is_continuation true) are not an entry-retrieval question: they go to
v4_dev/continuation.jsonl for the T7 policy check instead of the gguf_eval set.

usage: python3 t2_split.py
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter

from common import DEPTH

V4 = DEPTH / "blind_v4"


def side(qid: str) -> str:
    return "dev" if int(hashlib.sha256(qid.encode()).hexdigest(), 16) % 100 < 40 else "sealed"


def main() -> None:
    rows = [json.loads(l) for l in (V4 / "gold.jsonl").read_text().splitlines() if l.strip()]
    dev, sealed = [r for r in rows if side(r["qid"]) == "dev"], [r for r in rows if side(r["qid"]) == "sealed"]
    sp = V4 / "v4_sealed.jsonl"
    if sp.exists():
        raise SystemExit("v4_sealed.jsonl already exists; it is never rewritten")
    sp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sealed))
    (V4 / "v4_sealed.sha256").write_text(f"{hashlib.sha256(sp.read_bytes()).hexdigest()}  v4_sealed.jsonl\n")
    d = V4 / "v4_dev"
    d.mkdir(exist_ok=True)
    (d / "gold_dev.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in dev))
    q, lab, cont = [], [], []
    for r in dev:
        if r["is_continuation"] is not None:
            cont.append({"uid": r["uid"], "turns": r["turns"], "is_continuation": r["is_continuation"],
                         "acceptable": r["acceptable_ids"]})
        if r["is_continuation"]:
            continue
        style = "single" if r["type"] == "single" else f"{r['type']}_t{min(r['turn'], 3)}"
        q.append({"qid": r["uid"], "turns": r["turns"], "style": style})
        lab.append({"qid": r["uid"], "acceptable": r["acceptable_ids"]})
    (d / "queries_v4.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in q))
    (d / "labels_v4.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lab))
    (d / "continuation.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in cont))
    print("dev", len(dev), "sealed", len(sealed), "eval rows", len(q), Counter(x["style"] for x in q),
          "continuation", Counter(x["is_continuation"] for x in cont))


if __name__ == "__main__":
    main()
