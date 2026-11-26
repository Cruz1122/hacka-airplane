# T7 implementer — continuation runtime ("sigue"), reply rotation, partial disclosure

Repo: /home/cruz1122/dev/hacka-airplane. Mobile app: Expo + TypeScript in `mobile/`.

## Read first (and only what you need)
1. `.claude/skills/mobile-offline-stack/SKILL.md` and `.claude/skills/hackathon-lean/SKILL.md`.
2. `research_notes/depth_v1/ORCHESTRATION_PROMPT.md`, ONLY these parts: Part A R4, R6.5, R6.6, R7,
   acceptance A5, A7, A11, A13; Part B §4 (outputs table), §5, §5b, §6. Use `grep -n` to find them.
3. `mobile/src/core/knowledge/{engine,assets,types,policy,safety,clean,index}.ts`,
   their tests in `mobile/src/core/knowledge/__tests__/`, and `experiments/nlu/export_nlu.py`.
Do not read `data/knowledge/sections/` wholesale (use `jq`/python one-liners if you need a sample).
Never read `.env` or credentials. Do not commit. Do not touch files unrelated to this task.

## Build
1. `experiments/nlu/export_nlu.py`: when `data/knowledge/app/depth_replies.json`,
   `reply_variants.json` and `fact_inventory.json` exist, emit a mobile asset (e.g.
   `mobile/assets/data/knowledge/depth.json`) with per-entry L0 texts `{text, atoms}`, layers
   `{kind, texts:[{text, atoms}]}`, `walk`, the complement fids, and the emergency rotation sets; and
   `policy.continuation = {cue, max_words: 6, why_cue, bridges, texts: {no_state, exhausted}}`.
   When those files do not exist, emit `continuation: null` and no depth data, so the export is
   byte-identical to today. Today none of the three files exists.
2. `assets.ts`: types + validation for `continuation` and depth (every depth/walk id must be in the
   catalog, or validation fails).
3. `engine.ts` (Part B §6 + §5b):
   - continuation branch after `detectSafety` and before `embed` (R4.1–R4.5), accent-folded,
     whole message ≤6 words; urgent / abstain / off-topic / reset clear the state (R4.7);
   - re-asked same entry serves the next unserved L0 paraphrase, never the text just shown (R4.6);
   - seeded per-session rotation `rot` (R6.5); emergency entries rotate only over their approved
     set (R6.6); seed injectable (R7.7);
   - partial disclosure (R7.2–R7.5): choose texts by unserved complement atoms; every "sigue" reveals
     ≥1 new fid; then walk with a fact-free bridge; then the exhausted text with 2 related topic
     labels in text (no menu);
   - `prevText` untouched on continuation turns; `policy.continuation == null` => behaviour
     byte-identical to today.
4. Jest tests: detector table (≥40 positives incl. typos, ≥40 near-misses such as "¿sigue abierto?",
   "más o menos cuánto", "más cerca de Pereira"), state machine, urgent-clears-state, exhausted text,
   rotation (×8 distinct, wrap-around never repeats the last text), emergency rotation, A13 on a
   small synthetic depth fixture, null policy = today's output byte for byte.
5. `research_notes/depth_v1/tools/e2e_sigue.ts` (or a jest test it wraps): runs the REAL engine with
   a stub embedder that returns the target entry, over every catalog entry that has depth data:
   "ask → sigue ×4" (report repeats, distinct turns, exhaustions), same question ×8 (distinct texts),
   and A13. Must run in one documented command and print a summary table; it must work with the
   real `depth.json` once it exists and skip cleanly when it does not.

## Verify (read the real output)
`cd mobile && npx jest src/core/knowledge && npm run typecheck && npm run lint`, and
`cd experiments/nlu && uv run python export_nlu.py` (check that `git diff --stat mobile/assets` is
empty when the depth files are absent).

## Report
Write `research_notes/depth_v1/decisions/T7_impl.md`: files changed, design choices, test counts,
command outputs (pass/fail lines), anything not verified. Reply with one line: the path.
