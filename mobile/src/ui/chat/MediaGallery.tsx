// Photos under an answer (src/core/media), across the bubble's whole inner width: one wide photo,
// a list of rows, or portrait cards sharing the width (a list instead when they would be too
// narrow). The credit sits on each photo as a small clickable pill with a camera icon. Laid out
// from the bubble's first frame (the width the window predicts, then its own measured width) so
// nothing jumps while the text types out; once the text ends the cards rise in one after another
// and their captions type out like the reply, as one more reveal.ts stream (`mediaRevealId`)
// queued right after it.
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated,
  Easing,
  Image,
  type LayoutChangeEvent,
  Platform,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { photoSource } from '@/core/media/bundled';
import type { MediaPick, MediaPickItem } from '@/core/media/media';

import { PHOTO_CREDIT_INSET, PhotoCredit } from '../PhotoCredit';
import { brand, fonts, radius, spacing, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

import { useRevealedWords, type RevealRow } from './reveal';

/** A little shorter than the 4:5 source crop (cover trims top and bottom), capped on tablets. */
const SINGLE_RATIO = 1.1;
const SINGLE_MAX_HEIGHT = 360;
const THUMB = 104;
const CARD_RATIO = 1.25; // 4:5
const CARD_GAP = spacing.sm;
/**
 * Columns never scroll or clip: under this card width they fall back to a list of rows. Two
 * cards fit from a 360 pt phone; three need a tablet.
 */
const MIN_CARD_WIDTH = 100;
const CARD_MS = 360;
const STAGGER_MS = 90;
const IMAGE_FADE_MS = 260;
const PULSE_MS = 850;
const RISE = 8;
const CREDIT_INSET = PHOTO_CREDIT_INSET;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
const WEB_LINK = /^https?:\/\/\S+$/i;

/** Bundled photo files already decoded this session, so recycled/scrolled cells show without flicker. */
const loadedPhotos = new Set<string>();

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
  scientific ? `${common}, ${scientific}` : common;

/** The glyph family a photo's licence belongs to: CC or public domain. */
export const licenseFamily = (license: string): 'cc' | 'publicDomain' =>
  /^CC/i.test(license) ? 'cc' : 'publicDomain';

/** Web URL for a photo's attribution source: its explicit link, or its Wikimedia Commons search. */
export function photoSourceUrl(item: MediaPickItem): string {
  if (item.photo.url && WEB_LINK.test(item.photo.url)) return item.photo.url;
  const query = `${item.scientific ?? item.common} ${item.photo.author}`.trim();
  return `https://commons.wikimedia.org/w/index.php?search=${encodeURIComponent(query)}&title=Special:MediaSearch&type=image`;
}

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
    if (w > 0) setMeasured((prev) => (prev !== null && Math.abs(prev - w) <= 2 ? prev : w));
  };
  // Cascade only when this mount arrived while captions are still streaming; an already-read row
  // (or reduced motion) has `words === Infinity` and shows whole at once.
  const [cards] = useState(() => {
    const cascade = words < Infinity;
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
        easing: Easing.out(Easing.cubic),
        useNativeDriver: USE_NATIVE_DRIVER,
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
        <Photo key={item.photo.file} item={item} width={width} height={height} />
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
            <Photo key={item.photo.file} item={item} width={THUMB} height={THUMB} />
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
          <Photo
            key={item.photo.file}
            item={item}
            width={cardWidth}
            height={Math.round(cardWidth * CARD_RATIO)}
          />
          <Caption words={caption} shown={shown} />
        </Animated.View>
      ))}
    </View>
  );
}

const rise = (shown: Animated.Value) => ({
  opacity: shown,
  transform: [
    { translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [RISE, 0] }) },
    { scale: shown.interpolate({ inputRange: [0, 1], outputRange: [0.985, 1] }) },
  ],
});

function Photo({ item, width, height }: { item: MediaPickItem; width: number; height: number }) {
  const reduced = useReducedMotion();
  const file = item.photo.file;
  const [loaded, setLoaded] = useState(() => loadedPhotos.has(file));
  const [imageOpacity] = useState(() => new Animated.Value(loadedPhotos.has(file) ? 1 : 0));
  const [pulse] = useState(() => new Animated.Value(0.45));
  const doneRef = useRef(loaded);

  useEffect(() => {
    if (loaded || reduced) return;
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, {
          toValue: 0.72,
          duration: PULSE_MS,
          easing: Easing.inOut(Easing.sin),
          useNativeDriver: USE_NATIVE_DRIVER,
        }),
        Animated.timing(pulse, {
          toValue: 0.34,
          duration: PULSE_MS,
          easing: Easing.inOut(Easing.sin),
          useNativeDriver: USE_NATIVE_DRIVER,
        }),
      ]),
    );
    loop.start();
    return () => loop.stop();
  }, [loaded, pulse, reduced]);

  const onImageReady = useCallback(() => {
    if (doneRef.current) return;
    doneRef.current = true;
    loadedPhotos.add(file);
    setLoaded(true);
    if (reduced) {
      imageOpacity.setValue(1);
      return;
    }
    Animated.timing(imageOpacity, {
      toValue: 1,
      duration: IMAGE_FADE_MS,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  }, [file, imageOpacity, reduced]);

  return (
    <View style={[styles.photoFrame, { width, height }]}>
      {!loaded ? (
        <Animated.View
          pointerEvents="none"
          style={[StyleSheet.absoluteFill, styles.photoSkeleton, { opacity: pulse }]}
        />
      ) : null}
      <Animated.View style={{ opacity: imageOpacity }}>
        <Image
          source={photoSource(file)}
          style={[styles.photo, { width, height }]}
          resizeMode="cover"
          onLoad={onImageReady}
          onLoadEnd={onImageReady}
          accessible
          accessibilityRole="image"
          accessibilityLabel={captionLabel(item)}
        />
      </Animated.View>
      <View pointerEvents="none" style={[StyleSheet.absoluteFill, styles.photoBorder]} />
      <Animated.View
        style={[styles.creditWrap, { opacity: imageOpacity }]}
        pointerEvents={loaded ? 'box-none' : 'none'}
      >
        <Credit item={item} maxWidth={width - 2 * CREDIT_INSET} />
      </Animated.View>
    </View>
  );
}

/**
 * Common name on top; scientific name underneath in a smaller italic font without parentheses.
 * Words not typed yet are transparent so layout never shifts while streaming.
 */
function Caption({ words, shown }: { words: Word[]; shown: number }) {
  const split = words.findIndex((w) => w.italic);
  const common = split === -1 ? words : words.slice(0, split);
  const scientific = split === -1 ? [] : words.slice(split);
  return (
    <View style={styles.captionWrap}>
      <Text style={styles.caption}>
        {common.map((w, i) => (
          <Text key={i} style={i >= shown ? styles.untyped : undefined}>
            {w.text}
            {i < common.length - 1 ? ' ' : ''}
          </Text>
        ))}
      </Text>
      {scientific.length > 0 ? (
        <Text style={styles.scientific}>
          {scientific.map((w, i) => (
            <Text key={i} style={common.length + i >= shown ? styles.untyped : undefined}>
              {w.text}
              {i < scientific.length - 1 ? ' ' : ''}
            </Text>
          ))}
        </Text>
      ) : null}
    </View>
  );
}

/** Camera icon and author on the photo's corner; tapping opens the photo's source. */
function Credit({ item, maxWidth }: { item: MediaPickItem; maxWidth: number }) {
  return (
    <PhotoCredit
      author={item.photo.author}
      license={item.photo.license}
      url={photoSourceUrl(item)}
      maxWidth={maxWidth}
    />
  );
}

const styles = StyleSheet.create({
  gallery: { marginTop: spacing.md },
  photoFrame: {
    borderRadius: radius.md,
    overflow: 'hidden',
    backgroundColor: brand.card,
  },
  photoSkeleton: {
    backgroundColor: brand.primarySoft,
  },
  photo: { borderRadius: radius.md },
  photoBorder: {
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: brand.primarySoft,
  },
  row: { flexDirection: 'row', alignItems: 'center', paddingVertical: spacing.sm },
  rowDivider: { borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: brand.primarySoft },
  rowText: { flex: 1, marginLeft: spacing.md },
  strip: { flexDirection: 'row', gap: CARD_GAP },
  captionWrap: { marginTop: spacing.xs },
  caption: { ...type.caption, fontFamily: fonts.semibold, color: brand.ink },
  scientific: {
    fontFamily: fonts.medium,
    fontStyle: 'italic',
    fontSize: 11,
    lineHeight: 15,
    color: brand.inkMuted,
    marginTop: 1,
  },
  untyped: { color: 'transparent' },
  creditWrap: {
    position: 'absolute',
    left: CREDIT_INSET,
    bottom: CREDIT_INSET,
  },
});
