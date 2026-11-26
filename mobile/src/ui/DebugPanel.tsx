import { memo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import type { StepResult } from '@/core/driver';
import { t } from '@/i18n';

import { useColors } from './theme';
import { fontSize, spacing } from './theme/tokens';

export const DebugPanel = memo(function DebugPanel({ steps, state }: { steps: StepResult[]; state: string }) {
  const c = useColors();
  const [open, setOpen] = useState(false);
  return (
    <View style={{ borderTopWidth: StyleSheet.hairlineWidth, borderColor: c.border, backgroundColor: c.surface }}>
      <Pressable onPress={() => setOpen((o) => !o)} style={styles.head}>
        <Text style={{ color: c.textMuted, fontSize: fontSize.sm }}>
          {open ? '▾' : '▸'} {t.debug} · {t.state}: {state}
        </Text>
      </Pressable>
      {open && (
        <View style={styles.body}>
          {steps.length === 0 && <Text style={{ color: c.textMuted }}>{t.noSteps}</Text>}
          {steps.map((s, i) => {
            const x = s as unknown as {
              kind: string;
              call_type?: string | null;
              path: string[];
              completion?: { total_ms?: number | null; prompt_n?: number | null; predicted_n?: number | null } | null;
            };
            const ms = x.completion?.total_ms;
            const tok = (x.completion?.prompt_n ?? 0) + (x.completion?.predicted_n ?? 0);
            return (
              <Text key={i} style={{ color: c.text, fontSize: fontSize.sm, fontFamily: 'monospace' }}>
                {x.call_type ?? x.kind} {x.path.join('>')}
                {ms != null ? ` ${Math.round(ms)}${t.ms}` : ''}
                {x.completion ? ` ${tok}${t.tokens}` : ''}
              </Text>
            );
          })}
        </View>
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  head: { padding: spacing.sm, paddingHorizontal: spacing.lg },
  body: { paddingHorizontal: spacing.lg, paddingBottom: spacing.sm, gap: 2 },
});
