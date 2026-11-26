// Knowledge engine: safety rules -> e5 embedding -> retrieval -> optional reranker -> top-1 policy ->
// curated answer by id. Pure TS; the embedder and the vectors are injected.

import {
  validateAssets,
  type KnowledgeAssets,
  type KnowledgeFollowup,
  type LoadedIndex,
} from './assets';
import { answerFor, bannerFor, decide, policyContext, type PolicyContext } from './policy';
import { canRerank, isReordering, type Reranker } from './rerank';
import { retrieve, type RetrievalResult } from './retrieve';
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

const CHAIN_WORDS = 60; // e5 reads 512 tokens; a follow-up chain stays far below that

const now = (): number => (typeof performance !== 'undefined' ? performance.now() : Date.now());

export class KnowledgeEngine {
  private readonly idx: LoadedIndex;
  private readonly ctx: PolicyContext;
  /** Entry scores of the last ask that produced a retrieval; the follow-up context. */
  private prevScores: Float32Array | undefined;
  private prevText: string | undefined; // previous user message (followup.mode 'concat')

  /**
   * @param vectors side-loaded index.f32.bin, rows x dims as the manifest says.
   * @param embed receives the user's text RAW; the embedder itself adds the e5 "query: " prefix
   *   (manifest.prefix) and returns the L2-normalised vector.
   * @param reranker optional reorderer (Laya); skipped for pools outside its catalogIds.
   * @param score optional native scorer; without it the JS dot-product loop runs (~0.46 s in Hermes).
   */
  constructor(
    assets: KnowledgeAssets,
    vectors: Float32Array,
    private readonly embed: Embed,
    private readonly reranker?: Reranker,
    private readonly score?: Score,
  ) {
    this.idx = validateAssets(assets, vectors);
    this.ctx = policyContext(assets);
  }

  async ask(text: string, visualEntryId?: string, preferCaption = false): Promise<AskResult> {
    const t0 = now();
    // Rules first: they need no model, so a failing embedder cannot suppress the urgent notice.
    const safety = detectSafety(text);
    const banner = bannerFor(safety, this.ctx);
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

    if (text.trim() === '') return done({ reply: this.abstain(banner) });
    const visualFallback = visualEntryId && this.ctx.byId.has(visualEntryId) && !safety.urgent
      ? visualEntryId : undefined;
    if (visualFallback) {
      this.resetContext();
      if (!preferCaption) return done({ reply: this.answer(visualFallback, banner) });
    }

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
      if (f && prev !== undefined && !safety.urgent && isFollowup(text, retrieval.cos[0] ?? -1, f)) {
        let context: Float32Array;
        if (typeof prev === 'string') {
          const t3 = now();
          const cvec = await this.embed(prep(`${prev} ${text}`));
          timing.embedMs += now() - t3;
          context = retrieve(cvec, this.idx, this.score ? await this.score(cvec) : undefined).scores;
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
      if (visualFallback) return done({ reply: this.answer(visualFallback, banner), error });
      if (!banner) throw error;
      // Urgent without a model: the curated 123 entry under the urgent banner.
      const reply = safety.urgent
        ? this.answer(this.ctx.policy.emergency_line_id, banner)
        : this.abstain(banner);
      return done({ reply, error });
    }

    let order = retrieval.pool;
    let rerankedBy: string | undefined;
    let error: Error | undefined;
    const rr = this.reranker;
    if (rr && (!rr.catalogIds || canRerank(order, rr.catalogIds))) {
      const t3 = now();
      try {
        const out = await rr.rerank(text, [...order], [...retrieval.cos]);
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
    const topCos = contextUsed ? Number.POSITIVE_INFINITY : (retrieval.cos[0] ?? -1);
    const d = decide(safety.urgent, order, topCos, this.ctx);
    const id = d.type === 'answer' ? d.id : visualFallback;
    const reply = id ? this.answer(id, banner) : this.abstain(banner);
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
  }

  private answer(id: string, banner: Banner | undefined): KnowledgeReply {
    return { ...answerFor(this.ctx, id), ...(banner ? { banner } : {}) };
  }

  private abstain(banner: Banner | undefined): KnowledgeReply {
    return { type: 'abstain', ...(banner ? { banner } : {}), text: this.ctx.policy.texts.abstain };
  }
}
