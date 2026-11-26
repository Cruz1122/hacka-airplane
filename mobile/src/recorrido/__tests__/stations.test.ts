import { mapPoint, STATION_COORDS, STATION_IDS, STATION_NODES, type StationId } from '../stations';
import { TRAIL_MAP } from '../trailMap.generated';

/** The route sketch's six chunks start one row below the map's extra north row. */
const SKETCH_ROW0 = 1;

/** 1-based chunk number of the route sketch (row-major from the north-west, north up). */
function sketchChunk(id: StationId): number {
  const { x, y } = mapPoint(STATION_COORDS[id].lat, STATION_COORDS[id].lon);
  const col = Math.floor(x * TRAIL_MAP.cols);
  const row = Math.floor(y * TRAIL_MAP.rows) - SKETCH_ROW0;
  return row * TRAIL_MAP.cols + col + 1;
}

test('every stop lies inside the traced map', () => {
  for (const { x, y } of STATION_NODES) {
    expect(x).toBeGreaterThan(0);
    expect(x).toBeLessThan(1);
    expect(y).toBeGreaterThan(0);
    expect(y).toBeLessThan(1);
  }
});

test('the route runs north (Brisas) to south (Valle de las Tumbas)', () => {
  const lats = STATION_IDS.map((id) => STATION_COORDS[id].lat);
  expect([...lats].sort((a, b) => b - a)).toEqual(lats);
});

test('the map is shown south-up: the route climbs the screen', () => {
  const ys = STATION_NODES.map((n) => n.y);
  expect([...ys].sort((a, b) => b - a)).toEqual(ys);
});

test('stops fall in the chunks of the route sketch', () => {
  expect(sketchChunk('brisas')).toBe(2);
  expect(sketchChunk('aguacerales')).toBe(4);
  expect(sketchChunk('arenales')).toBe(3);
  expect(sketchChunk('valleLunar')).toBe(3);
  expect(sketchChunk('valleTumbas')).toBe(6);
});

test('every chunk has terrain', () => {
  expect(TRAIL_MAP.chunks).toHaveLength(TRAIL_MAP.cols * TRAIL_MAP.rows);
  for (const layers of TRAIL_MAP.chunks) expect(layers.length).toBeGreaterThan(0);
});
