// The Pet is working on an answer: three dots that breathe in turn. Opacity only, on the native
// driver, because the model is running on the same device; still under reduced motion.
import { useEffect, useState } from 'react';
import { Animated, Platform, StyleSheet, Text, View } from 'react-native';

import { useReducedMotion } from '../useReducedMotion';
import { brand, type } from '../theme/tokens';

import { BubbleRow } from './ChatBubble';

export function TypingBubble({ label, detail }: { label: string; detail?: string }) {
  const reduced = useReducedMotion();
  const [dots] = useState(() => [0, 1, 2].map(() => new Animated.Value(0.35)));
  useEffect(() => {
    if (reduced) return;
    const breathe = (v: Animated.Value) =>
      Animated.sequence([
        Animated.timing(v, { toValue: 1, duration: 320, useNativeDriver: true }),
        Animated.timing(v, { toValue: 0.35, duration: 320, useNativeDriver: true }),
      ]);
    const loop = Animated.loop(Animated.stagger(180, dots.map(breathe)));
    loop.start();
    return () => loop.stop();
  }, [dots, reduced]);
  return (
    <BubbleRow role="assistant">
      <View style={styles.dots} accessibilityLabel={label} accessibilityRole="progressbar">
        {dots.map((v, i) => (
          <Animated.View key={i} style={[styles.dot, { opacity: v }]} />
        ))}
      </View>
      {detail ? (
        <Text style={styles.detail} numberOfLines={3}>
          {detail}
        </Text>
      ) : null}
    </BubbleRow>
  );
}

const styles = StyleSheet.create({
  dots: { flexDirection: 'row', gap: 6, paddingVertical: 6 },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: brand.primary },
  // Live model output of the routing step, shown only with the debug view on.
  detail: {
    ...type.caption,
    color: brand.inkMuted,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    marginTop: 4,
  },
});
