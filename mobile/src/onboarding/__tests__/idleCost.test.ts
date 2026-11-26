// Why usePlayback holds idle motions during a transition: on the default scene, a 30 fps idle clock
// changes several times more object identities per camera frame (each one an SVG subtree the scene
// re-renders) than the tracks do. Counts identities, not renders or frame rate.
import { defaultScene } from '../scene/preset';
import { applyMotions, evaluateTracks } from '../scene/timeline';
import type { SceneDoc } from '../scene/types';

const FRAMES = 24; // a 400 ms move at 60 Hz
const scene = defaultScene();

function changedObjects(a: SceneDoc, b: SceneDoc): number {
  let n = 0;
  b.layers.forEach((l, i) =>
    l.objects.forEach((o, j) => (n += o !== a.layers[i].objects[j] ? 1 : 0)),
  );
  return n;
}

/** Mean object identity changes per frame of a 0 -> 1 easeOut move. */
function perFrame(timeAt: (frame: number) => number): number {
  const at = (f: number) =>
    applyMotions(evaluateTracks(scene, 1 - (1 - f / FRAMES) ** 3), timeAt(f));
  let prev = at(0);
  let total = 0;
  for (let f = 1; f <= FRAMES; f++) {
    const next = at(f);
    total += changedObjects(prev, next);
    prev = next;
  }
  return total / FRAMES;
}

it('holding the idle clock removes most per-frame object changes during a transition', () => {
  const running = perFrame((f) => 100 + Math.floor((f * 16.67) / 33) * 0.033);
  const held = perFrame(() => 200);
  expect(running).toBeGreaterThan(held * 3);
});
