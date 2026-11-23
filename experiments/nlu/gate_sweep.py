"""Sweep follow-up gates and an off-topic floor on the phone-faithful scores (exported assets + GGUF).

usage (laya venv): uv run python ../nlu/gate_sweep.py --gguf ../../models/knowledge/e5-nlu-ft3-f16.gguf [--blind work/blind_v2]
Gates: 'words' (<= max_words), 'words_low' (<= max_words and own top < b), 'cue' (starts with a
connective or <= 2 words). Floor tau: a final top score below tau answers conversation.off_topic_question.
"""
from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "laya")); sys.path.insert(0, str(HERE))
from evaluate import load_blind  # noqa: E402
from export_knowledge import ASSETS, embed_gguf  # noqa: E402
from export_nlu import entry_scores, fuse  # noqa: E402

ROOT = HERE.parents[1]
CUE = re.compile(r"^[¿¡\s]*(y|e|o|pero|entonces|eso|esa|ese|esos|esas|ahí|ahi|allá|alla|con|sin|para|pa|en|también|tambien|y\?)\b", re.I)
OFF = "conversation.off_topic_question"


def load_v2(d: Path) -> list[dict]:
    lab = {}
    for p in sorted(d.glob("labels_*.jsonl")):
        for l in p.read_text().splitlines():
            r = json.loads(l); lab[r["qid"]] = r
    rows = []
    for p in sorted(d.glob("queries_*.jsonl")):
        for l in p.read_text().splitlines():
            r = json.loads(l)
            if r["qid"] in lab:
                rows.append({**r, "acceptable": lab[r["qid"]]["acceptable"], "split": "v2"})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gguf", type=Path, required=True)
    ap.add_argument("--llama-embedding", type=Path, default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding")
    ap.add_argument("--blind", type=Path)
    a = ap.parse_args()
    catalog = json.loads((ASSETS / "catalog.json").read_text())
    m = json.loads((ASSETS / "index.json").read_text())
    vec = np.fromfile(ROOT / "models/knowledge" / m["vectors"]["file"], dtype="<f4").reshape(m["rows"], m["dims"])
    tv, owner = vec[: m["text_rows"]], np.asarray(m["row_entry"])
    ids = [e["id"] for e in catalog]; off = ids.index(OFF)
    rows = load_blind() + (load_v2(a.blind) if a.blind else [])
    # Topic switch: a standalone question after an unrelated first turn must not be pulled back.
    import random
    rnd = random.Random(7)
    singles = [r for r in rows if len(r["turns"]) == 1 and r["acceptable"]]
    firsts = [r["turns"][0] for r in rows]
    rows += [{**r, "turns": [rnd.choice([f for f in firsts if f != r["turns"][0]]), r["turns"][0]], "split": "switch"}
             for r in singles]
    norm = lambda t: " ".join(t.split())  # noqa: E731
    texts = {norm(t) for r in rows for t in r["turns"]}
    for r in rows:
        for i in range(1, len(r["turns"])):
            texts.add(norm(f"{r['turns'][i-1]} {r['turns'][i]}"))
            texts.add(norm(" ".join(r["turns"][: i + 1])))
    texts = sorted(texts)
    qv = dict(zip(texts, embed_gguf(texts, a.gguf, a.llama_embedding), strict=True))
    S = {t: entry_scores((tv @ v).astype(np.float32), owner, len(ids), 3) for t, v in qv.items()}

    def run(mw, b, w, tau, chain, demote):
        res, rep = {}, [0, 0]
        for r in rows:
            prev, fused, prev_id = None, False, None
            for t in r["turns"]:
                s, fused = S[norm(t)], False
                if prev is not None and (bool(CUE.match(t)) or (len(t.split()) <= mw and s.max() < b)):
                    s, fused = fuse(s, S[norm(f"{prev} {t}")], w), True
                order = np.argsort(-s, kind="stable")
                top = int(order[0])
                if fused and demote and ids[top] == prev_id:
                    top = int(order[1])
                pid = ids[top] if s[top] >= tau or fused else OFF
                cur_id = pid
                prev = " ".join(f"{prev} {t}".split()[-60:]) if (chain and fused) else t
                last_prev_id, prev_id = prev_id, cur_id
            ok = (pid in r["acceptable"]) if r["acceptable"] else pid == OFF
            if len(r["turns"]) > 1 and not ok:
                rep[0] += 1; rep[1] += pid == last_prev_id
            res.setdefault(r["split"], []).append(ok)
            if len(r["turns"]) > 1:
                res.setdefault(r["split"] + ":fu", []).append(ok)
        out = {k: round(float(np.mean(v)), 3) for k, v in sorted(res.items())}
        out["fu_fail_repeat"] = f"{rep[1]}/{rep[0]}"
        return out

    for demote in (False, True):
        r = run(5, 0.7, 5.0, 0.5, True, demote)
        print("demote", demote, r)


if __name__ == "__main__":
    main()
