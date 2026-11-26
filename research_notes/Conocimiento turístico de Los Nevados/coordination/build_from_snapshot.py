"""Builder for sections whose source of truth is a reviewed snapshot, not a generator.

`N/<section>/source/<section>.v1.json` holds the delivered v1 section (2026-11-21). These sections'
original generators predate corrections and polish that were applied to the JSON itself, so rerunning
them would revert reviewed text. The snapshot is frozen. Later rounds change the section only through
`N/<section>/source/overlay.py`, which defines `apply(section: dict) -> dict` (upsert/remove entries by id,
edit fields); this builder runs it on a fresh copy of the snapshot, so the overlay must be deterministic.
Then run coordination/coordinator_fixes.py.

Usage: python3 build_from_snapshot.py <section>
"""

import importlib.util
import json
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parents[1]
SECTIONS = NOTES.parents[1] / "data/knowledge/sections"


def main():
    section = sys.argv[1]
    data = json.loads((NOTES / section / "source" / f"{section}.v1.json").read_text(encoding="utf-8"))
    if data.get("id") != section:
        sys.exit(f"snapshot id {data.get('id')!r} does not match {section!r}")
    overlay = NOTES / section / "source" / "overlay.py"
    if overlay.exists():
        spec = importlib.util.spec_from_file_location(f"{section}_overlay", overlay)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        data = module.apply(data)
    (SECTIONS / f"{section}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {section}.json from snapshot: {len(data['entries'])} entries")


if __name__ == "__main__":
    main()
