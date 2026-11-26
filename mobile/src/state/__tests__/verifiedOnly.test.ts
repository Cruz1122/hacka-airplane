// jest.mock is hoisted: the store never touches the real kv-store.
jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: { getItemAsync: jest.fn(async () => null), setItemAsync: jest.fn(async () => {}) },
}));

type Store = typeof import('../verifiedOnly');
interface Kv {
  getItemAsync: jest.Mock<Promise<string | null>, [string]>;
  setItemAsync: jest.Mock<Promise<void>, [string, string]>;
}

/** A fresh store (it is module state) and the kv-store mock it writes to. */
function fresh(saved: string | null): { store: Store; kv: Kv } {
  let out!: { store: Store; kv: Kv };
  jest.isolateModules(() => {
    /* eslint-disable @typescript-eslint/no-require-imports -- isolateModules loads with require */
    const kv: Kv = require('expo-sqlite/kv-store').default;
    kv.getItemAsync.mockResolvedValue(saved);
    out = { store: require('../verifiedOnly'), kv };
    /* eslint-enable @typescript-eslint/no-require-imports */
  });
  return out;
}

const settle = () => new Promise((r) => setTimeout(r, 0));

describe('verified-only setting', () => {
  it('reads only a saved "true" as on', () => {
    const { store } = fresh(null);
    expect(store.parseVerifiedOnly('true')).toBe(true);
    for (const raw of [null, 'false', '1', 'yes', '']) {
      expect(store.parseVerifiedOnly(raw)).toBe(false);
    }
  });

  it('is off until the saved value loads, then follows it', async () => {
    const { store, kv } = fresh('true');
    expect(store.getVerifiedOnly()).toBe(false);
    await settle();
    expect(store.getVerifiedOnly()).toBe(true);
    expect(kv.getItemAsync).toHaveBeenCalledTimes(1);
    expect(kv.getItemAsync).toHaveBeenCalledWith('knowledge.verifiedOnly.v1');
  });

  it('saves a change once', () => {
    const { store, kv } = fresh(null);
    store.setVerifiedOnly(true);
    store.setVerifiedOnly(true);
    expect(store.getVerifiedOnly()).toBe(true);
    expect(kv.setItemAsync).toHaveBeenCalledTimes(1);
    expect(kv.setItemAsync).toHaveBeenCalledWith('knowledge.verifiedOnly.v1', 'true');
  });

  it('keeps a choice made before the saved value arrived', async () => {
    const { store } = fresh('true');
    store.loadVerifiedOnly();
    store.setVerifiedOnly(false);
    await settle();
    expect(store.getVerifiedOnly()).toBe(false);
  });
});
