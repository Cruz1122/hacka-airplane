// The park's emblem. The source art is a raster badge, so it ships as 1x/2x/3x PNGs and React
// Native loads the one that matches the screen density.
import { Image } from 'react-native';

import { t } from '@/i18n';

export function ParkEmblem({ size = 64 }: { size?: number }) {
  return (
    <Image
      source={require('../../assets/images/park-emblem.png')}
      style={{ width: size, height: size }}
      accessibilityRole="image"
      accessibilityLabel={t.parkName}
    />
  );
}
