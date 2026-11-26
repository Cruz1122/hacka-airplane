"""Knowledge base loading, text normalisation and cached embeddings for the NLU experiments.

Reads data/knowledge/sections/*.json directly (read-only). Embeddings are cached per model and
text, so trying a scoring idea never re-embeds the corpus.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ROOT / "data/knowledge/sections"
CACHE = ROOT / "experiments/nlu/work/emb_cache"


@dataclass
class Entry:
    id: str
    section: str
    label: str
    kind: str
    examples: list[str]
    hard_negatives: list[str]
    short: str
    variants: list[str] = field(default_factory=list)


APP = ROOT / "data/knowledge/app"


def load_hubs(path: Path | None = None) -> list[Entry]:
    """App-layer hub answers (composites of existing curated facts), as entries."""
    path = path or APP / "hubs.json"
    if not path.exists():
        return []
    return [Entry(h["id"], "hub", h["label"], "hub", list(h["examples"]), [], h["reply"])
            for h in json.loads(path.read_text())]


def app_texts(conv: bool = True, variants: bool = True, train_convs: bool = True) -> dict[str, list[str]]:
    """Extra index/training texts per entry id.

    aug_queries.json and followup_convs.json are the original pools and are not rewritten.
    train_variants.json and train_convs.json, when present, add the depth_v1 rows. A conversation
    turn is indexed under the entry that answers that turn, not under the conversation target:
    export_nlu embeds one row per text, and follow-up fusion happens at query time.
    variants=False leaves train_variants.json out (ft5 regressed with it in the training pool).
    train_convs=False leaves train_convs.json out (ft4 ships without the depth_v1 rows).
    """
    out: dict[str, list[str]] = {}
    aug = APP / "aug_queries.json"
    if aug.exists():
        for k, v in json.loads(aug.read_text()).items():
            out.setdefault(k, []).extend(v)
    convs = APP / "followup_convs.json"
    if conv and convs.exists():
        for k, v in json.loads(convs.read_text()).items():
            out.setdefault(k, []).extend(" ".join(c) for c in v)
    var_path = APP / "train_variants.json"
    if variants and var_path.exists():
        for k, v in json.loads(var_path.read_text()).items():
            out.setdefault(k, []).extend(v)
    trained = APP / "train_convs.json"
    if conv and train_convs and trained.exists():
        for groups in json.loads(trained.read_text()).values():
            for turns in groups:
                for turn in turns:
                    out.setdefault(turn["entry_id"], []).append(turn["text"])
    return out


def load_entries(hubs: bool = False) -> list[Entry]:
    out = load_hubs() if hubs else []
    for f in sorted(SECTIONS.glob("*.json")):
        d = json.loads(f.read_text())
        for e in d["entries"]:
            a = e["answer"]
            out.append(Entry(e["id"], d["id"], e["label"], e.get("kind", ""), list(e.get("examples", [])),
                             list(e.get("hard_negatives", [])), a["short"], list(a.get("variants", []))))
    return out


def fold(text: str) -> str:
    """Lowercase, strip accents and punctuation: the lexical channel's view of a text."""
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9ñ ]+", " ", t).strip()


# Colombian chat fillers that open or close a message ("ey parce, ...", "..., pues"). They carry no
# topic but dominate the embedding of a short message, pulling it toward any text with the same
# opener. Stripped from queries and index texts alike; a message that is only fillers is kept as is.
_F = (r"ey|ei|hey|oye|oiga|oigan|oe|ve|vea|uy|ay|ah|epa|hola|holi|buenas|buenos d[ií]as|buenas tardes|"
      r"buenas noches|parce|parcero|parcera|mano|manito|hermano|bro|mijo|mija|socio|amigo|amiga|"
      r"qu[eé] m[aá]s|quiubo|qu[eé] hubo|vos sab[eé]s|sab[eé]s|pues|porfa|por favor|una pregunta|"
      r"pregunta|disculpe|disculpa|me da pena pero|ome|che|y")
_LEAD = re.compile(rf"^(?:\s*[¿¡,.!?;:-]*\s*(?:{_F})\b[\s,.!?;:-]*)+", re.I)
_TRAIL = re.compile(r"[\s,]+(?:pues|parce|mano|porfa|o qu[eé]|bro)[\s?!.]*$", re.I)


def clean(text: str) -> str:
    t = _TRAIL.sub("", _LEAD.sub("", text)).strip()
    return t if len(t) >= 3 else text


class Embedder:
    def __init__(self, name: str, prefix: str = "query: ", device: str = "cpu", max_len: int = 128,
                 strip_fillers: bool = False):
        from sentence_transformers import SentenceTransformer

        self.name, self.prefix, self.strip = name, prefix, strip_fillers
        self.model = SentenceTransformer(name, device=device)
        self.model.max_seq_length = max_len
        tag = name
        weights = Path(name) / "model.safetensors"
        if weights.exists():  # a local fine-tune: retraining at the same path must not reuse old vectors
            tag = f"{name}@{int(weights.stat().st_mtime)}"
        self.dir = CACHE / re.sub(r"[^A-Za-z0-9_.-]+", "_", tag)
        self.dir.mkdir(parents=True, exist_ok=True)

    def encode(self, texts: list[str], batch: int = 64) -> np.ndarray:
        if self.strip:
            texts = [clean(t) for t in texts]
        key = hashlib.sha256(("\x00".join(texts) + self.prefix).encode()).hexdigest()[:20]
        path = self.dir / f"{key}.npy"
        if path.exists():
            return np.load(path)
        v = self.model.encode([self.prefix + t for t in texts], batch_size=batch,
                              normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True)
        v = v.astype(np.float32)
        np.save(path, v)
        return v
