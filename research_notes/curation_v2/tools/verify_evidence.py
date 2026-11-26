"""Check that every evidence record of a proposal points at really fetched bytes.

    python3 research_notes/curation_v2/tools/verify_evidence.py --proposal P.json [--refetch]

FAIL (exit 1):
  - evidence file missing, or outside the repository;
  - a new evidence file without fetch_evidence.py provenance, or whose .txt no longer equals the
    text extracted from its raw bytes (hand-edited), or whose URL differs from the record URL;
  - a pre-existing (Phase 2) evidence file absent from, or changed since, the legacy manifest
    snapshot taken before curation v2 started (raw evidence is gitignored, so git cannot vouch);
  - quote not literally present in the evidence text (what knowledge.py also requires).
FLAG (exit 0, reviewers must look): a number in a new/changed answer that appears in none of the
op's evidence texts. WARN: --refetch could not find the quote in a fresh download (dynamic page).
Literal presence is not entailment: reviewers still judge whether the passage supports the claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_evidence import extract_text, fetch  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
NEW_EVIDENCE = ROOT / "research_notes/curation_v2/evidence"
SECTIONS = ROOT / "data/knowledge/sections"
NUM = re.compile(r"\d+(?:[.,:]\d+)*")


def norm_ws(s: str) -> str:
    return " ".join(s.split())


def digits_text(s: str) -> str:
    return re.sub(r"(?<=\d)[.,  ](?=\d{3}\b)", "", s)


def strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)


def numbers(answer) -> set[str]:
    return {digits_text(m) for s in strings(answer) for m in NUM.findall(s)}


LEGACY = ROOT / "research_notes/curation_v2/snapshots/legacy_evidence_manifest.json"
_legacy: dict[str, str] | None = None


def legacy_ok(path: Path) -> bool:
    global _legacy
    if _legacy is None:
        _legacy = json.loads(LEGACY.read_text())["files"]
    rel = str(path.relative_to(ROOT))
    return _legacy.get(rel) == hashlib.sha256(path.read_bytes()).hexdigest()


def check_file(item: dict, fail: list, eid: str) -> str | None:
    p = (ROOT / item["path"]).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():
        fail.append(f"{eid}: evidence file missing or outside repo: {item['path']}")
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    if p.is_relative_to(NEW_EVIDENCE):
        meta_p = p.with_suffix(".meta.json")
        if not meta_p.is_file():
            fail.append(f"{eid}: {item['path']} has no fetch_evidence.py provenance")
            return text
        meta = json.loads(meta_p.read_text())
        raw = (p.parent / meta["raw_file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != meta["sha256_raw"]:
            fail.append(f"{eid}: raw bytes changed after fetch: {meta['raw_file']}")
        if extract_text(raw, meta["content_type"]) != text:
            fail.append(f"{eid}: {item['path']} differs from text extracted from its raw bytes")
        if item["url"] not in (meta["url"], meta["final_url"]):
            fail.append(f"{eid}: evidence URL {item['url']} != fetched URL {meta['url']}")
    elif not legacy_ok(p):
        fail.append(f"{eid}: {item['path']} is neither fetched by fetch_evidence.py nor in the "
                    "legacy evidence manifest (or changed since)")
    if item["quote"] not in text:
        fail.append(f"{eid}: quote not literally in {item['path']}: {item['quote'][:80]!r}")
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposal", required=True)
    ap.add_argument("--refetch", action="store_true")
    a = ap.parse_args()
    prop = json.loads(Path(a.proposal).read_text())
    ops = prop if isinstance(prop, list) else prop.get("operations", prop.get("entries", [prop]))
    current = {e["id"]: e for f in SECTIONS.glob("*.json")
               for e in json.loads(f.read_text())["entries"]}
    fail, flags, warn, n_items = [], [], [], 0
    for rec in ops:
        eid = rec.get("id") or rec["entry"]["id"]
        texts = []
        for item in rec.get("evidence", []):
            n_items += 1
            t = check_file(item, fail, eid)
            if t is not None:
                texts.append(digits_text(t))
            if a.refetch:
                try:
                    raw, info = fetch(item["url"])
                    fresh = extract_text(raw, info["content_type"])
                    if norm_ws(item["quote"]) not in norm_ws(fresh):
                        warn.append(f"{eid}: quote not found in fresh download of {item['url']}")
                except SystemExit as e:
                    warn.append(f"{eid}: refetch failed {item['url']}: {e}")
        if rec.get("op", "add") in ("add", "update") and "entry" in rec:
            before = current.get(eid, {}).get("answer")
            new_nums = numbers(rec["entry"]["answer"]) - (numbers(before) if before else set())
            blob = "\n".join(texts)
            for n in sorted(new_nums):
                if not re.search(rf"(?<!\d){re.escape(n)}(?!\d)", blob):
                    flags.append(f"{eid}: number {n!r} in answer not found in its evidence")
    print(json.dumps({"proposal": a.proposal, "ops": len(ops), "evidence_items": n_items,
                      "fail": fail, "flags": flags, "warn": warn}, indent=1, ensure_ascii=False))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
