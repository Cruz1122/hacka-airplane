// The sources behind one assistant reply. Only passages the reply cites AND the turn retrieved
// count: a cited id the tools never returned is the model's guess, not a source. The world's
// passages carry no links (it is the benchmark park), so each source is its station or the park
// plus the passage itself, verbatim.
import type { World } from '@/core/world';
import { parseCitations, type ChatSource } from '@/ui/chat/citations';

export function messageSources(
  text: string,
  world: World,
  retrieved: Iterable<string>,
): ChatSource[] {
  const shown = new Set(retrieved);
  const { meta } = world.json;
  return parseCitations(text).ids.flatMap((id) => {
    const passage = shown.has(id) ? (world.passages.get(id) ?? world.filler.get(id)) : undefined;
    // Injection passages exist to test the guards; they are never a source to show a visitor.
    if (!passage || passage.field === meta.injection_field) return [];
    const station = passage.station ? world.stations.get(passage.station)?.name : undefined;
    return [{ id, title: station ?? meta.park_name, excerpt: passage.text }];
  });
}
