import {
  DEFAULT_ACCESS_HOURS,
  HOUR_MS,
  LOCKED_ACCESS,
  STATION_CODES,
  isKnowledgeOpen,
  isStationUnlocked,
  openUntilMs,
  parseAccessHours,
  parseParkAccess,
  parseStationCode,
  scanStation,
  stationCode,
  stationToScan,
} from '../parkAccess';

const DAY = 24 * HOUR_MS;

describe('station codes', () => {
  it('round-trips every station and uses distinct 10-char tokens', () => {
    for (const s of Object.keys(STATION_CODES) as (keyof typeof STATION_CODES)[]) {
      expect(parseStationCode(stationCode(s))).toBe(s);
      expect(STATION_CODES[s]).toMatch(/^[a-z0-9]{10}$/);
    }
    expect(new Set(Object.values(STATION_CODES)).size).toBe(4);
  });

  it('rejects other text, brisas, a wrong token and extra parts', () => {
    for (const bad of [
      '',
      'hola',
      'NEVADOS-ESTACION:brisas:abc',
      'NEVADOS-ESTACION:arenales:wrongtoken',
      `${stationCode('arenales')}:x`,
      'NEVADOS-ESTACION:arenales:' + STATION_CODES.valleLunar,
    ]) {
      expect(parseStationCode(bad)).toBeNull();
    }
    expect(parseStationCode(`  ${stationCode('valleLunar')}\n`)).toBe('valleLunar');
  });
});

describe('scanStation and stations', () => {
  it('starts with brisas and stations 1 and 2 open, 3 and 4 closed', () => {
    expect(isStationUnlocked(LOCKED_ACCESS, 'brisas')).toBe(true);
    expect(isStationUnlocked(LOCKED_ACCESS, 'aguacerales')).toBe(true);
    expect(isStationUnlocked(LOCKED_ACCESS, 'arenales')).toBe(true);
    expect(isStationUnlocked(LOCKED_ACCESS, 'valleLunar')).toBe(false);
    expect(isStationUnlocked(LOCKED_ACCESS, 'valleTumbas')).toBe(false);
  });

  it('scanning N opens N+1; arenales opens valleLunar only', () => {
    const s = scanStation(LOCKED_ACCESS, 'arenales', 10);
    expect(isStationUnlocked(s, 'valleLunar')).toBe(true);
    expect(isStationUnlocked(s, 'valleTumbas')).toBe(false);
  });

  it('is a monotonic max: valleLunar opens valleTumbas without arenales, and never goes back', () => {
    const s = scanStation(LOCKED_ACCESS, 'valleLunar', 10);
    expect(isStationUnlocked(s, 'valleTumbas')).toBe(true);
    const again = scanStation(s, 'aguacerales', 20);
    expect(again.reached).toBe(3);
    expect(again.openedAtMs).toBe(20);
  });

  it('valleTumbas QR only reopens the window', () => {
    const s = scanStation(LOCKED_ACCESS, 'valleTumbas', 5);
    expect(s).toEqual({ openedAtMs: 5, reached: 4 });
  });

  it('names the QR that unlocks a station', () => {
    expect(stationToScan('valleLunar')).toBe('arenales');
    expect(stationToScan('valleTumbas')).toBe('valleLunar');
    expect(stationToScan('aguacerales')).toBeNull();
  });
});

describe('knowledge window', () => {
  const s = scanStation(LOCKED_ACCESS, 'aguacerales', 1000);
  it('is closed before any scan', () => {
    expect(isKnowledgeOpen(LOCKED_ACCESS, 1000, DAY)).toBe(false);
    expect(openUntilMs(LOCKED_ACCESS, DAY)).toBeNull();
  });
  it('is open inside the window and closes at the edge', () => {
    expect(isKnowledgeOpen(s, 1000 + DAY - 1, DAY)).toBe(true);
    expect(isKnowledgeOpen(s, 1000 + DAY, DAY)).toBe(false);
  });
  it('follows the current threshold, since the opening time is stored', () => {
    expect(isKnowledgeOpen(s, 1000 + 2 * DAY, DAY)).toBe(false);
    expect(isKnowledgeOpen(s, 1000 + 2 * DAY, 3 * DAY)).toBe(true);
    expect(openUntilMs(s, 3 * DAY)).toBe(1000 + 3 * DAY);
  });
  it('is closed when the clock went back before the opening', () => {
    expect(isKnowledgeOpen(s, 500, DAY)).toBe(false);
  });
});

describe('stored values', () => {
  it('damaged access is locked', () => {
    for (const raw of [null, '', 'x', '[]', '{"openedAtMs":"a","reached":-1}']) {
      expect(parseParkAccess(raw)).toEqual(LOCKED_ACCESS);
    }
    expect(parseParkAccess('{"openedAtMs":7,"reached":9}')).toEqual({ openedAtMs: 7, reached: 4 });
  });
  it('threshold falls back to the default unless 1..72 integer', () => {
    expect(parseAccessHours('48')).toBe(48);
    for (const raw of [null, '0', '73', '1.5', 'abc', '-3']) {
      expect(parseAccessHours(raw)).toBe(DEFAULT_ACCESS_HOURS);
    }
  });
});
