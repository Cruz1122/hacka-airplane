// The "Solo información verificada por UTON" mask (AskOptions.verifiedOnly) on the synthetic
// knowledge base: 6 entries, one unit vector each, k = 5, T = 0.5, "sigue" depth on every entry.
import { QUESTION, synthAssets } from '../__fixtures__/depth_synth';
import type { KnowledgeFollowup } from '../assets';
import { KnowledgeEngine } from '../engine';
import type { Reranker } from '../rerank';
import { detectSafety } from '../safety';
import type { KnowledgeReply } from '../types';

const ABSTAIN_VERIFIED = 'no esta en el guion';
const URGENT = 'auxilio el no respira que hago';
/** Every entry above T, f.zeta last: the k = 5 pool leaves it out. */
const GRADED = 'pregunta graduada';
const GRADES = [0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0, 0];

function engineOf(
  verified: readonly string[],
  {
    abstainVerified = true,
    reranker,
    followup = null,
  }: { abstainVerified?: boolean; reranker?: Reranker; followup?: KnowledgeFollowup | null } = {},
) {
  const s = synthAssets();
  const flagged = new Set(verified);
  const assets = {
    ...s.assets,
    catalog: s.assets.catalog.map((e) => ({ ...e, verified_by_uton: flagged.has(e.id) })),
    policy: {
      ...s.assets.policy,
      followup,
      texts: {
        ...s.assets.policy.texts,
        ...(abstainVerified ? { abstain_verified: ABSTAIN_VERIFIED } : {}),
      },
    },
  };
  const embed = (text: string) =>
    text === GRADED ? Promise.resolve(Float32Array.from(GRADES)) : s.embed(text);
  return new KnowledgeEngine(assets, s.vectors, embed, reranker, undefined, { seed: 3 });
}

function answer(r: KnowledgeReply): Extract<KnowledgeReply, { type: 'answer' }> {
  if (r.type !== 'answer') throw new Error(`expected an answer, got: ${r.text}`);
  return r;
}

const verifiedOnly = { verifiedOnly: true };

describe('verifiedOnly retrieval', () => {
  test('a verified entry ranked below k still answers, with its canonical text', async () => {
    const res = await engineOf(['f.zeta']).ask(GRADED, verifiedOnly);
    expect(res.retrieval?.pool).toHaveLength(5);
    expect(res.retrieval?.pool).not.toContain('f.zeta');
    const a = answer(res.reply);
    expect(a.id).toBe('f.zeta');
    expect(a.text).toBe('canonical f.zeta'); // not one of its L0 paraphrases
    expect(a.verified).toBe(true);
  });

  test('the reranker sees the verified pool and its scores', async () => {
    const rerank = jest.fn(async (_q: string, pool: string[]) => pool);
    await engineOf(['e.eps', 'f.zeta'], { reranker: { id: 'spy', rerank } }).ask(
      GRADED,
      verifiedOnly,
    );
    expect(rerank).toHaveBeenCalledWith(GRADED, ['e.eps', 'f.zeta'], [0.75, 0.7].map(Math.fround));
  });

  test('abstains with abstain_verified when no verified entry clears T', async () => {
    const e = engineOf(['f.zeta']);
    expect((await e.ask(QUESTION['a.alpha'], verifiedOnly)).reply).toEqual({
      type: 'abstain',
      text: ABSTAIN_VERIFIED,
    });
  });

  test('falls back to the plain abstain text in exports without abstain_verified', async () => {
    const e = engineOf(['f.zeta'], { abstainVerified: false });
    expect((await e.ask(QUESTION['a.alpha'], verifiedOnly)).reply).toEqual({
      type: 'abstain',
      text: 'no se',
    });
  });
});

describe('verifiedOnly follow-up fusion', () => {
  // Pins today's rule (brief: keep contextUsed): a fused turn has no T floor, so after an
  // abstain a short follow-up answers the best verified entry, however weak its own score.
  test('a fused follow-up answers the top verified entry with no T floor', async () => {
    const e = engineOf(['f.zeta'], { followup: { w: 0.5, max_words: 3, below: 0.5 } });
    expect((await e.ask(QUESTION['a.alpha'], verifiedOnly)).reply.text).toBe(ABSTAIN_VERIFIED);
    const res = await e.ask('y eso', verifiedOnly);
    expect(res.contextUsed).toBe(true);
    expect(answer(res.reply).id).toBe('f.zeta');
  });
});

describe('verifiedOnly bypasses', () => {
  test('an urgent turn ignores the mask: banner and emergency answer', async () => {
    expect(detectSafety(URGENT).urgent).toBe(true);
    const a = answer((await engineOf(['a.alpha']).ask(URGENT, verifiedOnly)).reply);
    expect(a.banner?.kind).toBe('urgent_safety');
    expect(['c.gamma', 'd.delta']).toContain(a.id);
    expect(a.verified).toBe(false);
  });

  test('the urgent banner tops an unverified emergency answer even with no model', async () => {
    const s = synthAssets();
    const e = new KnowledgeEngine(s.assets, s.vectors, () => Promise.reject(new Error('off')));
    const res = await e.ask(URGENT, verifiedOnly);
    expect(answer(res.reply)).toMatchObject({ id: 'c.gamma', banner: { kind: 'urgent_safety' } });
  });
});

describe('verifiedOnly answer paths', () => {
  test('a photo entry answers only when verified', async () => {
    const e = engineOf(['f.zeta']);
    const unverified = await e.ask('dime que es esto', {
      visualEntryId: 'b.beta',
      ...verifiedOnly,
    });
    expect(unverified.reply.text).toBe(ABSTAIN_VERIFIED);
    const a = answer(
      (await e.ask('dime que es esto', { visualEntryId: 'f.zeta', ...verifiedOnly })).reply,
    );
    expect(a).toMatchObject({ id: 'f.zeta', text: 'canonical f.zeta', verified: true });
    // The caption path keeps the verified photo entry as its fallback.
    const caption = await e.ask('algo raro', {
      visualEntryId: 'f.zeta',
      preferCaption: true,
      ...verifiedOnly,
    });
    expect(answer(caption.reply).id).toBe('f.zeta');
  });

  test('"sigue" serves no depth layer and walks to verified entries only', async () => {
    // a.alpha walks to b.beta then e.eps; only e.eps is verified.
    const e = engineOf(['a.alpha', 'e.eps']);
    const first = answer((await e.ask(QUESTION['a.alpha'], verifiedOnly)).reply);
    expect(first.text).toBe('canonical a.alpha');
    const walk = answer((await e.ask('sigue', verifiedOnly)).reply);
    expect(walk.id).toBe('e.eps');
    expect(walk.text).toMatch(/^(Relacionado:|Aparte:) canonical e\.eps$/);
    expect((await e.ask('sigue', verifiedOnly)).reply).toEqual({
      type: 'abstain',
      text: 'No tengo más detalle verificado sobre esto. Prueba con Tema e.eps.',
    });
  });

  test('"por qué" serves no why layer: it retrieves under the mask', async () => {
    const e = engineOf(['a.alpha']);
    await e.ask(QUESTION['a.alpha'], verifiedOnly);
    expect((await e.ask('por que', verifiedOnly)).reply.text).toBe(ABSTAIN_VERIFIED);
  });
});

describe('default mode', () => {
  const turns = [QUESTION['a.alpha'], 'sigue', 'por que', 'sigue', GRADED, QUESTION['b.beta']];

  test('the flags change nothing but the seal', async () => {
    const flagged = engineOf(['a.alpha', 'f.zeta']);
    const plain = engineOf([]);
    const seals: [string, boolean][] = [];
    for (const q of turns) {
      const x = (await flagged.ask(q)).reply;
      const y = (await plain.ask(q)).reply;
      if (x.type !== 'answer' || y.type !== 'answer') {
        expect(x).toEqual(y);
        continue;
      }
      expect({ ...x, verified: y.verified }).toEqual(y);
      seals.push([x.id, x.verified]);
    }
    expect(seals.length).toBeGreaterThanOrEqual(4);
    for (const [id, sealed] of seals) expect(sealed).toBe(['a.alpha', 'f.zeta'].includes(id));
  });

  test('verifiedOnly: false is the default', async () => {
    const a = engineOf(['f.zeta']);
    const b = engineOf(['f.zeta']);
    for (const q of turns) {
      expect((await a.ask(q, { verifiedOnly: false })).reply).toEqual((await b.ask(q)).reply);
    }
  });

  test('a verified entry answers with the seal and its L0 rotation', async () => {
    const a = answer((await engineOf(['a.alpha']).ask(QUESTION['a.alpha'])).reply);
    expect(a.verified).toBe(true);
    expect(a.text).toMatch(/^A0 /);
  });
});
