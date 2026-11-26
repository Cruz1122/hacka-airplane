import { fixture } from '../__fixtures__/load';
import { detectSafety, foldText } from '../safety';

// safety_probes.json: the 45 audit probes of results/p3-final/review/policy.md §3 (copied, since
// results/ is git-ignored). They were written against the old rules, so they are a regression set,
// not an unbiased estimate; the blind estimate is safety_blind.test.ts.
type Probe = [string, string];
const probes = fixture<{
  emergency: Probe[];
  informative: Probe[];
  static_status: Probe[];
}>('safety_probes.json');

// Extra variants written with the rules (dialect, typos, tense). Also not an estimate.
const MORE_URGENT = [
  'nos perdimos bajando del nevado y ya no hay luz',
  'estoy perdida, no se donde estoy',
  'se nos perdio el nino en el sendero',
  'mi hija no aparece, estaba aqui hace un rato',
  'perdimos a mi papa en la niebla',
  'no encontramos el camino de regreso',
  'parce se privo mi llave',
  'mi mama se desmallo',
  'esta inconciente y no reacciona',
  'NO RESPIRA!!! ayudenme',
  'qué hago si mi amigo no respira',
  'que hago si mi novia esta inconsciente',
  'se esta ahogando con comida',
  'tengo los labios morados y no paro de temblar',
  'no siento los pies, estamos a 4000 metros',
  'creo que me dio soroche, estoy vomitando',
  'le cuesta respirar y tose con sangre',
  'esta muy desorientado y se tambalea',
  'esta cayendo ceniza sobre el carro',
  'nos arden los ojos, huele a azufre',
  'viene una avalancha de lodo por la quebrada',
  'el volcan esta haciendo erupcion',
  'me fracture el brazo',
  'se le salio el hueso',
  'mi hermano se cayo por un barranco',
  'se golpeo duro la cabeza contra una roca',
  'me torci la rodilla y no me puedo mover',
  'esta sangrando muchisimo',
  'se esta desangrando',
  'no para de sangrar la cortada',
  'se prendio el pasto cerca de la carpa',
  'me queme con agua hirviendo',
  'le cayo un rayo a mi amigo',
  'estamos en plena tormenta electrica sin refugio',
  'tuvimos un accidente en la via a brisas',
  'nos volcamos en la carretera',
  'necesito una ambulancia',
  'socorrooo',
  'auxilio',
  'llamen a los bomberos',
  'me duele mucho el pecho',
  'le dio una convulsion',
];
const MORE_CALM = [
  '¿qué hago si me pierdo?',
  '¿cómo se previene el soroche?',
  '¿qué síntomas tiene la hipotermia?',
  '¿qué síntomas tiene el mal de altura?',
  '¿qué pasa si hay tormenta eléctrica?',
  '¿hay riesgo de incendio en el páramo?',
  '¿cuál es el número de emergencias?',
  'ayúdame a planear mi visita',
  'necesito ayuda con la reserva',
  '¿se me perdió la reserva, cómo la recupero?',
  'me perdí la reserva del sábado',
  '¿la vía a brisas es peligrosa?',
  '¿qué es el nivel de alerta amarilla?',
  'mi papá no puede caminar mucho, ¿qué sendero recomiendan?',
  '¿cuánto cuesta la entrada?',
  '¿se puede hacer fogata?',
  '¿qué llevar para el frío?',
  '¿cómo reporto una emergencia en la app?',
  'hola',
];
const MORE_LIVE = [
  '¿está abierto el nevado del ruiz?',
  '¿ya abrieron la vía?',
  '¿cómo está la vía a brisas?',
  '¿en qué alerta está el volcán?',
  '¿está lloviendo en el páramo?',
  '¿hay cierre hoy en la carretera?',
  '¿sigue cerrado el sendero al cráter?',
  '¿se puede subir hoy al nevado?',
  'la via sta havilitada?',
];
const MORE_STATIC = [
  '¿el parque abre los domingos?',
  '¿qué horario tiene el centro de visitantes?',
  '¿está abierto en diciembre?',
  '¿la laguna del otún está abierta para acampar?',
  '¿qué es el nivel de alerta naranja?',
  '¿cuánto cuesta la entrada?',
];

describe('foldText', () => {
  it('folds accents, case, punctuation and repeated letters without normalize()', () => {
    expect(foldText('¡AUXILIOOO! Él NO respíra… ¿Qué hágo?')).toBe(
      'auxilio el no respira que hago',
    );
    expect(foldText('Niño, cigüeña, socorrrro')).toBe('nino ciguena socorro');
    expect(foldText('e\u0301l')).toBe('el');
  });
});

describe('detectSafety: audit probe regression', () => {
  it.each(probes.emergency)('urgent: [%s] %s', (_tag, q) => {
    expect(detectSafety(q).urgent).toBe(true);
  });
  it.each(probes.informative)('not urgent: [%s] %s', (_tag, q) => {
    expect(detectSafety(q).urgent).toBe(false);
  });
  it.each(probes.static_status.filter(([t]) => !t.startsWith('live')))(
    'static, no live status: [%s] %s',
    (_t, q) => {
      expect(detectSafety(q).liveStatus).toBe(false);
    },
  );
  it.each(probes.static_status.filter(([t]) => t.startsWith('live')))(
    'live status: [%s] %s',
    (_t, q) => {
      expect(detectSafety(q).liveStatus).toBe(true);
    },
  );
});

describe('detectSafety: extra variants', () => {
  it.each(MORE_URGENT)('urgent: %s', (q) => expect(detectSafety(q).urgent).toBe(true));
  it.each(MORE_CALM)('not urgent: %s', (q) => expect(detectSafety(q).urgent).toBe(false));
  it.each(MORE_LIVE)('live status: %s', (q) => expect(detectSafety(q).liveStatus).toBe(true));
  it.each(MORE_STATIC)('no live status: %s', (q) => expect(detectSafety(q).liveStatus).toBe(false));

  it('never fires on bare "urgente" or "emergencia"', () => {
    for (const q of [
      'urgente',
      'emergencia',
      'es urgente',
      'en caso de emergencia',
      'número de emergencia',
    ]) {
      expect(detectSafety(q).urgent).toBe(false);
    }
  });

  it('reports which rules fired', () => {
    const r = detectSafety('hoy me perdí y está cayendo ceniza, ¿está abierta la vía?');
    expect(r.urgent).toBe(true);
    expect(r.liveStatus).toBe(true);
    expect(r.matched).toEqual(
      expect.arrayContaining(['emergency:lost', 'emergency:volcano', 'live:anchor']),
    );
  });

  it('handles empty input', () => {
    expect(detectSafety('  ¿?  ')).toEqual({
      urgent: false,
      liveStatus: false,
      matched: [],
    });
  });
});
