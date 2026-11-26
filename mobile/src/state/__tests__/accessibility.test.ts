// Persisted accessibility store and color-vision / high-contrast palette resolution tests.
import Storage from 'expo-sqlite/kv-store';

import {
  COLOR_VISION_MODES,
  DEFAULT_ACCESSIBILITY,
  isDefaultAccessibility,
  parseAccessibility,
  resetAccessibility,
  resetAccessibilityForTest,
  setAccessibility,
  snapTextScale,
  TEXT_SCALE_STEPS,
  textScaleFromIndex,
  textScaleIndex,
} from '../accessibility';
import { brand, resolveBrand, type } from '@/ui/theme/tokens';
import { buildScaledType, scaleSize } from '@/ui/useAccessibilityTheme';

jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: {
    getItemAsync: jest.fn(async () => null),
    setItemAsync: jest.fn(async () => {}),
  },
}));

const mockSetItem = Storage.setItemAsync as jest.Mock;

beforeEach(() => {
  mockSetItem.mockClear();
  resetAccessibilityForTest();
});

describe('snapTextScale & step indexing', () => {
  it('snaps arbitrary values to the closest supported text scale step', () => {
    expect(snapTextScale(1)).toBe(1);
    expect(snapTextScale(0.5)).toBe(1);
    expect(snapTextScale(1.12)).toBe(1.15);
    expect(snapTextScale(1.31)).toBe(1.3);
    expect(snapTextScale(2.5)).toBe(1.45);
    expect(snapTextScale(Number.NaN)).toBe(1);
  });

  it('round-trips every scale step through index helpers and clamps out-of-range indices', () => {
    TEXT_SCALE_STEPS.forEach((step, idx) => {
      expect(textScaleIndex(step)).toBe(idx);
      expect(textScaleFromIndex(idx)).toBe(step);
    });
    expect(textScaleFromIndex(-3)).toBe(TEXT_SCALE_STEPS[0]);
    expect(textScaleFromIndex(99)).toBe(TEXT_SCALE_STEPS[TEXT_SCALE_STEPS.length - 1]);
  });
});

describe('parseAccessibility', () => {
  it('parses valid saved JSON', () => {
    expect(
      parseAccessibility(
        '{"textScale":1.3,"highContrast":true,"reduceMotion":true,"autoSpeakReplies":true,"colorVision":"deuteranopia"}',
      ),
    ).toEqual({
      textScale: 1.3,
      highContrast: true,
      reduceMotion: true,
      autoSpeakReplies: true,
      colorVision: 'deuteranopia',
    });
  });

  it('falls back safely on null, malformed JSON, or invalid field values', () => {
    expect(parseAccessibility(null)).toEqual(DEFAULT_ACCESSIBILITY);
    expect(parseAccessibility('not json')).toEqual(DEFAULT_ACCESSIBILITY);
    expect(parseAccessibility('42')).toEqual(DEFAULT_ACCESSIBILITY);
    expect(
      parseAccessibility(
        '{"textScale":1.18,"highContrast":"yes","reduceMotion":1,"colorVision":"monochromacy"}',
      ),
    ).toEqual({
      textScale: 1.15,
      highContrast: false,
      reduceMotion: false,
      autoSpeakReplies: false,
      colorVision: 'none',
    });
  });
});

describe('setAccessibility & resetAccessibility', () => {
  it('persists updates and avoids redundant writes when values do not change', () => {
    setAccessibility({ textScale: 1.3, highContrast: true });
    expect(mockSetItem).toHaveBeenCalledTimes(1);
    expect(JSON.parse(mockSetItem.mock.calls[0][1])).toEqual({
      textScale: 1.3,
      highContrast: true,
      reduceMotion: false,
      autoSpeakReplies: false,
      colorVision: 'none',
    });

    // No-op patch does not re-persist.
    setAccessibility({ textScale: 1.3, highContrast: true });
    expect(mockSetItem).toHaveBeenCalledTimes(1);

    resetAccessibility();
    expect(mockSetItem).toHaveBeenCalledTimes(2);
    expect(JSON.parse(mockSetItem.mock.calls[1][1])).toEqual(DEFAULT_ACCESSIBILITY);

    // Already default: reset is a no-op.
    resetAccessibility();
    expect(mockSetItem).toHaveBeenCalledTimes(2);
  });

  it('identifies default vs customized preferences', () => {
    expect(isDefaultAccessibility(DEFAULT_ACCESSIBILITY)).toBe(true);
    expect(isDefaultAccessibility({ ...DEFAULT_ACCESSIBILITY, reduceMotion: true })).toBe(false);
    expect(isDefaultAccessibility({ ...DEFAULT_ACCESSIBILITY, autoSpeakReplies: true })).toBe(
      false,
    );
    expect(isDefaultAccessibility({ ...DEFAULT_ACCESSIBILITY, colorVision: 'tritanopia' })).toBe(
      false,
    );
  });
});

describe('resolveBrand & typography scaling', () => {
  it('returns the exact default brand palette for standard vision without high contrast', () => {
    expect(resolveBrand('none', false)).toBe(brand);
  });

  it('produces distinct accessible palettes for every color-vision mode and high contrast', () => {
    const standard = resolveBrand('none', false);
    const highContrast = resolveBrand('none', true);
    expect(highContrast.ink).not.toBe(standard.ink);
    expect(highContrast.inkMuted).not.toBe(standard.inkMuted);

    for (const mode of COLOR_VISION_MODES) {
      const normal = resolveBrand(mode, false);
      const hc = resolveBrand(mode, true);
      expect(normal.primary).toBeTruthy();
      expect(normal.alert).toBeTruthy();
      expect(normal.online).toBeTruthy();
      expect(hc.ink).not.toBe(normal.ink);
      expect(hc.inkMuted).not.toBe(normal.inkMuted);
      if (mode !== 'none') {
        expect(normal.primary !== standard.primary || normal.alert !== standard.alert).toBe(true);
      }
    }
  });

  it('scales font sizes and line heights proportionally', () => {
    expect(scaleSize(16, 1.3)).toBe(21);
    const scaled = buildScaledType(1.45);
    expect(scaled.body.fontSize).toBe(Math.round(type.body.fontSize * 1.45));
    expect(scaled.body.lineHeight).toBe(Math.round(type.body.lineHeight * 1.45));
    expect(scaled.title.fontSize).toBe(Math.round(type.title.fontSize * 1.45));
  });
});
