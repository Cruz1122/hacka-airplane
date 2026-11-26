import { CameraView, scanFromURLAsync, useCameraPermissions } from 'expo-camera';
import { useIsFocused } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';

import { t } from '@/i18n';

import { Icon } from './icons/Icon';
import { ScanFrame } from './ScanFrame';
import { SecondaryButton } from './SecondaryButton';
import { radius, spacing } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';

export async function readQrImage(uri: string) {
  return (await scanFromURLAsync(uri, ['qr']))[0]?.data;
}

export function QrCamera({
  onCode,
  onError,
}: {
  onCode: (code: string) => void;
  onError: () => void;
}) {
  const [permission, request] = useCameraPermissions();
  const focused = useIsFocused();
  const { palette, scaled } = useAccessibilityTheme();
  if (!focused) return null;
  if (!permission?.granted) {
    return (
      <View style={[styles.preview, styles.permission, { backgroundColor: palette.cardShade }]}>
        <Icon name="camera" size={32} color={palette.ink} />
        <Text style={[scaled.body, styles.center, { color: palette.ink }]}>
          {t.qrUpdate.permission}
        </Text>
        <SecondaryButton label={t.qrUpdate.allow} onPress={() => void request().catch(onError)} />
      </View>
    );
  }
  return (
    <View style={[styles.preview, { backgroundColor: palette.ink }]}>
      <CameraView
        facing="back"
        style={StyleSheet.absoluteFill}
        barcodeScannerSettings={{ barcodeTypes: ['qr'] }}
        onBarcodeScanned={({ data }) => onCode(data)}
        onMountError={onError}
      />
      <ScanFrame />
    </View>
  );
}

const styles = StyleSheet.create({
  preview: { aspectRatio: 4 / 3, borderRadius: radius.lg, overflow: 'hidden' },
  permission: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.md,
    padding: spacing.xl,
  },
  center: { textAlign: 'center' },
});
