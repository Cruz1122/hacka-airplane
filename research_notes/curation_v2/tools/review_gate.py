"""Gate between review rounds: what a v2 proposal may change, and what must be reviewed again.

    python3 research_notes/curation_v2/tools/review_gate.py --section S            # after the fix round
    python3 research_notes/curation_v2/tools/review_gate.py --section S --final    # after re-review

Fix round (default): compares proposals/S.v2.json with proposals/S.json and reviews/S.review.json.
FAIL if an approved op changed, or a `revise` op is unchanged (not addressed: drop it or fix it).
Writes reviews/S.rereview_queue.json with every v2 op that differs from an approved v1 op.

--final: builds proposals/S.final.json = approved v1 ops + v2 ops approved in
reviews/S.rereview.json. Every queued op must have a re-review record; anything else is left out.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[1]


def ops_of(path: Path) -> dict[str, dict]:
    d = json.loads(path.read_text())
    ops = d["operations"] if isinstance(d, dict) else d
    return {(o.get("id") or o["entry"]["id"]): o for o in ops}


def verdicts(path: Path) -> dict[str, str]:
    return {r["id"]: r["verdict"] for r in json.loads(path.read_text())["ops"]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True)
    ap.add_argument("--final", action="store_true")
    a = ap.parse_args()
    s = a.section
    v1 = ops_of(W / f"proposals/{s}.json")
    rev = verdicts(W / f"reviews/{s}.review.json")
    v2_path = W / f"proposals/{s}.v2.json"
    v2 = ops_of(v2_path) if v2_path.exists() else {}
    approved = {i: o for i, o in v1.items() if rev.get(i) == "approve"}
    fail = [f"{i}: reviewed op missing a verdict" for i in v1 if i not in rev]
    fail += [f"{i}: approved op changed in v2" for i, o in approved.items() if i in v2 and v2[i] != o]
    fail += [f"{i}: 'revise' op unchanged in v2 (fix it or drop it)"
             for i, o in v1.items() if rev.get(i) == "revise" and v2.get(i) == o]
    queue = sorted(i for i, o in v2.items() if approved.get(i) != o)
    if not a.final:
        (W / f"reviews/{s}.rereview_queue.json").write_text(json.dumps(queue, indent=1))
        print(json.dumps({"section": s, "v1_ops": len(v1), "approved_v1": len(approved),
                          "v2_ops": len(v2), "rereview_queue": len(queue),
                          "dropped": sorted(set(v1) - set(v2) - set(approved)), "fail": fail},
                         indent=1))
        sys.exit(1 if fail else 0)
    rr_path = W / f"reviews/{s}.rereview.json"
    rr = verdicts(rr_path) if rr_path.exists() else {}
    # An addendum records verdicts whose re-review condition was met mechanically afterwards
    # (e.g. a refetch that only needed a verified CA chain); it carries its own basis.
    add_path = W / f"reviews/{s}.rereview.addendum.json"
    if add_path.exists():
        rr.update(verdicts(add_path))
    fail += [f"{i}: queued op without a re-review verdict" for i in queue if i not in rr]
    final = dict(approved)
    final.update({i: v2[i] for i in queue if rr.get(i) == "approve"})
    # Critical rounds (critical_r3, critical_r3b, ...) override earlier ops of S, in name order,
    # but only ops their own review approved.
    for cp in sorted(W.glob("proposals/critical_r*.json")):
        if cp.name.count(".") > 1:  # .stage/.verify/.route outputs
            continue
        crev = W / f"reviews/{cp.stem}.review.json"
        cv = verdicts(crev) if crev.exists() else {}
        for i, o in ops_of(cp).items():
            if i.startswith(f"{s}.") and cv.get(i) == "approve":
                final[i] = o
    out = {"operations": [final[i] for i in sorted(final)]}
    (W / f"proposals/{s}.final.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"section": s, "final_ops": len(final), "from_v1": len(approved),
                      "from_v2": len(final) - len(approved),
                      "left_out": sorted((set(v1) | set(v2)) - set(final)), "fail": fail},
                     indent=1))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
