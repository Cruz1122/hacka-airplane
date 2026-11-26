import { router } from 'expo-router';
import { ScrollView, StyleSheet, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { t } from '@/i18n';
import { brand, spacing } from '@/ui/theme/tokens';

import { TrailPath } from './TrailPath';

export function RecorridoScreen() {
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const mapW = Math.min(width - spacing.xl * 2, 720);
  return (
    <View
      style={[styles.root, { paddingTop: insets.top }]}
      accessibilityLabel={t.trail.title}
    >
      {/* Flip the scroller so offset 0 shows the trail foot (station 1) and the user scrolls up. */}
      <ScrollView style={styles.invert}>
        <View style={[styles.invert, styles.pad, { paddingBottom: spacing.xl }]}>
          <TrailPath
            width={mapW}
            onStationPress={(id) => router.push(`/estacion/${id}`)}
          />
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.card },
  invert: { transform: [{ scaleY: -1 }] },
  pad: {
    paddingHorizontal: spacing.xl,
    maxWidth: 720 + spacing.xl * 2,
    width: '100%',
    alignSelf: 'center',
  },
});
