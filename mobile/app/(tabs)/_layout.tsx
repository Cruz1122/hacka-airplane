// Chat and Grupo are tabs: both stay mounted once opened (a guide's group session survives a
// trip to the chat), and Android back from Grupo returns to Chat, from Chat leaves the app.
// Each screen draws the cloud bar itself (AppNavBar), so the chat can fade it under the keyboard;
// the navigator's own bar is off.
import { Redirect, Tabs, usePathname } from 'expo-router';

import { markOnboardingDone, onboardingDone } from '@/onboarding/launch';
import { needsOnboarding } from '@/state/launchGate';

const hiddenTabBar = () => null;

export default function TabsLayout() {
  const pathname = usePathname();
  if (needsOnboarding(onboardingDone(), pathname)) return <Redirect href="/onboarding" />;
  // A launch that skipped the onboarding (a link into Grupo) must not meet it on the Chat tab.
  markOnboardingDone();
  return (
    <Tabs
      tabBar={hiddenTabBar}
      backBehavior="firstRoute"
      screenOptions={{ headerShown: false, animation: 'none' }}
    >
      <Tabs.Screen name="index" />
      <Tabs.Screen name="group" />
    </Tabs>
  );
}
