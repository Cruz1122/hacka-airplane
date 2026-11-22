// Port of nevados_bench.fsm.driver: free-run dialogue executor. The FSM state follows the
// model's own outputs; code validates tool calls, asks for missing slots, confirms before
// side-effect tools and handles cancel / intent switch. With guards on, the deterministic
// guards sit between the model and the FSM (see guards.ts).
import {
  CHECKED_ARGS,
  detectStation,
  groundedArgs,
  guardAnswer,
  guardRoute,
  stationNames,
} from './guards';
import { parseOutput } from './parse';
import { buildRequest, type FcMode } from './prompts';
import * as S from './states';
import { executeTool, type ToolResult } from './tools';
import type {
  CallType,
  Case,
  Completion,
  LLMBackend,
  ParsedOutput,
  PromptRequest,
  ToolCall,
} from './types';
import { ABSTAIN_ES, normalizeText } from './values';
import { loadWorld, pyRepr, regex, type World } from './world';

const D = loadWorld().json.driver;
const AFFIRM = new Set(D.affirm);
const CANCEL = D.cancel;
const FALLBACK = D.fallback;
// A message naming a station or date is a correction of a filled slot only if it says so.
const CORRECTION_RE = regex(D.correction_re);
const TPL = D.templates;
const BOUNDARY_ROUTER_STATES: readonly string[] = [S.ANSWER, S.OUT_OF_SCOPE, S.CLARIFY, S.ROUTER];

// "generate": the model writes the answer from the tool's passages (one more LLM call).
// "extractive": passages verbatim with citations (no LLM call, no value can be fabricated).
export type AnswerMode = 'generate' | 'extractive';

/** One step of a free-run dialogue (an LLM call, or a code-only step). Python StepResult. */
export interface StepResult {
  dialogue_id: string;
  turn_index: number;
  step_index: number;
  kind: 'llm' | 'code';
  call_type: CallType | null;
  path: string[]; // FSM states traversed by this step, first = state before
  request: PromptRequest | null;
  completion: Completion | null;
  parsed: ParsedOutput | null;
  executed_call: ToolCall | null;
  tool_result: ToolResult | null;
  assistant_message: string | null;
  note: string | null;
  slots: Record<string, unknown>; // flow slots after the step
}

interface Flow {
  tool: string;
  slots: Record<string, unknown>;
  pending: string | null;
}

interface LlmFields {
  call_type: CallType;
  request: PromptRequest;
  completion: Completion;
  parsed: ParsedOutput;
}

type RecordFields = Partial<
  Omit<StepResult, 'dialogue_id' | 'turn_index' | 'step_index' | 'kind' | 'path' | 'slots'>
>;

export interface DialogueRunOptions {
  guards?: boolean;
  deviceStation?: string | null;
  answerMode?: AnswerMode;
  /** Off-topic turns get a free model reply and answer guards stop abstaining (demo mode). */
  chat?: boolean;
  mode?: FcMode;
  dialogueId?: string;
}

/** Python str() of a value inside f-strings. */
function pyStr(value: unknown): string {
  return typeof value === 'string' ? value : pyRepr(value);
}

function fill(template: string, values: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (_, key: string) => {
    if (!(key in values)) throw new Error(`template value missing: ${key}`);
    return values[key];
  });
}

/** Follow-up turn for chat-mode replies. It is appended to the route conversation so the
 * ~2k-token route prefix stays in the KV cache (a separate system prompt would evict it and
 * the next route call would pay the full prefill again). */
function chatInstruction(world: World, deviceStation: string | null): string {
  const stations = [...world.stations.values()].map((st) => st.name).join(', ');
  const here = deviceStation ? world.stations.get(deviceStation)?.name : null;
  return [
    'Ninguna herramienta aplica. Ahora responde al visitante directamente en texto natural, sin JSON.',
    `Eres el asistente del Parque Nacional Nevados (estaciones: ${stations}).${here ? ` Estás en la ${here}.` : ''}`,
    'Sé cálido y breve (máximo 3 frases), en el idioma del visitante.',
    'No inventes horarios, precios, teléfonos ni cifras: si piden un dato así, invita a preguntarlo de forma concreta.',
  ].join(' ');
}

/** Python str.capitalize(). */
function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

// Python str.isalnum() without Unicode property escapes (not guaranteed on Hermes): a char
// with case is a letter; normalized text is accent-free so this covers what visitors type.
function isAlnum(ch: string): boolean {
  return /[0-9]/.test(ch) || ch.toLowerCase() !== ch.toUpperCase();
}

function tokens(text: string): string[] {
  const cleaned = Array.from(normalizeText(text), (ch) =>
    isAlnum(ch) || /\s/.test(ch) ? ch : ' ',
  ).join('');
  return cleaned.split(/\s+/).filter(Boolean);
}

export function isCancel(text: string): boolean {
  const norm = tokens(text).join(' ');
  return CANCEL.some((word) => norm.includes(word));
}

export function isAffirmative(text: string): boolean {
  const toks = tokens(text);
  return (
    toks.length > 0 &&
    AFFIRM.has(toks[0]) &&
    toks.length <= D.affirm_max_tokens &&
    !toks.includes('no')
  );
}

export function isPlainNegative(text: string): boolean {
  const toks = tokens(text);
  return toks.length > 0 && toks[0] === 'no' && toks.length <= 2;
}

export class DialogueRun {
  readonly world: World;
  readonly backend: LLMBackend;
  readonly guards: boolean;
  readonly deviceStation: string | null;
  readonly answerMode: AnswerMode;
  readonly chat: boolean;
  readonly mode: FcMode;
  readonly dialogueId: string;
  state: string = S.ROUTER;
  flow: Flow | null = null;
  history: { role: 'user' | 'assistant'; content: string }[] = [];
  steps: StepResult[] = [];
  // Python only sets this from run(); here turn() advances it so app steps are numbered.
  turnIndex = 0;
  language: 'es' | 'en' | 'mixed' = 'es';
  private currentMessage = '';
  // Streaming sink for the current turn; only free-text calls (chat, generated answer) use it.
  private onText: ((textSoFar: string) => void) | null = null;
  // Raw output of the structured calls (route/extract JSON), for a live "thinking" view.
  private onDraft: ((textSoFar: string) => void) | null = null;
  // Latest route call; chat mode continues its conversation to keep the KV prefix warm.
  private lastRoute: LlmFields | null = null;

  constructor(world: World, backend: LLMBackend, opts: DialogueRunOptions = {}) {
    this.world = world;
    this.backend = backend;
    this.guards = opts.guards ?? false;
    this.deviceStation = opts.deviceStation ?? null;
    this.answerMode = opts.answerMode ?? 'generate';
    this.chat = opts.chat ?? false;
    this.mode = opts.mode ?? 'uniform';
    this.dialogueId = opts.dialogueId ?? 'app';
  }

  // ------------------------------------------------------------------ helpers

  private makeCase(callType: CallType, message: string, kw: Partial<Case> = {}): Case {
    return {
      case_id: `${this.dialogueId}-t${this.turnIndex}-s${this.steps.length}`,
      suite: 'free_run',
      call_type: callType,
      fsm_state: this.state,
      user_message: message,
      language: this.language,
      history: [...this.history],
      state_summary: null,
      tool_names: [],
      passage_ids: [],
      context_level: null,
      bundle_id: null,
      slot_name: null,
      gold: {},
      tags: { dialogue_id: this.dialogueId, turn_index: this.turnIndex },
      ...kw,
    };
  }

  private async call(
    c: Case,
    onText?: (textSoFar: string) => void,
  ): Promise<[PromptRequest, Completion, ParsedOutput]> {
    const request = buildRequest(c, this.world, this.mode);
    const completion = await this.backend.complete(request, undefined, onText ?? this.onDraft ?? undefined);
    return [request, completion, parseOutput(completion, c, this.mode)];
  }

  private record(path: string[], kw: RecordFields = {}): StepResult {
    S.checkPath(path);
    const step: StepResult = {
      dialogue_id: this.dialogueId,
      turn_index: this.turnIndex,
      step_index: this.steps.length,
      kind: kw.request ? 'llm' : 'code',
      call_type: null,
      path,
      request: null,
      completion: null,
      parsed: null,
      executed_call: null,
      tool_result: null,
      assistant_message: null,
      note: null,
      ...kw,
      slots: this.flow ? { ...this.flow.slots } : {},
    };
    this.steps.push(step);
    this.state = path[path.length - 1];
    return step;
  }

  private summary(): string | null {
    if (this.flow === null) return null;
    const given =
      Object.entries(this.flow.slots)
        .map(([k, v]) => `${k}=${pyStr(v)}`)
        .join(', ') || TPL.summary_given_none;
    const lines = [
      fill(TPL.summary_flow, { tool: this.flow.tool }),
      fill(TPL.summary_given, { given }),
    ];
    if (this.flow.pending) lines.push(fill(TPL.summary_pending, { pending: this.flow.pending }));
    return lines.join('\n');
  }

  /** [call to act on, unstated required args]. The call is null if it must not run. */
  private guardCall(call: ToolCall): [ToolCall | null, string[]] {
    if (!this.guards) return [call, []];
    // Only the visitor's words ground arguments: an extractive reply quotes whole passages.
    const context = this.history.filter((m) => m.role === 'user').map((m) => m.content);
    const summary = this.summary();
    if (summary) context.push(summary);
    const result = guardRoute('call', [call], {
      userText: this.currentMessage,
      contextTexts: context,
      world: this.world,
      deviceStation: this.deviceStation,
    });
    if (result.missing.length > 0) return [result.partialCalls[0] ?? null, result.missing];
    return [result.calls[0] ?? null, []];
  }

  private routeTools(): string[] {
    return S.visibleTools(this.world, S.ROUTER);
  }

  /** Merge individually valid flow arguments; return the names rejected. */
  private mergeValid(args: Record<string, unknown>): string[] {
    const flow = this.flow!;
    const props: Record<string, unknown> = this.world.tools.get(flow.tool)!.parameters.properties;
    const rejected: string[] = [];
    for (const [name, value] of Object.entries(args)) {
      if (name in props && this.world.validateValue(name, value).length === 0)
        flow.slots[name] = value;
      else rejected.push(name);
    }
    return rejected;
  }

  /** Whether the message explicitly corrects an already filled slot instead of answering
   * the pending one (guards only). Needs a correction cue, a restated filled slot, and no
   * statement of the pending slot; unchecked pending slots (enums) cannot be told apart. */
  private isCorrection(): boolean {
    const flow = this.flow!;
    const message = this.currentMessage;
    const pending = flow.pending;
    if (!CORRECTION_RE.test(normalizeText(message))) return false;
    if (pending === null || !CHECKED_ARGS.includes(pending)) return false;
    const stated = groundedArgs(message, this.world);
    if (pending in stated) return false;
    const filled = flow.slots;
    const station = detectStation(message, stationNames(this.world), true);
    if (station !== null && 'station' in filled && station !== filled.station) return true;
    const props: Record<string, unknown> = this.world.tools.get(flow.tool)!.parameters.properties;
    return Object.keys(stated).some(
      (name) => name in props && name in filled && name !== 'station' && name !== 'trail_id',
    );
  }

  private nextMissing(): string | null {
    const flow = this.flow!;
    return S.REQUIRED_SLOTS[flow.tool].find((s) => !(s in flow.slots)) ?? null;
  }

  private confirmText(): string {
    const flow = this.flow!;
    const details = Object.entries(flow.slots)
      .map(([k, v]) => `${S.SLOT_LABELS[k] ?? k}: ${pyStr(v)}`)
      .join(', ');
    const label = S.TOOL_LABELS[flow.tool] ?? flow.tool;
    return fill(TPL.confirm, { label, details });
  }

  /** [next state, assistant message] after slots changed: ask next slot or confirm. */
  private advanceFlow(): [string, string] {
    const missing = this.nextMissing();
    this.flow!.pending = missing;
    if (missing) return [S.SLOT_FILLING, S.SLOT_QUESTIONS[missing]];
    return [S.CONFIRM, this.confirmText()];
  }

  // ----------------------------------------------------------------- dispatch

  /** Act on a routed tool call from ROUTER. Records the routing step; may run an answer
   * step. Returns the assistant message of the turn. */
  private async dispatch(callIn: ToolCall, path: string[], llm: LlmFields): Promise<string> {
    const world = this.world;
    const [guarded, unstated] = this.guardCall(callIn);
    if (guarded === null) {
      this.record([...path, S.CLARIFY], {
        assistant_message: FALLBACK,
        note: 'guard_blocked',
        ...llm,
      });
      return FALLBACK;
    }
    if (unstated.length > 0 && !(guarded.name in S.FLOW_STATE)) {
      // A query with an unstated argument: ask for it instead of guessing.
      const message = S.SLOT_QUESTIONS[unstated[0]] ?? FALLBACK;
      const note = `guard_missing=${pyRepr(unstated)}`;
      this.record([...path, S.CLARIFY], { assistant_message: message, note, ...llm });
      return message;
    }
    const call = guarded; // flows ask for the unstated slots themselves
    if (!this.routeTools().includes(call.name)) {
      this.record([...path, S.CLARIFY], {
        assistant_message: FALLBACK,
        note: 'unknown_tool',
        ...llm,
      });
      return FALLBACK;
    }
    if (call.name in S.FLOW_STATE) {
      this.flow = { tool: call.name, slots: {}, pending: null };
      const rejected = this.mergeValid(call.arguments);
      const [nxt, message] = this.advanceFlow();
      const route = [...path, S.FLOW_STATE[call.name], S.SLOT_FILLING];
      if (nxt === S.CONFIRM) route.push(S.CONFIRM);
      const note = rejected.length > 0 ? `rejected_args=${pyRepr(rejected)}` : null;
      this.record(route, { assistant_message: message, note, ...llm });
      return message;
    }
    const errors = world.validateArguments(call.name, call.arguments);
    if (errors.length > 0) {
      const missing = world.missingRequired(call.name, call.arguments);
      const message = missing.length > 0 ? (S.SLOT_QUESTIONS[missing[0]] ?? FALLBACK) : FALLBACK;
      this.record([...path, S.CLARIFY], {
        assistant_message: message,
        note: errors.join('; '),
        ...llm,
      });
      return message;
    }
    const topic = S.toolTopic(world, call.name);
    const result = executeTool(world, call);
    this.record([...path, topic], { executed_call: call, tool_result: result, ...llm });
    return this.answer(result, call);
  }

  /** The official passages verbatim, each with its citation; no model call. */
  private extractiveAnswer(result: ToolResult): string {
    const data = (result.ok && result.data) || {};
    const lines = Object.entries(data).map(
      ([k, v]) => `${capitalize(k.replace(/_/g, ' '))}: ${pyStr(v)}.`,
    );
    for (const pid of result.ok ? result.passage_ids : [])
      lines.push(`${this.world.getPassage(pid).text} [fuente: ${pid}]`);
    return lines.length > 0 ? lines.join('\n') : ABSTAIN_ES;
  }

  private async answer(result: ToolResult, call: ToolCall | null = null): Promise<string> {
    if (this.answerMode === 'extractive') {
      const message = this.extractiveAnswer(result);
      this.record([this.state, S.ANSWER], { assistant_message: message, note: 'extractive' });
      return message;
    }
    const data = (result.ok && result.data) || {};
    const entries = Object.entries(data);
    const summary =
      entries.length > 0
        ? TPL.summary_tool_result + entries.map(([k, v]) => `${k}=${pyStr(v)}`).join(', ')
        : null;
    const c = this.makeCase('answer', this.currentMessage, {
      passage_ids: result.ok ? [...result.passage_ids] : [],
      state_summary: summary,
    });
    const [request, completion, parsed] =
      this.chat && this.lastRoute
        ? await this.answerFromRoute(c, this.lastRoute)
        : await this.call(c, this.onText ?? undefined);
    let message = parsed.answer_text || ABSTAIN_ES;
    let note: string | null = null;
    if (this.guards && !this.chat) {
      const spec = call ? this.world.tools.get(call.name) : undefined;
      let station = (call?.arguments.station as string | undefined) ?? null;
      if (station === null && call !== null && 'trail_id' in call.arguments) {
        station = this.world.trails.get(call.arguments.trail_id as string)?.station ?? null;
      }
      const checked = guardAnswer(message, {
        userMessage: this.currentMessage,
        shown: new Map(c.passage_ids.map((pid) => [pid, this.world.getPassage(pid)])),
        targetStation: station || this.deviceStation,
        gazetteer: this.world.json.gazetteer,
        safety: Boolean(spec?.safety),
      });
      if (!checked.passed) {
        message = checked.text;
        note = `guard_answer=${pyRepr(checked.reasons)}`;
      }
    }
    this.record([this.state, S.ANSWER], {
      call_type: 'answer',
      request,
      completion,
      parsed,
      assistant_message: message,
      note,
    });
    return message;
  }

  /** Chat-mode generated answer: the official passages go in a follow-up turn of the route
   * conversation instead of the separate answer prompt, so the route prefix stays cached. */
  private async answerFromRoute(
    c: Case,
    route: LlmFields,
  ): Promise<[PromptRequest, Completion, ParsedOutput]> {
    const passages = c.passage_ids
      .map((pid) => `[${pid}] ${this.world.getPassage(pid).text}`)
      .join('\n');
    const facts = [c.state_summary, passages].filter(Boolean).join('\n');
    const request: PromptRequest = {
      messages: [
        ...route.request.messages,
        { role: 'assistant', content: route.completion.content },
        {
          role: 'user',
          content:
            `Datos oficiales:\n${facts || '(ninguno)'}\n\n` +
            'Responde al visitante en texto natural, sin JSON, breve y en su idioma, usando solo estos datos. ' +
            'Cita cada dato con [fuente: ID]. Si los datos no responden la pregunta, dilo.',
        },
      ],
      max_tokens: 200,
      temperature: 0.2,
    };
    const completion = await this.backend.complete(request, undefined, this.onText ?? undefined);
    return [request, completion, parseOutput(completion, c, this.mode)];
  }

  /** Free reply for turns no tool covers (greetings, small talk, open questions). */
  private async chatReply(path: string[], routeLlm: LlmFields): Promise<string> {
    this.record([...path, S.OUT_OF_SCOPE], { note: 'chat', ...routeLlm });
    const routeRequest = routeLlm.request;
    const request: PromptRequest = {
      messages: [
        ...routeRequest.messages,
        { role: 'assistant', content: routeLlm.completion.content },
        { role: 'user', content: chatInstruction(this.world, this.deviceStation) },
      ],
      max_tokens: 160,
      temperature: 0.3,
      top_p: 0.9,
    };
    const completion = await this.backend.complete(request, undefined, this.onText ?? undefined);
    const message = completion.content.trim() || ABSTAIN_ES;
    this.record([S.OUT_OF_SCOPE], {
      call_type: 'answer',
      request,
      completion,
      assistant_message: message,
      note: 'chat',
    });
    return message;
  }

  private async route(path: string[]): Promise<string> {
    const c = this.makeCase('route', this.currentMessage, {
      tool_names: this.routeTools(),
      state_summary: this.summary(),
    });
    const [request, completion, parsed] = await this.call(c);
    const llm: LlmFields = { call_type: 'route', request, completion, parsed };
    this.lastRoute = llm;
    if (!parsed.parse_ok) {
      this.record([...path, S.CLARIFY], {
        assistant_message: FALLBACK,
        note: 'parse_error',
        ...llm,
      });
      return FALLBACK;
    }
    if (parsed.decision === 'none') {
      if (this.chat) return this.chatReply(path, llm);
      const message = parsed.answer_text || ABSTAIN_ES;
      this.record([...path, S.OUT_OF_SCOPE], { assistant_message: message, ...llm });
      return message;
    }
    if (parsed.decision === 'clarify') {
      const message = parsed.answer_text || FALLBACK;
      this.record([...path, S.CLARIFY], { assistant_message: message, ...llm });
      return message;
    }
    return this.dispatch(parsed.calls[0], path, llm);
  }

  // ------------------------------------------------------------------ states

  private turnRouter(): Promise<string> {
    return this.route(this.state === S.ROUTER ? [this.state] : [this.state, S.ROUTER]);
  }

  private async turnSlotFilling(): Promise<string> {
    const flow = this.flow;
    if (flow === null || flow.pending === null)
      throw new Error('SLOT_FILLING without a pending slot');
    const message = this.currentMessage;
    if (isCancel(message)) {
      this.flow = null;
      const reply = TPL.slot_cancel_reply;
      this.record([S.SLOT_FILLING, S.ROUTER], { assistant_message: reply, note: 'cancel' });
      return reply;
    }
    const slot = flow.pending;
    const c = this.makeCase('extract', message, { slot_name: slot, state_summary: this.summary() });
    const [request, completion, parsed] = await this.call(c);
    const llm: LlmFields = { call_type: 'extract', request, completion, parsed };
    const value = parsed.slot_value;
    // The model tends to fabricate a pending value when the visitor corrects another slot;
    // discard it so the flow router sees the turn (r2 dlg-13, dlg-18).
    const correction = this.guards && this.isCorrection();
    const valid =
      parsed.parse_ok &&
      value !== null &&
      value !== undefined &&
      this.world.validateValue(slot, value).length === 0;
    if (valid && !correction) {
      flow.slots[slot] = value;
      const [nxt, reply] = this.advanceFlow();
      this.record([S.SLOT_FILLING, nxt], { assistant_message: reply, ...llm });
      return reply;
    }
    // Slot not given: record the extract, then let the router decide whether the user
    // switched intent, corrected another slot, or just did not answer.
    const note = correction ? 'correction_detected' : 'slot_not_extracted';
    this.record([S.SLOT_FILLING, S.SLOT_FILLING], { note, ...llm });
    return this.flowReroute(S.SLOT_FILLING, this.routeTools());
  }

  private async flowReroute(origin: string, toolNames: string[]): Promise<string> {
    const flow = this.flow!;
    const c = this.makeCase('route', this.currentMessage, {
      tool_names: toolNames,
      state_summary: this.summary(),
    });
    const [request, completion, parsed] = await this.call(c);
    const llm: LlmFields = { call_type: 'route', request, completion, parsed };
    this.lastRoute = llm;
    let call: ToolCall | null =
      parsed.parse_ok && parsed.decision === 'call' ? parsed.calls[0] : null;
    if (call !== null && call.name === flow.tool && this.guards) {
      [call] = this.guardCall(call); // merge only the arguments the user stated
    }
    if (call !== null && call.name !== flow.tool && toolNames.includes(call.name)) {
      // Intent switch: abandon the flow and handle the new call from ROUTER.
      this.flow = null;
      return this.dispatch(call, [origin, S.ROUTER], llm);
    }
    const route = origin === S.CONFIRM ? [origin, S.SLOT_FILLING] : [origin];
    if (call !== null && call.name === flow.tool) {
      const rejected = this.mergeValid(call.arguments);
      const [nxt, reply] = this.advanceFlow();
      route.push(nxt);
      const note =
        rejected.length > 0 ? `correction; rejected_args=${pyRepr(rejected)}` : 'correction';
      this.record(route, { assistant_message: reply, note, ...llm });
      return reply;
    }
    // Nothing usable: ask again for the pending slot (or the confirmation).
    const [nxt, reply] = this.advanceFlow();
    route.push(nxt);
    this.record(route, { assistant_message: reply, note: 'reask', ...llm });
    return reply;
  }

  private async turnConfirm(): Promise<string> {
    const flow = this.flow;
    if (flow === null) throw new Error('CONFIRM without a flow');
    const message = this.currentMessage;
    if (isAffirmative(message)) {
      const call: ToolCall = { name: flow.tool, arguments: { ...flow.slots } };
      const result = executeTool(this.world, call);
      let reply: string;
      if (result.ok) {
        const code = result.data.codigo_registro || result.data.codigo_reporte;
        reply = fill(TPL.done, { label: S.TOOL_LABELS[flow.tool], code: pyStr(code ?? null) });
      } else {
        reply = fill(TPL.failed, { error: result.error });
      }
      this.record([S.CONFIRM, S.EXECUTE, S.ANSWER], {
        executed_call: call,
        tool_result: result,
        assistant_message: reply,
      });
      this.flow = null;
      return reply;
    }
    if (isCancel(message) || isPlainNegative(message)) {
      this.flow = null;
      const reply = TPL.confirm_cancel_reply;
      this.record([S.CONFIRM, S.ROUTER], { assistant_message: reply, note: 'cancel' });
      return reply;
    }
    // Correction: let the model restate the flow call with the corrected arguments.
    return this.flowReroute(S.CONFIRM, [flow.tool]);
  }

  // -------------------------------------------------------------------- loop

  /** Handle one user message from the current state; returns the assistant reply. */
  async turn(
    message: string,
    onText?: (textSoFar: string) => void,
    onDraft?: (textSoFar: string) => void,
  ): Promise<string> {
    this.currentMessage = message;
    this.onText = onText ?? null;
    this.onDraft = onDraft ?? null;
    let reply: string;
    if (BOUNDARY_ROUTER_STATES.includes(this.state)) {
      reply = await this.turnRouter();
    } else if (this.state === S.SLOT_FILLING) {
      reply = await this.turnSlotFilling();
    } else if (this.state === S.CONFIRM) {
      reply = await this.turnConfirm();
    } else {
      throw new Error(`turn started in non-boundary state ${this.state}`);
    }
    this.history.push({ role: 'user', content: message }, { role: 'assistant', content: reply });
    this.turnIndex += 1;
    return reply;
  }
}

/** Minimal Python Dialogue shape run_dialogue needs. */
export interface Dialogue {
  dialogue_id: string;
  turns: { user_message: string; steps?: { language?: 'es' | 'en' | 'mixed' }[] }[];
}

/** Run `dialogue` free-running: FSM state follows the model's own outputs. */
export async function runDialogue(
  dialogue: Dialogue,
  backend: LLMBackend,
  world: World,
  opts: Omit<DialogueRunOptions, 'dialogueId'> = {},
): Promise<StepResult[]> {
  const run = new DialogueRun(world, backend, { ...opts, dialogueId: dialogue.dialogue_id });
  for (const [index, turn] of dialogue.turns.entries()) {
    run.turnIndex = index;
    const language = turn.steps?.[0]?.language;
    if (language) run.language = language;
    await run.turn(turn.user_message);
  }
  return run.steps;
}
