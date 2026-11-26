// Sizes a role card's Pet from the card's measured box: the cards share the screen's spare height,
// so the circle grows with it, held between a floor that still reads and a ceiling that leaves
// room for the label under it.

/** Share of the card's height the circle takes. */
const SHARE = 0.55;
export const ROLE_CIRCLE_MIN = 88;
export const ROLE_CIRCLE_MAX = 220;
/** The circle never takes more than this share of the card's width. */
const WIDTH_SHARE = 0.6;

/**
 * Diameter of the teal circle that holds the role's Pet, for a card `height` x `width` whose
 * padding and label take `reserved` points of its height.
 */
export function roleCircleSize(height: number, width: number, reserved: number): number {
  const fit = Math.min(height * SHARE, height - reserved, width * WIDTH_SHARE);
  return Math.round(Math.max(ROLE_CIRCLE_MIN, Math.min(ROLE_CIRCLE_MAX, fit)));
}
