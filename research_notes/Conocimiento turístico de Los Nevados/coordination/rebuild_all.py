"""Rebuild every section from its canonical builder, then run coordinator_fixes (coordinator only).

Unlike regen_test.py this keeps the result. Use after changing polish/style inputs that were already
applied to the live corpus (patches are not reversible in place).
"""

import fcntl
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import builders  # noqa: E402
import coordinator_fixes  # noqa: E402
from regen_test import build  # noqa: E402

if __name__ == "__main__":
    with open(HERE / "coordinator_fixes.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        failures = {sid: build(sid) for sid in builders.BUILDERS}
        failures = {k: v for k, v in failures.items() if v}
        if failures:
            sys.exit(f"builder failures: {failures}")
    coordinator_fixes.main()
    print("rebuilt", len(builders.BUILDERS), "sections")
