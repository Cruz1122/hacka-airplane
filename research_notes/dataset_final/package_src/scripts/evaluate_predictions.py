"""Score predictions against acceptable ids, by split, outcome type, none cause and scenario.

    python scripts/evaluate_predictions.py preds.jsonl [--baseline first_option]

A prediction is correct when the chosen option's FAQ id is in the row's acceptable ids, or when it
is "ninguna de estas opciones" and no acceptable id is in the pool. Rows without a single target
(`clarify`, `multi_positive`) count as correct if the choice is any acceptable id; for `clarify`
rows the report also gives how often an acceptable id is among the top-3 probabilities (what the
clarification menu would show). Train metadata is not needed: eval rows carry their trace in meta.

Error taxonomy (`error=` lines, share of the file's rows):
  reranking_error           an acceptable FAQ is in the pool but the decider chose another option
                            (another FAQ or "ninguna")
  false_answer:retrieval_miss    no acceptable FAQ in the pool (candidate_none) because retrieval
                            missed an existing FAQ, and the decider still picked an FAQ
  false_answer:true_out_of_scope no FAQ covers the query, and the decider picked an FAQ
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import NONE, PKG, jl  # noqa: E402


def wilson(k: int, n: int) -> str:
    if not n:
        return "n/a"
    p, z = k / n, 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{100 * p:.1f}% [{max(0.0, 100 * (c - h)):.1f}, {min(100.0, 100 * (c + h)):.1f}] (n={n})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("preds")
    ap.add_argument("--baseline", choices=("first_option",), help="score 'always option 1' (= e5 top-1) instead")
    a = ap.parse_args()
    preds = {(p["file"], p["row_id"]): p for p in jl(__import__("pathlib").Path(a.preds))}
    rows = {}
    for f in {k[0] for k in preds}:
        for r in jl(PKG / f):
            rows[(f, r["meta"]["row_id"])] = r
    groups = defaultdict(lambda: [0, 0])
    top3 = defaultdict(lambda: [0, 0])
    errors = defaultdict(lambda: defaultdict(int))
    for key, p in preds.items():
        r = rows[key]
        m, crit = r["meta"], r["questions"]["topic"]["criteria"]
        pool, acc = m["pool"], set(m.get("acceptable_ids", m.get("gold", [])))
        choice = crit[0] if a.baseline else p["choice"]
        picked = pool[crit.index(choice)] if choice in crit[:-1] else None
        hit_in_pool = bool(acc & set(pool))
        ok = (picked in acc) if picked else (not hit_in_pool)
        err = "correct" if ok else ("reranking_error" if hit_in_pool else f"false_answer:{m.get('none_cause')}")
        errors[key[0]][err] += 1
        for g in ("ALL", f"outcome={m.get('outcome')}", f"none_cause={m.get('none_cause')}", f"scenario={m.get('scenario')}",
                  f"provenance={m.get('provenance')}"):
            groups[(key[0], g)][0] += ok
            groups[(key[0], g)][1] += 1
        if m.get("outcome") in ("clarify", "multi_positive") and p.get("probabilities"):
            probs = p["probabilities"]
            order = sorted((o for o in crit[:-1] if o in probs), key=lambda o: -probs[o])[:3]
            top3[key[0]][0] += any(pool[crit.index(o)] in acc for o in order)
            top3[key[0]][1] += 1
    for (f, g), (k, n) in sorted(groups.items()):
        print(f"{f}\t{g}\t{wilson(k, n)}")
    for f, counts in sorted(errors.items()):
        n = sum(counts.values())
        for e, k in sorted(counts.items()):
            print(f"{f}\terror={e}\t{wilson(k, n)}")
    for f, (k, n) in sorted(top3.items()):
        print(f"{f}\tclarify_top3_contains_acceptable\t{wilson(k, n)}")


if __name__ == "__main__":
    main()
