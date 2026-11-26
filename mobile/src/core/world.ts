// Port of nevados_bench.world.model.World over the generated world.json.
import worldJson from '../../assets/data/world.json';

export interface RegexSpec {
  source: string;
  flags: string; // 'i' | 's' | '' (Python flags)
}

export interface Station {
  id: string;
  name: string;
  code: string;
  trails: string[];
}

export interface Trail {
  id: string;
  name: string;
  station: string;
  length_m: number;
  duration_min: number;
  difficulty: string;
}

export type JsonSchema = Record<string, any>;

export interface ToolSpec {
  name: string;
  description: string;
  parameters: JsonSchema;
  has_side_effects: boolean;
  safety: boolean;
  near_duplicate_of: string | null;
  fsm_states: string[];
}

export interface Passage {
  id: string;
  station: string | null;
  field: string;
  text: string;
  values: string[];
  safety: boolean;
  prior_values: string[];
}

export interface GazetteerEntry {
  value: string;
  passage_id: string;
  station: string | null;
  field: string;
}

export type DataSpec =
  | { key: string; kind: 'hash_mod4_nonzero' | 'station_trail_ids' | 'item_allowed' }
  | { key: string; kind: 'hash_choice'; choices: 'trail_status' | 'forecast' }
  | { key: string; kind: 'altitude_limit'; passage_id: string }
  | { key: string; kind: 'letter_code'; prefix: string };

export interface ExecRule {
  st?: string[];
  park?: string[];
  fee_by_visitor_type?: boolean;
  trail_passage?: boolean;
  item_rule?: boolean;
  procedure_by_emergency_type?: boolean;
  data?: DataSpec;
}

export interface ExecTable {
  park_passages: Record<string, string>;
  item_rules: Record<string, { passage_id: string; allowed: boolean }>;
  fee_field: Record<string, string>;
  trail_status: string[];
  forecast: string[];
  procedures: Record<string, ({ st: string } | { park: string })[]>;
  rules: Record<string, ExecRule>;
  hash_vectors: { text: string; value: string }[];
}

export interface WorldJson {
  meta: {
    park_name: string;
    reference_date: string;
    chars_per_token: number;
    suffix_allowance_tokens: number;
    max_tokens: { route: number; extract: number; answer: number };
    context_level_tokens: Record<string, number>;
    partial_tag: string;
    injection_field: string;
  };
  stations: Station[];
  trails: Trail[];
  tools: ToolSpec[];
  base_tools: string[];
  passages: Passage[];
  filler: Passage[];
  gazetteer: GazetteerEntry[];
  passage_index: Record<string, string[]>;
  slot_schemas: Record<string, JsonSchema>;
  exec: ExecTable;
  states: {
    all: string[];
    topic: string[];
    transitions: Record<string, string[]>;
    flow_state: Record<string, string>;
    required_slots: Record<string, string[]>;
    slot_labels: Record<string, string>;
    slot_questions: Record<string, string>;
    tool_labels: Record<string, string>;
    visible_tools: Record<string, string[]>;
    tool_topic: Record<string, string>;
  };
  prompts: {
    intro: string;
    route_rules: string;
    uniform_format: string;
    extract_rules: string;
    answer_rules: string;
  };
  values: {
    abstain_es: string;
    abstain_en: string;
    abstain_patterns: string[];
    time_re: RegexSpec;
    number_re: RegexSpec;
    citation_re: RegexSpec;
  };
  parse: { think_re: RegexSpec; tool_markup_re: RegexSpec };
  grounding: { small_number_limit: number; enum_line_re: RegexSpec; enum_paren_re: RegexSpec };
  guards: Record<string, any>;
  driver: {
    affirm: string[];
    affirm_max_tokens: number;
    cancel: string[];
    fallback: string;
    correction_re: RegexSpec;
    templates: Record<string, string>;
  };
}

/** JS RegExp from an exported Python pattern. A leading inline `(?m)` (JS has no global
 * inline flags) becomes the `m` flag. Python's Unicode `\w`/`\b` become ASCII: callers
 * apply them to normalized (accent-free) text. */
export function regex(spec: RegexSpec, extraFlags = ''): RegExp {
  let source = spec.source;
  let flags = spec.flags + extraFlags;
  if (source.startsWith('(?m)')) {
    source = source.slice(4);
    flags += 'm';
  }
  return new RegExp(source, flags);
}

// --------------------------------------------------------------------------- Python repr

const PY_ESCAPES: Record<string, string> = { '\\': '\\\\', '\n': '\\n', '\r': '\\r', '\t': '\\t' };

/** Python repr() of a str (quote choice and escapes of non-printable characters). */
export function pyStrRepr(s: string): string {
  const quote = s.includes("'") && !s.includes('"') ? '"' : "'";
  let out = quote;
  for (const ch of s) {
    const cp = ch.codePointAt(0)!;
    if (ch in PY_ESCAPES) out += PY_ESCAPES[ch];
    else if (ch === quote) out += '\\' + quote;
    else if (cp < 0x20 || (cp >= 0x7f && cp <= 0xa0) || cp === 0xad)
      out += '\\x' + cp.toString(16).padStart(2, '0');
    else if (
      (cp >= 0x2000 && cp <= 0x200f) ||
      (cp >= 0x2028 && cp <= 0x202f) ||
      (cp >= 0x205f && cp <= 0x206f) ||
      cp === 0x3000 ||
      cp === 0xfeff
    )
      out += '\\u' + cp.toString(16).padStart(4, '0');
    else out += ch;
  }
  return out + quote;
}

/** Python repr()/str() of a JSON value (numbers that are integers print as Python ints). */
export function pyRepr(value: unknown): string {
  if (value === null || value === undefined) return 'None';
  if (typeof value === 'boolean') return value ? 'True' : 'False';
  if (typeof value === 'string') return pyStrRepr(value);
  if (typeof value === 'number') return String(value);
  if (Array.isArray(value)) return `[${value.map(pyRepr).join(', ')}]`;
  const entries = Object.entries(value as Record<string, unknown>);
  return `{${entries.map(([k, v]) => `${pyStrRepr(k)}: ${pyRepr(v)}`).join(', ')}}`;
}

// --------------------------------------------------------------------------- validation

export function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isType(value: unknown, type: string): boolean {
  switch (type) {
    case 'string':
      return typeof value === 'string';
    case 'integer':
      // JSON cannot tell 4 from 4.0 here; Python jsonschema accepts both as integer.
      return typeof value === 'number' && Number.isInteger(value);
    case 'number':
      return typeof value === 'number';
    case 'boolean':
      return typeof value === 'boolean';
    case 'object':
      return isPlainObject(value);
    case 'array':
      return Array.isArray(value);
    case 'null':
      return value === null;
    default:
      throw new Error(`unsupported JSON schema type: ${type}`);
  }
}

/** Errors of Draft202012Validator.iter_errors for the keyword subset world.json uses,
 * in schema keyword order, with jsonschema's message text. */
function schemaErrors(schema: JsonSchema, value: unknown): string[] {
  const errors: string[] = [];
  for (const [keyword, arg] of Object.entries(schema)) {
    if (keyword === 'type') {
      if (!isType(value, arg)) errors.push(`${pyRepr(value)} is not of type ${pyStrRepr(arg)}`);
    } else if (keyword === 'enum') {
      if (!(arg as unknown[]).some((v) => v === value))
        errors.push(`${pyRepr(value)} is not one of ${pyRepr(arg)}`);
    } else if (keyword === 'properties') {
      if (!isPlainObject(value)) continue;
      for (const [prop, sub] of Object.entries(arg as Record<string, JsonSchema>)) {
        if (prop in value) errors.push(...schemaErrors(sub, value[prop]));
      }
    } else if (keyword === 'required') {
      if (!isPlainObject(value)) continue;
      for (const prop of arg as string[]) {
        if (!(prop in value)) errors.push(`${pyStrRepr(prop)} is a required property`);
      }
    } else if (keyword !== 'description') {
      throw new Error(`unsupported JSON schema keyword: ${keyword}`);
    }
  }
  return errors;
}

const DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

function isLeap(y: number): boolean {
  return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
}

/** Python `len(v) == 10 and date.fromisoformat(v)` (3.11+: also ISO week dates). */
export function isIsoDate(value: unknown): boolean {
  if (typeof value !== 'string' || value.length !== 10) return false;
  let m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (m) {
    const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
    if (y < 1 || mo < 1 || mo > 12 || d < 1) return false;
    const max = mo === 2 && isLeap(y) ? 29 : DAYS_IN_MONTH[mo - 1];
    return d <= max;
  }
  m = /^(\d{4})-W(\d{2})-(\d)$/.exec(value);
  if (!m) return false;
  const [y, w, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  if (y < 1 || w < 1 || d < 1 || d > 7) return false;
  if (w < 53) return true;
  // Week 53 exists when Jan 1 is a Thursday, or a Wednesday in a leap year.
  const jan1 = new Date(Date.UTC(y, 0, 1));
  jan1.setUTCFullYear(y);
  const dow = jan1.getUTCDay();
  return w === 53 && (dow === 4 || (dow === 3 && isLeap(y)));
}

// --------------------------------------------------------------------------- World

export class World {
  readonly json: WorldJson;
  readonly stations: Map<string, Station>;
  readonly trails: Map<string, Trail>;
  readonly tools: Map<string, ToolSpec>; // catalogue order
  readonly passages: Map<string, Passage>;
  readonly filler: Map<string, Passage>;

  constructor(json: WorldJson) {
    this.json = json;
    this.stations = new Map(json.stations.map((s) => [s.id, s]));
    this.trails = new Map(json.trails.map((t) => [t.id, t]));
    this.tools = new Map(json.tools.map((t) => [t.name, t]));
    this.passages = new Map(json.passages.map((p) => [p.id, p]));
    this.filler = new Map(json.filler.map((p) => [p.id, p]));
  }

  get baseTools(): string[] {
    return this.json.base_tools;
  }

  getPassage(passageId: string): Passage {
    const passage = this.passages.get(passageId) ?? this.filler.get(passageId);
    if (!passage) throw new Error(`unknown passage id: ${passageId}`);
    return passage;
  }

  passageIdsFor(station: string | null | undefined, fieldName: string): string[] {
    return [...(this.json.passage_index[`${station ?? ''}|${fieldName}`] ?? [])];
  }

  trailPassageId(trailId: string): string {
    const trail = this.trails.get(trailId);
    if (!trail) throw new Error(`unknown trail: ${trailId}`);
    const pid = this.passageIdsFor(trail.station, 'trail').find((id) =>
      this.getPassage(id).text.includes(trail.name),
    );
    if (!pid) throw new Error(`no passage for trail ${trailId}`);
    return pid;
  }

  stationName(stationId: string): string {
    const station = this.stations.get(stationId);
    if (!station) throw new Error(`unknown station: ${stationId}`);
    return station.name;
  }

  /** JSON Schema of a tool argument (first match across tools, incl. description). */
  slotSchema(slotName: string): JsonSchema {
    const schema = this.json.slot_schemas[slotName];
    if (!schema) throw new Error(`unknown slot: ${slotName}`);
    return schema;
  }

  /** Errors for a single argument value (empty when valid). */
  validateValue(slotName: string, value: unknown): string[] {
    const errors = schemaErrors(this.slotSchema(slotName), value);
    if (errors.length === 0 && slotName === 'date' && !isIsoDate(value))
      errors.push(`${pyRepr(value)} is not an ISO date (YYYY-MM-DD)`);
    return errors;
  }

  /** Errors for a full tool call: schema, unknown arguments and ISO dates. */
  validateArguments(toolName: string, args: unknown): string[] {
    const spec = this.tools.get(toolName);
    if (!spec) return [`unknown tool: ${toolName}`];
    if (!isPlainObject(args)) return ['arguments must be an object'];
    const errors = schemaErrors(spec.parameters, args);
    const known: Record<string, unknown> = spec.parameters.properties ?? {};
    for (const k of Object.keys(args)) if (!(k in known)) errors.push(`unexpected argument: ${k}`);
    if ('date' in args && 'date' in known && !isIsoDate(args.date))
      errors.push(`${pyRepr(args.date)} is not an ISO date (YYYY-MM-DD)`);
    return errors;
  }

  missingRequired(toolName: string, args: Record<string, unknown>): string[] {
    const spec = this.tools.get(toolName);
    if (!spec) throw new Error(`unknown tool: ${toolName}`);
    return ((spec.parameters.required ?? []) as string[]).filter((name) => !(name in args));
  }
}

let cached: World | null = null;

export function loadWorld(): World {
  cached ??= new World(worldJson as unknown as WorldJson);
  return cached;
}
