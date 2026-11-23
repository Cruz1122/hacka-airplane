"""Build compact, agent-sized inputs for the final dataset phase (no examples in the KB view)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CV2 = ROOT / "research_notes/curation_v2"
OUT = ROOT / "research_notes/dataset_final/inputs"
SECTIONS = ROOT / "data/knowledge/sections"


def flat_steps(steps) -> list[str]:
    out = []
    for s in steps or []:
        if isinstance(s, str):
            out.append(s)
        elif isinstance(s, dict):
            out.append(s.get("text") or s.get("step") or json.dumps(s, ensure_ascii=False))
            out.extend(flat_steps(s.get("steps") or s.get("substeps")))
    return out


def support() -> dict[str, dict]:
    res: dict[str, dict] = {}
    for p in sorted(CV2.glob("reviews/*.review.json")):
        if p.name.startswith("critical"):
            continue
        for r in json.loads(p.read_text()).get("audit_rows", []):
            res[r["id"]] = {"support": r.get("support"), "note": r.get("note", "")}
    for p in sorted(CV2.glob("reviews/*.rereview.json")):
        for r in json.loads(p.read_text()).get("audit_rows", []):
            res[r["id"]] = {"support": r.get("support"), "note": r.get("note", "")}
    # Final phase: every claim of an applied op was checked against its quotes by an independent reviewer.
    log = ROOT / "research_notes/dataset_final/proposals/FINAL_APPROVED.log.json"
    if log.exists():
        for r in json.loads(log.read_text()):
            if r["verdict"] == "approve":
                res[r["id"]] = {"support": "full", "note": f"final phase: claims re-verified ({r['review']})"}
    return res


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sup = support()
    view, full = [], {}
    for p in sorted(SECTIONS.glob("*.json")):
        sec = json.loads(p.read_text())
        for e in sec["entries"]:
            a = e.get("answer", {})
            full[e["id"]] = e
            view.append({
                "id": e["id"], "section": sec.get("id", p.stem), "label": e["label"], "kind": e.get("kind"),
                "audience": e.get("audience", "visitor"), "short": a.get("short", ""),
                "detail": a.get("detail", ""), "steps": flat_steps(a.get("steps")),
                "last_verified": e.get("last_verified"), "valid_until": e.get("valid_until"),
                "sources": [s.get("url") if isinstance(s, dict) else s for s in e.get("sources", [])],
                "support": sup.get(e["id"], {}).get("support", "not_reviewed"),
                "support_note": sup.get(e["id"], {}).get("note", ""),
            })
    (OUT / "kb_view.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in view))
    # Short catalog: id, section, label, first sentence of short (for query authors / clarification).
    cat = [{"id": v["id"], "section": v["section"], "label": v["label"], "short": v["short"]} for v in view]
    (OUT / "kb_catalog.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cat))

    sa = json.loads((CV2 / "reports/structural/structural_audit.json").read_text())
    applied = set()
    for p in CV2.glob("proposals/*.final.json"):
        for o in json.loads(p.read_text())["operations"]:
            applied.add(o.get("id") or o["entry"]["id"])
    temporal = sorted(i for i in sa["temporal_terms"] if i not in applied and i in full)
    temporal = sorted(set(temporal) | {"hours_status.park_open_today"})
    (OUT / "g1_temporal_entries.json").write_text(json.dumps(
        [{"entry": full[i], "flagged_terms": sa["temporal_terms"].get(i, []),
          "support": sup.get(i, {})} for i in temporal], ensure_ascii=False, indent=1))
    con = json.loads((CV2 / "findings/contradictions.json").read_text())
    high = [c for c in con if c.get("severity") in ("high", "critical")]
    (OUT / "g2_contradictions.json").write_text(json.dumps(
        [{**c, "entries": {i: full[i] for i in c["ids"] if i in full}} for c in high], ensure_ascii=False, indent=1))
    none_ids = sorted(i for i, s in sup.items() if s["support"] == "none" and i in full)
    (OUT / "g3_unsupported_entries.json").write_text(json.dumps(
        [{"entry": full[i], "support": sup[i]} for i in none_ids], ensure_ascii=False, indent=1))
    print(json.dumps({"view": len(view), "temporal": len(temporal), "contradictions_high": len(high),
                      "none_support": len(none_ids),
                      "support_counts": {k: sum(1 for v in view if v["support"] == k) for k in
                                         ("full", "partial", "none", "n/a", "not_reviewed")}}))


if __name__ == "__main__":
    main()
