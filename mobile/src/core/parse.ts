// Port of nevados_bench.fsm.parse for the uniform mode. Never throws.
import type { FcMode } from './prompts';
import type { Case, Completion, ParsedOutput } from './types';
import { isPlainObject, loadWorld, regex } from './world';

const THINK_RE = regex(loadWorld().json.parse.think_re, 'g');

function ok(fields: Partial<ParsedOutput>): ParsedOutput {
  return {
    parse_ok: true,
    decision: null,
    calls: [],
    slot_value: null,
    answer_text: null,
    parse_error: null,
    ...fields,
  };
}

function fail(error: string, fields: Partial<ParsedOutput> = {}): ParsedOutput {
  return { ...ok(fields), parse_ok: false, parse_error: error };
}

/** Python-style exception so parse_error reads like the reference ("<Type>: <message>"). */
class PyError extends Error {
  constructor(
    readonly pyType: string,
    message: string,
  ) {
    super(message);
  }
}

/** Drop `<think>` blocks some templates leak into content, plus an unclosed tail. */
export function stripReasoning(text: string): string {
  let out = text.replace(THINK_RE, '');
  const idx = out.toLowerCase().indexOf('<think>');
  if (idx !== -1) out = out.slice(0, idx);
  return out.trim();
}

function jsonLoads(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch (e) {
    // Message text differs from Python's json module; only the type name is kept.
    throw new PyError('JSONDecodeError', (e as Error).message);
  }
}

/** First balanced `{...}` in `text` that decodes as JSON; throws if none. */
export function firstJsonObject(text: string): unknown {
  let start = text.indexOf('{');
  while (start !== -1) {
    let depth = 0;
    let inString = false;
    let escaped = false;
    for (let i = start; i < text.length; i++) {
      const ch = text[i];
      if (inString) {
        if (escaped) escaped = false;
        else if (ch === '\\') escaped = true;
        else if (ch === '"') inString = false;
      } else if (ch === '"') inString = true;
      else if (ch === '{') depth++;
      else if (ch === '}') {
        depth--;
        if (depth === 0) {
          try {
            return JSON.parse(text.slice(start, i + 1));
          } catch {
            break; // not JSON: retry from the next '{'
          }
        }
      }
    }
    start = text.indexOf('{', start + 1);
  }
  throw new PyError('ValueError', 'no JSON object found in output');
}

function decode(text: string, tolerant: boolean): unknown {
  if (!tolerant) return jsonLoads(text);
  try {
    return jsonLoads(text);
  } catch {
    return firstJsonObject(text);
  }
}

function parseRouteJson(obj: unknown): ParsedOutput {
  if (!isPlainObject(obj) || typeof obj.tool !== 'string')
    return fail('route output lacks a string "tool" field');
  const tool = obj.tool;
  if (tool === 'none') return ok({ decision: 'none' });
  if (tool === 'clarify') {
    const question = obj.question;
    if (typeof question !== 'string')
      return fail('clarify output lacks a string "question"', { decision: 'clarify' });
    return ok({ decision: 'clarify', answer_text: question });
  }
  const args = 'args' in obj ? obj.args : {};
  if (!isPlainObject(args)) return fail('"args" is not an object');
  return ok({ decision: 'call', calls: [{ name: tool, arguments: args }] });
}

export function parseOutput(
  completion: Completion,
  c: Pick<Case, 'call_type'>,
  _mode: FcMode = 'uniform',
): ParsedOutput {
  if (completion.timeout) return fail('timeout');
  if (completion.http_error) return fail(`http error: ${completion.http_error}`);
  try {
    if (c.call_type === 'route') {
      return parseRouteJson(decode(stripReasoning(completion.content), false));
    }
    if (c.call_type === 'extract') {
      const obj = decode(stripReasoning(completion.content), true);
      if (!isPlainObject(obj) || !('value' in obj))
        return fail('extract output lacks a "value" field');
      return ok({ slot_value: obj.value });
    }
    const text = stripReasoning(completion.content);
    if (!text) return fail('empty answer', { answer_text: '' });
    return ok({ answer_text: text });
  } catch (e) {
    if (e instanceof PyError) return fail(`${e.pyType}: ${e.message}`);
    throw e;
  }
}
