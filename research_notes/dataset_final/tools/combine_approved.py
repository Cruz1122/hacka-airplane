"""Combine reviewer-approved factual ops into one proposal for a single knowledge.py stage/apply.

    python3 research_notes/dataset_final/tools/combine_approved.py
An op enters only if the latest review that saw exactly this op content approved it.
"""
from __future__ import annotations

import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]

# (proposal, [reviews in order, latest last]); a review covers an op if it lists its id. When a
# later proposal round leaves an op byte-identical, the earlier approval still holds.
ROUNDS = [
    ("G1", [("G1", "G1.review.H4.json")]),
    ("G1b", [("G1b", "G1b.review.H4.json")]),
    ("G2v2", [("G2", "G2.review.L1.json"), ("G2v2", "G2v2.review.L1.json")]),
    ("G3v3", [("G3", "G3.review.H4.json"), ("G3v2", "G3v2.review.H4.json"), ("G3v3", "G3v3.review.H4.json")]),
]


def ops(name: str) -> dict[str, dict]:
    return {o["entry"]["id"]: o for o in json.loads((W / f"proposals/{name}.json").read_text())["operations"]}


def main() -> None:
    final, log = [], []
    for prop, reviews in ROUNDS:
        target = ops(prop)
        for i, op in sorted(target.items()):
            verdict, by = None, None
            for rprop, rfile in reviews:
                rv = {o["id"]: o["verdict"] for o in json.loads((W / "reviews" / rfile).read_text())["ops"]}
                if i in rv and ops(rprop).get(i) == op:  # this review saw exactly this content
                    verdict, by = rv[i], rfile
            log.append({"id": i, "proposal": prop, "verdict": verdict, "review": by})
            if verdict == "approve":
                final.append(op)
    (W / "proposals/FINAL_APPROVED.json").write_text(json.dumps({"operations": final}, ensure_ascii=False, indent=1) + "\n")
    (W / "proposals/FINAL_APPROVED.log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"approved": len(final), "left_out": [x for x in log if x["verdict"] != "approve"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
