"""T4 write shards: 20 entries each = the entries of T30_{2k} + T30_{2k+1}, emitted only when both
inventories are resolved (resolved/T30_NNN.jsonl). Exempt entries (conversation section / chat) go
to T4_X shards with their L0 as the only key fact (R1.1: ≥10 variants).

Per entry: id, label, kind, KEY facts only (R7: a variant asking for a complement is a drop),
3 current examples, related labels as "do NOT ask these", the R1.2 bucket mix.

usage: python3 t4_shards.py   -> shards/T4_NNN.json (existing files are not rewritten)
"""

from __future__ import annotations

import json

from common import DEPTH, app, entries, exempt, read_jsonl

MIX = {"colloquial": 6, "misspelled": 4, "fragment": 3, "situational": 3, "english": 2, "specific_fact": 2}
MIX_X = {"colloquial": 4, "misspelled": 3, "fragment": 2, "situational": 2, "english": 1}


def row(e, E, nat, keys, flag=None):
    return {"entry_id": e["id"], "label": e["label"], "kind": e.get("kind"), "key_facts": keys,
            "examples": (e.get("examples") or [])[:3],
            "do_not_ask": [E[r]["label"] for r in (e.get("related") or []) if r in E][:6],
            **({"flag": flag} if flag else {})}


def main() -> None:
    E, nat = entries(), app("natural_replies.json")
    sh, made = DEPTH / "shards", []
    for k in range(39):
        out = sh / f"T4_{k:03d}.json"
        a, b = DEPTH / f"resolved/T30_{2 * k:03d}.jsonl", DEPTH / f"resolved/T30_{2 * k + 1:03d}.jsonl"
        if out.exists() or not a.exists() or not (b.exists() or 2 * k + 1 > 77):
            continue
        rows = []
        for p in (a, b):
            if not p.exists():
                continue
            ids = [x["entry_id"] for x in json.loads((sh / p.name.replace(".jsonl", ".json")).read_text())["entries"]]
            res = {r["entry_id"]: r for r in read_jsonl(p)}
            for eid in ids:
                keys = [f["text"] for f in res.get(eid, {}).get("facts", []) if f["class"] == "key"]
                rows.append(row(E[eid], E, nat, keys or [nat.get(eid, "")], None if keys else "no inventory: L0 as key"))
        out.write_text(json.dumps({"shard": out.stem, "mix": MIX, "per_entry": 24, "entries": rows},
                                  ensure_ascii=False, indent=0))
        made.append(out.stem)
    xs = [e for e in E.values() if exempt(e)]
    for i in range(0, len(xs), 15):
        out = sh / f"T4_X{i // 15:02d}.json"
        if not out.exists():
            out.write_text(json.dumps({"shard": out.stem, "mix": MIX_X, "per_entry": 12,
                                       "entries": [row(e, E, nat, [nat.get(e["id"], "")]) for e in xs[i: i + 15]]},
                                      ensure_ascii=False, indent=0))
            made.append(out.stem)
    print("made", made)


if __name__ == "__main__":
    main()
