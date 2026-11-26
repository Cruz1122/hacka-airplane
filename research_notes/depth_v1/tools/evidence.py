"""Evidence windows: section evidence files chunked into passages, ranked per entry by idf-weighted
overlap. A window id (qid) is "<file rel path>#<char start>"; check_depth verifies quotes against it."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from common import DEPTH, RESEARCH, content_words, entries, entry_facts_text

CHUNK = 900  # chars per window
# Only captured page/pdf text. Agent-written notes (*.md, research logs, quote digests) are not
# evidence: the flora correction receipt removed "facts" that existed only in such notes.
EXTS = {".txt"}


@lru_cache(maxsize=1)
def captures() -> set[str]:
    """inputs/evidence_provenance.json (provenance.py): only real captures are evidence."""
    prov = json.loads((DEPTH / "inputs/evidence_provenance.json").read_text())
    return {k for k, v in prov.items() if v["class"] == "capture"}


def section_files(section: str) -> list[Path]:
    base = RESEARCH / section / "evidence"
    files = sorted(p for p in base.rglob("*") if p.is_file() and p.suffix in EXTS) if base.is_dir() else []
    return [p for p in files if str(p.relative_to(RESEARCH)) in captures()]


def chunk(text: str) -> list[tuple[int, str]]:
    out, start, buf = [], 0, ""
    pos = 0
    for para in re.split(r"(\n\s*\n)", text):
        if not buf:
            start = pos
        if len(buf) + len(para) > CHUNK and buf.strip():
            out.append((start, buf))
            buf, start = "", pos
        buf += para
        pos += len(para)
        while len(buf) > CHUNK * 2:  # very long paragraph (pdf text): hard split on a sentence end
            cut = buf.rfind(". ", 0, CHUNK) + 1 or CHUNK
            out.append((start, buf[:cut]))
            buf, start = buf[cut:], start + cut
    if buf.strip():
        out.append((start, buf))
    return out


@lru_cache(maxsize=None)
def section_index(section: str):
    chunks = []
    for p in section_files(section):
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        rel = str(p.relative_to(RESEARCH))
        for s, t in chunk(text):
            cw = content_words(t)
            if len(cw) >= 5:
                chunks.append((f"{rel}#{s}", t, cw))
    df = Counter(w for _, _, cw in chunks for w in cw)
    n = max(len(chunks), 1)
    idf = {w: math.log(n / c) for w, c in df.items()}
    return chunks, idf


def ranked_windows(entry_id: str, k: int = 8) -> list[dict]:
    e = entries()[entry_id]
    chunks, idf = section_index(e["section"])
    q = content_words(e["label"] + " " + entry_facts_text(e))
    scored = []
    for qid, text, cw in chunks:
        inter = q & cw
        if len(inter) < 3:
            continue
        s = sum(idf.get(w, 0) for w in inter) / math.sqrt(len(cw))
        scored.append((s, qid, text, inter))
    scored.sort(reverse=True)
    return [{"qid": qid, "score": round(s, 3), "text": " ".join(text.split())} for s, qid, text, _ in scored[:k]]
