// What an assistant answer rests on: a sheet over the chat listing each source, with its link when
// it has one and the passage itself when it does not. One sheet per screen, not one per bubble, so
// opening it never resizes a list row (the list would jump to its end) and no open state can
// follow a recycled row onto another message.
import { useCallback, useEffect, useState } from 'react';
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

import { Icon } from '../icons/Icon';
import { brand, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

import type { ChatSource } from './citations';

const copy = t.chatScreen.sources;
/** Web pages only: a source never opens another app or runs a script. */
const WEB_LINK = /^https?:\/\/\S+$/i;

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
  const reduced = useReducedMotion() || reducedMotion;
  const [shown] = useState(() => new Animated.Value(reduced ? 1 : 0));
  // Leaving, the chat under the sheet already takes touches.
  const [closing, setClosing] = useState(false);
  useEffect(() => {
    if (reduced) return shown.setValue(1);
    const anim = Animated.timing(shown, {
      toValue: 1,
      duration: 260,
      easing: Easing.out(Easing.quad),
      useNativeDriver: true,
    });
    anim.start();
    return () => anim.stop();
  }, [reduced, shown]);
  /** Slides out from wherever it is, then tells the chat it is gone. */
  const close = useCallback(() => {
    if (reduced) return onClose();
    setClosing(true);
    Animated.timing(shown, {
      toValue: 0,
      duration: 200,
      easing: Easing.in(Easing.quad),
      useNativeDriver: true,
    }).start(({ finished }) => {
      if (finished) onClose();
    });
  }, [onClose, reduced, shown]);
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
          { opacity: shown.interpolate({ inputRange: [0, 1], outputRange: [0, 0.28] }) },
        ]}
      >
        {/* Tapping outside closes too; screen readers get the labelled close button instead. */}
        <Pressable style={StyleSheet.absoluteFill} onPress={close} accessible={false} />
      </Animated.View>
      <Animated.View
        style={[
          styles.sheet,
          { paddingBottom: bottom + 16 },
          {
            opacity: shown,
            transform: [
              { translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [16, 0] }) },
            ],
          },
        ]}
        accessibilityViewIsModal
      >
        <View style={styles.header}>
          <Text style={styles.title} accessibilityRole="header">
            {copy.title}
          </Text>
          <Pressable
            onPress={close}
            accessibilityRole="button"
            accessibilityLabel={copy.close}
            style={({ pressed }) => [styles.close, pressed && styles.closePressed]}
          >
            <Icon name="x" size={20} color={brand.ink} />
          </Pressable>
        </View>
        <ScrollView style={styles.list} contentContainerStyle={styles.listContent}>
          {sources.map((s, i) => (
            <SourceItem key={s.id} source={s} first={i === 0} />
          ))}
        </ScrollView>
      </Animated.View>
    </View>
  );
}

function SourceItem({ source, first }: { source: ChatSource; first: boolean }) {
  const url = source.url && WEB_LINK.test(source.url) ? source.url : null;
  const open = () => {
    if (!url) return;
    Linking.openURL(url).catch((e: unknown) =>
      console.warn(`Could not open source ${source.id} (${url})`, e),
    );
  };
  return (
    <View style={[styles.item, !first && styles.itemDivided]}>
      <Text style={styles.itemTitle}>{source.title}</Text>
      {source.excerpt ? <Text style={styles.excerpt}>{source.excerpt}</Text> : null}
      {source.date ? (
        <Text style={styles.date}>{fill(copy.retrieved, { date: source.date })}</Text>
      ) : null}
      {url ? (
        <Pressable
          onPress={open}
          accessibilityRole="link"
          accessibilityLabel={fill(copy.openLabel, { title: source.title })}
          style={({ pressed }) => [styles.link, pressed && styles.linkPressed]}
        >
          <Icon name="externalLink" size={16} color={brand.ink} />
          <Text style={styles.linkText}>{copy.open}</Text>
        </Pressable>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  // Bottom-anchored and centered, so on a tablet the sheet keeps a phone-like width.
  overlay: { justifyContent: 'flex-end', alignItems: 'center' },
  scrim: { backgroundColor: brand.ink },
  sheet: {
    maxHeight: '72%',
    width: '100%',
    maxWidth: 560,
    paddingTop: 8,
    borderTopLeftRadius: 26,
    borderTopRightRadius: 26,
    backgroundColor: brand.card,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 22,
    paddingRight: 10,
  },
  title: { ...type.title, color: brand.ink },
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
  listContent: { paddingHorizontal: 22, paddingBottom: 4 },
  item: { paddingVertical: 14, gap: 6 },
  itemDivided: { borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: brand.cardShade },
  itemTitle: { ...type.label, color: brand.ink },
  excerpt: { ...type.body, color: brand.inkMuted },
  date: { ...type.caption, color: brand.inkMuted },
  link: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: 8,
    minHeight: 44,
    paddingHorizontal: 14,
    marginTop: 2,
    borderRadius: 22,
    backgroundColor: brand.cardShade,
    outlineColor: brand.primary,
  },
  linkPressed: { opacity: 0.85 },
  linkText: { ...type.label, color: brand.ink },
});
