// Top-1 policy (user decision 2026-11-22, replaces the menu of docs/phase3-architecture.md §1.2):
// answer with the best entry when its e5 cosine clears T, else abstain. A banner sits above the reply
// and never replaces it; every text shown is a curated catalog answer or a policy text.

import type { CatalogEntry, KnowledgeAssets, KnowledgePolicy } from './assets';
import type { SafetyResult } from './safety';
import type { Banner, KnowledgeReply, Source } from './types';

export interface PolicyContext {
  policy: KnowledgePolicy;
  byId: ReadonlyMap<string, CatalogEntry>;
  emergencyDirect: ReadonlySet<string>;
}

export function policyContext(assets: KnowledgeAssets): PolicyContext {
  return {
    policy: assets.policy,
    byId: new Map(assets.catalog.map((e) => [e.id, e])),
    emergencyDirect: new Set(assets.policy.emergency_direct),
  };
}

function entry(ctx: PolicyContext, id: string): CatalogEntry {
  const e = ctx.byId.get(id);
  if (!e) throw new Error(`Unknown knowledge entry ${id}`);
  return e;
}

/** Urgent wins over live status: one banner at most. */
export function bannerFor(safety: SafetyResult, ctx: PolicyContext): Banner | undefined {
  if (safety.urgent) {
    const id = ctx.policy.emergency_line_id;
    return {
      kind: 'urgent_safety',
      text: entry(ctx, id).short,
      sourceIds: [id],
    };
  }
  if (safety.liveStatus) {
    return {
      kind: 'offline_current_status',
      text: ctx.policy.texts.offline_status,
      sourceIds: [],
    };
  }
  return undefined;
}

export type Decision = { type: 'answer'; id: string } | { type: 'abstain' };

/**
 * `order` is the (possibly reranked) pool; `topCos` is the best e5 cosine of the pool before any
 * reranking, because T was fitted on that.
 */
export function decide(
  urgent: boolean,
  order: readonly string[],
  topCos: number,
  ctx: PolicyContext,
): Decision {
  if (urgent) {
    // No threshold: the best emergency entry in the pool, else the curated 123 line.
    const id = order.find((x) => ctx.emergencyDirect.has(x)) ?? ctx.policy.emergency_line_id;
    return { type: 'answer', id };
  }
  if (order.length && topCos >= ctx.policy.T) return { type: 'answer', id: order[0] };
  return { type: 'abstain' };
}

const flattenStep = (s: string | string[]) => (Array.isArray(s) ? s.join(' ') : s);

export function answerFor(
  ctx: PolicyContext,
  id: string,
): Extract<KnowledgeReply, { type: 'answer' }> {
  const e = entry(ctx, id);
  const steps = e.steps.map(flattenStep).filter((s) => s.trim() !== '');
  const sources: Source[] = e.sources.map((s) => ({
    title: s.label,
    ...(s.url ? { url: s.url } : {}),
    ...(s.retrieved_at ? { date: s.retrieved_at } : {}),
  }));
  return {
    type: 'answer',
    id,
    title: e.menu_label || e.label,
    text: e.short,
    ...(steps.length ? { steps } : {}),
    sources,
    ...(e.last_verified ? { reviewed: e.last_verified } : {}),
  };
}
