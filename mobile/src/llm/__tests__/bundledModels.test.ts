// ensureBundledModels against an in-memory file system: copies on a new stamp, skips on the same
// one, replaces stale side-loaded files, and does nothing on a debug build (no bundled stamp).
const mockFs = new Map<string, string>();
const mockCopies: string[] = [];

jest.mock('expo-file-system', () => {
  class File {
    uri: string;
    constructor(...parts: string[]) {
      this.uri = parts.join('/');
    }
    get exists() {
      return mockFs.has(this.uri);
    }
    async text() {
      return mockFs.get(this.uri)!;
    }
    async write(s: string) {
      mockFs.set(this.uri, s);
    }
    delete() {
      mockFs.delete(this.uri);
    }
    async copy(to: File) {
      mockCopies.push(this.uri);
      mockFs.set(to.uri, mockFs.get(this.uri)!);
    }
    async move(to: File) {
      mockFs.set(to.uri, mockFs.get(this.uri)!);
      mockFs.delete(this.uri);
      this.uri = to.uri;
    }
  }
  return { File, Paths: { document: 'doc' } };
});

const NAMES = ['e5.gguf', 'index.f32.bin'];

function bundle(stamp: string, content: string) {
  mockFs.set('asset:///models/models.sha256', stamp);
  for (const n of NAMES) mockFs.set(`asset:///models/${n}`, `${content}:${n}`);
}

async function load() {
  // A fresh module per call: each call is one app launch (the in-flight promise is per process).
  let ensure!: typeof import('../bundledModels').ensureBundledModels;
  jest.isolateModules(() => {
    // eslint-disable-next-line @typescript-eslint/no-require-imports -- isolateModules loads with require
    ensure = require('../bundledModels').ensureBundledModels;
  });
  await ensure(NAMES);
}

beforeEach(() => {
  mockFs.clear();
  mockCopies.length = 0;
});

test('debug build without bundled models leaves the side-loaded files alone', async () => {
  mockFs.set('doc/e5.gguf', 'side');
  await load();
  expect(mockCopies).toEqual([]);
  expect(mockFs.get('doc/e5.gguf')).toBe('side');
});

test('first launch copies every bundled file and the stamp', async () => {
  bundle('v1', 'new');
  await load();
  expect(mockFs.get('doc/e5.gguf')).toBe('new:e5.gguf');
  expect(mockFs.get('doc/index.f32.bin')).toBe('new:index.f32.bin');
  expect(mockFs.get('doc/models.sha256')).toBe('v1');
  expect([...mockFs.keys()].some((k) => k.endsWith('.part'))).toBe(false);
});

test('same stamp skips the copy; a new release replaces same-size stale files', async () => {
  bundle('v1', 'new');
  await load();
  mockCopies.length = 0;
  await load();
  expect(mockCopies).toEqual([]);

  bundle('v2', 'newer');
  await load();
  expect(mockFs.get('doc/e5.gguf')).toBe('newer:e5.gguf');
  expect(mockFs.get('doc/models.sha256')).toBe('v2');
});

test('a missing file is copied again even with a matching stamp', async () => {
  bundle('v1', 'new');
  await load();
  mockFs.delete('doc/index.f32.bin');
  await load();
  expect(mockFs.get('doc/index.f32.bin')).toBe('new:index.f32.bin');
});

test('a leftover .part from an interrupted copy is replaced', async () => {
  bundle('v1', 'new');
  mockFs.set('doc/e5.gguf.part', 'half');
  await load();
  expect(mockFs.get('doc/e5.gguf')).toBe('new:e5.gguf');
  expect(mockFs.has('doc/e5.gguf.part')).toBe(false);
});
