import type { CatalogEntry, DepthEntry, KnowledgeAssets, LoadedIndex } from './assets';
import type { KnowledgePatch } from './qrPatch';

export interface IndexedPatch {
  patch: KnowledgePatch;
  vectors: number[][];
}

export function checkPatch(assets: KnowledgeAssets, patch: KnowledgePatch): void {
  const original = assets.catalog.find(({ id }) => id === patch.id);
  const { emergency_line_id, emergency_direct } = assets.policy;
  if (patch.id === emergency_line_id || emergency_direct.includes(patch.id) ||
      original?.kind === 'emergency' || original?.section === 'health_safety') {
    throw new Error('Las fichas de seguridad solo se actualizan con una versión de la app.');
  }
  if (patch.op === 'put' &&
      (patch.entry.section === 'health_safety' || !assets.manifest.section_rows.includes(patch.entry.section))) {
    throw new Error('La sección de esta ficha no admite actualizaciones por QR.');
  }
}

function depthFor(patch: Extract<KnowledgePatch, { op: 'put' }>): DepthEntry {
  const { answer, variants, more, why, related } = patch.entry;
  const detail = (text: string, i: number) => ({ text, atoms: ['detail_' + i] });
  const reasons = why.map((text, i) => ({ text, atoms: ['reason_' + i] }));
  const details = more.map(detail);
  return {
    l0: [answer, ...variants].map((text) => ({ text, atoms: [] })),
    layers: [
      ...details.map((item) => ({ kind: 'specifics', texts: [item] })),
      ...reasons.map((item) => ({ kind: 'why', texts: [item] })),
    ],
    walk: related.filter((id) => id !== patch.id),
    complements: [...details, ...reasons].flatMap(({ atoms }) => atoms),
  };
}

export function patchIndex(assets: KnowledgeAssets, base: LoadedIndex, records: readonly IndexedPatch[]) {
  const catalog = new Map(assets.catalog.map((entry) => [entry.id, entry]));
  const depth: Record<string, DepthEntry> = { ...assets.depth?.entries };
  const ids = [...base.ids];
  const positions = new Map(ids.map((id, i) => [id, i]));
  const entryRows = [...base.entryRows];
  const rowSection = base.rowSection.slice();
  const replacementSections = new Map<number, number>();
  const extraSections: number[] = [];
  const extraVectors = new Float32Array(records.reduce((n, record) => n + record.vectors.length, 0) * base.dims);
  const baseRows = base.textRows + base.sectionIds.length;

  for (const { patch, vectors } of records) {
    const existing = positions.get(patch.id);
    const previous = catalog.get(patch.id);
    const keepAliases = patch.op === 'put' && previous?.section === patch.entry.section;
    if (existing !== undefined && !keepAliases) {
      for (const row of entryRows[existing]) rowSection[row] = -1;
      entryRows[existing] = new Int32Array();
      replacementSections.set(existing, -1);
    }
    if (patch.op === 'remove') {
      catalog.delete(patch.id);
      delete depth[patch.id];
      continue;
    }
    const { section, title, answer, steps, sources } = patch.entry;
    const item: CatalogEntry = {
      id: patch.id, section, label: title, menu_label: title, kind: previous?.kind ?? 'faq',
      short: answer, steps, sources, last_verified: null,
    };
    catalog.set(item.id, item);
    depth[item.id] = depthFor(patch);
    const position = existing ?? ids.length;
    if (existing === undefined) ids.push(item.id);
    const sectionIndex = base.sectionIds.indexOf(section);
    replacementSections.set(position, sectionIndex);
    const firstRow = extraSections.length;
    for (const vector of vectors) {
      extraVectors.set(vector, extraSections.length * base.dims);
      extraSections.push(sectionIndex);
    }
    const originalRows = entryRows[position] ?? [];
    entryRows[position] = Int32Array.from([
      ...originalRows,
      ...vectors.map((_, i) => baseRows + firstRow + i),
    ]);
  }

  const sectionMembers = base.sectionMembers.map((members, section) => Int32Array.from([
    ...Array.from(members).filter((n) => !replacementSections.has(n)),
    ...Array.from(replacementSections).filter(([, target]) => target === section).map(([n]) => n),
  ]));
  const idx: LoadedIndex = {
    ...base, ids, entryRows, rowSection, sectionMembers,
    overlay: { vectors: extraVectors, sections: Int32Array.from(extraSections) },
  };
  return { idx, catalog, depth };
}

