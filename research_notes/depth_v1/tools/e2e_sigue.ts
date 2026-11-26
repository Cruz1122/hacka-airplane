// E2E "ask -> sigue x4", same question x8 and partial disclosure (A5, A11, A13) on the REAL engine,
// catalog and index vectors. A stub embedder returns the index row of the target entry, so only the
// depth / rotation logic is under test.
//
//   cd mobile && npx jest e2e_sigue --silent=false                        # prints the summary table
//   cd mobile && E2E_SIGUE_STRICT=1 npx jest e2e_sigue --silent=false     # also fails on A5/A11/A13 gaps
//
// Needs mobile/assets/data/knowledge/depth.json and policy.continuation, which export_nlu.py emits once
// data/knowledge/app/{depth_replies,reply_variants,fact_inventory}.json exist; without them the test
// is skipped and says so.
//
// The code lives under mobile/ because jest cannot resolve Babel's runtime from outside that package:
//   mobile/src/core/knowledge/__fixtures__/e2e_sigue.ts   (scenarios + report)
//   mobile/src/core/knowledge/__tests__/e2e_sigue.test.ts (jest entry)
export {
  e2ePasses,
  formatReport,
  runE2e,
} from '../../../mobile/src/core/knowledge/__fixtures__/e2e_sigue';
