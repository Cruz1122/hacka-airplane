// jest.mock is hoisted above the import: the store never touches the real kv-store.
import { DEFAULT_LOOK, DEFAULT_LOOKS, parsePetLooks, wornBy } from '../petLook';

jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: { getItemAsync: jest.fn(async () => null), setItemAsync: jest.fn(async () => {}) },
}));

describe('parsePetLooks', () => {
  it('reads the guide and the visitor looks apart', () => {
    expect(
      parsePetLooks(
        '{"guide":{"accessory":"beanie","tint":"sun"},"visitor":{"accessory":"flower","tint":null}}',
      ),
    ).toEqual({
      guide: { accessory: 'beanie', tint: 'sun' },
      visitor: { accessory: 'flower', tint: null },
    });
  });

  it('falls back field by field on unknown or damaged values', () => {
    expect(parsePetLooks(null)).toEqual(DEFAULT_LOOKS);
    expect(parsePetLooks('not json')).toEqual(DEFAULT_LOOKS);
    expect(parsePetLooks('{"guide":{"accessory":"crown","tint":"sun"}}')).toEqual({
      guide: { accessory: 'role', tint: 'sun' },
      visitor: DEFAULT_LOOK,
    });
    expect(parsePetLooks('{"visitor":{"accessory":"flower","tint":"teal"}}').visitor).toEqual({
      accessory: 'flower',
      tint: null,
    });
  });
});

describe('wornBy', () => {
  it('wears the role hat by default, in its own colors', () => {
    expect(wornBy(DEFAULT_LOOK, 'guide')).toEqual({ accessory: 'guideHat', tint: 'ink' });
    expect(wornBy(DEFAULT_LOOK, 'visitor')).toEqual({ accessory: 'visitorCap', tint: 'sky' });
  });

  it('wears the chosen accessory and tint whatever the role, or nothing', () => {
    expect(wornBy({ accessory: 'beanie', tint: 'sun' }, 'guide')).toEqual({
      accessory: 'beanie',
      tint: 'sun',
    });
    expect(wornBy({ accessory: 'none', tint: 'sun' }, 'visitor')).toEqual({});
  });
});
