# T7 reviewer — continuation runtime ("sigue"), rotation, partial disclosure

You review code another model wrote for an offline park assistant (Expo app, TypeScript). Be
adversarial: find real defects, prove each one by running code (a jest test in your scratch file or
`npx tsx`/`node` snippet), and report only proven or clearly reasoned ones.

## Read only
1. `research_notes/depth_v1/decisions/T7_impl.md` (the implementer's report).
2. `research_notes/depth_v1/ORCHESTRATION_PROMPT.md`, ONLY Part A R4, R6.5, R6.6, R7 (use
   `grep -n` to find them; print only those line ranges).
3. The code: `mobile/src/core/knowledge/continuation.ts`, and the diff of
   `git diff -- mobile/src/core/knowledge/engine.ts mobile/src/core/knowledge/assets.ts mobile/src/core/knowledge/index.ts experiments/nlu/export_nlu.py`.
4. Tests only as needed: `mobile/src/core/knowledge/__tests__/continuation.test.ts`.

Do NOT edit any repository file. Scratch tests go in `mobile/src/core/knowledge/__tests__/zz_review_<you>.test.ts`
and you DELETE that file before you finish. Do not run `export_nlu.py` (18 min, writes assets).

## Focus (the task names one)
- `logic`: R4 state machine (cue detector false positives on real questions, state clearing, R4.6
  re-ask never repeats the text just shown), R6.5 rotation (no immediate repeat, wrap), R7 partial
  disclosure (each "sigue" reveals ≥1 unserved complement fid or moves to the walk; never re-serves a
  fid), asset validation gaps, exporter `depth_assets()` contract.
- `safety`: urgent/emergency path. An urgent message must never take the continuation branch; an
  emergency entry must never serve an unapproved paraphrase (R6.6, fewer than 3 approved → canonical);
  "sigue" after an urgent/safety answer; a cue in a message that also has urgent words; that a
  null/absent `policy.continuation` is byte-identical to the old engine.

## Output
Write ONLY the output path given in the task, as markdown:

```
# T7 review (<focus>)
## Findings
- [high|med|low] <file>:<line> — <defect>. Proof: <command + observed output>. Fix: <one line>.
## Checked, no defect
- <what you tested, one line each>
```

Reply with one line: "<output path> <n findings>".
