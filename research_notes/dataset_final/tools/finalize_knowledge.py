"""Merge reviewed side tables into work/: clarification labels, answer policy, confusable sets,
source manifest and safety issues. Run before build_dataset.py build.

    python3 research_notes/dataset_final/tools/finalize_knowledge.py
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

W = Path(__file__).resolve().parents[1]
ROOT = W.parents[1]
CV2 = ROOT / "research_notes/curation_v2"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def main() -> None:
    work = W / "work"
    entries = {}
    for p in sorted((ROOT / "data/knowledge/sections").glob("*.json")):
        s = json.loads(p.read_text())
        for e in s["entries"]:
            entries[e["id"]] = {**e, "section": s["id"]}
    view = {r["id"]: r for r in jl(W / "inputs/kb_view.jsonl")}

    # clarification labels: X4 draft + H2 review changes
    labels = json.loads((W / "authored/clarification_labels.X4.json").read_text())
    changes = jl(W / "judgments/clarification_review.H2.jsonl")
    for c in changes:
        if c["id"] in labels:
            labels[c["id"]] = c["after"]
    labels = {i: labels[i] for i in entries}
    (work / "clarification_labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1) + "\n")

    # answer policy
    policy = {}
    for p in sorted((W / "proposals").glob("answer_policy.*.json")):
        for r in json.loads(p.read_text()):
            if r["id"] in entries:
                policy[r["id"]] = {"policy": r["policy"], "reason": r.get("reason", ""), "source": p.name}
    emergency = sorted(i for i, e in entries.items() if e["section"] == "actions" and ".report_" in i)
    em_gold = defaultdict(int)
    for v in sorted((W / "judgments").glob("authored_verify.*.jsonl")):
        for r in jl(v):
            pass
    for a in sorted((W / "authored").glob("*.jsonl")):
        for r in jl(a):
            if r.get("scenario") == "emergency" and r.get("gold"):
                em_gold[r["gold"]] += 1
    for i in emergency + sorted(em_gold):
        if i in entries and i not in policy:
            policy[i] = {"policy": "emergency_direct", "reason": "emergency guidance: answer directly, never behind a clarification menu",
                         "source": "actions section" if i in emergency else f"gold of {em_gold[i]} verified emergency queries"}
    (work / "answer_policy.json").write_text(json.dumps(dict(sorted(policy.items())), ensure_ascii=False, indent=1) + "\n")

    # confusable sets: reviewer-judged overlapping pairs + routing confusions from curation v2
    pairs = defaultdict(lambda: {"verdicts": set(), "notes": []})
    for p in sorted((W / "judgments").glob("pairs.*.jsonl")):
        for r in jl(p):
            if r["verdict"] != "distinct":
                k = tuple(sorted((r["a"], r["b"])))
                pairs[k]["verdicts"].add(r["verdict"]); pairs[k]["notes"].append(r.get("note", ""))
    routed = set()
    with open(CV2 / "audit/inventory_after/confusable_pairs.csv") as f:
        for r in csv.DictReader(f):
            if int(r["a_examples_to_b"]) + int(r["b_examples_to_a"]) >= 3:
                routed.add(tuple(sorted((r["a"], r["b"]))))
    conf = [{"ids": list(k), "verdicts": sorted(v["verdicts"]), "notes": v["notes"][:2],
             "clarification_labels": [labels.get(k[0]), labels.get(k[1])], "routing_confusion": k in routed}
            for k, v in sorted(pairs.items())]
    conf += [{"ids": list(k), "verdicts": [], "notes": [], "clarification_labels": [labels.get(k[0]), labels.get(k[1])],
              "routing_confusion": True} for k in sorted(routed - set(pairs))]
    (work / "confusable_sets.json").write_text(json.dumps(conf, ensure_ascii=False, indent=1) + "\n")

    # source manifest
    src = defaultdict(lambda: {"entries": [], "titles": set()})
    for i, e in entries.items():
        for s in e.get("sources", []):
            url = s.get("url") if isinstance(s, dict) else s
            src[url]["entries"].append(i)
            if isinstance(s, dict) and s.get("title"):
                src[url]["titles"].add(s["title"])
    man = {"sources": [{"url": u, "titles": sorted(v["titles"]), "entries": sorted(v["entries"])} for u, v in sorted(src.items())],
           "entry_support": {i: {"support": view.get(i, {}).get("support"), "last_verified": entries[i].get("last_verified"),
                                 "valid_until": entries[i].get("valid_until")} for i in sorted(entries)},
           "note": "support = latest independent reviewer judgment of whether the cited excerpt supports the answer (curation v2)."}
    (work / "source_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"labels": len(labels), "label_changes": len(changes), "policy": len(policy),
                      "confusable_sets": len(conf), "sources": len(man["sources"])}))


if __name__ == "__main__":
    main()
