// The chat header's scene, as data: kept apart from ChatBackdrop so layout code and tests can use it
// without loading a renderer.
import { updateLayer } from '@/onboarding/scene/doc';
import { defaultScene } from '@/onboarding/scene/preset';
import { evaluateTracks } from '@/onboarding/scene/timeline';
import type { LayerId } from '@/onboarding/scene/types';

import { withHeaderPeaks } from './headerPeaks';

/**
 * Layers the header leaves out: the volcano (the user wants the ranges behind it, not the summit
 * cut by the sheet) and the scene's Pet, which lives in the circle instead.
 */
const HIDDEN: LayerId[] = ['mainVolcano', 'snowCap', 'crater', 'ruizMascot'];

/**
 * The scene at the last onboarding screen, without the layers above, with the three nevados in
 * the ranges. The hidden volcano stays in the doc: chatLayout places the header by its crater.
 */
export const headerScene = withHeaderPeaks(
  HIDDEN.reduce(
    (doc, id) => updateLayer(doc, id, { visible: false }),
    evaluateTracks(defaultScene(), 2),
  ),
);
