import { Asset } from 'expo-asset';
import { useIsFocused } from 'expo-router';
import jsQR from 'jsqr';
import { useEffect, useRef } from 'react';
import { StyleSheet, View } from 'react-native';

import { ScanFrame } from './ScanFrame';
import { radius } from './theme/tokens';

function imagePixels(
  canvas: HTMLCanvasElement,
  image: CanvasImageSource,
  width: number,
  height: number,
) {
  const scale = Math.min(1, 1000 / Math.max(width, height));
  const w = Math.round(width * scale);
  const h = Math.round(height * scale);
  if (!w || !h) return;
  if (canvas.width !== w) canvas.width = w;
  if (canvas.height !== h) canvas.height = h;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  if (!ctx) throw new Error('El navegador no pudo leer el QR.');
  ctx.drawImage(image, 0, 0, w, h);
  return ctx.getImageData(0, 0, w, h);
}

function decodeFrame(frame: ImageData | undefined) {
  return frame && jsQR(frame.data, frame.width, frame.height)?.data;
}

export async function readQrImage(uri: string) {
  const image = new Image();
  image.src = uri;
  await image.decode();
  const frame = imagePixels(
    document.createElement('canvas'),
    image,
    image.naturalWidth,
    image.naturalHeight,
  );
  const code = decodeFrame(frame);
  if (code || !frame) return code;
  const { prepareZXingModule, readBarcodes } = await import('zxing-wasm/reader');
  // Metro registers the bundled WASM asset when resolving this static require.
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const wasm = Asset.fromModule(require('zxing-wasm/reader/zxing_reader.wasm'));
  const url = new URL(wasm.uri, window.location.href).href;
  await prepareZXingModule({ overrides: { locateFile: () => url }, fireImmediately: true });
  const results = await readBarcodes(frame, { formats: ['QRCode'], tryHarder: true });
  return results.find(({ isValid }) => isValid)?.text;
}

export function QrCamera({
  onCode,
  onError,
}: {
  onCode: (code: string) => void;
  onError: () => void;
}) {
  const video = useRef<HTMLVideoElement>(null);
  const focused = useIsFocused();
  useEffect(() => {
    if (!focused) return;
    const preview = video.current;
    if (!preview || !navigator.mediaDevices?.getUserMedia) {
      onError();
      return;
    }
    let active = true;
    let stream: MediaStream | undefined;
    let timer: ReturnType<typeof setInterval> | undefined;
    const canvas = document.createElement('canvas');
    const stop = () => {
      active = false;
      clearInterval(timer);
      stream?.getTracks().forEach((track) => track.stop());
    };
    void navigator.mediaDevices
      .getUserMedia({ video: { facingMode: { ideal: 'environment' } }, audio: false })
      .then(async (media) => {
        stream = media;
        if (!active) return stop();
        preview.srcObject = media;
        await preview.play();
        if (!active) return;
        timer = setInterval(() => {
          if (!preview.videoWidth) return;
          try {
            const code = decodeFrame(
              imagePixels(canvas, preview, preview.videoWidth, preview.videoHeight),
            );
            if (code) {
              stop();
              onCode(code);
            }
          } catch {
            stop();
            onError();
          }
        }, 260);
      })
      .catch(() => {
        if (active) {
          stop();
          onError();
        }
      });
    return stop;
  }, [focused, onCode, onError]);
  return (
    <View style={styles.preview}>
      <video
        ref={video}
        playsInline
        muted
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
      <ScanFrame />
    </View>
  );
}

const styles = StyleSheet.create({
  preview: { aspectRatio: 4 / 3, borderRadius: radius.lg, overflow: 'hidden' },
});
