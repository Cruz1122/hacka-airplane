// Design tokens: the only place UI colors, fonts and sizes are defined. The app-design skill
// (.claude/skills/app-design) documents how to use them; a jest guard rejects raw hex colors and
// font names in UI files.

/**
 * Brand palette: the teal of the park emblem's ring (#5E9999, the user's pick) and shades of the
 * same hue. Contrast on `card`: ink 9.3:1, inkMuted 5.2:1. White on `primary` is 3.2:1 (3.1:1
 * mid-gradient): below WCAG AA for the 16 px button label (4.5:1), accepted for the exact color.
 */
export const brand = {
  /** Buttons, active indicators. */
  primary: '#5E9999',
  /** Top of the primary button gradient. */
  primaryLight: '#68A3A3',
  /** Idle indicators and decorative tints; never text. */
  primarySoft: '#C2DADA',
  onPrimary: '#FFFFFF',
  /** Black at 55 %: the credit pill over a chat photo, under `onPrimary` text. Photos only. */
  photoScrim: '#0000008C',
  /** Titles on light surfaces. */
  ink: '#234B4B',
  /** Body text on light surfaces. */
  inkMuted: '#557070',
  /** Cloud card surface. */
  card: '#F9FCFC',
  /** Cloud card shading and puffs. */
  cardShade: '#DCEBEB',
  /** Teal vapor glow around chat bubbles, the composer and the Pet's circle (primary at 22%). */
  glow: '#5E999938',
  /** "Ready" dot on the Pet's circle in the chat. */
  online: '#3FB36A',
  /** Alert states of the group module: a visitor far or lost, the other guide lost. Contrast on
   *  `card` about 4.7:1; white text (`onPrimary`) on it about 4.8:1. */
  alert: '#DC2626',
  /** Vinotinto title of the visitor's error states ("drifting", "no signal"). Contrast on
   *  `wineSoft` 9.0:1 (AAA); on `card` 10.8:1. */
  wine: '#6E1E2E',
  /** Full-screen background of the visitor's error states. `ink` on it is 7.8:1; `inkMuted`
   *  only 4.3:1, so body text there is `ink`. */
  wineSoft: '#F5E3E6',
  /** Pet accessory tints only (the frailejón's yellow and the páramo lupine's purple); never
   *  text or UI surfaces. */
  sun: '#E9B949',
  lupine: '#7E62B8',
  /** Screen background while the illustration loads. */
  sky: '#8FA6F2',
} as const;

export type BrandPalette = { readonly [K in keyof typeof brand]: string };
export type PaletteColorVision = 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia';

/** Color-vision-adapted brand tokens (Okabe-Ito / Tol inspired, preserving high contrast). */
const COLOR_VISION_PALETTES: Record<PaletteColorVision, BrandPalette> = {
  none: brand,
  // Red-green (L-cone): shift primary/status onto a clear blue vs ochre-gold axis.
  protanopia: {
    ...brand,
    primary: '#2B6CB0',
    primaryLight: '#3B82C4',
    primarySoft: '#BDD6EE',
    ink: '#163659',
    inkMuted: '#426282',
    card: '#F8FBFE',
    cardShade: '#DCE9F5',
    glow: '#2B6CB038',
    online: '#0284C7',
    alert: '#A16207',
    wine: '#5C3806',
    wineSoft: '#FAF0DB',
  },
  // Red-green (M-cone): clear cobalt-blue vs warm burnt-amber axis.
  deuteranopia: {
    ...brand,
    primary: '#2563A6',
    primaryLight: '#3578BF',
    primarySoft: '#BFD5EE',
    ink: '#173454',
    inkMuted: '#44607E',
    card: '#F8FBFE',
    cardShade: '#DDE8F4',
    glow: '#2563A638',
    online: '#0385B8',
    alert: '#B45309',
    wine: '#5E2B04',
    wineSoft: '#FBECE0',
  },
  // Blue-yellow (S-cone): keep clear cyan-teal vs crimson-rose axis.
  tritanopia: {
    ...brand,
    primary: '#0E7C86',
    primaryLight: '#1A919C',
    primarySoft: '#B6E0E3',
    ink: '#0E3C40',
    inkMuted: '#3B6569',
    card: '#F7FCFC',
    cardShade: '#D6ECEE',
    glow: '#0E7C8638',
    online: '#0D8A72',
    alert: '#C81E4B',
    wine: '#6B102E',
    wineSoft: '#FCE7EE',
  },
};

/** High-contrast outdoor overrides (WCAG AAA text & strong borders) for each vision mode. */
const HIGH_CONTRAST_OVERRIDES: Record<PaletteColorVision, Partial<BrandPalette>> = {
  none: {
    primary: '#1B5C5C',
    primaryLight: '#247070',
    primarySoft: '#7CA8A8',
    ink: '#091B1B',
    inkMuted: '#1F3D3D',
    card: '#FFFFFF',
    cardShade: '#C4DEDE',
    glow: '#091B1B2E',
    online: '#166534',
    alert: '#A41212',
    wine: '#4F0E1B',
    wineSoft: '#F8DADF',
  },
  protanopia: {
    primary: '#144682',
    primaryLight: '#1D5AA3',
    primarySoft: '#7EA4CC',
    ink: '#0A1A2E',
    inkMuted: '#1D3550',
    card: '#FFFFFF',
    cardShade: '#BDD3EA',
    glow: '#0A1A2E2E',
    online: '#0369A1',
    alert: '#7C3A03',
    wine: '#452403',
    wineSoft: '#F7E4C0',
  },
  deuteranopia: {
    primary: '#14427A',
    primaryLight: '#1E5496',
    primarySoft: '#7EA2CC',
    ink: '#0A192B',
    inkMuted: '#1E344D',
    card: '#FFFFFF',
    cardShade: '#BED2E9',
    glow: '#0A192B2E',
    online: '#0369A1',
    alert: '#853804',
    wine: '#471E02',
    wineSoft: '#F9DFC8',
  },
  tritanopia: {
    primary: '#0A5B63',
    primaryLight: '#11707A',
    primarySoft: '#6EAAB0',
    ink: '#081C1E',
    inkMuted: '#193D41',
    card: '#FFFFFF',
    cardShade: '#B6DCDF',
    glow: '#081C1E2E',
    online: '#0B6353',
    alert: '#9B1237',
    wine: '#4F0920',
    wineSoft: '#FAD4E0',
  },
};

export function resolveBrand(
  colorVision: PaletteColorVision = 'none',
  highContrast = false,
): BrandPalette {
  const base = COLOR_VISION_PALETTES[colorVision];
  if (!highContrast) return base;
  return { ...base, ...HIGH_CONTRAST_OVERRIDES[colorVision] };
}

/** Manrope and Bricolage Grotesque, bundled in assets/fonts (static weights, Latin subset, OFL). One family per weight:
 * Android ignores fontWeight on custom fonts, so pick the weight by family, never by fontWeight. */
export const fonts = {
  regular: 'Manrope-Regular',
  medium: 'Manrope-Medium',
  semibold: 'Manrope-SemiBold',
  bold: 'Manrope-Bold',
  display: 'BricolageGrotesque-Bold',
  heading: 'BricolageGrotesque-SemiBold',
} as const;

/** Text styles. Spread into a StyleSheet and set only `color` on top. */
export const type = {
  display: { fontFamily: fonts.display, fontSize: 26, lineHeight: 32, letterSpacing: -0.4 },
  title: { fontFamily: fonts.heading, fontSize: 21, lineHeight: 27, letterSpacing: -0.3 },
  body: { fontFamily: fonts.regular, fontSize: 15, lineHeight: 22 },
  label: { fontFamily: fonts.semibold, fontSize: 16, lineHeight: 20 },
  caption: { fontFamily: fonts.medium, fontSize: 13, lineHeight: 18 },
} as const;

export const colors = {
  light: {
    background: '#ffffff',
    surface: '#f2f2f4',
    text: '#111111',
    textMuted: '#60646c',
    primary: '#2563eb',
    onPrimary: '#ffffff',
    border: '#d9dbe0',
    danger: '#dc2626',
  },
  dark: {
    background: '#000000',
    surface: '#1c1c1f',
    text: '#f5f5f5',
    textMuted: '#a0a4ab',
    primary: '#60a5fa',
    onPrimary: '#000000',
    border: '#2e3135',
    danger: '#f87171',
  },
} as const;

export const spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24 } as const;
export const radius = { sm: 6, md: 12, lg: 20, pill: 999 } as const;
export const fontSize = { sm: 13, md: 16, lg: 20, xl: 28 } as const;
