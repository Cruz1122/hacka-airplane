"""Turn the final near-duplicate and eval-leakage proposals into coordinator inputs (run once per proposal).

Swaps  -> style_final/<section>.json (example old->new, applied by coordinator_fixes.apply_polish)
Merges -> dedup_decisions.json "merges" (kept answer patched separately when facts are missing)
add_expected -> eval rows gain an alternative correct entry id.
"""

import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SWAPS_DIR = HERE / "style_final"


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.casefold().strip()) if unicodedata.category(c) != "Mn")


def main(path):
    prop = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = {e["id"]: e for f in sorted((ROOT / "data/knowledge/sections").glob("*.json"))
               for e in json.loads(f.read_text(encoding="utf-8"))["entries"]}
    existing = {fold(x) for e in entries.values() for x in e["examples"]}
    evalq = {fold(json.loads(l)["q"]) for p in (ROOT / "data/knowledge/phase2/eval").glob("*.jsonl")
             for l in p.read_text(encoding="utf-8").splitlines() if l.strip()}
    swaps = {}
    for f in sorted(SWAPS_DIR.glob("*.json")):
        swaps.update(json.loads(f.read_text(encoding="utf-8")))
    seen = {fold(n) for p in swaps.values() for n in p.get("examples", {}).values()}
    bad = []
    for s in prop.get("swaps", []):
        eid, old, new = s["entry"], s["old"], s["new"]
        if eid not in entries or old not in entries[eid]["examples"]:
            bad.append(("old not in entry", s)); continue
        if fold(new) in existing or fold(new) in seen or fold(new) in evalq:
            bad.append(("new not unique", s)); continue
        seen.add(fold(new))
        swaps.setdefault(eid, {}).setdefault("examples", {})[old] = new
    SWAPS_DIR.mkdir(exist_ok=True)
    by_section = {}
    for eid, patch in swaps.items():
        by_section.setdefault(eid.split(".")[0], {})[eid] = patch
    for sid, patches in by_section.items():
        (SWAPS_DIR / f"{sid}.json").write_text(json.dumps(patches, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if prop.get("merges"):
        dec = json.loads((HERE / "dedup_decisions.json").read_text(encoding="utf-8"))
        for m in prop["merges"]:
            pair = [m["keep"], m["drop"]]
            if pair not in dec["merges"]:
                dec["merges"].append(pair)
        (HERE / "dedup_decisions.json").write_text(json.dumps(dec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for a in prop.get("add_expected", []):
        p = ROOT / "data/knowledge/phase2/eval" / a["file"]
        rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        for r in rows:
            if r["q"] == a["q"] and a["add"] not in r["expected"]:
                r["expected"].append(a["add"])
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"swaps total {sum(len(p.get('examples', {})) for p in swaps.values())}; rejected {len(bad)}; "
          f"merges {len(prop.get('merges', []))}; add_expected {len(prop.get('add_expected', []))}")
    for reason, s in bad:
        print(reason, json.dumps(s, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
