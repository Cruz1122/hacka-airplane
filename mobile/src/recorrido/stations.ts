// Brisas vehicle route stops, north (Brisas) to south (Valle de las Tumbas). Press opens
// `/estacion/[id]`. Positions are real coordinates, placed on the traced map (trailMap.generated.ts).
// The map is shown south-up (turned 180°) so the route climbs the screen from Brisas at the
// bottom to Valle de las Tumbas at the top, the order the trail was designed in.
import { TRAIL_MAP } from './trailMap.generated';

export const STATION_IDS = [
  'brisas',
  'aguacerales',
  'arenales',
  'valleLunar',
  'valleTumbas',
] as const;

export type StationId = (typeof STATION_IDS)[number];

/** WGS84 degrees, in route order. */
export const STATION_COORDS: Readonly<Record<StationId, { lat: number; lon: number }>> = {
  brisas: { lat: 4.934637957115937, lon: -75.35013575948123 },
  aguacerales: { lat: 4.926719088658931, lon: -75.35213634741464 },
  arenales: { lat: 4.919985282750272, lon: -75.35527240417512 },
  valleLunar: { lat: 4.918099804883675, lon: -75.35748927188513 },
  valleTumbas: { lat: 4.908941693623378, lon: -75.35354216596245 },
};

function mercatorY(lat: number): number {
  const s = Math.sin((lat * Math.PI) / 180);
  return Math.log((1 + s) / (1 - s)) / 2;
}

/** A coordinate as 0..1 of the map box (Web Mercator, like the tiles it was traced from). */
export function mapPoint(lat: number, lon: number): { x: number; y: number } {
  const { north, south, west, east } = TRAIL_MAP.bounds;
  const top = mercatorY(north);
  return {
    x: (lon - west) / (east - west),
    y: (top - mercatorY(lat)) / (top - mercatorY(south)),
  };
}

/** A map point (north-up, 0..1) where the turned map shows it. */
export function viewPoint({ x, y }: { x: number; y: number }): { x: number; y: number } {
  return { x: 1 - x, y: 1 - y };
}

/** Stops in route order, 0..1 of the map as shown (south-up). */
export const STATION_NODES: readonly { id: StationId; x: number; y: number }[] = STATION_IDS.map(
  (id) => ({ id, ...viewPoint(mapPoint(STATION_COORDS[id].lat, STATION_COORDS[id].lon)) }),
);

export function isStationId(value: string): value is StationId {
  return (STATION_IDS as readonly string[]).includes(value);
}
