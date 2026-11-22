import type { ChatMessage, Completion, LLMBackend, PromptRequest } from '../core/types';

// Dev-only backend for a llama-server. Mirrors client.py LlamaClient with schema_via_completion:
// POST /apply-template, then POST /completion with the bare json_schema. Non-streaming, so ttft_ms is null.

const ERROR_BODY_LIMIT = 2000;
const DEFAULT_SEED = 1234; // same default as Python schemas.PromptRequest

export interface HttpBackendOptions {
  timeoutMs?: number;
  fetchImpl?: typeof fetch;
}

export function buildRawBody(req: PromptRequest, prompt: string): Record<string, unknown> {
  const body: Record<string, unknown> = {
    prompt,
    stream: false,
    n_predict: req.max_tokens,
    temperature: req.temperature ?? 0,
    seed: req.seed ?? DEFAULT_SEED,
    cache_prompt: true,
  };
  if (req.json_schema) body.json_schema = req.json_schema;
  if (req.top_p !== undefined) body.top_p = req.top_p;
  if (req.top_k !== undefined) body.top_k = req.top_k;
  return body;
}

class HttpStatusError extends Error {}

export class HttpBackend implements LLMBackend {
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly fetchImpl: typeof fetch;

  constructor(baseUrl: string, opts: HttpBackendOptions = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.timeoutMs = opts.timeoutMs ?? 300_000;
    this.fetchImpl = opts.fetchImpl ?? fetch;
  }

  private async post(path: string, body: unknown, signal: AbortSignal): Promise<Record<string, any>> {
    const resp = await this.fetchImpl(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
      signal,
    });
    if (!resp.ok) {
      const text = (await resp.text()).slice(0, ERROR_BODY_LIMIT);
      throw new HttpStatusError(`${resp.status}: ${text}`);
    }
    return (await resp.json()) as Record<string, any>;
  }

  async applyTemplate(messages: ChatMessage[], signal: AbortSignal): Promise<string> {
    const j = await this.post('/apply-template', { messages }, signal);
    if (typeof j.prompt !== 'string') throw new Error('/apply-template response has no "prompt"');
    return j.prompt;
  }

  // Never throws, like the Python client: failures land in `timeout` / `http_error`.
  async complete(req: PromptRequest, signal?: AbortSignal): Promise<Completion> {
    const t0 = Date.now();
    const total = () => Date.now() - t0;
    const ctl = new AbortController();
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      ctl.abort();
    }, this.timeoutMs);
    const onAbort = () => ctl.abort();
    if (signal?.aborted) ctl.abort();
    else signal?.addEventListener('abort', onAbort);
    try {
      const prompt = await this.applyTemplate(req.messages, ctl.signal);
      const j = await this.post('/completion', buildRawBody(req, prompt), ctl.signal);
      const t = (j.timings ?? {}) as Record<string, number | undefined>;
      return {
        content: typeof j.content === 'string' ? j.content : '',
        finish_reason: j.stop_type === 'limit' ? 'length' : j.stop ? 'stop' : null,
        total_ms: total(),
        prompt_n: t.prompt_n ?? null,
        cache_n: t.cache_n ?? null,
        predicted_n: t.predicted_n ?? null,
        prompt_ms: t.prompt_ms ?? null,
        predicted_ms: t.predicted_ms ?? null,
        ttft_ms: null,
      };
    } catch (e) {
      if (timedOut) return { content: '', total_ms: total(), timeout: true };
      if (signal?.aborted) return { content: '', finish_reason: 'interrupted', total_ms: total() };
      const msg = e instanceof HttpStatusError ? e.message : `transport: ${e instanceof Error ? e.message : String(e)}`;
      return { content: '', total_ms: total(), http_error: msg };
    } finally {
      clearTimeout(timer);
      signal?.removeEventListener('abort', onAbort);
    }
  }
}
