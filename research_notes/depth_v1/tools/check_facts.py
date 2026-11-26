"""R7.1 checks on a T3.0 proposal (+ optional review). Script-forced rules, never model judgment:

- every quote ref is a literal substring (folded, whitespace-normalised) of a CAPTURE file
- every field ref names a field that exists; numbers in the fact appear in its support text
- forced KEY: kind safety/rule/action, emergency_direct, steps-derived, disclaimers/caveats
- a complement that one of the entry's questions asks for directly -> KEY
- purged-claims blocklist -> reject the fact

usage: python3 check_facts.py <proposal.jsonl> [<review.jsonl>] [--write <resolved.jsonl>]
Prints a one-screen report. With --write, emits the resolved inventory rows (verifier verdicts and
script rules applied; unsupported facts dropped).
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

from common import DEPTH, RESEARCH, app, content_words, emergency_ids, entries, fold, read_jsonl
from evidence import captures

NUM = re.compile(r"\d[\d.,:]*")
DISCLAIMER = re.compile(r"puede cambiar|confirma|consulta|verifica|antes de (viajar|ir|salir)|no (esta|está) permitido|prohib|evita|no (debes|puedes)", re.I)
PURGED = [re.compile(p["re"], re.I) for p in json.loads((DEPTH / "inputs/purged_claims.json").read_text())["patterns"]]


def normtxt(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(t)))


@lru_cache(maxsize=None)
def file_norm(rel: str) -> str:
    return normtxt((RESEARCH / rel).read_text(errors="replace"))


def nums(t: str) -> set[str]:
    return {re.sub(r"[.,]", "", n).rstrip(":") for n in NUM.findall(t)}


def field_text(e: dict, nat: dict, f: str) -> str:
    if f == "L0":
        return nat.get(e["id"], "")
    v = (e.get("answer") or {}).get(f.split(".", 1)[1] if "." in f else f)
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False) if v else ""


def asked(fact: str, questions: list[str], label: str, l0: str = "") -> bool:
    """A question asks for this fact when it shares >=2 non-topic words with it, covering >=50 % of
    the question's non-topic words. Topic words (label + words in >=25 % of the questions, e.g. the
    species name) say what the entry is about, not which fact is asked."""
    qsets = [content_words(q) for q in questions]
    freq = Counter(w for s in qsets for w in s)
    # Words already in L0 are answered by the key reply, so they cannot make a complement "asked".
    lab = content_words(label) | content_words(l0) | {w for w, c in freq.items() if c >= max(2, len(qsets) / 4)}
    fw = content_words(fact) - lab
    for q in questions:
        qw = content_words(q) - lab
        inter = qw & fw
        if len(inter) >= 2 and len(inter) / max(len(qw), 1) >= 0.5:
            return True
    return False


def check(prop: Path, rev: Path | None):
    E, nat, aug, emerg, caps = entries(), app("natural_replies.json"), app("aug_queries.json"), emergency_ids(), captures()
    reviews = {r["entry_id"]: r for r in read_jsonl(rev)} if rev else {}
    stats, issues, resolved = Counter(), [], []
    for row in read_jsonl(prop):
        eid = row["entry_id"]
        e = E.get(eid)
        if not e:
            issues.append((eid, "-", "unknown entry"))
            continue
        forced = e.get("kind") in ("safety", "rule", "action") or eid in emerg
        qs = (e.get("examples") or []) + (aug.get(eid) or [])
        rv = {v["fid"]: v for v in reviews.get(eid, {}).get("fact_verdicts", [])}
        keep = []
        for f in row.get("facts", []):
            stats["facts"] += 1
            fid, text, sup = f.get("fid"), f.get("text", ""), f.get("support") or []
            bad = None
            sup_text = ""
            for s in sup:
                if "qid" in s:
                    rel = s["qid"].split("#")[0]
                    if rel not in caps:
                        bad = f"quote from non-capture {rel}"
                    elif normtxt(s.get("quote", "")) not in file_norm(rel) or len(s.get("quote", "")) < 20:
                        bad = "quote not literal in file"
                    # The capture file's name identifies the document ("resolucion_207_2023"), so
                    # a fact may cite its number and year (DECISION_LOG 14).
                    sup_text += " " + s.get("quote", "") + " " + Path(rel).stem.replace("_", " ")
                elif "field" in s:
                    ft = field_text(e, nat, s["field"])
                    if not ft:
                        bad = f"empty field {s['field']}"
                    sup_text += " " + ft
            if not sup:
                bad = "no support"
            if not bad and nums(text) - nums(sup_text):
                bad = f"numbers not in support: {sorted(nums(text) - nums(sup_text))}"
            if any(p.search(fold(text)) for p in PURGED):
                bad = "purged claim"
            v = rv.get(fid, {})
            if v.get("support") == "unsupported":
                bad = bad or "verifier: unsupported"
            if v.get("topic_ok") is False or (not v.get("topic_ok", True)):
                bad = bad or "verifier: off-topic"
            if bad:
                stats["rejected"] += 1
                issues.append((eid, fid, bad))
                continue
            if v.get("support") == "partial" and v.get("fixed_text"):
                text = v["fixed_text"]
                stats["narrowed"] += 1
            cls = f.get("class")
            if v.get("should_be") == "complement":
                cls = "complement"  # the forced-key rules below still win
            elif v.get("should_be") == "key" and cls == "complement":
                # A verifier "key" alone does not move a complement (DECISION_LOG 10): some verifiers
                # marked every non-L0 fact key, which would erase R7's partial disclosure. The move
                # stands only when a script rule agrees (below) or L0 already states the fact.
                fw = content_words(text)
                if fw and len(fw & content_words(nat.get(eid, ""))) / len(fw) >= 0.6:
                    cls = "key"
                    stats["verifier_key:in_L0"] += 1
                else:
                    stats["verifier_key:overruled"] += 1
            why = None
            if cls == "complement":
                if forced:
                    why = "forced kind/emergency"
                elif any(s.get("field") == "answer.steps" for s in sup):
                    why = "steps"
                elif DISCLAIMER.search(fold(text)):
                    why = "caveat/disclaimer"
                elif asked(text, qs, e["label"], nat.get(eid, "")):
                    why = "asked by a question"
                if why:
                    stats[f"forced_key:{why}"] += 1
                    cls = "key"
            stats[cls] += 1
            keep.append({"fid": fid, "text": text, "class": cls, "support": sup})
        if not any(k["class"] == "key" for k in keep):
            issues.append((eid, "-", "no key fact left"))
        resolved.append({"entry_id": eid, "facts": keep, "missing_key": reviews.get(eid, {}).get("missing_key", [])})
    return stats, issues, resolved


if __name__ == "__main__":
    a = sys.argv[1:]
    out = None
    if "--write" in a:
        i = a.index("--write")
        out = Path(a[i + 1])
        a = a[:i] + a[i + 2:]
    stats, issues, resolved = check(Path(a[0]), Path(a[1]) if len(a) > 1 else None)
    print(dict(stats))
    comp = Counter(sum(f["class"] == "complement" for f in r["facts"]) for r in resolved)
    print("complements per entry:", dict(sorted(comp.items())))
    for i in issues[:40]:
        print("  ", *i)
    if len(issues) > 40:
        print(f"  ... {len(issues) - 40} more")
    if out:
        out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in resolved))
