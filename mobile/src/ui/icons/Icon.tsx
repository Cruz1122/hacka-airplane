// Interface icons: Lucide glyphs (ISC, see LICENSE-lucide.md), copied as path data so no icon
// package ships with the app. One line family only; add a glyph by pasting its Lucide paths here.
import { memo } from 'react';
import Svg, { Circle, Path } from 'react-native-svg';

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
} satisfies Record<string, Glyph>;

export type IconName = keyof typeof GLYPHS;

export interface IconProps {
  name: IconName;
  /** Points; Lucide draws on a 24-unit grid. */
  size?: number;
  color: string;
  strokeWidth?: number;
}

/** Decorative by default: the control that holds it carries the accessibility label. */
export const Icon = memo(function Icon({ name, size = 20, color, strokeWidth = 2 }: IconProps) {
  const g: Glyph = GLYPHS[name];
  return (
    <Svg width={size} height={size} viewBox="0 0 24 24" pointerEvents="none">
      {g.paths.map((d) => (
        <Path
          key={d}
          d={d}
          fill="none"
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
