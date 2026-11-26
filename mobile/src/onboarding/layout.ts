// Screen split for the onboarding: the illustration on top, the cloud card at the bottom. Shared
// by the app screen and the Lab so the scene, its handles and the export see the same box.
import { CLOUD_EDGE } from '@/ui/CloudCard';
import { MAX_VIEW_WIDTH } from '@/onboarding/scene/geometry';
import { SCENE_HEIGHT } from '@/onboarding/scene/types';
import { PRIMARY_BUTTON_HEIGHT } from '@/ui/PrimaryButton';

/** Park emblem at the top of the card, with clear room under the vapor edge. */
export const EMBLEM_TOP = 64;
export const EMBLEM_SIZE = 64;

/** Card content from the top of its cloud edge to the button, in points. */
export const CARD_CONTENT =
  EMBLEM_TOP + EMBLEM_SIZE + 12 + 64 + 6 + 44 + 18 + 10 + 20 + PRIMARY_BUTTON_HEIGHT;

/** Space under the button: the bottom safe area, never less than a comfortable margin. */
export const cardBottomPadding = (bottomInset: number) => Math.max(bottomInset, 16) + 8;

export interface OnboardingLayout {
  /** Height of the cloud card, measured from the screen bottom. */
  card: number;
  /** Height of the scene drawing at the top; it runs under the card's cloud edge. */
  scene: number;
}

export function onboardingLayout(
  width: number,
  height: number,
  bottomInset: number,
): OnboardingLayout {
  const card = CARD_CONTENT + cardBottomPadding(bottomInset);
  // The scene never drops below half the screen, and never gets so wide and short that
  // sceneViewBox would crop the sky (and the Pet) off the top: on landscape tablets the card
  // covers more of the foreground instead.
  const scene = Math.max(
    height * 0.5,
    height - card + CLOUD_EDGE,
    (width * SCENE_HEIGHT) / MAX_VIEW_WIDTH,
  );
  return { card, scene: Math.min(scene, height) };
}
