export const imageSize = 224;
export const paddingColor = '#7c7468';

type Rect = [x: number, y: number, width: number, height: number];

export function* photoFrames(width: number, height: number): Generator<{
  source: Rect;
  destination: Rect;
  padded: boolean;
}> {
  const side = Math.min(width, height);
  const longSide = Math.max(width, height);
  yield {
    source: [Math.floor((width - side) / 2), Math.floor((height - side) / 2), side, side],
    destination: [0, 0, imageSize, imageSize],
    padded: false,
  };
  // A square crop can remove the shoreline or another feature at the edge of a wide photo.
  if (longSide < side * 1.25) return;
  const fitWidth = Math.max(1, Math.round(width * imageSize / longSide));
  const fitHeight = Math.max(1, Math.round(height * imageSize / longSide));
  yield {
    source: [0, 0, width, height],
    destination: [Math.floor((imageSize - fitWidth) / 2), Math.floor((imageSize - fitHeight) / 2), fitWidth, fitHeight],
    padded: true,
  };
}

export function normalizePixels(pixels: ArrayLike<number>): Float32Array {
  const plane = imageSize * imageSize;
  if (pixels.length !== plane * 4) throw new Error('Número de píxeles inesperado');
  const input = new Float32Array(plane * 3);
  const mean = [0.485, 0.456, 0.406];
  const deviation = [0.229, 0.224, 0.225];
  for (let channel = 0; channel < 3; channel++) {
    for (let pixel = 0; pixel < plane; pixel++) {
      input[channel * plane + pixel] = (pixels[pixel * 4 + channel] / 255 - mean[channel]) / deviation[channel];
    }
  }
  return input;
}
