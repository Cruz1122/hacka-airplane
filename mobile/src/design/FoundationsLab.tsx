// Workshop lab for the foundations: the Pet in any emotion, the brand colors, the Manrope type
// scale and the onboarding card with the park emblem.
import { useState } from 'react';
import { StyleSheet, Text, useWindowDimensions, View } from 'react-native';

import { t } from '@/i18n';
import { CLOUD_EDGE, CloudCard } from '@/ui/CloudCard';
import { PageDots } from '@/ui/PageDots';
import { ParkEmblem } from '@/ui/ParkEmblem';
import { Pet } from '@/ui/pet/Pet';
import {
  PET_ACCESSORIES,
  PET_EMOTIONS,
  PET_TINTS,
  type PetAccessory,
  type PetEmotion,
  type PetTint,
} from '@/ui/pet/petCore';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { brand, spacing, type } from '@/ui/theme/tokens';

import { Choices, Field, Stage, type LabProps } from './chrome';

const w = t.dev.workshop;

export function FoundationsLab({ wide, reducedMotion }: LabProps) {
  const [emotion, setEmotion] = useState<PetEmotion>('speaking');
  const [page, setPage] = useState(0);
  const [accessory, setAccessory] = useState<PetAccessory | 'none'>('none');
  const [tint, setTint] = useState<PetTint | 'auto'>('auto');
  const speaking = emotion === 'speaking';
  // The canvas and page padding take about 80 pt on a phone.
  const cardWidth = Math.min(360, useWindowDimensions().width - 80);

  const preview = (
    <>
      <View testID="pet-parity" style={styles.sky}>
        <Pet
          size={220}
          emotion={emotion}
          voice={speaking ? 'speaking' : 'idle'}
          audioLevel={speaking ? 0.39 : 0}
          reducedMotion={reducedMotion}
          accessory={accessory === 'none' ? undefined : accessory}
          tint={tint === 'auto' ? undefined : tint}
        />
      </View>

      <View style={styles.sheet}>
        <Text style={styles.heading}>{w.colors}</Text>
        <View style={styles.row}>
          {Object.entries(brand).map(([name, color]) => (
            <View key={name} style={styles.swatch}>
              <View style={[styles.chip, { backgroundColor: color }]} />
              <Text style={styles.caption}>{name}</Text>
            </View>
          ))}
        </View>
      </View>

      <View style={styles.sheet}>
        <Text style={styles.heading}>{w.typeScale}</Text>
        {Object.entries(type).map(([name, style]) => (
          <Text key={name} style={[style, { color: brand.ink }]}>
            {name} · Contigo, incluso sin señal
          </Text>
        ))}
      </View>

      <View style={[styles.sky, styles.cardSky]}>
        <CloudCard width={cardWidth} height={260}>
          <View style={[styles.cardBody, { paddingTop: CLOUD_EDGE + spacing.md }]}>
            <View style={styles.center}>
              <ParkEmblem />
            </View>
            <Text style={styles.cardTitle}>CloudCard</Text>
            <PageDots count={3} position={page} onSelect={setPage} />
            <PrimaryButton label="PrimaryButton" onPress={() => setPage((page + 1) % 3)} />
          </View>
        </CloudCard>
      </View>
    </>
  );

  const controls = (
    <>
      <Field label={`${w.pet} · ${w.emotion}`}>
        <Choices
          value={emotion}
          onChange={setEmotion}
          options={PET_EMOTIONS.map((e) => ({ value: e, label: e }))}
        />
      </Field>
      <Field label={`${w.pet} · ${w.accessory}`}>
        <Choices
          value={accessory}
          onChange={setAccessory}
          options={(['none', ...PET_ACCESSORIES] as const).map((a) => ({ value: a, label: a }))}
        />
      </Field>
      <Field label={`${w.pet} · ${t.group.pet.color}`}>
        <Choices
          value={tint}
          onChange={setTint}
          options={(['auto', ...PET_TINTS] as const).map((v) => ({ value: v, label: v }))}
        />
      </Field>
    </>
  );

  return <Stage wide={wide} preview={preview} controls={controls} />;
}

const styles = StyleSheet.create({
  sky: {
    width: '100%',
    maxWidth: 420,
    backgroundColor: brand.sky,
    borderRadius: 28,
    alignItems: 'center',
    paddingTop: spacing.xl,
    overflow: 'hidden',
  },
  cardSky: { paddingTop: 40 },
  sheet: {
    width: '100%',
    maxWidth: 420,
    gap: spacing.md,
    padding: spacing.xl,
    borderRadius: 28,
    backgroundColor: brand.card,
  },
  heading: { ...type.label, color: brand.ink },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  swatch: { alignItems: 'center', width: 84, gap: spacing.xs },
  chip: { width: 48, height: 48, borderRadius: 24, borderWidth: 1, borderColor: brand.cardShade },
  caption: { ...type.caption, color: brand.inkMuted },
  cardBody: { flex: 1, paddingHorizontal: spacing.xl, gap: spacing.md, alignItems: 'stretch' },
  cardTitle: { ...type.title, color: brand.ink, textAlign: 'center' },
  center: { alignItems: 'center' },
});
