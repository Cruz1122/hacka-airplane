// The options for one role's Pet, opened from the pencil on its role card: the accessories as
// small Pet heads wearing each one, then the color swatches (dimmed when the Pet wears nothing),
// and "Listo" closes the panel. The card above shows the result live. Every choice is a radio, at
// least 44 pt. The host owns the look.
import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { fill, t } from '@/i18n';
import { wornBy, type LookAccessory, type PetLook, type PetRole } from '@/state/petLook';

import { Icon } from './icons/Icon';
import {
  defaultTint,
  PET_ACCESSORIES,
  PET_NAME,
  PET_TINTS,
  tintColor,
  type PetTint,
} from './pet/petCore';
import { PetStill } from './pet/PetStill';
import { brand, spacing, type } from './theme/tokens';

// No "by your role" tile: until one is picked, the role's own hat shows as the selected tile.
const ACCESSORY_CHOICES: Exclude<LookAccessory, 'role'>[] = [...PET_ACCESSORIES, 'none'];
/** The head and hat of a Pet, in Pet units: what an accessory tile shows. */
const TILE_CROP = { x: -200, y: -200, width: 330, height: 330 };
const TILE = 56;
const SWATCH = 32;

export interface PetCustomizerProps {
  role: PetRole;
  look: PetLook;
  onChange: (patch: Partial<PetLook>) => void;
  onDone: () => void;
}

export function PetCustomizer({ role, look, onChange, onDone }: PetCustomizerProps) {
  const [focused, setFocused] = useState<string | null>(null);
  const p = t.group.pet;
  const worn = wornBy(look, role);
  const bare = worn.accessory === undefined;
  const current = worn.accessory ?? 'none';
  return (
    <View style={styles.card}>
      <View style={styles.headText}>
        <Text style={styles.title} accessibilityRole="header">
          {fill(p.title[role], { pet: PET_NAME })}
        </Text>
        <Text style={styles.caption}>{p.body}</Text>
      </View>

      <Text style={styles.label}>{p.accessory}</Text>
      <View style={styles.row} accessibilityRole="radiogroup" accessibilityLabel={p.accessory}>
        {ACCESSORY_CHOICES.map((choice) => {
          const on = current === choice;
          const shown = wornBy({ accessory: choice, tint: look.tint }, role);
          const key = `acc:${choice}`;
          return (
            <Pressable
              key={choice}
              onPress={() => onChange({ accessory: choice })}
              onFocus={() => setFocused(key)}
              onBlur={() => setFocused((f) => (f === key ? null : f))}
              accessibilityRole="radio"
              accessibilityLabel={p.accessories[choice]}
              accessibilityState={{ checked: on }}
              style={({ pressed }) => [
                styles.tile,
                on && styles.tileOn,
                focused === key && styles.focused,
                pressed && styles.pressed,
              ]}
            >
              <View style={styles.coin}>
                <PetStill
                  size={TILE}
                  emotion="happy"
                  accessory={shown.accessory}
                  tint={shown.tint}
                  crop={TILE_CROP}
                />
              </View>
            </Pressable>
          );
        })}
      </View>
      <Text style={styles.choice} accessibilityLiveRegion="polite">
        {p.accessories[current]}
      </Text>

      <Text style={styles.label}>{p.color}</Text>
      <View
        style={[styles.row, bare && styles.dimmed]}
        accessibilityRole="radiogroup"
        accessibilityLabel={p.color}
      >
        {([null, ...PET_TINTS] as (PetTint | null)[]).map((tint) => {
          const on = look.tint === tint;
          // "Original" shows the color the accessory wears by default.
          const swatch = tintColor(tint ?? (worn.accessory ? defaultTint(worn.accessory) : 'ink'));
          const name = p.tints[tint ?? 'auto'];
          const key = `tint:${tint ?? 'auto'}`;
          return (
            <Pressable
              key={tint ?? 'auto'}
              onPress={() => onChange({ tint })}
              onFocus={() => setFocused(key)}
              onBlur={() => setFocused((f) => (f === key ? null : f))}
              disabled={bare}
              accessibilityRole="radio"
              accessibilityLabel={name}
              accessibilityState={{ checked: on, disabled: bare }}
              hitSlop={6}
              style={({ pressed }) => [
                styles.swatchSlot,
                on && styles.swatchOn,
                focused === key && styles.focused,
                pressed && styles.pressed,
              ]}
            >
              <View style={[styles.swatch, { backgroundColor: swatch }]}>
                {tint === null && <View style={styles.autoDot} />}
              </View>
            </Pressable>
          );
        })}
      </View>
      <Text style={styles.choice} accessibilityLiveRegion="polite">
        {p.tints[look.tint ?? 'auto']}
      </Text>
      <Pressable
        onPress={onDone}
        onFocus={() => setFocused('done')}
        onBlur={() => setFocused((f) => (f === 'done' ? null : f))}
        accessibilityRole="button"
        accessibilityLabel={p.done}
        style={({ pressed }) => [
          styles.done,
          focused === 'done' && styles.focused,
          pressed && styles.pressed,
        ]}
      >
        <Icon name="check" size={18} color={brand.onPrimary} />
        <Text style={styles.doneText}>{p.done}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    gap: spacing.sm,
    padding: spacing.lg,
    borderRadius: 28,
    borderWidth: 2,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
  },
  done: {
    alignSelf: 'flex-end',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    minHeight: 44,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    borderRadius: 22,
    backgroundColor: brand.ink,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 3,
  },
  doneText: { ...type.label, color: brand.onPrimary },
  headText: { gap: spacing.xs },
  title: { ...type.title, color: brand.ink },
  caption: { ...type.caption, color: brand.inkMuted },
  label: { ...type.caption, color: brand.inkMuted, marginTop: spacing.xs },
  choice: { ...type.caption, color: brand.ink },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  tile: {
    padding: 3,
    borderRadius: 999,
    borderWidth: 3,
    borderColor: 'transparent',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  tileOn: { borderColor: brand.ink },
  coin: {
    width: TILE,
    height: TILE,
    borderRadius: TILE / 2,
    overflow: 'hidden',
    backgroundColor: brand.primary,
  },
  focused: { outlineWidth: 2 },
  pressed: { opacity: 0.75 },
  dimmed: { opacity: 0.4 },
  swatchSlot: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 3,
    borderColor: 'transparent',
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  swatchOn: { borderColor: brand.ink },
  swatch: {
    width: SWATCH,
    height: SWATCH,
    borderRadius: SWATCH / 2,
    borderWidth: 2,
    borderColor: brand.cardShade,
    alignItems: 'center',
    justifyContent: 'center',
  },
  autoDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: brand.card },
});
