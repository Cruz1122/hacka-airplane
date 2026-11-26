"""Export the knowledge runtime the phone runs, NLU v1 (replaces export_knowledge.py's output).

  cd experiments/laya && uv run python ../nlu/export_nlu.py --gguf ../../models/knowledge/e5-nlu-f16.gguf \
      --T 0.0 --w 0.5 --max-words 6 --below 0.0

What changed against export_knowledge.py (same asset format, read by mobile/src/core/knowledge):
- index rows: label + examples + data/knowledge/app aug queries + 2-turn conversations, embedded
  as written (filler stripping measured no gain, so it is off), plus the 37 hubs of data/knowledge/app/hubs.json;
- entry score: mean of the entry's best `score_topk` row cosines (policy.score_topk = 3);
- reply text: data/knowledge/app/natural_replies.json (curated facts rewritten, fidelity-reviewed),
  hubs: their reviewed reply; no title shown;
- follow-up: policy.followup fuses the previous turn's entry scores (engine.ts);
- section gating is disabled (every section gated): top-1 is the global best entry, as evaluated.

Writes GENERATED files (never edit them): mobile/assets/data/knowledge/{catalog,sections,policy,
index}.json, <out-bin>/{index.f32.bin,index_scorer.onnx}, and the TS parity fixtures
mobile/src/core/knowledge/__fixtures__/{retrieval,clean}.json.
T / w / max-words / below come from the blind dev split (experiments/nlu/context_eval.py).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "laya"))
sys.path.insert(0, str(HERE))

from export_knowledge import (  # noqa: E402
    ASSETS, EMERGENCY_LINE_ID, FIXTURES, PREFIX, SECTIONS, corpus_hash, embed_gguf, write_scorer,
)
from kb import APP, app_texts, clean  # noqa: E402

ROOT = HERE.parents[1]
K, SCORE_TOPK = 5, 3
VERSION = "e5-nlu-v1"
# A turn opening with a connective continues the previous topic (engine.ts isFollowup, gguf_eval.py).
# Lookahead instead of \\b: JS \\b is ASCII-only, so "ahí" would never match there.
CUE = r"^[¿¡\s]*(?:y|e|o|pero|entonces|eso|esa|ese|esos|esas|ahí|ahi|allá|alla|con|sin|para|pa|en|también|tambien)(?=[\s?,.!]|$)"


# "Sigue" cue (engine.ts continuation): matched against the WHOLE accent-folded message
# (safety.foldText: lowercase, a-z0-9 words, doubled vowels collapsed), so "¿sigue abierto?" or
# "más cerca de Pereira" never match.
_LEAD = r"(?:(?:ok|okay|oki|vale|bueno|dale|si|claro|listo|bien|entonces|pero|y|eh|mm|hola|gracias|perfecto|genial)\s+){0,2}"
_TAIL = r"(?:\s+(?:por\s?favor|porfa|porfavor|porfis|pls|plis|gracias|pues|ya|ahora|ok|dale))?"
_MAS = r"(?:mass?|maz)"
_CORE = (
    r"(?:sigue|sige|siga|sigamos|sigu|siguie|siegue|sigeu|sgue|sique"
    r"|continua|continuar|continue|continuemos|contina|contiua|cotinua|contnua|continia|kontinua|cntinua"
    rf"|{_MAS}(?:\s+(?:detalles?|info|informacion|datos|despacio|por\s?favor|porfa))?"
    rf"|(?:que|ke|qe|q|k)\s+{_MAS}"
    rf"|(?:un\s+poco|algo\s+de|con)\s+{_MAS}(?:\s+detalles?)?"
    rf"|(?:cuentame|cuenta|dime|dame|explicame|quiero\s+saber|quiero)\s+{_MAS}(?:\s+(?:detalles?|info|informacion|datos))?"
    r"|explicame\s+mejor|explica\s+mejor|explicalo\s+mejor|explicamelo\s+mejor"
    r"|amplia|ampliame|ampliar|amplialo|ampliala|amplia\s+(?:eso|esto)|profundiza|detalla|detallame)"
)
CONT_CUE = rf"^{_LEAD}{_CORE}{_TAIL}$"
CONT_WHY_CUE = r"^(?:y\s+)?(?:por\s?que|porque|por\s?ke|porke|pq|xq|x\s?que)(?:\s+(?:eso|es\s+asi|pues))?$"
CONT_BRIDGES = ["Relacionado con esto:", "Y sobre un tema cercano:", "Cambiando un poco de punto:", "Algo más del parque:"]
CONT_TEXTS = {
    "no_state": "¿Sobre qué tema quieres que siga?",
    "exhausted": "No tengo más detalle verificado sobre esto.",
    "related": "Puedo contarte sobre {topics}.",
}


def depth_assets(entries: list[dict]) -> tuple[dict | None, dict | None]:
    """(depth.json payload, policy.continuation) from the three T3/T5b outputs; (None, None) when absent.

    depth_replies.json  {id: {layers: [{kind, texts: [str | {text, atoms}]}], walk: [id]}}
    reply_variants.json {id: [{text, atoms, emergency_ok?}]}   (emergency_ok: second verifier, R6.6)
    fact_inventory.json {id: [{fid, class: key|complement, ...}]}
    """
    paths = [APP / n for n in ("depth_replies.json", "reply_variants.json", "fact_inventory.json")]
    if not all(p.exists() for p in paths):
        return None, None
    replies, variants, inv = (json.loads(p.read_text()) for p in paths)
    ids = {e["id"] for e in entries}
    emer = {k for k, v in json.loads((APP / "answer_policy.json").read_text()).items()
            if v.get("policy") == "emergency_direct"}

    def txt(t: object) -> dict:
        t = t if isinstance(t, dict) else {"text": t, "atoms": []}
        return {"text": t["text"], "atoms": list(t.get("atoms", []))}

    out: dict[str, dict] = {}
    for eid in sorted(ids & (set(replies) | set(variants))):
        r = replies.get(eid, {})
        raw = variants.get(eid, [])
        d = {
            "l0": [txt(t) for t in raw],
            "layers": [{"kind": l["kind"], "texts": [txt(t) for t in l["texts"]]} for l in r.get("layers", [])],
            "walk": [w for w in r.get("walk", []) if w in ids and w != eid],
            "complements": [f["fid"] for f in inv.get(eid, []) if f.get("class") == "complement"],
        }
        if eid in emer:
            d["rotation"] = [i for i, t in enumerate(raw) if t.get("emergency_ok")]
        out[eid] = d
    return {"entries": out}, {
        "cue": CONT_CUE, "max_words": 6, "why_cue": CONT_WHY_CUE,
        "bridges": CONT_BRIDGES, "texts": CONT_TEXTS,
    }


def load() -> tuple[dict, list[dict]]:
    sections, entries = {}, []
    for p in sorted(SECTIONS.glob("*.json")):
        s = json.loads(p.read_text())
        sid = s.get("id", p.stem)
        sections[sid] = s
        for e in s["entries"]:
            if e.get("audience", "visitor") == "visitor":
                entries.append({**e, "section": sid})
    by_id = {e["id"]: e for e in entries}
    for h in json.loads((APP / "hubs.json").read_text()):
        members = [by_id[m] for m in h["members"]]  # KeyError = a hub names a missing entry
        seen, sources = set(), []
        for m in members:
            for s in m.get("sources", []):
                if s.get("url", s["label"]) not in seen:
                    seen.add(s.get("url", s["label"]))
                    sources.append(s)
        entries.append({"id": h["id"], "section": members[0]["section"], "kind": "faq", "label": h["label"],
                        "examples": h["examples"], "reply": h["reply"], "sources": sources,
                        "last_verified": max((m.get("last_verified") or "" for m in members), default="") or None})
    return sections, entries


def entry_scores(sims: np.ndarray, owner: np.ndarray, n: int, k: int) -> np.ndarray:
    """float32 mean of each entry's best k row sims, summed sequentially (the TS contract)."""
    out = np.full(n, -1.0, dtype=np.float32)
    order = np.argsort(owner, kind="stable")
    bounds = np.searchsorted(owner[order], np.arange(n + 1))
    for e in range(n):
        rows = sims[order[bounds[e] : bounds[e + 1]]]
        if not len(rows):
            continue
        best = np.sort(rows)[::-1][:k].astype(np.float32)
        acc = np.float32(best[0])
        for v in best[1:]:
            acc = np.float32(acc + v)
        out[e] = np.float32(acc / np.float32(len(best)))
    return out


def fuse(s: np.ndarray, prev: np.ndarray, w: float) -> np.ndarray:
    w32 = np.float32(w)
    return ((s + w32 * prev).astype(np.float32) / np.float32(1 + w32)).astype(np.float32)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gguf", type=Path, required=True)
    ap.add_argument("--llama-embedding", type=Path,
                    default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding")
    ap.add_argument("--out-bin", type=Path, default=ROOT / "models/knowledge")
    ap.add_argument("--T", type=float, required=True)
    ap.add_argument("--w", type=float, required=True)
    ap.add_argument("--max-words", type=int, required=True)
    ap.add_argument("--below", type=float, required=True)
    ap.add_argument("--mode", choices=["scores", "concat"], default="concat",
                    help="follow-up context: previous turn's scores, or the joined previous+current text")
    ap.add_argument("--cue", action="store_true", help="gate follow-ups by CUE or (short and below)")
    ap.add_argument("--fixture-rows", type=int, default=60)
    ap.add_argument("--no-train-rows", action="store_true",
                    help="index without train_variants/train_convs (they lowered v4_dev with ft5/ft5b)")
    a = ap.parse_args()

    sections, entries = load()
    natural = json.loads((APP / "natural_replies.json").read_text())
    extra = app_texts(conv=True, variants=not a.no_train_rows, train_convs=not a.no_train_rows)
    sec_names = list(sections)
    redirects = {k: v for k, v in json.loads((APP / "redirects.json").read_text()).items() if not k.startswith("_")}
    pos = {e["id"]: n for n, e in enumerate(entries)}
    texts, owner = [], []
    for n, e in enumerate(entries):
        # A redirected entry's rows retrieve its target (a meta reply -> the content hub).
        n = pos[redirects.get(e["id"], e["id"])]
        for t in [e["label"], *e.get("examples", []), *extra.get(e["id"], [])]:
            t = " ".join(t.split())  # llama-embedding reads one prompt per line
            if t:
                texts.append(t)
                owner.append(n)
    owner = np.asarray(owner)
    desc = [sections[s].get("description", "") for s in sec_names]

    probe_q = [r["turns"][-1] for r in map(json.loads, (HERE / "work/queries_raw.jsonl").read_text().splitlines())]
    probe_q = probe_q[: a.fixture_rows]
    allv = embed_gguf(texts + desc + [" ".join(q.split()) for q in probe_q], a.gguf, a.llama_embedding)
    vec, qv = allv[: len(texts) + len(desc)], allv[len(texts) + len(desc) :]
    emb_id = {"kind": "gguf", "file": a.gguf.name, "bytes": a.gguf.stat().st_size,
              "sha256": hashlib.sha256(a.gguf.read_bytes()).hexdigest()}

    a.out_bin.mkdir(parents=True, exist_ok=True)
    bin_path = a.out_bin / "index.f32.bin"
    vec.astype("<f4").tofile(bin_path)
    bin_sha = hashlib.sha256(bin_path.read_bytes()).hexdigest()
    scorer_path = a.out_bin / "index_scorer.onnx"
    write_scorer(vec, scorer_path)

    apol = json.loads((APP / "answer_policy.json").read_text())
    ids = {e["id"] for e in entries}
    emergency_ids = sorted(k for k, v in apol.items() if v.get("policy") == "emergency_direct" and k in ids)
    emer = set(emergency_ids)
    missing = [e["id"] for e in entries if "reply" not in e and e["id"] not in natural]
    if missing:
        raise SystemExit(f"no natural reply for {missing[:5]} (+{len(missing) - 5})")
    catalog = []
    for e in entries:
        kind = "action" if e.get("kind") == "action" else "emergency" if e["id"] in emer else "faq"
        catalog.append({
            "id": e["id"], "section": e["section"], "kind": kind, "label": e["label"], "menu_label": e["label"],
            "short": e.get("reply") or natural[e["id"]], "steps": [], "sources": e.get("sources", []),
            "last_verified": e.get("last_verified"),
        })
    sec_out = [{"id": s, "order": sections[s].get("order"), "title": sections[s].get("title"),
                "top_k": K, "featured": sections[s].get("featured", [])} for s in sec_names]
    # The urgent banner shows the 123 entry's reply: its natural version, not the dated police note.
    policy = {
        "version": VERSION, "T": a.T, "k": K, "min_pool": 1, "max_sections": len(sec_names), "delta": 2.0,
        "score_topk": SCORE_TOPK, "strip_fillers": False,
        "followup": {"mode": a.mode, "w": a.w, "max_words": a.max_words, "below": a.below,
                     "cue": CUE if a.cue else None},
        "fitted_on": "experiments/nlu blind dev split (context_eval.py / evaluate.py)",
        "emergency_direct": emergency_ids, "emergency_line_id": EMERGENCY_LINE_ID,
        "texts": {
            "abstain": "Eso no lo tengo en la guía: solo sé del Parque Los Nevados (cómo llegar, reservas, horarios, clima, seguridad, normas, fauna y flora). ¿Me lo preguntas de otra forma?",
            "offline_status": "Sin conexión no puedo confirmar el estado de hoy (cierres, alertas o vías). Esto es lo que dice la guía:",
        },
        "laya": {"enabled": False, "model": "laya_final.gather_int8.onnx", "catalog_sha256": None, "mode": "reorder_only"},
    }
    depth, continuation = depth_assets(entries)
    if continuation is not None:  # absent key = disabled: no depth files leaves today's assets untouched
        policy["continuation"] = continuation
    entry_sec = [sec_names.index(e["section"]) for e in entries]
    manifest = {
        "embedder": emb_id, "prefix": PREFIX, "dims": int(vec.shape[1]), "rows": int(vec.shape[0]),
        "text_rows": len(texts), "row_entry": owner.tolist(), "section_rows": sec_names, "entry_section": entry_sec,
        "vectors": {"file": bin_path.name, "bytes": bin_path.stat().st_size, "sha256": bin_sha, "dtype": "float32-le"},
        "scorer": {"file": scorer_path.name, "bytes": scorer_path.stat().st_size, "input": "q", "output": "sims"},
        "corpus_sha256": corpus_hash(),
    }
    w = lambda p, o: p.write_text(json.dumps(o, ensure_ascii=False, separators=(",", ":")))  # noqa: E731
    w(ASSETS / "catalog.json", catalog)
    w(ASSETS / "sections.json", sec_out)
    w(ASSETS / "policy.json", policy)
    w(ASSETS / "index.json", manifest)
    # The cue is tested by the jest detector table even while policy.continuation is off.
    w(FIXTURES / "continuation.json", {"cue": CONT_CUE, "max_words": 6, "why_cue": CONT_WHY_CUE,
                                       "bridges": CONT_BRIDGES, "texts": CONT_TEXTS})
    if depth is not None:
        w(ASSETS / "depth.json", depth)
    else:
        (ASSETS / "depth.json").unlink(missing_ok=True)

    # TS parity: entry scores (top-k mean) and their fusion with the previous fixture row's scores.
    tv = vec[: len(texts)]
    fx, prev = [], None
    for q, v in zip(probe_q, qv, strict=True):
        s = entry_scores((tv @ v).astype(np.float32), owner, len(entries), SCORE_TOPK)
        top = np.argsort(-s, kind="stable")[:K]
        row = {"q": q, "vector": [round(float(x), 7) for x in v], "pool": [entries[i]["id"] for i in top],
               "cos": [round(float(s[i]), 6) for i in top]}
        if prev is not None:
            f = fuse(s, prev, a.w)
            row["fused_top"] = entries[int(np.argmax(f))]["id"]
            row["fused_cos"] = round(float(f.max()), 6)
        fx.append(row)
        prev = s
    w(FIXTURES / "retrieval.json", {"corpus_sha256": manifest["corpus_sha256"], "vectors_sha256": bin_sha,
                                     "score_topk": SCORE_TOPK, "w": a.w, "rows": fx})
    blind = [t for r in map(json.loads, (HERE / "work/queries_raw.jsonl").read_text().splitlines()) for t in r["turns"]]
    aug = json.loads((APP / "aug_queries.json").read_text())
    probes = blind + [q for v in list(aug.values())[::7] for q in v]
    w(FIXTURES / "clean.json", [{"in": t, "out": clean(t)} for t in probes])
    print(json.dumps({"entries": len(entries), "text_rows": len(texts), "bin": str(bin_path),
                      "bytes": bin_path.stat().st_size, "emergency": len(emergency_ids)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
