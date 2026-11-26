import {
  AlphaType,
  ColorType,
  FilterMode,
  MipmapMode,
  Skia,
} from '@shopify/react-native-skia';
import { Asset } from 'expo-asset';
import { File } from 'expo-file-system';
import type { InferenceSession } from 'onnxruntime-react-native';

import { ort } from '@/llm/ort';

import { matchPhoto } from './matchPhoto';
import { imageSize as size, normalizePixels, paddingColor, photoFrames } from './pixels';

// eslint-disable-next-line @typescript-eslint/no-require-imports
const encoderAsset: number = require('../../assets/vision/encoder.onnx');
let encoder: Promise<InferenceSession> | undefined;

function session(): Promise<InferenceSession> {
  encoder ??= Asset.loadAsync(encoderAsset).then(([asset]) => {
    if (!asset?.localUri) throw new Error('Falta el codificador visual local');
    return ort().InferenceSession.create(asset.localUri.replace(/^file:\/\//, ''));
  }).catch((error: unknown) => {
    encoder = undefined;
    throw error;
  });
  return encoder;
}

export async function classifyPhoto(uri: string) {
  const data = Skia.Data.fromBytes(await new File(uri).bytes());
  try {
    const image = Skia.Image.MakeImageFromEncoded(data);
    if (!image) throw new Error('Formato de foto no compatible');
    try {
      const surface = Skia.Surface.MakeOffscreen(size, size);
      if (!surface) throw new Error('No se pudo preparar la foto');
      try {
        const runtime = await session();
        const { Tensor } = ort();
        const canvas = surface.getCanvas();
        for (const { source, destination, padded } of photoFrames(image.width(), image.height())) {
          if (padded) canvas.clear(Skia.Color(paddingColor));
          canvas.drawImageRectOptions(
            image, Skia.XYWHRect(...source), Skia.XYWHRect(...destination), FilterMode.Linear, MipmapMode.None,
          );
          const pixels = canvas.readPixels(0, 0, {
            width: size, height: size, colorType: ColorType.RGBA_8888, alphaType: AlphaType.Unpremul,
          });
          if (!pixels) throw new Error('No se pudieron leer los píxeles');
          const input = normalizePixels(pixels);
          const result = await runtime.run({ pixel_values: new Tensor('float32', input, [1, 3, size, size]) });
          const vector = result[runtime.outputNames[0]].data;
          if (!(vector instanceof Float32Array)) throw new Error('Vector de imagen inválido');
          const match = matchPhoto(vector);
          if (match) return match;
        }
      } finally {
        surface.dispose();
      }
    } finally {
      image.dispose();
    }
  } finally {
    data.dispose();
  }
}
