// Brisas vehicle route stops. Press opens `/estacion/[id]`.

export const STATION_IDS = [
  'brisas',
  'aguacerales',
  'arenales',
  'valleLunar',
  'valleTumbas',
] as const;

export type StationId = (typeof STATION_IDS)[number];

/** Zigzag bottom (Brisas) to top; x/y are 0..1 of the map box. */
export const STATION_NODES: readonly { id: StationId; x: number; y: number }[] = [
  { id: 'brisas', x: 0.3, y: 0.88 },
  { id: 'aguacerales', x: 0.7, y: 0.68 },
  { id: 'arenales', x: 0.28, y: 0.47 },
  { id: 'valleLunar', x: 0.72, y: 0.27 },
  { id: 'valleTumbas', x: 0.36, y: 0.08 },
];

export function isStationId(value: string): value is StationId {
  return (STATION_IDS as readonly string[]).includes(value);
}
