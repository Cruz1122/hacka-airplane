// Dev-only device spike (docs/history/phase3-implementation-plan.md unit 6): open nevados://spike.
// Loads the real runtime (e5 GGUF + vectors + ONNX scorer), asks the 120 retrieval fixture
// questions and checks every pool against the Python export. Logs one "SPIKE {json}" line to Metro.
import { useEffect, useState } from 'react';
import { ScrollView, Text } from 'react-native';

import retrievalFx from '@/core/knowledge/__fixtures__/retrieval.json';
import { loadKnowledgeRuntime } from '@/llm/knowledgeRuntime';

const pct = (xs: number[], p: number) => {
  const s = [...xs].sort((a, b) => a - b);
  return Math.round(s[Math.min(s.length - 1, Math.floor((s.length * p) / 100))]);
};

async function runSpike(log: (k: string, v: unknown) => void): Promise<void> {
  const rt = await loadKnowledgeRuntime();
  log('runtime_load_ms', Math.round(rt.loadMs));
  const embed: number[] = [];
  const score: number[] = [];
  const total: number[] = [];
  const mismatches: string[] = [];
  for (const row of retrievalFx.rows) {
    const r = await rt.engine.ask(row.q);
    if (r.error) throw r.error;
    embed.push(r.timing.embedMs);
    score.push(r.timing.retrieveMs);
    total.push(r.timing.totalMs);
    if (JSON.stringify(r.retrieval?.pool) !== JSON.stringify(row.pool)) mismatches.push(row.q);
  }
  log('n', retrievalFx.rows.length);
  log('pool_mismatches', mismatches.length);
  log('mismatch_queries', mismatches.slice(0, 5));
  log('first_total_ms', Math.round(total[0]));
  log('embed_ms_p50_p95', [pct(embed, 50), pct(embed, 95)]);
  log('retrieve_ms_p50_p95', [pct(score, 50), pct(score, 95)]);
  log('total_ms_p50_p95_max', [pct(total, 50), pct(total, 95), Math.round(Math.max(...total))]);
  await rt.release();
}

export default function Spike() {
  const [out, setOut] = useState<Record<string, unknown>>({});
  useEffect(() => {
    const acc: Record<string, unknown> = {};
    const log = (k: string, v: unknown) => {
      acc[k] = v;
      setOut({ ...acc });
    };
    runSpike(log)
      .catch((e: unknown) => log('error', e instanceof Error ? e.message : String(e)))
      .finally(() => console.log('SPIKE ' + JSON.stringify(acc)));
  }, []);
  return (
    <ScrollView contentContainerStyle={{ padding: 24 }}>
      <Text selectable style={{ fontFamily: 'monospace' }}>
        {JSON.stringify(out, null, 2)}
      </Text>
    </ScrollView>
  );
}
