"""Dispatch ledger: the source of truth for who wrote / verified / arbitrated each shard.

Rows of decisions/dispatch.jsonl: {shard, task, role(write|verify|verify2|arbitrate|label|research),
agent, model, task_id, status(sent|done|failed|cancelled), ts, note}. Later rows for the same
(shard, role) override earlier ones. `by` in integrated outputs is stamped from here, never from
the child's self-report.

usage: python3 ledger.py add <shard> <task> <role> <agent> <task_id> [note]
       python3 ledger.py set <shard> <role> <status> [note]
       python3 ledger.py show [task]
       python3 ledger.py pick <shard_index> <role>      -> agent for alternation (Part B §8)
"""

from __future__ import annotations

import json
import sys
import time

from common import DEPTH

LEDGER = DEPTH / "decisions/dispatch.jsonl"
ROSTER = {
    "nv-sonnet": {"provider": "claudeAgent", "model": "claude-sonnet-5-5", "family": "anthropic"},
    "nv-luna": {"provider": "codex", "model": "gpt-6-luna", "family": "luna"},
    "nv-luna-cursor": {"provider": "cursor", "model": "gpt-5.6-luna", "family": "luna"},
}


def rows() -> list[dict]:
    return [json.loads(l) for l in LEDGER.read_text().splitlines()] if LEDGER.exists() else []


def state() -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    for r in rows():
        key = (r["shard"], r["role"])
        out[key] = {**out.get(key, {}), **{k: v for k, v in r.items() if v is not None}}
    return out


def append(r: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({**r, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False) + "\n")


def pick(i: int, role: str) -> str:
    """Even shard: Sonnet writes, Luna verifies. Odd: the reverse. Arbitration is always a fresh Luna
    session that neither wrote nor verified the shard (DECISION_LOG 4)."""
    if role == "write":
        return "nv-sonnet" if i % 2 == 0 else "nv-luna"
    if role in ("verify", "verify2"):  # verify2 is a second, fresh session of the non-writer family
        return "nv-luna" if i % 2 == 0 else "nv-sonnet"
    if role == "arbitrate":
        return "nv-luna"
    raise ValueError(role)


def by(agent: str) -> str:
    return f"{agent}/{ROSTER[agent]['model']}"


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "add":
        shard, task, role, agent, tid = a[1:6]
        append({"shard": shard, "task": task, "role": role, "agent": agent, "model": ROSTER[agent]["model"],
                "task_id": tid, "status": "sent", "note": a[6] if len(a) > 6 else None})
    elif a[0] == "set":
        append({"shard": a[1], "role": a[2], "status": a[3], "note": a[4] if len(a) > 4 else None})
    elif a[0] == "show":
        for (s, r), v in sorted(state().items()):
            if len(a) < 2 or v.get("task") == a[1]:
                print(s, r, v.get("agent"), v.get("status"), v.get("task_id"), v.get("note") or "")
    elif a[0] == "pick":
        print(pick(int(a[1]), a[2]))
