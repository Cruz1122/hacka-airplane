# Mobile knowledge engine

## Purpose

`mobile/src/core/knowledge` turns one chat message into one `KnowledgeReply` (`types.ts`): a curated answer or an abstain text, with an optional banner. It is pure TypeScript. The `Embed` and `Score` functions are injected, so Jest runs it on Node.

## Start here

- `engine.ts`. `KnowledgeEngine.ask(text, { visualEntryId?, preferCaption?, verifiedOnly? })` (`AskOptions`) and `resetContext()`.
- `assets.ts`. Asset shapes and `validateAssets`.
- Callers: `mobile/src/llm/knowledgeRuntime.ts`, `knowledgeAssets.ts` (`degradedKnowledgeEngine`), and `mobile/src/state/knowledgeChat.ts`.

## Runtime or data flow

`ask` runs these steps in order:

1. `detectSafety` (`safety.ts`) and `bannerFor` (`policy.ts`). No model runs, so the urgent banner survives an embedder failure.
2. A known `visualEntryId` answers that entry, unless `preferCaption` is true. Under `verifiedOnly` only a verified entry does.
3. A "sigue" or "por qué" cue (`continuation.ts`) serves depth text without retrieval.
4. `clean`, `embed`, `score`, and `retrieve` (`retrieve.ts`), with follow-up fusion from `policy.followup`.
5. An optional `Reranker` (`rerank.ts`). Its order is kept only when `isReordering` is true.
6. `decide` (`policy.ts`). An urgent turn takes the best `emergency_direct` entry. Other turns need a top cosine of at least `T`.

`verifiedOnly` (the Settings switch, `src/state/verifiedOnly.ts`) answers only from catalog rows with `verified_by_uton: true`. After step 4 it ranks every verified entry by its final score (`rankEntries`, cut to `k`), so a verified entry below the full pool's `k` still competes; the follow-up context keeps every entry. Its turns serve the canonical `short` (no L0 rotation, no depth layer), walk "sigue" to verified ids only, and abstain with `texts.abstain_verified ?? texts.abstain`. Urgent turns and the 123 banner ignore it. Every answer carries `verified` (the row flag) for the chat's seal.

On a retrieval error, an urgent turn returns `emergency_line_id`. A turn with no banner rethrows `KnowledgeEngineError`.

## Tests

- `__tests__/engine.test.ts` and `retrieve*.test.ts` load the git-ignored `models/knowledge/index.f32.bin` through `loadVectors` in `__fixtures__/load.ts`. `KNOWLEDGE_VECTORS` overrides the path.
- `safety.test.ts` uses `safety_probes.json`. Never tune rules on `safety_blind_set.json`.
- `continuation.test.ts` uses `depth_synth.ts`. `e2e_sigue.test.ts` asserts only with `E2E_SIGUE_STRICT=1`.
- `experiments/nlu/export_nlu.py` writes `retrieval.json`, `clean.json`, and `continuation.json`.

## Common change paths

- Safety phrasing: edit the rule arrays in `safety.ts` and add a probe.
- Thresholds: rerun the `EXPORTER` command in `__fixtures__/load.ts`. Do not edit `policy.json` by hand.
- Reranker: pass one to the constructor in `knowledgeRuntime.ts`. `mobile/src/llm/laya.ts` is a stub that throws.

## Related docs

- [architecture.md](../../architecture.md). The call sequence and native loaders.
- [retrieval-architecture.md](../../retrieval-architecture.md). Gates, scoring, and the policy parameters.
- [knowledge-contract.md](../../knowledge-contract.md). The catalog entry schema.
