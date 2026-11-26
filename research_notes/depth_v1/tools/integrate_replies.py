"""Write the T5b reply paraphrases for the app (R6, R7), from the final shard files only.

Re-runs t5b_final.py on every parent shard that has a resolved file, then reads
resolved/T5b_NNN.final.jsonl (the pilot T5b_P00 repeats entries of the real shards and is skipped).

  python3 integrate_replies.py
  -> data/knowledge/app/reply_variants.json  {entry_id: [{text, atoms, emergency_ok?}]}
  -> data/knowledge/app/depth_replies.json   {} when absent: depth layers (T3) are not written yet,
     and export_nlu.py needs all three depth files before it emits depth.json

Guards (each one fails the run):
- an entry in two final files;
- a row of a safety, rule or emergency entry without an ok second review (R6.6, T5b step 2);
- an empty list (an entry with no approved text is left out, so its canonical text serves).
The canonical L0 is the first text only for entries with fewer than 2 complements (R7.6); it is
never emergency_ok, so emergency entries rotate over second-verifier texts only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from common import DEPTH, app, emergency_ids, entries, read_jsonl  # noqa: E402
from t5b_merge import needs_second  # noqa: E402

APP = DEPTH.parents[1] / "data/knowledge/app"
GOAL = 8


def main() -> None:
    parents = sorted(p.stem for p in (DEPTH / "shards").glob("T5b_[0-9][0-9][0-9].json")
                     if (DEPTH / f"resolved/{p.stem}.jsonl").exists())
    for s in parents:
        subprocess.run([sys.executable, "t5b_final.py", s], check=True, cwd=TOOLS, capture_output=True)

    E, emer = entries(), emergency_ids()
    inv, nat = app("fact_inventory.json"), app("natural_replies.json")
    # second-review verdicts per (source shard, pid): top-ups reuse pids, so a pid alone is ambiguous
    second = {}
    for p in sorted((DEPTH / "reviews").glob("T5b_*_2.jsonl")):
        src = p.stem[: -len("_2")]
        for r in read_jsonl(p):
            second[(src, r["pid"])] = r.get("verdict")

    out: dict[str, list[dict]] = {}
    owner: dict[str, str] = {}
    owner_chat: set[str] = set()
    for s in parents:
        for r in read_jsonl(DEPTH / f"resolved/{s}.final.jsonl"):
            eid = r["entry_id"]
            if owner.setdefault(eid, s) != s:
                sys.exit(f"{eid} is in {owner[eid]} and {s}")
            if needs_second(E[eid], emer) and second.get((r["src"], r["pid"].split("@")[0])) != "ok":
                sys.exit(f"{r['pid']} ({s}) has no ok second review")
            t = {"text": r["text"], "atoms": list(r.get("atoms", []))}
            if eid in emer:
                t["emergency_ok"] = bool(r.get("emergency_ok"))
            out.setdefault(eid, []).append(t)

    for eid, texts in out.items():
        ncomp = sum(1 for f in inv.get(eid, []) if f["class"] == "complement")
        if ncomp >= 2:
            # R7.3 / A13: with more than GOAL-1 texts without complements, 8 asks in a row can all
            # land on them and show one subset; capping them keeps a complement in every 8 picks.
            bare = [t for t in texts if not t["atoms"]]
            if len(bare) > GOAL - 1 and len(texts) - (len(bare) - (GOAL - 1)) >= GOAL:
                drop = {id(t) for t in bare[GOAL - 1:]}
                texts[:] = [t for t in texts if id(t) not in drop]
        if ncomp < 2 and nat.get(eid):
            texts.insert(0, {"text": nat[eid], "atoms": [], **({"emergency_ok": False} if eid in emer else {})})
    # Small-talk entries are exempt from T5b; their rotation comes from the CHAT batch
    # (briefs/CHAT_writer.md, reviewed in reviews/CHAT.jsonl). Canonical text stays first.
    chat = DEPTH / "proposals/CHAT.jsonl"
    if chat.exists() and (DEPTH / "reviews/CHAT.jsonl").exists():
        ok = {r["pid"] for r in read_jsonl(DEPTH / "reviews/CHAT.jsonl") if r.get("verdict") == "ok"}
        for r in read_jsonl(chat):
            eid = r["entry_id"]
            if r["pid"] not in ok or eid not in E or eid in out and eid not in owner_chat:
                continue
            owner_chat.add(eid)
            out.setdefault(eid, [{"text": nat.get(eid) or E[eid]["answer"]["short"], "atoms": []}])
            out[eid].append({"text": r["text"], "atoms": []})
    # Hubs (hubs.json, not section entries): short first answers from the HUB batch
    # (briefs/HUB_writer.md, reviewed in reviews/HUB_n.jsonl). The long hub reply is not rotated.
    for p in sorted((DEPTH / "proposals").glob("HUB_[0-9].jsonl")):
        rev = DEPTH / f"reviews/{p.name}"
        if not rev.exists():
            continue
        ok = {r["pid"] for r in read_jsonl(rev) if r.get("verdict") == "ok"}
        for r in read_jsonl(p):
            if r["pid"] in ok:
                out.setdefault(r["hub_id"], []).append({"text": r["text"], "atoms": []})
    assert all(out.values())

    (APP / "reply_variants.json").write_text(json.dumps(dict(sorted(out.items())), ensure_ascii=False, indent=1) + "\n")
    depth = APP / "depth_replies.json"
    if not depth.exists():
        depth.write_text("{}\n")

    # served pool = what the engine rotates over: emergency entries only their emergency_ok texts
    pool = {e: (sum(t.get("emergency_ok", False) for t in v) if e in emer else len(v)) for e, v in out.items()}
    emer_out = [e for e in out if e in emer]
    report = {
        "shards": len(parents), "entries": len(out), "texts": sum(map(len, out.values())),
        "entries_at_goal": sum(1 for e, n in pool.items() if e not in emer and n >= GOAL),
        "entries_below_goal": sorted(e for e, n in pool.items() if e not in emer and n < GOAL),
        "emergency_entries": len(emer_out),
        "emergency_below_3": sorted(e for e in emer_out if pool[e] < 3),
        "entries_without_texts": len(set(E) - set(out)),
        "by_kind_without_texts": dict(Counter(E[e].get("kind") for e in set(E) - set(out))),
    }
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
