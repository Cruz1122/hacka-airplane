import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

import { validateAssets, type KnowledgeFollowup } from '../assets';
import { fixture, loadAssets, loadVectors } from '../__fixtures__/load';
import { KnowledgeEngine, KnowledgeEngineError } from '../engine';
import type { Reranker } from '../rerank';
import { canRerank, identityReranker } from '../rerank';
import { retrieve } from '../retrieve';
import { detectSafety } from '../safety';
import type { KnowledgeReply } from '../types';

interface Row {
  q: string;
  vector: number[];
  pool: string[];
  cos: number[];
}
const fx = fixture<{ vectors_sha256: string; rows: Row[] }>('retrieval.json');
// The shipped T can sit below every fixture cosine (export_nlu.py fits T = 0: never abstain), so these
// tests pin T at the fixture's median top cosine to exercise both sides of the threshold.
const loaded = loadAssets();
const medianTop = [...fx.rows.map((r) => r.cos[0])].sort((a, b) => a - b)[fx.rows.length >> 1];
const assets = { ...loaded, policy: { ...loaded.policy, T: medianTop } };
const vectors = loadVectors(fx.vectors_sha256);
const { policy } = assets;
const byId = new Map(assets.catalog.map((e) => [e.id, e]));
const E = new Set(policy.emergency_direct);
const line = byId.get(policy.emergency_line_id)!;

const calm = fx.rows.filter((r) => {
  const s = detectSafety(r.q);
  return !s.urgent && !s.liveStatus;
});
const above = calm.find((r) => r.cos[0] >= policy.T)!;
const below = calm.find((r) => r.cos[0] < policy.T)!;
const emergencyNotFirst = fx.rows.find(
  (r) => !E.has(r.pool[0]) && r.pool.slice(0, 5).some((id) => E.has(id)),
)!;

/** Fake embedder: the text is looked up in a table of query vectors; unknown text throws. */
function fakeEmbed(table: Record<string, Row>) {
  const calls: string[] = [];
  const embed = async (text: string) => {
    calls.push(text);
    const row = table[text];
    if (!row) throw new Error(`no vector for ${text}`);
    return Float32Array.from(row.vector);
  };
  return { embed, calls };
}

const failingEmbed = async (): Promise<Float32Array> => {
  throw new Error('embedder offline');
};

function expectAbstain(r: KnowledgeReply): Extract<KnowledgeReply, { type: 'abstain' }> {
  if (r.type !== 'abstain') throw new Error(`expected abstain, got ${r.type}`);
  return r;
}
function expectAnswer(r: KnowledgeReply): Extract<KnowledgeReply, { type: 'answer' }> {
  if (r.type !== 'answer') throw new Error(`expected answer, got ${r.type}`);
  return r;
}

const URGENT = 'me perdí en el páramo y ya está oscureciendo';
const LIVE = '¿hoy está abierta la vía a Brisas?';

describe('KnowledgeEngine.ask top-1 policy', () => {
  it('fixture has the rows these tests need', () => {
    expect(above && below && emergencyNotFirst).toBeTruthy();
    expect(detectSafety(URGENT).urgent).toBe(true);
    expect(detectSafety(LIVE)).toMatchObject({ urgent: false, liveStatus: true });
  });

  it('passes the raw text to embed and answers with the top-1 entry, verbatim, when cos0 >= T', async () => {
    const { embed, calls } = fakeEmbed({ [above.q]: above });
    const res = await new KnowledgeEngine(assets, vectors, embed).ask(above.q);
    expect(calls).toEqual([above.q]);
    const a = expectAnswer(res.reply);
    const e = byId.get(above.pool[0])!;
    expect(a.banner).toBeUndefined();
    expect(a.id).toBe(above.pool[0]);
    expect(a.title).toBe(e.menu_label || e.label);
    expect(a.text).toBe(e.short);
    expect(a.sources).toEqual(
      e.sources.map((s) => ({
        title: s.label,
        ...(s.url ? { url: s.url } : {}),
        ...(s.retrieved_at ? { date: s.retrieved_at } : {}),
      })),
    );
    expect(a.reviewed).toBe(e.last_verified ?? undefined);
    expect(res.retrieval?.pool).toEqual(above.pool);
    for (const k of ['rulesMs', 'embedMs', 'retrieveMs', 'rerankMs', 'totalMs'] as const) {
      expect(res.timing[k]).toBeGreaterThanOrEqual(0);
    }
  });

  it('abstains with the policy text when cos0 < T', async () => {
    const { embed } = fakeEmbed({ [below.q]: below });
    const a = expectAbstain((await new KnowledgeEngine(assets, vectors, embed).ask(below.q)).reply);
    expect(a).toEqual({ type: 'abstain', text: policy.texts.abstain });
  });

  it('urgent: curated 123 banner over the best emergency entry of the pool, no threshold', async () => {
    const { embed } = fakeEmbed({ [URGENT]: emergencyNotFirst });
    const res = await new KnowledgeEngine(assets, vectors, embed).ask(URGENT);
    const a = expectAnswer(res.reply);
    expect(a.banner).toEqual({ kind: 'urgent_safety', text: line.short, sourceIds: [line.id] });
    const pool = res.retrieval!.pool;
    expect(a.id).toBe(pool.find((id) => E.has(id)));
    expect(pool[0]).not.toBe(a.id);
  });

  it('urgent with no emergency entry in the pool answers with the curated 123 line', async () => {
    const noEmergency = fx.rows.find((r) => r.pool.every((id) => !E.has(id)))!;
    const { embed } = fakeEmbed({ [URGENT]: noEmergency });
    const res = await new KnowledgeEngine(assets, vectors, embed).ask(URGENT);
    expect(res.retrieval!.pool.some((id) => E.has(id))).toBe(false);
    expect(expectAnswer(res.reply).id).toBe(policy.emergency_line_id);
  });

  it('urgent wins over live status', async () => {
    const q = 'hoy me perdí, ¿está abierta la vía?';
    const { embed } = fakeEmbed({ [q]: above });
    const a = expectAnswer((await new KnowledgeEngine(assets, vectors, embed).ask(q)).reply);
    expect(a.banner?.kind).toBe('urgent_safety');
  });

  it('urgent still answers with the 123 entry under the banner when embed throws', async () => {
    const res = await new KnowledgeEngine(assets, vectors, failingEmbed).ask(URGENT);
    const a = expectAnswer(res.reply);
    expect(a.banner?.kind).toBe('urgent_safety');
    expect(a.id).toBe(policy.emergency_line_id);
    expect(res.error).toBeInstanceOf(KnowledgeEngineError);
    expect(res.retrieval).toBeUndefined();
  });

  it('urgent still shows the banner when retrieve throws (bad vector)', async () => {
    const embed = async () => new Float32Array(3);
    const res = await new KnowledgeEngine(assets, vectors, embed).ask(URGENT);
    expect(expectAnswer(res.reply).banner?.kind).toBe('urgent_safety');
    expect(res.error?.message).toMatch(/dims/);
  });

  it('rethrows with the cause when nothing needs a banner', async () => {
    await expect(new KnowledgeEngine(assets, vectors, failingEmbed).ask(above.q)).rejects.toThrow(
      /Knowledge retrieval failed: embedder offline/,
    );
  });

  it('live status: offline banner above the normal answer or abstain', async () => {
    const { embed } = fakeEmbed({ [LIVE]: above });
    const a = expectAnswer((await new KnowledgeEngine(assets, vectors, embed).ask(LIVE)).reply);
    expect(a.banner).toEqual({
      kind: 'offline_current_status',
      text: policy.texts.offline_status,
      sourceIds: [],
    });
    expect(a.id).toBe(above.pool[0]);

    const low = fakeEmbed({ [LIVE]: below });
    const ab = expectAbstain((await new KnowledgeEngine(assets, vectors, low.embed).ask(LIVE)).reply);
    expect(ab.banner?.kind).toBe('offline_current_status');

    const failed = await new KnowledgeEngine(assets, vectors, failingEmbed).ask(LIVE);
    expect(expectAbstain(failed.reply).banner?.kind).toBe('offline_current_status');
    expect(failed.error).toBeInstanceOf(KnowledgeEngineError);
  });

  it('empty input abstains without calling the embedder', async () => {
    const { embed, calls } = fakeEmbed({});
    expectAbstain((await new KnowledgeEngine(assets, vectors, embed).ask('   ')).reply);
    expect(calls).toEqual([]);
  });

  it('flattens list-of-paragraph steps into strings', async () => {
    // The NLU export ships no steps (the natural reply carries them); give the 123 entry list steps.
    // Urgent with no model answers policy.emergency_line_id.
    const withSteps = { ...line, steps: [['Llama al 123.', 'Di dónde estás.'], 'Espera.'] };
    const custom = {
      ...assets,
      catalog: assets.catalog.map((e) => (e.id === line.id ? withSteps : e)),
    };
    const res = await new KnowledgeEngine(custom, vectors, failingEmbed).ask(URGENT);
    const a = expectAnswer(res.reply);
    expect(a.steps).toEqual(withSteps.steps.map((st) => (Array.isArray(st) ? st.join(' ') : st)));
    expect(a.steps!.every((st) => typeof st === 'string')).toBe(true);
  });
});

describe('KnowledgeEngine reranker seam (Laya; off in policy.laya)', () => {
  const reverse = (extra: Partial<Reranker> = {}): Reranker & { calls: number } => {
    const r = {
      id: 'reverse',
      calls: 0,
      rerank: async (_q: string, pool: string[]) => {
        r.calls++;
        return [...pool].reverse();
      },
      ...extra,
    };
    return r;
  };

  it('uses the reranked top-1, but the threshold stays on the e5 top cosine', async () => {
    const { embed } = fakeEmbed({ [above.q]: above, [below.q]: below });
    const engine = new KnowledgeEngine(assets, vectors, embed, reverse());
    const res = await engine.ask(above.q);
    expect(res.rerankedBy).toBe('reverse');
    expect(expectAnswer(res.reply).id).toBe(above.pool[above.pool.length - 1]);
    expectAbstain((await engine.ask(below.q)).reply);
  });

  it('identity reranker keeps the e5 top-1', async () => {
    const { embed } = fakeEmbed({ [above.q]: above });
    const res = await new KnowledgeEngine(assets, vectors, embed, identityReranker).ask(above.q);
    expect(expectAnswer(res.reply).id).toBe(above.pool[0]);
  });

  it('is skipped when a pool id is outside its training catalog', async () => {
    const catalogIds = new Set(above.pool.slice(1));
    expect(canRerank(above.pool, catalogIds)).toBe(false);
    expect(canRerank(above.pool, new Set(above.pool))).toBe(true);
    const rr = reverse({ catalogIds });
    const { embed } = fakeEmbed({ [above.q]: above });
    const res = await new KnowledgeEngine(assets, vectors, embed, rr).ask(above.q);
    expect(rr.calls).toBe(0);
    expect(res.rerankedBy).toBeUndefined();
    expect(expectAnswer(res.reply).id).toBe(above.pool[0]);
  });

  it('falls back to e5 order, with an error, when the reranker throws or drops ids', async () => {
    const { embed } = fakeEmbed({ [above.q]: above });
    const bad: Reranker[] = [
      { id: 'throws', rerank: async () => Promise.reject(new Error('onnx failed')) },
      { id: 'drops', rerank: async (_q, pool) => pool.slice(1) },
      { id: 'invents', rerank: async (_q, pool) => ['made.up', ...pool.slice(1)] },
    ];
    for (const rr of bad) {
      const res = await new KnowledgeEngine(assets, vectors, embed, rr).ask(above.q);
      expect(expectAnswer(res.reply).id).toBe(above.pool[0]);
      expect(res.error?.message).toMatch(rr.id === 'throws' ? /onnx failed/ : /reordering/);
    }
  });
});

describe('KnowledgeEngine follow-up context (policy.followup)', () => {
  const words = (q: string) => q.trim().split(/\s+/).length;
  const SHORT = 'y eso?';
  const FOLLOWUP: KnowledgeFollowup = { w: 0.5, max_words: 3, below: 0.5 };
  const withFollowup = (followup: KnowledgeFollowup | null) => ({
    ...assets,
    policy: { ...policy, followup },
  });
  const idx = validateAssets(assets, vectors);
  // A second confident calm row, long enough not to count as a follow-up by length.
  const longConfident = calm.find(
    (r) => r !== above && words(r.q) > FOLLOWUP.max_words && r.cos[0] >= FOLLOWUP.below,
  )!;
  const table = { [above.q]: above, [SHORT]: below, [longConfident.q]: longConfident, [URGENT]: below };

  it('fixture has the rows these tests need', () => {
    expect(longConfident).toBeTruthy();
    expect(detectSafety(SHORT)).toMatchObject({ urgent: false, liveStatus: false });
    expect(words(SHORT)).toBeLessThanOrEqual(FOLLOWUP.max_words);
  });

  it('a short follow-up fuses the previous scores; the first turn never does', async () => {
    const engine = new KnowledgeEngine(withFollowup(FOLLOWUP), vectors, fakeEmbed(table).embed);
    const first = await engine.ask(above.q);
    expect(first.contextUsed).toBe(false);
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(true);
    const q = Float32Array.from(below.vector);
    const fused = retrieve(q, idx, undefined, { scores: first.retrieval!.scores, w: FOLLOWUP.w });
    expect(res.retrieval!.scores).toEqual(fused.scores);
    expect(res.retrieval!.pool).toEqual(fused.pool);
    expect(res.retrieval!.scores).not.toEqual(retrieve(q, idx).scores);
  });

  it("mode 'concat' blends the scores of '<previous text> <this text>' embedded together", async () => {
    const CONCAT = { mode: 'concat' as const, w: 1, max_words: 5, below: 0 };
    const joined = `${above.q} ${SHORT}`;
    // Any row on another topic than SHORT's own vector stands in for the joined text's embedding.
    const other = fx.rows.find((r) => r.pool[0] !== below.pool[0] && r !== above)!;
    const { embed, calls } = fakeEmbed({ ...table, [joined]: other });
    const engine = new KnowledgeEngine(withFollowup(CONCAT), vectors, embed);
    await engine.ask(above.q);
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(true);
    expect(calls).toEqual([above.q, SHORT, joined]);
    const own = retrieve(Float32Array.from(below.vector), idx);
    const ctx = retrieve(Float32Array.from(other.vector), idx).scores;
    const want = retrieve(Float32Array.from(below.vector), idx, undefined, { scores: ctx, w: 1 });
    expect(res.retrieval!.scores).toEqual(want.scores);
    expect(res.retrieval!.scores).not.toEqual(own.scores);
    engine.resetContext();
    expect((await engine.ask(SHORT)).contextUsed).toBe(false);
  });

  it("mode 'concat' chains a fused turn's context into the next follow-up", async () => {
    const CONCAT = { mode: 'concat' as const, w: 1, max_words: 5, below: 0 };
    const other = fx.rows.find((r) => r.pool[0] !== below.pool[0] && r !== above)!;
    const second = `${above.q} ${SHORT}`;
    const third = `${above.q} ${SHORT} ${SHORT}`;
    const { embed, calls } = fakeEmbed({ ...table, [second]: other, [third]: other });
    const engine = new KnowledgeEngine(withFollowup(CONCAT), vectors, embed);
    await engine.ask(above.q);
    await engine.ask(SHORT);
    expect((await engine.ask(SHORT)).contextUsed).toBe(true);
    expect(calls).toEqual([above.q, SHORT, second, SHORT, third]);
  });

  it('with a cue pattern, a short confident question stands alone and a connective fuses', async () => {
    const CUE = { ...FOLLOWUP, max_words: 50, below: 0, cue: '^[¿¡\\s]*(?:y|con|eso)(?=[\\s?,.!]|$)' };
    const engine = new KnowledgeEngine(withFollowup(CUE), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    expect((await engine.ask(longConfident.q)).contextUsed).toBe(false); // short, but confident
    expect((await engine.ask(SHORT)).contextUsed).toBe(true); // 'y eso?' opens with a connective
    expect(() => validateAssets(withFollowup({ ...CUE, cue: '(' }), vectors)).toThrow(/followup.cue/);
  });

  it('a long, confidently matched message is scored on its own', async () => {
    const engine = new KnowledgeEngine(withFollowup(FOLLOWUP), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    const res = await engine.ask(longConfident.q);
    expect(res.contextUsed).toBe(false);
    expect(res.retrieval!.pool).toEqual(longConfident.pool);
  });

  it('a long message whose own top cosine is below `below` fuses', async () => {
    const lowBar = { ...FOLLOWUP, below: 2 }; // every cosine is below 2
    const engine = new KnowledgeEngine(withFollowup(lowBar), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    expect((await engine.ask(longConfident.q)).contextUsed).toBe(true);
  });

  it('T does not apply to a fused follow-up (it continues a park topic)', async () => {
    const engine = new KnowledgeEngine(withFollowup(FOLLOWUP), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(true);
    expect(expectAnswer(res.reply).id).toBe(res.retrieval!.pool[0]);
    engine.resetContext();
    const alone = await engine.ask(SHORT); // same text, standalone: below T, abstains
    expect(below.cos[0]).toBeLessThan(policy.T);
    expect(alone.reply.type).toBe('abstain');
  });

  it('resetContext stops fusion for the next turn', async () => {
    const engine = new KnowledgeEngine(withFollowup(FOLLOWUP), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    engine.resetContext();
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(false);
    expect(res.retrieval!.pool).toEqual(below.pool);
  });

  it('followup null never fuses', async () => {
    const engine = new KnowledgeEngine(withFollowup(null), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(false);
    expect(res.retrieval!.pool).toEqual(below.pool);
  });

  it('a failed embed keeps the stored context', async () => {
    let fail = false;
    const { embed } = fakeEmbed(table);
    const flaky = async (t: string) => (fail ? failingEmbed() : embed(t));
    const engine = new KnowledgeEngine(withFollowup(FOLLOWUP), vectors, flaky);
    const first = await engine.ask(above.q);
    fail = true;
    await expect(engine.ask(longConfident.q)).rejects.toThrow(/embedder offline/);
    fail = false;
    const res = await engine.ask(SHORT);
    expect(res.contextUsed).toBe(true);
    const q = Float32Array.from(below.vector);
    const w = FOLLOWUP.w;
    expect(res.retrieval!.scores).toEqual(
      retrieve(q, idx, undefined, { scores: first.retrieval!.scores, w }).scores,
    );
  });

  it('urgent turns keep their own pool', async () => {
    const lowBar = { ...FOLLOWUP, below: 2 };
    const engine = new KnowledgeEngine(withFollowup(lowBar), vectors, fakeEmbed(table).embed);
    await engine.ask(above.q);
    const res = await engine.ask(URGENT);
    expect(res.contextUsed).toBe(false);
    expect(res.retrieval!.pool).toEqual(below.pool);
    expect(expectAnswer(res.reply).banner?.kind).toBe('urgent_safety');
  });
});

describe('knowledge path isolation', () => {
  it('no module under src/core/knowledge imports the FSM, world.json or React', () => {
    const dir = join(__dirname, '..');
    const files = readdirSync(dir).filter((f) => f.endsWith('.ts'));
    expect(files.length).toBeGreaterThan(5);
    for (const f of files) {
      const src = readFileSync(join(dir, f), 'utf8');
      expect(src).not.toMatch(
        /world\.json|from '\.\.\/(world|driver|states|tools|guards|prompts)'|from 'react/,
      );
      expect(src).not.toMatch(/\.normalize\(|toLocaleLowerCase|\.at\(|Intl\./);
    }
  });
});
