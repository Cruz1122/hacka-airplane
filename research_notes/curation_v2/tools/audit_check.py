"""Check a curator's audit CSV against the corpus and the evidence it claims to have read.

    python3 research_notes/curation_v2/tools/audit_check.py --section S

FAIL (exit 1): an entry of S without a row; an unknown verdict/source_status/temporal value; a row
with source_status `primary_ok` or `secondary_only` whose `evidence_ref` file is not hash-pinned
legacy evidence or fetch_evidence.py output, or whose `evidence_excerpt` (>= 20 chars, verbatim)
is not in that file. "Checked" must point at what was read.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_evidence import NEW_EVIDENCE, ROOT, legacy_ok, norm_ws  # noqa: E402

W = ROOT / "research_notes/curation_v2"
VERDICTS = ("keep", "modify_meta", "modify_fact", "merge_into:", "delete", "move_to:", "flag_review")
SOURCE = {"primary_ok", "secondary_only", "quote_missing", "url_dead", "not_checked"}
TEMPORAL = {"none", "dated_ok", "needs_date", "claims_current_state"}
REQUIRED = ["id", "verdict", "reasons", "source_status", "evidence_ref", "evidence_excerpt",
            "temporal", "confusable_with", "notes"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True)
    a = ap.parse_args()
    s = a.section
    ids = [e["id"] for e in json.loads((W / f"snapshots/sections_before/{s}.json").read_text())["entries"]]
    rows = list(csv.DictReader(open(W / f"audit/{s}.csv", newline="")))
    fail = []
    missing_cols = [c for c in REQUIRED if rows and c not in rows[0]]
    if missing_cols:
        fail.append(f"missing columns: {missing_cols}")
    by_id = {r["id"]: r for r in rows}
    fail += [f"{i}: no audit row" for i in ids if i not in by_id]
    counts: dict[str, int] = {}
    for r in rows:
        i = r["id"]
        if not r.get("verdict", "").startswith(VERDICTS):
            fail.append(f"{i}: bad verdict {r.get('verdict')!r}")
        st = r.get("source_status", "")
        counts[st] = counts.get(st, 0) + 1
        if st not in SOURCE:
            fail.append(f"{i}: bad source_status {st!r}")
        if r.get("temporal") not in TEMPORAL:
            fail.append(f"{i}: bad temporal {r.get('temporal')!r}")
        if st in ("primary_ok", "secondary_only"):
            ref, exc = r.get("evidence_ref", "").strip(), r.get("evidence_excerpt", "").strip()
            p = (ROOT / ref).resolve() if ref else None
            if not p or not p.is_file() or not p.is_relative_to(ROOT):
                fail.append(f"{i}: {st} without a readable evidence_ref")
                continue
            if not (p.is_relative_to(NEW_EVIDENCE) and p.with_suffix(".meta.json").is_file()) \
                    and not legacy_ok(p):
                fail.append(f"{i}: evidence_ref is neither fetched nor pinned legacy evidence")
            if len(exc) < 20 or norm_ws(exc) not in norm_ws(p.read_text(errors="replace")):
                fail.append(f"{i}: evidence_excerpt not verbatim in {ref}")
    print(json.dumps({"section": s, "entries": len(ids), "rows": len(rows),
                      "source_status": counts, "fail": fail}, indent=1, ensure_ascii=False))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
