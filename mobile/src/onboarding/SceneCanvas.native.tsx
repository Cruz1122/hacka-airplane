// Native scene renderer: the SceneDoc drawn on one Skia canvas (GPU). See skia/drawScene.ts for
// why native does not use the SVG renderer; web keeps NevadoScene (SceneCanvas.tsx).
import { Canvas, Picture, Skia, type SkPicture } from '@shopify/react-native-skia';
import { useMemo } from 'react';

import { drawPet } from '@/ui/pet/drawPet';
import { blinkAt, PET_PRESET, petFrame, type FaceState, type PetConfig } from '@/ui/pet/petCore';
import { useFaceTransition } from '@/ui/pet/useFaceTransition';
import { useReducedMotion } from '@/ui/useReducedMotion';

import type { NevadoSceneProps } from './NevadoScene';
import { resolveColor } from './scene/doc';
import type { PetBody, SceneDoc } from './scene/types';
import { drawFrame, layoutFrame, recordPicture } from './skia/drawScene';

function petOf(doc: SceneDoc): PetBody | null {
  for (const l of doc.layers) {
    if (!l.visible) continue;
    for (const o of l.objects) if (o.body.kind === 'pet') return o.body;
  }
  return null;
}

const NO_PET: PetBody['emotion'] = 'happy';

/** One Pet frame in its own coordinates; the scene replays it under the Pet's matrix. */
function petPicture(
  pose: Pick<PetBody, 'emotion' | 'voice' | 'audio' | 'clock'>,
  face: FaceState,
  fill: string,
  shade: string,
): SkPicture {
  const cfg: PetConfig = {
    ...PET_PRESET,
    emotion: pose.emotion,
    voice: pose.voice,
    audio: pose.audio,
  };
  const f = petFrame(cfg, {
    time: pose.clock,
    face,
    blink: blinkAt(pose.clock, PET_PRESET.motion.blinkInterval),
  });
  return recordPicture((c) => drawPet(c, cfg, f, fill, shade));
}

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
  // Three steps, each redone only when its inputs change. The Pet's are values, not its body:
  // tracks rebuild that body on every frame, but its pose holds still while the camera moves with
  // the idle clock held, and between idle ticks during a drag.
  const frame = useMemo(() => layoutFrame(doc, width, height), [doc, width, height]);
  const emotion = pet?.emotion;
  const voice = pet?.voice;
  const audio = pet?.audio;
  const clock = pet?.clock;
  const fill = pet && resolveColor(doc.palette, pet.fill);
  const shade = pet && resolveColor(doc.palette, pet.shade);
  const petShot = useMemo(
    () =>
      emotion !== undefined &&
      voice !== undefined &&
      audio !== undefined &&
      clock !== undefined &&
      fill &&
      shade
        ? petPicture({ emotion, voice, audio, clock }, face, fill, shade)
        : null,
    [emotion, voice, audio, clock, face, fill, shade],
  );
  const picture = useMemo(() => {
    const recorder = Skia.PictureRecorder();
    drawFrame(recorder.beginRecording(Skia.XYWHRect(0, 0, width, height)), frame, (c) => {
      if (petShot) c.drawPicture(petShot);
    });
    return recorder.finishRecordingAsPicture();
  }, [frame, petShot, width, height]);
  return (
    <Canvas style={{ width, height }}>
      <Picture picture={picture} />
    </Canvas>
  );
}
