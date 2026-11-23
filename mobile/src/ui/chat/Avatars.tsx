// The user's chat avatar: a person glyph in plain views (no Svg per row).
import { memo } from 'react';
import { StyleSheet, View } from 'react-native';

import { brand } from '../theme/tokens';

export const UserAvatar = memo(function UserAvatar({ size }: { size: number }) {
  return (
    <View style={[styles.circle, { width: size, height: size }]}>
      <View
        style={[
          styles.part,
          { width: size * 0.36, height: size * 0.36, top: size * 0.18, left: size * 0.32 - 2 },
        ]}
      />
      <View
        style={[
          styles.part,
          { width: size * 0.66, height: size * 0.5, top: size * 0.6, left: size * 0.17 - 2 },
        ]}
      />
    </View>
  );
});

const styles = StyleSheet.create({
  circle: {
    borderRadius: 999,
    borderWidth: 2,
    borderColor: brand.card,
    backgroundColor: brand.primary,
    overflow: 'hidden',
  },
  part: { position: 'absolute', borderRadius: 999, backgroundColor: brand.card },
});
