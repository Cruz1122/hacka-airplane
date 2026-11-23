import { loadWorld } from '@/core/world';

import { messageSources } from '../messageSources';

const world = loadWorld();

describe('messageSources', () => {
  it('lists the cited passages the turn retrieved, titled by station or park, once each', () => {
    const text =
      'Abre a las 06:10 [fuente: EST-D-01] y exige protector [fuente: PAR-07, EST-D-01].';
    expect(messageSources(text, world, ['EST-D-01', 'PAR-07', 'EST-D-04'])).toEqual([
      {
        id: 'EST-D-01',
        title: 'Estación Refugio Quelital',
        excerpt: world.getPassage('EST-D-01').text,
      },
      { id: 'PAR-07', title: world.json.meta.park_name, excerpt: world.getPassage('PAR-07').text },
    ]);
  });

  it('drops ids no tool returned this turn, unknown ids and injection passages', () => {
    const injection = world.json.passages.find((p) => p.field === world.json.meta.injection_field)!;
    const text = `Dato [fuente: EST-D-01] [fuente: EST-Z-99] [fuente: ${injection.id}]`;
    expect(messageSources(text, world, ['EST-Z-99', injection.id])).toEqual([]);
  });
});
