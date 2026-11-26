// What an assistant answer rests on: a redesigned bottom sheet listing each source card with its
// favicon preview, main URL fragment, clock-icon timestamp, favorite toggle, and icon-only link
// button on the same row. One sheet per screen, not one per bubble, so opening it never resizes a
// list row and no open state can follow a recycled row onto another message.
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated,
  BackHandler,
  Easing,
  Linking,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { fill, t } from '@/i18n';
import {
  sourceFavoriteKey,
  toggleFavoriteSource,
  useFavoriteSources,
} from '@/state/favoriteSources';

import { Icon } from '../icons/Icon';
import { brand, fonts, radius, spacing, type } from '../theme/tokens';
import { scaleSize, useAccessibilityTheme } from '../useAccessibilityTheme';
import { useReducedMotion } from '../useReducedMotion';

import type { ChatSource } from './citations';
import { formatSourceLink, SourceFaviconBall, sourcePreviewFor } from './SourceFavicon';

const copy = t.chatScreen.sources;
/** Web pages only: a source never opens another app or runs a script. */
const WEB_LINK = /^https?:\/\/\S+$/i;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';

export interface SourcesSheetProps {
  /** The sources to list; null or empty keeps the sheet closed. */
  sources: ChatSource[] | null;
  onClose: () => void;
  /** Bottom safe-area inset, so the last source clears the home indicator. */
  bottom?: number;
  /** No motion even when the system setting is off (the design catalog's toggle). */
  reducedMotion?: boolean;
}

export function SourcesSheet({ sources, ...rest }: SourcesSheetProps) {
  return sources?.length ? <OpenSheet sources={sources} {...rest} /> : null;
}

function OpenSheet({
  sources,
  onClose,
  bottom = 0,
  reducedMotion = false,
}: SourcesSheetProps & { sources: ChatSource[] }) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  const reduced = useReducedMotion() || reducedMotion;
  const [shown] = useState(() => new Animated.Value(reduced ? 1 : 0));
  const favorites = useFavoriteSources();
  const favoriteKeys = useMemo(() => new Set(favorites.map((f) => f.key)), [favorites]);
  // Leaving, the chat under the sheet already takes touches. Keyed by the sources it is closing,
  // so asking for others while it leaves makes it take touches again.
  const [closingFor, setClosingFor] = useState<ChatSource[] | null>(null);
  const closing = closingFor === sources;
  const leaving = useRef<Animated.CompositeAnimation | null>(null);
  // Opens on mount, and again from wherever it is when the chat asks for other sources while it
  // leaves: stopping the exit (finished: false) keeps it from closing the new sources.
  useEffect(() => {
    leaving.current?.stop();
    leaving.current = null;
    if (reduced) return shown.setValue(1);
    const anim = Animated.timing(shown, {
      toValue: 1,
      duration: 260,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [reduced, shown, sources]);
  useEffect(() => () => leaving.current?.stop(), []);
  /** Slides out from wherever it is, then tells the chat it is gone. */
  const close = useCallback(() => {
    if (reduced) return onClose();
    setClosingFor(sources);
    const anim = Animated.timing(shown, {
      toValue: 0,
      duration: 200,
      easing: Easing.in(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    leaving.current = anim;
    anim.start(({ finished }) => {
      if (finished && leaving.current === anim) {
        leaving.current = null;
        onClose();
      }
    });
  }, [onClose, reduced, shown, sources]);
  // Android's back button closes the sheet before it leaves the screen (web has no back button
  // and logs an error on subscribe).
  useEffect(() => {
    if (Platform.OS !== 'android') return;
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      close();
      return true;
    });
    return () => sub.remove();
  }, [close]);
  return (
    <View
      style={[StyleSheet.absoluteFill, styles.overlay]}
      pointerEvents={closing ? 'none' : 'auto'}
    >
      <Animated.View
        style={[
          StyleSheet.absoluteFill,
          styles.scrim,
          {
            backgroundColor: palette.ink,
            opacity: shown.interpolate({
              inputRange: [0, 1],
              outputRange: [0, highContrast ? 0.42 : 0.28],
            }),
          },
        ]}
      >
        {/* Tapping outside closes too; screen readers get the labelled close button instead. */}
        <Pressable style={StyleSheet.absoluteFill} onPress={close} accessible={false} />
      </Animated.View>
      <Animated.View
        style={[
          styles.sheet,
          {
            paddingBottom: bottom + 16,
            backgroundColor: palette.card,
            borderTopWidth: highContrast ? borderWidth : 0,
            borderColor: palette.ink,
          },
          {
            opacity: shown,
            transform: [
              { translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [16, 0] }) },
            ],
          },
        ]}
        accessibilityViewIsModal
      >
        <View style={[styles.handle, { backgroundColor: palette.primarySoft }]} aria-hidden />
        <View style={styles.header}>
          <View style={styles.titleRow}>
            <Text style={[styles.title, scaled.title, { color: palette.ink }]} accessibilityRole="header">
              {copy.title}
            </Text>
            <View style={[styles.countBadge, { backgroundColor: palette.cardShade }]} aria-hidden>
              <Text style={[styles.countText, { color: palette.ink }]}>{sources.length}</Text>
            </View>
          </View>
          <Pressable
            onPress={close}
            accessibilityRole="button"
            accessibilityLabel={copy.close}
            style={({ pressed }) => [
              styles.close,
              { outlineColor: palette.primary },
              pressed && { backgroundColor: palette.cardShade },
            ]}
          >
            <Icon name="x" size={20} color={palette.ink} />
          </Pressable>
        </View>
        <ScrollView style={styles.list} contentContainerStyle={styles.listContent}>
          {sources.map((s, i) => (
            <SourceCard
              key={s.id}
              source={s}
              index={i}
              saved={favoriteKeys.has(sourceFavoriteKey(s))}
              reduced={reduced}
            />
          ))}
        </ScrollView>
      </Animated.View>
    </View>
  );
}

function SourceCard({
  source,
  index,
  saved,
  reduced,
}: {
  source: ChatSource;
  index: number;
  saved: boolean;
  reduced: boolean;
}) {
  const { palette, textScale, highContrast, borderWidth } = useAccessibilityTheme();
  const url = source.url && WEB_LINK.test(source.url) ? source.url : null;
  const fragment = useMemo(() => formatSourceLink(url ?? undefined), [url]);
  const preview = useMemo(() => sourcePreviewFor(source, index), [source, index]);
  const [starScale] = useState(() => new Animated.Value(1));
  const open = () => {
    if (!url) return;
    Linking.openURL(url).catch((e: unknown) =>
      console.warn(`Could not open source ${source.id} (${url})`, e),
    );
  };
  const toggleFav = () => {
    toggleFavoriteSource(source);
    if (reduced) return;
    starScale.setValue(0.84);
    Animated.spring(starScale, {
      toValue: 1,
      stiffness: 420,
      damping: 20,
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  };
  return (
    <View
      style={[
        styles.card,
        {
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          backgroundColor: palette.card,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View style={styles.cardHead}>
        <SourceFaviconBall preview={preview} size={28} ringColor={palette.cardShade} />
        <View style={styles.cardHeadText}>
          <Text
            style={[
              styles.itemTitle,
              {
                color: palette.ink,
                fontSize: scaleSize(15, textScale),
                lineHeight: scaleSize(20, textScale),
              },
            ]}
          >
            {source.title}
          </Text>
          {fragment ? (
            <Text
              style={[
                styles.linkFragment,
                {
                  color: palette.primary,
                  fontSize: scaleSize(12, textScale),
                  lineHeight: scaleSize(16, textScale),
                },
              ]}
              numberOfLines={1}
              ellipsizeMode="tail"
            >
              {fragment}
            </Text>
          ) : null}
          {source.verified ? (
            <View
              style={[
                styles.verifiedMark,
                { backgroundColor: palette.goldSoft, borderColor: palette.gold },
              ]}
            >
              <Icon name="circleCheck" size={13} color={palette.gold} strokeWidth={2.4} />
              <Text
                style={[
                  styles.verifiedText,
                  {
                    color: palette.goldInk,
                    fontSize: scaleSize(12, textScale),
                    lineHeight: scaleSize(16, textScale),
                  },
                ]}
              >
                {t.chatScreen.verified.source}
              </Text>
            </View>
          ) : null}
        </View>
      </View>
      {source.excerpt ? (
        <Text
          style={[
            styles.excerpt,
            {
              color: palette.inkMuted,
              fontSize: scaleSize(14, textScale),
              lineHeight: scaleSize(20, textScale),
            },
          ]}
        >
          {source.excerpt}
        </Text>
      ) : null}
      <View style={styles.cardFooter}>
        <View style={styles.dateRow}>
          {source.date ? (
            <>
              <Icon name="clock" size={13} color={palette.inkMuted} strokeWidth={2} />
              <Text style={[styles.date, { color: palette.inkMuted }]}>{source.date}</Text>
            </>
          ) : null}
        </View>
        <View style={styles.actions}>
          <Animated.View style={{ transform: [{ scale: starScale }] }}>
            <Pressable
              onPress={toggleFav}
              hitSlop={4}
              accessibilityRole="button"
              accessibilityState={{ selected: saved }}
              accessibilityLabel={fill(saved ? copy.unfavoriteLabel : copy.favoriteLabel, {
                title: source.title,
              })}
              style={({ pressed }) => [
                styles.iconAction,
                {
                  backgroundColor: saved ? palette.primary : palette.cardShade,
                  outlineColor: palette.primary,
                },
                pressed && styles.iconActionPressed,
              ]}
            >
              <Icon
                name="star"
                size={16}
                color={saved ? palette.onPrimary : palette.ink}
                fill={saved ? palette.onPrimary : 'none'}
                strokeWidth={2}
              />
            </Pressable>
          </Animated.View>
          {url ? (
            <Pressable
              onPress={open}
              hitSlop={4}
              accessibilityRole="link"
              accessibilityLabel={fill(copy.openLabel, { title: source.title })}
              style={({ pressed }) => [
                styles.iconAction,
                { backgroundColor: palette.cardShade, outlineColor: palette.primary },
                pressed && styles.iconActionPressed,
              ]}
            >
              <Icon name="externalLink" size={16} color={palette.ink} strokeWidth={2} />
            </Pressable>
          ) : null}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  // Bottom-anchored and centered, so on a tablet the sheet keeps a phone-like width.
  overlay: { justifyContent: 'flex-end', alignItems: 'center' },
  scrim: { backgroundColor: brand.ink },
  sheet: {
    maxHeight: '76%',
    width: '100%',
    maxWidth: 560,
    paddingTop: 8,
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    backgroundColor: brand.card,
  },
  handle: {
    width: 36,
    height: 4,
    borderRadius: 2,
    backgroundColor: brand.primarySoft,
    alignSelf: 'center',
    marginBottom: 6,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 20,
    paddingRight: 10,
    paddingBottom: 8,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  title: { ...type.title, color: brand.ink },
  countBadge: {
    minWidth: 24,
    height: 22,
    paddingHorizontal: 7,
    borderRadius: radius.pill,
    backgroundColor: brand.cardShade,
    alignItems: 'center',
    justifyContent: 'center',
  },
  countText: {
    fontFamily: fonts.bold,
    fontSize: 12,
    lineHeight: 16,
    color: brand.ink,
    fontVariant: ['tabular-nums'],
  },
  close: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
  },
  closePressed: { backgroundColor: brand.cardShade },
  list: { flexGrow: 0 },
  listContent: { paddingHorizontal: 18, paddingTop: 4, paddingBottom: 8, gap: 10 },
  card: {
    borderRadius: 18,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
    paddingHorizontal: 14,
    paddingVertical: 12,
    gap: 10,
    boxShadow: `0 2px 10px ${brand.glow}`,
  },
  cardHead: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  cardHeadText: {
    flex: 1,
    gap: 2,
  },
  itemTitle: {
    ...type.label,
    fontSize: 15,
    lineHeight: 20,
    color: brand.ink,
  },
  linkFragment: {
    ...type.caption,
    fontSize: 12,
    lineHeight: 16,
    color: brand.primary,
  },
  verifiedMark: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: 4,
    marginTop: 4,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: radius.pill,
    borderWidth: 1,
  },
  verifiedText: { ...type.caption, fontFamily: fonts.semibold, fontSize: 12, lineHeight: 16 },
  excerpt: {
    ...type.body,
    fontSize: 14,
    lineHeight: 20,
    color: brand.inkMuted,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  dateRow: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  date: {
    ...type.caption,
    fontSize: 12,
    lineHeight: 16,
    color: brand.inkMuted,
    fontVariant: ['tabular-nums'],
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  iconAction: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: brand.cardShade,
    outlineColor: brand.primary,
  },
  iconActionSaved: {
    backgroundColor: brand.primary,
  },
  iconActionPressed: {
    opacity: 0.8,
  },
});
