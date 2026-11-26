import { setStringAsync } from 'expo-clipboard';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Text, View } from 'react-native';

import {
  draftFromCatalog,
  draftFromEntry,
  prepareDraft,
  emptyDraft,
  entryFromDraft,
  type Draft,
  type ListField,
} from '@/core/knowledge/adminDraft';
import { checkPatch } from '@/core/knowledge/qrIndex';
import {
  collectKnowledgeQr,
  encodeKnowledgeQrSeries,
  QR_LIMIT,
  QR_RELATED_LIMIT,
  validateKnowledgePatch,
  type KnowledgePatch,
} from '@/core/knowledge/qrPatch';
import { fill, t } from '@/i18n';
import { knowledgeAssets } from '@/llm/knowledgeAssets';
import { readAdminCatalog, type AdminEntry } from '@/state/knowledgeAdminCatalog';
import { applyKnowledgePatch } from '@/state/useKnowledge';

import { AdminButton, AdminField, AdminPanel, adminStyles as styles } from './KnowledgeAdminFields';
import { KnowledgeEntryPicker } from './KnowledgeEntryPicker';
import { KnowledgeQr } from './KnowledgeQr';

const labels = t.knowledgeAdmin;
const sections = knowledgeAssets.sections
  .filter(
    (section) =>
      section.id !== 'health_safety' && knowledgeAssets.manifest.section_rows.includes(section.id),
  )
  .sort((first, second) => first.order - second.order);
const initialSection = sections.find((section) => section.id === 'geography')?.id ?? sections[0].id;
const extras = [
  'variants',
  'more',
  'why',
  'steps',
  'sources',
] as const satisfies readonly ListField[];
const bundledTitles = new Map(
  knowledgeAssets.catalog.map(({ id, menu_label, label }) => [id, menu_label || label]),
);

type ViewMode = 'catalog' | 'edit' | 'remove' | 'result';
type Publication = { codes: string[]; count: number };
const message = (cause: unknown) => (cause instanceof Error ? cause.message : labels.error);

export function KnowledgeManager({ goTop }: { goTop: () => void }) {
  const [mode, setMode] = useState<ViewMode>('catalog');
  const [catalog, setCatalog] = useState<AdminEntry[]>([]);
  const [removed, setRemoved] = useState(false);
  const [draft, setDraft] = useState<Draft>(() => emptyDraft(initialSection));
  const [selected, setSelected] = useState<AdminEntry>();
  const [showSections, setShowSections] = useState(false);
  const [advanced, setAdvanced] = useState(false);
  const [relatedOpen, setRelatedOpen] = useState(false);
  const [importing, setImporting] = useState(false);
  const [raw, setRaw] = useState('');
  const [publication, setPublication] = useState<Publication>();
  const [page, setPage] = useState(0);
  const saveLock = useRef(false);
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const latest = useRef(0);

  useEffect(() => {
    let active = true;
    void readAdminCatalog()
      .then((rows) => {
        if (active) setCatalog(rows);
      })
      .catch((cause) => {
        if (active) setError(message(cause));
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(goTop, [goTop, mode]);

  const visible = useMemo(
    () => catalog.filter((row) => (row.patch?.op === 'remove') === removed),
    [catalog, removed],
  );
  const relatedOptions = useMemo(
    () => catalog.filter((row) => row.id !== draft.id && row.patch?.op !== 'remove'),
    [catalog, draft.id],
  );
  const titles = useMemo(() => new Map(catalog.map(({ id, label }) => [id, label])), [catalog]);
  const saved = useMemo(() => catalog.flatMap(({ patch }) => patch ? [patch] : []), [catalog]);

  function toggleRelated(id: string) {
    setDraft((previous) => {
      const related = previous.related.includes(id)
        ? previous.related.filter((item) => item !== id)
        : previous.related.length < QR_RELATED_LIMIT
          ? [...previous.related, id]
          : previous.related;
      return { ...previous, related };
    });
    setError('');
  }

  function field(key: keyof Draft, value: string) {
    setDraft((previous) => ({ ...previous, [key]: value }));
    setError('');
  }

  function openEdit(row?: AdminEntry) {
    setSelected(row);
    setDraft(
      row?.patch?.op === 'put'
        ? draftFromEntry(row.id, row.patch.entry)
        : row?.original
          ? draftFromCatalog(row.original, knowledgeAssets.depth?.entries[row.id])
          : emptyDraft(initialSection, row?.id),
    );
    setAdvanced(false);
    setRelatedOpen(false);
    setShowSections(false);
    setError('');
    setStatus('');
    setMode('edit');
  }

  function share(patches: readonly KnowledgePatch[]) {
    try {
      const codes = encodeKnowledgeQrSeries(patches);
      setPublication({ codes, count: patches.length });
      setPage(0);
      setError('');
      setStatus('');
      setMode('result');
    } catch (cause) {
      setError(message(cause));
    }
  }

  async function save(op: 'put' | 'remove') {
    if (saveLock.current) return;
    saveLock.current = true;
    setSaving(true);
    setError('');
    setStatus('');
    try {
      const prepared = op === 'put' ? prepareDraft({ ...draft, id: selected ? draft.id : '' }) : draft;
      const id = prepared.id.trim();
      const previous = catalog.find((row) => row.id === id);
      if (op === 'put' && previous && !selected) throw new Error(labels.exists);
      const revision = Math.max(Date.now(), latest.current + 1, (previous?.patch?.revision ?? 0) + 1);
      const patch = validateKnowledgePatch(op === 'remove' ? { id, revision, op } : {
        id, revision, op, entry: entryFromDraft(prepared, labels.sourceError),
      });
      checkPatch(knowledgeAssets, patch);
      await applyKnowledgePatch(patch);
      latest.current = revision;
      setCatalog(await readAdminCatalog());
      setMode('catalog');
      setStatus(labels.saved);
    } catch (cause) {
      setError(message(cause));
    } finally {
      saveLock.current = false;
      setSaving(false);
    }
  }

  function openCode() {
    try {
      const result = collectKnowledgeQr(raw.trim());
      if ('series' in result || result.patches.length !== 1) {
        throw new Error(labels.importSeries);
      }
      const [patch] = result.patches;
      checkPatch(knowledgeAssets, patch);
      latest.current = Math.max(latest.current, patch.revision);
      const importedTitle = patch.op === 'put' ? patch.entry.title : labels.retiredTitle;
      const row = catalog.find(({ id }) => id === patch.id) ?? {
        id: patch.id,
        label: importedTitle,
      };
      openEdit(row);
      if (patch.op === 'put') setDraft(draftFromEntry(patch.id, patch.entry));
      else setMode('remove');
      setImporting(false);
      setRaw('');
    } catch (cause) {
      setError(message(cause));
    }
  }

  async function copyCode() {
    if (!publication) return;
    try {
      if (!(await setStringAsync(publication.codes[page]))) throw new Error(labels.copyError);
      setError('');
      setStatus(labels.copied);
    } catch {
      setError(labels.copyError);
    }
  }

  function backToCatalog() {
    setError('');
    setMode('catalog');
  }

  const sectionLabel =
    sections.find(({ id }) => draft.section === id)?.title ?? labels.otherSection;
  const saveLabel = saving ? labels.saving : labels.save;
  const removeLabel = saving ? labels.saving : labels.saveRemove;
  const switchLabel = removed ? labels.showActive : labels.showRemoved;
  const canRemove = !!selected && selected.patch?.op !== 'remove';
  const heading =
    selected?.patch?.op === 'remove' ? labels.restore : selected ? labels.edit : labels.newEntry;
  const extraLabel = advanced ? labels.less : labels.extra;
  const picker = selected?.patch;
  const relatedLimit = draft.related.length >= QR_RELATED_LIMIT;
  const relatedAction = relatedOpen ? labels.hideRelated : labels.chooseRelated;

  return (
    <>
      {!!status && (
        <Text accessibilityLiveRegion="polite" style={styles.body}>
          {status}
        </Text>
      )}
      {mode === 'catalog' && (
        <>
          <View style={styles.row}>
            <AdminButton label={labels.newEntry} primary onPress={() => openEdit()} />
            <AdminButton label={labels.shareSaved} disabled={!saved.length} onPress={() => share(saved)} />
            <AdminButton
              label={labels.importCode}
              onPress={() => {
                setImporting(!importing);
                setError('');
              }}
            />
            <AdminButton
              label={switchLabel}
              onPress={() => {
                setRemoved(!removed);
              }}
            />
          </View>
          {importing && (
            <AdminPanel>
              <Text style={styles.note}>{labels.changeImport}</Text>
              <AdminField
                multiline
                label={labels.paste}
                autoCapitalize="none"
                autoCorrect={false}
                value={raw}
                maxLength={QR_LIMIT}
                onChangeText={setRaw}
              />
              <AdminButton label={labels.read} disabled={!raw.trim()} onPress={openCode} />
            </AdminPanel>
          )}
          <KnowledgeEntryPicker rows={visible} sections={sections} onPick={openEdit} />
          <Text style={styles.note}>{labels.safety}</Text>
        </>
      )}
      {mode === 'edit' && (
        <>
          <AdminButton label={labels.catalog} disabled={saving} onPress={backToCatalog} />
          <Text accessibilityRole="header" style={styles.title}>
            {heading}
          </Text>
          <AdminPanel>
            <Text style={styles.title}>{labels.section}</Text>
            <Text style={styles.body}>{sectionLabel}</Text>
            <AdminButton
              label={labels.changeSection}
              onPress={() => setShowSections(!showSections)}
            />
            {showSections && (
              <View style={styles.row}>
                {sections.map((section) => (
                  <AdminButton
                    key={section.id}
                    label={section.title}
                    onPress={() => {
                      field('section', section.id);
                      setShowSections(false);
                    }}
                  />
                ))}
              </View>
            )}
            <AdminField
              label={labels.title}
              editable={!saving}
              value={draft.title}
              onChangeText={(text) => field('title', text)}
            />
            <AdminField
              multiline
              label={labels.answer}
              editable={!saving}
              value={draft.answer}
              onChangeText={(text) => field('answer', text)}
            />
            {!!draft.variants.trim() && <Text style={styles.note}>{labels.reviewVariants}</Text>}
            <AdminField
              multiline
              label={labels.questions}
              editable={!saving}
              value={draft.questions}
              onChangeText={(text) => field('questions', text)}
            />
            <AdminButton label={extraLabel} onPress={() => setAdvanced(!advanced)} />
            {advanced &&
              extras.map((key) => (
                <AdminField
                  key={key}
                  multiline
                  label={labels[key]}
                  editable={!saving}
                  value={draft[key]}
                  onChangeText={(text) => field(key, text)}
                />
              ))}
            {advanced && (
              <View style={styles.list}>
                <Text style={styles.title}>{labels.related}</Text>
                {draft.related.map((id, index) => {
                  const title =
                    titles.get(id) ??
                    bundledTitles.get(id) ??
                    fill(labels.unknownRelated, { number: index + 1 });
                  return (
                    <AdminButton
                      key={id}
                      label={fill(labels.unlinkRelated, { title })}
                      onPress={() => toggleRelated(id)}
                    />
                  );
                })}
                <AdminButton label={relatedAction} onPress={() => setRelatedOpen(!relatedOpen)} />
                {relatedLimit && (
                  <Text style={styles.note}>
                    {fill(labels.relatedLimit, { max: QR_RELATED_LIMIT })}
                  </Text>
                )}
                {relatedOpen && (
                  <KnowledgeEntryPicker
                    rows={relatedOptions}
                    sections={sections}
                    onPick={({ id }) => toggleRelated(id)}
                    selected={draft.related}
                    limitReached={relatedLimit}
                  />
                )}
              </View>
            )}
          </AdminPanel>
          <AdminButton primary label={saveLabel} disabled={saving} onPress={() => void save('put')} />
          {canRemove && (
            <AdminButton
              label={labels.remove}
              disabled={saving}
              onPress={() => {
                setError('');
                setMode('remove');
              }}
            />
          )}
          {picker && <AdminButton label={labels.shareEntry} disabled={saving} onPress={() => share([picker])} />}
        </>
      )}
      {mode === 'remove' && (
        <AdminPanel>
          <Text style={styles.title}>{labels.removeHeading}</Text>
          <Text style={styles.body}>{selected?.label ?? labels.retiredTitle}</Text>
          <Text style={styles.note}>{labels.removeBody}</Text>
          <AdminButton primary label={removeLabel} disabled={saving} onPress={() => void save('remove')} />
          <AdminButton label={t.qrUpdate.cancel} disabled={saving} onPress={backToCatalog} />
        </AdminPanel>
      )}
      {mode === 'result' && publication && (
        <AdminPanel>
          <Text accessibilityRole="header" style={styles.title}>
            {labels.result}
          </Text>
          <Text style={styles.body}>{fill(labels.shareCount, { count: publication.count })}</Text>
          <KnowledgeQr code={publication.codes[page]} />
          <Text style={styles.note}>{labels.shareHint}</Text>
          {publication.codes.length > 1 && (
            <>
              <Text style={styles.body}>
                {fill(labels.qrPage, { page: page + 1, total: publication.codes.length })}
              </Text>
              <View style={styles.row}>
                <AdminButton label={labels.previousQr} disabled={page === 0}
                  onPress={() => { setPage(page - 1); setStatus(''); }} />
                <AdminButton label={labels.nextQr} disabled={page === publication.codes.length - 1}
                  onPress={() => { setPage(page + 1); setStatus(''); }} />
              </View>
            </>
          )}
          <AdminButton label={labels.copy} onPress={() => void copyCode()} />
          <AdminField label={t.qrUpdate.code} multiline editable={false} value={publication.codes[page]} />
          <AdminButton label={labels.catalog} onPress={backToCatalog} />
        </AdminPanel>
      )}
      {!!error && (
        <Text accessibilityLiveRegion="polite" style={[styles.body, styles.error]}>
          {error}
        </Text>
      )}
    </>
  );
}
