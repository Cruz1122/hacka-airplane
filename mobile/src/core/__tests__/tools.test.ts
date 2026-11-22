import { readFileSync } from 'node:fs';
import { join } from 'node:path';

import { executeTool, stableHash, toolKey } from '../tools';
import type { ToolCall } from '../types';
import {
  evidenceValues,
  extractCitations,
  extractValues,
  isAbstention,
  normalizeText,
  containsNamedValue,
} from '../values';
import { isIsoDate, loadWorld, pyRepr } from '../world';

const world = loadWorld();

interface Step {
  executed_call: ToolCall | null;
  tool_result: unknown;
}

describe('executeTool parity with Python execute_tool', () => {
  it('reproduces every executed call in replays.json', () => {
    const replays = JSON.parse(
      readFileSync(join(__dirname, '..', '__fixtures__', 'replays.json'), 'utf8'),
    ) as { steps: Step[] }[];
    const executed = replays.flatMap((r) => r.steps).filter((s) => s.executed_call);
    expect(executed.length).toBeGreaterThan(100);
    for (const s of executed)
      expect([s.executed_call, executeTool(world, s.executed_call!)]).toEqual([
        s.executed_call,
        s.tool_result,
      ]);
  });

  it('matches the exported stable_hash vectors', () => {
    for (const v of world.json.exec.hash_vectors)
      expect(stableHash(v.text).toString()).toBe(v.value);
  });

  it('builds the Python sorted(args.items()) key', () => {
    expect(toolKey('t', { station: 'alto_cenizo', group_size: 4 })).toBe(
      "t|[('group_size', 4), ('station', 'alto_cenizo')]",
    );
    expect(pyRepr(["o'x", 'a"b', 'a\'b"c', true, null])).toBe(
      `["o'x", 'a"b', 'a\\'b"c', True, None]`,
    );
  });

  it('returns clones empty and validation errors with jsonschema texts', () => {
    const clone = world.json.tools.find((t) => t.near_duplicate_of)!;
    const args = Object.fromEntries(
      Object.entries(
        clone.parameters.properties as Record<string, { enum?: string[]; type: string }>,
      ).map(([k, v]) => [k, v.enum ? v.enum[0] : v.type === 'integer' ? 3 : '2026-12-03']),
    );
    expect(executeTool(world, { name: clone.name, arguments: args })).toEqual({
      ok: true,
      tool: clone.name,
      passage_ids: [],
      data: {},
    });
    const stations = "['alto_cenizo', 'laguna_espejo', 'valle_bruma', 'refugio_quelital']";
    // Expected texts recorded from Python World.validate_arguments.
    const cases: [string, Record<string, unknown>, string[]][] = [
      ['get_opening_hours', {}, ["'station' is a required property"]],
      ['get_opening_hours', { station: 'x' }, [`'x' is not one of ${stations}`]],
      [
        'get_opening_hours',
        { station: 5 },
        ["5 is not of type 'string'", `5 is not one of ${stations}`],
      ],
      [
        'register_visit',
        {
          station: 'alto_cenizo',
          date: '2026-02-30',
          group_size: '4',
          visitor_type: 'nacional',
          foo: 1,
        },
        [
          "'4' is not of type 'integer'",
          'unexpected argument: foo',
          "'2026-02-30' is not an ISO date (YYYY-MM-DD)",
        ],
      ],
      [
        'register_visit',
        { station: 'alto_cenizo', date: '2026-12-01', group_size: true, visitor_type: 'nacional' },
        ["True is not of type 'integer'"],
      ],
      [
        'register_visit',
        { station: 'alto_cenizo', date: '2026-12-01', group_size: 4.5, visitor_type: 'nacional' },
        ["4.5 is not of type 'integer'"],
      ],
      ['nope', {}, ['unknown tool: nope']],
      [
        'get_acclimatization_advice',
        { target_altitude_m: null },
        ["None is not of type 'integer'"],
      ],
      [
        'report_emergency',
        { station: "o'x", emergency_type: 'incendio', people_count: 2 },
        [`"o'x" is not one of ${stations}`],
      ],
    ];
    for (const [name, a, errors] of cases) {
      expect(world.validateArguments(name, a)).toEqual(errors);
      expect(executeTool(world, { name, arguments: a })).toEqual({
        ok: false,
        tool: name,
        error: errors.join('; '),
      });
    }
    expect(world.validateValue('date', '2026-13-01')).toEqual([
      "'2026-13-01' is not an ISO date (YYYY-MM-DD)",
    ]);
    expect(world.validateValue('people_count', '3')).toEqual(["'3' is not of type 'integer'"]);
    expect(world.validateValue('item', 'x')).toEqual([
      "'x' is not one of ['drones', 'mascotas', 'carpas', 'bebidas_alcoholicas']",
    ]);
    expect(world.missingRequired('register_visit', { station: 'alto_cenizo' })).toEqual([
      'date',
      'group_size',
      'visitor_type',
    ]);
  });

  it('accepts ISO dates like Python date.fromisoformat (len 10)', () => {
    const ok = ['2026-11-26', '2024-02-29', '2026-W48-4', '2026-W53-1'];
    const bad = [
      '2026-02-29',
      '0000-01-01',
      '2026-W01-8',
      '2026-12-1 ',
      '2026/12/01',
      '20261201',
      20261201,
    ];
    expect(ok.map(isIsoDate)).toEqual(ok.map(() => true));
    expect(bad.map(isIsoDate)).toEqual(bad.map(() => false));
  });
});

describe('values parity (expectations recorded from Python)', () => {
  const rows: [string, string, string[], string[], string[], boolean][] = [
    [
      'La Estación Alto Cenizo abre todos los días a las 06:40 y cierra a las 3:50 p. m., incluidos los festivos.',
      'la estacion alto cenizo abre todos los dias a las 06:40 y cierra a las 3:50 p. m., incluidos los festivos.',
      ['06:40', '15:50'],
      ['06:40', '15:50'],
      [],
      false,
    ],
    [
      'Tarifa: $38.500 por persona; altitud 4.137 m [fuente: EST-A-03] y [EST-C-15].',
      'tarifa: $38.500 por persona; altitud 4.137 m [fuente: est-a-03] y [est-c-15].',
      ['38500', '4137'],
      ['38500', '4137'],
      ['EST-A-03', 'EST-C-15'],
      false,
    ],
    [
      'Pasos:\n1. Llame al 123-4567\n2) Espere 12 h 30 en el refugio, 7 personas.',
      'pasos: 1. llame al 123-4567 2) espere 12 h 30 en el refugio, 7 personas.',
      ['1', '123', '12:30', '2', '4567', '7'],
      ['123', '12:30', '4567'],
      [],
      false,
    ],
    ['Ñandú  ÁRBOL’s   niño\tcafé', "nandu arbol's nino cafe", [], [], [], false],
    [
      "I don't have official information about that.",
      "i don't have official information about that.",
      [],
      [],
      [],
      true,
    ],
    [
      '6:15 pm o 12:05 a.m., 25:00, 1,234,567 y 3',
      '6:15 pm o 12:05 a.m., 25:00, 1,234,567 y 3',
      ['00:05', '1234567', '18:15', '3'],
      ['00:05', '1234567', '18:15'],
      [],
      false,
    ],
  ];
  it.each(rows)('%s', (text, normalized, values, evidence, citations, abstain) => {
    expect(normalizeText(text)).toBe(normalized);
    expect([...extractValues(text)].sort()).toEqual(values);
    expect([...evidenceValues(text)].sort()).toEqual(evidence);
    expect(extractCitations(text)).toEqual(citations);
    expect(isAbstention(text)).toBe(abstain);
  });
  it('matches named values on whole phrases', () => {
    expect(containsNamedValue('Se permite el ingreso de niños mayores', 'Niños')).toBe(true);
    expect(containsNamedValue('ninosx', 'ninos')).toBe(false);
  });
});
