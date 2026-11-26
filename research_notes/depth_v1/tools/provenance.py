"""Classify every evidence .txt as a real capture or an agent-written summary.

capture  = a same-stem .pdf/.html sibling exists, or >=50 % of its sampled sentences appear verbatim
           (folded, whitespace-normalised) in the section's raw html/pdf/xml/json captures.
summary  = otherwise. Summaries are never evidence (T0 frailejón finding).

usage: python3 provenance.py  -> inputs/evidence_provenance.json
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

from common import DEPTH, RESEARCH, SECTION_ORDER, fold

BANNED = ("no-citar", "unverified-notes", "_quotes", "urls-read")
RAW_EXT = {".html", ".htm", ".pdf", ".xml", ".json"}
CACHE = DEPTH / "inputs/raw_text_cache"


def norm(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", fold(t)))


def raw_text(p: Path) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / (str(p.relative_to(RESEARCH)).replace("/", "__") + ".n")
    if c.exists():
        return c.read_text()
    if p.suffix == ".pdf":
        r = subprocess.run(["pdftotext", "-q", str(p), "-"], capture_output=True, text=True, check=False)
        t = r.stdout
    else:
        t = p.read_text(errors="replace")
        if p.suffix in {".html", ".htm", ".xml"}:
            t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
            t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = norm(t)
    c.write_text(t)
    return t


def sentences(t: str) -> list[str]:
    out = [s for s in re.split(r"(?<=[.!?])\s+|\n", t) if len(s) >= 60]
    step = max(1, len(out) // 25)
    return out[::step][:25]


def main() -> None:
    res = {}
    blob_all = None
    for sec in SECTION_ORDER:
        base = RESEARCH / sec / "evidence"
        if not base.is_dir():
            continue
        raws = [p for p in base.rglob("*") if p.is_file() and p.suffix in RAW_EXT]
        blob = None
        for p in sorted(base.rglob("*.txt")):
            rel = str(p.relative_to(RESEARCH))
            low = rel.lower()
            if any(k in low for k in BANNED):
                res[rel] = {"class": "summary", "why": "explicitly unverified / quote digest / url list"}
                continue
            sib = any(p.with_suffix(x).exists() for x in RAW_EXT) or p.with_suffix("").exists()
            if sib or "/raw/" in rel:
                res[rel] = {"class": "capture", "why": "same-stem raw sibling"}
                continue
            if blob is None:
                blob = "\n".join(raw_text(r) for r in raws)
            ss = sentences(p.read_text(errors="replace"))
            if blob_all is None:
                blob_all = "\n".join(raw_text(r) for r in RESEARCH.rglob("*") if r.is_file() and r.suffix in RAW_EXT and "coordination" not in r.parts)
            hit = sum(1 for s in ss if norm(s)[:120] and norm(s)[:120] in blob_all)
            frac = hit / len(ss) if ss else 0.0
            res[rel] = {"class": "capture" if frac >= 0.5 else "summary", "why": f"{hit}/{len(ss)} sentences in raw"}
    (DEPTH / "inputs/evidence_provenance.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    from collections import Counter
    print(Counter(v["class"] for v in res.values()))
    for sec in SECTION_ORDER:
        c = Counter(v["class"] for k, v in res.items() if k.startswith(sec + "/"))
        print(f"  {sec:18s} {dict(c)}")


if __name__ == "__main__":
    main()
