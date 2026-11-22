import { Directory, Paths } from 'expo-file-system';
import { initLlama, type LlamaContext } from 'llama.rn';

import type { ChatMessage, LLMBackend } from '../core/types';
import { LlamaRnBackend } from './llamaRn';
import { getModelSpec, resolveModelFile, type ModelId } from './models';

export type ModelStatus = 'missing' | 'loading' | 'ready' | 'error';
export interface ModelState {
  id: string;
  status: ModelStatus;
  path?: string;
  error?: string;
}

const CONTEXT_PARAMS = {
  n_ctx: 4096,
  n_threads: 4,
  n_gpu_layers: 0, // r2 phone numbers were CPU-only; revisit only with a measurement
  ctx_shift: false, // never silently drop prompt head: it would also break the prefix cache
} as const;

// GGUFs are side-loaded into the app files dir (see scripts/push-model.sh).
function toNativePath(uri: string): string {
  return uri.replace(/^file:\/\//, '');
}

export function locateModel(id: string): string | null {
  const spec = getModelSpec(id);
  const files = new Directory(Paths.document).list().filter((f) => !(f instanceof Directory));
  const name = resolveModelFile(spec, files.map((f) => f.name));
  const hit = files.find((f) => f.name === name);
  return hit ? toNativePath(hit.uri) : null;
}

export class ModelManager {
  private ctx: LlamaContext | null = null;
  private current: LLMBackend | null = null;
  private state: ModelState = { id: '', status: 'missing' };
  private listeners = new Set<(s: ModelState) => void>();
  private loadSeq = 0;
  private inflight: { id: string; promise: Promise<LLMBackend> } | null = null;

  getState(): ModelState {
    return this.state;
  }

  subscribe(fn: (s: ModelState) => void): () => void {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  }

  private set(s: ModelState): void {
    this.state = s;
    this.listeners.forEach((fn) => fn(s));
  }

  // Throws unless status is 'ready'; callers gate on getState().
  backend(): LLMBackend {
    if (!this.current || this.state.status !== 'ready') {
      throw new Error(`Model not ready (status=${this.state.status}${this.state.error ? `: ${this.state.error}` : ''})`);
    }
    return this.current;
  }

  async exists(id: ModelId | string): Promise<boolean> {
    return locateModel(id) !== null;
  }

  // Loads (or switches to) a model and returns its backend; rejects when missing or failing.
  // The outcome is also in getState()/subscribe(). Concurrent calls for one id share the load.
  load(id: ModelId | string): Promise<LLMBackend> {
    if (this.state.id === id && this.state.status === 'ready' && this.current) return Promise.resolve(this.current);
    if (this.inflight?.id === id) return this.inflight.promise;
    const promise = this.doLoad(id);
    this.inflight = { id, promise };
    const clear = () => {
      if (this.inflight?.promise === promise) this.inflight = null;
    };
    promise.then(clear, clear);
    return promise;
  }

  private async doLoad(id: string): Promise<LLMBackend> {
    await this.release(); // bumps loadSeq, invalidating any load still in flight
    const seq = ++this.loadSeq;
    const fail = (message: string, status: ModelStatus): never => {
      if (seq === this.loadSeq) this.set({ id, status, error: message });
      throw new Error(message);
    };
    let spec;
    let path: string | null;
    try {
      spec = getModelSpec(id);
      path = locateModel(id);
    } catch (e) {
      return fail(e instanceof Error ? e.message : String(e), 'error');
    }
    if (!path) return fail(`No file matching "${spec.file}" in app files dir; run scripts/push-model.sh`, 'missing');
    this.set({ id, status: 'loading', path });
    let ctx: LlamaContext;
    try {
      ctx = await initLlama({ model: path, ...CONTEXT_PARAMS });
    } catch (e) {
      return fail(e instanceof Error ? e.message : String(e), 'error');
    }
    if (seq !== this.loadSeq) {
      // A newer load()/release() superseded this one while the model was loading.
      await ctx.release();
      throw new Error(`load of ${id} superseded`);
    }
    this.ctx = ctx;
    this.current = new LlamaRnBackend(ctx, spec.quirks);
    this.set({ id, status: 'ready', path });
    return this.current;
  }

  async release(): Promise<void> {
    this.loadSeq++;
    const ctx = this.ctx;
    this.ctx = null;
    this.current = null;
    if (ctx) await ctx.release();
    this.set({ id: this.state.id, status: 'missing' });
  }

  // Pre-fills the stable route prefix so the first real turn hits the KV cache.
  // `prefix` must be the exact leading messages of a route request (from core/prompts).
  async warmup(prefix: ChatMessage[]): Promise<void> {
    const res = await this.backend().complete({ messages: prefix, max_tokens: 1, temperature: 0 });
    if (res.http_error) throw new Error(`warmup failed: ${res.http_error}`);
  }
}

export const modelManager = new ModelManager();
