// Chat state for the knowledge engine (top-1 curated answers). Plain store so it is testable
// without React; useKnowledge.ts subscribes to it. Never touches modelManager: e5 has its own context.
import type { KnowledgeEngine } from '@/core/knowledge';
import { detectSafety } from '@/core/knowledge/safety';
import type { KnowledgeReply, KnowledgeTiming } from '@/core/knowledge/types';
import { pickMedia, type MediaCatalog, type MediaPick } from '@/core/media/media';
import type { PhotoMatch } from '@/vision/matchPhoto';

export type KnowledgeRow =
  | { id: string; role: 'user'; text: string; photoUri?: string }
  | {
      id: string;
      role: 'assistant';
      reply: KnowledgeReply;
      timing?: KnowledgeTiming;
      /** Photos under the answer, decided once when the reply arrived. */
      media?: MediaPick;
    }
  | { id: string; role: 'assistant'; error: string };

export interface KnowledgeChatState {
  rows: KnowledgeRow[];
  busy: boolean;
  status: 'loading' | 'ready' | 'degraded';
  /** Why the runtime is degraded (missing side-loaded file, native load error). */
  error?: string;
}

type Engine = Pick<KnowledgeEngine, 'ask'> & Partial<Pick<KnowledgeEngine, 'resetContext'>>;
export interface LoadedEngine {
  engine: Engine;
  degraded?: string;
}

export interface KnowledgeChatOptions {
  /** Photos answers may show; without it no answer shows any. */
  media?: MediaCatalog;
  /** The dice for photos, in [0, 1). */
  rng?: () => number;
}

const message = (e: unknown) => (e instanceof Error ? e.message : String(e));

const unknownPhoto = 'No logro identificar lo que hay en tu imagen. ¿Podrías preguntarle a tu guía turístico por esto?';
const editPhoto = 'No puedo editar imágenes. Puedo intentar identificar lo que aparece en la foto.';
const photoRequest = /\b(?:fotos?|fotografias?|imagen(?:es)?|retrato|selfie|fondo)\b/;

function normalizeRequest(text: string): string {
  return text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9 ]/g, ' ').trim().replace(/ +/g, ' ');
}

function requestsPhotoEdit(words: string, hasPhoto: boolean): boolean {
  const request = /^(?:(?:por favor|(?:me )?(?:puedes|podrias)|quiero que|necesito que|quiero|necesito|me ayudas a) )*/;
  const verb = words.replace(request, '').replace(/^(?:me|le|nos|lo|la) /, '');
  if (/^(?:edita\w*|retoc\w*|recort\w*|modific\w*|reemplaz\w*|ajust\w*|transform\w*|mejor\w*|arregl\w*|gira\w*|rot\w*|borra\w*|elimin\w*|quit\w*|pon\w*|agreg\w*|cambi\w*|haz\w*|anad\w*|coloc\w*|aplic\w*)\b/.test(verb)) {
    if (photoRequest.test(verb)) return true;
    return hasPhoto && /^(?:edita\w*|retoc\w*|recort\w*|rot\w*|gira\w*|modifical\w*)(?: |$)|\b(?:sombrero|gafas|lentes|camiseta|filtro|colores?|brillo|contraste|nitidez|blanco y negro|mas alto|mas alta)\b/.test(verb);
  }
  return false;
}

function capabilityReply(text: string): string | undefined {
  const words = normalizeRequest(text);
  const help = /^(?:(?:hola|oye) )?(?:que (?:puedes hacer|sabes hacer|haces|puedo preguntarte|te puedo preguntar)|como funcionas|como te uso|cuales son tus capacidades|ayuda)(?: por favor)?$/.test(words);
  const photo = /\b(?:foto(?:s|grafia|grafias)?|imagen(?:es)?|camara)\b/.test(words)
    && /\b(?:mand\w*|envi\w*|adjunt\w*|sub\w*|carg\w*|seleccion\w*|eleg\w*|acept\w*|recib\w*|identific\w*|reconoc\w*|boton|icono)\b/.test(words);
  const photoControl = /^(?:donde (?:esta|veo|encuentro)|como (?:abro|uso|activo)|puedo usar|tienes) (?:la |tu )?camara$/.test(words);
  if (!(help || photo || photoControl) || detectSafety(text).urgent) return;
  const how = 'Sí. Toca la cámara a la izquierda del cuadro donde escribes. Elige una foto o tómala con la app del celular. Puedes añadir texto antes de tocar Enviar. Puedo sugerir qué aparece si se parece a alguna de mis referencias de Los Nevados.';
  return help ? 'Puedo responder preguntas sobre Los Nevados e intentar identificar fotos del parque. Para enviar una foto, toca la cámara a la izquierda del cuadro donde escribes.' : how;
}

export class KnowledgeChat {
  private state: KnowledgeChatState = { rows: [], busy: false, status: 'loading' };
  private readonly listeners = new Set<() => void>();
  private readonly engine: Promise<Engine>;
  private readonly media: MediaCatalog | undefined;
  private readonly rng: () => number;
  private seq = 0;
  private generation = 0;

  constructor(
    load: () => Promise<LoadedEngine>,
    { media, rng = Math.random }: KnowledgeChatOptions = {},
  ) {
    this.media = media;
    this.rng = rng;
    this.engine = load().then(({ engine, degraded }) => {
      this.set({ status: degraded ? 'degraded' : 'ready', ...(degraded ? { error: degraded } : {}) });
      return engine;
    });
  }

  snapshot = (): KnowledgeChatState => this.state;

  subscribe = (fn: () => void): (() => void) => {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  };

  async ask(text: string): Promise<void> {
    const q = text.trim();
    if (!q || this.state.busy) return;
    this.push({ id: this.id(), role: 'user', text: q }, true);
    const lastUser = this.state.rows.slice(0, -1).findLast(row => row.role === 'user');
    const capability = requestsPhotoEdit(normalizeRequest(q), !!lastUser?.photoUri) && !detectSafety(q).urgent
      ? editPhoto : capabilityReply(q);
    if (capability) {
      this.push({ id: this.id(), role: 'assistant', reply: { type: 'abstain', text: capability } }, false);
      return;
    }
    try {
      const r = await (await this.engine).ask(q);
      const media = this.mediaFor(r.reply, q);
      this.push(
        {
          id: this.id(),
          role: 'assistant',
          reply: r.reply,
          timing: r.timing,
          ...(media ? { media } : {}),
        },
        false,
      );
    } catch (e) {
      this.push({ id: this.id(), role: 'assistant', error: message(e) }, false);
    }
  }

  async askPhoto(photoUri: string, caption: string, classify: () => Promise<PhotoMatch | undefined>): Promise<void> {
    if (this.state.busy) return;
    const generation = this.generation;
    const text = caption.trim();
    const words = normalizeRequest(text);
    this.push({ id: this.id(), role: 'user', text, photoUri }, true);
    try {
      if (text && detectSafety(text).urgent) {
        const result = await (await this.engine).ask(text);
        if (generation === this.generation) {
          this.push({ id: this.id(), role: 'assistant', reply: result.reply, timing: result.timing }, false);
        }
        return;
      }
      if (requestsPhotoEdit(words, true)) {
        this.photoMessage(editPhoto);
        return;
      }
      const match = await classify();
      if (generation !== this.generation) return;
      if (!match) {
        this.photoMessage(unknownPhoto);
        return;
      }
      if ('id' in match) {
        this.push({
          id: this.id(),
          role: 'assistant',
          reply: {
            type: 'answer',
            id: match.id,
            title: match.label,
            text: `La foto se parece a ${match.label}.\n\n${match.description}`,
            sources: [match.source],
          },
        }, false);
        return;
      }
      const identify = /^(?:(?:dime )?que (?:es (?:esto|eso|lo que (?:encontre|vi))|(?:ves|hay)(?: (?:aqui|aca|en (?:esta |la )?(?:foto|imagen)))?)|(?:mira|mire)(?: (?:esto|eso|mi selfie|lo que (?:encontre|vi)))?|identifica (?:esto|la foto)|mirame(?: en (?:esta |la )?foto)?|miranos(?: en (?:esta |la )?foto)?)$/;
      if ('kind' in match) {
        this.photoMessage(!words || identify.test(words)
          ? '¡Te identifico a ti pasándola muy bien en nuestro parque!'
          : unknownPhoto);
        return;
      }
      const useCaption = !!text && !identify.test(words);
      const prompt = `${text.replace(/[:[\]{}]+/g, ' ').replace(/\s+/g, ' ').trim() || 'dime que es esto'} ${match.label}`;
      const engine = await this.engine;
      if (generation !== this.generation) return;
      const result = useCaption
        ? await engine.ask(prompt, match.entryId, true)
        : await engine.ask(prompt, match.entryId);
      if (generation !== this.generation) return;
      const base = result.reply;
      const usesVisualEntry = base.type === 'answer' && base.id === match.entryId;
      const description = usesVisualEntry && 'description' in match ? match.description : undefined;
      const reply: KnowledgeReply = {
        ...base,
        text: [usesVisualEntry ? `La foto se parece a ${match.label}.` : undefined, description, base.text].filter(Boolean).join('\n\n'),
        ...(usesVisualEntry && 'source' in match ? { sources: [match.source, ...base.sources] } : {}),
      };
      this.push({ id: this.id(), role: 'assistant', reply, timing: result.timing }, false);
    } catch {
      if (generation !== this.generation) return;
      this.photoMessage(unknownPhoto);
    }
  }

  /** Clears the chat and the engine's follow-up context, so the next question stands alone. */
  reset(): void {
    this.generation++;
    for (const row of this.state.rows) {
      if (row.role === 'user' && row.photoUri?.startsWith('blob:')) URL.revokeObjectURL(row.photoUri);
    }
    this.set({ rows: [], busy: false });
    // A load failure already surfaced through ask(); nothing to reset then.
    void this.engine.then(
      (e) => e.resetContext?.(),
      () => undefined,
    );
  }

  /**
   * Answers only. The banner row itself never shows photos (toChatRows); an urgent reply shows
   * none at all, while one under the offline-status notice still may.
   */
  private mediaFor(reply: KnowledgeReply, userText: string): MediaPick | null {
    if (!this.media || reply.type !== 'answer' || reply.banner?.kind === 'urgent_safety') {
      return null;
    }
    const previous = this.state.rows.findLast((r) => r.role === 'assistant');
    const afterMedia =
      previous !== undefined && 'reply' in previous && previous.media !== undefined;
    return pickMedia(this.media, { topicId: reply.id, userText, afterMedia }, this.rng);
  }

  private photoMessage(text: string): void {
    this.push({ id: this.id(), role: 'assistant', reply: { type: 'abstain', text } }, false);
  }

  private id(): string {
    return `k${++this.seq}`;
  }

  private push(row: KnowledgeRow, busy: boolean): void {
    this.set({ rows: [...this.state.rows, row], busy });
  }

  private set(patch: Partial<KnowledgeChatState>): void {
    this.state = { ...this.state, ...patch };
    this.listeners.forEach((fn) => fn());
  }
}
