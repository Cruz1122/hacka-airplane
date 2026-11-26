import type { KnowledgeReply } from '@/core/knowledge/types';
import type { MediaCatalog } from '@/core/media/media';

import { KnowledgeChat, type LoadedEngine } from '../knowledgeChat';

const answer: KnowledgeReply = {
  type: 'answer',
  id: 'access.from_manizales',
  title: 'Cómo llegar desde Manizales',
  text: 'Por la vía...',
  sources: [],
  verified: false,
};
const timing = { rulesMs: 0, embedMs: 1, retrieveMs: 1, rerankMs: 0, totalMs: 2 };

function fakeEngine(over: Partial<LoadedEngine['engine']> = {}) {
  return {
    ask: jest.fn(async () => ({
      reply: answer,
      timing,
      safety: { urgent: false } as never,
      contextUsed: false,
    })),
    ...over,
  };
}

describe('KnowledgeChat', () => {
  it('goes ready after load and appends the user turn then the answer', async () => {
    const engine = fakeEngine();
    const chat = new KnowledgeChat(async () => ({ engine }));
    expect(chat.snapshot().status).toBe('loading');
    await chat.ask('  como llego  ');
    const s = chat.snapshot();
    expect(s.status).toBe('ready');
    expect(engine.ask).toHaveBeenCalledWith('como llego', { verifiedOnly: false });
    expect(s.rows.map((r) => r.role)).toEqual(['user', 'assistant']);
    expect(s.rows[1]).toMatchObject({ reply: answer, timing });
    expect(s.busy).toBe(false);
  });

  it('ignores blank input', async () => {
    const engine = fakeEngine();
    const chat = new KnowledgeChat(async () => ({ engine }));
    await chat.ask('   ');
    expect(chat.snapshot().rows).toEqual([]);
    expect(engine.ask).not.toHaveBeenCalled();
  });

  it('shows an engine failure as an error row instead of throwing', async () => {
    const engine = fakeEngine({ ask: jest.fn(async () => Promise.reject(new Error('embedder gone'))) });
    const chat = new KnowledgeChat(async () => ({ engine }));
    await chat.ask('hola');
    expect(chat.snapshot().rows[1]).toEqual({ id: expect.any(String), role: 'assistant', error: 'embedder gone' });
    expect(chat.snapshot().busy).toBe(false);
  });

  it('reports a degraded runtime', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: fakeEngine(), degraded: 'e5-base-f16.gguf not found' }));
    await chat.ask('hola');
    const s = chat.snapshot();
    expect(s.status).toBe('degraded');
    expect(s.error).toContain('not found');
  });

  it('notifies subscribers on every change', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: fakeEngine() }));
    const fn = jest.fn();
    const off = chat.subscribe(fn);
    await chat.ask('hola');
    off();
    chat.reset();
    expect(fn.mock.calls.length).toBeGreaterThanOrEqual(3); // ready, user row, reply row
    expect(chat.snapshot().rows).toEqual([]);
  });

  it('reset clears the engine follow-up context', async () => {
    const engine = { ...fakeEngine(), resetContext: jest.fn() };
    const chat = new KnowledgeChat(async () => ({ engine }));
    await chat.ask('hola');
    expect(engine.resetContext).not.toHaveBeenCalled();
    chat.reset();
    await Promise.resolve(); // the engine is behind a promise
    expect(engine.resetContext).toHaveBeenCalledTimes(1);
    expect(chat.snapshot().rows).toEqual([]);
  });

  it('asks under the verified-only switch as it is at each question', async () => {
    let on = false;
    const engine = fakeEngine();
    const chat = new KnowledgeChat(async () => ({ engine }), { verifiedOnly: () => on });
    await chat.ask('uno');
    on = true;
    await chat.ask('dos');
    expect(engine.ask).toHaveBeenNthCalledWith(1, 'uno', { verifiedOnly: false });
    expect(engine.ask).toHaveBeenNthCalledWith(2, 'dos', { verifiedOnly: true });
  });

  it('a flipped switch drops the follow-up context but keeps the conversation', async () => {
    let on = false;
    const engine = { ...fakeEngine(), resetContext: jest.fn() };
    const chat = new KnowledgeChat(async () => ({ engine }), { verifiedOnly: () => on });
    await chat.ask('uno');
    await chat.ask('dos');
    expect(engine.resetContext).not.toHaveBeenCalled();
    on = true;
    await chat.ask('tres');
    expect(engine.resetContext).toHaveBeenCalledTimes(1);
    await chat.ask('cuatro');
    expect(engine.resetContext).toHaveBeenCalledTimes(1);
    expect(chat.snapshot().rows).toHaveLength(8);
  });

  it('reset works with an engine that has no context to clear', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: fakeEngine() }));
    await chat.ask('hola');
    expect(() => chat.reset()).not.toThrow();
    await Promise.resolve();
    expect(chat.snapshot().rows).toEqual([]);
  });
});

describe('KnowledgeChat photos', () => {
  const condor: KnowledgeReply = {
    ...answer,
    id: 'fauna.condor',
    text: 'El cóndor anida en los riscos.',
  };
  const MEDIA: MediaCatalog = {
    items: {
      condor: {
        kind: 'species',
        common: 'Cóndor de los Andes',
        scientific: 'Vultur gryphus',
        photos: [{ file: 'condor.1.webp', author: 'Ana', license: 'CC BY 2.0' }],
      },
    },
    topics: { 'fauna.condor': ['condor'] },
  };
  const replying = (reply: KnowledgeReply) =>
    fakeEngine({
      ask: jest.fn(async () => ({
        reply,
        timing,
        safety: { urgent: false } as never,
        contextUsed: false,
      })),
    });
  const media = (chat: KnowledgeChat) =>
    chat
      .snapshot()
      .rows.flatMap((r) => (r.role === 'assistant' && 'reply' in r ? [r.media ?? null] : []));

  it('decides once per reply and keeps the decision on its row', async () => {
    const rng = jest.fn(() => 0);
    const chat = new KnowledgeChat(async () => ({ engine: replying(condor) }), {
      media: MEDIA,
      rng,
    });
    await chat.ask('háblame del cóndor');
    const row = chat.snapshot().rows[1];
    expect(media(chat)).toEqual([
      {
        layout: 'single',
        items: [
          {
            id: 'condor',
            common: 'Cóndor de los Andes',
            scientific: 'Vultur gryphus',
            photo: { file: 'condor.1.webp', author: 'Ana', license: 'CC BY 2.0' },
          },
        ],
      },
    ]);
    rng.mockReturnValue(0.99);
    await chat.ask('¿y dónde vive?');
    // Later turns roll their own dice; the first reply keeps what it showed.
    expect(chat.snapshot().rows[1]).toBe(row);
    expect(media(chat)[0]).toMatchObject({ layout: 'single' });
  });

  it('keeps showing photos on consecutive replies without a per-chat cooldown', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: replying(condor) }), {
      media: MEDIA,
      rng: () => 0.99,
    });
    await chat.ask('háblame del cóndor');
    await chat.ask('¿y dónde vive?');
    expect(media(chat).map((m) => m?.layout ?? null)).toEqual(['single', 'single']);
  });

  it('shows photos when asked for them, whatever the dice say', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: replying(condor) }), {
      media: MEDIA,
      rng: () => 0.99,
    });
    await chat.ask('háblame del cóndor');
    await chat.ask('muéstrame una foto del cóndor');
    expect(media(chat).map((m) => m?.layout ?? null)).toEqual(['single', 'single']);
  });

  it('never shows photos under an urgent banner', async () => {
    const urgent: KnowledgeReply = {
      ...condor,
      banner: { kind: 'urgent_safety', text: 'Marca el 123.', sourceIds: [] },
    };
    const chat = new KnowledgeChat(async () => ({ engine: replying(urgent) }), {
      media: MEDIA,
      rng: () => 0,
    });
    await chat.ask('me caí cerca de un cóndor, muéstrame fotos');
    expect(media(chat)).toEqual([null]);
  });

  it('may still show them under the offline-status notice', async () => {
    const live: KnowledgeReply = {
      ...condor,
      banner: { kind: 'offline_current_status', text: 'Sin conexión.', sourceIds: [] },
    };
    const chat = new KnowledgeChat(async () => ({ engine: replying(live) }), {
      media: MEDIA,
      rng: () => 0,
    });
    await chat.ask('¿hoy se ve el cóndor?');
    expect(media(chat).map((m) => m?.layout ?? null)).toEqual(['single']);
  });

  it('shows none without a catalog', async () => {
    const chat = new KnowledgeChat(async () => ({ engine: replying(condor) }), { rng: () => 0 });
    await chat.ask('muéstrame el cóndor');
    expect(media(chat)).toEqual([null]);
  });
});

test.each([
  '¿Puedo enviarte una foto?',
  '¿Dónde está la cámara?',
  '¿Qué puedes hacer?',
])('answers app help without calling the text retriever for %s', async (question) => {
  const engine = fakeEngine();
  const chat = new KnowledgeChat(async () => ({ engine, degraded: 'modelo ausente' }));
  await chat.ask(question);
  expect(engine.ask).not.toHaveBeenCalled();
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    role: 'assistant',
    reply: { text: expect.stringContaining('cámara a la izquierda') },
  });
});

test('a park photography question still goes to the knowledge engine', async () => {
  const engine = fakeEngine();
  const chat = new KnowledgeChat(async () => ({ engine }));
  const question = '¿Puedo tomar fotos en el parque?';
  await chat.ask(question);
  expect(engine.ask).toHaveBeenCalledWith(question, { verifiedOnly: false });
});
