// Eight-cell OTP-style password field backed by a single overlaid TextInput so typing, pasting,
// backspacing, and screen readers behave natively across web, Android, and iOS.
import { useEffect, useRef, useState, type ComponentRef } from 'react';
import {
  Animated,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
  type TextInputProps,
} from 'react-native';

import { t } from '@/i18n';

import { Icon } from './icons/Icon';
import { brand, fonts, radius, spacing, type } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';
import { useReducedMotion } from './useReducedMotion';

export const OTP_PASSWORD_LENGTH = 8;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
const copy = t.knowledgeAdmin;

export interface OtpPasswordInputProps {
  label: string;
  value: string;
  onChangeText: (next: string) => void;
  length?: number;
  error?: boolean;
  disabled?: boolean;
  autoFocus?: boolean;
  autoComplete?: TextInputProps['autoComplete'];
  onSubmitEditing?: () => void;
}

export function OtpPasswordInput({
  label,
  value,
  onChangeText,
  length = OTP_PASSWORD_LENGTH,
  error = false,
  disabled = false,
  autoFocus = false,
  autoComplete = 'current-password',
  onSubmitEditing,
}: OtpPasswordInputProps) {
  const { palette, scaled, highContrast } = useAccessibilityTheme();
  const reduced = useReducedMotion();
  const inputRef = useRef<ComponentRef<typeof TextInput>>(null);
  const [focused, setFocused] = useState(false);
  const [revealed, setRevealed] = useState(false);
  const [caretOpacity] = useState(() => new Animated.Value(1));

  const chars = Array.from(value).slice(0, length);
  const activeIndex = Math.min(chars.length, length - 1);
  const showCaret = focused && !disabled && chars.length < length;

  useEffect(() => {
    if (!showCaret || reduced) {
      caretOpacity.setValue(1);
      return;
    }
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(caretOpacity, {
          toValue: 0,
          duration: 500,
          useNativeDriver: USE_NATIVE_DRIVER,
        }),
        Animated.timing(caretOpacity, {
          toValue: 1,
          duration: 500,
          useNativeDriver: USE_NATIVE_DRIVER,
        }),
      ]),
    );
    loop.start();
    return () => loop.stop();
  }, [caretOpacity, reduced, showCaret]);

  const handleChange = (raw: string) => {
    const trimmed = Array.from(raw).slice(0, length).join('');
    onChangeText(trimmed);
  };

  return (
    <View style={styles.container}>
      <View style={styles.labelRow}>
        <Text style={[styles.label, scaled.caption, { color: palette.ink }]}>{label}</Text>
        <Pressable
          onPress={() => setRevealed((prev) => !prev)}
          hitSlop={8}
          accessibilityRole="button"
          accessibilityLabel={revealed ? copy.hidePassword : copy.showPassword}
          accessibilityState={{ selected: revealed }}
          style={({ pressed }) => [
            styles.toggleBtn,
            pressed && { backgroundColor: palette.cardShade },
          ]}
        >
          <Icon
            name={revealed ? 'eyeOff' : 'eye'}
            size={18}
            color={palette.inkMuted}
            strokeWidth={2}
          />
        </Pressable>
      </View>

      <Pressable
        onPress={() => inputRef.current?.focus()}
        accessible={false}
        style={styles.cellsWrap}
      >
        <View style={styles.cellsRow} pointerEvents="none" aria-hidden>
          {Array.from({ length }, (_, idx) => {
            const char = chars[idx];
            const filled = char !== undefined;
            const isActive = focused && !disabled && idx === activeIndex;
            const borderColor = error
              ? palette.wine
              : isActive || filled
                ? palette.primary
                : highContrast
                  ? palette.ink
                  : palette.primarySoft;
            const borderWidth = isActive || highContrast ? 2 : 1.5;
            const backgroundColor = error && filled ? palette.wineSoft : palette.card;

            return (
              <View
                key={idx}
                style={[
                  styles.cell,
                  idx === Math.floor(length / 2) && styles.cellSplit,
                  {
                    backgroundColor,
                    borderColor,
                    borderWidth,
                    boxShadow: isActive ? `0 0 0 3px ${palette.glow}` : undefined,
                  },
                ]}
              >
                {filled ? (
                  revealed ? (
                    <Text style={[styles.charText, { color: error ? palette.wine : palette.ink }]}>
                      {char}
                    </Text>
                  ) : (
                    <View
                      style={[styles.dot, { backgroundColor: error ? palette.wine : palette.ink }]}
                    />
                  )
                ) : isActive && showCaret ? (
                  <Animated.View
                    style={[
                      styles.caret,
                      { backgroundColor: palette.primary, opacity: caretOpacity },
                    ]}
                  />
                ) : null}
              </View>
            );
          })}
        </View>

        <TextInput
          ref={inputRef}
          value={chars.join('')}
          onChangeText={handleChange}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onSubmitEditing={onSubmitEditing}
          editable={!disabled}
          autoFocus={autoFocus}
          autoCapitalize="none"
          autoCorrect={false}
          spellCheck={false}
          secureTextEntry={!revealed}
          autoComplete={autoComplete}
          maxLength={length}
          caretHidden
          accessibilityLabel={label}
          style={[StyleSheet.absoluteFill, styles.hiddenInput]}
        />
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: spacing.sm,
  },
  labelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  label: {
    ...type.caption,
    fontFamily: fonts.semibold,
    color: brand.ink,
    flexShrink: 1,
  },
  toggleBtn: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: 'center',
    justifyContent: 'center',
  },
  cellsWrap: {
    position: 'relative',
    width: '100%',
  },
  cellsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    width: '100%',
  },
  cell: {
    flex: 1,
    minWidth: 0,
    height: 48,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  cellSplit: {
    marginLeft: 4,
  },
  dot: {
    width: 9,
    height: 9,
    borderRadius: 5,
  },
  charText: {
    fontFamily: fonts.bold,
    fontSize: 18,
    lineHeight: 22,
  },
  caret: {
    width: 2,
    height: 20,
    borderRadius: 1,
  },
  hiddenInput: {
    opacity: 0.01,
    zIndex: 2,
  },
});
