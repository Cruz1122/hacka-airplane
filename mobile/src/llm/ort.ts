// onnxruntime-react-native, loaded lazily: requiring the package installs its native JSI binding,
// and expo-router evaluates every route at startup, so a static import would run native code on
// screens (and the web build) that never use it.
import type * as Ort from 'onnxruntime-react-native';

export function ort(): typeof Ort {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  return require('onnxruntime-react-native');
}
