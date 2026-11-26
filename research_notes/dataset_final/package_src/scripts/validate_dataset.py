"""Validate the Laya choice contract, IDs, labels and traceability of every split.

    python scripts/validate_dataset.py            # standard library only
    python scripts/validate_dataset.py --laya BASE_DIR   # also parse rows with laya==0.5.1's own loader
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import NONE, PKG, SPLITS, TRAINABLE, Report, jl, norm  # noqa: E402

TRACE = ["row_id", "query", "canonical_id", "acceptable_ids", "candidate_ids", "candidate_positions",
         "candidate_cosines", "gate_sections", "pool_source", "example_type", "provenance", "review_status",
         "outcome", "none_cause", "decision_reason", "family"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--laya", help="laya base checkpoint dir; runs laya.train.items_from_rows on train/selection")
    a = ap.parse_args()
    rep = Report("validate_dataset")
    catalog = {e["id"]: e for e in json.loads((PKG / "knowledge/faq_catalog.json").read_text(encoding="utf-8"))}
    clar = json.loads((PKG / "knowledge/clarification_labels.json").read_text(encoding="utf-8"))
    meta_rows = {m["row_id"]: m for m in jl(PKG / "train/metadata.jsonl")}
    ids_seen = Counter()
    for split, rel in SPLITS.items():
        rows = jl(PKG / rel)
        outcome, pos, k = Counter(), Counter(), Counter()
        for n, r in enumerate(rows):
            where = f"{split}:{n + 1}"
            q = r.get("questions", {}).get("topic", {})
            crit = q.get("criteria", [])
            meta = r.get("meta", {})
            pool = meta.get("pool", [])
            gold = set(meta.get("gold", []))
            ids_seen[meta.get("row_id")] += 1
            rep.check(isinstance(r.get("state"), str) and r["state"].strip() != "", f"{where} empty state")
            rep.check(q.get("type") == "choice" and isinstance(q.get("instructions"), str), f"{where} not a choice question")
            rep.check(3 <= len(pool) <= 5 and len(crit) == len(pool) + 1, f"{where} pool size {len(pool)} / criteria {len(crit)}")
            rep.check(crit[-1:] == [NONE] and len(set(crit)) == len(crit), f"{where} criteria must be unique and end with NONE")
            for c, label in zip(pool, crit):
                e = catalog.get(c)
                rep.check(e is not None, f"{where} unknown candidate {c}")
                if e:
                    rep.check(label in (e["label"], f"{e['label']} ({e['section']})"), f"{where} option text != catalog label for {c}")
            rep.check(all(g in catalog for g in gold), f"{where} unknown gold id")
            exp = r.get("expected", {})
            if split in TRAINABLE:
                rep.check("topic" in exp and exp["topic"] in crit, f"{where} expected not in criteria")
            if exp.get("topic") is not None:
                rep.check(exp["topic"] in crit, f"{where} expected not in criteria")
                hits = [c for c in pool if c in gold]
                if exp["topic"] == NONE:
                    rep.check(not hits, f"{where} target none but an acceptable id is in the pool")
                    outcome["none"] += 1
                else:
                    i = crit.index(exp["topic"])
                    rep.check(pool[i] in gold, f"{where} target option is not an acceptable id")
                    if split in TRAINABLE:
                        rep.check(len(hits) == 1, f"{where} trainable row with {len(hits)} acceptable ids in pool")
                    outcome["positive"] += 1
                    pos[i + 1] += 1
            else:
                outcome["no_single_target"] += 1
                rep.check(split not in TRAINABLE, f"{where} trainable row without target")
            k[len(pool)] += 1
            trace = meta_rows.get(meta.get("row_id"), {}) if split == "train" else meta
            missing = [f for f in TRACE if f not in trace]
            rep.check(not missing, f"{where} trace fields missing {missing}")
            no_target = trace.get("outcome") in ("clarify", "multi_positive")
            rep.check(no_target == (exp.get("topic") is None), f"{where} outcome {trace.get('outcome')} vs expected {exp}")
        rep.notes.append(f"{split}: {len(rows)} rows, outcomes {dict(outcome)}, target position {dict(sorted(pos.items()))}, pool size {dict(sorted(k.items()))}")
    # Historical 1,790 rows: legacy pools from an older corpus, kept verbatim and read only. Format
    # must parse; IDs no longer in the catalog are reported, not fixed (the file is not edited).
    hist = jl(PKG / "evaluation/historical_READ_ONLY.jsonl")
    unknown = Counter()
    for n, r in enumerate(hist):
        q = r.get("questions", {}).get("topic", {})
        rep.check(q.get("type") == "choice" and r.get("expected", {}).get("topic") in q.get("criteria", []),
                  f"historical:{n + 1} not a valid choice row")
        for i in r.get("meta", {}).get("pool", []) + r.get("meta", {}).get("gold", []):
            if i not in catalog:
                unknown[i] += 1
    rep.notes.append(f"historical_READ_ONLY: {len(hist)} rows; ids absent from the current catalog: {len(unknown)} distinct "
                     f"({sum(unknown.values())} mentions) — legacy, report only")
    rep.check(len(meta_rows) == len(jl(PKG / SPLITS["train"])), "train/metadata.jsonl row count != train.jsonl")
    dup = [i for i, c in ids_seen.items() if c > 1]
    rep.check(not dup, f"row_id repeated across splits: {dup[:5]}")
    # clarification labels
    rep.check(set(clar) == set(catalog), f"clarification labels missing for {len(set(catalog) - set(clar))} ids")
    normed = Counter(norm(v) for v in clar.values())
    for i, v in clar.items():
        words = len(v.split())
        rep.check(2 <= words <= 10, f"clarification label length {words} for {i}")
        rep.check(not any(ch.isdigit() for ch in v), f"clarification label has a digit: {i}")
        rep.check(" hoy " not in f" {norm(v)} ", f"clarification label says hoy: {i}")
        rep.check(normed[norm(v)] == 1, f"duplicate clarification label: {i} '{v}'")
    # emergency bypass and clarification tables must reference real FAQs
    policy = json.loads((PKG / "knowledge/answer_policy.json").read_text(encoding="utf-8"))
    rep.check(all(i in catalog for i in policy), f"answer_policy ids not in catalog: {[i for i in policy if i not in catalog][:5]}")
    emergency = [i for i, v in policy.items() if v.get("policy") == "emergency_direct"]
    rep.check(len(emergency) > 0, "no emergency_direct ids in answer_policy")
    # emergency answers bypass the clarification menu, so no row may expect a menu for them
    for split, rel in SPLITS.items():
        if split == "train":
            continue
        for r in jl(PKG / rel):
            m = r["meta"]
            if m.get("outcome") == "clarify":
                rep.check(not set(m.get("acceptable_ids") or []) & set(emergency),
                          f"{split}:{m['row_id']} clarify row whose acceptable FAQ is emergency_direct")
    conf = json.loads((PKG / "knowledge/confusable_sets.json").read_text(encoding="utf-8"))
    bad = [c["ids"] for c in conf if not all(i in catalog for i in c["ids"])]
    rep.check(not bad, f"confusable_sets ids not in catalog: {bad[:3]}")
    rep.notes.append(f"answer_policy: {len(policy)} ids ({len(emergency)} emergency_direct); confusable sets: {len(conf)}")
    if a.laya:
        from laya.train import items_from_rows, load_checkpoint  # noqa: PLC0415

        _model, tok, cfg = load_checkpoint(a.laya)  # same lengths finetune() uses by default
        for split in sorted(TRAINABLE):
            items, skipped = items_from_rows(tok, jl(PKG / SPLITS[split]), cfg.get("max_len", 512), cfg.get("head_max_len", 192))
            rep.notes.append(f"laya {split}: {len(items)} items, skipped {skipped}")
            rep.check(not skipped, f"laya skipped rows in {split}: {skipped}")
    rep.done()


if __name__ == "__main__":
    main()
