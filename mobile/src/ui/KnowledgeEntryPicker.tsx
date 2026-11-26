import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import type { SectionInfo } from '@/core/knowledge/assets';
import { foldText } from '@/core/knowledge/safety';
import { t } from '@/i18n';

import { Icon } from './icons/Icon';
import { AdminButton, AdminField, AdminPanel, adminStyles as styles } from './KnowledgeAdminFields';
import { brand, radius, spacing, type } from './theme/tokens';

type Entry = { id: string; label: string; section?: string };
const PAGE_SIZE = 12;
const copy = t.knowledgeAdmin;

export function KnowledgeEntryPicker<Row extends Entry>({
  rows,
  sections,
  onPick,
  selected,
  limitReached,
}: {
  rows: readonly Row[];
  sections: readonly SectionInfo[];
  onPick: (item: Row) => void;
  selected?: readonly string[];
  limitReached?: boolean;
}) {
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const [pageSizes, setPageSizes] = useState<Record<string, number>>({});
  const query = foldText(search);
  const groups = useMemo(() => {
    const bySection = new Map(
      sections.map(({ id, title }) => [id, { id, title, items: [] as Row[] }]),
    );
    const other = { id: '', title: copy.otherSection, items: [] as Row[] };
    for (const item of rows) {
      if (query && !foldText(item.label).includes(query)) continue;
      (bySection.get(item.section ?? '') ?? other).items.push(item);
    }
    return [...bySection.values(), other].filter(({ items }) => items.length);
  }, [query, rows, sections]);

  return (
    <View style={styles.list}>
      <AdminField
        label={copy.search}
        value={search}
        onChangeText={(text) => {
          setSearch(text);
          setExpanded({});
          setPageSizes({});
        }}
      />
      {!groups.length && <Text style={styles.note}>{copy.noEntries}</Text>}
      {groups.map(({ id, title, items }) => {
        const open = expanded[id] ?? !!query;
        const page = pageSizes[id] ?? PAGE_SIZE;
        return (
          <AdminPanel key={id}>
            <Pressable
              accessibilityRole="button"
              accessibilityState={{ expanded: open }}
              style={sectionStyles.heading}
              onPress={() => setExpanded((previous) => ({ ...previous, [id]: !open }))}
            >
              <Text style={sectionStyles.title}>{title}</Text>
              <View style={open && sectionStyles.expanded}>
                <Icon name="chevronRight" size={18} color={brand.ink} />
              </View>
            </Pressable>
            {open && (
              <View style={styles.list}>
                {items.slice(0, page).map((item) => {
                  const checked = selected?.includes(item.id);
                  const disabled = !!limitReached && !checked;
                  return (
                    <Pressable
                      key={item.id}
                      accessibilityRole={selected ? 'checkbox' : 'button'}
                      accessibilityState={selected ? { checked, disabled } : undefined}
                      disabled={disabled}
                      style={[sectionStyles.item, disabled && sectionStyles.disabled]}
                      onPress={() => onPick(item)}
                    >
                      <Text style={sectionStyles.itemTitle}>{item.label}</Text>
                      {checked && <Icon name="check" size={18} color={brand.ink} />}
                    </Pressable>
                  );
                })}
                {items.length > page && (
                  <AdminButton
                    label={copy.moreEntries}
                    onPress={() =>
                      setPageSizes((previous) => ({ ...previous, [id]: page + PAGE_SIZE }))
                    }
                  />
                )}
              </View>
            )}
          </AdminPanel>
        );
      })}
    </View>
  );
}

const sectionStyles = StyleSheet.create({
  heading: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: spacing.md,
    minHeight: 36,
  },
  title: { ...type.label, color: brand.ink, flex: 1 },
  expanded: { transform: [{ rotate: '90deg' }] },
  item: {
    backgroundColor: brand.card,
    borderRadius: radius.md,
    minHeight: 44,
    padding: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  itemTitle: { ...type.body, color: brand.ink, flex: 1 },
  disabled: { opacity: 0.6 },
});
