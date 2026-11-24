// The chat screen as plain props (app/index.tsx wires it to the assistant), so the design catalog
// can show every state on web, where the model never loads.
import { FlashList } from '@shopify/flash-list';
import {
  type RefObject,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from 'react';
import {
  Animated,
  Easing,
  Keyboard,
  type LayoutChangeEvent,
  type NativeScrollEvent,
  type NativeSyntheticEvent,
  Platform,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Defs, LinearGradient, Rect, Stop } from 'react-native-svg';

import type { StepResult } from '@/core/driver';
import { fill, t } from '@/i18n';
import { ChatBubble } from '@/ui/chat/ChatBubble';
import type { ChatSource } from '@/ui/chat/citations';
import { ChatComposer, DOCK } from '@/ui/chat/ChatComposer';
import { ChatMenu } from '@/ui/chat/ChatMenu';
import { keywordsFor } from '@/ui/chat/keywords';
import { replyReveal } from '@/ui/chat/reveal';
import { SourcesSheet } from '@/ui/chat/SourcesSheet';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { DebugPanel } from '@/ui/DebugPanel';
import { PET_NAME, type VoiceState } from '@/ui/pet/petCore';
import { brand, type } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

import { ChatBackdrop } from './ChatBackdrop';
import { headerScene } from './headerScene';
import { chatLayout } from './chatLayout';
import { GazeChannel } from './gaze';
import { PetCircle } from './PetCircle';
import { useChatKeyboard } from './useChatKeyboard';

export interface ChatRow {
  id: string;
  role: 'user' | 'assistant';
  /** As written, citation markers included (the bubble hides them). */
  text: string;
  /** The catalog entry whose `short` this text is; picks the keywords set in bold. */
  entryId?: string;
  latencyMs?: number;
  /** Validated references of an assistant reply; none means no source button. */
  sources?: ChatSource[];
}

export interface ChatModel {
  id: string;
  status: 'missing' | 'loading' | 'ready' | 'error';
  error?: string;
}

export interface ChatViewProps {
  messages: ChatRow[];
  busy: boolean;
  /** Live model output of the routing step, for the debug view. */
  draft: string;
  model: ChatModel;
  steps: StepResult[];
  state: string;
  /** Idle-motion time of the backdrop (from the onboarding), or null for its rest pose. */
  sceneTime: number | null;
  /** Fade the conversation in: the onboarding just handed over the header (see handoff.ts). */
  fadeIn?: boolean;
  onSend: (text: string) => void;
  onReset: () => void;
  onSettings: () => void;
  onHistory: () => void;
}

const MAX_COLUMN = 720;
const keyExtractor = (m: ChatRow) => m.id;
const greeting = (
  <ChatBubble role="assistant" text={fill(t.chatScreen.greeting, { pet: PET_NAME })} />
);

/** Messages scrolling up melt into the sheet instead of being cut at the list's edge. */
function TopFade() {
  return (
    // Sized by its wrapper: a bare absolute <svg> on web keeps its intrinsic 300 px width.
    <View style={styles.fade} pointerEvents="none">
      <Svg width="100%" height="100%">
        <Defs>
          <LinearGradient id="chat-top-fade" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor={brand.card} stopOpacity={1} />
            <Stop offset="1" stopColor={brand.card} stopOpacity={0} />
          </LinearGradient>
        </Defs>
        <Rect width="100%" height="100%" fill="url(#chat-top-fade)" />
      </Svg>
    </View>
  );
}

/**
 * Rows on screen when the chat mounts show whole (read before, or arrived while it was away); each
 * later assistant row types itself out after the one before it.
 */
function useReplyReveal(messages: ChatRow[]): ReadonlySet<string> {
  const [seen] = useState(() => new Set(messages.map((m) => m.id)));
  // Before paint, in data order: a banner always types out before its reply.
  useLayoutEffect(() => replyReveal.schedule(messages, seen, performance.now()), [messages, seen]);
  return seen;
}

/**
 * What the Pet is doing: thinking while an answer is worked out, then talking while it types
 * itself out (a reply not scheduled yet counts, unless it was there when the chat mounted).
 */
function usePetVoice(messages: ChatRow[], busy: boolean, seen: ReadonlySet<string>): VoiceState {
  const last = messages.at(-1);
  const id = last?.role === 'assistant' ? last.id : undefined;
  const read = () => id !== undefined && (replyReveal.revealing(id) ?? !seen.has(id));
  const talking = useSyncExternalStore(replyReveal.subscribe, read, read);
  if (talking) return 'speaking';
  return busy ? 'thinking' : 'idle';
}

function statusText(model: ChatModel): string | null {
  if (model.status === 'ready') return null;
  if (model.status === 'loading') return t.modelLoading;
  const detail =
    model.status === 'missing'
      ? `${t.modelMissing}: ${model.id}`
      : `${t.modelError}: ${model.error ?? ''}`;
  // The real cause stays visible; on web it is expected, so say so first.
  return Platform.OS === 'web' ? `${t.chatScreen.webNoModel}\n${detail}` : detail;
}

/**
 * The view's size, plus the tallest height seen at that width. The header is laid out from the
 * tallest, so the keyboard shrinking the screen never moves (and redraws) the Nevado, while the
 * composer follows the real height. Measured, not read from the window: on Android the keyboard
 * resizes the screen's container, not necessarily the window.
 */
function useChatSize() {
  // The window is the first guess (the chat fills the screen), so the first frame is already
  // drawn; an empty one flashed between the onboarding's handoff and the chat.
  const window = useWindowDimensions();
  const [size, setSize] = useState(() => ({
    width: window.width,
    height: window.height,
    tall: window.height,
    measured: false,
  }));
  // The view's bottom edge in window coordinates: what the keyboard's top is compared against.
  const root = useRef<React.ComponentRef<typeof View>>(null);
  const [bottom, setBottom] = useState(window.height);
  const onLayout = useCallback((e: LayoutChangeEvent) => {
    const { width, height } = e.nativeEvent.layout;
    setSize((s) => ({
      width,
      height,
      // The first measure replaces the window guess (the view may be shorter than the window).
      tall: s.measured && width === s.width ? Math.max(s.tall, height) : height,
      measured: true,
    }));
    root.current?.measureInWindow((_x, y, _w, h) => setBottom(y + h));
  }, []);
  return { ...size, bottom, root, onLayout };
}

export function ChatView(p: ChatViewProps) {
  const { width, tall, bottom, root, onLayout } = useChatSize();
  return (
    <View ref={root} style={styles.root} onLayout={onLayout}>
      <ChatContent {...p} width={width} tall={tall} viewBottom={bottom} />
    </View>
  );
}

/**
 * Android reports its keyboard with no duration, so the motion follows the IME's own unsynced
 * animation (AOSP InsetsController: 200 ms, linear-out-slow-in shown, fast-out-linear-in hidden).
 * Not tuned on the phone yet.
 */
const KEYBOARD_IN = { duration: 200, easing: Easing.bezier(0, 0, 0.2, 1) };
const KEYBOARD_OUT = { duration: 200, easing: Easing.bezier(0.4, 0, 1, 1) };

/**
 * Follows the keyboard with transforms on the native driver, so no frame lays anything out: the
 * composer rises by the whole occlusion, the sheet, circle and conversation by at most `maxRise`.
 * The list instead gets end padding for the part of it the composer then covers, so its last
 * row can scroll above the composer.
 */
function useKeyboardMotion(occlusion: number, maxRise: number) {
  const still = useReducedMotion();
  const rise = Math.min(occlusion, maxRise);
  const covered = occlusion - rise;
  const [composerY] = useState(() => new Animated.Value(-occlusion));
  const [sheetY] = useState(() => new Animated.Value(-rise));
  // A closing keyboard's padding stays until the composer is down: dropped at once, the scroll
  // offset would clamp and the rows would jump down by it in one frame.
  const [pad, setPad] = useState({ covered, held: 0 });
  if (pad.covered !== covered) {
    const held = covered < pad.covered && !still ? Math.max(pad.covered, pad.held) : 0;
    setPad({ covered, held });
  }
  useEffect(() => {
    if (still) {
      composerY.setValue(-occlusion);
      sheetY.setValue(-rise);
      return;
    }
    const curve = occlusion > 0 ? KEYBOARD_IN : KEYBOARD_OUT;
    const anim = Animated.parallel([
      Animated.timing(composerY, { toValue: -occlusion, ...curve, useNativeDriver: true }),
      Animated.timing(sheetY, { toValue: -rise, ...curve, useNativeDriver: true }),
    ]);
    anim.start(({ finished }) => {
      if (finished) setPad((p) => (p.held ? { ...p, held: 0 } : p));
    });
    return () => anim.stop();
  }, [occlusion, rise, still, composerY, sheetY]);
  return {
    composerY,
    sheetY,
    listPad: Math.max(pad.covered, pad.held),
    /** Padding about to go once the keyboard is down (0 when none is). */
    dropping: Math.max(0, pad.held - pad.covered),
  };
}

/** Within this many points of its end the list counts as at the end. */
const NEAR_END = 24;
/** How long our own scroll back may report offsets moving up (Android smooth scroll: 250 ms). */
const OWN_SCROLL_MS = 400;

type ListRef = RefObject<React.ComponentRef<typeof FlashList<ChatRow>> | null>;

/**
 * Keeps the newest row in view while the reader is at the end, with one scroll per frame however
 * often the content grows: while a reply types out each new line jumps into view, as an animated
 * scroll per line would stack. Reading back (dragging, or the offset moving up away from the end)
 * stops it until the reader is near the end again or sends a message.
 */
function useListFollow(list: ListRef) {
  const following = useRef(true);
  const dragging = useRef(false);
  const scroll = useRef({ offset: 0, ownUntil: -Infinity });
  const frame = useRef<number | null>(null);
  useEffect(
    () => () => {
      if (frame.current !== null) cancelAnimationFrame(frame.current);
    },
    [],
  );
  const toEnd = useCallback(() => {
    if (!following.current || dragging.current || frame.current !== null) return;
    frame.current = requestAnimationFrame(() => {
      frame.current = null;
      list.current?.scrollToEnd({ animated: !replyReveal.busy() });
    });
  }, [list]);
  return useMemo(
    () => ({
      toEnd,
      /** The reader's own message: follow it whatever they were reading. */
      rearm: () => {
        following.current = true;
      },
      /**
       * End padding of `px` is about to go. At the end, scroll back by it now, so the rows move
       * down with the composer instead of dropping when the padding goes and the offset clamps.
       */
      release: (px: number) => {
        const s = scroll.current;
        if (!following.current || s.offset <= 0) return;
        s.ownUntil = performance.now() + OWN_SCROLL_MS;
        list.current?.scrollToOffset({ offset: Math.max(0, s.offset - px), animated: true });
      },
      onScroll: (e: NativeSyntheticEvent<NativeScrollEvent>) => {
        const { contentOffset, contentSize, layoutMeasurement } = e.nativeEvent;
        const s = scroll.current;
        const offset = contentOffset.y;
        if (contentSize.height - layoutMeasurement.height - offset <= NEAR_END) {
          following.current = true;
        } else if (offset < s.offset - 1 && performance.now() > s.ownUntil) {
          // Web has no drag events for a wheel or a scrollbar.
          following.current = false;
        }
        s.offset = offset;
      },
      onScrollBeginDrag: () => {
        dragging.current = true;
        following.current = false;
      },
      onScrollEndDrag: () => {
        dragging.current = false;
      },
    }),
    [list, toEnd],
  );
}

function ChatContent(p: ChatViewProps & { width: number; tall: number; viewBottom: number }) {
  const { tall } = p;
  const insets = useSafeAreaInsets();
  const keyboard = useChatKeyboard(p.viewBottom);
  const [gaze] = useState(() => new GazeChannel());
  const layout = useMemo(
    () => chatLayout(headerScene, p.width, tall, { top: insets.top, bottom: insets.bottom }),
    [p.width, tall, insets.top, insets.bottom],
  );
  const [debug, setDebug] = useState(false);
  // One sheet for the screen: the bubbles only say which sources to list.
  const [sheet, setSheet] = useState<ChatSource[] | null>(null);
  const openSheet = useCallback((sources: ChatSource[]) => {
    Keyboard.dismiss(); // the sheet rises from the bottom edge, where the keyboard would cover it
    setSheet(sources);
  }, []);
  const closeSheet = useCallback(() => setSheet(null), []);
  const renderItem = useCallback(
    ({ item }: { item: ChatRow }) => (
      <ChatBubble
        role={item.role}
        text={item.text}
        keywords={keywordsFor(item.entryId)}
        revealId={item.role === 'assistant' ? item.id : undefined}
        sources={item.sources}
        onOpenSources={openSheet}
        meta={
          item.latencyMs != null
            ? fill(t.chatScreen.seconds, { s: (item.latencyMs / 1000).toFixed(1) })
            : undefined
        }
      />
    ),
    [openSheet],
  );
  const list = useRef<React.ComponentRef<typeof FlashList<ChatRow>>>(null);
  const follow = useListFollow(list);
  // Keyboard open: the mist, the circle and the conversation rise over the ranges together.
  const motion = useKeyboardMotion(keyboard.bottom, layout.keyboardLift);
  const { release, toEnd } = follow;
  useEffect(() => {
    if (motion.dropping > 0) release(motion.dropping);
  }, [motion.dropping, release]);
  // The end padding moved the end (a web ScrollView reports no content size change for padding).
  useEffect(toEnd, [motion.listPad, toEnd]);
  const listContent = useMemo(
    () => [styles.listContent, { paddingBottom: motion.listPad }],
    [motion.listPad],
  );
  const { onSend } = p;
  const send = useCallback(
    (text: string) => {
      follow.rearm();
      onSend(text);
    },
    [follow, onSend],
  );
  const seen = useReplyReveal(p.messages);
  const voice = usePetVoice(p.messages, p.busy, seen);
  const [shown] = useState(() => new Animated.Value(p.fadeIn ? 0 : 1));
  useEffect(() => {
    if (!p.fadeIn) return;
    const anim = Animated.timing(shown, { toValue: 1, duration: 280, useNativeDriver: true });
    anim.start();
    return () => anim.stop();
  }, [p.fadeIn, shown]);
  const status = statusText(p.model);
  const ready = p.model.status === 'ready';
  // The docked composer's base strip covers the home indicator, so the sheet needs no padding.
  const floor = keyboard.open ? DOCK.floor : Math.max(insets.bottom, DOCK.floor);
  return (
    <>
      <ChatBackdrop
        width={p.width}
        height={tall}
        layout={layout}
        time={p.sceneTime}
        rise={motion.sheetY}
      />
      <Animated.View
        style={[StyleSheet.absoluteFill, { transform: [{ translateY: motion.sheetY }] }]}
        pointerEvents="none"
      >
        <PetCircle
          x={layout.circle.x}
          y={layout.circle.y}
          r={layout.circle.r}
          voice={voice}
          ready={ready}
          gaze={gaze}
        />
      </Animated.View>
      <Animated.View style={[StyleSheet.absoluteFill, { opacity: shown }]} pointerEvents="box-none">
        <View style={[styles.body, { top: layout.listTop }]}>
          <Animated.View
            style={[styles.conversation, { transform: [{ translateY: motion.sheetY }] }]}
          >
            {status && (
              <View style={styles.column}>
                <Text style={styles.status} numberOfLines={3}>
                  {status}
                </Text>
              </View>
            )}
            <View style={[styles.column, styles.list]}>
              <FlashList
                ref={list}
                data={p.messages}
                renderItem={renderItem}
                keyExtractor={keyExtractor}
                ListHeaderComponent={greeting}
                ListFooterComponent={
                  p.busy ? (
                    <TypingBubble
                      label={fill(t.chatScreen.typing, { pet: PET_NAME })}
                      detail={debug ? p.draft || t.thinking : undefined}
                    />
                  ) : null
                }
                onContentSizeChange={follow.toEnd}
                onScroll={follow.onScroll}
                onScrollBeginDrag={follow.onScrollBeginDrag}
                onScrollEndDrag={follow.onScrollEndDrag}
                keyboardShouldPersistTaps="handled"
                contentContainerStyle={listContent}
              />
              <TopFade />
            </View>
          </Animated.View>
          <Animated.View style={{ transform: [{ translateY: motion.composerY }] }}>
            {debug && (
              <View style={styles.column}>
                <DebugPanel steps={p.steps} state={p.state} />
              </View>
            )}
            <View>
              {/* Past the reading column the base strip still runs along the whole bottom edge,
                  and a screen further down, so no row shows under the composer as it rises. */}
              <View style={[styles.dockBase, { height: floor + 1 + tall, bottom: -tall }]} />
              <View style={styles.column}>
                <ChatComposer
                  variant="docked"
                  floor={floor}
                  disabled={p.busy || !ready}
                  placeholder={t.inputPlaceholder}
                  sendLabel={t.send}
                  onSend={send}
                  onCaret={gaze.set}
                />
              </View>
            </View>
          </Animated.View>
        </View>
        <ChatMenu
          label={t.chatScreen.more}
          top={insets.top + 10}
          right={insets.right + 16}
          items={[
            { label: t.chatScreen.newChat, onPress: p.onReset },
            { label: t.history, onPress: p.onHistory },
            { label: t.settings, onPress: p.onSettings },
            {
              label: debug ? t.chatScreen.debugHide : t.chatScreen.debugShow,
              onPress: () => setDebug((d) => !d),
            },
          ]}
        />
        <SourcesSheet sources={sheet} onClose={closeSheet} bottom={insets.bottom} />
      </Animated.View>
    </>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.sky, overflow: 'hidden' },
  body: { position: 'absolute', left: 0, right: 0, bottom: 0 },
  // Tablets keep a phone-like reading column under the wide header.
  column: { width: '100%', maxWidth: MAX_COLUMN, alignSelf: 'center' },
  list: { flex: 1 },
  conversation: { flex: 1 },
  dockBase: { position: 'absolute', left: 0, right: 0, backgroundColor: brand.cardShade },
  listContent: { paddingTop: 10 },
  fade: { position: 'absolute', top: 0, left: 0, right: 0, height: 22 },
  status: {
    ...type.caption,
    color: brand.inkMuted,
    textAlign: 'center',
    marginHorizontal: 24,
    marginBottom: 4,
  },
});
