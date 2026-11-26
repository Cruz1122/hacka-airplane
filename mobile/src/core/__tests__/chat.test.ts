import { FakeBackend } from '../../llm/fake';
import { DialogueRun } from '../driver';
import { ABSTAIN_ES } from '../values';
import { loadWorld } from '../world';

const NONE = '{"tool": "none"}';

describe('chat mode', () => {
  it('answers off-topic turns with a free model reply', async () => {
    const backend = new FakeBackend([NONE, '¡Hola! ¿En qué te ayudo?']);
    const run = new DialogueRun(loadWorld(), backend, { guards: true, answerMode: 'extractive', chat: true });
    expect(await run.turn('Hola')).toBe('¡Hola! ¿En qué te ayudo?');
    expect(backend.requests[1].json_schema).toBeUndefined();
    // Chat continues the route conversation so the route prefix stays in the KV cache.
    const route = backend.requests[0].messages;
    expect(backend.requests[1].messages.slice(0, route.length)).toEqual(route);
    expect(backend.requests[1].messages.at(-1)!.content).toContain('Estación Laguna Espejo');
    expect(run.state).toBe('OUT_OF_SCOPE');
  });

  it('streams the chat reply through the turn callback', async () => {
    const backend = {
      calls: 0,
      async complete(_req: unknown, _signal?: AbortSignal, onText?: (s: string) => void) {
        if (this.calls++ === 0) return { content: NONE };
        onText?.('¡Ho');
        onText?.('¡Hola!');
        return { content: '¡Hola!' };
      },
    };
    const seen: string[] = [];
    const run = new DialogueRun(loadWorld(), backend, { guards: true, answerMode: 'extractive', chat: true });
    expect(await run.turn('Hola', (s) => seen.push(s))).toBe('¡Hola!');
    expect(seen).toEqual(['¡Ho', '¡Hola!']);
  });

  it('generated answers continue the route conversation', async () => {
    const backend = new FakeBackend([
      '{"tool": "get_opening_hours", "args": {"station": "laguna_espejo"}}',
      'Abre a las 05:55 [fuente: EST-B-01].',
    ]);
    const run = new DialogueRun(loadWorld(), backend, { guards: true, answerMode: 'generate', chat: true });
    expect(await run.turn('¿A qué hora abre Laguna Espejo?')).toBe('Abre a las 05:55 [fuente: EST-B-01].');
    const route = backend.requests[0].messages;
    expect(backend.requests[1].messages.slice(0, route.length)).toEqual(route);
    expect(backend.requests[1].messages.at(-1)!.content).toContain('EST-B-01');
  });

  it('keeps the fixed abstention when chat is off', async () => {
    const run = new DialogueRun(loadWorld(), new FakeBackend([NONE]), { guards: true, answerMode: 'extractive' });
    expect(await run.turn('Hola')).toBe(ABSTAIN_ES);
  });
});
