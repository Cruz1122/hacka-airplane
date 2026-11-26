// Quiet message surfaces. A concave foot grounds each bubble on its side of the conversation; an
// assistant answer with sources gets a favicon preview badge tucked on its bottom-right corner
// (nudged slightly left), while response time sits below with a clock icon. Assistant text is a
// small Markdown subset (markdown.ts) with its keywords in bold, typed out word by word
// (reveal.ts) unless motion is reduced or a screen reader is on.
import {
  memo,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
  type ReactNode,
} from 'react';
import {
  Alert,
  Animated,
  Easing,
  Image,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';

import type { MediaPick } from '@/core/media/media';
import { fill, t } from '@/i18n';
import { autoSpeakReply, getSpeakingKey, subscribeSpeak, toggleSpeak } from '@/speech/speak';

import { Icon } from '../icons/Icon';
import { brand, fonts, radius, spacing, type } from '../theme/tokens';
import { scaleSize, useAccessibilityTheme } from '../useAccessibilityTheme';
import { useReducedMotion } from '../useReducedMotion';

import type { ChatSource } from './citations';
import { replyDoc, sliceDoc, type Block } from './markdown';
import { MediaGallery } from './MediaGallery';
import { useRevealedWords } from './reveal';
import { SourceFaviconBall, sourcePreviews } from './SourceFavicon';
import { useScreenReader } from './useScreenReader';

export interface ChatBubbleProps {
  role: 'user' | 'assistant';
  /** As written; an assistant's citation markers are hidden, the user's words shown as typed. */
  text: string;
  photoUri?: string;
  meta?: string;
  /** Assistant only: what the answer rests on, opened by the sources badge. */
  sources?: ChatSource[];
  onOpenSources?: (sources: ChatSource[]) => void;
  /** Assistant only: phrases of `text` to set in bold (`keywordsFor(entryId)`). */
  keywords?: readonly string[];
  /**
   * Assistant only: the row id `replyReveal` types this reply out under. Until the store schedules
   * it the bubble shows nothing; without an id the text shows whole.
   */
  revealId?: string;
  /**
   * The row id whose first appearance plays the entry; a cell showing it again (recycled, or
   * scrolled back into view) does not. Without an id the bubble enters on every mount.
   */
  entryId?: string;
  /** Assistant only: photos under the text, shown once it has typed out. */
  media?: MediaPick;
}

/** A slow, short rise: the message settles in instead of popping. */
const ENTRY_MS = 280;
const ENTRY_RISE = 4;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
const NO_KEYWORDS: readonly string[] = [];
/** The row's side margins, a bubble's share of what is left, and its padding (styles below). */
const ROW_PADDING = 22;
const COLUMN_SHARE = 0.88;
const BUBBLE_PADDING = 17;

/**
 * A photo bubble's inner width as the window predicts it, for its gallery's first frame. The
 * gallery then measures itself: inside a narrower frame (the chat's centred column on a wide
 * screen, the design catalog) it settles one layout later.
 */
const predictedGalleryWidth = (screen: number) =>
  Math.floor(COLUMN_SHARE * (screen - 2 * ROW_PADDING)) - 2 * BUBBLE_PADDING;

/** Row ids whose bubble has entered, or that were on screen before; FlashList reuses cells. */
const entered = new Set<string>();

/** Rows the reader has already seen show without an entry. */
export function markEntered(ids: Iterable<string>) {
  for (const id of ids) entered.add(id);
}

export const ChatBubble = memo(function ChatBubble({
  role,
  text,
  photoUri,
  meta,
  sources,
  onOpenSources,
  keywords = NO_KEYWORDS,
  revealId,
  entryId,
  media,
}: ChatBubbleProps) {
  const { palette, scaled, autoSpeakReplies } = useAccessibilityTheme();
  const mine = role === 'user';
  const reduced = useReducedMotion();
  const reader = useScreenReader();
  const doc = useMemo(() => (mine ? null : replyDoc(text, keywords)), [mine, text, keywords]);
  const streamId = mine || reduced || reader ? undefined : revealId;
  const words = useRevealedWords(streamId);
  const screen = useWindowDimensions().width;
  const doneNow = !doc || words >= doc.stops.length;
  const wasDone = useRef(false);
  useEffect(() => {
    const justFinished = doneNow && !wasDone.current;
    wasDone.current = doneNow;
    if (!autoSpeakReplies || mine || !revealId || !doc?.text || words === 0 || !justFinished) return;
    autoSpeakReply(revealId, doc.text, (error) => {
      Alert.alert(t.chatScreen.voice.speakError, error.message);
    });
  }, [autoSpeakReplies, mine, revealId, doc, words, doneNow]);
  // Waiting for its turn (a banner is still typing out) or for the chat to schedule it.
  if (words === 0) return null;
  const done = doneNow;
  const cited = !mine && sources?.length ? sources : null;
  const sourced = cited !== null && onOpenSources !== undefined;
  const canSpeak = !mine && done && !!doc?.text;
  const gallery = mine ? undefined : media;
  const sentPhoto =
    mine && photoUri ? (
      <SentPhoto
        key={photoUri}
        uri={photoUri}
        reduced={reduced}
        placeholderBg={palette.cardShade}
      />
    ) : null;
  const bubbleContent = doc ? (
    <Reply blocks={done ? doc.blocks : sliceDoc(doc, doc.stops[words - 1])} label={doc.text} />
  ) : text ? (
    <Text style={[styles.mineText, scaled.body, { color: palette.onPrimary }]} selectable>
      {text}
    </Text>
  ) : null;
  const hasBubble = bubbleContent !== null || (gallery !== undefined && done);
  return (
    <BubbleRow
      role={role}
      entryId={entryId}
      meta={done ? meta : undefined}
      fill={gallery !== undefined}
      above={sentPhoto}
      accessory={
        done && (canSpeak || sourced) ? (
          <View style={styles.accessories}>
            {sourced ? <SourcesBadge sources={cited} onPress={() => onOpenSources(cited)} /> : null}
            {canSpeak && doc ? (
              <SpeakButton speakId={revealId ?? entryId ?? doc.text} text={doc.text} />
            ) : null}
          </View>
        ) : null
      }
    >
      {hasBubble ? (
        <>
          {bubbleContent}
          {gallery && done ? (
            <MediaGallery
              key={entryId}
              media={gallery}
              width={predictedGalleryWidth(screen)}
              revealId={streamId}
            />
          ) : null}
        </>
      ) : null}
    </BubbleRow>
  );
});

const SENT_PHOTO_WIDTH = 220;
const SENT_PHOTO_DEFAULT = { width: SENT_PHOTO_WIDTH, height: 165 };

/** User photo URIs already decoded this session (with measured size) so scrolling never re-fades. */
const loadedSentPhotos = new Map<string, { width: number; height: number }>();

function SentPhoto({
  uri,
  reduced,
  placeholderBg,
}: {
  uri: string;
  reduced: boolean;
  placeholderBg: string;
}) {
  const cached = loadedSentPhotos.get(uri);
  const initial = reduced || cached !== undefined;
  const [size, setSize] = useState(() => cached ?? SENT_PHOTO_DEFAULT);
  const [opacity] = useState(() => new Animated.Value(initial ? 1 : 0));
  const doneRef = useRef(initial);
  const onReady = useCallback(() => {
    if (doneRef.current) return;
    doneRef.current = true;
    if (!loadedSentPhotos.has(uri)) loadedSentPhotos.set(uri, SENT_PHOTO_DEFAULT);
    if (reduced) {
      opacity.setValue(1);
      return;
    }
    Animated.timing(opacity, {
      toValue: 1,
      duration: 220,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  }, [opacity, reduced, uri]);
  const onLoad = useCallback(
    (e: { nativeEvent?: { source?: { width?: number; height?: number } } }) => {
      const w = e.nativeEvent?.source?.width;
      const h = e.nativeEvent?.source?.height;
      if (w && h && w > 0 && h > 0) {
        const ratio = Math.min(1.5, Math.max(0.72, w / h));
        const next = { width: SENT_PHOTO_WIDTH, height: Math.round(SENT_PHOTO_WIDTH / ratio) };
        loadedSentPhotos.set(uri, next);
        setSize(next);
      }
      onReady();
    },
    [onReady, uri],
  );
  return (
    <View style={[styles.photoFrame, size, { backgroundColor: placeholderBg }]}>
      <Animated.View style={[StyleSheet.absoluteFill, { opacity }]}>
        <Image
          source={{ uri }}
          accessibilityLabel={t.chatScreen.photo.sent}
          accessible
          resizeMode="cover"
          onLoad={onLoad}
          onLoadEnd={onReady}
          style={styles.photo}
        />
      </Animated.View>
    </View>
  );
}

/** The shown blocks; screen readers get the whole reply from the first frame. */
function Reply({ blocks, label }: { blocks: Block[]; label: string }) {
  return (
    <View accessible accessibilityLabel={label}>
      {blocks.map((b, i) => (
        <BlockView key={i} block={b} first={i === 0} />
      ))}
    </View>
  );
}

/**
 * One paragraph or list item. Memoized by identity: `sliceDoc` keeps a whole block's object, so
 * while a reply types out only its last block re-renders.
 */
const BlockView = memo(function BlockView({ block: b, first }: { block: Block; first: boolean }) {
  const { palette, scaled } = useAccessibilityTheme();
  const textStyle = [styles.theirsText, scaled.body, { color: palette.ink }];
  return b.marker === null ? (
    <Text style={[textStyle, !first && styles.paragraphGap]} selectable>
      {spans(b)}
    </Text>
  ) : (
    <View style={[styles.item, !first && styles.itemGap]}>
      <Text style={[textStyle, styles.marker]}>{b.marker}</Text>
      <Text style={[textStyle, styles.itemText]} selectable>
        {spans(b)}
      </Text>
    </View>
  );
});

/** Plain runs as bare strings (a plain block is just its text), bold runs as nested Text. */
function spans(block: Block): ReactNode[] {
  return block.spans.map((s, i) =>
    s.bold ? (
      <Text key={i} style={styles.bold}>
        {s.text}
      </Text>
    ) : (
      s.text
    ),
  );
}

function SpeakButton({ speakId, text }: { speakId: string; text: string }) {
  const { palette, highContrast, borderWidth } = useAccessibilityTheme();
  const speaking = useSyncExternalStore(subscribeSpeak, getSpeakingKey) === speakId;
  const onPress = useCallback(() => {
    toggleSpeak(speakId, text, () => {
      Alert.alert(t.chatScreen.voice.errorTitle, t.chatScreen.voice.speakError);
    });
  }, [speakId, text]);
  const copy = t.chatScreen.voice;
  // Same content height as Fuentes: 18 pt glyph + 4 pt vertical padding + the shared edge.
  const badgeSize = 18 + 8 + 2 * borderWidth;
  return (
    <Pressable
      onPress={onPress}
      hitSlop={10}
      accessibilityRole="button"
      accessibilityLabel={speaking ? copy.speakStop : copy.speak}
      accessibilityState={{ busy: speaking }}
      style={({ pressed }) => [
        styles.speakBadge,
        {
          width: badgeSize,
          height: badgeSize,
          borderRadius: badgeSize / 2,
          borderColor: pressed ? palette.primary : highContrast ? palette.ink : palette.primarySoft,
          borderWidth,
          backgroundColor: pressed ? palette.cardShade : palette.card,
          boxShadow: `0 2px 8px ${palette.glow}`,
          outlineColor: palette.primary,
        },
      ]}
    >
      <Icon
        name={speaking ? 'circlePause' : 'volume2'}
        size={18}
        color={palette.ink}
        strokeWidth={2.1}
      />
    </Pressable>
  );
}

/** Bottom-right sources badge (nudged slightly left) with overlapping circular favicon previews. */
function SourcesBadge({
  sources,
  onPress,
}: {
  sources: readonly ChatSource[];
  onPress: () => void;
}) {
  const { palette, textScale, highContrast, borderWidth } = useAccessibilityTheme();
  const copy = t.chatScreen.sources;
  const count = sources.length;
  const previews = useMemo(() => sourcePreviews(sources), [sources]);
  // Gold only when every source is the UTON guion: a mixed answer keeps the ordinary badge.
  const verified = sources.every((s) => s.verified);
  const label = verified
    ? t.chatScreen.verified.label
    : count === 1
      ? copy.showOne
      : fill(copy.showMany, { n: count });
  const idleEdge = verified ? palette.gold : highContrast ? palette.ink : palette.primarySoft;
  const surface = verified ? palette.goldSoft : palette.card;
  return (
    <Pressable
      onPress={onPress}
      hitSlop={8}
      accessibilityRole="button"
      accessibilityLabel={label}
      style={({ pressed }) => [
        styles.sourceBadge,
        {
          borderColor: pressed ? (verified ? palette.goldInk : palette.primary) : idleEdge,
          borderWidth,
          backgroundColor: pressed ? palette.cardShade : surface,
          boxShadow: `0 2px 8px ${palette.glow}`,
          outlineColor: palette.primary,
        },
      ]}
    >
      <View style={styles.faviconStack}>
        {previews.map((preview, index) => (
          <SourceFaviconBall
            key={preview.key}
            preview={preview}
            size={18}
            overlap={index > 0}
            ringColor={surface}
          />
        ))}
      </View>
      {verified ? (
        <Icon name="circleCheck" size={14} color={palette.gold} strokeWidth={2.4} />
      ) : null}
      <Text
        style={[
          styles.sourceLabel,
          {
            color: verified ? palette.goldInk : palette.ink,
            fontSize: scaleSize(12, textScale),
            lineHeight: scaleSize(16, textScale),
          },
        ]}
      >
        {verified ? t.chatScreen.verified.badge : copy.title}
      </Text>
    </Pressable>
  );
}

export function BubbleRow({
  role,
  meta,
  above,
  accessory,
  entryId,
  fill = false,
  children,
}: {
  role: 'user' | 'assistant';
  meta?: string;
  /** Standalone media rendered above the bubble with no bubble surface or border. */
  above?: ReactNode;
  /** Overlaid on the bubble's bottom-right corner, nudged slightly left. */
  accessory?: ReactNode;
  /** See ChatBubbleProps.entryId. */
  entryId?: string;
  /**
   * The bubble takes its whole share of the row (photos span it), sized by the row and never by
   * its content.
   */
  fill?: boolean;
  children?: ReactNode;
}) {
  const { palette, textScale, highContrast } = useAccessibilityTheme();
  const mine = role === 'user';
  const reduced = useReducedMotion();
  // A value per row id, hidden from its first frame: a recycled cell must not flash a new row.
  const start = () => {
    const enter = !reduced && !(entryId !== undefined && entered.has(entryId));
    return { id: entryId, enter, shown: new Animated.Value(enter ? 0 : 1) };
  };
  const [entry, setEntry] = useState(start);
  if (entry.id !== entryId) setEntry(start());
  // Once per row: streamed text re-renders the row but never replays the entrance.
  useEffect(() => {
    const { id, enter, shown } = entry;
    if (id !== undefined) entered.add(id);
    if (reduced || !enter) {
      shown.setValue(1);
      return;
    }
    const animation = Animated.timing(shown, {
      toValue: 1,
      duration: ENTRY_MS,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    animation.start();
    return () => animation.stop();
  }, [entry, reduced]);
  const bubbleBg = mine ? palette.ink : palette.cardShade;
  return (
    <Animated.View
      style={[
        styles.row,
        mine && styles.rowMine,
        {
          opacity: entry.shown,
          transform: [
            {
              translateY: entry.shown.interpolate({
                inputRange: [0, 1],
                outputRange: [ENTRY_RISE, 0],
              }),
            },
          ],
        },
      ]}
    >
      <View style={[styles.column, mine && styles.columnMine, fill && styles.columnFill]}>
        {above}
        {children != null ? (
          <View
            style={[
              styles.line,
              above != null && styles.lineAfterAbove,
              accessory != null && styles.lineWithSource,
              fill && styles.lineFill,
            ]}
          >
            <View
              style={[
                styles.bubble,
                mine ? styles.mine : styles.theirs,
                {
                  backgroundColor: bubbleBg,
                  borderWidth: !mine && highContrast ? 1 : 0,
                  borderColor: palette.ink,
                },
                accessory != null && styles.bubbleWithSource,
                fill && styles.bubbleFill,
              ]}
            >
              {children}
              <Svg
                width={11}
                height={11}
                viewBox="0 0 11 11"
                style={[styles.join, mine ? styles.joinMine : styles.joinTheirs]}
                pointerEvents="none"
              >
                <Path
                  d={mine ? 'M0 0H1A10 10 0 0 0 11 10V11H0Z' : 'M11 0H10A10 10 0 0 1 0 10V11H11Z'}
                  fill={bubbleBg}
                />
              </Svg>
            </View>
            {accessory}
          </View>
        ) : null}
        {meta ? (
          <View
            style={[
              styles.metaRow,
              mine && styles.metaRowMine,
              accessory != null && styles.metaRowWithSource,
            ]}
          >
            <Icon name="clock" size={12} color={palette.inkMuted} strokeWidth={2} />
            <Text
              style={[
                styles.meta,
                {
                  color: palette.inkMuted,
                  fontSize: scaleSize(12, textScale),
                  lineHeight: scaleSize(16, textScale),
                },
              ]}
            >
              {meta}
            </Text>
          </View>
        ) : null}
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', paddingHorizontal: ROW_PADDING, paddingVertical: 8 },
  photoFrame: { maxWidth: '100%', borderRadius: 18, overflow: 'hidden' },
  photo: { width: '100%', height: '100%' },
  rowMine: { flexDirection: 'row-reverse' },
  column: { flexShrink: 1, maxWidth: `${COLUMN_SHARE * 100}%`, alignItems: 'flex-start' },
  columnMine: { alignItems: 'flex-end' },
  columnFill: { width: `${COLUMN_SHARE * 100}%` },
  line: { flexDirection: 'row', alignItems: 'flex-end' },
  lineAfterAbove: { marginTop: 6 },
  // Leaves room under the bubble's bottom edge for the overlaid sources badge to sit cleanly.
  lineWithSource: { paddingBottom: 14 },
  lineFill: { alignSelf: 'stretch' },
  bubble: {
    flexShrink: 1,
    borderRadius: 22,
    paddingHorizontal: BUBBLE_PADDING,
    paddingVertical: 13,
  },
  bubbleWithSource: { paddingBottom: 22, minWidth: 148 },
  // flexBasis 0: the line's width, whatever the photos inside would ask for.
  bubbleFill: { flex: 1, paddingRight: BUBBLE_PADDING },
  theirs: { backgroundColor: brand.cardShade, borderBottomLeftRadius: 0 },
  mine: { backgroundColor: brand.ink, borderBottomRightRadius: 0 },
  join: { position: 'absolute', bottom: 0 },
  joinTheirs: { left: -10 },
  joinMine: { right: -10 },
  theirsText: { ...type.body, color: brand.ink },
  bold: { fontFamily: fonts.bold },
  paragraphGap: { marginTop: spacing.sm },
  item: { flexDirection: 'row' },
  itemGap: { marginTop: spacing.xs },
  marker: { minWidth: 18, marginRight: spacing.xs },
  itemText: { flexShrink: 1 },
  mineText: { ...type.body, color: brand.onPrimary },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginTop: 6,
    marginLeft: 4,
  },
  metaRowWithSource: {
    marginTop: 2,
  },
  metaRowMine: {
    marginLeft: 0,
    marginRight: 4,
  },
  meta: {
    ...type.caption,
    fontSize: 12,
    lineHeight: 16,
    color: brand.inkMuted,
    fontVariant: ['tabular-nums'],
  },
  accessories: {
    position: 'absolute',
    right: 14,
    bottom: 0,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  speakBadge: {
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    boxShadow: `0 2px 8px ${brand.glow}`,
    outlineColor: brand.primary,
  },
  sourceBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingLeft: 5,
    paddingRight: 10,
    paddingVertical: 4,
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    boxShadow: `0 2px 8px ${brand.glow}`,
    outlineColor: brand.primary,
  },
  sourceBadgePressed: {
    backgroundColor: brand.cardShade,
    borderColor: brand.primary,
  },
  faviconStack: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sourceLabel: {
    ...type.caption,
    fontFamily: fonts.semibold,
    fontSize: 12,
    lineHeight: 16,
    color: brand.ink,
  },
});
