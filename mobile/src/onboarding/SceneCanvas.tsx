// Web scene renderer: Skia on CanvasKit (WebGL), the native renderer's pictures and matrices
// (skia/SkiaSceneWeb.tsx). The SVG renderer re-rendered its React tree on every frame and held the
// onboarding near 30 fps. NevadoScene (SVG) stays the reference look; it draws the scene while
// CanvasKit loads (an 8 MB wasm the dev server serves, see metro.config.js) and for good when it
// cannot load, WebGL is missing or WebGL runs in software.
import { LoadSkiaWeb } from '@shopify/react-native-skia/lib/module/web';
import { lazy, Suspense, useSyncExternalStore } from 'react';

import { NevadoScene, type NevadoSceneProps } from './NevadoScene';

const CANVASKIT_URL = '/skia/canvaskit.wasm';

/**
 * WebGL backed by a GPU. Software WebGL (SwiftShader, llvmpipe) drew the Skia scene at 3-9 fps
 * where SVG ran near 30 (headless Chromium, CPU 4x), so it keeps SVG.
 */
function gpuWebGL(): boolean {
  if (typeof document === 'undefined') return false;
  const probe = document.createElement('canvas');
  const options: WebGLContextAttributes = { failIfMajorPerformanceCaveat: true };
  const gl = probe.getContext('webgl2', options) ?? probe.getContext('webgl', options);
  if (!gl) return false;
  const info = gl.getExtension('WEBGL_debug_renderer_info');
  const name = String(gl.getParameter(info ? info.UNMASKED_RENDERER_WEBGL : gl.RENDERER));
  gl.getExtension('WEBGL_lose_context')?.loseContext();
  return !/swiftshader|llvmpipe|softpipe|software|basic render/i.test(name);
}

// Once per page, and every scene on screen follows it: SVG when there is no GPU, when CanvasKit
// fails to load, or once a WebGL context is lost.
let svg: boolean | null = null;
const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

function isSvg() {
  svg ??= !gpuWebGL();
  return svg;
}

function toSvg() {
  svg = true;
  listeners.forEach((l) => l());
}

const SkiaScene = lazy(() =>
  LoadSkiaWeb({ locateFile: () => CANVASKIT_URL })
    // The Skia API binds to the CanvasKit global when its module first runs, so the renderer and
    // everything that imports Skia load only now.
    .then(() => import('./skia/SkiaSceneWeb'))
    .then((m) => ({ default: m.SkiaSceneWeb }))
    .catch((e: unknown) => {
      console.warn('Skia is unavailable; the scene draws with SVG.', e);
      toSvg();
      return { default: NevadoScene };
    }),
);

export function SceneCanvas(props: NevadoSceneProps) {
  const fallback = useSyncExternalStore(subscribe, isSvg, isSvg);
  if (fallback) return <NevadoScene {...props} />;
  return (
    <Suspense fallback={<NevadoScene {...props} />}>
      <SkiaScene {...props} onLost={toSvg} />
    </Suspense>
  );
}
