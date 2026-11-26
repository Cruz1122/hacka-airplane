// Web replacement for onnxruntime-react-native (see metro.config.js). Its binding installs a JSI
// module at import time, which the browser lacks; the Laya session is native-only. Only the
// exports src/llm/laya.ts uses exist here, and each fails on use rather than faking inference.
function unsupported(): never {
  throw new Error(
    'onnxruntime-react-native is not available on web; run Laya on an Android dev build',
  );
}

export const InferenceSession = { create: unsupported };

export class Tensor {
  constructor() {
    unsupported();
  }
}
