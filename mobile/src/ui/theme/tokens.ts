// Neutral placeholder tokens; visual design is decided later.
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
export const radius = { sm: 6, md: 12, lg: 20 } as const;
export const fontSize = { sm: 13, md: 16, lg: 20, xl: 28 } as const;
