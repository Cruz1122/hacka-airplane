import { createHash } from 'node:crypto';

import { fromByteArray } from 'base64-js';
import { zlibSync } from 'fflate';

import type { CatalogEntry, KnowledgeAssets } from '../assets';
import { KnowledgeEngine } from '../engine';
import {
  collectKnowledgeQr, encodeKnowledgePatch, encodeKnowledgeQrSeries, parseKnowledgePatch,
  utf8Bytes, type KnowledgePatch,
} from '../qrPatch';

function entry(id: string, section: string, short: string): CatalogEntry {
  return { id, section, kind: 'faq', label: id, menu_label: id, short, steps: [], sources: [], last_verified: null };
}

const assets: KnowledgeAssets = {
  catalog: [entry('geography.original', 'geography', 'original'), entry('health_safety.123', 'health_safety', '123')],
  sections: [
    { id: 'geography', title: 'Geography', featured: [], order: 0, top_k: 5 },
    { id: 'health_safety', title: 'Safety', featured: [], order: 1, top_k: 5 },
  ],
  policy: {
    version: 'test', T: 0.6, k: 2, min_pool: 2, max_sections: 2, delta: 1,
    texts: { abstain: '?', offline_status: 'offline' },
    emergency_direct: ['health_safety.123'], emergency_line_id: 'health_safety.123',
    laya: { enabled: false, model: '', mode: '', catalog_sha256: null },
    continuation: {
      cue: '^sigue$', why_cue: '^por que$', max_words: 2, bridges: ['También.'],
      texts: { no_state: 'Sin tema', exhausted: 'No hay más' },
    },
  },
  manifest: {
    embedder: { file: 'test' }, prefix: 'query: ', rows: 4, dims: 2, text_rows: 2,
    row_entry: [0, 1], section_rows: ['geography', 'health_safety'], entry_section: [0, 1],
    vectors: { file: 'test', bytes: 32, sha256: '', dtype: 'float32' }, corpus_sha256: '',
  },
};

const encode = async () => Float32Array.of(1, 0);
const bank = Float32Array.of(0, 1, 0, -1, 0, 1, 0, -1);
const baseScore = async () => Float32Array.of(0, 0, 0, 0);
const patch: KnowledgePatch = {
  id: 'geography.mirador', revision: 1, op: 'put',
  entry: {
    section: 'geography', title: 'Mirador', answer: 'Vista de páramo.',
    questions: ['¿Dónde está el mirador?', 'Háblame del mirador'],
    variants: ['Desde el mirador se ve el páramo.'],
    steps: ['Usa el sendero señalizado.'],
    more: ['Lleva abrigo.'], why: ['El viento enfría el mirador.'],
    related: ['geography.original'], sources: [{ label: 'Parque', url: 'https://example.org/parque' }],
  },
};

test('QR text round-trips Spanish, questions, variants and removal without vectors', () => {
  const raw = encodeKnowledgePatch(patch);
  expect(parseKnowledgePatch(raw)).toEqual(patch);
  expect(parseKnowledgePatch(encodeKnowledgePatch({ op: 'remove', id: patch.id, revision: 2 }))).toEqual({
    op: 'remove', id: patch.id, revision: 2,
  });
  expect(() => parseKnowledgePatch('https://example.org')).toThrow('no es una actualización');
  expect(() => parseKnowledgePatch('NEVADOS1:' + 'ñ'.repeat(850))).toThrow('tamaño');
});

test('the overlay works with the native scorer and survives restart, replacement and deletion', async () => {
  let snapshot: string | null = null;
  const storage = { read: async () => snapshot, write: async (value: string) => { snapshot = value; } };
  const embed = jest.fn(encode);
  const make = () => new KnowledgeEngine(assets, bank, embed, undefined, baseScore, { seed: 5 });
  const live = make();
  await live.restorePatches(storage);
  await expect(live.applyPatch(patch)).resolves.toBe('applied');
  expect(embed.mock.calls).toHaveLength(2);
  await expect(live.applyPatch(patch)).resolves.toBe('duplicate');
  expect((await live.ask('mirador')).reply).toMatchObject({ id: patch.id, sources: [{ title: 'Parque' }] });
  expect((await live.ask('por qué')).reply).toMatchObject({ id: patch.id, text: 'El viento enfría el mirador.' });
  expect((await live.ask('sigue')).reply).toMatchObject({ id: patch.id, text: 'Lleva abrigo.' });
  expect((await live.ask('sigue')).reply).toMatchObject({ id: 'geography.original' });

  const restarted = make();
  await restarted.restorePatches(storage);
  expect((await restarted.ask('mirador')).reply).toMatchObject({ id: patch.id });
  if (patch.op !== 'put') throw new Error('expected put fixture');
  await restarted.applyPatch({ ...patch, revision: 2, entry: { ...patch.entry, answer: 'Nueva versión.', variants: [] } });
  expect((await restarted.ask('mirador')).reply).toMatchObject({ id: patch.id, text: 'Nueva versión.' });
  await restarted.applyPatch({ id: patch.id, revision: 3, op: 'remove' });
  await expect(restarted.applyPatch(patch)).rejects.toThrow('revisión igual o más reciente');
  const removed = make();
  await removed.restorePatches(storage);
  expect((await removed.ask('mirador', patch.id)).reply).toMatchObject({ type: 'abstain' });
  await expect(removed.applyPatch({ id: 'health_safety.123', revision: 4, op: 'remove' })).rejects.toThrow('seguridad');
});

test('a failed write never publishes the staged entry', async () => {
  const engine = new KnowledgeEngine(assets, bank, encode);
  await engine.restorePatches({ read: async () => null, write: async () => { throw new Error('disk full'); } });
  await expect(engine.applyPatch(patch)).rejects.toThrow('disk full');
  expect((await engine.ask('mirador')).reply).toMatchObject({ type: 'abstain' });
});


test('compresses a Spanish entry above the old QR limit and recovers every field', () => {
  if (patch.op !== 'put') throw new Error('Expected put fixture');
  const addition = 'En este páramo se ven frailejones, lagunas andinas y caminos de roca volcánica. ';
  const large: KnowledgePatch = {
    ...patch,
    entry: {
      ...patch.entry,
      answer: addition.repeat(7).trim(),
      variants: Array.from({ length: 6 }, (_, i) => ('Vista ' + (i + 1) + '. ' + addition.repeat(12)).trim()),
      more: [addition.repeat(4).trim()],
      why: [('Por la altitud. ' + addition).repeat(3).trim()],
    },
  };
  if (large.op !== 'put') throw new Error('Expected put fixture');
  expect(large.entry.variants.every((variant) => variant.length > 400)).toBe(true);
  expect(utf8Bytes('NEVADOS1:' + JSON.stringify(large)).length).toBeGreaterThan(1500);
  const code = encodeKnowledgePatch(large);
  expect(code).toMatch(/^NEVADOS2:[A-Za-z0-9_-]+$/);
  expect(code.length).toBeLessThan(1500);
  expect(parseKnowledgePatch(code)).toEqual(large);
  expect(parseKnowledgePatch('NEVADOS1:' + JSON.stringify(patch))).toEqual(patch);
});

test('rejects corrupted compressed data and caps decompression', () => {
  const oversized = fromByteArray(zlibSync(utf8Bytes(' '.repeat(33_000) + JSON.stringify(patch))))
    .split('+').join('-').split('/').join('_').replace(/=+$/, '');
  expect(() => parseKnowledgePatch('NEVADOS2:' + oversized)).toThrow('dañado');
  expect(() => parseKnowledgePatch('NEVADOS2:@')).toThrow('dañado');
  const damaged = zlibSync(utf8Bytes(JSON.stringify(patch)));
  damaged[damaged.length - 1] ^= 1;
  const code = fromByteArray(damaged).split('+').join('-').split('/').join('_').replace(/=+$/, '');
  expect(() => parseKnowledgePatch('NEVADOS2:' + code)).toThrow('dañado');
});

test('collects compact QR parts out of order and rejects other series before applying anything', () => {
  if (patch.op !== 'put') throw new Error('Expected put fixture');
  const variant = Array.from({ length: 25 }, (_, i) =>
    createHash('sha256').update(String(i)).digest('hex'),
  ).join(' ');
  const entries: KnowledgePatch[] = [
    { ...patch, entry: { ...patch.entry, variants: [variant] } },
    { id: 'geography.original', revision: 2, op: 'remove' },
  ];
  const codes = encodeKnowledgeQrSeries(entries);
  expect(codes.length).toBeGreaterThan(1);
  expect(codes.every((code) => code.length <= 540)).toBe(true);
  const last = collectKnowledgeQr(codes[codes.length - 1]);
  if (!('series' in last)) throw new Error('Expected more parts');
  expect(collectKnowledgeQr(codes[codes.length - 1], last.series)).toEqual(last);
  expect(() => collectKnowledgeQr(encodeKnowledgeQrSeries([patch])[0], last.series)).toThrow('otra actualización');
  let result = last as ReturnType<typeof collectKnowledgeQr>;
  for (const code of codes.slice(0, -1).reverse()) {
    if (!('series' in result)) throw new Error('Expected more parts');
    result = collectKnowledgeQr(code, result.series);
  }
  expect(result).toEqual({ patches: entries });
  expect(collectKnowledgeQr(encodeKnowledgePatch(patch))).toEqual({ patches: [patch] });
});

test('does not save a partial batch and updates the answer behind existing query vectors', async () => {
  if (patch.op !== 'put') throw new Error('Expected put fixture');
  const edit: KnowledgePatch = {
    ...patch, id: 'geography.original',
    entry: { ...patch.entry, answer: 'La respuesta editada.', variants: [], related: [] },
  };
  const score = async () => Float32Array.of(1, 0, 1, 0);
  const embed = async (query: string) => {
    if (query === 'pregunta inválida') throw new Error('embedding failed');
    if (query === 'pregunta anterior') return Float32Array.of(0, 1);
    return encode();
  };
  const engine = new KnowledgeEngine(assets, bank, embed, undefined, score);
  const write = jest.fn(async () => {});
  await engine.restorePatches({ read: async () => null, write });
  const broken: KnowledgePatch = {
    ...patch, entry: { ...patch.entry, questions: ['pregunta inválida'] },
  };
  await expect(engine.applyPatches([edit, broken])).rejects.toThrow('embedding failed');
  expect(write).not.toHaveBeenCalled();
  expect((await engine.ask('pregunta anterior')).reply).toMatchObject({ text: 'original' });
  await expect(engine.applyPatches([edit])).resolves.toBe(1);
  expect((await engine.ask('pregunta anterior')).reply).toMatchObject({ text: 'La respuesta editada.' });
});
