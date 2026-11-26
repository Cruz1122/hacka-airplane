// Quiet message surfaces. A concave foot grounds each bubble on its side of the conversation; an
// assistant answer with sources gets a small round button over its other bottom corner. Assistant
// text is a small Markdown subset (markdown.ts) with its keywords in bold, typed out word by word
// (reveal.ts) unless motion is reduced or a screen reader is on.
import { memo, useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  Animated,
  Easing,
  Pressable,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';

import type { MediaPick } from '@/core/media/media';
import { fill, t } from '@/i18n';

import { Icon } from '../icons/Icon';
import { brand, fonts, spacing, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

import type { ChatSource } from './citations';
import { replyDoc, sliceDoc, type Block } from './markdown';
import { MediaGallery } from './MediaGallery';
import { useRevealedWords } from './reveal';
import { useScreenReader } from './useScreenReader';

export interface ChatBubbleProps {
  role: 'user' | 'assistant';
  /** As written; an assistant's citation markers are hidden, the user's words shown as typed. */
  text: string;
  meta?: string;
  /** Assistant only: what the answer rests on, opened by the corner button. */
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
const NO_KEYWORDS: readonly string[] = [];
/** The row's side margins, a bubble's share of what is left, and its padding (styles below). */
const ROW_PADDING = 22;
const COLUMN_SHARE = 0.88;
const BUBBLE_PADDING = 17;
/** The line's room for the source button beside a bubble's corner. */
const SOURCE_GUTTER = 22;

/**
 * A photo bubble's inner width as the window predicts it, for its gallery's first frame. The
 * gallery then measures itself: inside a narrower frame (the chat's centred column on a wide
 * screen, the design catalog) it settles one layout later.
 */
const predictedGalleryWidth = (screen: number, sourced: boolean) =>
  Math.floor(COLUMN_SHARE * (screen - 2 * ROW_PADDING)) -
  (sourced ? SOURCE_GUTTER : 0) -
  2 * BUBBLE_PADDING;

/** Row ids whose bubble has entered, or that were on screen before; FlashList reuses cells. */
const entered = new Set<string>();

/** Rows the reader has already seen show without an entry. */
export function markEntered(ids: Iterable<string>) {
  for (const id of ids) entered.add(id);
}

export const ChatBubble = memo(function ChatBubble({
  role,
  text,
  meta,
  sources,
  onOpenSources,
  keywords = NO_KEYWORDS,
  revealId,
  entryId,
  media,
}: ChatBubbleProps) {
  const mine = role === 'user';
  const reduced = useReducedMotion();
  const reader = useScreenReader();
  const doc = useMemo(() => (mine ? null : replyDoc(text, keywords)), [mine, text, keywords]);
  const streamId = mine || reduced || reader ? undefined : revealId;
  const words = useRevealedWords(streamId);
  const screen = useWindowDimensions().width;
  // Waiting for its turn (a banner is still typing out) or for the chat to schedule it.
  if (words === 0) return null;
  const done = !doc || words >= doc.stops.length;
  const cited = !mine && sources?.length ? sources : null;
  const sourced = cited !== null && onOpenSources !== undefined;
  const gallery = mine ? undefined : media;
  return (
    <BubbleRow
      role={role}
      entryId={entryId}
      meta={done ? meta : undefined}
      fill={gallery !== undefined}
      accessory={
        sourced ? (
          done ? (
            <SourceButton count={cited.length} onPress={() => onOpenSources(cited)} />
          ) : (
            // The button's room, kept while the text arrives so its lines never re-wrap.
            <View style={styles.source} pointerEvents="none" />
          )
        ) : null
      }
    >
      {doc ? (
        <Reply blocks={done ? doc.blocks : sliceDoc(doc, doc.stops[words - 1])} label={doc.text} />
      ) : (
        <Text style={styles.mineText} selectable>
          {text}
        </Text>
      )}
      {gallery ? (
        <MediaGallery
          key={entryId}
          media={gallery}
          width={predictedGalleryWidth(screen, sourced)}
          revealId={streamId}
        />
      ) : null}
    </BubbleRow>
  );
});

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
  return b.marker === null ? (
    <Text style={[styles.theirsText, !first && styles.paragraphGap]} selectable>
      {spans(b)}
    </Text>
  ) : (
    <View style={[styles.item, !first && styles.itemGap]}>
      <Text style={[styles.theirsText, styles.marker]}>{b.marker}</Text>
      <Text style={[styles.theirsText, styles.itemText]} selectable>
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

/** A 44 pt target around a small ring, so it needs no hitSlop past the row's bounds. */
function SourceButton({ count, onPress }: { count: number; onPress: () => void }) {
  const copy = t.chatScreen.sources;
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={count === 1 ? copy.showOne : fill(copy.showMany, { n: count })}
      style={styles.source}
    >
      {({ pressed }) => (
        <View style={[styles.sourceRing, pressed && styles.sourceRingPressed]}>
          <Icon name="bookOpen" size={14} color={brand.ink} strokeWidth={2.2} />
        </View>
      )}
    </Pressable>
  );
}

export function BubbleRow({
  role,
  meta,
  accessory,
  entryId,
  fill = false,
  children,
}: {
  role: 'user' | 'assistant';
  meta?: string;
  /** Overlaid on the bubble's bottom corner, opposite its foot. */
  accessory?: ReactNode;
  /** See ChatBubbleProps.entryId. */
  entryId?: string;
  /**
   * The bubble takes its whole share of the row (photos span it), sized by the row and never by
   * its content, with even sides: the source button sits in the bottom padding, below the photos.
   */
  fill?: boolean;
  children: ReactNode;
}) {
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
      useNativeDriver: true,
    });
    animation.start();
    return () => animation.stop();
  }, [entry, reduced]);
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
        <View
          style={[styles.line, accessory != null && styles.lineWithSource, fill && styles.lineFill]}
        >
          <View
            style={[
              styles.bubble,
              mine ? styles.mine : styles.theirs,
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
                fill={mine ? brand.ink : brand.cardShade}
              />
            </Svg>
          </View>
          {accessory}
        </View>
        {meta ? <Text style={[styles.meta, mine && styles.metaMine]}>{meta}</Text> : null}
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', paddingHorizontal: ROW_PADDING, paddingVertical: 8 },
  rowMine: { flexDirection: 'row-reverse' },
  column: { flexShrink: 1, maxWidth: `${COLUMN_SHARE * 100}%`, alignItems: 'flex-start' },
  columnMine: { alignItems: 'flex-end' },
  columnFill: { width: `${COLUMN_SHARE * 100}%` },
  line: { flexDirection: 'row', alignItems: 'flex-end' },
  // Keep the overlaid 44 pt target inside the row so native hit testing can reach all of it.
  lineWithSource: { paddingRight: SOURCE_GUTTER, paddingBottom: 14 },
  lineFill: { alignSelf: 'stretch' },
  bubbleWithSource: { paddingRight: 28, paddingBottom: 24 },
  bubble: {
    flexShrink: 1,
    borderRadius: 22,
    paddingHorizontal: BUBBLE_PADDING,
    paddingVertical: 13,
  },
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
  meta: { ...type.caption, color: brand.inkMuted, marginTop: 6, marginLeft: 4 },
  metaMine: { marginLeft: 0, marginRight: 4 },
  source: {
    width: 44,
    height: 44,
    position: 'absolute',
    right: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 22,
    outlineColor: brand.primary,
  },
  sourceRing: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
  },
  sourceRingPressed: { backgroundColor: brand.cardShade },
});
