import classes from '@/../assets/vision/classes.json';
import references from '@/../assets/vision/index.json';

type ClassId = keyof typeof classes;
const mountainMatch = {
  label: 'un paisaje de alta montaña',
  entryId: 'geography.main_peaks',
};

export type PhotoMatch = (typeof classes)[ClassId] | typeof mountainMatch;

type ReferenceId = ClassId | 'other';

const thresholds: Record<ClassId, { minimum: number; margin: number }> = {
  frailejon: { minimum: 0.42, margin: 0.06 },
  otun: { minimum: 0.35, margin: 0.04 },
  roca: { minimum: 0.29, margin: 0.06 },
  chivito: { minimum: 0.43, margin: 0.06 },
  condor: { minimum: 0.43, margin: 0.06 },
  persona: { minimum: 0.27, margin: 0.04 },
  ruiz: { minimum: 0.47, margin: 0.09 },
  dulima: { minimum: 0.47, margin: 0.09 },
  santa_isabel: { minimum: 0.47, margin: 0.09 },
  pato_andino: { minimum: 0.41, margin: 0.04 },
  picoespada: { minimum: 0.41, margin: 0.03 },
  mariposa_cydno: { minimum: 0.40, margin: 0.05 },
  abejorro_funebris: { minimum: 0.42, margin: 0.05 },
};

const mountains = new Set<ReferenceId>(['ruiz', 'dulima', 'santa_isabel']);

export function matchPhoto(vector: Float32Array): PhotoMatch | undefined {
  const norm = Math.hypot(...vector);
  if (vector.length !== 1024 || !Number.isFinite(norm) || norm === 0) return;

  const similarities = new Map<ReferenceId, number[]>();
  for (const reference of references) {
    const id = reference.classId as ReferenceId;
    let dot = 0;
    for (let i = 0; i < vector.length; i++) dot += vector[i] * reference.vector[i];
    const scores = similarities.get(id) ?? [];
    scores.push(dot / norm);
    similarities.set(id, scores);
  }
  const ranked = [...similarities].map(([id, scores]) => {
    scores.sort((a, b) => b - a);
    const nearest = scores.slice(0, 3);
    const mean = nearest.reduce((sum, score) => sum + score, 0) / nearest.length;
    // Landscape classes need support from several views, since one silhouette can be misleading.
    const score = id === 'otun' || mountains.has(id) ? 0.80 * nearest[0] + 0.20 * mean : nearest[0];
    return { id, score };
  }).sort((a, b) => b.score - a.score);
  const [best, runnerUp] = ranked;
  if (!best || !runnerUp || best.id === 'other') return;
  // These empirical floors are similarities, not calibrated probabilities.
  const { minimum, margin } = thresholds[best.id];
  if (best.score < minimum) return;
  if (best.score - runnerUp.score >= margin) return classes[best.id];

  // Similar mountain views can support the landscape without supporting a specific summit.
  if (mountains.has(best.id) && mountains.has(runnerUp.id) && best.score >= 0.57) {
    const alternative = ranked.find(({ id }) => !mountains.has(id));
    if (alternative && best.score - alternative.score >= 0.05) return mountainMatch;
  }
}
