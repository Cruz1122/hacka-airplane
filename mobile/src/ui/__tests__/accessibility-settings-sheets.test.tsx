// Interactive tests for AccessibilitySheet and SettingsSheet bottom-sheet overlays.
import { act } from 'react';
import { AccessibilityInfo, Linking } from 'react-native';
import Storage from 'expo-sqlite/kv-store';
import { createRoot, type Root, type TestInstance } from 'test-renderer';

import { fill, t } from '@/i18n';
import {
  resetAccessibilityForTest,
  useAccessibility,
  type AccessibilityPrefs,
} from '@/state/accessibility';
import {
  resetFavoriteSourcesForTest,
  toggleFavoriteSource,
  useFavoriteSources,
} from '@/state/favoriteSources';
import { setVerifiedOnly, useVerifiedOnly } from '@/state/verifiedOnly';

import { AccessibilitySheet } from '../AccessibilitySheet';
import { SettingsSheet } from '../SettingsSheet';
import { useReducedMotion } from '../useReducedMotion';

jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: {
    getItemAsync: jest.fn(async () => null),
    setItemAsync: jest.fn(async () => {}),
  },
}));

jest.mock('react-native-reanimated', () => {
  const { View } = jest.requireActual('react-native');
  return {
    __esModule: true,
    default: { View },
    useSharedValue: (value: number) => ({
      value,
      set(v: number) {
        this.value = v;
      },
    }),
    useAnimatedStyle: (style: () => object) => style(),
    withTiming: (value: number) => value,
  };
});

jest.mock('react-native-gesture-handler', () => {
  const { View } = jest.requireActual('react-native');
  return {
    GestureHandlerRootView: View,
    GestureDetector: ({ children }: { children: unknown }) => children,
    usePanGesture: () => ({}),
  };
});

const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

const mounted: Root[] = [];

function createHarness(root: Root) {
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const texts = () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join(''));
  const press = async (node: TestInstance) => act(async () => node.props.onClick(PRESS));
  const byRoleAndLabel = (role: string, label: string) => {
    const found = all(
      (n) =>
        n.props.accessibilityRole === role &&
        n.props.accessibilityLabel === label &&
        typeof n.props.onClick === 'function',
    );
    expect(found.length).toBeGreaterThan(0);
    return found[0];
  };
  const byTextPressable = (text: string) => {
    const found = all((n) => n.type === 'Text' && [n.props.children].flat().join('') === text);
    expect(found.length).toBeGreaterThan(0);
    let node: TestInstance | null = found[0];
    while (node && typeof node.props.onClick !== 'function') node = node.parent;
    expect(node).not.toBeNull();
    return node!;
  };
  return {
    all,
    texts,
    hasText: (text: string) => texts().includes(text),
    pressButton: (label: string) => press(byRoleAndLabel('button', label)),
    pressLink: (label: string) => press(byRoleAndLabel('link', label)),
    pressSwitch: (label: string) => press(byRoleAndLabel('switch', label)),
    pressRadio: (label: string) => press(byRoleAndLabel('radio', label)),
    pressText: (text: string) => press(byTextPressable(text)),
  };
}

beforeEach(() => {
  resetAccessibilityForTest();
  resetFavoriteSourcesForTest();
  jest.spyOn(AccessibilityInfo, 'isReduceMotionEnabled').mockResolvedValue(false);
});

afterEach(() => {
  for (const root of mounted.splice(0)) act(() => root.unmount());
  jest.restoreAllMocks();
});

describe('AccessibilitySheet', () => {
  it('controls text size, high contrast, reduce motion, color vision, and reset live', async () => {
    let latestPrefs: AccessibilityPrefs | null = null;
    let latestReduced = false;

    function Probe() {
      latestPrefs = useAccessibility();
      latestReduced = useReducedMotion();
      return null;
    }

    const onClose = jest.fn();
    const root = createRoot();
    mounted.push(root);
    await act(async () => {
      root.render(
        <>
          <Probe />
          <AccessibilitySheet open onClose={onClose} reducedMotion />
        </>,
      );
    });

    const ui = createHarness(root);
    const copy = t.accessibilityPanel;

    expect(ui.hasText(copy.title)).toBe(true);
    expect(ui.hasText(copy.textSize.previewTitle)).toBe(true);
    expect(ui.hasText(copy.textSize.previewBody)).toBe(true);
    expect(ui.hasText(copy.reset)).toBe(false);

    // Increase text size via + button, then select Extra pill directly.
    await ui.pressButton(copy.textSize.increase);
    expect(latestPrefs!.textScale).toBe(1.15);
    await ui.pressRadio(copy.textSize.levels.extra);
    expect(latestPrefs!.textScale).toBe(1.45);
    await ui.pressButton(copy.textSize.decrease);
    expect(latestPrefs!.textScale).toBe(1.3);

    // High contrast switch.
    await ui.pressSwitch(copy.highContrast.title);
    expect(latestPrefs!.highContrast).toBe(true);

    // Reduce motion switch propagates immediately to useReducedMotion().
    expect(latestReduced).toBe(false);
    await ui.pressSwitch(copy.reduceMotion.title);
    expect(latestPrefs!.reduceMotion).toBe(true);
    expect(latestReduced).toBe(true);

    await ui.pressSwitch(copy.autoSpeakReplies.title);
    expect(latestPrefs!.autoSpeakReplies).toBe(true);

    // Color vision radio selection.
    await ui.pressRadio(copy.colorVision.modes.tritanopia.label);
    expect(latestPrefs!.colorVision).toBe('tritanopia');

    // Reset button is now visible and restores defaults.
    expect(ui.hasText(copy.reset)).toBe(true);
    await ui.pressButton(copy.reset);
    expect(latestPrefs).toEqual({
      textScale: 1,
      highContrast: false,
      reduceMotion: false,
      autoSpeakReplies: false,
      colorVision: 'none',
    });
    expect(latestReduced).toBe(false);
    expect(ui.hasText(copy.reset)).toBe(false);

    // Close button calls onClose immediately under reducedMotion.
    await ui.pressButton(copy.close);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('shows the device reduce-motion notice when the system setting is active', async () => {
    jest.spyOn(AccessibilityInfo, 'isReduceMotionEnabled').mockResolvedValue(true);
    const root = createRoot();
    mounted.push(root);
    await act(async () => {
      root.render(<AccessibilitySheet open onClose={jest.fn()} reducedMotion />);
    });
    const ui = createHarness(root);
    expect(ui.hasText(t.accessibilityPanel.reduceMotion.systemActive)).toBe(true);
  });
});

describe('SettingsSheet', () => {
  it('toggles the verified-only switch and saves it', async () => {
    let on: boolean | undefined;
    function Probe() {
      on = useVerifiedOnly();
      return null;
    }
    const root = createRoot();
    mounted.push(root);
    await act(async () => {
      root.render(
        <>
          <Probe />
          <SettingsSheet open onClose={jest.fn()} reducedMotion />
        </>,
      );
    });
    const ui = createHarness(root);
    const copy = t.settingsPanel.verifiedOnly;
    const row = () =>
      ui.all(
        (n) => n.props.accessibilityRole === 'switch' && n.props.accessibilityLabel === copy.title,
      )[0];
    expect(on).toBe(false);
    expect(ui.hasText(copy.title)).toBe(true);
    expect(row().props.accessibilityState).toEqual({ checked: false });

    await ui.pressSwitch(copy.title);
    expect(on).toBe(true);
    expect(row().props.accessibilityState).toEqual({ checked: true });
    expect(Storage.setItemAsync).toHaveBeenCalledWith('knowledge.verifiedOnly.v1', 'true');

    await ui.pressSwitch(copy.title);
    expect(on).toBe(false);
    act(() => setVerifiedOnly(false));
  });

  it('shows Saved Sources and About in the root menu and handles empty Saved Sources', async () => {
    const root = createRoot();
    mounted.push(root);
    await act(async () => {
      root.render(<SettingsSheet open onClose={jest.fn()} reducedMotion />);
    });

    const ui = createHarness(root);
    const copy = t.settingsPanel;
    expect(ui.hasText(copy.title)).toBe(true);
    expect(ui.hasText(copy.savedSources.title)).toBe(true);
    expect(ui.hasText(copy.about.title)).toBe(true);

    // Drill into Saved sources -> empty state.
    await ui.pressText(copy.savedSources.title);
    expect(ui.hasText(copy.savedSources.emptyTitle)).toBe(true);
    expect(ui.hasText(copy.savedSources.emptyBody)).toBe(true);

    // Back returns to root menu, then drill into About.
    await ui.pressButton(copy.back);
    expect(ui.hasText(copy.about.title)).toBe(true);
    await ui.pressText(copy.about.title);
    expect(ui.hasText(t.appTitle)).toBe(true);
    expect(ui.hasText(t.parkName)).toBe(true);
    expect(ui.hasText(copy.about.offlineTitle)).toBe(true);
    expect(ui.hasText(copy.about.sourcesTitle)).toBe(true);
    expect(ui.hasText(copy.about.creditsTitle)).toBe(true);
  });

  it('lists saved sources, opens web links, removes with inline Undo, and restores on Undo', async () => {
    const openUrlSpy = jest.spyOn(Linking, 'openURL').mockResolvedValue(undefined);
    const sample = {
      id: 'pnn-nevados',
      title: 'Parque Nacional Natural Los Nevados',
      url: 'https://www.parquesnacionales.gov.co/los-nevados',
      excerpt: 'Guía oficial de senderos, altitud y recomendaciones del parque.',
      retrievedAt: '2026-04-12',
    };
    toggleFavoriteSource(sample);

    let savedCount = 0;
    function Probe() {
      savedCount = useFavoriteSources().length;
      return null;
    }

    const root = createRoot();
    mounted.push(root);
    await act(async () => {
      root.render(
        <>
          <Probe />
          <SettingsSheet open onClose={jest.fn()} reducedMotion initialView="savedSources" />
        </>,
      );
    });

    const ui = createHarness(root);
    const copy = t.settingsPanel;

    expect(savedCount).toBe(1);
    expect(ui.hasText(sample.title)).toBe(true);

    // Open external link.
    await ui.pressLink(fill(t.chatScreen.sources.openLabel, { title: sample.title }));
    expect(openUrlSpy).toHaveBeenCalledWith(sample.url);

    // Remove saved source -> empty state + inline Undo banner.
    await ui.pressButton(fill(t.chatScreen.sources.unfavoriteLabel, { title: sample.title }));
    expect(savedCount).toBe(0);
    expect(ui.hasText(copy.savedSources.emptyTitle)).toBe(true);
    expect(ui.hasText(copy.savedSources.removedNotice)).toBe(true);
    expect(ui.hasText(copy.savedSources.undo)).toBe(true);

    // Press Undo -> restores the saved source immediately.
    await ui.pressButton(copy.savedSources.undo);
    expect(savedCount).toBe(1);
    expect(ui.hasText(sample.title)).toBe(true);
    expect(ui.hasText(copy.savedSources.removedNotice)).toBe(false);
  });
});
