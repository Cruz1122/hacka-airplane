"""E8: prompt variants for Laya PT/ES NLI as an answer selector (choice / noul / score).

The task: given the visitor query and the top-k candidate entries from e5-base (flat kNN), pick the
entry whose curated answer best answers the query, or abstain.

  uv run python prompts_exp.py            # all variants, k=5 (k=3 is the top-3 subset)
"""

from __future__ import annotations

import json
import time

import numpy as np
from exp import (
    NLI_CRITERIA,
    OUT,
    Embedder,
    abstention,
    build_index,
    ci,
    entry_scores,
    load_eval,
    load_laya,
    nli_question,
)
from kb import load_sections

K = 5
SETS = ("paraphrase", "out_of_scope", "near_miss")


def first_sentence(text: str, limit: int = 160) -> str:
    s = text.split(". ")[0].strip()
    return (s if s.endswith(".") else s + ".")[:limit]


def nli(state_fn, hyp_fn):
    """Per-candidate 3-way NLI; score = P(entailment)."""

    def build(q, e):
        return state_fn(q, e), nli_question(hyp_fn(q, e))

    return {"kind": "nli", "build": build}


def noul(instr: str, state_fn, false: str, true: str):
    def build(q, e):
        return state_fn(q, e), {
            "type": "noul",
            "instructions": instr,
            "criteria": {"false": false, "true": true},
            "labels": {"false": "no", "true": "sí"},
        }

    return {"kind": "noul", "build": build}


def score(instr: str, state_fn, levels: list[str]):
    def build(q, e):
        return state_fn(q, e), {"type": "score", "instructions": instr, "criteria": levels}

    return {"kind": "score", "build": build}


QA_STATE = lambda q, e: {"pregunta del visitante": q, "respuesta candidata": e.answer}  # noqa: E731
QL_STATE = lambda q, e: {"pregunta del visitante": q, "tema": e.label, "respuesta": first_sentence(e.answer)}  # noqa: E731
LEVELS4 = [
    "no tiene relación con la pregunta",
    "es del mismo tema pero no contesta la pregunta",
    "contesta la pregunta en parte",
    "contesta exactamente lo que pregunta el visitante",
]

PER_CANDIDATE = {
    "nli_label": nli(lambda q, e: q, lambda q, e: f"El visitante pregunta sobre {e.label}."),
    "nli_quiere_saber": nli(lambda q, e: q, lambda q, e: f"El visitante quiere saber {e.label}."),
    "nli_answer_premise": nli(lambda q, e: e.answer, lambda q, e: f"Este texto responde la pregunta «{q}»."),
    "nli_qa_pair": nli(
        lambda q, e: f"Pregunta del visitante: {q}\nRespuesta: {e.answer}",
        lambda q, e: "La respuesta contesta lo que pregunta el visitante.",
    ),
    "noul_answers": noul(
        "¿La respuesta candidata contesta la pregunta del visitante?",
        QA_STATE,
        "no la contesta o habla de otra cosa",
        "sí contesta lo que el visitante pregunta",
    ),
    "noul_label": noul(
        "¿La pregunta del visitante trata exactamente de este tema?",
        QL_STATE,
        "trata de otra cosa",
        "trata exactamente de este tema",
    ),
    "score_answer": score("¿Qué tan bien contesta la respuesta candidata la pregunta del visitante?", QA_STATE, LEVELS4),
    "score_label": score("¿Qué tan bien corresponde el tema a la pregunta del visitante?", QL_STATE, LEVELS4),
}


def choice_q(kind: str, q: str, cands: list) -> tuple:
    if kind == "choice_label":
        crit = {e.id: e.label for e in cands}
        instr = "¿Qué tema contesta la pregunta del visitante?"
    else:  # choice_answer
        crit = {e.id: f"{e.label}: {first_sentence(e.answer, 110)}" for e in cands}
        instr = "¿Qué respuesta contesta mejor la pregunta del visitante?"
    crit["none"] = "ninguna contesta la pregunta"
    return q, {"type": "choice", "instructions": instr, "criteria": crit}


def cand_score(kind: str, ans: dict) -> float:
    if kind == "nli":
        return float(ans["probabilities"]["entailment"])
    if kind == "noul":
        return float(ans["noul"]) if "noul" in ans else float(ans["probabilities"]["true"])
    # score: expected level in [0, 1]
    probs = ans["probabilities"]
    vals = [float(probs[k]) for k in sorted(probs, key=lambda x: int(x))] if all(
        str(k).isdigit() for k in probs
    ) else list(map(float, probs.values()))
    return float(sum(i * p for i, p in enumerate(vals)) / (len(vals) - 1))


def main() -> None:
    _, entries = load_sections()
    emb = Embedder("e5-base")
    index = build_index(emb, entries)
    agent = load_laya()
    queries = [(s, r) for s in SETS for r in load_eval(s)]
    qv = emb([r["q"] for _, r in queries], query=True)
    # Sanity print of one answer structure per type, so cand_score reads the right field.
    e0 = entries[0]
    for name in ("noul_answers", "score_answer"):
        st, qd = PER_CANDIDATE[name]["build"]("hola", e0)
        print(name, json.dumps(agent.system_one(st, {"x": qd})["answers"]["x"], ensure_ascii=False)[:300])

    rows = []
    lat: dict[str, list[float]] = {}
    for (set_name, r), v in zip(queries, qv, strict=True):
        s = entry_scores(index, v)
        top = list(np.argsort(-s)[:K])
        cands = [entries[i] for i in top]
        row = {"set": set_name, "q": r["q"], "expected": r["expected"], "pool": [e.id for e in cands],
               "emb": [float(s[i]) for i in top]}
        for name, spec in PER_CANDIDATE.items():
            # One call per candidate state (states differ), timed as a batch over the pool.
            built = [spec["build"](r["q"], e) for e in cands]
            t0 = time.perf_counter()
            same_state = len({json.dumps(b[0], ensure_ascii=False) for b in built}) == 1
            same_q = len({json.dumps(b[1], ensure_ascii=False) for b in built}) == 1
            if same_state:  # one forward pass, one question per candidate
                out = agent.system_one(built[0][0], {f"c{i}": b[1] for i, b in enumerate(built)})
                answers = [out["answers"][f"c{i}"] for i in range(len(built))]
            elif same_q:  # one batched pass, one state per candidate
                outs = agent.predict_batch([b[0] for b in built], {"x": built[0][1]})
                answers = [o["answers"]["x"] for o in outs]
            else:
                answers = [agent.system_one(b[0], {"x": b[1]})["answers"]["x"] for b in built]
            lat.setdefault(name, []).append(time.perf_counter() - t0)
            row[name] = [cand_score(spec["kind"], a) for a in answers]
        for kind in ("choice_label", "choice_answer"):
            for k in (3, 5):
                st, qd = choice_q(kind, r["q"], cands[:k])
                t0 = time.perf_counter()
                out = agent.system_one(st, {"x": qd})["answers"]["x"]["probabilities"]
                lat.setdefault(f"{kind}_k{k}", []).append(time.perf_counter() - t0)
                row[f"{kind}_k{k}"] = [float(out[e.id]) for e in cands[:k]]
                row[f"{kind}_k{k}_none"] = float(out["none"])
        rows.append(row)
    (OUT / "prompt_rows.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    report = {"latency_ms_p50_k5": {k: round(1000 * float(np.median(v)), 1) for k, v in lat.items()},
              "results": summarize(rows)}
    (OUT / "prompts.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print_table(report)


def summarize(rows: list[dict]) -> dict:
    para = [r for r in rows if r["set"] == "paraphrase"]
    res = {}
    variants = [("emb_only", "emb", None)]
    for name in PER_CANDIDATE:
        variants += [(name, name, None), (name + "+emb", name, "emb")]
    for kind in ("choice_label", "choice_answer"):
        for k in (3, 5):
            variants += [(f"{kind}_k{k}", f"{kind}_k{k}", None), (f"{kind}_k{k}+emb", f"{kind}_k{k}", "emb")]
    for name, key, add in variants:
        for k in (3, 5):
            if key.startswith("choice") and not key.endswith(f"k{k}"):
                continue

            def sc(r, key=key, add=add, k=k):
                base = r[key][:k]
                return [a + b for a, b in zip(base, r["emb"][:k], strict=True)] if add else base

            pick = lambda r, sc=sc, k=k: r["pool"][:k][int(np.argmax(sc(r)))]  # noqa: E731
            top1 = ci(sum(pick(r) in r["expected"] for r in para), len(para))
            tagged = [dict(r, _p=pick(r), _c=float(max(sc(r)))) for r in rows]
            ab = abstention(tagged, conf=lambda r: r["_c"], pick=lambda r: r["_p"])
            res[f"{name}@k{k}"] = {"top1": top1["rate"], "lo": top1["lo"], "hi": top1["hi"], **ab}
    ceil = {k: round(np.mean([bool(set(r["pool"][:k]) & set(r["expected"])) for r in para]), 4) for k in (3, 5)}
    res["_ceiling_correct_in_pool"] = ceil
    return res


def print_table(report: dict) -> None:
    print("latency p50 ms (k=5):", report["latency_ms_p50_k5"])
    print(f"{'variant':34s} top1   auroc  cov@3%  wrong")
    for k, v in report["results"].items():
        if k.startswith("_"):
            print(k, v)
            continue
        print(f"{k:34s} {v['top1']:.3f}  {v['auroc_in_vs_out']:.3f}  {v['cv_correct_coverage']:.3f}  {v['cv_wrong_rate']:.3f}")


if __name__ == "__main__":
    _ = NLI_CRITERIA
    main()
