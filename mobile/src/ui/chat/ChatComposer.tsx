// Message input. It owns the draft text, so keystrokes re-render only this component, never the
// message list. Two looks: 'docked', the chat's tab that rises out of the bottom edge and joins it
// with concave shoulders, and 'floating', a soft pill.
import { memo, useCallback, useEffect, useRef, useState } from 'react';
import {
  Animated,
  Easing,
  Image,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  type TextLayoutEvent,
  TextInput,
  View,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { t } from '@/i18n';
import { Icon } from '../icons/Icon';
import { brand, type } from '../theme/tokens';
import { useAccessibilityTheme } from '../useAccessibilityTheme';
import { useReducedMotion } from '../useReducedMotion';

export type ComposerVariant = 'floating' | 'docked';

const USE_NATIVE_DRIVER = Platform.OS !== 'web';

export interface ChatComposerProps {
  /** Sending is blocked while a turn is being processed; typing still works. */
  disabled: boolean;
  placeholder: string;
  sendLabel: string;
  onSend: (text: string) => void;
  onPhoto?: () => void;
  photoUri?: string;
  onRemovePhoto?: () => void;
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

/** Clears the field after sending text or an attachment. */
function useDraft(
  initialText: string | undefined,
  disabled: boolean,
  onSend: (t: string) => void,
  onHasTextChange?: (hasText: boolean) => void,
  hasAttachment = false,
) {
  const [text, setText] = useState(initialText ?? '');
  const hasText = text.trim() !== '';
  const canSend = !disabled && (hasText || hasAttachment);
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
  const { palette, scaled } = useAccessibilityTheme();
  const { text, setText, canSend, submit } = useDraft(
    initialText,
    disabled,
    onSend,
    onHasTextChange,
  );
  return (
    <View
      style={[
        floating.bar,
        { backgroundColor: palette.card, borderColor: palette.cardShade },
      ]}
    >
      <TextInput
        value={text}
        onChangeText={setText}
        placeholder={placeholder}
        placeholderTextColor={palette.inkMuted}
        selectionColor={palette.primarySoft}
        onSubmitEditing={submit}
        returnKeyType="send"
        style={[
          floating.input,
          {
            fontSize: scaled.body.fontSize,
            lineHeight: scaled.body.lineHeight,
            backgroundColor: palette.cardShade,
            color: palette.ink,
          },
        ]}
      />
      <Pressable
        onPress={submit}
        disabled={!canSend}
        accessibilityRole="button"
        accessibilityLabel={sendLabel}
        accessibilityState={{ disabled: !canSend }}
        style={({ pressed }) => [
          floating.send,
          { backgroundColor: palette.ink, opacity: !canSend ? 0.45 : pressed ? 0.85 : 1 },
        ]}
      >
        <Svg width={20} height={20} viewBox="0 0 24 24">
          <Path
            d="M4 12 H18 M12 5.5 L18.5 12 L12 18.5"
            stroke={palette.onPrimary}
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
  onPhoto,
  photoUri,
  onRemovePhoto,
  floor = DOCK.floor,
  reducedMotion = false,
  onCaret,
}: ChatComposerProps) {
  const { palette, scaled, highContrast } = useAccessibilityTheme();
  const { text, setText, canSend, submit } = useDraft(
    initialText,
    disabled,
    onSend,
    onHasTextChange,
    !!photoUri,
  );
  const [focused, setFocused] = useState(false);
  const [photoFocused, setPhotoFocused] = useState(false);
  const { field, onMirrorLayout } = useCaret(text, focused, onCaret);
  const still = useReducedMotion() || reducedMotion;
  // Native-driver opacity/scale only: the model runs on the same device as this screen.
  const [ready] = useState(() => new Animated.Value(canSend ? 1 : 0));
  const [press] = useState(() => new Animated.Value(1));
  const [photoPress] = useState(() => new Animated.Value(1));
  useEffect(() => {
    const to = canSend ? 1 : 0;
    if (still) return ready.setValue(to);
    const anim = Animated.timing(ready, {
      toValue: to,
      duration: 160,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [canSend, still, ready]);
  const pressTo = (toValue: number, duration: number) => {
    if (still) return press.setValue(1);
    Animated.timing(press, { toValue, duration, useNativeDriver: USE_NATIVE_DRIVER }).start();
  };
  const photoPressTo = (toValue: number) => {
    if (still) return photoPress.setValue(1);
    Animated.spring(photoPress, {
      toValue,
      stiffness: 420,
      damping: 24,
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  };
  const hasPhoto = !!photoUri;
  return (
    <View>
      <View style={[docked.row, { paddingHorizontal: DOCK.inset - DOCK.fillet }]}>
        <Shoulder side="left" fill={palette.cardShade} />
        <View style={[docked.tab, { backgroundColor: palette.cardShade }]}>
          {photoUri ? (
            <PhotoAttachment key={photoUri} uri={photoUri} onRemove={onRemovePhoto} still={still} />
          ) : null}
          <View style={docked.inputRow}>
            {onPhoto && (
              <Animated.View style={{ transform: [{ scale: photoPress }] }}>
                <Pressable
                  accessibilityRole="button"
                  accessibilityLabel={t.chatScreen.photo.identify}
                  accessibilityState={{ disabled, selected: hasPhoto }}
                  disabled={disabled}
                  onPress={onPhoto}
                  onPressIn={() => photoPressTo(0.9)}
                  onPressOut={() => photoPressTo(1)}
                  onFocus={() => setPhotoFocused(true)}
                  onBlur={() => setPhotoFocused(false)}
                  style={({ pressed }) => [
                    docked.photo,
                    {
                      backgroundColor: palette.card,
                      borderColor: highContrast ? palette.ink : palette.primarySoft,
                      borderWidth: highContrast ? 2 : 1,
                    },
                    hasPhoto && {
                      backgroundColor: palette.primary,
                      borderColor: palette.primary,
                    },
                    pressed &&
                      (hasPhoto
                        ? { backgroundColor: palette.primaryLight, borderColor: palette.primaryLight }
                        : { backgroundColor: palette.primarySoft, borderColor: palette.primary }),
                    photoFocused && docked.photoFocused,
                    disabled && docked.photoDisabled,
                  ]}
                >
                  <Icon
                    name="camera"
                    size={20}
                    strokeWidth={2.1}
                    color={
                      disabled ? palette.inkMuted : hasPhoto ? palette.onPrimary : palette.primary
                    }
                  />
                </Pressable>
              </Animated.View>
            )}
            <View style={docked.fieldBox}>
              <TextInput
                ref={field}
                value={text}
                onChangeText={setText}
                placeholder={photoUri ? t.chatScreen.photo.captionPlaceholder : placeholder}
                placeholderTextColor={palette.inkMuted}
                selectionColor={palette.primarySoft}
                onSubmitEditing={submit}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                returnKeyType="send"
                style={[
                  docked.field,
                  {
                    fontSize: scaled.body.fontSize,
                    lineHeight: scaled.body.lineHeight,
                    backgroundColor: palette.card,
                    color: palette.ink,
                    borderColor: highContrast ? palette.ink : palette.primarySoft,
                    borderWidth: highContrast ? 2 : 1,
                  },
                  focused && { borderColor: palette.primary, outlineWidth: 2 },
                ]}
              />
              {onCaret && (
                // Same font, one unwrapped line: its width is how far the text runs in the field.
                <Text
                  style={[
                    docked.mirror,
                    { fontSize: scaled.body.fontSize, lineHeight: scaled.body.lineHeight },
                  ]}
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
                style={[docked.send, { backgroundColor: palette.ink }]}
              >
                <Icon name="arrowUp" size={22} color={palette.onPrimary} strokeWidth={2.4} />
              </Pressable>
            </Animated.View>
          </View>
        </View>
        <Shoulder side="right" fill={palette.cardShade} />
      </View>
      {/* Drawn after the row and 1 pt into it, so no seam shows between tab and base. */}
      <View style={[docked.floor, { height: floor + 1, backgroundColor: palette.cardShade }]} />
    </View>
  );
}

/** Framed thumbnail tucked inside the top of the docked composer with a compact corner dismiss chip. */
function PhotoAttachment({
  uri,
  onRemove,
  still,
}: {
  uri: string;
  onRemove?: () => void;
  still: boolean;
}) {
  const [enter] = useState(() => new Animated.Value(still ? 1 : 0));
  const [imageReady] = useState(() => new Animated.Value(still ? 1 : 0));
  const shownRef = useRef(still);

  useEffect(() => {
    if (still) {
      enter.setValue(1);
      return;
    }
    const anim = Animated.timing(enter, {
      toValue: 1,
      duration: 200,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [enter, still]);

  const onLoaded = useCallback(() => {
    if (shownRef.current) return;
    shownRef.current = true;
    if (still) {
      imageReady.setValue(1);
      return;
    }
    Animated.timing(imageReady, {
      toValue: 1,
      duration: 180,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  }, [imageReady, still]);

  return (
    <Animated.View
      style={[
        docked.attachmentRow,
        {
          opacity: enter,
          transform: [
            { translateY: enter.interpolate({ inputRange: [0, 1], outputRange: [6, 0] }) },
            { scale: enter.interpolate({ inputRange: [0, 1], outputRange: [0.95, 1] }) },
          ],
        },
      ]}
    >
      <View style={docked.attachmentCard}>
        <View style={docked.thumbnailFrame}>
          <Animated.View style={[StyleSheet.absoluteFill, { opacity: imageReady }]}>
            <Image
              source={{ uri }}
              accessible
              accessibilityLabel={t.chatScreen.photo.attached}
              resizeMode="cover"
              onLoad={onLoaded}
              onLoadEnd={onLoaded}
              style={docked.thumbnail}
            />
          </Animated.View>
        </View>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={t.chatScreen.photo.remove}
          onPress={onRemove}
          hitSlop={10}
          style={({ pressed }) => [docked.removePhoto, pressed && docked.removePhotoPressed]}
        >
          <Icon name="x" color={brand.onPrimary} size={12} strokeWidth={2.6} />
        </Pressable>
      </View>
    </Animated.View>
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
function Shoulder({ side, fill = brand.cardShade }: { side: 'left' | 'right'; fill?: string }) {
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
      <Path d={d} fill={fill} />
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
    flexDirection: 'column',
    gap: 8,
    paddingTop: 8,
    paddingHorizontal: 8,
    paddingBottom: 9,
    borderTopLeftRadius: DOCK.radius,
    borderTopRightRadius: DOCK.radius,
    backgroundColor: brand.cardShade,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  attachmentRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 4,
    paddingHorizontal: 4,
  },
  attachmentCard: {
    position: 'relative',
  },
  thumbnailFrame: {
    width: 64,
    height: 64,
    borderRadius: 14,
    overflow: 'hidden',
    backgroundColor: brand.card,
  },
  thumbnail: { width: '100%', height: '100%' },
  removePhoto: {
    position: 'absolute',
    top: -6,
    right: -6,
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: brand.ink,
    borderWidth: 2,
    borderColor: brand.cardShade,
    alignItems: 'center',
    justifyContent: 'center',
  },
  removePhotoPressed: { opacity: 0.78 },
  photo: {
    width: 46,
    height: 46,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  photoActive: {
    backgroundColor: brand.primary,
    borderColor: brand.primary,
  },
  photoPressed: {
    backgroundColor: brand.primarySoft,
    borderColor: brand.primary,
  },
  photoActivePressed: {
    backgroundColor: brand.primaryLight,
    borderColor: brand.primaryLight,
  },
  photoFocused: { outlineWidth: 2 },
  photoDisabled: { opacity: 0.45 },
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
