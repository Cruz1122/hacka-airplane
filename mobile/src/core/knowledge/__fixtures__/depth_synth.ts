// Tiny hand-written knowledge base for the "sigue" tests: 6 entries, unit-vector index, a stub
// embedder keyed by text. Test-only; never import from app code.
import type { DepthEntry, DepthText, KnowledgeAssets, KnowledgeContinuation } from '../assets';

export const IDS = ['a.alpha', 'b.beta', 'c.gamma', 'd.delta', 'e.eps', 'f.zeta'] as const;
const DIMS = 8;

const t = (text: string, ...atoms: string[]): DepthText => ({ text, atoms });

/** Two-word-different texts so no test can pass on an accidental repeat. */
const alphaL0 = [
  t('A0 uno', 'c1', 'c2'),
  t('A0 dos', 'c3', 'c4'),
  t('A0 tres', 'c1', 'c3'),
  t('A0 cuatro', 'c2', 'c4'),
  t('A0 cinco', 'c1', 'c4'),
  t('A0 seis', 'c2', 'c3'),
  t('A0 siete', 'c1'),
  t('A0 ocho', 'c4'),
];

export const DEPTH: Record<string, DepthEntry> = {
  'a.alpha': {
    l0: alphaL0,
    layers: [
      {
        kind: 'why',
        texts: [
          t('A why 1', 'c1', 'c2', 'c3'),
          t('A why 2', 'c1', 'c2', 'c3'),
          t('A why 3', 'c1', 'c2', 'c3'),
          t('A why 4', 'c1', 'c2', 'c3'),
        ],
      },
      { kind: 'specifics', texts: [t('A spec 1', 'c3', 'c4'), t('A spec 2', 'c3', 'c4')] },
    ],
    walk: ['b.beta', 'e.eps'],
    complements: ['c1', 'c2', 'c3', 'c4'],
  },
  // No complement inventory (a safety-like entry): layers go in order, atoms are empty.
  'b.beta': {
    l0: [t('B0 uno'), t('B0 dos'), t('B0 tres')],
    layers: [
      { kind: 'how', texts: [t('B how 1'), t('B how 2')] },
      { kind: 'specifics', texts: [t('B spec 1'), t('B spec 2')] },
    ],
    walk: ['e.eps'],
    complements: [],
  },
  // Emergency, 3 approved of 5.
  'c.gamma': {
    l0: [t('C0 uno'), t('C0 dos'), t('C0 tres'), t('C0 cuatro'), t('C0 cinco')],
    layers: [],
    walk: [],
    complements: [],
    rotation: [0, 2, 4],
  },
  // Emergency, only 1 approved: keeps the canonical text.
  'd.delta': {
    l0: [t('D0 uno'), t('D0 dos')],
    layers: [],
    walk: [],
    complements: [],
    rotation: [1],
  },
  'e.eps': { l0: [t('E0 uno'), t('E0 dos'), t('E0 tres')], layers: [], walk: [], complements: [] },
  'f.zeta': { l0: [t('F0 uno'), t('F0 dos')], layers: [], walk: [], complements: [] },
};

export const QUESTION: Record<string, string> = Object.fromEntries(
  IDS.map((id) => [id, `pregunta ${id}`]),
);

export function continuationPolicy(
  cue: Partial<KnowledgeContinuation> = {},
): KnowledgeContinuation {
  return {
    cue: '^(?:sigue|mas|que mas)$',
    max_words: 6,
    why_cue: '^por que$',
    bridges: ['Relacionado:', 'Aparte:'],
    texts: {
      no_state: '¿Sobre qué tema?',
      exhausted: 'No tengo más detalle verificado sobre esto.',
      related: 'Prueba con {topics}.',
    },
    ...cue,
  };
}

export function synthAssets(opts: { continuation?: boolean; depth?: boolean } = {}): {
  assets: KnowledgeAssets;
  vectors: Float32Array;
  embed: (text: string) => Promise<Float32Array>;
  embedCalls: string[];
} {
  const { continuation = true, depth = true } = opts;
  const catalog = IDS.map((id) => ({
    id,
    section: 's',
    kind: id.startsWith('c.') || id.startsWith('d.') ? ('emergency' as const) : ('faq' as const),
    label: `Tema ${id}`,
    menu_label: `Tema ${id}`,
    short: `canonical ${id}`,
    steps: [],
    sources: [{ label: `Fuente ${id}` }],
    last_verified: null,
  }));
  const rows = IDS.length + 1;
  const vectors = new Float32Array(rows * DIMS);
  for (let i = 0; i < rows; i++) vectors[i * DIMS + i] = 1;
  const assets: KnowledgeAssets = {
    catalog,
    sections: [{ id: 's', order: 0, title: 'S', top_k: IDS.length, featured: [] }],
    policy: {
      version: 'synthetic',
      T: 0.5,
      k: 5,
      min_pool: 1,
      max_sections: 1,
      delta: 2,
      score_topk: 1,
      followup: null,
      emergency_direct: ['c.gamma', 'd.delta'],
      emergency_line_id: 'c.gamma',
      ...(continuation ? { continuation: continuationPolicy() } : {}),
      texts: { abstain: 'no se', offline_status: 'sin conexion' },
      laya: { enabled: false, model: '', catalog_sha256: null, mode: 'reorder_only' },
    },
    manifest: {
      embedder: {},
      prefix: 'query: ',
      dims: DIMS,
      rows,
      text_rows: IDS.length,
      row_entry: IDS.map((_, i) => i),
      section_rows: ['s'],
      entry_section: IDS.map(() => 0),
      vectors: { file: 'x', bytes: vectors.byteLength, sha256: '', dtype: 'float32-le' },
      corpus_sha256: '',
    },
    ...(depth ? { depth: { entries: DEPTH } } : {}),
  };
  const embedCalls: string[] = [];
  const embed = async (text: string): Promise<Float32Array> => {
    embedCalls.push(text);
    const n = IDS.findIndex((id) => QUESTION[id] === text);
    const v = new Float32Array(DIMS);
    if (n >= 0) v[n] = 1;
    else v[DIMS - 1] = 1; // off-topic: only the section row matches
    return v;
  };
  return { assets, vectors, embed, embedCalls };
}
