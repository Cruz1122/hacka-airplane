import { useMemo } from 'react';
import { View, StyleSheet, useWindowDimensions } from 'react-native';
import Svg, { Path, Rect } from 'react-native-svg';

import { utf8Bytes } from '@/core/knowledge/qrPatch';
import { t } from '@/i18n';
import { colors } from './theme/tokens';

// Use the matrix encoder directly. Canvas and filesystem renderers are browser- or Node-only.
// eslint-disable-next-line @typescript-eslint/no-require-imports
const { create } = require('qrcode/lib/core/qrcode') as {
  create: (
    segments: { data: Uint8Array; mode: 'byte' }[],
    options: { errorCorrectionLevel: 'M' },
  ) => {
    modules: { size: number; data: Uint8Array };
  };
};

export function KnowledgeQr({ code }: { code: string }) {
  const { width } = useWindowDimensions();
  const pixels = Math.min(400, Math.max(160, width - 76));
  const { size, path } = useMemo(() => {
    const {
      modules: { size, data },
    } = create([{ data: utf8Bytes(code), mode: 'byte' }], { errorCorrectionLevel: 'M' });
    const lines: string[] = [];
    // Join touching modules on each row for a compact SVG path.
    for (let y = 0; y < size; y++) {
      let x = 0;
      while (x < size) {
        if (!data[y * size + x]) {
          x++;
          continue;
        }
        const start = x;
        while (x < size && data[y * size + x]) x++;
        const run = x - start;
        lines.push('M' + (start + 4) + ' ' + (y + 4) + 'h' + run + 'v1h-' + run + 'z');
      }
    }
    return { size: size + 8, path: lines.join('') };
  }, [code]);
  const scaled = Math.max(1, Math.floor(pixels / size)) * size;
  return (
    <View
      accessibilityRole="image"
      accessibilityLabel={t.knowledgeAdmin.result}
      style={styles.code}
    >
      <Svg width={scaled} height={scaled} viewBox={'0 0 ' + size + ' ' + size}>
        <Rect width={size} height={size} fill={colors.light.background} />
        <Path d={path} fill={colors.light.text} />
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({ code: { alignSelf: 'center' } });
