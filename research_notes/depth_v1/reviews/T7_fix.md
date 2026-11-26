# T7 fix review
## Still open
- None.
## Closed
- `[continuation.ts:140-146]` unknown atoms — `assets.ts` now rejects every text atom absent from `d.complements`; the asset-validation test passes for this case.
- `[continuation.ts:140-146]` re-served complement facts — `pool()` prefers fully disjoint positive-gain texts and falls back only when no such text exists, so a new complement is revealed whenever one exists; the focused continuation suite passes.
- `[engine.ts:309]` emergency depth bypass — `continuation()` skips all depth-layer serving for `emergency_direct` entries, while walk replies remain separate; the emergency safety test passes.
- `[assets.ts:320]` continuation-off compatibility — `validateContinuation()` returns before inspecting depth when `policy.continuation` is absent or null; the null-policy compatibility tests pass.
- Verification — `npx jest src/core/knowledge/__tests__/continuation.test.ts --runInBand` observed 1 passed suite and 198 passed tests.
