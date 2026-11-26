// Corner brackets over a camera preview: where to hold the QR. Drawn, never a photo or asset.
import { StyleSheet, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { useAccessibilityTheme } from './useAccessibilityTheme';

const CORNERS = [
  'M4 30V12a8 8 0 0 1 8-8h18',
  'M70 4h18a8 8 0 0 1 8 8v18',
  'M96 70v18a8 8 0 0 1-8 8H70',
  'M30 96H12a8 8 0 0 1-8-8V70',
];

export function ScanFrame() {
  const { palette } = useAccessibilityTheme();
  return (
    <View style={styles.frame} pointerEvents="none" aria-hidden>
      <Svg width="100%" height="100%" viewBox="0 0 100 100">
        {CORNERS.map((d) => (
          <Path
            key={d}
            d={d}
            fill="none"
            stroke={palette.onPrimary}
            strokeWidth={3.5}
            strokeLinecap="round"
          />
        ))}
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    position: 'absolute',
    top: '18%',
    bottom: '18%',
    aspectRatio: 1,
    alignSelf: 'center',
  },
});
