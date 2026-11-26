// Workshop labs for buttons and indicators: the real components, each control wired so a press
// shows what happened.
import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { fill, t } from '@/i18n';
import { AccessibilitySheet } from '@/ui/AccessibilitySheet';
import { Chip } from '@/ui/Chip';
import { CloudNavBar, NAV_BAR_HEIGHT, type NavTab } from '@/ui/CloudNavBar';
import { UserAvatar } from '@/ui/chat/Avatars';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { PageDots } from '@/ui/PageDots';
import { PET_NAME } from '@/ui/pet/petCore';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { SettingsSheet } from '@/ui/SettingsSheet';
import { brand, spacing, type } from '@/ui/theme/tokens';

import { ActionButton, Choices, Field, Stage, Status, Toggle, type LabProps } from './chrome';

const w = t.dev.workshop;

export function ButtonsLab({ wide }: LabProps) {
  const [chevron, setChevron] = useState(true);
  const [mode, setMode] = useState<'extractive' | 'generate'>('extractive');
  const [last, setLast] = useState<{ name: string; count: number } | null>(null);
  const [tab, setTab] = useState<NavTab>('chat');
  const [navWidth, setNavWidth] = useState(0);
  const [openSheet, setOpenSheet] = useState<'accessibility' | 'settings' | null>(null);
  const hit = (name: string) =>
    setLast((l) => ({ name, count: l?.name === name ? l.count + 1 : 1 }));

  const preview = (
    <View style={styles.sheet}>
      <Text style={styles.specimen}>PrimaryButton</Text>
      <PrimaryButton
        label={chevron ? t.onboarding.next : t.onboarding.start}
        chevron={chevron}
        onPress={() => hit('PrimaryButton')}
      />
      <Text style={styles.specimen}>Chip</Text>
      <View style={styles.row}>
        {(['extractive', 'generate'] as const).map((m) => (
          <Chip
            key={m}
            label={t[m]}
            selected={mode === m}
            onPress={() => {
              setMode(m);
              hit(`Chip · ${t[m]}`);
            }}
          />
        ))}
      </View>
      <Text style={styles.specimen}>CloudNavBar</Text>
      {/* CloudNavBar places itself absolutely over a screen; this box is that screen's top. */}
      <View style={styles.navBox} onLayout={(e) => setNavWidth(e.nativeEvent.layout.width)}>
        {navWidth > 0 && (
          <CloudNavBar
            active={tab}
            top={spacing.md}
            screenWidth={navWidth}
            activeSide={openSheet}
            onSelect={(next) => {
              setTab(next);
              hit(`CloudNavBar · ${t.nav[next]}`);
            }}
            onAccessibility={() => {
              setOpenSheet((prev) => (prev === 'accessibility' ? null : 'accessibility'));
              hit(`CloudNavBar · ${t.nav.accessibility}`);
            }}
            onSettings={() => {
              setOpenSheet((prev) => (prev === 'settings' ? null : 'settings'));
              hit(`CloudNavBar · ${t.nav.settings}`);
            }}
          />
        )}
      </View>
    </View>
  );

  const controls = (
    <>
      <Toggle label="chevron" value={chevron} onChange={setChevron} />
      <View style={styles.row}>
        <ActionButton
          icon="accessibility"
          label={t.nav.accessibility}
          onPress={() => setOpenSheet('accessibility')}
        />
        <ActionButton
          icon="settings"
          label={t.nav.settings}
          onPress={() => setOpenSheet('settings')}
        />
      </View>
      <Status>{last ? fill(w.pressed, last) : w.notPressed}</Status>
    </>
  );
  return (
    <>
      <Stage wide={wide} preview={preview} controls={controls} />
      <AccessibilitySheet open={openSheet === 'accessibility'} onClose={() => setOpenSheet(null)} />
      <SettingsSheet open={openSheet === 'settings'} onClose={() => setOpenSheet(null)} />
    </>
  );
}

export function IndicatorsLab({ wide }: LabProps) {
  const [count, setCount] = useState<'3' | '4' | '5'>('3');
  const [page, setPage] = useState(0);
  const total = Number(count);
  const go = (to: number) => setPage(Math.min(total - 1, Math.max(0, to)));

  const preview = (
    <View style={styles.sheet}>
      <Text style={styles.specimen}>PageDots</Text>
      <PageDots count={total} position={page} onSelect={go} />
      <Status>{fill(w.step, { n: page + 1, total })}</Status>
      <Text style={styles.specimen}>TypingBubble</Text>
      <TypingBubble label={fill(t.chatScreen.typing, { pet: PET_NAME })} />
      <Text style={styles.specimen}>UserAvatar</Text>
      <View style={styles.row}>
        {[28, 36, 48].map((size) => (
          <UserAvatar key={size} size={size} />
        ))}
      </View>
    </View>
  );

  const controls = (
    <>
      <Field label="count">
        <Choices
          value={count}
          onChange={(c) => {
            setCount(c);
            setPage((p) => Math.min(p, Number(c) - 1));
          }}
          options={(['3', '4', '5'] as const).map((c) => ({ value: c, label: c }))}
        />
      </Field>
      <View style={styles.row}>
        <ActionButton icon="chevronLeft" label={w.previous} onPress={() => go(page - 1)} />
        <ActionButton icon="chevronRight" label={w.next} onPress={() => go(page + 1)} />
      </View>
    </>
  );
  return <Stage wide={wide} preview={preview} controls={controls} />;
}

const styles = StyleSheet.create({
  sheet: {
    width: '100%',
    maxWidth: 420,
    gap: spacing.md,
    padding: spacing.xl,
    borderRadius: 28,
    backgroundColor: brand.card,
  },
  specimen: { ...type.caption, color: brand.inkMuted, marginTop: spacing.sm },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, alignItems: 'center' },
  navBox: {
    height: NAV_BAR_HEIGHT + 2 * spacing.md,
    borderRadius: 20,
    backgroundColor: brand.sky,
    overflow: 'hidden',
  },
});
