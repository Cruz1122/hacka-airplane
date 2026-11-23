// Keeps app UI on the design tokens (see .claude/skills/app-design): no raw colors, no font names,
// no fontWeight. Exempt on purpose: the Lab (web-only editor with its own CSS), the onboarding
// illustration (its palette lives in the scene document and is edited in the Lab) and the Pet's
// drawing (character colors are part of the asset, ported from its own lab).
import { readdirSync, readFileSync, statSync } from 'fs';
import { join, relative } from 'path';

const ROOT = join(__dirname, '../../..');
const SCANNED = ['app', 'src/ui', 'src/chat', 'src/onboarding/OnboardingOverlay.tsx'];
const EXEMPT = [/^app\/lab/, /^src\/ui\/pet\//, /^src\/ui\/theme\//, /__tests__/];

function files(path: string): string[] {
  const full = join(ROOT, path);
  if (!statSync(full).isDirectory()) return [path];
  return readdirSync(full).flatMap((name) => files(join(path, name)));
}

const uiFiles = SCANNED.flatMap(files).filter(
  (f) => /\.tsx?$/.test(f) && !EXEMPT.some((re) => re.test(relative('.', f))),
);

/** Each offending line as "file:line: text"; comments are ignored. */
function offenders(test: (code: string) => boolean): string[] {
  return uiFiles.flatMap((f) =>
    readFileSync(join(ROOT, f), 'utf8')
      .split('\n')
      .map((line, i) => ({
        code: line.replace(/\/\/.*$/, ''),
        at: `${f}:${i + 1}: ${line.trim()}`,
      }))
      .filter(({ code }) => test(code))
      .map(({ at }) => at),
  );
}

describe('design guard', () => {
  it('scans the app UI', () => {
    expect(uiFiles).toEqual(
      expect.arrayContaining(['app/onboarding.tsx', 'src/onboarding/OnboardingOverlay.tsx']),
    );
  });

  it('uses token colors only', () => {
    expect(offenders((c) => /#[0-9a-fA-F]{3,8}\b|\brgba?\(/.test(c))).toEqual([]);
  });

  it('uses token fonts only (platform monospace allowed for debug output)', () => {
    expect(
      offenders((c) => {
        const m = c.match(/fontFamily:\s*(.*)/);
        return !!m && !/^fonts\./.test(m[1]) && !/monospace|Menlo/.test(m[1]);
      }),
    ).toEqual([]);
  });

  it('never sets fontWeight (Android ignores it for bundled fonts; pick the family)', () => {
    expect(offenders((c) => /fontWeight/.test(c))).toEqual([]);
  });

  it('takes user-facing copy from src/i18n, never from literals', () => {
    // JSX text with words, or quoted words in a copy prop's value (`label="..."`,
    // `title: '...'`, `label={last ? '...' : '...'}`).
    const jsxText = />[^<>{}]*\p{L}{2,}[^<>{}]*<\//u;
    const copyProp =
      /\b(label|title|subtitle|placeholder|hint|accessibilityLabel|accessibilityHint)(=\{?|:)[^'"`{}]*['"`][^'"`]*\p{L}{2,}/u;
    expect(
      offenders((c) => jsxText.test(c) || copyProp.test(c)).filter(
        // The design catalog names its own samples.
        (at) => !at.startsWith('app/design.tsx'),
      ),
    ).toEqual([]);
  });
});
