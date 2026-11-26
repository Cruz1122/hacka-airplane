import { CameraView, scanFromURLAsync, useCameraPermissions } from 'expo-camera';
import { useIsFocused } from 'expo-router';
import { Button, StyleSheet, Text, View } from 'react-native';

import { t } from '@/i18n';

export async function readQrImage(uri: string) {
  return (await scanFromURLAsync(uri, ['qr']))[0]?.data;
}

export function QrCamera({ onCode, onError }: { onCode: (code: string) => void; onError: () => void }) {
  const [permission, request] = useCameraPermissions();
  const focused = useIsFocused();
  if (!focused) return null;
  if (!permission?.granted) {
    return (
      <View style={styles.permission}>
        <Text>{t.qrUpdate.permission}</Text>
        <Button title={t.qrUpdate.allow} onPress={() => void request().catch(onError)} />
      </View>
    );
  }
  return <CameraView facing="back" style={styles.preview} barcodeScannerSettings={{ barcodeTypes: ['qr'] }}
    onBarcodeScanned={({ data }) => onCode(data)} onMountError={onError} />;
}

const styles = StyleSheet.create({
  preview: { aspectRatio: 4 / 3, borderRadius: 16, overflow: 'hidden' },
  permission: { gap: 12 },
});

