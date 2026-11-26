// UIOverlay layer: the cloud card with real text and buttons (React Native, not SVG) over the
// bottom of the scene. Everything follows the scene's progress value, so copy, dots and camera
// move together. Styling comes from the design tokens only.
import { memo } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { fill, t } from '@/i18n';
import { CloudCard } from '@/ui/CloudCard';
import { PageDots } from '@/ui/PageDots';
import { ParkEmblem } from '@/ui/ParkEmblem';
import { PET_NAME } from '@/ui/pet/petCore';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { brand, type } from '@/ui/theme/tokens';

import { cardBottomPadding, EMBLEM_SIZE, EMBLEM_TOP } from './layout';
import { uiStyleOf } from './scene/doc';
import type { SceneDoc } from './scene/types';
import { ONBOARDING_SCREENS } from './scene/types';

/** Distance the copy slides while it fades between screens. */
const COPY_SHIFT = 40;

export interface OnboardingOverlayProps {
  doc: SceneDoc;
  /** 0 = first screen, ONBOARDING_SCREENS - 1 = last; fractional while moving between screens. */
  progress: number;
  /** Screen width and card height (onboardingLayout). */
  width: number;
  cardHeight: number;
  onGo: (screen: number) => void;
  onDone: () => void;
}

// memo: the onboarding re-renders on every idle-motion frame; the card only changes with progress.
export const OnboardingOverlay = memo(function OnboardingOverlay({
  doc,
  progress,
  width,
  cardHeight,
  onGo,
  onDone,
}: OnboardingOverlayProps) {
  const insets = useSafeAreaInsets();
  if (!uiStyleOf(doc)) return null;
  const index = Math.min(ONBOARDING_SCREENS - 1, Math.max(0, Math.round(progress)));
  // -0.5..0.5 around the nearest screen: the copy fades out toward the midpoint and the next one
  // fades in from the other side.
  const offset = progress - index;
  const copy = t.onboarding.screens[index];
  const last = index === ONBOARDING_SCREENS - 1;
  return (
    <View pointerEvents="box-none" style={[styles.root, { height: cardHeight }]}>
      <CloudCard width={width} height={cardHeight}>
        <View
          style={[
            styles.column,
            {
              paddingTop: EMBLEM_TOP,
              paddingBottom: cardBottomPadding(insets.bottom),
              paddingLeft: insets.left + 28,
              paddingRight: insets.right + 28,
            },
          ]}
        >
          <View style={styles.mark}>
            <ParkEmblem size={EMBLEM_SIZE} />
          </View>
          <View
            style={[
              styles.copy,
              {
                opacity: 1 - Math.min(1, Math.abs(offset) * 2),
                transform: [{ translateX: -offset * COPY_SHIFT }],
              },
            ]}
          >
            <Text style={styles.title} accessibilityRole="header" numberOfLines={2}>
              {fill(copy.title, { pet: PET_NAME })}
            </Text>
            <Text style={styles.subtitle} numberOfLines={2}>
              {fill(copy.subtitle, { pet: PET_NAME })}
            </Text>
          </View>
          <PageDots count={ONBOARDING_SCREENS} position={progress} onSelect={onGo} />
          <View style={styles.action}>
            <PrimaryButton
              label={last ? t.onboarding.start : t.onboarding.next}
              onPress={() => (last ? onDone() : onGo(index + 1))}
            />
          </View>
        </View>
      </CloudCard>
    </View>
  );
});

const styles = StyleSheet.create({
  root: { position: 'absolute', left: 0, right: 0, bottom: 0 },
  // Tablets: keep the content phone-sized and centered instead of stretching across the screen.
  mark: { alignItems: 'center', height: EMBLEM_SIZE, justifyContent: 'center' },
  column: { flex: 1, width: '100%', maxWidth: 520, alignSelf: 'center', alignItems: 'stretch' },
  copy: { height: 64 + 6 + 44, marginTop: 12, marginBottom: 18, justifyContent: 'flex-start' },
  title: { ...type.display, color: brand.ink, textAlign: 'center' },
  subtitle: { ...type.body, color: brand.inkMuted, textAlign: 'center', marginTop: 6 },
  action: { marginTop: 20 },
});
