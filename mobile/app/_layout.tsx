import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { useEffect } from 'react';

import { t } from '@/i18n';
import { requestDevicePermissions } from '@/platform/devicePermissions';
import { preloadKnowledge } from '@/state/useKnowledge';
import { FONT_FILES } from '@/ui/theme/fonts';

export default function RootLayout() {
  const [loaded, error] = useFonts(FONT_FILES);
  // After the first commit, so it never delays the first frame; native loads run off the JS thread.
  useEffect(preloadKnowledge, []);
  useEffect(() => {
    void requestDevicePermissions();
  }, []);
  useEffect(() => {
    if (error) console.warn('Inter failed to load; text falls back to the system font.', error);
  }, [error]);
  // Wait for the bundled font so text does not reflow; a load error still renders the app.
  if (!loaded && !error) return null;
  return (
    <Stack>
      {/* Chat and Grupo tabs. The chat draws its own header; it appears without a slide so the
          onboarding can hand over its last frame. */}
      <Stack.Screen name="(tabs)" options={{ headerShown: false, animation: 'none' }} />
      <Stack.Screen name="administrar-informacion" options={{ title: t.knowledgeAdmin.heading }} />
      <Stack.Screen name="actualizar" options={{ title: t.qrUpdate.nav }} />
      <Stack.Screen name="history" options={{ title: t.history }} />
      <Stack.Screen name="onboarding" options={{ headerShown: false }} />
      <Stack.Screen name="lab" options={{ headerShown: false, title: t.dev.lab }} />
      <Stack.Screen name="design" options={{ title: t.dev.design }} />
      <Stack.Screen name="estacion" options={{ headerShown: false }} />
    </Stack>
  );
}
