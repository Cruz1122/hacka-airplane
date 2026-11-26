import type { Completion, LLMBackend, PromptRequest } from '../core/types';

export type FakeReply = string | Partial<Completion> | ((req: PromptRequest) => string | Partial<Completion>);

// Scripted backend for tests: replies are consumed in order; running out is an error, not a silent "".
export class FakeBackend implements LLMBackend {
  readonly requests: PromptRequest[] = [];
  private i = 0;

  constructor(private readonly replies: readonly FakeReply[]) {}

  async complete(req: PromptRequest): Promise<Completion> {
    this.requests.push(req);
    if (this.i >= this.replies.length) {
      throw new Error(`FakeBackend exhausted: call #${this.i + 1} but only ${this.replies.length} scripted`);
    }
    const r = this.replies[this.i++];
    const out = typeof r === 'function' ? r(req) : r;
    return typeof out === 'string' ? { content: out, finish_reason: 'stop' } : { content: '', ...out };
  }
}
