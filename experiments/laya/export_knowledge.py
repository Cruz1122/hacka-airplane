"""Export the knowledge system the phone runs (docs/history/phase3-architecture.md §3).

  uv run python export_knowledge.py --embedder st                       # sentence-transformers reference
  uv run python export_knowledge.py --embedder gguf --gguf <e5.gguf>    # the vectors the phone uses

Writes GENERATED files (never edit them):
  mobile/assets/data/knowledge/{catalog,sections,policy,index}.json   bundled with the app
  <out-bin>/index.f32.bin                                            side-loaded (34 MB)
  mobile/src/core/knowledge/__fixtures__/retrieval.json              TS parity spec

Reads data/knowledge/sections (never writes it) plus data/knowledge/app/{clarification_labels,
answer_policy}.json and data/knowledge/app/calibration.jsonl (copied from the final Laya dataset).
The retrieval is the dataset contract (build_dataset.py Index.retrieve), so pools match training.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ROOT / "data/knowledge/sections"
APP_IN = ROOT / "data/knowledge/app"
ASSETS = ROOT / "mobile/assets/data/knowledge"
FIXTURES = ROOT / "mobile/src/core/knowledge/__fixtures__"
PREFIX = "query: "
K, MIN_POOL, MAX_SECTIONS, DELTA = 5, 3, 5, 0.05
MAX_OPTIONS = 1  # user decision 2026-11-22: answer with the top-1 entry only, no menu
EMERGENCY_LINE_ID = "health_safety.national_emergency_number_123"
T_GRID = np.round(np.arange(0.80, 0.951, 0.001), 3)


def norm(text: str) -> str:
    t = unicodedata.normalize("NFD", text.casefold()).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^\w\s]", " ", t).split())


def write_scorer(vec: np.ndarray, path: Path) -> None:
    """ONNX MatMul q[1,d] x W[d,rows] -> sims[1,rows]: the phone scores natively in onnxruntime
    (Hermes JS took 462 ms per query on the Moto; this is ~2 ms on the laptop)."""
    import onnx
    from onnx import TensorProto, helper, numpy_helper

    w = numpy_helper.from_array(np.ascontiguousarray(vec.T.astype(np.float32)), "W")
    g = helper.make_graph(
        [helper.make_node("MatMul", ["q", "W"], ["sims"])], "knowledge_scorer",
        [helper.make_tensor_value_info("q", TensorProto.FLOAT, [1, vec.shape[1]])],
        [helper.make_tensor_value_info("sims", TensorProto.FLOAT, [1, vec.shape[0]])], [w],
    )
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 17)])
    m.ir_version = 8
    onnx.checker.check_model(m)
    onnx.save(m, str(path))


def corpus_hash() -> str:
    h = hashlib.sha256()
    for p in sorted(SECTIONS.glob("*.json")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


# --- embedders ---------------------------------------------------------------------------------


def embed_st(texts: list[str]) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    m = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu")
    v = m.encode([PREFIX + t for t in texts], batch_size=64, normalize_embeddings=True)
    return np.asarray(v, dtype=np.float32)


def embed_gguf(texts: list[str], gguf: Path, binary: Path) -> np.ndarray:
    """llama.cpp llama-embedding: mean pooling, L2-normalised, one prompt per line."""
    if any("\n" in t for t in texts):
        raise ValueError("texts must be single-line for llama-embedding")
    out = []
    for i in range(0, len(texts), 256):
        chunk = [PREFIX + t for t in texts[i : i + 256]]
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("\n".join(chunk))
        res = subprocess.run(
            # Non-causal BERT needs every sequence of a batch inside one ubatch: size them together.
            [str(binary), "-m", str(gguf), "-f", f.name, "--pooling", "mean",
             "--embd-normalize", "2", "--embd-output-format", "json",
             "-c", "16384", "-b", "16384", "-ub", "16384"],
            capture_output=True, text=True, check=False,
        )
        Path(f.name).unlink()
        if res.returncode != 0:
            raise RuntimeError(f"llama-embedding failed: {res.stderr[-2000:]}")
        data = json.loads(res.stdout[res.stdout.index("{") :])["data"]
        out += [d["embedding"] for d in sorted(data, key=lambda d: d["index"])]
    v = np.asarray(out, dtype=np.float32)
    if v.shape[0] != len(texts):
        raise RuntimeError(f"expected {len(texts)} vectors, got {v.shape[0]}")
    return v


# --- index and retrieval (port of build_dataset.py Index) -------------------------------------


class Index:
    def __init__(self) -> None:
        self.sections: dict[str, dict] = {}
        self.entries: list[dict] = []
        for p in sorted(SECTIONS.glob("*.json")):
            s = json.loads(p.read_text())
            self.sections[s.get("id", p.stem)] = s
            for e in s["entries"]:
                if e.get("audience", "visitor") == "visitor":
                    self.entries.append({**e, "section": s.get("id", p.stem)})
        self.ids = [e["id"] for e in self.entries]
        texts, owner = [], []
        for n, e in enumerate(self.entries):
            for t in [e["label"], *e.get("examples", [])]:
                texts.append(t)
                owner.append(n)
        self.texts, self.owner = texts, np.asarray(owner)
        self.sec_names = list(self.sections)
        self.text_sec = np.asarray([self.sec_names.index(self.entries[o]["section"]) for o in owner])
        self.entry_sec = np.asarray([self.sec_names.index(e["section"]) for e in self.entries])
        self.top_k = [int(self.sections[s].get("retrieval", {}).get("top_k", 2)) for s in self.sec_names]
        self.norm_text = [norm(x) for x in texts]
        self.desc = [self.sections[s].get("description", "") for s in self.sec_names]

    def set_vectors(self, vec: np.ndarray) -> None:
        self.tv, self.dv = vec[: len(self.texts)], vec[len(self.texts) :]

    def retrieve(self, q: np.ndarray, mask: list[int] | None = None) -> dict:
        sims = self.tv @ q
        if mask:
            sims[mask] = -1.0
        scores = np.full(len(self.entries), -1.0, dtype=np.float32)
        np.maximum.at(scores, self.owner, sims)
        sec = self.dv @ q
        np.maximum.at(sec, self.text_sec, sims)
        order = sorted(range(len(self.sec_names)), key=lambda s: (-sec[s], self.sec_names[s]))
        gates = [s for s in order if sec[s] >= sec[order[0]] - DELTA][:MAX_SECTIONS]
        pool: list[int] = []
        for s in gates:
            members = [n for n in np.flatnonzero(self.entry_sec == s) if scores[n] > -1.0]
            pool += sorted(members, key=lambda n: (-scores[n], self.ids[n]))[: self.top_k[s]]
        pool = sorted(pool, key=lambda n: (-scores[n], self.ids[n]))[:K]
        if len(pool) < MIN_POOL:
            seen = set(pool)
            for n in np.argsort(-scores, kind="stable"):
                if len(pool) >= MIN_POOL:
                    break
                if int(n) not in seen and scores[n] > -1.0:
                    pool.append(int(n))
                    seen.add(int(n))
            pool = sorted(pool, key=lambda n: (-scores[n], self.ids[n]))
        return {
            "pool": [self.ids[n] for n in pool],
            "cos": [float(scores[n]) for n in pool],
            "gates": [self.sec_names[s] for s in gates],
        }

    def mask_for(self, query: str) -> list[int]:
        """Index texts identical to the query after normalisation (fit/eval only, never on device)."""
        q = norm(query)
        return [i for i, t in enumerate(self.norm_text) if t == q]


# --- threshold fit ---------------------------------------------------------------------------


def menu_success(rows: list[dict], T: float) -> int:
    ok = 0
    for r in rows:
        acc = set(r["acceptable"])
        shown = r["cos"][0] >= T
        if acc:
            ok += shown and bool(acc & set(r["pool"][:MAX_OPTIONS]))
        else:
            ok += not shown
    return ok


def fit_threshold(rows: list[dict]) -> dict:
    curve = [(float(t), menu_success(rows, float(t))) for t in T_GRID]
    best = max(s for _, s in curve)
    # Plateau centre: every T within 2 rows of the best, then its median (argmax alone is noise).
    plateau = [t for t, s in curve if s >= best - 2]
    t = float(np.median(plateau))
    return {"T": round(t, 3), "best_success": best, "n": len(rows),
            "plateau": [min(plateau), max(plateau)], "success_at_T": menu_success(rows, t)}


# --- export ----------------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--embedder", choices=["st", "gguf"], required=True)
    ap.add_argument("--gguf", type=Path)
    ap.add_argument("--llama-embedding", type=Path,
                    default=Path.home() / ".cache/llama.cpp-src/src/build/bin/llama-embedding")
    ap.add_argument("--out-bin", type=Path, default=ROOT / "models/knowledge")
    ap.add_argument("--fixture-rows", type=int, default=120)
    a = ap.parse_args()

    ix = Index()
    labels = json.loads((APP_IN / "clarification_labels.json").read_text())
    apol = json.loads((APP_IN / "answer_policy.json").read_text())
    emergency_ids = sorted(k for k, v in apol.items() if v.get("policy") == "emergency_direct")
    calib = [json.loads(x) for x in (APP_IN / "calibration.jsonl").read_text().splitlines() if x]

    texts = ix.texts + ix.desc
    queries = [r["state"] for r in calib]
    if a.embedder == "st":
        allv = embed_st(texts + queries)
        emb_id = {"kind": "sentence-transformers", "model": "intfloat/multilingual-e5-base"}
    else:
        if not a.gguf:
            raise SystemExit("--gguf is required with --embedder gguf")
        allv = embed_gguf(texts + queries, a.gguf, a.llama_embedding)
        emb_id = {"kind": "gguf", "file": a.gguf.name, "bytes": a.gguf.stat().st_size,
                  "sha256": hashlib.sha256(a.gguf.read_bytes()).hexdigest()}
    vec, qv = allv[: len(texts)], allv[len(texts) :]
    ix.set_vectors(vec)

    fit_rows = []
    for r, v in zip(calib, qv, strict=True):
        res = ix.retrieve(v, ix.mask_for(r["state"]))
        fit_rows.append({**res, "acceptable": r["meta"].get("acceptable_ids") or []})
    fit = fit_threshold(fit_rows)

    chash = corpus_hash()
    a.out_bin.mkdir(parents=True, exist_ok=True)
    bin_path = a.out_bin / "index.f32.bin"
    vec.astype("<f4").tofile(bin_path)
    bin_sha = hashlib.sha256(bin_path.read_bytes()).hexdigest()
    scorer_path = a.out_bin / "index_scorer.onnx"
    write_scorer(vec, scorer_path)

    ASSETS.mkdir(parents=True, exist_ok=True)
    emer = set(emergency_ids)
    catalog = []
    for e in ix.entries:
        kind = "action" if e["kind"] == "action" else "emergency" if e["id"] in emer else "faq"
        ans = e.get("answer", {})
        catalog.append({
            "id": e["id"], "section": e["section"], "kind": kind, "label": e["label"],
            "menu_label": labels.get(e["id"], e["label"]), "short": ans.get("short", ""),
            "steps": ans.get("steps") or [], "sources": e.get("sources", []),
            "last_verified": e.get("last_verified"),
        })
    sections = [{
        "id": s, "order": ix.sections[s].get("order"), "title": ix.sections[s].get("title"),
        "top_k": ix.top_k[i], "featured": ix.sections[s].get("featured", []),
    } for i, s in enumerate(ix.sec_names)]
    featured = [f for s in sorted(sections, key=lambda s: s["order"]) for f in s["featured"][:1]][:3]
    policy = {
        "version": "e5-top1-v1", "T": fit["T"], "fit": fit, "fitted_on": "data/knowledge/app/calibration.jsonl",
        "k": K, "min_pool": MIN_POOL, "max_sections": MAX_SECTIONS, "delta": DELTA,
        "max_options": MAX_OPTIONS, "emergency_direct": emergency_ids,
        "emergency_line_id": EMERGENCY_LINE_ID, "abstain_featured": featured,
        "texts": {
            "menu_prompt": "¿Es alguno de estos temas?", "none_label": "Ninguna de estas",
            "abstain": "No encontré ese tema en la guía del parque. ¿Puedes decirlo con otras palabras?",
            "offline_status": "Sin conexión no puedo confirmar el estado de hoy (cierres, alertas o vías). Esto es lo que dice la guía:",
        },
        "laya": {"enabled": False, "model": "laya_final.gather_int8.onnx",
                 "catalog_sha256": None, "mode": "reorder_only"},
    }
    manifest = {
        "embedder": emb_id, "prefix": PREFIX, "dims": int(vec.shape[1]), "rows": int(vec.shape[0]),
        "text_rows": len(ix.texts), "row_entry": ix.owner.tolist(),
        "section_rows": ix.sec_names, "entry_section": ix.entry_sec.tolist(),
        "vectors": {"file": bin_path.name, "bytes": bin_path.stat().st_size, "sha256": bin_sha,
                    "dtype": "float32-le"},
        "scorer": {"file": scorer_path.name, "bytes": scorer_path.stat().st_size,
                   "input": "q", "output": "sims"},
        "corpus_sha256": chash,
    }
    w = lambda p, o: p.write_text(json.dumps(o, ensure_ascii=False, separators=(",", ":")))  # noqa: E731
    w(ASSETS / "catalog.json", catalog)
    w(ASSETS / "sections.json", sections)
    w(ASSETS / "policy.json", policy)
    w(ASSETS / "index.json", manifest)

    # TS parity spec: unmasked retrieval of calibration queries with these exact vectors.
    FIXTURES.mkdir(parents=True, exist_ok=True)
    fx = []
    for r, v in list(zip(calib, qv, strict=True))[: a.fixture_rows]:
        res = ix.retrieve(v)
        fx.append({"q": r["state"], "vector": [round(float(x), 7) for x in v],
                   "pool": res["pool"], "cos": [round(c, 6) for c in res["cos"]], "gates": res["gates"]})
    w(FIXTURES / "retrieval.json", {"corpus_sha256": chash, "vectors_sha256": bin_sha, "rows": fx})
    np.save(a.out_bin / f"calib_queries.{a.embedder}.npy", qv)
    print(json.dumps({"embedder": emb_id, "rows": vec.shape[0], "fit": fit, "corpus": chash[:12],
                      "bin": str(bin_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
