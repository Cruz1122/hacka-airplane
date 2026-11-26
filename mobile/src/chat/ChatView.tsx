// The chat screen as plain props (app/index.tsx wires it to the assistant), so the design catalog
// can show every state on web, where the model never loads.
import { FlashList } from '@shopify/flash-list';
import {
  type ReactNode,
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
  useWindowDimensions,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Defs, LinearGradient, Rect, Stop } from 'react-native-svg';

import type { MediaPick } from '@/core/media/media';
import { fill, t } from '@/i18n';
import { ChatBubble, markEntered } from '@/ui/chat/ChatBubble';
import type { ChatSource } from '@/ui/chat/citations';
import { ChatComposer, DOCK } from '@/ui/chat/ChatComposer';
import { keywordsFor } from '@/ui/chat/keywords';
import { revealRows } from '@/ui/chat/MediaGallery';
import { replyReveal } from '@/ui/chat/reveal';
import { SourcesSheet } from '@/ui/chat/SourcesSheet';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { useChatNavFade } from '@/ui/AppNavBar';
import { VAPOR_BODY_TOP } from '@/ui/CloudCard';
import { NAV_BAR_HEIGHT } from '@/ui/CloudNavBar';
import { PET_NAME, type VoiceState } from '@/ui/pet/petCore';
import { brand } from '@/ui/theme/tokens';
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
  photoUri?: string;
  /** The catalog entry whose `short` this text is; picks the keywords set in bold. */
  entryId?: string;
  keywords?: readonly string[];
  latencyMs?: number;
  /** Validated references of an assistant reply; none means no source button. */
  sources?: ChatSource[];
  /** Photos under an answer, decided once when it arrived (src/core/media). */
  media?: MediaPick;
}

export interface ChatModel {
  id: string;
  status: 'missing' | 'loading' | 'ready' | 'error';
  error?: string;
}

export interface ChatViewProps {
  messages: ChatRow[];
  busy: boolean;
  model: ChatModel;
  /** Idle-motion time of the backdrop (from the onboarding), or null for its rest pose. */
  sceneTime: number | null;
  /** Fade the conversation in: the onboarding just handed over the header (see handoff.ts). */
  fadeIn?: boolean;
  onSend: (text: string) => void;
  onPhoto?: () => void;
  photoUri?: string;
  onRemovePhoto?: () => void;
  /** Starts a new conversation. */
  onReset: () => void;
  /** The cloud navigation bar, drawn over the header and under the sources sheet. */
  nav?: ReactNode;
}

const MAX_COLUMN = 720;
/** Points the sheet rises before the navigation bar is fully faded out. */
const NAV_FADE = 60;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
/** Scroll thresholds (with hysteresis) to raise the mist in a long chat and bring mountains back. */
const COLLAPSE_AT = 48;
const EXPAND_AT = 16;
const COLLAPSE_MIN_OVERFLOW = 36;
const MIST_COLLAPSE = { duration: 240, easing: Easing.out(Easing.cubic) };
const FLASHLIST_DISABLE_MVCP = { disabled: true } as const;
const keyExtractor = (m: ChatRow) => m.id;
const greeting = (
  <ChatBubble
    role="assistant"
    text={fill(t.chatScreen.greeting, { pet: PET_NAME })}
    keywords={t.chatScreen.greetingKeywords.map((keyword) => fill(keyword, { pet: PET_NAME }))}
  />
);

/** Formats response time without rounding fast offline answers down to "0.0 s". */
export function formatLatency(ms: number): string {
  const rounded = Math.max(1, Math.round(ms));
  if (rounded < 1000) return fill(t.chatScreen.milliseconds, { ms: rounded });
  return fill(t.chatScreen.seconds, { s: (rounded / 1000).toFixed(1) });
}

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
 * Rows on screen when the chat mounts show whole and without an entry (read before, or arrived
 * while it was away); each later assistant row types itself out after the one before it.
 */
function useReplyReveal(messages: ChatRow[]): ReadonlySet<string> {
  const [seen] = useState(() => {
    markEntered(messages.map((m) => m.id));
    return new Set(revealRows(messages).map((r) => r.id));
  });
  // Before paint, in data order: a banner always types out before its reply, photo captions after.
  useLayoutEffect(
    () => replyReveal.schedule(revealRows(messages), seen, performance.now()),
    [messages, seen],
  );
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
 * Android reports its keyboard with no duration. AOSP's InsetsController runs an IME animation the
 * app does not drive in 200 ms; the curves (decelerate in, accelerate out) are a guess, not yet
 * tuned against the A24's keyboard.
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
      Animated.timing(composerY, {
        toValue: -occlusion,
        ...curve,
        useNativeDriver: USE_NATIVE_DRIVER,
      }),
      Animated.timing(sheetY, { toValue: -rise, ...curve, useNativeDriver: USE_NATIVE_DRIVER }),
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
function useListFollow(
  list: ListRef,
  onScrollMetrics?: (offset: number, contentHeight: number, viewportHeight: number) => void,
) {
  const following = useRef(true);
  const dragging = useRef(false);
  const scroll = useRef({ offset: 0, gap: 0, ownUntil: -Infinity });
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
      // Re-checked: the reader may have scrolled up between the request and this frame.
      if (following.current && !dragging.current) {
        list.current?.scrollToEnd({ animated: !replyReveal.busy() });
      }
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
        s.gap = contentSize.height - layoutMeasurement.height - offset;
        if (s.gap <= NEAR_END) {
          following.current = true;
        } else if (offset < s.offset - 1 && performance.now() > s.ownUntil) {
          // Moving up, and not by our own scroll back: web has no drag events for a wheel.
          following.current = false;
        }
        s.offset = offset;
        onScrollMetrics?.(offset, contentSize.height, layoutMeasurement.height);
      },
      onScrollBeginDrag: () => {
        dragging.current = true;
      },
      // A drag that left the list away from its end is reading back; one that moved nothing is not.
      onScrollEndDrag: () => {
        dragging.current = false;
        if (scroll.current.gap > NEAR_END) following.current = false;
      },
    }),
    [list, onScrollMetrics, toEnd],
  );
}

/**
 * Raises the mist to the bottom limit of the top nav bar during a long scrolled chat and unmounts
 * the mountains once covered; remounts the mountains immediately when scrolling back to the top.
 */
function useMistCollapse(
  collapsed: boolean,
  sheetLift: number,
  convLift: number,
  still: boolean,
) {
  const [progress] = useState(() => new Animated.Value(collapsed ? 1 : 0));
  const [phase, setPhase] = useState({
    collapsed,
    layoutCollapsed: collapsed,
    sceneHidden: collapsed,
  });
  if (phase.collapsed !== collapsed) {
    setPhase(
      collapsed
        ? { collapsed: true, layoutCollapsed: true, sceneHidden: still }
        : { collapsed: false, layoutCollapsed: !still, sceneHidden: false },
    );
  }
  const prev = useRef(collapsed);

  useEffect(() => {
    if (prev.current === collapsed) return;
    prev.current = collapsed;
    if (collapsed) {
      if (still) {
        progress.setValue(1);
        return;
      }
      const anim = Animated.timing(progress, {
        toValue: 1,
        ...MIST_COLLAPSE,
        useNativeDriver: USE_NATIVE_DRIVER,
      });
      anim.start(({ finished }) => {
        if (finished) setPhase((p) => (p.collapsed ? { ...p, sceneHidden: true } : p));
      });
      return () => anim.stop();
    }
    if (still) {
      progress.setValue(0);
      return;
    }
    const anim = Animated.timing(progress, {
      toValue: 0,
      ...MIST_COLLAPSE,
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start(({ finished }) => {
      if (finished) setPhase((p) => (!p.collapsed ? { ...p, layoutCollapsed: false } : p));
    });
    return () => anim.stop();
  }, [collapsed, progress, still]);

  const sheetScrollY = useMemo(
    () => progress.interpolate({ inputRange: [0, 1], outputRange: [0, -sheetLift] }),
    [progress, sheetLift],
  );
  const convOffsetY = useMemo(
    () => progress.interpolate({ inputRange: [0, 1], outputRange: [convLift, 0] }),
    [progress, convLift],
  );
  const circleOpacity = useMemo(
    () => progress.interpolate({ inputRange: [0, 0.65, 1], outputRange: [1, 0, 0] }),
    [progress],
  );
  const circleScrollY = useMemo(
    () => progress.interpolate({ inputRange: [0, 1], outputRange: [0, -36] }),
    [progress],
  );
  const circleScale = useMemo(
    () => progress.interpolate({ inputRange: [0, 1], outputRange: [1, 0.78] }),
    [progress],
  );

  return {
    layoutCollapsed: phase.layoutCollapsed,
    sceneHidden: phase.sceneHidden,
    sheetScrollY,
    convOffsetY,
    circleOpacity,
    circleScrollY,
    circleScale,
  };
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
  // Bottom limit of the compact top nav bar where the raised mist and expanded list meet it.
  const navLimit = insets.top + 2 + NAV_BAR_HEIGHT + 6;
  // Bring the solid mist body right up behind the nav bar's midline so the vapor puffs frame it
  // and no mountain peaks peek out when SceneCanvas unmounts.
  const sheetScrollLift = Math.max(
    0,
    Math.ceil(layout.sheetTop + VAPOR_BODY_TOP - (navLimit - 22)),
  );
  const convScrollLift = Math.max(0, Math.round(layout.listTop - navLimit));
  const [scrollCollapsed, setScrollCollapsed] = useState(false);
  if (scrollCollapsed && p.messages.length === 0) setScrollCollapsed(false);
  const keyboardOpenRef = useRef(keyboard.open);
  useEffect(() => {
    keyboardOpenRef.current = keyboard.open;
  }, [keyboard.open]);

  const onScrollMetrics = useCallback(
    (offset: number, contentHeight: number, viewportHeight: number) => {
      if (keyboardOpenRef.current) return;
      setScrollCollapsed((was) => {
        if (!was) {
          // Only collapse when the chat still overflows after expanding, so scrolling back up
          // always has room to bring the mountains back cleanly without oscillation.
          return (
            offset > COLLAPSE_AT &&
            contentHeight > viewportHeight + convScrollLift + COLLAPSE_MIN_OVERFLOW
          );
        }
        return offset > EXPAND_AT;
      });
    },
    [convScrollLift],
  );

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
        photoUri={item.photoUri}
        keywords={item.keywords ?? keywordsFor(item.entryId)}
        revealId={item.role === 'assistant' ? item.id : undefined}
        entryId={item.id}
        sources={item.sources}
        onOpenSources={openSheet}
        media={item.media}
        meta={item.latencyMs != null ? formatLatency(item.latencyMs) : undefined}
      />
    ),
    [openSheet],
  );
  const list = useRef<React.ComponentRef<typeof FlashList<ChatRow>>>(null);
  const follow = useListFollow(list, onScrollMetrics);
  // Keyboard open: the mist, the circle and the conversation rise over the ranges together.
  const motion = useKeyboardMotion(keyboard.bottom, layout.keyboardLift);
  const still = useReducedMotion();
  const mist = useMistCollapse(
    scrollCollapsed && p.messages.length > 0 && !keyboard.open,
    sheetScrollLift,
    convScrollLift,
    still,
  );
  const backdropRise = useMemo(
    () => Animated.add(motion.sheetY, mist.sheetScrollY),
    [motion.sheetY, mist.sheetScrollY],
  );
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
    if (still) return shown.setValue(1);
    const anim = Animated.timing(shown, {
      toValue: 1,
      duration: 280,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [p.fadeIn, shown, still]);
  const navFadeOpacity = useMemo(
    () =>
      motion.sheetY.interpolate({
        inputRange: [-NAV_FADE, 0],
        outputRange: [0, 1],
        extrapolate: 'clamp',
      }),
    [motion.sheetY],
  );
  useChatNavFade(p.nav ? null : navFadeOpacity, keyboard.open || !!sheet);
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
        rise={backdropRise}
        extraLift={sheetScrollLift}
        hideScene={mist.sceneHidden}
      />
      <Animated.View
        style={[
          StyleSheet.absoluteFill,
          mist.layoutCollapsed
            ? {
                opacity: mist.circleOpacity,
                transform: [
                  { translateY: motion.sheetY },
                  { translateY: mist.circleScrollY },
                  { scale: mist.circleScale },
                ],
              }
            : { transform: [{ translateY: motion.sheetY }] },
        ]}
        pointerEvents="none"
      >
        <PetCircle
          x={layout.circle.x}
          y={layout.circle.y}
          r={layout.circle.r}
          voice={voice}
          ready={ready}
          loading={p.model.status === 'loading'}
          hidden={mist.sceneHidden}
          gaze={gaze}
        />
      </Animated.View>
      <Animated.View style={[StyleSheet.absoluteFill, { opacity: shown }]} pointerEvents="box-none">
        <View style={[styles.body, { top: layout.listTop }]}>
          <Animated.View
            style={[
              styles.conversation,
              mist.layoutCollapsed
                ? {
                    marginTop: -convScrollLift,
                    transform: [{ translateY: motion.sheetY }, { translateY: mist.convOffsetY }],
                  }
                : { transform: [{ translateY: motion.sheetY }] },
            ]}
          >
            <View style={[styles.column, styles.list]}>
              <FlashList
                ref={list}
                data={p.messages}
                renderItem={renderItem}
                keyExtractor={keyExtractor}
                drawDistance={900}
                maintainVisibleContentPosition={FLASHLIST_DISABLE_MVCP}
                ListHeaderComponent={greeting}
                ListFooterComponent={
                  p.busy ? (
                    <TypingBubble label={fill(t.chatScreen.typing, { pet: PET_NAME })} />
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
                  onPhoto={p.onPhoto}
                  photoUri={p.photoUri}
                  onRemovePhoto={p.onRemovePhoto}
                  onCaret={gaze.set}
                />
              </View>
            </View>
          </Animated.View>
        </View>
        {p.nav && (
          // The circle rises into the bar's place while typing, so the bar fades out of its way.
          <Animated.View
            style={[StyleSheet.absoluteFill, { opacity: navFadeOpacity }]}
            pointerEvents={keyboard.open ? 'none' : 'box-none'}
          >
            {p.nav}
          </Animated.View>
        )}
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
});
