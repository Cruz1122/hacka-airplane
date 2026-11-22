import { Stack } from 'expo-router';

import { es } from '@/ui/strings';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: es.appTitle }} />
      <Stack.Screen name="settings" options={{ title: es.settings }} />
      <Stack.Screen name="history" options={{ title: es.history }} />
    </Stack>
  );
}
