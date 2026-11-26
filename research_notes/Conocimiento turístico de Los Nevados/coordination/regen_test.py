"""Regeneration test (coordinator only; restores corpus and polish/ when done).

Modes:
  full     delete every section, run each canonical builder, run coordinator_fixes once,
           compare all 15 sections against the delivered corpus and polish/ against its backup.
  base     record each builder's raw short/variants in coordination/polish_base.json.
  scratch  for each section alone: delete S.json, run its builder, run coordinator_fixes,
           compare S.json (the path a research agent takes).

Usage: python3 regen_test.py full|scratch [section ...]
Never run while research agents are active: it holds the coordinator lock and swaps the corpus.
"""

import fcntl
import json
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parents[1]
SECTIONS = ROOT / "data/knowledge/sections"
POLISH = HERE / "polish"
STATE_FILES = [HERE / "merged_examples.json"]
OUT = Path(tempfile.gettempdir()) / "regen_out"

sys.path.insert(0, str(HERE))
import builders  # noqa: E402  (canonical builder per section)
import coordinator_fixes  # noqa: E402


def canon(path):
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True, ensure_ascii=False)


def run(command):
    script, *args = command.split(" ")
    target = NOTES / script
    proc = subprocess.run([sys.executable, str(target), *args], cwd=target.parent, capture_output=True, text=True, timeout=600)
    return proc.returncode, (proc.stdout + proc.stderr)[-400:]


def diff_summary(a, b):
    da, db = json.loads(a), json.loads(b)
    ea = {e["id"]: e for e in da["entries"]}
    eb = {e["id"]: e for e in db["entries"]}
    changed = [i for i in ea if i in eb and ea[i] != eb[i]]
    fields = sorted({k for i in changed for k in set(ea[i]) | set(eb[i]) if ea[i].get(k) != eb[i].get(k)})
    return {"only_delivered": sorted(set(ea) - set(eb)), "only_regenerated": sorted(set(eb) - set(ea)),
            "changed": changed[:8], "changed_count": len(changed), "fields": fields,
            "section_keys": sorted(k for k in set(da) | set(db) if k != "entries" and da.get(k) != db.get(k))}


def build(sid):
    logs = [run(script) for script in builders.BUILDERS[sid]]
    return [log for log in logs if log[0]]


def compare(sid, backup):
    delivered = canon(backup / "sections" / f"{sid}.json")
    path = SECTIONS / f"{sid}.json"
    if not path.exists():
        return {"status": "MISSING"}
    OUT.mkdir(exist_ok=True)
    shutil.copy(path, OUT / f"{sid}.json")
    if canon(path) == delivered:
        return {"status": "OK"}
    return {"status": "DIFF", "diff": diff_summary(delivered, canon(path))}


def restore(backup):
    for src, dst in ((backup / "sections", SECTIONS), (backup / "polish", POLISH)):
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
    for f in STATE_FILES:
        saved = backup / f.name
        if saved.exists():
            shutil.copy(saved, f)
        elif f.exists():
            f.unlink()


def main():
    mode, wanted = sys.argv[1], sys.argv[2:] or list(builders.BUILDERS)
    if mode not in ("full", "scratch", "base"):
        sys.exit("mode must be full, scratch or base")
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(1))  # let `timeout` reach the restore
    backup = Path(tempfile.mkdtemp(prefix="regen-backup-"))
    shutil.copytree(SECTIONS, backup / "sections")
    shutil.copytree(POLISH, backup / "polish")
    for f in STATE_FILES:
        if f.exists():
            shutil.copy(f, backup / f.name)
    report = {}
    lock = open(HERE / "coordinator_fixes.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    try:
        if mode == "full":
            for f in SECTIONS.glob("*.json"):
                f.unlink()
            errors = {sid: build(sid) for sid in builders.BUILDERS}
            # health_safety and weather_volcano check their hard negatives against the other
            # sections' files, which do not exist yet on the first pass: retry once after the rest.
            for sid in [s for s in builders.BUILDERS if not (SECTIONS / f"{s}.json").exists()]:
                errors[sid] = build(sid)
            missing = [sid for sid in builders.BUILDERS if not (SECTIONS / f"{sid}.json").exists()]
            if missing:
                report["_builder_failures"] = {sid: errors[sid] for sid in missing}
                raise RuntimeError(f"builders did not produce: {missing}")
            coordinator_fixes.main()
            for sid in builders.BUILDERS:
                report[sid] = {**compare(sid, backup), **({"errors": errors[sid]} if errors[sid] else {})}
            report["_polish_unchanged"] = all(
                (backup / "polish" / f.name).exists() and (backup / "polish" / f.name).read_bytes() == f.read_bytes()
                for f in POLISH.glob("*.json"))
        elif mode == "base":
            # Record the builder's own short/variants per entry: polish patches were written
            # against these, and apply_polish only replaces a short that still equals its base.
            base = {}
            for sid in wanted:
                restore(backup)
                (SECTIONS / f"{sid}.json").unlink()
                errors = build(sid)
                if errors or not (SECTIONS / f"{sid}.json").exists():
                    report[sid] = {"status": "NO_OUTPUT", "errors": errors}
                    continue
                for entry in json.loads((SECTIONS / f"{sid}.json").read_text(encoding="utf-8"))["entries"]:
                    base[entry["id"]] = {"short": entry["answer"]["short"], "variants": entry["answer"].get("variants", [])}
                report[sid] = {"status": "BASE", "entries": sum(1 for k in base if k.startswith(sid + "."))}
            (HERE / "polish_base.json").write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            for sid in wanted:
                restore(backup)
                (SECTIONS / f"{sid}.json").unlink()
                errors = build(sid)
                if not (SECTIONS / f"{sid}.json").exists():
                    report[sid] = {"status": "NO_OUTPUT", "errors": errors}
                    continue
                coordinator_fixes.main()
                report[sid] = {**compare(sid, backup), **({"errors": errors} if errors else {})}
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
    finally:
        restore(backup)
        fcntl.flock(lock, fcntl.LOCK_UN)
        print(f"restored corpus and polish/ from {backup}", file=sys.stderr)
    (HERE / f"regen_report.{mode}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for sid, r in report.items():
        print(f"{sid:17} {json.dumps(r, ensure_ascii=False)[:260]}")


if __name__ == "__main__":
    main()
