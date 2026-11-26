"""T0 inputs and per-task shards for depth_v1.

usage: python3 digest.py t0            -> inputs/{headroom,detail_overlap,baseline}.jsonl/json
       python3 digest.py followups     -> inputs/followup_failures.jsonl (needs inputs/ft4_dump_v*.jsonl)
       python3 digest.py snapshot      -> inputs/snapshot_sha256.json
"""

from __future__ import annotations

import hashlib
import re
import json
import sys
from collections import Counter, defaultdict

from common import APP, DEPTH, SECTIONS, app, content_words, emergency_ids, entries, entry_facts_text, exempt, write_jsonl
from evidence import ranked_windows

INP = DEPTH / "inputs"
CUE = json.loads((DEPTH.parents[1] / "mobile/assets/data/knowledge/policy.json").read_text())["followup"]["cue"]


def snapshot() -> None:
    out = {}
    for d in (SECTIONS, APP):
        for p in sorted(d.glob("*.json")):
            out[str(p.relative_to(d.parents[2]))] = hashlib.sha256(p.read_bytes()).hexdigest()
    (INP / "snapshot_sha256.json").write_text(json.dumps(out, indent=1))
    print(f"snapshot: {len(out)} files")


def novel(text: str, l0: set[str]) -> set[str]:
    return content_words(text) - l0


def t0() -> None:
    E = entries()
    nat, aug, conv = app("natural_replies.json"), app("aug_queries.json"), app("followup_convs.json")
    head, over, base = [], [], {}
    hist = defaultdict(Counter)
    for eid, e in E.items():
        a = e.get("answer") or {}
        l0 = nat.get(eid, a.get("short", ""))
        l0w = content_words(l0)
        corpus_extra = set()
        for f in ("detail", "reflection", "steps", "variants"):
            v = a.get(f)
            if v:
                corpus_extra |= novel(json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v, l0w)
        wins = [] if exempt(e) else ranked_windows(eid, k=6)
        ev_extra = set()
        for w in wins:
            if w["score"] >= 1.0:
                ev_extra |= novel(w["text"], l0w)
        n = len(corpus_extra) + len(ev_extra)
        cls = "exempt" if exempt(e) else ("rich" if n >= 40 else "some" if n >= 12 else "none")
        hist[e["section"]][cls] += 1
        head.append({
            "entry_id": eid, "section": e["section"], "kind": e.get("kind"), "class": cls,
            "source_urls": [s["url"] for s in e.get("sources", [])],
            "corpus_novel_words": len(corpus_extra), "evidence_novel_words": len(ev_extra),
            "windows": [{"qid": w["qid"], "score": w["score"]} for w in wins],
        })
        d = a.get("detail")
        if d:
            dw = content_words(d if isinstance(d, str) else json.dumps(d, ensure_ascii=False))
            over.append({"entry_id": eid, "detail_words": len(dw), "in_l0": round(len(dw & l0w) / max(len(dw), 1), 3)})
        base[eid] = {"examples": len(e.get("examples", [])), "aug": len(aug.get(eid, [])), "convs": len(conv.get(eid, []))}
    write_jsonl(INP / "headroom.jsonl", head)
    write_jsonl(INP / "detail_overlap.jsonl", over)
    (INP / "baseline.json").write_text(json.dumps(base, indent=0))
    (INP / "headroom_hist.json").write_text(json.dumps({s: dict(c) for s, c in hist.items()}, indent=1))
    tot = Counter()
    for c in hist.values():
        tot.update(c)
    print("headroom", dict(tot))
    for s, c in hist.items():
        print(f"  {s:18s} {dict(c)}")


def followups() -> None:
    E = entries()
    rel = {k: set(v.get("related", [])) for k, v in E.items()}
    rows = []
    for v in ("v2", "v3"):
        p = INP / f"ft4_dump_{v}.jsonl"
        if not p.exists():
            print("missing", p)
            continue
        for l in p.read_text().splitlines():
            r = json.loads(l)
            if len(r["turns"]) < 2 or r["ok"]:
                continue
            acc = set(r["acceptable"])
            pred = r["pred"]
            if pred and any(pred in rel.get(x, set()) or x in rel.get(pred, set()) for x in acc):
                cls = "label"  # neighbour of a gold id: plausibly a labelling or granularity issue
            elif not (re.match(CUE, r["turns"][-1], re.I) or len(r["turns"][-1].split()) <= 5):
                cls = "gate_miss"  # neither the cue nor the short rule could fire: context never used
            else:
                cls = "fused_wrong"
            rows.append({"set": v, "qid": r["qid"], "turns": r["turns"], "pred": pred, "acceptable": r["acceptable"], "class": cls})
    write_jsonl(INP / "followup_failures.jsonl", rows)
    print(Counter((r["set"], r["class"]) for r in rows))



# --- T3.0 fact-inventory shards -------------------------------------------------------------


def t30() -> None:
    from evidence import ranked_windows
    E = entries()
    nat, aug = app("natural_replies.json"), app("aug_queries.json")
    emerg = emergency_ids()
    from common import SECTION_ORDER
    ids = [i for s in SECTION_ORDER for i, e in E.items() if e["section"] == s and not exempt(e)]
    out = DEPTH / "shards"
    n = 0
    for k in range(0, len(ids), 10):
        rows = []
        for eid in ids[k:k + 10]:
            e = E[eid]
            a = e.get("answer") or {}
            forced = e.get("kind") in ("safety", "rule", "action") or eid in emerg
            rows.append({
                "entry_id": eid, "section": e["section"], "kind": e.get("kind"), "label": e["label"],
                "all_key_forced": forced, "L0": nat.get(eid, a.get("short")),
                "answer": {f: a.get(f) for f in ("short", "variants", "steps", "detail", "reflection") if a.get(f)},
                "questions": (e.get("examples") or [])[:14] + (aug.get(eid) or [])[:12],
                "evidence_windows": [] if forced else ranked_windows(eid, k=8),
            })
        (out / f"T30_{n:03d}.json").write_text(json.dumps({"shard": f"T30_{n:03d}", "entries": rows}, ensure_ascii=False, indent=1))
        n += 1
    print("T3.0 shards", n, "entries", len(ids))


if __name__ == "__main__":
    {"t0": t0, "followups": followups, "snapshot": snapshot, "t30": t30}[sys.argv[1]]()
