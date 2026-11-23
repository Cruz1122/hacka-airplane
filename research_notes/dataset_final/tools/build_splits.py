"""Second half of build_dataset.py: labels, splits, leakage filter and export of the final package."""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from build_dataset import (
    AUDIT, EVAL_V2, HISTORICAL, INSTR, LEAK_COS, NONE, ROOT, SEED, UNSEEN_PER_FAQ, W, Index,
    bucket, jl, load_audit, load_authored, load_embed, load_pair_judgments, make_row, norm, sha256,
    unseen_ids, wjl,
)

PKG = "LOS_NEVADOS_LAYA_FINAL_DATASET"
OUT = W / "out" / PKG
HIGH_SIM = 0.88  # answer-text cosine at or above which a decisive pair must be judged by a reviewer

# family bucket -> split, per author group. Ambiguous / multi-positive rows never go to train.
ROUTES = {
    "X1": [("train", 0.30), ("adversarial", 1.0)],
    "X3": [("train", 0.25), ("calibration", 0.50), ("adversarial", 1.0)],
    "default": [("train", 0.20), ("checkpoint_selection", 0.45), ("calibration", 0.65), ("final_test", 1.0)],
}


def route(row: dict) -> str:
    rules = ROUTES.get(row["qid"].split("-")[0], ROUTES["default"])
    # X1 writes mirrored questions for one FAQ pair in separate families: route by the pair so a
    # contrast never lands in both train and evaluation.
    key = row["family"]
    if row["qid"].startswith("X1") and row.get("gold"):
        key = "pair:" + "|".join(sorted([row["gold"], *(row.get("near_ids") or [])[:1]]))
    b = bucket(key, "family")
    return next(split for split, edge in rules if b < edge)


def decisive(pool: list[str], gold: str | None) -> list[str]:
    """Candidates whose label decides the row: all others if gold is absent, else those ranked above it."""
    if gold not in pool:
        return [c for c in pool if c != gold]
    return pool[: pool.index(gold)]


def build(_args) -> None:
    embed = load_embed()
    ix = Index(embed)
    held = set(unseen_ids(ix))
    excl = np.asarray([i in held for i in ix.ids])
    pairs = load_pair_judgments()
    audit = load_audit()
    pair_sim = json.loads((W / "work/pair_sim.json").read_text())
    ex_owner = {}
    for e in ix.entries:
        for x in e.get("examples", []):
            ex_owner.setdefault(x, e["id"])
    curated_hn = {(e["id"], ex_owner.get(x)) for e in ix.entries for x in e.get("hard_negatives", [])}

    def pair_status(a: str, b: str) -> str:
        if (a, b) in pairs:
            return "judged:" + pairs[(a, b)]["verdict"]
        if (a, b) in curated_hn or (b, a) in curated_hn:
            return "curated_hard_negative"
        sim = pair_sim.get(f"{a}|{b}", [0.0])[0]
        return "pending_high_similarity" if sim >= HIGH_SIM else "auto_low_similarity"

    corrections, excluded, unresolved = [], [], []
    splits: dict[str, list[dict]] = defaultdict(list)

    def label_with_pairs(gid: str, pool: list[str], acceptable: set[str], row_id: str, q: str):
        doubt, statuses = set(), {}
        for c in pool:
            if c in acceptable:
                continue
            j = pairs.get((gid, c))
            if not j:
                continue
            if j["verdict"] == "also_answers":
                acceptable.add(c)
                corrections.append({"row_id": row_id, "query": q, "canonical_id": gid, "added_acceptable": c,
                                    "source": j["file"], "by": j.get("by"), "reason": j.get("note", "")})
            elif j["verdict"] in ("query_dependent", "mislabeled"):
                doubt.add(c)
        for c in decisive(pool, gid):
            statuses[c] = pair_status(gid, c)
        return doubt, statuses

    # ---------------------------------------------------------------- corpus examples
    owners_by_text = defaultdict(set)
    for e in ix.entries:
        for x in e.get("examples", []):
            owners_by_text[norm(x)].add(e["id"])
    seen = set()
    for n, e in enumerate(ix.entries):
        gid = e["id"]
        is_held = gid in held
        examples = e.get("examples", [])
        if is_held:  # unseen-topic eval: a deterministic sample of its examples, full index
            order = sorted(range(len(examples)), key=lambda j: bucket(f"{gid}:{j}", "unseen"))[:UNSEEN_PER_FAQ]
        else:
            order = range(len(examples))
        for j in order:
            q = examples[j]
            nq = norm(q)
            row_id = f"ex:{gid}:{j}"
            base = {"row_id": row_id, "canonical_id": gid, "section": e["section"], "provenance": "original",
                    "example_type": "corpus_example", "family": f"faq:{gid}", "scenario": "corpus_example"}
            if len(owners_by_text[nq]) > 1:
                excluded.append({**base, "query": q, "reason": "same_text_in_several_faqs",
                                 "owners": sorted(owners_by_text[nq])}); continue
            if (gid, nq) in seen:
                excluded.append({**base, "query": q, "reason": "duplicate_text_same_faq"}); continue
            seen.add((gid, nq))
            t = ix.example_pos[(n, j)]
            ret = ix.retrieve(ix.tv[t], mask_text=ix.self_mask(n, t), excluded=None if is_held else excl)
            pool = [ix.ids[m] for m in ret["pool"]]
            acceptable, doubt = {gid}, set()
            a = audit.get(nq)
            review = "auto"
            if a:
                review = "label_audit"
                if a["case"] == "D":
                    unresolved.append({**base, "query": q, "reason": "label_audit_case_D",
                                       "acceptable_ids": a.get("acceptable_ids", []), "rationale": a.get("rationale", "")})
                    excluded.append({**base, "query": q, "reason": "label_audit_case_D"}); continue
                extra = set(a.get("acceptable_ids", [])) - acceptable
                if extra:
                    corrections.append({"row_id": row_id, "query": q, "canonical_id": gid,
                                        "added_acceptable": sorted(extra), "source": "curation_v2/audit/label_audit.jsonl",
                                        "by": "label_audit", "reason": a.get("rationale", "")})
                    acceptable |= extra
            if not is_held and acceptable & held:  # never let an unseen topic id reach a training row
                base["acceptable_unseen_removed"] = sorted(acceptable & held)
                acceptable -= held
            d2, statuses = label_with_pairs(gid, pool, acceptable, row_id, q)
            doubt |= d2
            row = make_row(ix, q, ret, acceptable, doubt, base)
            tr = row["_trace"]
            tr["pair_status"] = statuses
            if review == "auto" and statuses:
                vals = set(statuses.values())
                if "pending_high_similarity" in vals:
                    review = "pending_pair_review"
                elif all(v.startswith("judged") or v == "curated_hard_negative" for v in vals):
                    review = "pairs_verified"
                else:
                    review = "auto_low_similarity"
            elif review == "auto":
                review = "no_decisive_pair"  # gold ranked first: nothing to reject
            tr["review_status"] = review
            split = "unseen_topics" if is_held else "train"
            if tr["doubt_ids_in_pool"]:
                unresolved.append({**base, "query": q, "reason": "pair_query_dependent",
                                   "doubt_ids": tr["doubt_ids_in_pool"], "candidate_ids": pool})
                if split == "train":
                    excluded.append({**base, "query": q, "reason": "pair_query_dependent"}); continue
            if tr["outcome"] == "multi_positive":
                unresolved.append({**base, "query": q, "reason": "multi_positive_in_pool",
                                   "acceptable_in_pool": sorted(set(pool) & acceptable)})
                if split == "train":
                    excluded.append({**base, "query": q, "reason": "multi_positive_in_pool"}); continue
            if split == "train" and "pending_high_similarity" in statuses.values():
                excluded.append({**base, "query": q, "reason": "pending_pair_review",
                                 "pending": [c for c, v in statuses.items() if v == "pending_high_similarity"]}); continue
            splits[split].append(row)

    # ---------------------------------------------------------------- authored rows
    authored, auth_excl = load_authored()
    excluded += [{**x, "provenance": "authored"} for x in auth_excl]
    avecs = embed([r["q"] for r in authored]) if authored else []
    for r, qv in zip(authored, avecs):
        if r.get("label_before") and r["label_before"] != {k: r.get(k) for k in ("case", "gold", "acceptable")}:
            corrections.append({"row_id": f"au:{r['qid']}", "query": r["q"], "before": r["label_before"],
                                "after": {k: r.get(k) for k in ("case", "gold", "acceptable")},
                                "source": "authored verification", "by": r["review"]["by"], "reason": r["review"]["note"]})
        split = route(r)
        acceptable = set(r.get("acceptable") or [])
        if r.get("gold"):
            acceptable.add(r["gold"])
        unknown = [i for i in acceptable | set(r.get("near_ids") or []) if i not in ix.pos]
        base = {"row_id": f"au:{r['qid']}", "canonical_id": r.get("gold"), "section": (r.get("gold") or "none.").split(".")[0],
                "provenance": "adversarial" if r["qid"].startswith(("X1", "X3")) else "synthetic",
                "example_type": r["scenario"], "scenario": r["scenario"], "case": r["case"], "family": r["family"],
                "author": r.get("author"), "review": r["review"], "near_ids": r.get("near_ids", []), "why": r.get("why", "")}
        if unknown:
            excluded.append({**base, "query": r["q"], "reason": "unknown_faq_id", "ids": unknown}); continue
        if acceptable & held and split in ("train", "checkpoint_selection", "calibration"):
            split = "unseen_topics"
        if r["case"] == "ambiguous" and split in ("train", "checkpoint_selection"):
            split = "calibration"
        use_excl = excl if split == "train" else None
        ret = ix.retrieve(qv, excluded=use_excl)
        pool = [ix.ids[m] for m in ret["pool"]]
        doubt, statuses = (label_with_pairs(r["gold"], pool, acceptable, base["row_id"], r["q"])
                           if r.get("gold") else (set(), {}))
        row = make_row(ix, r["q"], ret, acceptable, doubt, base)
        if r["case"] == "ambiguous":
            to_clarify(row, acceptable)
        tr = row["_trace"]
        tr["pair_status"] = statuses
        near = set(r.get("near_ids") or [])
        tr["verified_hard_negatives_in_pool"] = sorted(near & set(pool))
        tr["review_status"] = f"verified:{r['review']['verdict']}"
        if split in ("train", "checkpoint_selection"):
            if tr["doubt_ids_in_pool"] or tr["outcome"] == "multi_positive":
                unresolved.append({**base, "query": r["q"], "reason": tr["outcome"] if tr["outcome"] == "multi_positive" else "pair_query_dependent",
                                   "candidate_ids": pool, "acceptable_ids": sorted(acceptable)})
                split = "calibration"
            elif split == "train" and {c for c, v in statuses.items() if v == "pending_high_similarity"} - near:
                excluded.append({**base, "query": r["q"], "reason": "pending_pair_review"}); continue
        if tr["outcome"] == "candidate_none" and r["case"] == "none":
            tr["none_cause"] = "true_out_of_scope"
        splits[split].append(row)

    # ---------------------------------------------------------------- retrospective / historical
    retro = []
    for name in ("dev_gate", "test_blind"):
        rrows = jl(EVAL_V2 / f"{name}.jsonl")
        for r, rv in zip(rrows, embed([r["q"] for r in rrows])):
            acc = set(r.get("acceptable") or ([r["gold"]] if r.get("gold") else []))
            acc = {i for i in acc if i in ix.pos}
            ret = ix.retrieve(rv)
            base = {"row_id": f"v2:{name}:{r['qid']}", "canonical_id": r.get("gold"), "provenance": "eval_v2_" + name,
                    "example_type": r.get("scenario"), "scenario": r.get("scenario"), "case": r.get("case"),
                    "family": r.get("family"), "read_only": True, "review_status": "eval_v2_verified"}
            row = make_row(ix, r["q"], ret, acc, set(), base)
            if r.get("case") == "ambiguous":
                to_clarify(row, acc)  # same rule as authored ambiguous rows
            retro.append(row)
    splits["retrospective_READ_ONLY"] = retro

    # ---------------------------------------------------------------- leakage filter
    train_states = [r["state"] for r in splits["train"]]
    tvec = embed(train_states)
    tnorm = {norm(s) for s in train_states}
    leak_log = []
    protected = {"historical_READ_ONLY", "retrospective_READ_ONLY"}
    for split in sorted(splits):
        if split == "train" or split in protected:
            continue
        rows = splits[split]
        if not rows:
            continue
        vec = embed([r["state"] for r in rows])
        sims = vec @ tvec.T
        keep = []
        for r, s in zip(rows, sims, strict=True):
            m = int(np.argmax(s))
            if norm(r["state"]) in tnorm or s[m] >= LEAK_COS:
                leak_log.append({"split": split, "row_id": r["meta"]["row_id"], "query": r["state"],
                                 "train_match": train_states[m], "cos": round(float(s[m]), 4)})
                excluded.append({"row_id": r["meta"]["row_id"], "query": r["state"], "reason": f"leak_vs_train:{split}",
                                 "cos": round(float(s[m]), 4)})
            else:
                keep.append(r)
        splits[split] = keep
    # Train rows near the retrospective sealed rows are dropped so that comparison stays honest.
    rvec = embed([r["state"] for r in retro])
    sims = tvec @ rvec.T
    drop = {i for i, s in enumerate(sims) if s.max() >= LEAK_COS} | {
        i for i, s in enumerate(train_states) if norm(s) in {norm(r["state"]) for r in retro}}
    for i in sorted(drop):
        r = splits["train"][i]
        excluded.append({"row_id": r["meta"]["row_id"], "query": r["state"], "reason": "leak_vs_retrospective_sealed"})
    splits["train"] = [r for i, r in enumerate(splits["train"]) if i not in drop]
    # Cross-split near-duplicates between evaluation splits: keep the first by priority.
    priority = ["final_test", "adversarial", "unseen_topics", "calibration", "checkpoint_selection"]
    kept_vecs, kept_norm = list(rvec), {norm(r["state"]) for r in retro}  # retrospective rows win too
    for split in priority:
        rows = splits.get(split, [])
        if not rows:
            continue
        vec = embed([r["state"] for r in rows])
        keep = []
        for r, v in zip(rows, vec, strict=True):
            near = bool(kept_vecs) and float((np.stack(kept_vecs) @ v).max()) >= LEAK_COS
            hit = norm(r["state"]) in kept_norm or (near and r["meta"]["row_id"].startswith("au:"))
            if hit:
                excluded.append({"row_id": r["meta"]["row_id"], "query": r["state"], "reason": f"near_duplicate_across_eval:{split}"})
                continue
            keep.append(r); kept_vecs.append(v); kept_norm.add(norm(r["state"]))
        splits[split] = keep

    export(ix, held, splits, corrections, excluded, unresolved, leak_log)


def emergency_ids() -> set[str]:
    pol = json.loads((W / "work/answer_policy.json").read_text())
    return {i for i, v in pol.items() if v["policy"] == "emergency_direct"}


EMERGENCY = emergency_ids()


def to_clarify(row: dict, acceptable: set[str]) -> None:
    """Ambiguous rows expect the top-3 menu, except when an acceptable FAQ is emergency_direct:
    the app bypasses the menu for those, so the row keeps its direct target (positive / none /
    multi_positive from make_row) and is flagged."""
    if acceptable & EMERGENCY:
        row["_trace"]["emergency_overrides_clarify"] = sorted(acceptable & EMERGENCY)
        return
    row["expected"] = {}
    row["_trace"]["outcome"] = "clarify"


def strip(row: dict) -> dict:
    return {k: v for k, v in row.items() if k != "_trace"}


def decision_reason(tr: dict) -> str:
    """Why the row carries its target, from the final trace (outcome, none cause, review)."""
    o, review = tr["outcome"], tr.get("review_status")
    why = {
        "positive": f"exactly one acceptable FAQ in the pool, at position {tr.get('target_position')}",
        "multi_positive": "several acceptable FAQs in the pool; scored against meta.gold, never trained",
        "clarify": "ambiguous query; expected behaviour is the top-3 clarification menu",
    }.get(o)
    if o == "candidate_none":
        why = ("query outside the knowledge base" if tr.get("none_cause") == "true_out_of_scope"
               else "no acceptable FAQ was retrieved into the pool")
    return f"{why}; review: {review}"


def export(ix, held, splits, corrections, excluded, unresolved, leak_log) -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    layout = {
        "train": "train/train.jsonl", "checkpoint_selection": "validation/checkpoint_selection.jsonl",
        "calibration": "validation/calibration.jsonl", "unseen_topics": "validation/unseen_topics.jsonl",
        "adversarial": "evaluation/adversarial.jsonl", "final_test": "evaluation/final_test_SEALED.jsonl",
        "retrospective_READ_ONLY": "evaluation/retrospective_test_blind_READ_ONLY.jsonl",
    }
    for split, rel in layout.items():
        rows = splits.get(split, [])
        if split == "train":
            wjl(OUT / rel, [strip(r) for r in rows])
            wjl(OUT / "train/metadata.jsonl", [{**r["_trace"], "decision_reason": decision_reason(r["_trace"]),
                                                "split": "train"} for r in rows])
        else:
            wjl(OUT / rel, [{**strip(r), "meta": {**r["meta"], **r["_trace"], "decision_reason": decision_reason(r["_trace"]),
                                                   "split": split}} for r in rows])
    # Historical 1,790 rows: verbatim, read only (old corpus pools; IDs checked in validate_dataset).
    (OUT / "evaluation").mkdir(parents=True, exist_ok=True)
    shutil.copy(HISTORICAL, OUT / "evaluation/historical_READ_ONLY.jsonl")

    write_knowledge(ix, held)
    wjl(OUT / "audit/label_corrections.jsonl", corrections)
    wjl(OUT / "audit/excluded_examples.jsonl", excluded)
    wjl(OUT / "audit/unresolved_ambiguities.jsonl", unresolved)
    wjl(OUT / "audit/leakage_drops.jsonl", leak_log)
    safety = W / "work/safety_issues.json"
    shutil.copy(safety, OUT / "audit/safety_issues.json") if safety.exists() else (OUT / "audit/safety_issues.json").write_text("[]\n")
    counts = {s: len(splits.get(s, [])) for s in layout}
    counts["historical_READ_ONLY"] = sum(1 for _ in open(HISTORICAL))
    families = defaultdict(set)
    for s, rows in splits.items():
        for r in rows:
            families[r["_trace"].get("family")].add(s)
    manifest = {
        "seed": SEED, "unseen_topic_ids": sorted(held), "counts": counts,
        "families_in_several_splits": sorted(f for f, s in families.items() if f and len(s) > 1 and not f.startswith("faq:")),
        "outcomes": {s: dict(Counter(r["_trace"]["outcome"] for r in rows)) for s, rows in splits.items()},
        "review_status": {s: dict(Counter(r["_trace"].get("review_status") for r in rows)) for s, rows in splits.items()},
        "provenance": {s: dict(Counter(r["_trace"].get("provenance") for r in rows)) for s, rows in splits.items()},
        "excluded_reasons": dict(Counter(x["reason"].split(":")[0] for x in excluded)),
        "label_corrections": len(corrections), "unresolved": len(unresolved),
        "inputs_sha256": {
            "label_audit": sha256(AUDIT),
            "pair_sim": sha256(W / "work/pair_sim.json"),
            "train_pools_pairs_todo": sha256(W / "work/pairs_todo.jsonl"),
            "pair_judgments": {p.name: sha256(p) for p in sorted((W / "judgments").glob("pairs*.jsonl"))},
            "authored": {p.name: sha256(p) for p in sorted((W / "authored").glob("*.jsonl"))},
            "authored_verification": {p.name: sha256(p) for p in sorted((W / "judgments").glob("authored_*.jsonl"))},
            "sections": {p.name: sha256(p) for p in sorted((ROOT / "data/knowledge/sections").glob("*.json"))},
        },
    }
    (OUT / "audit/split_manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"counts": counts, "outcomes": manifest["outcomes"], "review": manifest["review_status"]["train"],
                      "excluded": manifest["excluded_reasons"], "corrections": len(corrections)}, ensure_ascii=False))


def write_knowledge(ix, held) -> None:
    labels_path = W / "work/clarification_labels.json"
    clar = json.loads(labels_path.read_text()) if labels_path.exists() else {}
    policy_path = W / "work/answer_policy.json"
    policy = json.loads(policy_path.read_text()) if policy_path.exists() else {}
    view = {json.loads(x)["id"]: json.loads(x) for x in (W / "inputs/kb_view.jsonl").read_text().splitlines()}
    catalog = []
    for p in sorted((ROOT / "data/knowledge/sections").glob("*.json")):
        s = json.loads(p.read_text())
        for e in s["entries"]:
            catalog.append({
                "id": e["id"], "section": s["id"], "label": e["label"], "clarification_label": clar.get(e["id"]),
                "kind": e.get("kind"), "audience": e.get("audience", "visitor"), "answer": e.get("answer"),
                "examples": e.get("examples", []), "sources": e.get("sources", []),
                "last_verified": e.get("last_verified"), "valid_until": e.get("valid_until"),
                "support": view.get(e["id"], {}).get("support"), "answer_policy": policy.get(e["id"], {"policy": "auto_answer"}),
                "unseen_topic_holdout": e["id"] in held,
            })
    k = OUT / "knowledge"
    k.mkdir(parents=True, exist_ok=True)
    (k / "faq_catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + "\n")
    secs = [{"id": s, **{key: ix.sections[s].get(key) for key in ("title", "description", "order", "retrieval")}}
            for s in ix.sec_names]
    (k / "sections.json").write_text(json.dumps({"retrieval_contract": {
        "embedder": "intfloat/multilingual-e5-base", "prefix": "query: (questions and index texts)",
        "index_texts": "label + examples of audience=visitor entries", "k": 5, "min_pool": 3,
        "max_sections": 5, "delta": 0.05, "per_section": "retrieval.top_k", "fill": "flat ranking when pool < 3",
        "option_text": "entry label; '<label> (<section>)' on collision; last option 'ninguna de estas opciones'"},
        "sections": secs}, ensure_ascii=False, indent=1) + "\n")
    (k / "clarification_labels.json").write_text(json.dumps(clar, ensure_ascii=False, indent=1) + "\n")
    for extra in ("confusable_sets.json", "answer_policy.json", "source_manifest.json"):
        src = W / "work" / extra
        if src.exists():
            shutil.copy(src, k / extra)
