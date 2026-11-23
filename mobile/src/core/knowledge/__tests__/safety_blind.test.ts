import { fixture } from '../__fixtures__/load';
import { detectSafety } from '../safety';

// Frozen blind set, written without seeing the rules. It was read only by this test, after the rules
// were final; never tune safety.ts on it. Report aggregates only.
interface BlindSet {
  version: number;
  items: { q: string; label: 'emergency' | 'informative'; topic: string }[];
}

/** Wilson score interval, 95 %. */
function wilson(k: number, n: number, z = 1.96): [number, number] {
  if (n === 0) return [0, 1];
  const p = k / n;
  const d = 1 + (z * z) / n;
  const c = p + (z * z) / (2 * n);
  const h = z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
  return [Math.max(0, (c - h) / d), Math.min(1, (c + h) / d)];
}

const pct = (x: number) => `${(100 * x).toFixed(1)} %`;

describe('safety rules on the frozen blind set', () => {
  const set = fixture<BlindSet>('safety_blind_set.json');
  const emergency = set.items.filter((i) => i.label === 'emergency');
  const informative = set.items.filter((i) => i.label === 'informative');
  const tp = emergency.filter((i) => detectSafety(i.q).urgent).length;
  const fp = informative.filter((i) => detectSafety(i.q).urgent).length;

  it('reports recall and false-positive rate with Wilson 95 % intervals', () => {
    expect(emergency.length).toBeGreaterThan(0);
    expect(informative.length).toBeGreaterThan(0);
    const recall = tp / emergency.length;
    const fpr = fp / informative.length;
    const [rl, rh] = wilson(tp, emergency.length);
    const [fl, fh] = wilson(fp, informative.length);
    process.stdout.write(
      `blind set v${set.version}: recall ${tp}/${emergency.length} = ${pct(recall)} [${pct(rl)}, ${pct(rh)}]; ` +
        `false positives ${fp}/${informative.length} = ${pct(fpr)} [${pct(fl)}, ${pct(fh)}]\n`,
    );
    expect(recall).toBeGreaterThanOrEqual(0.5);
  });
});
