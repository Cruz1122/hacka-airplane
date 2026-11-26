// A stop's card, opened from its circle on the map: the place's name and what makes it special, its
// animal with a real photo, and the way into the full station page.
// One sheet per screen, like the chat's SourcesSheet, whose scrim, motion and Android back it follows.
import { useCallback, useEffect, useState } from 'react';
import {
  Animated,
  BackHandler,
  Easing,
  Image,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { t } from '@/i18n';
import { Icon } from '@/ui/icons/Icon';
import { PHOTO_CREDIT_INSET, PhotoCredit } from '@/ui/PhotoCredit';
import { brand, radius, spacing, type } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';
import { useReducedMotion } from '@/ui/useReducedMotion';

import type { StationId } from './stations';
import { type SpeciesPhoto, speciesPhoto } from './trailPhotos';

/** The square photo on the sheet's right. */
const PHOTO_W = 132;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';

/** The sheet for `id`, or nothing when it is null. */
export function StationSheet({
  id,
  onClose,
  onMore,
  bottom = 0,
}: {
  id: StationId | null;
  onClose: () => void;
  /** Opens the station's full page. */
  onMore: (id: StationId) => void;
  /** Bottom safe-area inset. */
  bottom?: number;
}) {
  return id ? (
    <OpenSheet key={id} id={id} onClose={onClose} onMore={onMore} bottom={bottom} />
  ) : null;
}

function OpenSheet({
  id,
  onClose,
  onMore,
  bottom,
}: {
  id: StationId;
  onClose: () => void;
  onMore: (id: StationId) => void;
  bottom: number;
}) {
  const { palette, scaled } = useAccessibilityTheme();
  const reduced = useReducedMotion();
  const [shown] = useState(() => new Animated.Value(reduced ? 1 : 0));
  const [closing, setClosing] = useState(false);
  useEffect(() => {
    if (reduced) return;
    const anim = Animated.timing(shown, {
      toValue: 1,
      duration: 260,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [reduced, shown]);
  const close = useCallback(() => {
    if (reduced) return onClose();
    setClosing(true);
    Animated.timing(shown, {
      toValue: 0,
      duration: 200,
      easing: Easing.in(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start(({ finished }) => finished && onClose());
  }, [onClose, reduced, shown]);
  // Android's back button closes the sheet before it leaves the screen (web has no back button).
  useEffect(() => {
    if (Platform.OS !== 'android') return;
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      close();
      return true;
    });
    return () => sub.remove();
  }, [close]);

  const photo = speciesPhoto(id);
  const mark = t.trail.marks[id];
  return (
    <View
      style={[StyleSheet.absoluteFill, styles.overlay]}
      pointerEvents={closing ? 'none' : 'auto'}
    >
      <Animated.View
        style={[
          StyleSheet.absoluteFill,
          {
            backgroundColor: palette.ink,
            opacity: shown.interpolate({ inputRange: [0, 1], outputRange: [0, 0.32] }),
          },
        ]}
      >
        {/* Tapping outside closes too; screen readers get the labelled close button instead. */}
        <Pressable style={StyleSheet.absoluteFill} onPress={close} accessible={false} />
      </Animated.View>
      <Animated.View
        accessibilityViewIsModal
        style={[
          styles.sheet,
          {
            paddingBottom: bottom + spacing.lg,
            backgroundColor: palette.card,
            opacity: shown,
            transform: [
              { translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [24, 0] }) },
            ],
          },
        ]}
      >
        <View style={[styles.handle, { backgroundColor: palette.primarySoft }]} aria-hidden />
        <View style={styles.header}>
          <Text
            style={[styles.title, scaled.title, { color: palette.ink }]}
            accessibilityRole="header"
          >
            {t.trail.stations[id].name}
          </Text>
          <Pressable
            onPress={close}
            accessibilityRole="button"
            accessibilityLabel={t.trail.sheet.close}
            style={({ pressed }) => [
              styles.close,
              pressed && { backgroundColor: palette.cardShade },
            ]}
          >
            <Icon name="x" size={20} color={palette.ink} />
          </Pressable>
        </View>
        <Text style={[styles.place, scaled.body, { color: palette.inkMuted }]}>
          {t.trail.sheet.blurbs[id]}
        </Text>
        <View style={styles.body}>
          <View style={styles.text}>
            <Text style={[styles.mark, { color: palette.primary }]}>{mark}</Text>
            <Text style={[styles.blurb, scaled.body, { color: palette.inkMuted }]}>
              {t.trail.sheet.species[id]}
            </Text>
          </View>
          <View style={[styles.photo, { backgroundColor: palette.cardShade }]}>
            <Image
              source={photo.source}
              style={squareCrop(photo)}
              resizeMode="cover"
              accessible
              accessibilityRole="image"
              accessibilityLabel={mark}
            />
            <View style={styles.credit} pointerEvents="box-none">
              <PhotoCredit
                author={photo.author}
                license={photo.license}
                url={photo.url}
                maxWidth={PHOTO_W - PHOTO_CREDIT_INSET * 2}
              />
            </View>
          </View>
        </View>
        <MoreButton label={t.trail.sheet.more} onPress={() => onMore(id)} />
      </Animated.View>
    </View>
  );
}

/** The photo scaled to cover the square `zoom` times over, its `crop` point slid to the centre. */
function squareCrop({ aspect, crop }: SpeciesPhoto) {
  const width = PHOTO_W * crop.zoom;
  const height = width * aspect;
  const centre = (at: number, size: number) =>
    Math.min(0, Math.max(PHOTO_W - size, PHOTO_W / 2 - at * size));
  return {
    position: 'absolute' as const,
    left: centre(crop.x, width),
    top: centre(crop.y, height),
    width,
    height,
  };
}

/** Opens the station page: a teal (`primary`) button with an open book, as the guide's reading. */
function MoreButton({ label, onPress }: { label: string; onPress: () => void }) {
  const { palette, scaled } = useAccessibilityTheme();
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      onPress={onPress}
      style={({ pressed }) => [
        styles.more,
        { backgroundColor: pressed ? palette.ink : palette.primary },
      ]}
    >
      <Icon name="bookOpen" size={20} color={palette.onPrimary} />
      <Text style={[styles.moreLabel, scaled.label, { color: palette.onPrimary }]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  overlay: { justifyContent: 'flex-end', alignItems: 'center' },
  sheet: {
    width: '100%',
    maxWidth: 560,
    paddingTop: spacing.sm,
    paddingHorizontal: spacing.xl,
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    backgroundColor: brand.card,
  },
  handle: {
    width: 36,
    height: 4,
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: spacing.sm,
    backgroundColor: brand.primarySoft,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginRight: -spacing.md,
    marginBottom: spacing.md,
  },
  title: { ...type.title, flex: 1, color: brand.ink },
  close: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  place: { ...type.body, marginBottom: spacing.lg, color: brand.inkMuted },
  body: { flexDirection: 'row', gap: spacing.lg, marginBottom: spacing.xl },
  text: { flex: 1 },
  side: { width: PHOTO_W },
  photo: {
    width: PHOTO_W,
    height: PHOTO_W,
    borderRadius: radius.lg,
    overflow: 'hidden',
    justifyContent: 'flex-end',
  },
  credit: { position: 'absolute', left: PHOTO_CREDIT_INSET, bottom: PHOTO_CREDIT_INSET },
  mark: { ...type.label, color: brand.primary },
  blurb: { ...type.body, marginTop: spacing.xs, color: brand.inkMuted },
  more: {
    height: 54,
    borderRadius: 17,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    backgroundColor: brand.primary,
  },
  moreLabel: { ...type.label, color: brand.onPrimary },
});
