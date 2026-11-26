// Sample content for the /design workshop. On web the model never loads, so these fixtures are
// the only way to see the chat's states; they are samples, not product copy.
import catalog from '@/../assets/data/knowledge/catalog.json';
import type { ChatModel, ChatRow } from '@/chat/ChatView';
import type { CatalogEntry } from '@/core/knowledge/assets';
import { MEDIA } from '@/core/media/bundled';
import { pickMedia, type MediaPick } from '@/core/media/media';
import { loadWorld } from '@/core/world';
import { t } from '@/i18n';
import { toChatRows } from '@/state/knowledgeRows';
import { messageSources } from '@/state/messageSources';

export const READY: ChatModel = { id: 'gemma4-e2b', status: 'ready' };

/** A reply citing two real passages of the app's world, resolved the way the live chat does. */
const TRAIL_REPLY =
  'El Sendero del Pajonal parte de la Estación Refugio Quelital: 2.180 metros, unos 86 minutos ida y regreso, dificultad media. [fuente: EST-D-09] Por ahí se han registrado 97 especies de aves. [fuente: EST-D-24]';

export const TALK: ChatRow[] = [
  { id: '1', role: 'user', text: '¿Qué sendero corto hay en Refugio Quelital?' },
  {
    id: '2',
    role: 'assistant',
    text: TRAIL_REPLY,
    latencyMs: 1840,
    sources: messageSources(TRAIL_REPLY, loadWorld(), ['EST-D-09', 'EST-D-24']),
  },
  { id: '3', role: 'user', text: '¿Necesito guía?' },
  {
    id: '4',
    role: 'assistant',
    text: 'No es obligatorio para ese sendero, pero debes registrar tu visita antes de salir.',
    latencyMs: 920,
  },
];

/**
 * One knowledge-catalog answer with its sources, copied verbatim from
 * assets/data/knowledge/catalog.json (the app does not bundle the catalog yet); a test keeps the
 * copy equal to the catalog.
 */
export const CATALOG_ANSWER = {
  id: 'access.brisas_entry_altitude',
  short:
    'El centro de inducción Brisas está a unos 4100 m. Es la altura de la entrada, no la de la cima ni la del final del carreteable.',
  sources: [
    {
      label: 'Parques Nacionales Naturales de Colombia — Parque Nacional Natural Los Nevados',
      url: 'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/',
      retrieved_at: '2026-11-21',
    },
    {
      label:
        'Parques Nacionales Naturales — Reglamentación transitoria de ecoturismo, PNN Los Nevados, diciembre de 2023',
      url: 'https://www.parquesnacionales.gov.co/wp-content/uploads/2023/12/ANEXO-PNN-NEVADOS.pdf',
      retrieved_at: '2026-11-21',
    },
    {
      label: 'Servicio Geológico Colombiano — Generalidades del volcán Nevado del Ruiz',
      url: 'https://www2.sgc.gov.co/sgc/volcanes/VolcanNevadoRuiz/Paginas/generalidades-volcan-nevado-ruiz.aspx',
      retrieved_at: '2026-11-21',
    },
  ],
};

const REGISTER_REPLY = '¿Para qué fecha? [trámite: admite datos parciales] [fuente: EST-Z-99]';

/** Sources on their own: links that open, a bracket that is prose, a citation nobody retrieved. */
export const SOURCED: ChatRow[] = [
  { id: 's1', role: 'user', text: '¿A qué altura está la entrada de Brisas?' },
  {
    id: 's2',
    role: 'assistant',
    text: CATALOG_ANSWER.short,
    entryId: CATALOG_ANSWER.id,
    latencyMs: 640,
    sources: CATALOG_ANSWER.sources.map((s, i) => ({
      id: `${CATALOG_ANSWER.id}#${i}`,
      title: s.label,
      url: s.url,
      date: s.retrieved_at,
    })),
  },
  { id: 's3', role: 'user', text: 'Quiero registrar la visita.' },
  {
    // No button: the marker is hidden, but EST-Z-99 is no passage the turn retrieved.
    id: 's4',
    role: 'assistant',
    text: REGISTER_REPLY,
    latencyMs: 910,
    sources: messageSources(REGISTER_REPLY, loadWorld(), ['EST-D-01']),
  },
];

function catalogEntry(id: string): CatalogEntry {
  const entry = (catalog as CatalogEntry[]).find((e) => e.id === id);
  if (!entry) throw new Error(`No knowledge catalog entry ${id}`);
  return entry;
}

const EMERGENCY_LINE = catalogEntry('health_safety.national_emergency_number_123');
const REPORT = catalogEntry('actions.report_emergency_general');

/**
 * An urgent question as the live chat maps it (toChatRows): the 123 banner, then a catalog answer
 * with a list, both with their keywords in bold.
 */
export const URGENT: ChatRow[] = toChatRows(
  [
    { id: 'u1', role: 'user', text: 'Mi amigo se cayó en el sendero y no se puede mover.' },
    {
      id: 'u2',
      role: 'assistant',
      timing: { rulesMs: 1, embedMs: 0, retrieveMs: 0, rerankMs: 0, totalMs: 12 },
      reply: {
        type: 'answer',
        id: REPORT.id,
        title: REPORT.label,
        text: REPORT.short,
        sources: REPORT.sources.map((s) => ({ title: s.label, url: s.url, date: s.retrieved_at })),
        verified: false,
        banner: {
          kind: 'urgent_safety',
          text: EMERGENCY_LINE.short,
          sourceIds: [EMERGENCY_LINE.id],
        },
      },
    },
  ],
  t.knowledge.error,
  t.knowledge.locked,
);

/**
 * One answer per gallery layout, from the real catalog and media.json as the live chat maps them;
 * `roll` fixes the dice (0: rows, 0.7: columns).
 */
const PHOTO_TURNS: Record<MediaPick['layout'], { ask: string; topic: string; roll: number }> = {
  single: { ask: '¿Cómo es el cóndor andino?', topic: 'fauna.andean_condor', roll: 0 },
  rows: { ask: '¿Qué aves hay en el parque?', topic: 'fauna.birds_overview', roll: 0 },
  columns: {
    ask: 'Muéstrame los mamíferos del parque',
    topic: 'fauna.mammals_overview',
    roll: 0.7,
  },
};

function photoTurn(layout: MediaPick['layout']): ChatRow[] {
  const { ask, topic, roll } = PHOTO_TURNS[layout];
  const entry = catalogEntry(topic);
  const media = pickMedia(MEDIA, { topicId: topic, userText: ask, afterMedia: false }, () => roll);
  const reply = {
    type: 'answer' as const,
    id: topic,
    title: entry.label,
    text: entry.short,
    verified: false,
  };
  return toChatRows(
    [
      { id: `${layout}/q`, role: 'user', text: ask },
      {
        id: `${layout}/a`,
        role: 'assistant',
        reply: { ...reply, sources: [] },
        ...(media ? { media } : {}),
      },
    ],
    t.knowledge.error,
    t.knowledge.locked,
  );
}

export const PHOTO_THREADS: Record<MediaPick['layout'], ChatRow[]> = {
  single: photoTurn('single'),
  rows: photoTurn('rows'),
  columns: photoTurn('columns'),
};
export const PHOTO_TALK: ChatRow[] = Object.values(PHOTO_THREADS).flat();

export interface ChatScreenState {
  label: string;
  messages: ChatRow[];
  busy?: boolean;
  model?: ChatModel;
}

export const CHAT_STATES: ChatScreenState[] = [
  { label: 'Conversación', messages: TALK },
  { label: 'Fuentes', messages: SOURCED },
  { label: 'Urgencia', messages: URGENT },
  { label: 'Fotos', messages: PHOTO_TALK },
  { label: 'Pensando', messages: TALK.slice(0, 3), busy: true },
  {
    label: 'Larga',
    messages: [TALK[0], { ...TALK[1], id: 'l', text: TALK[1].text.repeat(6), latencyMs: 4100 }],
  },
  {
    label: '40 mensajes',
    messages: Array.from({ length: 40 }, (_, i) => ({ ...TALK[i % 4], id: `m${i}` })),
  },
  { label: 'Sin modelo', messages: [], model: { id: 'gemma4-e2b', status: 'missing' } },
];

/** Texts the composer presets put in the field. */
export const COMPOSER_TEXT = {
  typing: '¿A qué hora abre el centro de visitantes?',
  long: 'Vamos cuatro personas, una de ellas con poca experiencia en altura, y queremos subir al nevado Santa Isabel el sábado. ¿Qué equipo necesitamos y a qué hora conviene salir?',
  pending: '¿Y si llueve durante la caminata?',
};

/** What the Pet "answers" in the composer demo once a send lands. */
export const DEMO_REPLY = 'Mensaje recibido. En la app real aquí llega la respuesta del parque.';

/** How long the composer demo stays in "sending" before the sample reply lands. */
export const DEMO_SEND_MS = 1400;
