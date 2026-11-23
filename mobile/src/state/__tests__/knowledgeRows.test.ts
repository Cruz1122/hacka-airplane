import type { KnowledgeRow } from '../knowledgeChat';
import { toChatRows } from '../knowledgeRows';

const timing = { rulesMs: 0, embedMs: 200, retrieveMs: 10, rerankMs: 0, totalMs: 212.4 };

describe('toChatRows', () => {
  it('maps a top-1 answer to one bubble with only its reply text, sources and latency', () => {
    const rows: KnowledgeRow[] = [
      { id: 'k1', role: 'user', text: 'cómo llego desde Manizales' },
      {
        id: 'k2',
        role: 'assistant',
        timing,
        reply: {
          type: 'answer',
          id: 'access.from_manizales',
          title: 'Cómo llegar desde Manizales',
          text: 'Por la vía al Magdalena.',
          steps: ['Sal temprano.', 'Lleva abrigo.'],
          sources: [{ title: 'PNN', url: 'https://example.org' }],
        },
      },
    ];
    expect(toChatRows(rows, 'ERR')).toEqual([
      { id: 'k1', role: 'user', text: 'cómo llego desde Manizales' },
      {
        id: 'k2',
        role: 'assistant',
        text: 'Por la vía al Magdalena.',
        latencyMs: 212,
        sources: [{ id: 'access.from_manizales#0', title: 'PNN', url: 'https://example.org' }],
      },
    ]);
  });

  it('puts a banner in its own bubble above the reply', () => {
    const rows: KnowledgeRow[] = [
      {
        id: 'k3',
        role: 'assistant',
        reply: {
          type: 'abstain',
          text: 'No encontré ese tema.',
          banner: { kind: 'urgent_safety', text: 'Llama al 123', sourceIds: [] },
        },
      },
    ];
    expect(toChatRows(rows, 'ERR')).toEqual([
      { id: 'k3:banner', role: 'assistant', text: 'Llama al 123' },
      { id: 'k3', role: 'assistant', text: 'No encontré ese tema.' },
    ]);
  });

  it('shows the i18n error text, never the raw error', () => {
    expect(toChatRows([{ id: 'k4', role: 'assistant', error: 'embedder gone' }], 'ERR')).toEqual([
      { id: 'k4', role: 'assistant', text: 'ERR' },
    ]);
  });
});
