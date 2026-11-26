import type { LlamaContext } from 'llama.rn';

import type { Completion, LLMBackend, PromptRequest } from '../core/types';
import type { ModelQuirks } from './models';

// Mirrors the benchmark /completion path: chat template (reasoning off) -> raw completion
// constrained by the JSON schema. The single context is kept alive so llama.cpp reuses the
// KV prefix between calls (route prefix ~2k tokens).

export const DEFAULT_SEED = 1234; // same default as Python schemas.PromptRequest

export type LlamaCtx = Pick<LlamaContext, 'getFormattedChat' | 'completion' | 'stopCompletion'>;

export class LlamaRnBackend implements LLMBackend {
  private queue: Promise<unknown> = Promise.resolve();
  private warnedThink = false;

  constructor(
    private readonly ctx: LlamaCtx,
    private readonly quirks: ModelQuirks,
  ) {}

  // One native context decodes one request at a time; serialize instead of racing it.
  complete(req: PromptRequest, signal?: AbortSignal, onText?: (textSoFar: string) => void): Promise<Completion> {
    const run = this.queue.then(() => this.run(req, signal, onText));
    this.queue = run.catch(() => undefined);
    return run;
  }

  private async run(
    req: PromptRequest,
    signal?: AbortSignal,
    onText?: (textSoFar: string) => void,
  ): Promise<Completion> {
    const t0 = Date.now();
    if (signal?.aborted) return { content: '', finish_reason: 'interrupted', total_ms: 0 };
    const onAbort = () => void this.ctx.stopCompletion().catch(() => undefined);
    signal?.addEventListener('abort', onAbort);
    try {
      const formatted = await this.ctx.getFormattedChat(req.messages, null, {
        jinja: true,
        // The wrapper defaults enable_thinking to true; the benchmark runs with reasoning off.
        enable_thinking: false,
        reasoning_format: 'none',
        add_generation_prompt: true,
      });
      this.checkThinkBlock(formatted.prompt);

      let ttft: number | null = null;
      let soFar = '';
      const res = await this.ctx.completion(
        {
          prompt: formatted.prompt,
          n_predict: req.max_tokens,
          temperature: req.temperature ?? 0,
          seed: req.seed ?? DEFAULT_SEED,
          ...(req.top_p !== undefined && { top_p: req.top_p }),
          ...(req.top_k !== undefined && { top_k: req.top_k }),
          ...(this.quirks.stop.length && { stop: this.quirks.stop }),
          // JSON-stringified by hand: the wrapper only stringifies via response_format, which
          // would also trigger the chat-format path we deliberately skip.
          ...(req.json_schema && { json_schema: JSON.stringify(req.json_schema) }),
        },
        (d) => {
          if (ttft === null && d.token) ttft = Date.now() - t0;
          if (onText && d.token) onText((soFar += d.token));
        },
      );

      const t = res.timings;
      return {
        content: res.text ?? '',
        finish_reason: res.interrupted
          ? 'interrupted'
          : res.stopped_limit || res.context_full
            ? 'length'
            : res.stopped_eos || res.stopped_word
              ? 'stop'
              : null,
        prompt_n: t?.prompt_n ?? res.tokens_evaluated ?? null,
        cache_n: t?.cache_n ?? res.tokens_cached ?? null,
        predicted_n: t?.predicted_n ?? res.tokens_predicted ?? null,
        prompt_ms: t?.prompt_ms ?? null,
        predicted_ms: t?.predicted_ms ?? null,
        ttft_ms: ttft,
        total_ms: Date.now() - t0,
      };
    } catch (e) {
      if (signal?.aborted) return { content: '', finish_reason: 'interrupted', total_ms: Date.now() - t0 };
      return { content: '', total_ms: Date.now() - t0, http_error: `native: ${e instanceof Error ? e.message : String(e)}` };
    } finally {
      signal?.removeEventListener('abort', onAbort);
    }
  }

  private checkThinkBlock(prompt: string): void {
    if (!this.quirks.emptyThinkBlock || this.warnedThink) return;
    if (!/<think>\s*<\/think>/.test(prompt)) {
      this.warnedThink = true;
      // Non-fatal: the schema grammar prevents think text, but the prompt would differ from the Python reference.
      console.warn('[llm] expected an empty <think></think> block in the formatted prompt; template/params mismatch');
    }
  }
}
