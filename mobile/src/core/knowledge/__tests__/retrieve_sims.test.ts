import { validateAssets } from '../assets';
import { fixture, loadAssets, loadVectors } from '../__fixtures__/load';
import { RetrievalInputError, retrieve } from '../retrieve';

interface RetrievalFixture {
  vectors_sha256: string;
  rows: { q: string; vector: number[]; pool: string[]; gates: string[] }[];
}

const fx = fixture<RetrievalFixture>('retrieval.json');
const vectors = loadVectors(fx.vectors_sha256);
const idx = validateAssets(loadAssets(), vectors);
const nRows = vectors.length / idx.dims;

// What the native onnxruntime scorer (index_scorer.onnx, MatMul q x W) returns.
function nativeLikeSims(q: Float32Array): Float32Array {
  const out = new Float32Array(nRows);
  for (let r = 0; r < nRows; r++) {
    let acc = 0;
    for (let j = 0; j < idx.dims; j++) acc += vectors[r * idx.dims + j] * q[j];
    out[r] = acc;
  }
  return out;
}

describe('retrieve with precomputed similarities (native scorer path)', () => {
  it.each(fx.rows.slice(0, 40).map((r, i) => [i, r] as const))('row %i matches the JS path', (_i, row) => {
    const q = Float32Array.from(row.vector);
    const viaSims = retrieve(q, idx, nativeLikeSims(q));
    expect(viaSims.pool).toEqual(row.pool);
    expect(viaSims.gates).toEqual(retrieve(q, idx).gates);
  });

  it('rejects a similarity array of the wrong length', () => {
    const q = Float32Array.from(fx.rows[0].vector);
    expect(() => retrieve(q, idx, new Float32Array(10))).toThrow(RetrievalInputError);
  });
});
