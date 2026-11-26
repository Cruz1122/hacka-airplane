// Shared bottom-sheet overlay matching SourcesSheet's geometry and motion: scrim, rounded top
// corners, grab handle, Android hardware-back support, and reduced-motion respect.
import { useCallback, useEffect, useState, type ReactNode } from 'react';
import {
  Animated,
  BackHandler,
  Easing,
  Platform,
  Pressable,
  StyleSheet,
  useWindowDimensions,
  View,
} from 'react-native';

import { useChatKeyboard } from '@/chat/useChatKeyboard';

import { brand } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';
import { useReducedMotion } from './useReducedMotion';

const USE_NATIVE_DRIVER = Platform.OS !== 'web';

export interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  /** Bottom safe-area inset so the last control clears the home indicator. */
  bottom?: number;
  /** Optional back handler; return true to consume Android back without closing the sheet. */
  onHardwareBack?: () => boolean;
  /** No motion even when the system/app setting is off (design catalog). */
  reducedMotion?: boolean;
  children: (close: () => void) => ReactNode;
}

export function BottomSheet({ open, ...rest }: BottomSheetProps) {
  return open ? <OpenBottomSheet {...rest} /> : null;
}

function OpenBottomSheet({
  onClose,
  bottom = 0,
  onHardwareBack,
  reducedMotion = false,
  children,
}: Omit<BottomSheetProps, 'open'>) {
  const reduced = useReducedMotion() || reducedMotion;
  const { palette, highContrast, borderWidth } = useAccessibilityTheme();
  const [shown] = useState(() => new Animated.Value(reduced ? 1 : 0));
  const [closing, setClosing] = useState(false);
  // Edge to edge, the keyboard no longer shrinks the window: lift the sheet above it ourselves,
  // or a short sheet (the admin password) sits entirely under the keyboard.
  const { height } = useWindowDimensions();
  const keyboard = useChatKeyboard(height);

  useEffect(() => {
    if (closing) {
      if (reduced) {
        onClose();
        return;
      }
      let cancelled = false;
      const anim = Animated.timing(shown, {
        toValue: 0,
        duration: 200,
        easing: Easing.in(Easing.quad),
        useNativeDriver: USE_NATIVE_DRIVER,
      });
      anim.start(({ finished }) => {
        if (finished && !cancelled) onClose();
      });
      return () => {
        cancelled = true;
        anim.stop();
      };
    }

    if (reduced) {
      shown.setValue(1);
      return;
    }
    const anim = Animated.timing(shown, {
      toValue: 1,
      duration: 260,
      easing: Easing.out(Easing.quad),
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [closing, onClose, reduced, shown]);

  const close = useCallback(() => {
    if (reduced) {
      onClose();
      return;
    }
    setClosing(true);
  }, [onClose, reduced]);

  useEffect(() => {
    if (Platform.OS !== 'android') return;
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      if (onHardwareBack?.()) return true;
      close();
      return true;
    });
    return () => sub.remove();
  }, [close, onHardwareBack]);

  return (
    <View
      style={[StyleSheet.absoluteFill, styles.overlay, { paddingBottom: keyboard.bottom }]}
      pointerEvents={closing ? 'none' : 'auto'}
    >
      <Animated.View
        style={[
          StyleSheet.absoluteFill,
          {
            backgroundColor: palette.ink,
            opacity: shown.interpolate({
              inputRange: [0, 1],
              outputRange: [0, highContrast ? 0.42 : 0.28],
            }),
          },
        ]}
      >
        <Pressable style={StyleSheet.absoluteFill} onPress={close} accessible={false} />
      </Animated.View>
      <Animated.View
        style={[
          styles.sheet,
          {
            paddingBottom: (keyboard.open ? 0 : bottom) + 16,
            maxHeight: keyboard.open ? (height - keyboard.bottom) * 0.84 : '84%',
            backgroundColor: palette.card,
            borderTopWidth: highContrast ? borderWidth : 0,
            borderColor: palette.ink,
            boxShadow: `0 -6px 24px ${palette.glow}`,
            opacity: shown,
            transform: [
              { translateY: shown.interpolate({ inputRange: [0, 1], outputRange: [18, 0] }) },
            ],
          },
        ]}
        accessibilityViewIsModal
      >
        <View style={[styles.handle, { backgroundColor: palette.primarySoft }]} aria-hidden />
        {children(close)}
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    justifyContent: 'flex-end',
    alignItems: 'center',
    zIndex: 40,
  },
  sheet: {
    maxHeight: '84%',
    width: '100%',
    maxWidth: 560,
    paddingTop: 10,
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    backgroundColor: brand.card,
  },
  handle: {
    width: 36,
    height: 4,
    borderRadius: 2,
    backgroundColor: brand.primarySoft,
    alignSelf: 'center',
    marginBottom: 8,
  },
});
