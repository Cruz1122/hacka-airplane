"""Audit source quality per section (coordinator gate; read-only).

Reports homepage-only URLs, whether evidence folders hold raw downloads, evidence
timestamp clustering, and answer tokens (numbers, legal citations) that never
appear in the section's evidence files.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parents[1]
SECTIONS = ROOT / "data/knowledge/sections"
RAW_EXT = {".html", ".htm", ".pdf", ".docx", ".xml", ".json"}
LEGAL = re.compile(r"(?:Resoluci[oó]n|Ley|Decreto|Sentencia)\s+(?:No\.?\s*)?([0-9][0-9.]*)", re.I)
NUMBER = re.compile(r"\d[\d.,]*")


def fold(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    return "".join(c for c in text if not unicodedata.combining(c))


def evidence_text(folder):
    chunks = []
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".txt", ".md", ".html", ".htm", ".json", ".xml"}:
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                pass
    return fold("\n".join(chunks))


def tokens(answer):
    found = set()
    for match in LEGAL.finditer(answer):
        found.add(match.group(1).rstrip("."))
    for match in NUMBER.finditer(answer):
        token = match.group(0).rstrip(".,")
        if len(token.replace(".", "").replace(",", "")) >= 2:
            found.add(token)
    return found


def audit(section_file):
    sid = section_file.stem
    data = json.loads(section_file.read_text(encoding="utf-8"))
    folder = NOTES / sid
    files = [p for p in folder.rglob("*") if p.is_file()] if folder.exists() else []
    evidence = [p for p in files if "evidence" in p.parts]
    raw = [p for p in evidence if p.suffix.lower() in RAW_EXT]
    times = sorted(p.stat().st_mtime for p in evidence if p.suffix.lower() in {".txt", ".md"})
    spread = (times[-1] - times[0]) if len(times) > 1 else None
    corpus = evidence_text(folder) if folder.exists() else ""
    homepage, missing = [], []
    for entry in data["entries"]:
        for source in entry.get("sources", []):
            path = urlparse(source.get("url", "")).path
            if path in ("", "/"):
                homepage.append((entry["id"], source["url"]))
        short = entry["answer"].get("short", "")
        absent = sorted(t for t in tokens(short) if fold(t) not in corpus)
        if absent:
            missing.append((entry["id"], absent))
    return {
        "section": sid,
        "entries": len(data["entries"]),
        "evidence_files": len(evidence),
        "raw_files": len(raw),
        "prose_mtime_spread_s": round(spread) if spread is not None else None,
        "homepage_sources": homepage,
        "answer_tokens_not_in_evidence": missing,
    }


def main():
    report = [audit(f) for f in sorted(SECTIONS.glob("*.json"))]
    for row in report:
        print(
            f"{row['section']:17} entries={row['entries']:3} evidence={row['evidence_files']:3} "
            f"raw={row['raw_files']:3} spread_s={row['prose_mtime_spread_s']} "
            f"homepage={len(row['homepage_sources']):3} missing_tokens={len(row['answer_tokens_not_in_evidence']):3}"
        )
    out = HERE / "source_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"details: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
