---
name: repo-search-budget
description: Use before any grep, rg, find, cat, or Read in this repo, and before briefing a subagent that will search. Gives the scoped search command, the files never to read whole, and how to peek inside the multi-MB JSON data. Prevents flooded search results and context blowups.
---

# Repo search budget

Start from `docs/agent-index/README.md`. It routes each task to an area page with the exact files. Search only when the area page does not name the file.

## Search code, not data

An unscoped `rg -l nevado` matches 1936 files. The scoped command below matches 98 (measured 2026-11-26, approximate). Most of the noise is research evidence and data rows.

```bash
rg -n -M 300 \
  -g '!research_notes' -g '!data' -g '!mobile/assets' \
  -g '!experiments/nlu/work' -g '!**/__fixtures__' \
  '<pattern>'
```

- `-M 300` hides lines over 300 characters. Several JSON files are one line of 0.7 to 10 MB.
- Drop one `-g '!…'` only when the task is about that folder.
- For Spanish corpus text, search `data/knowledge/sections/` alone. It holds the source entries.

## Never read these whole

| File | Size |
|---|---|
| `mobile/assets/vision/index.json` | 10 MB, list of 492 |
| `mobile/assets/data/knowledge/depth.json` | 4.2 MB, `entries` map of 843 |
| `mobile/assets/data/knowledge/catalog.json` | 0.7 MB, list of 843 |
| `data/knowledge/app/*.json` | 1 to 3.6 MB each |
| `data/knowledge/laya_ft/*.jsonl`, `research_notes/**/work/*.jsonl` | 1 to 5.6 MB |
| `research_notes/**/evidence/*` | up to 9.8 MB |
| `mobile/package-lock.json`, `uv.lock` | 0.7 MB |

Peek instead:

```bash
jq '.[0] | keys' mobile/assets/vision/index.json
jq '.entries["access.how_to_choose_sector"]' mobile/assets/data/knowledge/depth.json
jq '.[] | select(.id=="access.how_to_choose_sector")' mobile/assets/data/knowledge/catalog.json
head -n 3 data/knowledge/laya_ft/train.jsonl; wc -l data/knowledge/laya_ft/train.jsonl
rg -n -M 300 '<term>' <evidence file>
```

Before you open an unknown data file, run `du -b <file>`. Over 200 KB, query it instead of reading it.

## Ignored heavy folders

`mobile/node_modules` (12 GB), `experiments/nlu/.venv` (6.8 GB), `experiments/laya/.venv`, and `models/` (2.5 GB of GGUF and ONNX) are git-ignored. `rg` skips them by default. `find` and `du` do not, so pass `-not -path '*/node_modules/*' -not -path '*/.venv/*'`.

## Generated files

Never edit generated files by hand. `mobile/README.md` ("Generated, never edit by hand") and the `mobile-offline-stack` skill list them with their generators. `docs/system-map.md` says what to rerun after each change.

## Delegating a search

Put the scoped command and this file's path in the child's brief. Ask for paths and line numbers, not file contents.
