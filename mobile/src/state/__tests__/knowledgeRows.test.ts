import type { MediaPick } from '@/core/media/media';

import type { KnowledgeRow } from '../knowledgeChat';
import { toChatRows } from '../knowledgeRows';

const timing = { rulesMs: 0, embedMs: 200, retrieveMs: 10, rerankMs: 0, totalMs: 212.4 };

describe('toChatRows', () => {
  it('maps a top-1 answer to one bubble with its reply text, entry id, sources and latency', () => {
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
        entryId: 'access.from_manizales',
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

  it('tags an urgent banner with the emergency entry whose short it shows', () => {
    const rows: KnowledgeRow[] = [
      {
        id: 'k5',
        role: 'assistant',
        reply: {
          type: 'answer',
          id: 'actions.report_emergency_general',
          title: 'Reporte',
          text: 'Si hay peligro inmediato, marca el 123.',
          sources: [],
          banner: {
            kind: 'urgent_safety',
            text: 'Marca el 123.',
            sourceIds: ['health_safety.national_emergency_number_123'],
          },
        },
      },
    ];
    expect(toChatRows(rows, 'ERR')).toEqual([
      {
        id: 'k5:banner',
        role: 'assistant',
        text: 'Marca el 123.',
        entryId: 'health_safety.national_emergency_number_123',
      },
      {
        id: 'k5',
        role: 'assistant',
        text: 'Si hay peligro inmediato, marca el 123.',
        entryId: 'actions.report_emergency_general',
      },
    ]);
  });

  it('carries the photos to the reply bubble, never to its banner', () => {
    const media: MediaPick = {
      layout: 'single',
      items: [
        {
          id: 'condor',
          common: 'Cóndor de los Andes',
          scientific: 'Vultur gryphus',
          photo: { file: 'condor.1.webp', author: 'Ana', license: 'CC BY 2.0' },
        },
      ],
    };
    const rows: KnowledgeRow[] = [
      {
        id: 'k6',
        role: 'assistant',
        media,
        reply: {
          type: 'answer',
          id: 'fauna.condor',
          title: 'Cóndor',
          text: 'Anida en los riscos.',
          sources: [],
          banner: { kind: 'offline_current_status', text: 'Sin conexión.', sourceIds: [] },
        },
      },
    ];
    const [banner, reply] = toChatRows(rows, 'ERR');
    expect(banner.media).toBeUndefined();
    expect(reply.media).toBe(media);
  });

  it('shows the i18n error text, never the raw error', () => {
    expect(toChatRows([{ id: 'k4', role: 'assistant', error: 'embedder gone' }], 'ERR')).toEqual([
      { id: 'k4', role: 'assistant', text: 'ERR' },
    ]);
  });
});
