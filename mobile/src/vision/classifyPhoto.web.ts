import type * as Ort from 'onnxruntime-web/wasm';

import { matchPhoto } from './matchPhoto';
import { imageSize, normalizePixels, paddingColor, photoFrames } from './pixels';

let encoder: Promise<{ session: Ort.InferenceSession; Tensor: typeof Ort.Tensor }> | undefined;

function session() {
  const host = window as Window & { ort?: typeof Ort };
  // Metro cannot transform the dynamic WASM imports in ORT's browser distribution.
  const load = async () => {
    if (!host.ort) {
      await new Promise<void>((resolve, reject) => {
        const script = document.createElement('script');
        script.src = '/knowledge-files/ort.wasm.min.js';
        script.onload = () => { script.remove(); resolve(); };
        script.onerror = () => { script.remove(); reject(new Error('No se pudo cargar ONNX Web')); };
        document.head.appendChild(script);
      });
    }
    if (!host.ort) throw new Error('No se encontró ONNX Web');
    const { env, InferenceSession, Tensor } = host.ort;
    env.wasm.numThreads = 1;
    env.wasm.wasmPaths = new URL('/knowledge-files/', window.location.href).href;
    const session = await InferenceSession.create('/knowledge-files/vision-encoder.onnx', {
      executionProviders: ['wasm'],
    });
    return { session, Tensor };
  };
  encoder ??= load().catch((error: unknown) => {
    encoder = undefined;
    throw error;
  });
  return encoder;
}

export async function classifyPhoto(uri: string) {
  const image = new Image();
  image.src = uri;
  await image.decode();

  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = imageSize;
  const context = canvas.getContext('2d');
  if (!context) throw new Error('No se pudo preparar la foto');
  const { session: runtime, Tensor } = await session();
  for (const { source, destination, padded } of photoFrames(image.naturalWidth, image.naturalHeight)) {
    if (padded) {
      context.fillStyle = paddingColor;
      context.fillRect(0, 0, imageSize, imageSize);
    }
    context.drawImage(image, ...source, ...destination);
    const input = normalizePixels(context.getImageData(0, 0, imageSize, imageSize).data);
    const result = await runtime.run({
      pixel_values: new Tensor('float32', input, [1, 3, imageSize, imageSize]),
    });
    const vector = result[runtime.outputNames[0]].data;
    if (!(vector instanceof Float32Array)) throw new Error('Vector de imagen inválido');
    const match = matchPhoto(vector);
    if (match) return match;
  }
}
