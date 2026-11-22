// Port of nevados_bench.fsm.prompts (uniform mode, default extract layout).
import { stableHash } from './tools';
import type { Case, ChatMessage, PromptRequest } from './types';
import type { JsonSchema, World } from './world';

export type FcMode = 'uniform';

/** Python round(): half to even. */
export function pyRound(x: number): number {
  const f = Math.floor(x);
  const diff = x - f;
  if (diff > 0.5) return f + 1;
  if (diff < 0.5) return f;
  return f % 2 === 0 ? f : f + 1;
}

/** Python len(): code points, not UTF-16 units. */
function pyLen(text: string): number {
  let n = 0;
  for (let i = 0; i < text.length; i++) {
    const c = text.charCodeAt(i);
    if (c < 0xdc00 || c > 0xdfff) n++; // count everything but low surrogates
  }
  return n;
}

export function estimateTokens(world: World, text: string): number {
  return pyRound(pyLen(text) / world.json.meta.chars_per_token);
}

// ----------------------------------------------------------------------------- tools

function renderParam(name: string, schema: JsonSchema, required: boolean): string {
  const kind = 'enum' in schema ? (schema.enum as string[]).join('|') : (schema.type ?? 'any');
  return `${name}${required ? '*' : ''}: ${kind}`;
}

/** Side-effect (slot-filling) tools drop `required` so a constrained model can emit a
 * partial call instead of fabricating missing slots. */
export function exposedParameters(world: World, name: string): JsonSchema {
  const spec = world.tools.get(name)!;
  if (!spec.has_side_effects) return spec.parameters;
  const { required: _required, ...rest } = spec.parameters;
  return rest;
}

export function renderToolsCompact(world: World, toolNames: string[]): string {
  const tag = world.json.meta.partial_tag;
  const lines = [
    `Herramientas disponibles (* = argumento obligatorio; ${tag} = llámala aunque falten datos):`,
  ];
  for (const name of toolNames) {
    const spec = world.tools.get(name)!;
    const props: Record<string, JsonSchema> = spec.parameters.properties ?? {};
    const req = new Set<string>(spec.parameters.required ?? []);
    const args = Object.entries(props)
      .map(([k, v]) => renderParam(k, v, req.has(k)))
      .join(', ');
    lines.push(`- ${name}(${args})${spec.has_side_effects ? ` ${tag}` : ''}: ${spec.description}`);
  }
  return lines.join('\n');
}

function closed(schema: JsonSchema): JsonSchema {
  return { ...schema, additionalProperties: false };
}

/** anyOf: one object per visible tool, plus "none" and "clarify". */
export function uniformSchema(world: World, toolNames: string[]): JsonSchema {
  const options: JsonSchema[] = toolNames.map((name) => ({
    type: 'object',
    properties: { tool: { const: name }, args: closed(exposedParameters(world, name)) },
    required: ['tool', 'args'],
    additionalProperties: false,
  }));
  options.push({
    type: 'object',
    properties: { tool: { const: 'none' } },
    required: ['tool'],
    additionalProperties: false,
  });
  options.push({
    type: 'object',
    properties: { tool: { const: 'clarify' }, question: { type: 'string' } },
    required: ['tool', 'question'],
    additionalProperties: false,
  });
  return { anyOf: options };
}

export function extractSchema(world: World, slotName: string): JsonSchema {
  const { description: _description, ...slot } = world.slotSchema(slotName);
  return {
    type: 'object',
    properties: { value: { anyOf: [slot, { type: 'null' }] } },
    required: ['value'],
    additionalProperties: false,
  };
}

// ----------------------------------------------------------------------------- context

export function renderPassage(world: World, passageId: string): string {
  return `[${passageId}] ${world.getPassage(passageId).text}`;
}

/** Deterministic filler selection; depends only on the prefix inputs, never the question. */
function paddingIds(world: World, c: Case, baseTokens: number): string[] {
  if (c.context_level === null || c.context_level === undefined) return [];
  const meta = world.json.meta;
  let budget =
    meta.context_level_tokens[c.context_level] - meta.suffix_allowance_tokens - baseTokens;
  const seed = c.bundle_id || c.passage_ids.join(',');
  const candidates = [...world.filler.keys()]
    .filter((pid) => !c.passage_ids.includes(pid))
    .map((pid) => ({ pid, h: stableHash(`${seed}|${c.context_level}|${pid}`) }))
    .sort((a, b) => (a.h < b.h ? -1 : a.h > b.h ? 1 : 0));
  const chosen: string[] = [];
  for (const { pid } of candidates) {
    if (budget <= 0) break;
    chosen.push(pid);
    budget -= estimateTokens(world, renderPassage(world, pid) + '\n\n');
  }
  return chosen;
}

/** Spread padding evenly over the gaps so real passages keep their relative position. */
function interleave(real: string[], padding: string[]): string[] {
  if (real.length === 0) return [...padding];
  const gaps = real.length + 1;
  const out: string[] = [];
  let start = 0;
  for (let gap = 0; gap < gaps; gap++) {
    const end = pyRound((padding.length * (gap + 1)) / gaps);
    out.push(...padding.slice(start, end));
    start = end;
    if (gap < real.length) out.push(real[gap]);
  }
  return out;
}

export function contextPassageIds(world: World, c: Case, basePrefix: string): string[] {
  const base = basePrefix + c.passage_ids.map((p) => renderPassage(world, p) + '\n\n').join('');
  return interleave([...c.passage_ids], paddingIds(world, c, estimateTokens(world, base)));
}

function contextBlock(world: World, passageIds: string[]): string {
  if (passageIds.length === 0) return '';
  return `Pasajes oficiales:\n\n${passageIds.map((pid) => renderPassage(world, pid)).join('\n\n')}`;
}

// ----------------------------------------------------------------------------- request

export function slotLine(world: World, slotName: string): string {
  const schema = world.slotSchema(slotName);
  let line = `${slotName}: ${world.json.states.slot_labels[slotName] ?? slotName}`;
  if ('enum' in schema) line += `. Valores permitidos: ${(schema.enum as string[]).join(', ')}`;
  return line;
}

function systemPrefix(world: World, c: Case, toolNames: string[]): string {
  const p = world.json.prompts;
  const parts = [p.intro];
  if (c.call_type === 'route')
    parts.push(p.route_rules, p.uniform_format, renderToolsCompact(world, toolNames));
  else if (c.call_type === 'extract') parts.push(p.extract_rules);
  else parts.push(p.answer_rules);
  return parts.join('\n\n');
}

function userContent(world: World, c: Case): string {
  const sections: string[] = [];
  if (c.state_summary) sections.push(`[Estado del trámite]\n${c.state_summary}`);
  if (c.call_type === 'extract') {
    if (!c.slot_name) throw new Error(`extract case ${c.case_id} has no slot_name`);
    sections.push(`[Dato solicitado]\n${slotLine(world, c.slot_name)}`);
  }
  if (sections.length === 0) return c.user_message;
  sections.push(`[Mensaje del usuario]\n${c.user_message}`);
  return sections.join('\n\n');
}

function historyMessages(c: Case): ChatMessage[] {
  return c.history.map((turn) => {
    if (turn.role !== 'user' && turn.role !== 'assistant')
      throw new Error(`case ${c.case_id}: unsupported history role ${turn.role}`);
    return { role: turn.role, content: turn.content ?? '' };
  });
}

export function resolveToolNames(world: World, c: Case): string[] {
  const names =
    c.tool_names.length > 0 ? c.tool_names : (world.json.states.visible_tools[c.fsm_state] ?? []);
  const unknown = names.filter((n) => !world.tools.has(n));
  if (unknown.length > 0) throw new Error(`case ${c.case_id}: unknown tools ${unknown.join(', ')}`);
  return [...names];
}

/** Python build_request(case, world, 'uniform') dumped with exclude_none (same key order). */
export function buildRequest(c: Case, world: World, _mode: FcMode = 'uniform'): PromptRequest {
  const toolNames = c.call_type === 'route' ? resolveToolNames(world, c) : [];
  const prefix = systemPrefix(world, c, toolNames);
  const context = contextBlock(world, contextPassageIds(world, c, prefix));
  const system = context ? `${prefix}\n\n${context}` : prefix;

  const messages: ChatMessage[] = [
    { role: 'system', content: system },
    ...historyMessages(c),
    { role: 'user', content: userContent(world, c) },
  ];

  // Key order follows the Pydantic model so JSON.stringify matches the Python dump.
  let schemaFields: Pick<PromptRequest, 'tool_choice' | 'json_schema'> = {};
  if (c.call_type === 'route') {
    schemaFields = { tool_choice: 'none', json_schema: uniformSchema(world, toolNames) };
  } else if (c.call_type === 'extract') {
    if (!c.slot_name) throw new Error(`extract case ${c.case_id} has no slot_name`);
    schemaFields = { json_schema: extractSchema(world, c.slot_name) };
  }
  return {
    messages,
    ...schemaFields,
    max_tokens: world.json.meta.max_tokens[c.call_type],
    temperature: 0,
    seed: 1234,
    cache_prompt: true,
    extra_body: {},
  };
}
