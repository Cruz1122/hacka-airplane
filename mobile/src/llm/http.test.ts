import { HttpBackend } from './http';

const req = {
  messages: [{ role: 'user' as const, content: 'hi' }],
  max_tokens: 64,
  json_schema: { type: 'object' },
};

function resp(status: number, body: unknown): Response {
  return {
    ok: status < 400,
    status,
    json: async () => body,
    text: async () => (typeof body === 'string' ? body : JSON.stringify(body)),
  } as Response;
}

describe('HttpBackend', () => {
  it('applies the template then posts /completion with the bare schema', async () => {
    const fetchImpl = jest
      .fn()
      .mockResolvedValueOnce(resp(200, { prompt: '<p>' }))
      .mockResolvedValueOnce(
        resp(200, {
          content: '{"a":1}',
          stop: true,
          stop_type: 'eos',
          timings: { prompt_n: 10, cache_n: 4, predicted_n: 3, prompt_ms: 5, predicted_ms: 7 },
        }),
      );
    const out = await new HttpBackend('http://h:1/', { fetchImpl }).complete(req);

    expect(fetchImpl.mock.calls[0][0]).toBe('http://h:1/apply-template');
    expect(JSON.parse(fetchImpl.mock.calls[0][1].body)).toEqual({ messages: req.messages });
    expect(fetchImpl.mock.calls[1][0]).toBe('http://h:1/completion');
    expect(JSON.parse(fetchImpl.mock.calls[1][1].body)).toEqual({
      prompt: '<p>',
      stream: false,
      n_predict: 64,
      temperature: 0,
      seed: 1234,
      cache_prompt: true,
      json_schema: { type: 'object' },
    });
    expect(out).toMatchObject({
      content: '{"a":1}',
      finish_reason: 'stop',
      prompt_n: 10,
      cache_n: 4,
      predicted_n: 3,
      prompt_ms: 5,
      predicted_ms: 7,
    });
    expect(out.http_error).toBeUndefined();
  });

  it('maps stop_type limit to finish_reason length', async () => {
    const fetchImpl = jest
      .fn()
      .mockResolvedValueOnce(resp(200, { prompt: 'p' }))
      .mockResolvedValueOnce(resp(200, { content: '{', stop: true, stop_type: 'limit' }));
    expect((await new HttpBackend('http://h', { fetchImpl }).complete(req)).finish_reason).toBe('length');
  });

  it('reports HTTP errors instead of throwing', async () => {
    const fetchImpl = jest.fn().mockResolvedValueOnce(resp(500, 'boom'));
    const out = await new HttpBackend('http://h', { fetchImpl }).complete(req);
    expect(out).toMatchObject({ content: '', http_error: '500: boom' });
  });

  it('reports transport errors', async () => {
    const fetchImpl = jest.fn().mockRejectedValueOnce(new Error('ECONNREFUSED'));
    const out = await new HttpBackend('http://h', { fetchImpl }).complete(req);
    expect(out.http_error).toBe('transport: ECONNREFUSED');
  });

  it('flags timeout when the request is aborted by the timer', async () => {
    const fetchImpl = jest.fn(
      (_u: string, init: RequestInit) =>
        new Promise((_res, rej) => init.signal!.addEventListener('abort', () => rej(new Error('aborted')))),
    );
    const out = await new HttpBackend('http://h', { fetchImpl: fetchImpl as never, timeoutMs: 20 }).complete(req);
    expect(out.timeout).toBe(true);
  });
});
