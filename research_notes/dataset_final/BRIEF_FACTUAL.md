# Factual fix brief (G1, G2, G3)

Read `$W/BRIEF_COMMON.md` first. Then read the skill `$R/.claude/skills/add-park-knowledge/SKILL.md`
(operation format and evidence rules; it is authoritative) and `$R/docs/knowledge-contract.md`.

## Output

- `$W/proposals/<AGENT>.json` — `{"operations": [...]}` in the skill's format, `op: "update"` only
  (no adds or deletes unless your task says so). Each op carries a `reason` and full `entry`.
  Get the current entry with:
  `uv run python $R/.claude/skills/add-park-knowledge/scripts/knowledge.py --root $R inspect --id <ID>`
- `$W/decisions/<AGENT>.md` — one line per touched or deliberately untouched ID: what was wrong,
  what changed, which source/quote supports it.
- Existing evidence under `$R/research_notes/curation_v2/evidence/<section>/*.txt` may be cited by
  path (read-only; `ls`/`grep` it first, most sources are already there). New sources are fetched
  only with the provenance tool, into a section named after you (the one write exception):
  `python3 $R/research_notes/curation_v2/tools/fetch_evidence.py --section final_<AGENT> --name <slug> <URL>`
  and cited by the `.txt` path it prints. Never write or edit evidence `.txt` files by hand.
  A quote must appear verbatim in the file it cites.

Validate before you finish (read-only commands; they do not change the corpus):

```sh
TOOL=$R/.claude/skills/add-park-knowledge/scripts/knowledge.py
uv run python $TOOL --root $R stage --proposal $W/proposals/<AGENT>.json --out $W/proposals/<AGENT>.stage.json
python3 $R/research_notes/curation_v2/tools/verify_evidence.py --proposal $W/proposals/<AGENT>.json
```

Both must pass (stage `ok`, verify `fail: []`). Never run `apply`.

## Editing standard

- Change only what is wrong or misleading. Keep IDs, labels and examples unless the label itself
  is false. Do not rewrite for style.
- A dated fact (price, schedule, alert, opening, closure, registration point) states its date and
  source in the text ("según la resolución de 2023…", "a noviembre de 2026…") and sends the visitor to
  the official channel for the current value. Never present an old fact as today's state. Words
  like "hoy", "actualmente", "vigente", "está abierto" need a date or must go.
- Two official sources disagree → say both, with source and date, and do not pick one as current.
- No source supports a critical claim (access, safety, health, fees, volcanic activity) → remove the
  claim or make it conditional; if the remaining answer is empty or useless, list the ID in
  `answer_policy` (below) instead of inventing.
- Emergency guidance stays immediate and concrete; never make it depend on a menu choice; never say
  the app/phone contacts rescue, sends a location or registers anything with the park.

## `answer_policy` (G3 writes it; G1/G2 may append)

`$W/proposals/answer_policy.<AGENT>.json`: `[{"id": ..., "policy": "no_auto_answer" | "clarify_only",
"reason": ...}]`. `no_auto_answer`: the FAQ may be shown only after the visitor explicitly picks it
from a clarification list, never as an automatic answer. Use it only for entries whose remaining
answer is critical and unverifiable.
