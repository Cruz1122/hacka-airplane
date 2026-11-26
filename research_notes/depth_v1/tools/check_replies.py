"""R6.2 / R6.3 / R7.2 / R7.3 checks on L0 reply paraphrases (T5b). Script rules only.

Row (JSONL): {"pid": "<entry_id>#p01", "entry_id", "structure", "register", "atoms": [fid], "text"}

Per row:
- entry known and non-exempt; structure in STRUCTURES; register in REGISTERS
- atoms are complement fids of the entry (assets.ts rejects any other atom)
- numbers: every number of the canonical L0 and of the key facts is in the text (list markers
  "1." excluded); every number in the text is in L0, the key facts or the tagged atoms (DECISION_LOG 15)
- R7.2: an entry with >=2 complements carries at most half of them (floor)
- no emoji; single paragraph allowed with line breaks for steps
Per entry (on the rows that pass):
- R6.3 greedy keep: char-trigram Jaccard < 0.55 (key-fact words removed, DECISION_LOG 17) to every kept text and to the canonical L0,
  and a different first-4-words key
- reports: kept count (goal >= 8), structures used (goal >= 3), distinct atom subsets (goal >= 2
  when >= 2 complements)

usage: python3 check_replies.py <rows.jsonl> [--write <clean.jsonl>] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from common import app, entries, exempt, fold, read_jsonl
from check_facts import nums

STRUCTURES = {"direct", "context", "advice", "question_back"}
REGISTERS = {"warm", "neutral", "brief", "explained"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
MARKER = re.compile(r"(?:^|\n|\s)(\d)[.)]\s")
JACCARD, GOAL, MAXLEN = 0.55, 8, 2.0


def key_mask(facts: list[dict]) -> set[str]:
    """Words every paraphrase must repeat (content words of the key facts, len > 3)."""
    return {w for f in facts if f["class"] == "key" for w in re.findall(r"[a-z0-9]+", fold(f["text"])) if len(w) > 3}


def tri(t: str, mask: frozenset | set = frozenset()) -> set[str]:
    # R6.3 is measured on the wording around the facts: the key-fact words every text must repeat
    # are removed first (DECISION_LOG 17), otherwise short or name-dense entries can never differ.
    s = " ".join(w for w in re.findall(r"[a-z0-9]+", fold(t)) if w not in mask)
    return {s[i:i + 3] for i in range(max(len(s) - 2, 0))}


def jac(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def head4(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(t))[:4])


def strip_markers(t: str) -> str:
    return MARKER.sub(" ", t)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", type=Path)
    ap.add_argument("--write", type=Path)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--base", type=Path, action="append", default=[],
                    help="already approved rows (top-up): kept first, never rejected for similarity")
    a = ap.parse_args()
    E, inv, nat = entries(), app("fact_inventory.json"), app("natural_replies.json")
    why, keep = Counter(), []
    by_entry: dict[str, list] = defaultdict(list)
    bad_rows: list[str] = []
    base_rows = [{**r, "_base": True} for b in a.base for r in read_jsonl(b)]
    for r in base_rows + read_jsonl(a.rows):
        eid, text = r.get("entry_id"), r.get("text") or ""
        e = E.get(eid)
        bad = None
        if not e or exempt(e):
            bad = "unknown or exempt entry"
        else:
            facts = inv.get(eid, [])
            comp = {f["fid"]: f for f in facts if f["class"] == "complement"}
            base_len = max(len(nat.get(eid, "")), sum(len(f["text"]) for f in facts if f["class"] == "key"))
            keyn = set().union(*[nums(f["text"]) for f in facts if f["class"] == "key"]) if facts else set()
            # a canonical number that only a complement carries belongs to that complement: it is
            # required only when the text tags that atom (otherwise nothing could be held back)
            compn = set().union(*[nums(f["text"]) for f in comp.values()]) if comp else set()
            l0n = nums(strip_markers(nat.get(eid, ""))) - (compn - keyn)
            atoms = r.get("atoms") or []
            tn = nums(strip_markers(text))
            atomn = set().union(*[nums(comp[x]["text"]) for x in atoms if x in comp]) if atoms else set()
            allowed = keyn | l0n | atomn
            if r.get("structure") not in STRUCTURES:
                bad = "bad structure"
            elif r.get("register") not in REGISTERS:
                bad = "bad register"
            elif any(x not in comp for x in atoms):
                bad = "atom not a complement fid"
            elif len(comp) >= 2 and len(set(atoms)) > len(comp) // 2:
                bad = "more than half of the complements"
            elif (keyn | l0n) - tn:
                bad = f"missing number {sorted((keyn | l0n) - tn)}"
            elif tn - allowed:
                bad = f"number outside inventory {sorted(tn - allowed)}"
            elif EMOJI.search(text):
                bad = "emoji"
            elif len(text) < 20:
                bad = "too short"
            elif len(text) > MAXLEN * (base_len + sum(len(comp[x]["text"]) for x in atoms if x in comp)):
                # brief rule 6: about the canonical length, <= 1.5x plus the complements it adds.
                # The base is the longer of L0 and the key facts: every key fact must be stated, and in
                # 128 entries they exceed 2x L0, so a canonical-only base rejects every correct text (DECISION_LOG 21)
                bad = "too long"
        if bad:
            why[bad.split(" [")[0]] += 1
            bad_rows.append(f"{r.get('pid')}: {bad}")
            continue
        by_entry[eid].append(r)
    report = {}
    for eid, rows in by_entry.items():
        ncomp = sum(1 for f in inv.get(eid, []) if f["class"] == "complement")
        # R7.6: with >=2 complements the canonical text leaves the rotation, so R6.3 compares
        # the paraphrases only among themselves; otherwise the canonical is part of the set.
        canon = ncomp < 2
        mask = key_mask(inv.get(eid, []))
        T = [tri(r["text"], mask) for r in rows]
        H = [head4(r["text"]) for r in rows]
        ct, ch = tri(nat.get(eid, ""), mask), head4(nat.get(eid, ""))
        sim = [[jac(T[i], T[j]) if i != j else 0.0 for j in range(len(rows))] for i in range(len(rows))]
        # greedy max set: fewest conflicts first, so one bad text does not evict two good ones
        conflicts = [sum(1 for j in range(len(rows)) if j != i and (sim[i][j] >= JACCARD or H[i] == H[j]))
                     for i in range(len(rows))]
        kept_i: list[int] = []
        for i in sorted(range(len(rows)), key=lambda i: (not rows[i].get("_base"), conflicts[i], i)):
            if canon and (jac(T[i], ct) >= JACCARD or H[i] == ch):
                why["too close to canonical"] += 1
                bad_rows.append(f"{rows[i].get('pid')}: vs canonical jaccard {jac(T[i], ct):.2f}")
                continue
            clash = [j for j in kept_i if sim[i][j] >= JACCARD or H[i] == H[j]]
            if clash:
                j = max(clash, key=lambda j: sim[i][j])
                why["same first 4 words" if H[i] == H[j] else "trigram jaccard"] += 1
                bad_rows.append(f"{rows[i].get('pid')}: vs {rows[j].get('pid')} jaccard {sim[i][j]:.2f}"
                                + (" same first 4 words" if H[i] == H[j] else ""))
                continue
            kept_i.append(i)
        everything = [rows[i] for i in sorted(kept_i)]
        kept = [r for r in everything if not r.get("_base")]
        keep += kept
        report[eid] = {"kept": len(everything), "structures": len({r["structure"] for r in everything}),
                       "subsets": len({tuple(sorted(r.get("atoms") or [])) for r in everything}), "complements": ncomp}
    low = {k: v for k, v in report.items()
           if v["kept"] < GOAL or v["structures"] < 3 or (v["complements"] >= 2 and v["subsets"] < 2)}
    print(json.dumps({"rows_kept": len(keep), "rejected": dict(why), "entries": len(report),
                      "below_goal": len(low)}, ensure_ascii=False))
    if not a.quiet:
        for x in bad_rows[:120]:
            print("  ", x)
        for k, v in list(low.items())[:20]:
            print("  low", k, v)
    if a.write:
        a.write.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep))
        a.write.with_suffix(".low.json").write_text(json.dumps(low, ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main()
