import { MODELS, getModelSpec, resolveModelFile } from './models';

describe('model registry', () => {
  const files = [
    'gemma-4-E2B-it-Q4_K_M.gguf',
    'qwen3-0.6b-router-r1-Q4_K_M.gguf',
    'qwen3-0.6b-router-r2-Q4_K_M.gguf',
    'Qwen3-0.6B-Q4_K_M.gguf',
    'Qwen3-1.7B-Q4_K_M.gguf',
    'notes.txt',
  ];

  it('resolves each id to its own file', () => {
    expect(resolveModelFile(getModelSpec('gemma4-e2b'), files)).toBe('gemma-4-E2B-it-Q4_K_M.gguf');
    expect(resolveModelFile(getModelSpec('qwen3-0.6b'), files)).toBe('Qwen3-0.6B-Q4_K_M.gguf');
    expect(resolveModelFile(getModelSpec('qwen3-1.7b'), files)).toBe('Qwen3-1.7B-Q4_K_M.gguf');
  });

  it('router glob picks the newest name and never matches the base 0.6b', () => {
    expect(resolveModelFile(getModelSpec('qwen3-0.6b-router'), files)).toBe('qwen3-0.6b-router-r2-Q4_K_M.gguf');
    expect(resolveModelFile(getModelSpec('qwen3-0.6b'), ['qwen3-0.6b-router-r1-Q4_K_M.gguf'])).toBeNull();
  });

  it('is case-insensitive and null when absent', () => {
    expect(resolveModelFile(getModelSpec('qwen3-1.7b'), ['QWEN3-1.7B-q4_k_m.GGUF'])).toBe('QWEN3-1.7B-q4_k_m.GGUF');
    expect(resolveModelFile(getModelSpec('gemma4-e2b'), ['notes.txt'])).toBeNull();
  });

  it('has unique ids and rejects unknown ones', () => {
    expect(new Set(MODELS.map((m) => m.id)).size).toBe(MODELS.length);
    expect(() => getModelSpec('nope')).toThrow(/Unknown model id/);
  });
});
