import type { KnowledgeContinuation } from '../assets';
import { Rotation, cueMatcher, factKey, newState, pickLayer, seededRandom } from '../continuation';
import { KnowledgeEngine } from '../engine';
import { fixture } from '../__fixtures__/load';
import { DEPTH, QUESTION, continuationPolicy, synthAssets } from '../__fixtures__/depth_synth';
import type { KnowledgeReply } from '../types';

// ---- detector: the REAL cue exported by export_nlu.py (__fixtures__/continuation.json) ----------

const real = fixture<KnowledgeContinuation>('continuation.json');
const m = cueMatcher(real);

const MORE = [
  'sigue',
  'Sigue',
  'SIGUE',
  '¡sigue!',
  'sigue.',
  'siga',
  'sigamos',
  'sige',
  'sigeu',
  'sigu',
  'siguie',
  'siegue',
  'sgue',
  'siguee',
  'sigueee',
  'continua',
  'continúa',
  'continuar',
  'continue',
  'continúe',
  'contina',
  'cotinua',
  'contnua',
  'kontinua',
  'mas',
  'más',
  'MÁS',
  'mass',
  'más!',
  '¿más?',
  'maz',
  'que mas',
  'qué más',
  'ke mas',
  'q mas',
  'y que mas',
  'y qué más',
  'y mas',
  'cuéntame más',
  'cuentame mas',
  'cuentame mas detalles',
  'dime más',
  'dime mas info',
  'dame más',
  'dame más detalles',
  'más detalle',
  'más detalles',
  'mas informacion',
  'más datos',
  'con más detalle',
  'un poco más',
  'explícame mejor',
  'explicame mejor',
  'explica mejor',
  'explícalo mejor',
  'amplía',
  'amplia',
  'amplía eso',
  'ampliar',
  'profundiza',
  'detalla',
  'ok sigue',
  'bueno, sigue',
  'dale sigue',
  'sí, sigue',
  'sigue por favor',
  'sigue porfa',
  'sigue gracias',
  'ok gracias sigue',
  'más por favor',
  'continua por favor',
  'siga pues',
  'quiero saber más',
  'y sigue',
];

const NOT_MORE = [
  '¿sigue abierto?',
  'sigue abierto',
  'sigue lloviendo',
  '¿sigue cerrado el parque?',
  'sigue vigente la alerta',
  'más o menos cuánto',
  'más o menos cuanto cuesta',
  'más cerca de Pereira',
  'más cerca de Manizales',
  'mas barato',
  'más económico',
  'más información sobre la entrada al parque nevado',
  'que más hay para hacer en el parque',
  'qué más puedo ver',
  'hay más guías',
  '¿hay algo más barato?',
  'cuánto más',
  'mucho más frío',
  'a qué hora sigue el bus',
  'sigue el sendero',
  'sigue la vía en mal estado',
  'sigue siendo peligroso',
  'cuando más gente',
  'más temprano',
  'más tarde',
  'mas alto que el ruiz',
  'continua el camino hasta la laguna',
  'continuación del sendero',
  'el cierre continua',
  'si sigue abierto',
  'y si sigue lloviendo',
  'más de tres dias',
  'mas de 4000 metros',
  'donde queda el nevado',
  'hola',
  'gracias',
  'ok',
  'no',
  'cuéntame del páramo',
  'dime el precio',
  'dime cómo llegar',
  'explícame cómo reservar',
  'amplía la reserva de grupos',
  'detalla el costo de la entrada',
];

const WHY = [
  'por qué',
  'por que',
  '¿Por qué?',
  'porque',
  'y por qué',
  'por qué eso',
  'pq',
  'xq',
  'por ke',
];
const NOT_WHY = [
  'por qué cierran el parque',
  'por qué es tan caro',
  'porque hace frío',
  'por favor',
];

describe('continuation cue (real exported pattern)', () => {
  test('has the table sizes the brief asks for', () => {
    expect(MORE.length).toBeGreaterThanOrEqual(40);
    expect(NOT_MORE.length).toBeGreaterThanOrEqual(40);
  });

  test.each(MORE)('positive: %s', (q) => {
    expect(m.match(q)).toBe('more');
  });

  test.each(NOT_MORE)('near-miss: %s', (q) => {
    expect(m.match(q)).toBeNull();
  });

  test.each(WHY)('why: %s', (q) => {
    expect(m.match(q)).toBe('why');
  });

  test.each(NOT_WHY)('not why: %s', (q) => {
    expect(m.match(q)).toBeNull();
  });

  test('more than max_words words never matches, even if every word is a cue', () => {
    expect(m.match('sigue sigue sigue sigue sigue sigue sigue')).toBeNull();
  });
});

// ---- rotation ---------------------------------------------------------------------------------

describe('Rotation', () => {
  test('a full cycle serves every index once, in a seeded order', () => {
    const r = new Rotation(seededRandom(7));
    const first = Array.from({ length: 8 }, () => r.take('k', 8));
    expect([...first].sort()).toEqual([0, 1, 2, 3, 4, 5, 6, 7]);
    const again = new Rotation(seededRandom(7));
    expect(Array.from({ length: 8 }, () => again.take('k', 8))).toEqual(first);
  });

  test('wrap-around never starts with the index just served', () => {
    for (let seed = 0; seed < 200; seed++) {
      const r = new Rotation(seededRandom(seed));
      let last = -1;
      for (let i = 0; i < 40; i++) {
        const x = r.take('k', 3);
        expect(x).not.toBe(last);
        last = x;
      }
    }
  });

  test('a filter is honoured and the last index is still avoided', () => {
    const r = new Rotation(seededRandom(1));
    const ok = (i: number) => i === 2 || i === 5;
    const got = Array.from({ length: 10 }, () => r.take('k', 8, ok));
    expect(new Set(got)).toEqual(new Set([2, 5]));
    got.slice(1).forEach((x, i) => expect(x).not.toBe(got[i]));
  });
});

// ---- engine on the synthetic knowledge base ---------------------------------------------------

type Setup = ReturnType<typeof synthAssets>;

function engineOf(
  seed: number,
  opts?: Parameters<typeof synthAssets>[0],
): { e: KnowledgeEngine } & Setup {
  const s = synthAssets(opts);
  const e = new KnowledgeEngine(s.assets, s.vectors, s.embed, undefined, undefined, { seed });
  return { e, ...s };
}

const text = (r: KnowledgeReply) => r.text;
const ask = async (e: KnowledgeEngine, q: string) => (await e.ask(q)).reply;
const fx = (id: string) => QUESTION[id];

describe('state machine', () => {
  test('a cue with no last answer asks for the topic and does not embed (R4.4)', async () => {
    const { e, embedCalls } = engineOf(1);
    const r = await ask(e, 'sigue');
    expect(r).toEqual({ type: 'abstain', text: '¿Sobre qué tema?' });
    expect(embedCalls).toEqual([]);
  });

  test('answer -> sigue never embeds and is served from the layers (R4.1)', async () => {
    const { e, embedCalls } = engineOf(1);
    await ask(e, fx('b.beta'));
    const n = embedCalls.length;
    const r1 = await ask(e, 'sigue');
    const r2 = await ask(e, 'Más');
    expect(embedCalls.length).toBe(n);
    expect(r1.type === 'answer' && r1.id).toBe('b.beta');
    expect(text(r1)).toMatch(/^B how/);
    expect(text(r2)).toMatch(/^B spec/);
  });

  test('layers -> walk with a bridge -> exhausted with two related labels (R4.2, R4.3)', async () => {
    const { e } = engineOf(3);
    await ask(e, fx('b.beta'));
    await ask(e, 'sigue');
    await ask(e, 'sigue');
    const walk = await ask(e, 'sigue');
    expect(walk.type === 'answer' && walk.id).toBe('e.eps');
    expect(text(walk)).toMatch(/^(Relacionado:|Aparte:) E0 /);
    const end = await ask(e, 'sigue');
    expect(end.type).toBe('abstain');
    expect(text(end)).toBe('No tengo más detalle verificado sobre esto. Prueba con Tema e.eps.');
    expect(text(await ask(e, 'sigue'))).toBe(text(end));
  });

  test('exhausted text names two related topics when the walk has them', async () => {
    const { e } = engineOf(5);
    await ask(e, fx('a.alpha'));
    for (let i = 0; i < 6; i++) await ask(e, 'sigue');
    const end = await ask(e, 'sigue');
    expect(text(end)).toBe(
      'No tengo más detalle verificado sobre esto. Prueba con Tema b.beta y Tema e.eps.',
    );
  });

  test('"por qué" serves the unserved why layer once, then falls to the normal path (R4.5)', async () => {
    const { e, embedCalls } = engineOf(2);
    await ask(e, fx('a.alpha'));
    const n = embedCalls.length;
    const why = await ask(e, 'por qué');
    expect(text(why)).toMatch(/^A why/);
    expect(embedCalls.length).toBe(n);
    await ask(e, 'por qué'); // no why layer left: embeds like any other turn
    expect(embedCalls.length).toBe(n + 1);
  });

  test('"por qué" without state or why layer is an ordinary turn', async () => {
    const { e, embedCalls } = engineOf(2);
    await ask(e, 'por qué');
    expect(embedCalls).toEqual(['por qué']);
  });

  test('a new question starts a fresh conversation on the new entry', async () => {
    const { e } = engineOf(4);
    await ask(e, fx('b.beta'));
    await ask(e, 'sigue');
    await ask(e, fx('a.alpha'));
    const r = await ask(e, 'sigue');
    expect(r.type === 'answer' && r.id).toBe('a.alpha');
  });

  test('prevText / follow-up context is untouched by continuation turns', async () => {
    const s = synthAssets();
    const policy = {
      ...s.assets.policy,
      followup: { mode: 'concat' as const, w: 1, max_words: 5, below: 0.7, cue: null },
    };
    const e = new KnowledgeEngine(
      { ...s.assets, policy },
      s.vectors,
      s.embed,
      undefined,
      undefined,
      { seed: 1 },
    );
    await e.ask(fx('b.beta'));
    await e.ask('sigue');
    s.embedCalls.length = 0;
    await e.ask(fx('a.alpha'));
    // The fused follow-up embeds "<previous user text> <this text>": the previous text is the
    // question, not "sigue".
    expect(s.embedCalls).toContain(`${fx('b.beta')} ${fx('a.alpha')}`);
  });
});

describe('R4.7: state is cleared', () => {
  const states: [string, (e: KnowledgeEngine) => Promise<unknown>][] = [
    ['urgent', (e) => e.ask('auxilio el no respira que hago')],
    ['abstain (off-topic)', (e) => e.ask('algo que no existe en la guia')],
    ['empty message', (e) => e.ask('   ')],
    ['reset', async (e) => e.resetContext()],
  ];
  test.each(states)('%s -> next "sigue" asks for the topic', async (_n, act) => {
    const { e } = engineOf(1);
    await ask(e, fx('b.beta'));
    await act(e);
    expect(text(await ask(e, 'sigue'))).toBe('¿Sobre qué tema?');
  });

  test('an urgent message is never read as a cue and keeps its banner', async () => {
    const { e } = engineOf(1);
    await ask(e, fx('b.beta'));
    const res = await e.ask('auxilio el no respira que hago');
    expect(res.safety.urgent).toBe(true);
    expect(res.reply.banner?.kind).toBe('urgent_safety');
    expect(res.reply.type).toBe('answer');
  });
});

describe('R4.6 / R6.5: same question again', () => {
  test('x8 gives 8 different texts, then wraps without repeating the last', async () => {
    for (const seed of [1, 2, 3]) {
      const { e } = engineOf(seed);
      const got: string[] = [];
      for (let i = 0; i < 24; i++) got.push(text(await ask(e, fx('a.alpha'))));
      expect(new Set(got.slice(0, 8)).size).toBe(8);
      expect(new Set(got.slice(8, 16)).size).toBe(8);
      got.slice(1).forEach((x, i) => expect(x).not.toBe(got[i]));
    }
  });

  test('two-paraphrase entry alternates', async () => {
    const { e } = engineOf(9);
    const got: string[] = [];
    for (let i = 0; i < 7; i++) got.push(text(await ask(e, fx('f.zeta'))));
    got.slice(1).forEach((x, i) => expect(x).not.toBe(got[i]));
  });

  test('the rotation survives resetContext (new chat)', async () => {
    const { e } = engineOf(5);
    const got: string[] = [];
    for (let i = 0; i < 3; i++) {
      got.push(text(await ask(e, fx('a.alpha'))));
      e.resetContext();
    }
    expect(new Set(got).size).toBe(3);
  });

  test('same seed, same texts (R7.7)', async () => {
    const run = async () => {
      const { e } = engineOf(42);
      const out: string[] = [];
      for (let i = 0; i < 6; i++) out.push(text(await ask(e, fx('a.alpha'))));
      for (let i = 0; i < 4; i++) out.push(text(await ask(e, 'sigue')));
      return out;
    };
    expect(await run()).toEqual(await run());
  });

  test('layers rotate across conversations on the same entry', async () => {
    const { e } = engineOf(6);
    const seen = new Set<string>();
    for (let round = 0; round < 4; round++) {
      await ask(e, fx('b.beta'));
      seen.add(text(await ask(e, 'sigue')));
      await ask(e, fx('e.eps')); // leave the entry so the next round starts fresh
    }
    expect(seen.size).toBe(2); // the two paraphrases of B's first layer
  });
});

describe('R6.6: emergency rotation', () => {
  test('only the doubly approved paraphrases are served', async () => {
    const { e } = engineOf(1);
    const got = new Set<string>();
    for (let i = 0; i < 12; i++) got.add(text(await ask(e, fx('c.gamma'))));
    expect(got).toEqual(new Set(['C0 uno', 'C0 tres', 'C0 cinco']));
  });

  test('fewer than 3 approved: canonical text, always', async () => {
    const { e } = engineOf(1);
    for (let i = 0; i < 4; i++) expect(text(await ask(e, fx('d.delta')))).toBe('canonical d.delta');
  });

  test('an urgent turn serves the emergency entry from its approved set', async () => {
    const { e } = engineOf(1);
    const r = await ask(e, 'auxilio el no respira que hago');
    expect(['C0 uno', 'C0 tres', 'C0 cinco']).toContain(text(r));
  });

  test('sigue does not serve an unapproved depth layer of an emergency entry', async () => {
    const s = synthAssets();
    s.assets.depth = {
      entries: {
        ...DEPTH,
        'c.gamma': {
          ...DEPTH['c.gamma'],
          layers: [{ kind: 'specifics', texts: [{ text: 'UNAPPROVED EMERGENCY LAYER', atoms: [] }] }],
        },
      },
    };
    const e = new KnowledgeEngine(s.assets, s.vectors, s.embed, undefined, undefined, { seed: 1 });
    await e.ask(fx('c.gamma'));
    expect(text(await ask(e, 'sigue'))).not.toBe('UNAPPROVED EMERGENCY LAYER');
  });
});

describe('A13: partial disclosure', () => {
  const COMPLEMENTS = new Set(DEPTH['a.alpha'].complements);

  test.each(Array.from({ length: 24 }, (_, i) => i + 1))('seed %i', async (seed) => {
    const { e } = engineOf(seed);
    const served = new Set<string>();
    const atomsOf = (t: string): string[] => {
      const all = [...DEPTH['a.alpha'].l0, ...DEPTH['a.alpha'].layers.flatMap((l) => l.texts)];
      return all.find((x) => x.text === t)?.atoms ?? [];
    };
    const first = text(await ask(e, fx('a.alpha')));
    const firstAtoms = atomsOf(first);
    expect(firstAtoms.length).toBeLessThan(COMPLEMENTS.size); // never all of them
    firstAtoms.forEach((a) => served.add(a));

    const shown = new Set([first]);
    for (let i = 0; i < 8; i++) {
      const r = await ask(e, 'sigue');
      const t = text(r);
      expect(shown.has(t)).toBe(false); // never repeats
      shown.add(t);
      if (r.type === 'abstain') break; // exhausted
      if (r.type === 'answer' && r.id !== 'a.alpha') continue; // walk: another entry
      const fresh = atomsOf(t).filter((a) => !served.has(a));
      expect(fresh.length).toBeGreaterThanOrEqual(1); // every sigue reveals something new
      fresh.forEach((a) => served.add(a));
    }
  });

  test('the first replies cover at least two different complement subsets', async () => {
    const { e } = engineOf(11);
    const subsets = new Set<string>();
    for (let i = 0; i < 8; i++) {
      const t = text(await ask(e, fx('a.alpha')));
      subsets.add(DEPTH['a.alpha'].l0.find((x) => x.text === t)!.atoms.join(','));
    }
    expect(subsets.size).toBeGreaterThanOrEqual(2);
  });

  test('a text that repeats a served complement is not chosen', () => {
    const d = {
      ...DEPTH['a.alpha'],
      layers: [
        {
          kind: 'specifics' as const,
          texts: [
            { text: 'fresh only', atoms: ['c1'] },
            { text: 'repeats', atoms: ['c1', 'c2', 'c3'] },
          ],
        },
      ],
    };
    const st = newState('a.alpha');
    st.served.add(factKey('a.alpha', 'c3'));
    st.served.add(factKey('a.alpha', 'c4'));
    const pick = pickLayer(d, st, () => 0);
    expect(pick).toBeDefined();
    const chosen = [...pick!.texts].map((i) => d.layers[pick!.layer].texts[i].text);
    expect(chosen).toEqual(['fresh only']);
  });

  test('a repeating text is used only when no fully new text reveals a complement', () => {
    const d = {
      ...DEPTH['a.alpha'],
      layers: [{ kind: 'specifics' as const, texts: [{ text: 'repeats', atoms: ['c1', 'c2', 'c3'] }] }],
    };
    const st = newState('a.alpha');
    st.served.add(factKey('a.alpha', 'c3'));
    const pick = pickLayer(d, st, () => 0);
    expect(pick).toBeDefined();
    expect(d.layers[pick!.layer].texts[[...pick!.texts][0]].text).toBe('repeats');
  });

  test('the text that adds the most unserved facts comes first', async () => {
    // L0 carrying c1,c2 -> "spec" (c3,c4: gain 2) beats "why" (c3: gain 1).
    for (let seed = 1; seed < 40; seed++) {
      const { e } = engineOf(seed);
      if (text(await ask(e, fx('a.alpha'))) !== 'A0 uno') continue;
      expect(text(await ask(e, 'sigue'))).toMatch(/^A spec/);
      return;
    }
    throw new Error('A0 uno never came up first');
  });
});

describe('null policy = today (R4.8)', () => {
  const nullish: [string, Setup][] = [
    ['continuation absent, depth present', synthAssets({ continuation: false, depth: true })],
    [
      'continuation null, depth present',
      (() => {
        const s = synthAssets({ continuation: true, depth: true });
        s.assets.policy = { ...s.assets.policy, continuation: null };
        return s;
      })(),
    ],
    ['neither', synthAssets({ continuation: false, depth: false })],
  ];

  test.each(nullish)('%s: replies are byte-identical to the plain engine', async (_n, s) => {
    const plain = synthAssets({ continuation: false, depth: false });
    const a = new KnowledgeEngine(s.assets, s.vectors, s.embed, undefined, undefined, { seed: 5 });
    const b = new KnowledgeEngine(plain.assets, plain.vectors, plain.embed);
    const turns = [
      fx('a.alpha'),
      'sigue',
      fx('a.alpha'),
      'más',
      fx('c.gamma'),
      'por qué',
      fx('d.delta'),
      'auxilio el no respira que hago',
      'algo que no existe en la guia',
      fx('b.beta'),
      fx('b.beta'),
    ];
    for (const q of turns) {
      const x = await a.ask(q);
      const y = await b.ask(q);
      expect(JSON.stringify(x.reply)).toBe(JSON.stringify(y.reply));
      expect(JSON.stringify(x.retrieval)).toBe(JSON.stringify(y.retrieval));
    }
  });

  test('"sigue" with the policy off goes through retrieval like any text', async () => {
    const s = synthAssets({ continuation: false });
    const e = new KnowledgeEngine(s.assets, s.vectors, s.embed);
    await e.ask('sigue');
    expect(s.embedCalls).toEqual(['sigue']);
  });
});

describe('asset validation', () => {
  const bad =
    (mut: (s: Setup) => void): (() => void) =>
    () => {
      const s = synthAssets();
      mut(s);
      new KnowledgeEngine(s.assets, s.vectors, s.embed);
    };

  test('continuation null ignores a depth block the old engine never read', () => {
    const s = synthAssets({ continuation: false, depth: true });
    s.assets.depth = { entries: { 'not-in-catalog': DEPTH['e.eps'] } };
    expect(() => new KnowledgeEngine(s.assets, s.vectors, s.embed)).not.toThrow();
  });

  test('a layer atom outside the complement inventory fails', () => {
    expect(
      bad((s) => {
        s.assets.depth = {
          entries: {
            'a.alpha': {
              ...DEPTH['a.alpha'],
              layers: [{ kind: 'why', texts: [{ text: 'rogue', atoms: ['not-a-complement'] }] }],
            },
          },
        };
      }),
    ).toThrow(/not-a-complement/);
  });

  test('a depth id outside the catalog fails', () => {
    expect(bad((s) => (s.assets.depth = { entries: { 'x.nope': DEPTH['e.eps'] } }))).toThrow(
      /x\.nope/,
    );
  });

  test('a walk id outside the catalog fails', () => {
    expect(
      bad(
        (s) => (s.assets.depth = { entries: { 'e.eps': { ...DEPTH['e.eps'], walk: ['x.nope'] } } }),
      ),
    ).toThrow(/walk id x\.nope/);
  });

  test('a walk to itself fails', () => {
    expect(
      bad(
        (s) => (s.assets.depth = { entries: { 'e.eps': { ...DEPTH['e.eps'], walk: ['e.eps'] } } }),
      ),
    ).toThrow(/walk id/);
  });

  test('an out-of-range emergency rotation index fails', () => {
    expect(
      bad(
        (s) =>
          (s.assets.depth = { entries: { 'c.gamma': { ...DEPTH['c.gamma'], rotation: [9] } } }),
      ),
    ).toThrow(/rotation/);
  });

  test('a broken cue fails', () => {
    expect(bad((s) => (s.assets.policy.continuation = continuationPolicy({ cue: '(' })))).toThrow(
      /continuation\.cue/,
    );
  });

  test('missing texts fail', () => {
    expect(
      bad((s) => (s.assets.policy.continuation = continuationPolicy({ bridges: [] }))),
    ).toThrow(/bridges/);
  });
});
