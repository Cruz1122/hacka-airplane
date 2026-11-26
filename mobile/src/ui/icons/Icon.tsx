// Interface icons: Lucide glyphs (ISC, see LICENSE-lucide.md), copied as path data so no icon
// package ships with the app. One line family only; add a glyph by pasting its Lucide paths here.
import { memo } from 'react';
import { Platform } from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';

const NATIVE_HIDDEN =
  Platform.OS === 'web'
    ? undefined
    : ({
        accessible: false,
        accessibilityElementsHidden: true,
        importantForAccessibility: 'no-hide-descendants',
      } as const);

interface Glyph {
  paths: readonly string[];
  /** Filled dots (cx, cy, r), drawn in the stroke color. */
  dots?: readonly (readonly [number, number, number])[];
  /** Outlined circles (cx, cy, r). */
  rings?: readonly (readonly [number, number, number])[];
}

const GLYPHS = {
  arrowUp: { paths: ['m5 12l7-7l7 7m-7 7V5'] },
  chevronLeft: { paths: ['m15 18l-6-6l6-6'] },
  chevronRight: { paths: ['m9 18l6-6l-6-6'] },
  textCursorInput: {
    paths: [
      'M12 20h-1a2 2 0 0 1-2-2a2 2 0 0 1-2 2H6m7-12h7a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-7m-8 0H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h1m1-4h1a2 2 0 0 1 2 2a2 2 0 0 1 2-2h1M9 6v12',
    ],
  },
  messagesSquare: {
    paths: [
      'M16 10a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 14.286V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2zm4-1a2 2 0 0 1 2 2v10.286a.71.71 0 0 1-1.212.502l-2.202-2.202A2 2 0 0 0 17.172 19H10a2 2 0 0 1-2-2v-1',
    ],
  },
  squareMousePointer: {
    paths: [
      'M12.034 12.681a.498.498 0 0 1 .647-.647l9 3.5a.5.5 0 0 1-.033.943l-3.444 1.068a1 1 0 0 0-.66.66l-1.067 3.443a.5.5 0 0 1-.943.033z',
      'M21 11V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6',
    ],
  },
  camera: {
    paths: ['M14 4h-4L8 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-4z'],
    rings: [[12, 13, 3]],
  },
  // Lucide `mic` 24×24, verbatim from lucide icons/mic.svg.
  mic: {
    paths: [
      'M12 2a3 3 0 0 1 3 3v7a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z',
      'M19 10v2a7 7 0 0 1-14 0v-2',
      'M12 19v3',
    ],
  },
  circleDot: {
    paths: [],
    rings: [[12, 12, 10]],
    dots: [[12, 12, 1]],
  },
  palette: {
    paths: [
      'M12 22a1 1 0 0 1 0-20a10 9 0 0 1 10 9a5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z',
    ],
    dots: [
      [13.5, 6.5, 0.5],
      [17.5, 10.5, 0.5],
      [6.5, 12.5, 0.5],
      [8.5, 7.5, 0.5],
    ],
  },
  play: {
    paths: ['M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z'],
  },
  // Lucide `volume-2` 24×24, verbatim from lucide icons/volume-2.svg.
  volume2: {
    paths: [
      'M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z',
      'M16 9a5 5 0 0 1 0 6',
      'M19.364 18.364a9 9 0 0 0 0-12.728',
    ],
  },
  rotateCcw: {
    paths: ['M3 12a9 9 0 1 0 9-9a9.75 9.75 0 0 0-6.74 2.74L3 8', 'M3 3v5h5'],
  },
  bookOpen: {
    paths: [
      'M12 7v14',
      'M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4a4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3a3 3 0 0 0-3-3z',
    ],
  },
  externalLink: {
    paths: ['M15 3h6v6', 'M10 14L21 3', 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'],
  },
  x: { paths: ['M18 6L6 18', 'm6 6l12 12'] },
  // Group sync glyphs, verbatim from lucide icons/*.svg (triangle-alert via lucide-static).
  users: {
    paths: [
      'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2',
      'M16 3.128a4 4 0 0 1 0 7.744',
      'M22 21v-2a4 4 0 0 0-3-3.87',
    ],
    rings: [[9, 7, 4]],
  },
  triangleAlert: {
    paths: [
      'm21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3',
      'M12 9v4',
      'M12 17h.01',
    ],
  },
  radio: {
    paths: [
      'M16.247 7.761a6 6 0 0 1 0 8.478',
      'M19.075 4.933a10 10 0 0 1 0 14.134',
      'M4.925 19.067a10 10 0 0 1 0-14.134',
      'M7.753 16.239a6 6 0 0 1 0-8.478',
    ],
    rings: [[12, 12, 2]],
  },
  eyeOff: {
    paths: [
      'M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49',
      'M14.084 14.158a3 3 0 0 1-4.242-4.242',
      'M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143',
      'm2 2 20 20',
    ],
  },
  flag: {
    paths: [
      'M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.528',
    ],
  },
  nfc: {
    paths: [
      'M6 8.32a7.43 7.43 0 0 1 0 7.36',
      'M9.46 6.21a11.76 11.76 0 0 1 0 11.58',
      'M12.91 4.1a15.91 15.91 0 0 1 .01 15.8',
      'M16.37 2a20.16 20.16 0 0 1 0 20',
    ],
  },
  // Navigation and composer glyphs, verbatim from lucide-react 0.577 icons/*.js.
  messageCircle: {
    paths: [
      'M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719',
    ],
  },
  route: {
    paths: ['M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15'],
    rings: [
      [6, 19, 3],
      [18, 5, 3],
    ],
  },
  pencil: {
    paths: [
      'M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z',
      'm15 5 4 4',
    ],
  },
  check: { paths: ['M20 6 9 17l-5-5'] },
  // Verbatim from lucide-static 0.460.0 icons/refresh-cw.svg.
  refreshCw: {
    paths: [
      'M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8',
      'M21 3v5h-5',
      'M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16',
      'M8 16H3v5',
    ],
  },
  squarePen: {
    paths: [
      'M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7',
      'M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z',
    ],
  },
  minus: { paths: ['M5 12h14'] },
  plus: { paths: ['M5 12h14', 'M12 5v14'] },
  chevronsUpDown: { paths: ['m7 15 5 5 5-5', 'm7 9 5-5 5 5'] },
  settings: {
    paths: [
      'M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915',
    ],
    rings: [[12, 12, 3]],
  },
  accessibility: {
    paths: ['m9 20 3-6 3 6', 'm6 8 6 2 6-2', 'M12 10v4'],
    rings: [[12, 5, 1]],
  },
  clock: {
    paths: ['M12 6v6l4 2'],
    rings: [[12, 12, 10]],
  },
  star: {
    paths: [
      'M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z',
    ],
  },
  // Accessibility and settings sheet glyphs, verbatim from Lucide 24x24 icons.
  type: {
    paths: ['M4 7V4h16v3', 'M9 20h6', 'M12 4v16'],
  },
  contrast: {
    paths: ['M12 18a6 6 0 0 0 0-12v12z'],
    rings: [[12, 12, 10]],
  },
  eye: {
    paths: [
      'M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0',
    ],
    rings: [[12, 12, 3]],
  },
  circlePause: {
    paths: ['M10 15V9', 'M14 15V9'],
    rings: [[12, 12, 10]],
  },
  circleCheck: {
    paths: ['m9 12 2 2 4-4'],
    rings: [[12, 12, 10]],
  },
  info: {
    paths: ['M12 16v-4', 'M12 8h.01'],
    rings: [[12, 12, 10]],
  },
  wifiOff: {
    paths: [
      'M12 20h.01',
      'M8.5 16.429a5 5 0 0 1 7 0',
      'M5 12.859a10 10 0 0 1 5.17-2.69',
      'M19 12.859a10 10 0 0 0-2.007-1.523',
      'M2 8.82a15 15 0 0 1 4.177-2.643',
      'M22 8.82a15 15 0 0 0-11.288-3.764',
      'm2 2 20 20',
    ],
  },
} satisfies Record<string, Glyph>;

export type IconName = keyof typeof GLYPHS;

export interface IconProps {
  name: IconName;
  /** Points; Lucide draws on a 24-unit grid. */
  size?: number;
  color: string;
  strokeWidth?: number;
  fill?: string;
}

/** Decorative by default: the control that holds it carries the accessibility label. */
export const Icon = memo(function Icon({
  name,
  size = 20,
  color,
  strokeWidth = 2,
  fill = 'none',
}: IconProps) {
  const g: Glyph = GLYPHS[name];
  return (
    <Svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      pointerEvents="none"
      aria-hidden
      {...NATIVE_HIDDEN}
    >
      {g.paths.map((d) => (
        <Path
          key={d}
          d={d}
          fill={fill}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
      {g.rings?.map(([cx, cy, r]) => (
        <Circle
          key={`r${cx},${cy}`}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
        />
      ))}
      {g.dots?.map(([cx, cy, r]) => (
        <Circle
          key={`d${cx},${cy}`}
          cx={cx}
          cy={cy}
          r={r}
          fill={color}
          stroke={color}
          strokeWidth={strokeWidth}
        />
      ))}
    </Svg>
  );
});
