#!/usr/bin/env python3
"""Write the corrected activities section. Does not load pre-correction entries."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corrected_lib import ENTRIES, write_section
import corrected_entries_a
import corrected_entries_b
import corrected_entries_c
import corrected_entries_d


def main() -> None:
    corrected_entries_a.register()
    corrected_entries_b.register()
    corrected_entries_c.register()
    corrected_entries_d.register()
    out = Path("/home/cruz1122/dev/hacka-airplane/data/knowledge/sections/activities.json")
    write_section(out)
    print(f"entries={len(ENTRIES)} -> {out}")


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: activities now builds from activities/source/activities.v1.json via coordination/build_from_snapshot.py activities; rerunning this script would revert reviewed corrections.")
    main()
