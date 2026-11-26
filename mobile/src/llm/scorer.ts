// Native index scorer: index_scorer.onnx is one MatMul q[1,768] x W[768,rows] built by the exporter
// with the index vectors as its weight. Hermes JS took 462 ms per query on the Moto (app/spike.tsx).
import type { Score } from '@/core/knowledge/engine';

import { findSideLoaded } from './embedder';
import { ort } from './ort';

export async function loadScorer(
  name: string,
  expectedBytes: number,
  io: { input: string; output: string },
): Promise<Score> {
  const file = findSideLoaded(name);
  if (!file) throw new Error(`scorer ${name} not found in app files; run scripts/push-knowledge.sh`);
  if (file.size !== expectedBytes) throw new Error(`scorer ${name}: ${file.size} bytes, manifest says ${expectedBytes}`);
  const { InferenceSession, Tensor } = ort();
  const session = await InferenceSession.create(file.uri.replace(/^file:\/\//, ''), { intraOpNumThreads: 4 });
  return async (q: Float32Array) => {
    const out = await session.run({ [io.input]: new Tensor('float32', q, [1, q.length]) });
    return out[io.output].data as Float32Array;
  };
}
