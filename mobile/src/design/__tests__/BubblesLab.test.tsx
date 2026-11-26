import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import catalog from '@/../assets/data/knowledge/catalog.json';
import { fill, t } from '@/i18n';

import { fonts } from '@/ui/theme/tokens';

import { BubblesLab } from '../BubblesLab';
import { CATALOG_ANSWER } from '../fixtures';

jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => true }));
// The bubbles view never draws the chat screen, and jest cannot load FlashList's ESM build.
jest.mock('@/chat/ChatView', () => ({ ChatView: () => null }));

const w = t.dev.workshop;
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

const flat = (n: TestInstance | string): string =>
  typeof n === 'string' ? n : n.children.map(flat).join('');

function mount() {
  const root = createRoot();
  act(() => root.render(<BubblesLab wide={false} reducedMotion />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const byLabel = (label: string) =>
    all((n) => n.type === 'View' && n.props.accessibilityLabel === label);
  return {
    byLabel,
    texts: () => all((n) => n.type === 'Text' && n.parent?.type !== 'Text').map(flat),
    bold: () => all((n) => n.type === 'Text' && n.props.style?.fontFamily === fonts.bold).map(flat),
    press: (node: TestInstance) => act(() => node.props.onClick(PRESS)),
  };
}

describe('BubblesLab sources', () => {
  it('shows a cited world answer without its markers and opens its passages', () => {
    const lab = mount();
    expect(lab.texts().join('\n')).not.toContain('[fuente:');
    lab.press(lab.byLabel(fill(t.chatScreen.sources.showMany, { n: 2 }))[0]);
    expect(lab.texts()).toEqual(expect.arrayContaining(['Estación Refugio Quelital']));
  });

  it('opens the catalog answer with its real links, and keeps an unretrieved citation buttonless', () => {
    const lab = mount();
    lab.press(lab.byLabel(w.threadSources)[0]);
    expect(lab.texts()).toEqual(
      expect.arrayContaining(['¿Para qué fecha? [trámite: admite datos parciales]']),
    );
    const buttons = lab.byLabel(fill(t.chatScreen.sources.showMany, { n: 3 }));
    expect(buttons).toHaveLength(1);
    lab.press(buttons[0]);
    for (const s of CATALOG_ANSWER.sources) {
      expect(lab.byLabel(fill(t.chatScreen.sources.openLabel, { title: s.label }))).toHaveLength(1);
    }
  });

  it('copies its catalog answer verbatim from the catalog', () => {
    const entry = catalog.find((e) => e.id === CATALOG_ANSWER.id)!;
    expect({ id: entry.id, short: entry.short, sources: entry.sources }).toEqual(CATALOG_ANSWER);
  });
});

describe('BubblesLab urgent thread', () => {
  it('shows the 123 banner and the catalog answer with keywords in bold and a list', () => {
    const lab = mount();
    lab.press(lab.byLabel(w.threadUrgent)[0]);
    expect(lab.bold()).toEqual(
      expect.arrayContaining([
        'Marca el 123',
        'Esta app no avisa a rescate',
        'avísale de inmediato',
      ]),
    );
    expect(lab.texts()).toEqual(
      expect.arrayContaining(['•', 'Si tienes guía registrado, avísale de inmediato.']),
    );
  });

  it('replays the turn whole under reduced motion', () => {
    // The reveal loop's frames never run here: no timer keeps spinning after the test.
    const raf = jest.spyOn(global, 'requestAnimationFrame').mockImplementation(() => 0);
    const lab = mount();
    lab.press(lab.byLabel(w.threadUrgent)[0]);
    const before = lab.texts();
    lab.press(lab.byLabel(w.replayReply)[0]);
    expect(lab.texts()).toEqual(before);
    raf.mockRestore();
  });
});
