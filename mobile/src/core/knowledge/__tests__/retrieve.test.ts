import { KnowledgeAssetError, validateAssets } from '../assets';
import { fixture, loadAssets, loadVectors } from '../__fixtures__/load';
import { RetrievalInputError, retrieve } from '../retrieve';

interface RetrievalRow {
  q: string;
  vector: number[];
  pool: string[];
  cos: number[];
  gates?: string[]; // export_knowledge.py only; export_nlu.py gates every section
  fused_top?: string; // export_nlu.py: top entry after fusing the previous row's scores
  fused_cos?: number;
}
interface RetrievalFixture {
  corpus_sha256: string;
  vectors_sha256: string;
  w?: number;
  rows: RetrievalRow[];
}

const fx = fixture<RetrievalFixture>('retrieval.json');
const assets = loadAssets();
const vectors = loadVectors(fx.vectors_sha256);
const idx = validateAssets(assets, vectors);

describe('retrieve parity with the Python exporter (retrieval.json)', () => {
  it('fixture, manifest and vectors come from the same export', () => {
    expect(fx.corpus_sha256).toBe(assets.manifest.corpus_sha256);
    expect(fx.vectors_sha256).toBe(assets.manifest.vectors.sha256);
    expect(fx.rows.length).toBeGreaterThan(0);
  });

  it.each(fx.rows.map((r, i) => [i, r.q, r] as const))('%i %s', (_i, _q, row) => {
    const got = retrieve(Float32Array.from(row.vector), idx);
    if (row.gates) expect(got.gates).toEqual(row.gates);
    expect(got.pool).toEqual(row.pool);
    // The fixture rounds the query to 7 decimals and cos to 6.
    got.cos.forEach((c, i) => expect(Math.abs(c - row.cos[i])).toBeLessThan(1e-5));
  });

  const fused = fx.rows.map((r, i) => [i, r] as const).filter(([, r]) => r.fused_top);
  (fused.length ? it : it.skip)('fuses the previous turn like Python (follow-up)', () => {
    for (const [i, row] of fused) {
      const prev = retrieve(Float32Array.from(fx.rows[i - 1].vector), idx).scores;
      const got = retrieve(Float32Array.from(row.vector), idx, undefined, { scores: prev, w: fx.w! });
      expect(got.pool[0]).toBe(row.fused_top);
      expect(Math.abs(got.cos[0] - row.fused_cos!)).toBeLessThan(1e-5);
    }
  });

  it('rejects a wrong-sized or non-finite query vector', () => {
    expect(() => retrieve(new Float32Array(idx.dims - 1), idx)).toThrow(RetrievalInputError);
    const bad = Float32Array.from(fx.rows[0].vector);
    bad[3] = NaN;
    expect(() => retrieve(bad, idx)).toThrow(RetrievalInputError);
  });

  it('validateAssets rejects vectors that do not match the manifest', () => {
    expect(() => validateAssets(assets, vectors.subarray(0, vectors.length - idx.dims))).toThrow(
      KnowledgeAssetError,
    );
  });

  it('runs fast enough in Node (micro benchmark, logged)', () => {
    const qs = fx.rows.slice(0, 40).map((r) => Float32Array.from(r.vector));
    for (const q of qs.slice(0, 5)) retrieve(q, idx); // warm-up
    const t0 = performance.now();
    for (const q of qs) retrieve(q, idx);
    const ms = (performance.now() - t0) / qs.length;
    process.stdout.write(
      `retrieve: ${ms.toFixed(2)} ms/query over ${assets.manifest.rows} x ${idx.dims} (Node ${process.version}, JIT; Hermes not measured)\n`,
    );
    expect(ms).toBeLessThan(200);
  });
});
