"""Check that held-out sets are isolated: FAQ ids, paraphrase families, row ids and texts.

    python scripts/validate_splits.py
"""
from __future__ import annotations

import json
from collections import defaultdict

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PKG, SPLITS, Report, jl, norm  # noqa: E402


def main() -> None:
    rep = Report("validate_splits")
    man = json.loads((PKG / "audit/split_manifest.json").read_text(encoding="utf-8"))
    unseen = set(man["unseen_topic_ids"])
    rows = {s: jl(PKG / rel) for s, rel in SPLITS.items()}
    trace = {m["row_id"]: m for m in jl(PKG / "train/metadata.jsonl")}

    def tr(split, r):
        return trace[r["meta"]["row_id"]] if split == "train" else r["meta"]

    for s, rs in rows.items():
        rep.check(len(rs) == man["counts"][s], f"{s}: {len(rs)} rows, manifest says {man['counts'][s]}")
    for r in rows["train"]:
        m = tr("train", r)
        bad = unseen & set(m["candidate_ids"] + m["acceptable_ids"] + [m.get("canonical_id") or ""])
        rep.check(not bad, f"train row {m['row_id']} touches unseen topic {sorted(bad)}")
    for r in rows["checkpoint_selection"] + rows["calibration"]:
        bad = unseen & set(r["meta"]["acceptable_ids"])
        rep.check(not bad, f"{r['meta']['row_id']} selection/calibration row has unseen gold {sorted(bad)}")
    fam = defaultdict(set)
    text = defaultdict(set)
    for s, rs in rows.items():
        if s == "retrospective_READ_ONLY":
            continue
        for r in rs:
            m = tr(s, r)
            if m.get("family") and not str(m["family"]).startswith("faq:"):
                fam[m["family"]].add(s)
            text[norm(r["state"])].add(s)
    multi = {f: v for f, v in fam.items() if len(v) > 1}
    rep.check(not multi, f"families in several splits: {list(multi.items())[:5]}")
    shared = {t: v for t, v in text.items() if len(v) > 1}
    rep.check(not shared, f"identical texts in several splits: {list(shared.items())[:5]}")
    # corpus-example families (faq:<id>) only in train or unseen_topics, never both
    faq_split = defaultdict(set)
    for s in ("train", "unseen_topics"):
        for r in rows[s]:
            m = tr(s, r)
            if str(m.get("family", "")).startswith("faq:"):
                faq_split[m["family"]].add(s)
    both = [f for f, v in faq_split.items() if len(v) > 1]
    rep.check(not both, f"FAQ example families in train and unseen: {both[:5]}")
    rep.notes.append(f"unseen topic ids: {len(unseen)}; families checked: {len(fam)}; texts checked: {len(text)}")
    rep.done()


if __name__ == "__main__":
    main()
