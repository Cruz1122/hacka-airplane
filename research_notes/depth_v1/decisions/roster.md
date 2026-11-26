# Roster — depth_v1 (T3 Code delegate_task)

| Agent | providerInstanceId | model | family | smoke row |
|---|---|---|---|---|
| nv-sonnet | claudeAgent | claude-sonnet-5-5 | Anthropic | proposals/T1_smoke_nv-sonnet.jsonl |
| nv-luna | codex | gpt-6-luna | OpenAI Luna | proposals/T1_smoke_nv-luna.jsonl |

- Alternation and roles: `tools/ledger.py pick` (even shard: Sonnet writes / Luna verifies; odd: reverse;
  arbitration: fresh Luna session).
- OpenCode agents (nv-go, nv-zen) removed on user request (DECISION_LOG 4). An nv-zen smoke row was
  produced before the cancel and deleted.
