// Small inline SVG icons for the web-only Lab (DOM elements, not react-native-svg).
const paths = {
  eye: 'M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8Z M8 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z',
  eyeOff:
    'M2 2l12 12 M6.2 4c.6-.3 1.2-.5 1.8-.5 4 0 6.5 4.5 6.5 4.5s-.6 1.1-1.7 2.2 M10.6 11.8c-.8.4-1.7.7-2.6.7-4 0-6.5-4.5-6.5-4.5s.9-1.6 2.5-2.9',
  lock: 'M4 7.5h8v6H4z M5.5 7.5V5.5a2.5 2.5 0 0 1 5 0v2',
  unlock: 'M4 7.5h8v6H4z M5.5 7.5V5.5a2.5 2.5 0 0 1 4.8-1',
  up: 'M8 13V3 M4 7l4-4 4 4',
  down: 'M8 3v10 M4 9l4 4 4-4',
  copy: 'M5.5 5.5h7v7h-7z M3.5 10.5v-7h7',
  trash: 'M3 4.5h10 M6.5 4.5V3h3v1.5 M4.5 4.5l.7 8.5h5.6l.7-8.5',
  chevronRight: 'M6 3.5 10.5 8 6 12.5',
  chevronDown: 'M3.5 6 8 10.5 12.5 6',
  undo: 'M5.5 3 2.5 6l3 3 M2.5 6h7a4 4 0 0 1 0 8H7',
  redo: 'M10.5 3l3 3-3 3 M13.5 6h-7a4 4 0 0 0 0 8H9',
} as const;

export type IconName = keyof typeof paths;

export function Icon({ name, size = 16 }: { name: IconName; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.4}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name]} />
    </svg>
  );
}
