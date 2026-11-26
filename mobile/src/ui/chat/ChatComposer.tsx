// Message input. It owns the draft text, so keystrokes re-render only this component, never the
// message list. Two looks: 'docked', the chat's tab that rises out of the bottom edge and joins it
// with concave shoulders, and 'floating', a soft pill.
import { memo, useCallback, useEffect, useRef, useState } from 'react';
import {
  Animated,
  Easing,
  Pressable,
  StyleSheet,
  Text,
  type TextLayoutEvent,
  TextInput,
  View,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { Icon } from '../icons/Icon';
import { brand, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

export type ComposerVariant = 'floating' | 'docked';

export interface ChatComposerProps {
  /** Sending is blocked (model busy or not ready); typing still works. */
  disabled: boolean;
  placeholder: string;
  sendLabel: string;
  onSend: (text: string) => void;
  /** Reports empty/non-empty changes without lifting every keystroke into the parent. */
  onHasTextChange?: (hasText: boolean) => void;
  /** Default 'floating'. */
  variant?: ComposerVariant;
  /** Text already in the field when it mounts; remount (new `key`) to apply another. */
  initialText?: string;
  /** Docked only: height of the base strip under the tab, e.g. the screen's bottom inset. */
  floor?: number;
  /** Docked only: no motion even when the system setting is off (the design catalog's toggle). */
  reducedMotion?: boolean;
  /**
   * Docked only: where the last typed character is, in window coordinates, while the field has
   * focus (the start of the field when it is empty); null once it loses focus. The Pet looks there.
   */
  onCaret?: (point: { x: number; y: number } | null) => void;
  /** Docked only: a pen button left of the field that starts a new conversation. */
  onNewChat?: () => void;
  /** Docked only: the pen button's accessibility label (required with `onNewChat`). */
  newChatLabel?: string;
}

/** Docked geometry in pt, named so the shape can be tuned in one place. */
export const DOCK = {
  /** Radius of the concave shoulders where the tab meets the base strip. */
  fillet: 16,
  /** Top corners of the tab. */
  radius: 26,
  /** Screen edge to the tab's side; at least `fillet`, so the shoulders fit inside the screen. */
  inset: 22,
  /** Default base strip height. */
  floor: 10,
} as const;

export const ChatComposer = memo(function ChatComposer(props: ChatComposerProps) {
  return props.variant === 'docked' ? (
    <DockedComposer {...props} />
  ) : (
    <FloatingComposer {...props} />
  );
});

/** Clears the field after a send; empty text or a blocked send does nothing. */
function useDraft(
  initialText: string | undefined,
  disabled: boolean,
  onSend: (t: string) => void,
  onHasTextChange?: (hasText: boolean) => void,
) {
  const [text, setText] = useState(initialText ?? '');
  const hasText = text.trim() !== '';
  const canSend = !disabled && hasText;
  useEffect(() => onHasTextChange?.(hasText), [hasText, onHasTextChange]);
  const submit = () => {
    if (!canSend) return;
    onSend(text);
    setText('');
  };
  return { text, setText, canSend, submit };
}

function FloatingComposer({
  disabled,
  placeholder,
  sendLabel,
  onSend,
  initialText,
  onHasTextChange,
}: ChatComposerProps) {
  const { text, setText, canSend, submit } = useDraft(
    initialText,
    disabled,
    onSend,
    onHasTextChange,
  );
  return (
    <View style={floating.bar}>
      <TextInput
        value={text}
        onChangeText={setText}
        placeholder={placeholder}
        placeholderTextColor={brand.inkMuted}
        selectionColor={brand.primarySoft}
        onSubmitEditing={submit}
        returnKeyType="send"
        style={floating.input}
      />
      <Pressable
        onPress={submit}
        disabled={!canSend}
        accessibilityRole="button"
        accessibilityLabel={sendLabel}
        accessibilityState={{ disabled: !canSend }}
        style={({ pressed }) => [floating.send, { opacity: !canSend ? 0.45 : pressed ? 0.85 : 1 }]}
      >
        <Svg width={20} height={20} viewBox="0 0 24 24">
          <Path
            d="M4 12 H18 M12 5.5 L18.5 12 L12 18.5"
            stroke={brand.onPrimary}
            strokeWidth={2.4}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </Svg>
      </Pressable>
    </View>
  );
}

function DockedComposer({
  disabled,
  placeholder,
  sendLabel,
  onSend,
  initialText,
  onHasTextChange,
  floor = DOCK.floor,
  reducedMotion = false,
  onCaret,
  onNewChat,
  newChatLabel,
}: ChatComposerProps) {
  const { text, setText, canSend, submit } = useDraft(
    initialText,
    disabled,
    onSend,
    onHasTextChange,
  );
  const [focused, setFocused] = useState(false);
  const { field, onMirrorLayout } = useCaret(text, focused, onCaret);
  const still = useReducedMotion() || reducedMotion;
  // Native-driver opacity/scale only: the model runs on the same device as this screen.
  const [ready] = useState(() => new Animated.Value(canSend ? 1 : 0));
  const [press] = useState(() => new Animated.Value(1));
  useEffect(() => {
    const to = canSend ? 1 : 0;
    if (still) return ready.setValue(to);
    const anim = Animated.timing(ready, {
      toValue: to,
      duration: 160,
      easing: Easing.out(Easing.quad),
      useNativeDriver: true,
    });
    anim.start();
    return () => anim.stop();
  }, [canSend, still, ready]);
  const pressTo = (toValue: number, duration: number) => {
    if (still) return press.setValue(1);
    Animated.timing(press, { toValue, duration, useNativeDriver: true }).start();
  };
  return (
    <View>
      <View style={[docked.row, { paddingHorizontal: DOCK.inset - DOCK.fillet }]}>
        <Shoulder side="left" />
        <View style={docked.tab}>
          {onNewChat && (
            <Pressable
              onPress={onNewChat}
              accessibilityRole="button"
              accessibilityLabel={newChatLabel}
              style={({ pressed }) => [docked.newChat, pressed && docked.newChatPressed]}
            >
              <Icon name="squarePen" size={20} color={brand.ink} />
            </Pressable>
          )}
          <View style={docked.fieldBox}>
            <TextInput
              ref={field}
              value={text}
              onChangeText={setText}
              placeholder={placeholder}
              placeholderTextColor={brand.inkMuted}
              selectionColor={brand.primarySoft}
              onSubmitEditing={submit}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              returnKeyType="send"
              style={[docked.field, focused && docked.fieldFocused]}
            />
            {onCaret && (
              // Same font, one unwrapped line: its width is how far the text runs in the field.
              <Text
                style={docked.mirror}
                numberOfLines={1}
                onTextLayout={onMirrorLayout}
                aria-hidden
                accessibilityElementsHidden
                importantForAccessibility="no-hide-descendants"
              >
                {text}
              </Text>
            )}
          </View>
          <Animated.View
            style={{
              opacity: ready.interpolate({ inputRange: [0, 1], outputRange: [0.4, 1] }),
              transform: [
                {
                  scale: Animated.multiply(
                    ready.interpolate({ inputRange: [0, 1], outputRange: [0.9, 1] }),
                    press,
                  ),
                },
              ],
            }}
          >
            <Pressable
              onPress={submit}
              onPressIn={() => pressTo(0.92, 120)}
              onPressOut={() => pressTo(1, 160)}
              disabled={!canSend}
              accessibilityRole="button"
              accessibilityLabel={sendLabel}
              accessibilityState={{ disabled: !canSend }}
              style={docked.send}
            >
              <Icon name="arrowUp" size={22} color={brand.onPrimary} strokeWidth={2.4} />
            </Pressable>
          </Animated.View>
        </View>
        <Shoulder side="right" />
      </View>
      {/* Drawn after the row and 1 pt into it, so no seam shows between tab and base. */}
      <View style={[docked.floor, { height: floor + 1 }]} />
    </View>
  );
}

/**
 * Reports the end of the draft in window coordinates. The width comes from a hidden copy of the
 * text in the field's font; a single-line field scrolls once the text is wider, so the point stops
 * at the field's right padding.
 */
function useCaret(
  text: string,
  focused: boolean,
  onCaret: ChatComposerProps['onCaret'],
) {
  const field = useRef<React.ComponentRef<typeof TextInput>>(null);
  const [textWidth, setTextWidth] = useState(0);
  const onMirrorLayout = useCallback((e: TextLayoutEvent) => {
    setTextWidth(e.nativeEvent.lines[0]?.width ?? 0);
  }, []);
  const width = text === '' ? 0 : textWidth;
  useEffect(() => {
    if (!onCaret) return;
    const node = field.current;
    if (!focused || !node) return onCaret(null);
    node.measureInWindow((x, y, w, h) => {
      const pad = FIELD_PAD;
      onCaret({ x: x + pad + Math.min(width, Math.max(0, w - pad * 2)), y: y + h / 2 });
    });
  }, [focused, width, onCaret]);
  useEffect(() => () => onCaret?.(null), [onCaret]);
  return { field, onMirrorLayout };
}

/**
 * Concave fillet joining the tab's side to the base strip: a square minus a quarter circle.
 * One extra pt column reaches under the tab so the seam never shows. Explicit numeric size: a
 * bare <svg> on web keeps its intrinsic 300 px width.
 */
function Shoulder({ side }: { side: 'left' | 'right' }) {
  const r = DOCK.fillet;
  const w = r + 1;
  const d =
    side === 'left'
      ? `M${r} 0H${w}V${r}H0A${r} ${r} 0 0 0 ${r} 0Z`
      : `M1 0H0V${r}H${w}A${r} ${r} 0 0 1 1 0Z`;
  return (
    <Svg
      width={w}
      height={r}
      viewBox={`0 0 ${w} ${r}`}
      style={side === 'left' ? docked.shoulderLeft : docked.shoulderRight}
      pointerEvents="none"
    >
      <Path d={d} fill={brand.cardShade} />
    </Svg>
  );
}

const floating = StyleSheet.create({
  bar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    padding: 6,
    marginHorizontal: 12,
    borderRadius: 30,
    backgroundColor: brand.card,
    borderWidth: 1,
    borderColor: brand.cardShade,
  },
  input: {
    ...type.body,
    flex: 1,
    minWidth: 0,
    minHeight: 46,
    paddingHorizontal: 18,
    borderRadius: 23,
    backgroundColor: brand.cardShade,
    color: brand.ink,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineOffset: -1,
  },
  send: {
    width: 46,
    height: 46,
    borderRadius: 16,
    backgroundColor: brand.ink,
    alignItems: 'center',
    justifyContent: 'center',
  },
});

/** The field's horizontal text padding. */
const FIELD_PAD = 18;

const docked = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'flex-end', marginBottom: -1 },
  shoulderLeft: { marginRight: -1 },
  shoulderRight: { marginLeft: -1 },
  tab: {
    flex: 1,
    minWidth: 0,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingTop: 8,
    paddingHorizontal: 8,
    paddingBottom: 9,
    borderTopLeftRadius: DOCK.radius,
    borderTopRightRadius: DOCK.radius,
    backgroundColor: brand.cardShade,
  },
  newChat: {
    width: 44,
    height: 46,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
  },
  newChatPressed: { backgroundColor: brand.primarySoft },
  fieldBox: { flex: 1, minWidth: 0 },
  mirror: {
    ...type.body,
    position: 'absolute',
    left: 0,
    top: 0,
    width: 4000,
    opacity: 0,
  },
  field: {
    ...type.body,
    flex: 1,
    minWidth: 0,
    minHeight: 46,
    paddingHorizontal: FIELD_PAD,
    borderRadius: 23,
    borderWidth: 1,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    color: brand.ink,
    // The border is the focus indicator; the browser's own outline would double it.
    outlineWidth: 0,
    outlineStyle: 'solid',
    outlineColor: brand.primary,
    outlineOffset: -1,
  },
  fieldFocused: { borderColor: brand.primary, outlineWidth: 2 },
  send: {
    width: 46,
    height: 46,
    borderRadius: 16,
    backgroundColor: brand.ink,
    outlineColor: brand.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  floor: { backgroundColor: brand.cardShade },
});
