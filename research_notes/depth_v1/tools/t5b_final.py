"""T5b final set per parent shard: resolved/S.jsonl plus the approved top-up rows
(resolved/T5b_U<nn>r.jsonl) of S's entries, then the check_replies selection.

Writes resolved/S.final.jsonl (kept rows) and resolved/S.final.low.json (entries still below goal).

usage: python3 t5b_final.py T5b_000 T5b_001 ...
"""

from __future__ import annotations

import json
import subprocess
import sys

from common import DEPTH, read_jsonl


def main() -> None:
    # Each top-up numbers its pids from #u01, so two top-ups of one entry reuse pids: the row keeps
    # its source shard in `src` and a top-up pid gets "@<src>" so pids stay unique per entry.
    topups = [{**r, "pid": f"{r['pid']}@{p.stem}", "src": p.stem}
              for p in sorted((DEPTH / "resolved").glob("T5b_U[0-9][0-9]r.jsonl")) for r in read_jsonl(p)]
    for s in sys.argv[1:]:
        ids = {e["entry_id"] for e in json.loads((DEPTH / f"shards/{s}.json").read_text())["entries"]}
        rows = ([{**r, "src": s} for r in read_jsonl(DEPTH / f"resolved/{s}.jsonl")]
                + [r for r in topups if r["entry_id"] in ids])
        both = DEPTH / f"resolved/{s}.all.jsonl"
        both.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        out = subprocess.run([sys.executable, "check_replies.py", str(both), "--write",
                              str(DEPTH / f"resolved/{s}.final.jsonl"), "--quiet"],
                             check=True, cwd=DEPTH / "tools", capture_output=True, text=True).stdout.strip()
        print(s, out)


if __name__ == "__main__":
    main()
