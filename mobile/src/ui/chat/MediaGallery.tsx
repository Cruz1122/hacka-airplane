// Photos under an answer (src/core/media), across the bubble's whole inner width: one wide photo,
// a list of rows, or portrait cards sharing the width (a list instead when they would be too
// narrow). The credit sits on each photo as a small pill. Laid out from the bubble's first frame
// (the width the window predicts, then its own measured width) so nothing jumps while the text
// types out; once the text ends the cards rise in one after another and their captions type out
// like the reply, as one more reveal.ts stream (`mediaRevealId`) queued right after it.
import { useEffect, useMemo, useState } from 'react';
import {
  Animated,
  Easing,
  Image,
  type LayoutChangeEvent,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';

import { photoSource } from '@/core/media/bundled';
import type { MediaPhoto, MediaPick, MediaPickItem } from '@/core/media/media';
import { fill, t } from '@/i18n';

import { brand, fonts, radius, spacing, type } from '../theme/tokens';

import { useRevealedWords, type RevealRow } from './reveal';

/** A little shorter than the 4:5 source crop (cover trims top and bottom), capped on tablets. */
const SINGLE_RATIO = 1.1;
const SINGLE_MAX_HEIGHT = 360;
const THUMB = 104;
const CARD_RATIO = 1.25; // 4:5
const CARD_GAP = spacing.sm;
/**
 * Columns never scroll or clip: under this card width they fall back to a list of rows. Two
 * cards fit from a 360 pt phone (about 107 pt each beside the source button); three need a
 * tablet.
 */
const MIN_CARD_WIDTH = 100;
const CARD_MS = 280;
const STAGGER_MS = 90;
const RISE = 8;
const CREDIT_INSET = 6;
const MARK = 11;

/** The reveal.ts stream of row `id`'s captions. */
export const mediaRevealId = (id: string) => `${id}:media`;

interface Word {
  text: string;
  italic: boolean;
}

/** A caption's words, as reveal.ts counts them (`\S+`): the common name, then the scientific one. */
function captionWords({ common, scientific }: MediaPickItem): Word[] {
  const words = (s: string, italic: boolean) =>
    (s.match(/\S+/g) ?? []).map((text) => ({ text, italic }));
  return [...words(common, false), ...(scientific ? words(scientific, true) : [])];
}

/** How many of the stream's first `words` each caption gets, in order. */
function splitWords(captions: readonly Word[][], words: number): number[] {
  let left = words;
  return captions.map((c) => {
    const shown = Math.min(c.length, Math.max(0, left));
    left -= c.length;
    return shown;
  });
}

const captionLabel = ({ common, scientific }: MediaPickItem) =>
  scientific ? `${common} (${scientific})` : common;

/** The glyph a photo's credit wears: every licence media.json allows is CC or public domain. */
export const licenseFamily = (license: string): 'cc' | 'publicDomain' =>
  /^CC/i.test(license) ? 'cc' : 'publicDomain';

/**
 * The rows to hand `replyReveal.schedule`: each reply with photos is followed by its captions'
 * stream, so they type out after the reply and before the next one. Pass every row through this,
 * the `seen` set included: the store drops streams it is not handed.
 */
export function revealRows<R extends RevealRow & { media?: MediaPick }>(
  rows: readonly R[],
): RevealRow[] {
  return rows.flatMap((r): RevealRow[] =>
    r.role === 'assistant' && r.media
      ? [
          r,
          {
            id: mediaRevealId(r.id),
            role: 'assistant',
            text: r.media.items.map(captionLabel).join(' '),
          },
        ]
      : [r],
  );
}

export interface MediaGalleryProps {
  media: MediaPick;
  /**
   * The bubble's inner width as the window predicts it. The gallery lays out at this width on its
   * first frame, then at its own measured width (the bubble's, never its content's).
   */
  width: number;
  /**
   * The reply's reveal row id; the gallery waits for its captions' stream. Without one (reduced
   * motion, a screen reader, the catalog) it shows whole at once.
   */
  revealId?: string;
}

export function MediaGallery({ media, width: predicted, revealId }: MediaGalleryProps) {
  const words = useRevealedWords(revealId === undefined ? undefined : mediaRevealId(revealId));
  const [measured, setMeasured] = useState<number | null>(null);
  const width = measured ?? predicted;
  const onLayout = (e: LayoutChangeEvent) => {
    const w = Math.floor(e.nativeEvent.layout.width);
    if (w > 0) setMeasured(w);
  };
  // Hidden only when this mount saw the stream before it started; a row already read shows whole.
  const [cards] = useState(() => {
    const cascade = words === 0;
    return { cascade, shown: media.items.map(() => new Animated.Value(cascade ? 0 : 1)) };
  });
  const started = words > 0;
  useEffect(() => {
    if (!started || !cards.cascade) return;
    const runs = cards.shown.map((v, i) =>
      Animated.timing(v, {
        toValue: 1,
        duration: CARD_MS,
        delay: i * STAGGER_MS,
        easing: Easing.out(Easing.quad),
        useNativeDriver: true,
      }),
    );
    runs.forEach((r) => r.start());
    return () => runs.forEach((r) => r.stop());
  }, [started, cards]);

  const captions = useMemo(() => media.items.map(captionWords), [media]);
  // Built once: captions re-render the gallery every chunk, and a new interpolation each time
  // would re-attach the native-driven animation mid-flight.
  const rises = useMemo(() => cards.shown.map(rise), [cards]);
  const typed = splitWords(captions, words);
  const items = media.items.map((item, i) => ({
    item,
    caption: captions[i],
    shown: typed[i],
    style: rises[i],
  }));

  if (media.layout === 'single') {
    const [{ item, caption, shown, style }] = items;
    const height = Math.min(Math.round(width * SINGLE_RATIO), SINGLE_MAX_HEIGHT);
    return (
      <Animated.View style={[styles.gallery, style]} onLayout={onLayout}>
        <Photo item={item} width={width} height={height} />
        <Caption words={caption} shown={shown} />
      </Animated.View>
    );
  }
  const n = items.length;
  const cardWidth = Math.floor((width - CARD_GAP * (n - 1)) / n);
  if (media.layout === 'rows' || cardWidth < MIN_CARD_WIDTH) {
    return (
      <View style={styles.gallery} onLayout={onLayout}>
        {items.map(({ item, caption, shown, style }, i) => (
          <Animated.View key={item.id} style={[styles.row, i > 0 && styles.rowDivider, style]}>
            <Photo item={item} width={THUMB} height={THUMB} />
            <View style={styles.rowText}>
              <Caption words={caption} shown={shown} />
            </View>
          </Animated.View>
        ))}
      </View>
    );
  }
  return (
    <View style={[styles.gallery, styles.strip]} onLayout={onLayout}>
      {items.map(({ item, caption, shown, style }) => (
        <Animated.View key={item.id} style={[{ width: cardWidth }, style]}>
          <Photo item={item} width={cardWidth} height={Math.round(cardWidth * CARD_RATIO)} />
          <Caption words={caption} shown={shown} />
        </Animated.View>
      ))}
    </View>
  );
}

const rise = (shown: Animated.Value) => ({
  opacity: shown,
  transform: [{ translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [RISE, 0] }) }],
});

function Photo({ item, width, height }: { item: MediaPickItem; width: number; height: number }) {
  return (
    <View>
      <Image
        source={photoSource(item.photo.file)}
        style={[styles.photo, { width, height }]}
        resizeMode="cover"
        accessible
        accessibilityRole="image"
        accessibilityLabel={captionLabel(item)}
      />
      <Credit photo={item.photo} maxWidth={width - 2 * CREDIT_INSET} />
    </View>
  );
}

/** The whole caption is laid out from the first frame; words not typed yet are transparent. */
function Caption({ words, shown }: { words: Word[]; shown: number }) {
  const last = words.length - 1;
  const firstItalic = words.findIndex((w) => w.italic);
  return (
    <Text style={styles.caption}>
      {words.map((w, i) => (
        <Text key={i} style={i >= shown ? styles.untyped : undefined}>
          {i === firstItalic ? '(' : ''}
          <Text style={w.italic ? styles.italic : undefined}>{w.text}</Text>
          {w.italic && i === last ? ')' : ''}
          {i < last ? ' ' : ''}
        </Text>
      ))}
    </Text>
  );
}

/** Licence glyph and author on the photo's corner; screen readers hear the full licence. */
function Credit({ photo, maxWidth }: { photo: MediaPhoto; maxWidth: number }) {
  return (
    <View
      style={[styles.credit, { maxWidth }]}
      accessible
      accessibilityLabel={fill(t.chatScreen.media.credit, {
        author: photo.author,
        license: photo.license,
      })}
    >
      <LicenseMark license={photo.license} />
      <Text style={styles.author} numberOfLines={1} ellipsizeMode="tail">
        {photo.author}
      </Text>
    </View>
  );
}

// 24-unit glyphs drawn as strokes: a ring around "cc" (Creative Commons) or around a struck-through
// "c" (the Public Domain Mark).
const CC_LETTERS = 'M11.22 9.88A3 3 0 1 0 11.22 14.12M17.82 9.88A3 3 0 1 0 17.82 14.12';
const PD_LETTER = 'M15.25 8.75A4.6 4.6 0 1 0 15.25 15.25M5.2 5.2L18.8 18.8';

function LicenseMark({ license }: { license: string }) {
  const family = licenseFamily(license);
  return (
    <Svg
      width={MARK}
      height={MARK}
      viewBox="0 0 24 24"
      testID={`license-${family}`}
    >
      <Circle cx={12} cy={12} r={10.5} stroke={brand.onPrimary} strokeWidth={2.2} fill="none" />
      <Path
        d={family === 'cc' ? CC_LETTERS : PD_LETTER}
        stroke={brand.onPrimary}
        strokeWidth={2.4}
        strokeLinecap="round"
        fill="none"
      />
    </Svg>
  );
}

const styles = StyleSheet.create({
  gallery: { marginTop: spacing.md },
  photo: { borderRadius: radius.md, backgroundColor: brand.primarySoft },
  row: { flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.sm },
  rowDivider: { borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: brand.primarySoft },
  rowText: { flex: 1, marginLeft: spacing.md },
  strip: { flexDirection: 'row', gap: CARD_GAP },
  caption: { ...type.caption, fontFamily: fonts.semibold, color: brand.ink, marginTop: spacing.xs },
  italic: { fontStyle: 'italic', fontFamily: fonts.medium },
  untyped: { color: 'transparent' },
  credit: {
    position: 'absolute',
    left: CREDIT_INSET,
    bottom: CREDIT_INSET,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingLeft: 5,
    paddingRight: 7,
    paddingVertical: 3,
    borderRadius: radius.pill,
    backgroundColor: brand.photoScrim,
  },
  author: {
    flexShrink: 1,
    fontFamily: fonts.bold,
    fontSize: 10,
    lineHeight: 13,
    color: brand.onPrimary,
  },
});
