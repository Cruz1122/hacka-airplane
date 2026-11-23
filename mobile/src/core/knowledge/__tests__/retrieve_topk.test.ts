import { KnowledgeAssetError, validateAssets, type KnowledgeAssets, type KnowledgePolicy } from '../assets';
import { fixture, loadAssets, loadVectors } from '../__fixtures__/load';
import { RetrievalInputError, retrieve } from '../retrieve';

const f = Math.fround;

// Tiny index: 2 dims, query [1, 0], every row [v, 0], so each row cosine is exactly f(v).
// s1 holds A (4 rows), B (2 rows, fewer than k = 3) and C (1 row); s2 holds D (3 rows).
const ROWS: Record<string, number[]> = {
  A: [0.1, 0.2, 0.3, 0.9],
  B: [0.5, 0.4],
  C: [0.7],
  D: [0.95, 0, 0],
};
const ENTRY_SECTION: Record<string, string> = { A: 's1', B: 's1', C: 's1', D: 's2' };
const IDS = Object.keys(ROWS);
const Q = Float32Array.from([1, 0]);

function tiny(policy: Partial<KnowledgePolicy> = {}): { assets: KnowledgeAssets; vectors: Float32Array } {
  const rowEntry = IDS.flatMap((id, n) => ROWS[id].map(() => n));
  const values = [...IDS.flatMap((id) => ROWS[id]), 0, 0]; // + description rows of s1, s2
  const vectors = new Float32Array(values.length * 2);
  values.forEach((v, r) => (vectors[r * 2] = v));
  const assets: KnowledgeAssets = {
    catalog: IDS.map((id) => ({
      id,
      section: ENTRY_SECTION[id],
      kind: 'faq',
      label: id,
      menu_label: id,
      short: id,
      steps: [],
      sources: [],
      last_verified: null,
    })),
    sections: ['s1', 's2'].map((id, order) => ({ id, order, title: id, top_k: 4, featured: [] })),
    policy: {
      version: 'test',
      T: 0.5,
      k: 4,
      min_pool: 1,
      max_sections: 2,
      delta: 1,
      emergency_direct: [],
      emergency_line_id: 'A',
      texts: { abstain: '', offline_status: '' },
      laya: { enabled: false, model: '', catalog_sha256: null, mode: '' },
      ...policy,
    },
    manifest: {
      embedder: {},
      prefix: 'query: ',
      dims: 2,
      rows: values.length,
      text_rows: rowEntry.length,
      row_entry: rowEntry,
      section_rows: ['s1', 's2'],
      entry_section: IDS.map((id) => (ENTRY_SECTION[id] === 's1' ? 0 : 1)),
      vectors: { file: '', bytes: 0, sha256: '', dtype: 'float32' },
      corpus_sha256: '',
    },
  };
  return { assets, vectors };
}

const idxOf = (policy: Partial<KnowledgePolicy> = {}) => {
  const { assets, vectors } = tiny(policy);
  return validateAssets(assets, vectors);
};
const byId = (scores: Float32Array) => Object.fromEntries(IDS.map((id, n) => [id, scores[n]]));
// What the native scorer returns: every row's dot product, float32.
const simsOf = (vectors: Float32Array, q: Float32Array, dims: number) => {
  const out = new Float32Array(vectors.length / dims);
  for (let r = 0; r < out.length; r++) {
    let acc = 0;
    for (let j = 0; j < dims; j++) acc += vectors[r * dims + j] * q[j];
    out[r] = acc;
  }
  return out;
};

describe('entry score = mean of the best score_topk row cosines', () => {
  it('k = 1 (and an absent score_topk) is the max row cosine', () => {
    const idx = idxOf();
    expect(idx.scoreTopK).toBe(1);
    const r = retrieve(Q, idx);
    expect(byId(r.scores)).toEqual({ A: f(0.9), B: f(0.5), C: f(0.7), D: f(0.95) });
    expect(r.pool).toEqual(['D', 'A', 'C', 'B']);
    expect(r.cos).toEqual([f(0.95), f(0.9), f(0.7), f(0.5)]);
  });

  it('k = 3 averages the best 3 in float32, best first; fewer rows average all of them', () => {
    const r = retrieve(Q, idxOf({ score_topk: 3 }));
    const s = byId(r.scores);
    expect(s.A).toBe(f(f(f(f(0.9) + f(0.3)) + f(0.2)) / 3));
    expect(s.A).toBeCloseTo((0.9 + 0.3 + 0.2) / 3, 6);
    expect(s.B).toBe(f(f(f(0.5) + f(0.4)) / 2)); // 2 rows < k
    expect(s.C).toBe(f(0.7)); // 1 row
    expect(s.D).toBe(f(f(0.95) / 3));
    expect(r.pool).toEqual(['C', 'A', 'B', 'D']);
    for (const v of r.scores) expect(v).toBe(f(v));
  });

  it('section gating stays on the max row cosine, not the entry mean', () => {
    // s2's best row (0.95) beats s1's (0.9) although every s1 entry outscores D under k = 3.
    const r = retrieve(Q, idxOf({ score_topk: 3, max_sections: 1, delta: 0.01 }));
    expect(r.gates).toEqual(['s2']);
    expect(r.pool).toEqual(['D']);
  });

  it('the native sims path gives the same float32 scores as the JS loop', () => {
    for (const score_topk of [1, 2, 3, 10]) {
      const { assets, vectors } = tiny({ score_topk });
      const idx = validateAssets(assets, vectors);
      const q = Float32Array.from([0.6, 0.8]);
      const js = retrieve(q, idx);
      const native = retrieve(q, idx, simsOf(vectors, q, 2));
      expect(native.scores).toEqual(js.scores);
      expect(native.pool).toEqual(js.pool);
      expect(native.cos).toEqual(js.cos);
      expect(native.gates).toEqual(js.gates);
    }
  });
});

describe('context fusion', () => {
  it("blends the previous turn's scores before gating and pooling", () => {
    const idx = idxOf();
    const prev = Float32Array.from([0, 1, 0, 0]); // the last turn was about B
    const r = retrieve(Q, idx, undefined, { scores: prev, w: 1 });
    expect(byId(r.scores)).toEqual({
      A: f(f(0.9) / 2),
      B: f(f(f(0.5) + 1) / 2),
      C: f(f(0.7) / 2),
      D: f(f(0.95) / 2),
    });
    expect(r.pool).toEqual(['B', 'D', 'A', 'C']);
    expect(r.cos[0]).toBe(r.scores[1]);
  });

  it('rounds w * c, the sum and the quotient to float32', () => {
    const idx = idxOf({ score_topk: 2 });
    const own = retrieve(Q, idx).scores;
    const prev = Float32Array.from([0.31, 0.77, 0.12, 0.66]);
    const w = 0.35;
    const r = retrieve(Q, idx, undefined, { scores: prev, w });
    own.forEach((s, n) => {
      expect(r.scores[n]).toBe(f(f(s + f(f(w) * prev[n])) / f(1 + w)));
    });
  });

  it('rejects context scores of the wrong length', () => {
    expect(() => retrieve(Q, idxOf(), undefined, { scores: new Float32Array(3), w: 1 })).toThrow(
      RetrievalInputError,
    );
  });
});

describe('validateAssets: score_topk and followup', () => {
  const problems = (policy: Partial<KnowledgePolicy>) => {
    const { assets, vectors } = tiny(policy);
    try {
      validateAssets(assets, vectors);
      return [];
    } catch (e) {
      if (!(e instanceof KnowledgeAssetError)) throw e;
      return e.problems;
    }
  };

  it('accepts valid values and a null or absent followup', () => {
    expect(problems({ score_topk: 3, followup: { w: 0.5, max_words: 0, below: -1 } })).toEqual([]);
    expect(problems({ score_topk: 1, followup: null })).toEqual([]);
    expect(problems({})).toEqual([]);
    expect(idxOf({ score_topk: 3 }).scoreTopK).toBe(3);
  });

  it.each([
    [{ score_topk: 0 }, /score_topk/],
    [{ score_topk: 1.5 }, /score_topk/],
    [{ followup: { w: 0, max_words: 3, below: 0.8 } }, /followup\.w/],
    [{ followup: { w: Infinity, max_words: 3, below: 0.8 } }, /followup\.w/],
    [{ followup: { w: 0.5, max_words: -1, below: 0.8 } }, /followup\.max_words/],
    [{ followup: { w: 0.5, max_words: 2.5, below: 0.8 } }, /followup\.max_words/],
    [{ followup: { w: 0.5, max_words: 3, below: NaN } }, /followup\.below/],
  ] as const)('rejects %j', (policy, re) => {
    expect(problems(policy).join('; ')).toMatch(re);
  });
});

describe('score_topk on the real index (retrieval.json vectors)', () => {
  const fx = fixture<{ vectors_sha256: string; rows: { vector: number[] }[] }>('retrieval.json');
  const vectors = loadVectors(fx.vectors_sha256);
  const assets = loadAssets();
  const idx3 = validateAssets({ ...assets, policy: { ...assets.policy, score_topk: 3 } }, vectors);
  const idx1 = validateAssets(assets, vectors);

  it('sims and JS paths agree under k = 3, and k = 3 never beats the k = 1 max', () => {
    for (const row of fx.rows.slice(0, 10)) {
      const q = Float32Array.from(row.vector);
      const js = retrieve(q, idx3);
      const native = retrieve(q, idx3, simsOf(vectors, q, idx3.dims));
      expect(native.pool).toEqual(js.pool);
      native.scores.forEach((s, n) => expect(Math.abs(s - js.scores[n])).toBeLessThan(1e-6));
      const max = retrieve(q, idx1).scores;
      js.scores.forEach((s, n) => expect(s).toBeLessThanOrEqual(max[n] + 1e-7));
    }
  });
});
