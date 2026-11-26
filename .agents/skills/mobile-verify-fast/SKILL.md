---
name: mobile-verify-fast
description: Use before running tests, typecheck, lint, Metro, or a phone check for mobile/. Gives the fastest check that proves a change, measured run times, and the Metro, adb, and web-versus-native traps that waste runs.
---

# Fast verification for mobile/

Run every command from `mobile/`. The test map is `docs/agent-index/areas/29-tests-and-quality.md`.

## Pick the smallest check

| Check | Time (approximate, measured 2026-11-26 on a loaded laptop) | When |
|---|---|---|
| `npx jest <path>` | 3.6 s for `src/core/group` (35 tests) | after every edit |
| `npx tsc --noEmit` | 30 s | once, before you report |
| `npx expo lint` | | once, before you report. Add `--no-cache` if `import/no-unresolved` names a path that exists |
| `npx jest` (all) | 4 min 9 s, 2316 tests | only when you changed a shared module, an export, or `policy.json` |

- Pass test folders or files to `npx jest`. Use `-t '<name>'` for one case.
- UI files under `app/`, `src/ui/`, and `src/chat/` are scanned by `src/ui/__tests__/design-guard.test.ts`. Run it after a UI edit: `npx jest src/ui/__tests__/design-guard`.
- Format only the files you touched: `npx prettier --single-quote --print-width 100 --write <files>`. There is no repo Prettier config.
- Jest cannot load Skia. Keep scene and layout data modules free of renderer imports, or their tests fail to import.

## Tests that need side-loaded files

Knowledge tests read `models/knowledge/index.f32.bin` (git-ignored) and check its sha256. `src/core/__tests__/driver.test.ts` reads the ignored `src/core/__fixtures__/replays.json`. In a fresh worktree, run the `shared-checkout` skill's link script first. A sha256 error means the vectors and the bundled fixtures come from different exports. The error prints the regenerate command.

## Metro and the phone

- Port 8081 often belongs to another session's Metro. Check with `ss -ltnp | grep 8081`. Start your own on a free port: `npx expo start --dev-client --port 8082 < /dev/null`, then `adb reverse tcp:8082 tcp:8082`.
- Start Metro with `< /dev/null` and without `CI=1`. With `CI=1`, Metro does not watch files and the app keeps the old bundle.
- In a dev build, `console.log` goes to the Metro output, not to logcat.
- `adb shell input text` crashes on `ñ` and accented letters, and the screen keeps the previous reply. Fold typed text to ASCII.
- Side-load model and knowledge files with `scripts/push-knowledge.sh` and `scripts/push-model.sh`.

## What a check proves

- A web preview does not prove native behavior. Native scenes and the Pet draw with Skia. Web uses Canvas2D and SVG.
- Do not measure native performance on a debug APK. react-native-svg Java runs about 4 times slower there. Use `./gradlew assembleRelease` (see `mobile/README.md`).
- Do not report a native speedup from web numbers.

## Shared checkout

Other chats often edit `mobile/` in the main checkout at the same time. A test that fails in a file you did not touch may be their work in progress. Check `git status` and `git diff <file>` before you fix it. See the `shared-checkout` skill.
