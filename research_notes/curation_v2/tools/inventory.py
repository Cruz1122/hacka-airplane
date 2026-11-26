"""Per-entry inventory and e5 confusion map of a sections directory (read-only).

    uv run --project experiments/laya python research_notes/curation_v2/tools/inventory.py \
        --sections data/knowledge/sections --out research_notes/curation_v2/audit/inventory_before

Writes <out>/<section>.csv (one row per entry), <out>/confusable_pairs.csv (entry pairs whose
examples route to each other leave-one-out) and <out>/summary.json.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route_check import flat_index  # noqa: E402

TEMPORAL = re.compile(r"\b(hoy|actual(?:mente)?|vigente|en este momento|ahora mismo|abiert[oa]|"
                      r"cerrad[oa]|alerta (?:amarilla|naranja|roja)|20(?:2[3-9]))\b", re.I)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sections", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sections = {p.stem: json.loads(p.read_text()) for p in sorted(Path(a.sections).glob("*.json"))}
    ids, owner, vecs, _ = flat_index(sections)
    n = len(ids)
    sims = vecs @ vecs.T
    np.fill_diagonal(sims, -1.0)
    is_label = np.r_[True, owner[1:] != owner[:-1]]
    loo_hits = collections.Counter()
    loo_tot = collections.Counter()
    confused = collections.defaultdict(collections.Counter)
    for r in np.nonzero(~is_label)[0]:
        best = np.full(n, -1.0, np.float32)
        np.maximum.at(best, owner, sims[r])
        top = int(np.argmax(best))
        own = int(owner[r])
        loo_tot[own] += 1
        if top == own:
            loo_hits[own] += 1
        else:
            confused[own][top] += 1
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pos = {eid: i for i, eid in enumerate(ids)}
    summary = {}
    for sid, s in sections.items():
        rows = []
        for e in s["entries"]:
            i = pos.get(e["id"])
            ans = json.dumps(e["answer"], ensure_ascii=False)
            top_conf = confused[i].most_common(2) if i is not None else []
            rows.append({
                "id": e["id"], "label": e["label"], "kind": e["kind"], "audience": e["audience"],
                "n_examples": len(e["examples"]), "n_hard_negatives": len(e.get("hard_negatives", [])),
                "n_related": len(e.get("related", [])),
                "source_hosts": " ".join(sorted({re.sub(r"^https?://", "", x["url"]).split("/")[0]
                                                 for x in e["sources"]})),
                "last_verified": e.get("last_verified") or "", "valid_until": e.get("valid_until") or "",
                "answer_has_digits": bool(re.search(r"\d", ans)),
                "temporal_terms": " | ".join(sorted({m.lower() for m in TEMPORAL.findall(ans)})),
                "loo_top1": round(loo_hits[i] / loo_tot[i], 3) if i is not None and loo_tot[i] else "",
                "confused_with": " ".join(f"{ids[j]}:{c}" for j, c in top_conf),
                "short": e["answer"]["short"],
            })
        with open(out / f"{sid}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        vals = [r["loo_top1"] for r in rows if r["loo_top1"] != ""]
        summary[sid] = {"entries": len(rows), "examples": sum(r["n_examples"] for r in rows),
                        "mean_loo_top1": round(float(np.mean(vals)), 3) if vals else None,
                        "temporal_entries": sum(bool(r["temporal_terms"]) for r in rows)}
    pairs = []
    for i, cnt in confused.items():
        for j, c in cnt.items():
            if c >= 2:
                pairs.append({"a": ids[i], "b": ids[j], "a_examples_to_b": c,
                              "b_examples_to_a": confused[j][i]})
    pairs.sort(key=lambda p: -(p["a_examples_to_b"] + p["b_examples_to_a"]))
    with open(out / "confusable_pairs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["a", "b", "a_examples_to_b", "b_examples_to_a"])
        w.writeheader()
        w.writerows(pairs)
    total = sum(loo_hits.values()) / max(1, sum(loo_tot.values()))
    summary["_all"] = {"entries": n, "loo_top1": round(total, 4), "confusable_pairs_ge2": len(pairs)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary["_all"]))


if __name__ == "__main__":
    main()
