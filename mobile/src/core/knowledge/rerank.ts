// Reranker seam (docs/phase3-architecture.md §2). Laya plugs in here later; it may only reorder the
// e5 pool ("reorder_only"), never add, drop or cut it.

export interface Reranker {
  readonly id: string;
  /** Ids the reranker was trained on. When set, the engine skips it for a pool with any other id. */
  readonly catalogIds?: ReadonlySet<string>;
  /** Returns the same ids as `pool`, best first. */
  rerank(query: string, pool: string[], cos: number[]): Promise<string[]>;
}

export const identityReranker: Reranker = {
  id: 'identity',
  rerank: async (_query, pool) => [...pool],
};

/** False when any pool id is outside the reranker's training catalog: it never saw that entry. */
export function canRerank(pool: readonly string[], catalogIds: ReadonlySet<string>): boolean {
  return pool.every((id) => catalogIds.has(id));
}

/** A reranker's output is usable only if it is a reordering of the pool. */
export function isReordering(out: readonly string[], pool: readonly string[]): boolean {
  if (out.length !== pool.length) return false;
  const rest = new Set(pool);
  for (const id of out) if (!rest.delete(id)) return false;
  return rest.size === 0;
}
