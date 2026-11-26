"""Apply the R24 re-judged second reviews (DECISION_LOG 24) to reviews/S_2.jsonl, then re-merge.

Reads second_queue/R24_*.jsonl (input rows, each with `src`) and the matching *.out.jsonl verdicts.
For every touched source shard S, the old reviews/S_2.jsonl is copied once to reviews/order_strict/,
then each re-judged pid's verdict replaces the old one (or is added). Finally t5b_merge.py re-runs
on the touched shards so resolved/S.jsonl picks up the new verdicts.

usage: python3 r24_apply.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys

from common import DEPTH, read_jsonl


def main() -> None:
    new: dict[str, dict[str, dict]] = {}
    for q in sorted((DEPTH / "second_queue").glob("R24_*.jsonl")):
        if q.name.endswith(".out.jsonl"):
            continue
        rows, out = read_jsonl(q), read_jsonl(q.with_suffix(".out.jsonl"))
        if [r["pid"] for r in rows] != [o["pid"] for o in out]:
            sys.exit(f"{q.name}: output pids do not match the input order")
        for r, o in zip(rows, out):
            if o.get("verdict") not in ("ok", "drop"):
                sys.exit(f"{q.name}: bad verdict for {o['pid']}")
            new.setdefault(r["src"], {})[r["pid"]] = o
    (DEPTH / "reviews/order_strict").mkdir(exist_ok=True)
    for src, verdicts in sorted(new.items()):
        path = DEPTH / f"reviews/{src}_2.jsonl"
        old = read_jsonl(path) if path.exists() else []
        backup = DEPTH / f"reviews/order_strict/{src}_2.jsonl"
        if path.exists() and not backup.exists():
            shutil.copy(path, backup)
        merged = {r["pid"]: r for r in old} | verdicts
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged.values()))
        ok = sum(v["verdict"] == "ok" for v in verdicts.values())
        print(src, f"re-judged {len(verdicts)}, ok {ok}")
    subprocess.run([sys.executable, "t5b_merge.py", *sorted(new)], check=True, cwd=DEPTH / "tools")


if __name__ == "__main__":
    main()
