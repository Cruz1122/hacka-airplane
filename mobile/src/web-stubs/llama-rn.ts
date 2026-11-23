// Web replacement for llama.rn (see metro.config.js). On-device inference is native-only.
export function initLlama(): never {
  throw new Error('llama.rn is not available on web; run the assistant on an Android dev build');
}
