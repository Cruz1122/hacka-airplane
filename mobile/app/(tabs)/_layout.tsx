// Chat, Grupo and Ruta are tabs: screens stay mounted once opened (a guide's group session survives
// a trip to the chat), and Android back from Grupo returns to Chat, from Chat leaves the app.
// A single persistent AppTabBar sits above the navigator so tab transitions animate only the page
// underneath while the top switch stays fixed and slides its active pill.
import { Redirect, Tabs, usePathname } from 'expo-router';

import { markOnboardingDone, onboardingDone } from '@/onboarding/launch';
import { needsOnboarding } from '@/state/launchGate';
import { AppTabBar, NavBarHost, type AppTabBarProps } from '@/ui/AppNavBar';
import { useReducedMotion } from '@/ui/useReducedMotion';

const renderTabBar = (props: AppTabBarProps) => <AppTabBar {...props} />;

export default function TabsLayout() {
  const pathname = usePathname();
  const reduced = useReducedMotion();
  if (needsOnboarding(onboardingDone(), pathname)) return <Redirect href="/onboarding" />;
  // A launch that skipped the onboarding (a link into Grupo) must not meet it on the Chat tab.
  markOnboardingDone();
  return (
    <NavBarHost>
      <Tabs
        tabBar={renderTabBar}
        backBehavior="firstRoute"
        screenOptions={{ headerShown: false, animation: reduced ? 'none' : 'shift' }}
      >
        <Tabs.Screen name="index" />
        <Tabs.Screen name="group" />
        <Tabs.Screen name="recorrido" />
      </Tabs>
    </NavBarHost>
  );
}
