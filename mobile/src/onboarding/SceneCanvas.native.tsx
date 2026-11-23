// Native scene renderer: the SceneDoc drawn on one Skia canvas (GPU). See skia/drawScene.ts for
// why native does not use the SVG renderer; web keeps NevadoScene (SceneCanvas.tsx).
import { Canvas, Picture, Skia, type SkCanvas } from '@shopify/react-native-skia';
import { useMemo } from 'react';

import { drawPet } from '@/ui/pet/drawPet';
import { blinkAt, PET_PRESET, petFrame, type PetConfig } from '@/ui/pet/petCore';
import { useFaceTransition } from '@/ui/pet/useFaceTransition';
import { useReducedMotion } from '@/ui/useReducedMotion';

import type { NevadoSceneProps } from './NevadoScene';
import { resolveColor } from './scene/doc';
import type { PetBody, SceneDoc } from './scene/types';
import { drawFrame, layoutFrame } from './skia/drawScene';

function petOf(doc: SceneDoc): PetBody | null {
  for (const l of doc.layers) {
    if (!l.visible) continue;
    for (const o of l.objects) if (o.body.kind === 'pet') return o.body;
  }
  return null;
}

const NO_PET: PetBody['emotion'] = 'happy';

export function SceneCanvas({ doc, width, height }: NevadoSceneProps) {
  const reduced = useReducedMotion();
  const pet = petOf(doc);
  const motion = PET_PRESET.motion;
  // The emotion track steps halfway through a swipe; the face morphs like the Pet component's.
  const face = useFaceTransition(
    PET_PRESET.poses,
    pet?.emotion ?? NO_PET,
    reduced ? 0 : motion.transition,
    motion.easing,
  );
  const picture = useMemo(() => {
    const frame = layoutFrame(doc, width, height);
    let paintPet: (c: SkCanvas) => void = () => {};
    if (pet) {
      const cfg: PetConfig = {
        ...PET_PRESET,
        emotion: pet.emotion,
        voice: pet.voice,
        audio: pet.audio,
      };
      const f = petFrame(cfg, {
        time: pet.clock,
        face,
        blink: blinkAt(pet.clock, motion.blinkInterval),
      });
      const fill = resolveColor(doc.palette, pet.fill);
      const shade = resolveColor(doc.palette, pet.shade);
      paintPet = (c) => drawPet(c, cfg, f, fill, shade);
    }
    const recorder = Skia.PictureRecorder();
    drawFrame(recorder.beginRecording(Skia.XYWHRect(0, 0, width, height)), frame, paintPet);
    return recorder.finishRecordingAsPicture();
  }, [doc, width, height, pet, face, motion.blinkInterval]);
  return (
    <Canvas style={{ width, height }}>
      <Picture picture={picture} />
    </Canvas>
  );
}
