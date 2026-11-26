import type { CatalogEntry } from '@/core/knowledge/assets';
import { checkPatch } from '@/core/knowledge/qrIndex';
import { validateKnowledgePatch, type KnowledgePatch } from '@/core/knowledge/qrPatch';
import { t } from '@/i18n';
import { knowledgeAssets } from '@/llm/knowledgeAssets';

import { KNOWLEDGE_PATCH_KEY, knowledgePatchStorage } from './knowledgePatchStorage';

export interface AdminEntry {
  id: string;
  label: string;
  section?: string;
  original?: CatalogEntry;
  patch?: KnowledgePatch;
}

export async function readAdminCatalog(): Promise<AdminEntry[]> {
  const saved = await knowledgePatchStorage(KNOWLEDGE_PATCH_KEY).read();
  const records =
    saved === null ? [] : (JSON.parse(saved) as { records: { patch: KnowledgePatch }[] }).records;
  const menu = new Map(
    knowledgeAssets.catalog.map((row) => [
      row.id,
      {
        id: row.id,
        label: row.menu_label || row.label,
        section: row.section,
        original: row,
      } as AdminEntry,
    ]),
  );
  for (const { patch: raw } of records) {
    const patch = validateKnowledgePatch(raw);
    const original = menu.get(patch.id)?.original;
    menu.set(patch.id, {
      id: patch.id,
      label:
        patch.op === 'put'
          ? patch.entry.title
          : original?.menu_label || original?.label || t.knowledgeAdmin.retiredTitle,
      section:
        patch.op === 'put' ? patch.entry.section : (original?.section ?? patch.id.split('.')[0]),
      original,
      patch,
    });
  }
  return [...menu.values()]
    .filter(({ id }) => {
      try {
        checkPatch(knowledgeAssets, { id, revision: 1, op: 'remove' });
        return true;
      } catch {
        return false;
      }
    })
    .sort((a, b) => a.label.localeCompare(b.label, 'es'));
}
