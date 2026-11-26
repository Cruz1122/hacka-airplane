// Knowledge engine: safety rules -> e5 embedding -> retrieval -> optional reranker -> top-1 policy ->
// curated answer by id. Pure TS; the embedder and the vectors are injected.

import {
  validateAssets,
  type DepthEntry,
  type DepthText,
  type KnowledgeAssets,
  type KnowledgeContinuation,
  type KnowledgeFollowup,
  type LoadedIndex,
} from './assets';
import {
  bestTexts,
  cueMatcher,
  factKey,
  joinTopics,
  newState,
  pickLayer,
  Rotation,
  seededRandom,
  type ContinuationState,
  type CueKind,
  type CueMatcher,
} from './continuation';
import { answerFor, bannerFor, decide, policyContext, type PolicyContext } from './policy';
import { canRerank, isReordering, type Reranker } from './rerank';
import { rankEntries, retrieve, type RetrievalResult } from './retrieve';
import { clean } from './clean';
import { detectSafety, type SafetyResult } from './safety';
import type { Banner, KnowledgeReply, KnowledgeTiming } from './types';

export type Embed = (text: string) => Promise<Float32Array>;
/** Native scorer: all index-row dot products for a query vector (onnxruntime MatMul). */
export type Score = (queryVec: Float32Array) => Promise<Float32Array>;

export interface AskResult {
  reply: KnowledgeReply;
  timing: KnowledgeTiming;
  safety: SafetyResult;
  retrieval?: RetrievalResult; // absent when embedding or retrieval failed
  /** The retrieval fused the previous turn's scores (policy.followup). */
  contextUsed: boolean;
  rerankedBy?: string; // reranker id, when its order was used
  error?: Error; // a degraded path was taken (failed embed/retrieve under a banner, or a reranker failure)
}

export class KnowledgeEngineError extends Error {
  constructor(
    message: string,
    readonly cause: unknown,
  ) {
    super(cause instanceof Error ? `${message}: ${cause.message}` : message);
    this.name = 'KnowledgeEngineError';
  }
}

/** Short, or not confidently matched on its own: read it in the light of the previous turn. */
function isFollowup(text: string, ownTopCos: number, f: KnowledgeFollowup): boolean {
  const short = text.trim().split(/\s+/).length <= f.max_words;
  if (f.cue != null) return new RegExp(f.cue, 'iu').test(text) || (short && ownTopCos < f.below);
  return short || ownTopCos < f.below;
}

export interface AskOptions {
  /** A photo match's catalog entry: it answers unless `preferCaption`, then backs an abstain. */
  visualEntryId?: string;
  /** Retrieve on the caption first; the visual entry answers only when retrieval abstains. */
  preferCaption?: boolean;
  /**
   * Answer only from entries with `verified_by_uton` (the Settings switch). Urgent turns and the
   * 123 banner ignore it: an emergency answer is never suppressed.
   */
  verifiedOnly?: boolean;
}

/** What a turn may answer with: `verified` only the canonical text of UTON-verified entries. */
type Turn = 'calm' | 'urgent' | 'verified';

export interface KnowledgeEngineOptions {
  /** Seeds the paraphrase rotation and the tie-breaks (R7.7). Default: random per session. */
  seed?: number;
}

const CHAIN_WORDS = 60; // e5 reads 512 tokens; a follow-up chain stays far below that

const now = (): number => (typeof performance !== 'undefined' ? performance.now() : Date.now());

export class KnowledgeEngine {
  private readonly idx: LoadedIndex;
  private readonly ctx: PolicyContext;
  /** Entry scores of the last ask that produced a retrieval; the follow-up context. */
  private prevScores: Float32Array | undefined;
  private prevText: string | undefined; // previous user message (followup.mode 'concat')
  private readonly cont: KnowledgeContinuation | null;
  private readonly cue: CueMatcher | null;
  private readonly depth: Readonly<Record<string, DepthEntry>>;
  /** Paraphrase rotation: lives for the app session, so resetContext keeps it (R6.5). */
  private readonly rot: Rotation;
  private state: ContinuationState | undefined; // "sigue" conversation on one entry (R4)
  /** Catalog indexes of the UTON-verified entries that have index rows. */
  private readonly verifiedEntries: number[];
  /** Catalog index of each conversational entry (states no park fact) by id. */
  private readonly conversational: Map<string, number>;

  /**
   * @param vectors side-loaded index.f32.bin, rows x dims as the manifest says.
   * @param embed receives the user's text RAW; the embedder itself adds the e5 "query: " prefix
   *   (manifest.prefix) and returns the L2-normalised vector.
   * @param reranker optional reorderer (Laya); skipped for pools outside its catalogIds.
   * @param score optional native scorer; without it the JS dot-product loop runs (~0.46 s in Hermes).
   * @param options `seed` for the rotation; depth and "sigue" only run when policy.continuation is set.
   */
  constructor(
    assets: KnowledgeAssets,
    vectors: Float32Array,
    private readonly embed: Embed,
    private readonly reranker?: Reranker,
    private readonly score?: Score,
    options: KnowledgeEngineOptions = {},
  ) {
    this.idx = validateAssets(assets, vectors);
    this.ctx = policyContext(assets);
    this.cont = assets.policy.continuation ?? null;
    this.cue = this.cont ? cueMatcher(this.cont) : null;
    this.depth = this.cont ? (assets.depth?.entries ?? {}) : {};
    this.rot = new Rotation(seededRandom(options.seed ?? Math.floor(Math.random() * 2 ** 32)));
    this.verifiedEntries = assets.catalog.flatMap((e, n) =>
      e.verified_by_uton === true && this.idx.entryRows[n].length > 0 ? [n] : [],
    );
    this.conversational = new Map(
      assets.catalog.flatMap((e, n) => (e.conversational === true ? [[e.id, n] as const] : [])),
    );
  }

  async ask(text: string, options: AskOptions = {}): Promise<AskResult> {
    const { visualEntryId, preferCaption = false } = options;
    const t0 = now();
    // Rules first: they need no model, so a failing embedder cannot suppress the urgent notice.
    const safety = detectSafety(text);
    const banner = bannerFor(safety, this.ctx);
    const turn: Turn = safety.urgent ? 'urgent' : options.verifiedOnly ? 'verified' : 'calm';
    const timing: KnowledgeTiming = {
      rulesMs: now() - t0,
      embedMs: 0,
      retrieveMs: 0,
      rerankMs: 0,
      totalMs: 0,
    };
    let contextUsed = false;
    const done = (r: Omit<AskResult, 'timing' | 'safety' | 'contextUsed'>): AskResult => {
      timing.totalMs = now() - t0;
      return { ...r, timing, safety, contextUsed };
    };

    if (text.trim() === '') return done({ reply: this.abstain(banner, turn) });
    const visualFallback =
      visualEntryId &&
      this.ctx.byId.has(visualEntryId) &&
      turn !== 'urgent' &&
      (turn !== 'verified' || this.isVerified(visualEntryId))
        ? visualEntryId
        : undefined;
    if (visualFallback) {
      this.resetContext();
      if (!preferCaption) return done({ reply: this.answer(visualFallback, banner, turn) });
    }

    // Rules-only turn: no embedding. Urgent text never continues a conversation (R4.7).
    const kind = this.cue && turn !== 'urgent' ? this.cue.match(text) : null;
    const cont = kind ? this.continuation(kind, banner, turn) : undefined;
    if (cont) return done({ reply: cont });

    let retrieval: RetrievalResult;
    try {
      const t1 = now();
      // The index was embedded from filler-stripped texts (export_nlu.py), so the query is too.
      const prep = (t: string) => (this.ctx.policy.strip_fillers ? clean(t) : t);
      const vec = await this.embed(prep(text));
      const t2 = now();
      timing.embedMs = t2 - t1;
      const sims = this.score ? await this.score(vec) : undefined;
      retrieval = retrieve(vec, this.idx, sims);
      const f = this.ctx.policy.followup ?? null;
      const prev = f?.mode === 'concat' ? this.prevText : this.prevScores;
      // Urgent turns keep their own pool so a previous topic cannot push emergency entries out.
      if (
        f &&
        prev !== undefined &&
        !safety.urgent &&
        isFollowup(text, retrieval.cos[0] ?? -1, f)
      ) {
        let context: Float32Array;
        if (typeof prev === 'string') {
          const t3 = now();
          const cvec = await this.embed(prep(`${prev} ${text}`));
          timing.embedMs += now() - t3;
          context = retrieve(
            cvec,
            this.idx,
            this.score ? await this.score(cvec) : undefined,
          ).scores;
        } else {
          context = prev;
        }
        retrieval = retrieve(vec, this.idx, sims, { scores: context, w: f.w });
        contextUsed = true;
      }
      timing.retrieveMs = now() - t2 - (timing.embedMs - (t2 - t1));
      this.prevScores = retrieval.scores;
      // A fused follow-up carries its context on ("¿hay guías?" "¿son obligatorios?" "¿y dónde
      // los consigo?" keeps "guías"); the last CHAIN_WORDS words bound the embedded text.
      this.prevText = contextUsed
        ? `${this.prevText} ${text}`.trim().split(/\s+/).slice(-CHAIN_WORDS).join(' ')
        : text;
    } catch (cause) {
      const error = new KnowledgeEngineError('Knowledge retrieval failed', cause);
      if (visualFallback) return done({ reply: this.answer(visualFallback, banner, turn), error });
      if (!banner) throw error;
      // Urgent without a model: the curated 123 entry under the urgent banner.
      const reply =
        turn === 'urgent'
          ? this.answer(this.ctx.policy.emergency_line_id, banner, turn)
          : this.abstain(banner, turn);
      return done({ reply, error });
    }

    // Verified only: rank every verified entry by its final score. Cutting retrieval's k-pool
    // instead would abstain on a verified entry ranked below k. The context keeps every entry.
    // A conversational entry that tops the whole corpus joins them: it states no park fact, so an
    // off-topic question still gets "that is off topic" instead of the nearest guion entry. Only
    // as the overall top: as a runner-up ("no reliable clock" under "today's alert") it misleads.
    const topChat =
      retrieval.pool[0] === undefined ? undefined : this.conversational.get(retrieval.pool[0]);
    const ranked =
      turn === 'verified'
        ? rankEntries(
            retrieval.scores,
            this.idx.ids,
            topChat === undefined ? this.verifiedEntries : [...this.verifiedEntries, topChat],
            this.ctx.policy.k,
          )
        : retrieval;
    let order = ranked.pool;
    let rerankedBy: string | undefined;
    let error: Error | undefined;
    const rr = this.reranker;
    if (rr && (!rr.catalogIds || canRerank(order, rr.catalogIds))) {
      const t3 = now();
      try {
        const out = await rr.rerank(text, [...order], [...ranked.cos]);
        if (isReordering(out, order)) {
          order = out;
          rerankedBy = rr.id;
        } else {
          error = new Error(
            `Reranker ${rr.id} did not return a reordering of the pool; kept e5 order`,
          );
        }
      } catch (cause) {
        error = new KnowledgeEngineError(`Reranker ${rr.id} failed; kept e5 order`, cause);
      }
      timing.rerankMs = now() - t3;
    }

    // T is the off-topic floor of a standalone message; a fused follow-up continues a park topic.
    const topCos = contextUsed ? Number.POSITIVE_INFINITY : (ranked.cos[0] ?? -1);
    const d = decide(safety.urgent, order, topCos, this.ctx);
    const id = d.type === 'answer' ? d.id : visualFallback;
    const reply = id ? this.answer(id, banner, turn) : this.abstain(banner, turn);
    return done({
      reply,
      retrieval,
      ...(rerankedBy ? { rerankedBy } : {}),
      ...(error ? { error } : {}),
    });
  }

  /** Forget the previous turn: the next ask is scored on its own. */
  resetContext(): void {
    this.prevScores = undefined;
    this.prevText = undefined;
    this.state = undefined;
  }

  private isVerified(id: string): boolean {
    return this.ctx.byId.get(id)?.verified_by_uton === true;
  }

  private answer(id: string, banner: Banner | undefined, turn: Turn): KnowledgeReply {
    const base = { ...answerFor(this.ctx, id), ...(banner ? { banner } : {}) };
    if (!this.cont) return base;
    // L0 paraphrases are not guion text: a verified turn keeps the canonical answer.
    const pick = turn === 'verified' ? undefined : this.l0(id);
    if (turn === 'urgent') this.state = undefined;
    else {
      if (this.state?.id !== id) this.state = newState(id);
      this.markServed(this.state, id, pick?.atoms ?? []);
    }
    return pick ? { ...base, text: pick.text } : base;
  }

  /** Abstain or off-topic: the "sigue" conversation ends (R4.7). */
  private abstain(banner: Banner | undefined, turn: Turn): KnowledgeReply {
    this.state = undefined;
    const { abstain, abstain_verified } = this.ctx.policy.texts;
    return this.policyText(banner, turn === 'verified' ? (abstain_verified ?? abstain) : abstain);
  }

  private policyText(banner: Banner | undefined, text: string): KnowledgeReply {
    return { type: 'abstain', ...(banner ? { banner } : {}), text };
  }

  /** Next L0 paraphrase of the seeded rotation (R6.5); undefined keeps the canonical text. */
  private l0(id: string): DepthText | undefined {
    const d = this.depth[id];
    if (!d || !d.l0.length) return undefined;
    // R6.6: an emergency entry rotates only over its doubly approved set, and only if it has 3.
    const pool = this.ctx.emergencyDirect.has(id) ? (d.rotation ?? []) : d.l0.map((_, i) => i);
    if (this.ctx.emergencyDirect.has(id) && pool.length < 3) return undefined;
    return d.l0[pool[this.rot.take(`${id}:L0`, pool.length)]];
  }

  private markServed(st: ContinuationState, id: string, atoms: readonly string[]): void {
    for (const f of atoms) st.served.add(factKey(id, f));
  }

  /** A served depth text under the entry's own title and sources; steps stay in the first answer. */
  private reply(id: string, text: string, banner: Banner | undefined): KnowledgeReply {
    const { steps: _steps, ...base } = answerFor(this.ctx, id);
    return { ...base, text, ...(banner ? { banner } : {}) };
  }

  /**
   * "sigue" / "por qué" without retrieval (R4.1-R4.5). undefined: not handled, take the normal
   * path (a "por qué" with no unserved why layer is an ordinary follow-up, R4.5).
   */
  private continuation(
    kind: CueKind,
    banner: Banner | undefined,
    turn: Turn,
  ): KnowledgeReply | undefined {
    const c = this.cont;
    const st = this.state;
    if (!c) return undefined;
    const d = st ? this.depth[st.id] : undefined;
    // R6.6: an emergency entry never continues into a depth layer. Those texts are not the
    // doubly approved paraphrase set. "por qué" falls through to retrieval; "sigue" may still walk.
    const emergency = !!st && this.ctx.emergencyDirect.has(st.id);
    // Depth layers and L0 paraphrases are not guion text either: a verified turn serves neither
    // and walks to verified entries' canonical answers only.
    const verified = turn === 'verified';
    if (kind === 'why') {
      if (emergency || verified) return undefined;
      const li = st && d ? d.layers.findIndex((l, i) => l.kind === 'why' && !st.layers.has(i)) : -1;
      return st && d && li >= 0 ? this.serveLayer(st, d, li, banner) : undefined;
    }
    if (!st) return this.policyText(banner, c.texts.no_state);
    if (!emergency && !verified) {
      const pick = d ? pickLayer(d, st, () => this.rot.random()) : undefined;
      if (d && pick) return this.serveLayer(st, d, pick.layer, banner, pick.texts);
    }

    const walk = (d?.walk ?? []).filter((w) => !verified || this.isVerified(w));
    for (const w of walk) {
      if (st.walked.has(w)) continue;
      st.walked.add(w);
      const t = verified ? undefined : this.l0(w);
      const text = t?.text ?? this.ctx.byId.get(w)?.short ?? '';
      this.markServed(st, w, t?.atoms ?? []);
      const bridge = c.bridges[this.rot.take('bridges', c.bridges.length)];
      return this.reply(w, `${bridge} ${text}`, banner);
    }
    const labels = walk.slice(0, 2).map((w) => this.ctx.byId.get(w)?.menu_label ?? w);
    const related =
      c.texts.related && labels.length
        ? c.texts.related.replace('{topics}', joinTopics(labels))
        : '';
    return this.policyText(banner, `${c.texts.exhausted} ${related}`.trim());
  }

  private serveLayer(
    st: ContinuationState,
    d: DepthEntry,
    layer: number,
    banner: Banner | undefined,
    allowed?: Set<number>,
  ): KnowledgeReply {
    const l = d.layers[layer];
    const ok = allowed ?? bestTexts(l, st);
    const t = l.texts[this.rot.take(`${st.id}:L${layer + 1}`, l.texts.length, (i) => ok.has(i))];
    st.layers.add(layer);
    this.markServed(st, st.id, t.atoms);
    return this.reply(st.id, t.text, banner);
  }
}
