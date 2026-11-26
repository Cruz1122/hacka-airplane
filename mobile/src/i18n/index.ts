// UI copy. Each language is one file with the same shape as `es`; adding one means a new file
// plus a line in LOCALES, and the type checker rejects a file with missing or extra keys.
import { en } from './en';
import { es } from './es';

export type Labels = typeof es;

export const LOCALES = { es, en } satisfies Record<string, Labels>;
export type Locale = keyof typeof LOCALES;

/**
 * Active UI language. Fixed on purpose: the park knowledge and the assistant's answers are
 * Spanish only, so following the device language would mix languages on one screen.
 */
export const LOCALE: Locale = 'es';

export const t: Labels = LOCALES[LOCALE];

/** Replaces each `{name}` in a label; a placeholder without a value is a bug in the caller. */
export function fill(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (_, name: string) => {
    if (!(name in values)) throw new Error(`Label "${template}" needs a value for {${name}}`);
    return String(values[name]);
  });
}
