"""Recompute SHA-256 and size of every file listed in MANIFEST.json.

    python scripts/verify_manifest.py
"""
from __future__ import annotations

import hashlib
import json

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# `python -I` (used for the clean-copy checks) does not put the script dir on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PKG, Report  # noqa: E402


def main() -> None:
    rep = Report("verify_manifest")
    man = json.loads((PKG / "MANIFEST.json").read_text(encoding="utf-8"))
    listed = set()
    for rel, info in man["files"].items():
        p = PKG / rel
        listed.add(rel)
        if not p.is_file():
            rep.check(False, f"missing {rel}"); continue
        b = p.read_bytes()
        rep.check(hashlib.sha256(b).hexdigest() == info["sha256"], f"sha256 mismatch {rel}")
        rep.check(len(b) == info["bytes"], f"size mismatch {rel}")
    extra = sorted(str(p.relative_to(PKG)) for p in PKG.rglob("*") if p.is_file()
                   and str(p.relative_to(PKG)) not in listed and p.name != "MANIFEST.json" and "__pycache__" not in p.parts)
    rep.check(not extra, f"files not in manifest: {extra[:10]}")
    rep.notes.append(f"{len(listed)} files checked")
    rep.done()


if __name__ == "__main__":
    main()
