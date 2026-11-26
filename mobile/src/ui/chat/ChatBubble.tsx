// Quiet message surfaces. A concave foot grounds each bubble on its side of the conversation; an
// assistant answer with sources gets a small round button over its other bottom corner.
import { memo, useEffect, useMemo, useState, type ReactNode } from 'react';
import { Animated, Easing, Pressable, StyleSheet, Text, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { fill, t } from '@/i18n';

import { Icon } from '../icons/Icon';
import { brand, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

import { parseCitations, type ChatSource } from './citations';

export interface ChatBubbleProps {
  role: 'user' | 'assistant';
  /** As written; an assistant's citation markers are hidden, the user's words shown as typed. */
  text: string;
  meta?: string;
  /** Assistant only: what the answer rests on, opened by the corner button. */
  sources?: ChatSource[];
  onOpenSources?: (sources: ChatSource[]) => void;
}

/** A slow, short rise: the message settles in instead of popping. */
const ENTRY_MS = 280;
const ENTRY_RISE = 4;

export const ChatBubble = memo(function ChatBubble({
  role,
  text,
  meta,
  sources,
  onOpenSources,
}: ChatBubbleProps) {
  const mine = role === 'user';
  const shown = useMemo(() => (mine ? text : parseCitations(text).prose), [mine, text]);
  const cited = !mine && sources?.length ? sources : null;
  return (
    <BubbleRow
      role={role}
      meta={meta}
      accessory={
        cited && onOpenSources ? (
          <SourceButton count={cited.length} onPress={() => onOpenSources(cited)} />
        ) : null
      }
    >
      <Text style={mine ? styles.mineText : styles.theirsText} selectable>
        {shown}
      </Text>
    </BubbleRow>
  );
});

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
  children,
}: {
  role: 'user' | 'assistant';
  meta?: string;
  /** Overlaid on the bubble's bottom corner, opposite its foot. */
  accessory?: ReactNode;
  children: ReactNode;
}) {
  const mine = role === 'user';
  const reduced = useReducedMotion();
  const [entry] = useState(() => new Animated.Value(reduced ? 1 : 0));
  // Once per mount: streamed text re-renders the row but never replays the entrance.
  useEffect(() => {
    if (reduced) {
      entry.setValue(1);
      return;
    }
    const animation = Animated.timing(entry, {
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
          opacity: entry,
          transform: [
            { translateY: entry.interpolate({ inputRange: [0, 1], outputRange: [ENTRY_RISE, 0] }) },
          ],
        },
      ]}
    >
      <View style={[styles.column, mine && styles.columnMine]}>
        <View style={[styles.line, accessory != null && styles.lineWithSource]}>
          <View style={[styles.bubble, mine ? styles.mine : styles.theirs, accessory != null && styles.bubbleWithSource]}>
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
  row: { flexDirection: 'row', paddingHorizontal: 22, paddingVertical: 8 },
  rowMine: { flexDirection: 'row-reverse' },
  column: { flexShrink: 1, maxWidth: '88%', alignItems: 'flex-start' },
  columnMine: { alignItems: 'flex-end' },
  line: { flexDirection: 'row', alignItems: 'flex-end' },
  // Keep the overlaid 44 pt target inside the row so native hit testing can reach all of it.
  lineWithSource: { paddingRight: 22, paddingBottom: 14 },
  bubbleWithSource: { paddingRight: 28, paddingBottom: 24 },
  bubble: { flexShrink: 1, borderRadius: 22, paddingHorizontal: 17, paddingVertical: 13 },
  theirs: { backgroundColor: brand.cardShade, borderBottomLeftRadius: 0 },
  mine: { backgroundColor: brand.ink, borderBottomRightRadius: 0 },
  join: { position: 'absolute', bottom: 0 },
  joinTheirs: { left: -10 },
  joinMine: { right: -10 },
  theirsText: { ...type.body, color: brand.ink },
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
