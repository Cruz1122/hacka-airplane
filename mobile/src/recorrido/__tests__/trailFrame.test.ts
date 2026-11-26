import { trailFrame } from '../RecorridoScreen';
import { STATION_NODES } from '../stations';
import { markExtent, trailMapHeight } from '../TrailPath';

jest.mock('expo-router', () => ({ router: { push: jest.fn() } }));
jest.mock('@/ui/useAccessibilityTheme', () => ({ useAccessibilityTheme: jest.fn() }));

const TOP = 47 + 53 + 16;
const BOTTOM = 34 + 36;

function onScreen(vw: number, vh: number) {
  const f = trailFrame(vw, vh, TOP, BOTTOM);
  const h = trailMapHeight(f.width);
  const { above, below } = markExtent(f.width);
  const ys = STATION_NODES.map((n) => f.y + n.y * h);
  const xs = STATION_NODES.map((n) => f.x + n.x * f.width);
  return { f, h, first: Math.min(...ys) - above, last: Math.max(...ys) + below, xs };
}

test.each([
  [390, 844],
  [360, 740],
  [390, 640],
  [820, 1180],
  [820, 600],
])('the whole route fits a %ix%i screen', (vw, vh) => {
  const { first, last, xs } = onScreen(vw, vh);
  expect(first).toBeGreaterThanOrEqual(TOP - 0.5);
  expect(last).toBeLessThanOrEqual(vh - BOTTOM + 0.5);
  for (const x of xs) {
    expect(x).toBeGreaterThan(0);
    expect(x).toBeLessThan(vw);
  }
});

test('on a phone the map covers the width and reaches the bottom edge', () => {
  const { f, h } = onScreen(390, 844);
  expect(f.width).toBeGreaterThanOrEqual(390);
  expect(f.x).toBeLessThanOrEqual(0);
  expect(f.y + h).toBeGreaterThanOrEqual(844 - 0.5);
  expect(f.y).toBeLessThanOrEqual(0);
});

test('Brisas is at the bottom and Valle de las Tumbas at the top', () => {
  const y = Object.fromEntries(STATION_NODES.map((n) => [n.id, n.y]));
  expect(y.brisas).toBeGreaterThan(y.aguacerales);
  expect(y.aguacerales).toBeGreaterThan(y.valleTumbas);
});
