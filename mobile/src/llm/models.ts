// Single registry of selectable models. Swapping the model = picking another id.
// This file must stay free of native imports so jest can load it.

export type ModelId = 'gemma4-e2b' | 'qwen3-0.6b-router' | 'qwen3-0.6b' | 'qwen3-1.7b' | 'granite4-micro';

export interface ModelQuirks {
  // Qwen3 template renders an empty `<think>\n\n</think>` block when enable_thinking is false.
  // Used only to sanity-check the formatted prompt, which must match the Python /apply-template output.
  emptyThinkBlock: boolean;
  // Extra stop strings on top of EOS. The schema grammar normally ends generation first.
  stop: string[];
}

export interface ModelSpec {
  id: ModelId;
  // File name pattern in the app files dir; `*` matches any run of characters, case-insensitive.
  file: string;
  label: string;
  quirks: ModelQuirks;
}

export const MODELS: readonly ModelSpec[] = [
  {
    id: 'gemma4-e2b',
    file: 'gemma-4-E2B-it-Q4_K_M.gguf',
    label: 'Gemma 4 E2B',
    // TODO(gemma4 stop token, unverified on device): EOS ends generation today; add the real end-of-turn string if a run shows overrun.
    quirks: { emptyThinkBlock: false, stop: [] },
  },
  {
    id: 'qwen3-0.6b-router',
    file: 'qwen3-0.6b-router-*-Q4_K_M.gguf',
    label: 'Qwen3 0.6B router (fine-tuned)',
    quirks: { emptyThinkBlock: true, stop: ['<|im_end|>'] },
  },
  {
    id: 'qwen3-0.6b',
    file: 'Qwen3-0.6B-Q4_K_M.gguf',
    label: 'Qwen3 0.6B',
    quirks: { emptyThinkBlock: true, stop: ['<|im_end|>'] },
  },
  {
    id: 'qwen3-1.7b',
    file: 'Qwen3-1.7B-Q4_K_M.gguf',
    label: 'Qwen3 1.7B',
    quirks: { emptyThinkBlock: true, stop: ['<|im_end|>'] },
  },
  {
    id: 'granite4-micro',
    file: 'granite-4.0-micro-Q4_K_M.gguf',
    label: 'Granite 4.0 Micro',
    quirks: { emptyThinkBlock: false, stop: [] },
  },
];

export const DEFAULT_MODEL_ID: ModelId = 'gemma4-e2b';

export function getModelSpec(id: string): ModelSpec {
  const spec = MODELS.find((m) => m.id === id);
  if (!spec) throw new Error(`Unknown model id "${id}"; known: ${MODELS.map((m) => m.id).join(', ')}`);
  return spec;
}

function globToRegExp(glob: string): RegExp {
  const escaped = glob.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*');
  return new RegExp(`^${escaped}$`, 'i');
}

// With several matches (e.g. two router checkpoints) the lexicographically last name wins.
export function resolveModelFile(spec: ModelSpec, fileNames: readonly string[]): string | null {
  const re = globToRegExp(spec.file);
  const hits = fileNames.filter((n) => re.test(n)).sort();
  return hits.length ? hits[hits.length - 1] : null;
}
