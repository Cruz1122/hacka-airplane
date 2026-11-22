import { readFileSync } from 'node:fs';
import { join } from 'node:path';

import { parseOutput, stripReasoning } from '../parse';
import { buildRequest, estimateTokens, pyRound } from '../prompts';
import type { Case, PromptRequest } from '../types';
import { loadWorld } from '../world';

// Read with fs, not import: tsc would otherwise infer types for 13 MB of JSON.
const fixture = <T>(name: string): T =>
  JSON.parse(readFileSync(join(__dirname, '..', '__fixtures__', name), 'utf8')) as T;

const world = loadWorld();
const prompts = fixture<{ case: Case; request: PromptRequest }[]>('prompts.json');

describe('buildRequest parity with Python build_request (prompts.json)', () => {
  it('covers every call type and padded contexts', () => {
    expect(prompts.length).toBeGreaterThan(1000);
    const kinds = new Set(prompts.map((p) => p.case.call_type));
    expect([...kinds].sort()).toEqual(['answer', 'extract', 'route']);
    expect(prompts.some((p) => p.case.context_level !== null)).toBe(true);
  });

  it.each(prompts.map((p, i) => [`${i} ${p.case.case_id}`, p] as const))('%s', (_id, p) => {
    const request = buildRequest(p.case, world, 'uniform');
    expect(request).toEqual(p.request);
    // Byte parity including key order (llama.cpp sees the serialized schema).
    expect(JSON.stringify(request)).toBe(JSON.stringify(p.request));
  });
});

describe('Python rounding helpers', () => {
  it('rounds half to even', () => {
    expect([0.5, 1.5, 2.5, 3.5, 2.4999, 2.5001].map(pyRound)).toEqual([0, 2, 2, 4, 2, 3]);
  });
  it('counts code points like len()', () => {
    expect(estimateTokens(world, '😀'.repeat(9))).toBe(2); // 9 / 3.6 = 2.5 -> 2
  });
});

describe('parseOutput (uniform)', () => {
  const route = { call_type: 'route' } as const;
  const extract = { call_type: 'extract' } as const;
  const answer = { call_type: 'answer' } as const;
  const parse = (content: string, c: Pick<Case, 'call_type'>) => parseOutput({ content }, c);

  it('parses route calls, none and clarify', () => {
    expect(
      parse('{"tool": "get_opening_hours", "args": {"station": "alto_cenizo"}}', route),
    ).toEqual({
      parse_ok: true,
      decision: 'call',
      calls: [{ name: 'get_opening_hours', arguments: { station: 'alto_cenizo' } }],
      slot_value: null,
      answer_text: null,
      parse_error: null,
    });
    expect(parse('{"tool": "register_visit"}', route).calls).toEqual([
      { name: 'register_visit', arguments: {} },
    ]);
    expect(parse(' {"tool": "none"} ', route)).toMatchObject({
      parse_ok: true,
      decision: 'none',
      calls: [],
    });
    expect(parse('<think>x</think>{"tool": "clarify", "question": "¿Cuál?"}', route)).toMatchObject(
      {
        parse_ok: true,
        decision: 'clarify',
        answer_text: '¿Cuál?',
      },
    );
  });

  it('rejects malformed route output with Python error texts', () => {
    expect(parse('{"tool": "clarify"}', route)).toMatchObject({
      parse_ok: false,
      decision: 'clarify',
      parse_error: 'clarify output lacks a string "question"',
    });
    expect(parse('{"tool": 3}', route).parse_error).toBe(
      'route output lacks a string "tool" field',
    );
    expect(parse('{"tool": "x", "args": null}', route).parse_error).toBe('"args" is not an object');
    // Route is strict JSON (not tolerant): prose around the object is an error.
    expect(parse('ok {"tool": "none"}', route).parse_error).toMatch(/^JSONDecodeError: /);
  });

  it('parses extract values tolerantly', () => {
    expect(parse('{"value": 4}', extract)).toMatchObject({ parse_ok: true, slot_value: 4 });
    expect(parse('{"value": null}', extract)).toMatchObject({ parse_ok: true, slot_value: null });
    expect(parse('Claro: {"value": "alto_cenizo"} listo', extract).slot_value).toBe('alto_cenizo');
    expect(parse('{"v": 1}', extract).parse_error).toBe('extract output lacks a "value" field');
    expect(parse('nada', extract).parse_error).toBe('ValueError: no JSON object found in output');
  });

  it('handles answers, timeouts and http errors', () => {
    expect(parse(' Hola <think>tail', answer)).toMatchObject({
      parse_ok: true,
      answer_text: 'Hola',
    });
    expect(parse('  ', answer)).toMatchObject({
      parse_ok: false,
      parse_error: 'empty answer',
      answer_text: '',
    });
    expect(parseOutput({ content: '', timeout: true }, answer).parse_error).toBe('timeout');
    expect(parseOutput({ content: '', http_error: '500' }, answer).parse_error).toBe(
      'http error: 500',
    );
    expect(stripReasoning('<THINK>a\nb</think> x')).toBe('x');
  });

  it('parses every recorded oracle completion in replays.json', () => {
    const replays =
      fixture<
        {
          steps: {
            kind: string;
            call_type: 'route' | 'extract' | 'answer' | null;
            completion_content: string | null;
          }[];
        }[]
      >('replays.json');
    const llm = replays.flatMap((r) => r.steps).filter((s) => s.kind === 'llm' && s.call_type);
    expect(llm.length).toBeGreaterThan(0);
    const bad = llm.filter(
      (s) =>
        !parseOutput({ content: s.completion_content ?? '' }, { call_type: s.call_type! }).parse_ok,
    );
    expect(bad).toEqual([]);
  });
});
