// Component workshop: one design-system component at a time, live, with its own controls. The
// app-design skill points here; each component gets a lab in src/design and a row in its registry.
import { Stack } from 'expo-router';
import { useState, type ComponentType } from 'react';
import { ScrollView, StyleSheet, Text, useWindowDimensions, View } from 'react-native';

import { BubblesLab } from '@/design/BubblesLab';
import { Toggle, WorkshopNav, type LabProps } from '@/design/chrome';
import { ComposerLab } from '@/design/ComposerLab';
import { ButtonsLab, IndicatorsLab } from '@/design/ControlsLabs';
import { FoundationsLab } from '@/design/FoundationsLab';
import { WORKSHOP_ITEMS, type WorkshopId } from '@/design/registry';
import { fill, t } from '@/i18n';
import { brand, spacing, type } from '@/ui/theme/tokens';
import { ReducedMotionOverride, useReducedMotion } from '@/ui/useReducedMotion';

const LABS: Record<WorkshopId, ComponentType<LabProps>> = {
  composer: ComposerLab,
  bubbles: BubblesLab,
  buttons: ButtonsLab,
  indicators: IndicatorsLab,
  foundations: FoundationsLab,
};

/** Nav column + canvas + controls side by side from this width; stacked below it. */
const WIDE = 1000;

export default function DesignScreen() {
  const { width } = useWindowDimensions();
  const wide = width >= WIDE;
  const [selected, setSelected] = useState<WorkshopId>('composer');
  const [reduceMotion, setReduceMotion] = useState(false);
  const reducedMotion = useReducedMotion() || reduceMotion;
  const item = WORKSHOP_ITEMS.find((i) => i.id === selected)!;
  const Lab = LABS[selected];
  const w = t.dev.workshop;

  return (
    <ScrollView
      style={styles.screen}
      contentContainerStyle={[styles.root, wide && styles.rootWide]}
    >
      {/* The page has its own header; the stack's would repeat the title. */}
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.header}>
        <View style={styles.titles}>
          <Text style={styles.h1} accessibilityRole="header">
            {w.title}
          </Text>
          <Text style={styles.position}>
            {fill(w.position, { n: item.index, name: item.label })}
          </Text>
        </View>
        <View style={styles.motion}>
          <Toggle label={w.reduceMotion} value={reduceMotion} onChange={setReduceMotion} />
        </View>
      </View>
      <View style={[styles.body, wide && styles.bodyWide]}>
        <WorkshopNav selected={selected} onSelect={setSelected} vertical={wide} />
        <View style={wide ? styles.labWide : undefined}>
          {/* Keyed so a lab's timers and demo state never leak into the next one. */}
          <ReducedMotionOverride.Provider value={reducedMotion}>
            <Lab key={selected} wide={wide} reducedMotion={reducedMotion} />
          </ReducedMotionOverride.Provider>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { backgroundColor: brand.card },
  root: { padding: spacing.lg, paddingTop: spacing.xl, gap: spacing.xl },
  rootWide: { padding: 40, maxWidth: 1440, width: '100%', alignSelf: 'center' },
  header: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.md,
  },
  titles: { gap: spacing.xs },
  h1: { ...type.display, color: brand.ink },
  position: { ...type.caption, color: brand.inkMuted, fontVariant: ['tabular-nums'] },
  motion: { minWidth: 200 },
  body: { gap: spacing.lg },
  bodyWide: { flexDirection: 'row', alignItems: 'flex-start', gap: 32 },
  labWide: { flex: 1, minWidth: 0 },
});
