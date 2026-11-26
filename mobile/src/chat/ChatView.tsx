// The chat screen as plain props (app/index.tsx wires it to the assistant), so the design catalog
// can show every state on web, where the model never loads.
import { FlashList } from '@shopify/flash-list';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated,
  Easing,
  Keyboard,
  type LayoutChangeEvent,
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
  photoUri?: string;
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
  onPhoto?: () => void;
  photoUri?: string;
  onRemovePhoto?: () => void;
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
 * What the Pet is doing: thinking while an answer is worked out, then talking while it arrives
 * (each streamed chunk extends it) and for a moment per character after, as if reading it out.
 */
function usePetVoice(messages: ChatRow[], busy: boolean): VoiceState {
  const last = messages.at(-1);
  const length = last?.role === 'assistant' ? last.text.length : 0;
  const key = length > 0 && last ? `${last.id}:${length}` : null;
  // The reply (or chunk) the Pet has finished saying; any newer key means it is still talking.
  const [said, setSaid] = useState<string | null>(null);
  useEffect(() => {
    if (!key) return;
    const ms = Math.min(6000, Math.max(1500, length * 40));
    const timer = setTimeout(() => setSaid(key), ms);
    return () => clearTimeout(timer);
  }, [key, length]);
  if (key !== null && key !== said) return 'speaking';
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

/** Points of keyboard after which the mist is fully raised (the keyboard is never this short). */
const RAISED_AT = 80;

/**
 * The keyboard's occlusion as an animated value, eased in both directions so the composer rises
 * with the keyboard and settles back; the JS driver, because it moves layout (the list's bottom).
 */
function useKeyboardMotion(bottom: number) {
  const still = useReducedMotion();
  const [value] = useState(() => new Animated.Value(bottom));
  useEffect(() => {
    if (still) return value.setValue(bottom);
    const anim = Animated.timing(value, {
      toValue: bottom,
      duration: 220,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: false,
    });
    anim.start();
    return () => anim.stop();
  }, [bottom, still, value]);
  return value;
}

function ChatContent(p: ChatViewProps & { width: number; tall: number; viewBottom: number }) {
  const { tall } = p;
  const insets = useSafeAreaInsets();
  const keyboard = useChatKeyboard(p.viewBottom);
  const occluded = useKeyboardMotion(keyboard.bottom);
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
        photoUri={item.photoUri}
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
  const toEnd = useCallback(() => list.current?.scrollToEnd({ animated: true }), []);
  const voice = usePetVoice(p.messages, p.busy);
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
  // Keyboard open: the mist, the circle and the conversation rise over the ranges together.
  const rise = occluded.interpolate({
    inputRange: [0, RAISED_AT],
    outputRange: [0, -layout.keyboardLift],
    extrapolate: 'clamp',
  });
  return (
    <>
      <ChatBackdrop
        width={p.width}
        height={tall}
        layout={layout}
        time={p.sceneTime}
        rise={rise}
      />
      <Animated.View
        style={[StyleSheet.absoluteFill, { transform: [{ translateY: rise }] }]}
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
        <Animated.View
          style={[styles.body, { top: Animated.add(layout.listTop, rise), bottom: occluded }]}
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
              onContentSizeChange={toEnd}
              keyboardShouldPersistTaps="handled"
              contentContainerStyle={styles.listContent}
            />
            <TopFade />
          </View>
          {debug && (
            <View style={styles.column}>
              <DebugPanel steps={p.steps} state={p.state} />
            </View>
          )}
          <View>
            {/* Past the reading column the base strip still runs along the whole bottom edge. */}
            <View style={[styles.dockBase, { height: floor + 1 }]} />
            <View style={styles.column}>
              <ChatComposer
                variant="docked"
                floor={floor}
                disabled={p.busy}
                placeholder={t.inputPlaceholder}
                sendLabel={t.send}
                onSend={p.onSend}
                onPhoto={p.onPhoto}
                photoUri={p.photoUri}
                onRemovePhoto={p.onRemovePhoto}
                onCaret={gaze.set}
              />
            </View>
          </View>
        </Animated.View>
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
  dockBase: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: brand.cardShade,
  },
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
