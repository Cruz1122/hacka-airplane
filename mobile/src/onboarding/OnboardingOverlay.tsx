// UIOverlay layer: the cloud card with real text and buttons (React Native, not SVG) over the
// bottom of the scene. Everything follows the scene's progress value, so copy, dots and camera
// move together. Styling comes from the design tokens only.
import { memo, useMemo } from 'react';
import { Animated, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { fill, t } from '@/i18n';
import { CloudCard } from '@/ui/CloudCard';
import { PageDots, usePagePosition, type PagePosition } from '@/ui/PageDots';
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

/**
 * Motion of screen `k`'s copy: fully shown on its screen, faded out half a screen away while it
 * slides COPY_SHIFT / 2 to that side. Each screen has its own block, so no text swaps mid-motion.
 */
export function copyMotion(value: Animated.Value, k: number) {
  const range = [k - 0.5, k, k + 0.5];
  return {
    opacity: value.interpolate({ inputRange: range, outputRange: [0, 1, 0], extrapolate: 'clamp' }),
    transform: [
      {
        translateX: value.interpolate({
          inputRange: range,
          outputRange: [COPY_SHIFT / 2, 0, -COPY_SHIFT / 2],
          extrapolate: 'clamp',
        }),
      },
    ],
  };
}

export interface OnboardingOverlayProps {
  doc: SceneDoc;
  /**
   * 0 = first screen, ONBOARDING_SCREENS - 1 = last; fractional while moving between screens. A
   * PagePosition animates the copy and dots without re-rendering the overlay on each frame.
   */
  progress: number | PagePosition;
  /** Screen width and card height (onboardingLayout). */
  width: number;
  cardHeight: number;
  onGo: (screen: number) => void;
  onDone: () => void;
}

// memo: with a PagePosition the overlay renders only when the screen it rounds to changes.
export const OnboardingOverlay = memo(function OnboardingOverlay({
  doc,
  progress,
  width,
  cardHeight,
  onGo,
  onDone,
}: OnboardingOverlayProps) {
  const insets = useSafeAreaInsets();
  const position = usePagePosition(progress);
  // Built once per value: the page-swap render mid-move must not rebuild the native nodes.
  const motions = useMemo(
    () => t.onboarding.screens.map((_, k) => copyMotion(position.value, k)),
    [position.value],
  );
  if (!uiStyleOf(doc)) return null;
  const index = Math.min(ONBOARDING_SCREENS - 1, Math.max(0, position.index));
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
          <View style={styles.copy}>
            {t.onboarding.screens.map((copy, k) => (
              <Animated.View key={k} style={[styles.page, motions[k]]} aria-hidden={k !== index}>
                <Text style={styles.title} accessibilityRole="header" numberOfLines={2}>
                  {fill(copy.title, { pet: PET_NAME })}
                </Text>
                <Text style={styles.subtitle} numberOfLines={2}>
                  {fill(copy.subtitle, { pet: PET_NAME })}
                </Text>
              </Animated.View>
            ))}
          </View>
          <PageDots count={ONBOARDING_SCREENS} position={position} onSelect={onGo} />
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
  copy: { height: 64 + 6 + 44, marginTop: 12, marginBottom: 18 },
  // Screens' copy blocks stack in the copy box; the one off its screen is transparent.
  page: { position: 'absolute', top: 0, left: 0, right: 0 },
  title: { ...type.display, color: brand.ink, textAlign: 'center' },
  subtitle: { ...type.body, color: brand.inkMuted, textAlign: 'center', marginTop: 6 },
  action: { marginTop: 20 },
});
