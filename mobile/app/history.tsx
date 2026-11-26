import { FlashList } from '@shopify/flash-list';
import { useFocusEffect } from 'expo-router';
import { memo, useCallback } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { useHistory, type HistoryRow } from '@/state/history';
import { es } from '@/ui/strings';
import { useColors } from '@/ui/theme';
import { fontSize, spacing } from '@/ui/theme/tokens';

const Row = memo(function Row({ row }: { row: HistoryRow }) {
  const c = useColors();
  const title = (es as Record<string, string>)[row.kind] ?? row.kind;
  return (
    <View style={[styles.row, { borderColor: c.border }]}>
      <Text style={{ color: c.text, fontSize: fontSize.md }}>{title}</Text>
      <Text style={{ color: c.textMuted, fontSize: fontSize.sm }}>{new Date(row.at).toLocaleString('es')}</Text>
      <Text style={{ color: c.textMuted, fontSize: fontSize.sm }}>{row.args}</Text>
    </View>
  );
});

const renderItem = ({ item }: { item: HistoryRow }) => <Row row={item} />;
const keyExtractor = (r: HistoryRow) => String(r.id);

export default function HistoryScreen() {
  const c = useColors();
  const { rows, refresh } = useHistory();
  useFocusEffect(useCallback(() => refresh(), [refresh]));
  return (
    <View style={{ flex: 1, backgroundColor: c.background }}>
      <FlashList
        data={rows}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        ListEmptyComponent={<Text style={{ color: c.textMuted, padding: spacing.lg }}>{es.historyEmpty}</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  row: { padding: spacing.lg, borderBottomWidth: StyleSheet.hairlineWidth, gap: 2 },
});
