"""R1/R2/R5.2 checks on approved training rows (variants or conversation turns). Script rules only.

Row formats (JSONL):
  variant:      {"entry_id", "text", "bucket", ...}
  conversation: {"entry_id", "conv_id", "type", "turns": [{"text", "entry_id"}], ...}

Checks:
- normalised dedup inside an entry (variants: text; conversations: last-turn text + type)
- same-entry near-dup: e5 cos >= 0.93 between two variants of one entry -> keep the first
- continuation lint (R2.4): no turn may be a bare continuation cue
- leak vs blind_v4 (dev AND sealed, R5.2): exact normalised match or cos >= 0.93 to any v4 turn.
  Uses blind_v4/all_rows.jsonl (texts only, written before the split): v4_sealed is never opened.
- per-entry approved counts and bucket / type mix

usage (nlu venv): uv run python ../../research_notes/depth_v1/tools/check_rows.py <rows.jsonl> --kind variant|conversation [--write <clean.jsonl>]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from common import DEPTH, content_words, entries, fold, read_jsonl
from emb import embed, norm

CUE = re.compile(r"^\W*(sigue|segui|continua|continue|cuentame mas|y que mas|que mas|mas|y\?|por que|porque|"
                 r"explicame mejor|dale|tell me more|go on|more)\W*$")
NEAR, LEAK = 0.93, 0.93


def key(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(t)))


def v4_texts() -> list[str]:
    out = set()
    for r in read_jsonl(DEPTH / "blind_v4/all_rows.jsonl"):
        out |= {norm(t) for t in r["turns"]}
    return sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", type=Path)
    ap.add_argument("--kind", choices=["variant", "conversation"], required=True)
    ap.add_argument("--write", type=Path)
    a = ap.parse_args()
    E = entries()
    rows = read_jsonl(a.rows)
    v4 = v4_texts()
    v4k = {key(t) for t in v4}
    texts = [r["text"] for r in rows] if a.kind == "variant" else [t["text"] for r in rows for t in r["turns"]]
    V = embed(texts + v4)
    tv, v4v = V[: len(texts)], V[len(texts):]
    leak_cos = (tv @ v4v.T).max(axis=1) if len(texts) else np.zeros(0)
    stats, why, keep = Counter(), Counter(), []
    seen: dict[str, set] = defaultdict(set)
    kept_vecs: dict[str, list] = defaultdict(list)
    kept_words: dict[str, list] = defaultdict(list)
    ti = 0
    for r in rows:
        eid = r["entry_id"]
        n = 1 if a.kind == "variant" else len(r["turns"])
        idx = list(range(ti, ti + n))
        ti += n
        stats["rows"] += 1
        if eid not in E:
            why["unknown entry"] += 1
            continue
        tt = [r["text"]] if a.kind == "variant" else [t["text"] for t in r["turns"]]
        bad = None
        if a.kind == "conversation":
            if any(t.get("entry_id") not in E for t in r["turns"]):
                bad = "turn id unknown"
            elif r["turns"][-1].get("entry_id") != eid:
                bad = "last turn not the target"
        if not bad and any(CUE.match(key(t)) for t in tt):
            bad = "continuation cue"
        if not bad and any(key(t) in v4k for t in tt):
            bad = "leak exact"
        if not bad and any(leak_cos[i] >= LEAK for i in idx):
            bad = "leak cos"
        k = key(tt[0]) if a.kind == "variant" else f"{r.get('type')}|{key(tt[-1])}|{key(tt[0])}"
        if not bad and k in seen[eid]:
            bad = "dup"
        if not bad and a.kind == "variant" and kept_vecs[eid]:
            # ft4 is trained to pull an entry's queries together, so cos >= 0.93 alone also hits
            # differently worded variants (DECISION_LOG 13): a near-dup must also share >= 50 %
            # of its content words with the kept variant it is close to.
            sims = np.stack(kept_vecs[eid]) @ tv[idx[0]]
            cw = content_words(tt[0])
            for j in np.nonzero(sims >= NEAR)[0]:
                other = kept_words[eid][j]
                if cw and other and len(cw & other) / len(cw | other) >= 0.5:
                    bad = "near-dup"
                    break
        if bad:
            why[bad] += 1
            continue
        seen[eid].add(k)
        if a.kind == "variant":
            kept_vecs[eid].append(tv[idx[0]])
            kept_words[eid].append(content_words(tt[0]))
        keep.append(r)
    per = Counter(r["entry_id"] for r in keep)
    goal_hi = 20 if a.kind == "variant" else 8
    low = [e for e in {r["entry_id"] for r in rows} if per[e] < (10 if a.kind == "variant" and E.get(e, {}).get("section") == "conversation" else goal_hi)]
    mix = Counter(r.get("bucket") if a.kind == "variant" else r.get("type") for r in keep)
    print(dict(stats), "kept", len(keep), "rejected", dict(why))
    print("mix", dict(mix), "entries", len(per), "below goal", len(low))
    if a.write:
        a.write.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep))
        (a.write.with_suffix(".low.json")).write_text(json.dumps(sorted(low), indent=0))


if __name__ == "__main__":
    main()
