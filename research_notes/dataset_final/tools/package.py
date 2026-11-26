"""Finish the package: copy scripts/docs, write MANIFEST.json, zip, extract to a clean dir, re-validate.

    python3 research_notes/dataset_final/tools/package.py
"""
from __future__ import annotations

import getpass
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

W = Path(__file__).resolve().parents[1]
PKG = "LOS_NEVADOS_LAYA_FINAL_DATASET"
OUT = W / "out" / PKG
SRC = W / "package_src"
ZIP = W / "out" / f"{PKG}.zip"
CHECKS = [["scripts/verify_manifest.py"], ["scripts/validate_dataset.py"], ["scripts/validate_splits.py"],
          ["scripts/check_leakage.py"]]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_checks(root: Path) -> dict:
    res = {}
    for c in CHECKS:
        r = subprocess.run([sys.executable, "-I", *c], cwd=root, capture_output=True, text=True)
        res[c[0]] = {"returncode": r.returncode, "tail": (r.stdout + r.stderr).strip().splitlines()[-12:]}
    return res


def main() -> None:
    for rel in ("scripts", "reports"):
        if (SRC / rel).exists():
            shutil.rmtree(OUT / rel, ignore_errors=True)
            shutil.copytree(SRC / rel, OUT / rel, ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("README.md", "requirements.txt"):
        shutil.copy(SRC / name, OUT / name)
    shutil.copy(W / "decisions/orchestrator.md", OUT / "reports/DECISION_LOG.md")
    shutil.rmtree(OUT / "scripts/build", ignore_errors=True)
    (OUT / "scripts/build").mkdir(parents=True)
    for f in ("build_dataset.py", "build_splits.py", "digest.py", "verify_digest.py", "finalize_knowledge.py",
              "combine_approved.py", "stats.py", "package.py"):
        shutil.copy(W / "tools" / f, OUT / "scripts/build" / f)
    # Refuse to ship unfinished docs or local/private identifiers.
    banned = ("PLACE" + "HOLDER", str(Path.home()), getpass.getuser())
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".py", ".json", ".jsonl", ".txt"):
            text = p.read_text(encoding="utf-8")
            hits = [b for b in banned if b.lower() in text.lower()]
            if hits:
                sys.exit(f"package.py: {p.relative_to(OUT)} contains {hits}")
    files = {}
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json" and "__pycache__" not in p.parts:
            rel = str(p.relative_to(OUT))
            n = sum(1 for _ in p.open(encoding="utf-8")) if p.suffix == ".jsonl" else None
            files[rel] = {"sha256": sha(p), "bytes": p.stat().st_size, **({"rows": n} if n is not None else {})}
    split = json.loads((OUT / "audit/split_manifest.json").read_text())
    manifest = {"package": PKG, "format": "laya==0.5.1 choice rows (state, questions.topic, expected.topic, meta.pool, meta.gold)",
                "counts": split["counts"], "unseen_topic_ids": len(split["unseen_topic_ids"]), "files": files}
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    in_place = run_checks(OUT)
    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, f"{PKG}/{p.relative_to(OUT)}")
    with zipfile.ZipFile(ZIP) as z:
        bad = z.testzip()
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(tmp)
        extracted = run_checks(Path(tmp) / PKG)
    report = {"zip": str(ZIP), "bytes": ZIP.stat().st_size, "sha256": sha(ZIP), "testzip_first_bad": bad,
              "checks_in_place": in_place, "checks_extracted": extracted}
    (W / "out/package_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: report[k] for k in ("zip", "bytes", "sha256", "testzip_first_bad")}
                     | {"extracted": {k: v["returncode"] for k, v in extracted.items()}}, indent=1))


if __name__ == "__main__":
    main()
