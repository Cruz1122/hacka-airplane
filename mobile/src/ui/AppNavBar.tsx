// CloudNavBar wired to the Chat/Grupo/Ruta tabs (app/(tabs)/_layout.tsx): rendered once by the tab
// navigator so switching tabs animates only the page underneath while the cloud bar stays pinned
// and slides its active pill.
import type { Tabs } from 'expo-router';
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ComponentProps,
  type ReactNode,
} from 'react';
import { Animated, StyleSheet, useWindowDimensions, View } from 'react-native';

import { AccessibilitySheet } from './AccessibilitySheet';
import { CloudNavBar, type NavSidePanel, type NavTab } from './CloudNavBar';
import { SettingsSheet } from './SettingsSheet';

/** Route name of each tab in the tabs layout. */
const ROUTE = { chat: 'index', group: 'group', route: 'recorrido' } as const;
const TAB_BY_ROUTE: Record<string, NavTab> = {
  index: 'chat',
  group: 'group',
  recorrido: 'route',
};

/** Gap between the safe area and the bar. */
const GAP = 2;

export type AppTabBarProps = Parameters<NonNullable<ComponentProps<typeof Tabs>['tabBar']>>[0];

interface ChatNavFade {
  opacity: Animated.AnimatedInterpolation<number> | Animated.Value;
  hidden: boolean;
}

interface NavBarHostContextValue {
  chatFade: ChatNavFade | null;
  setChatFade: (fade: ChatNavFade | null) => void;
  activeSheet: NavSidePanel | null;
  toggleSheet: (panel: NavSidePanel) => void;
  setBottomInset: (bottom: number) => void;
}

const NavBarHostContext = createContext<NavBarHostContextValue | null>(null);

export function NavBarHost({ children }: { children: ReactNode }) {
  const [chatFade, setChatFadeState] = useState<ChatNavFade | null>(null);
  const [activeSheet, setActiveSheet] = useState<NavSidePanel | null>(null);
  const [bottomInset, setBottomInset] = useState(0);

  const setChatFade = useCallback((next: ChatNavFade | null) => {
    setChatFadeState((prev) => {
      if (prev === next) return prev;
      if (prev && next && prev.opacity === next.opacity && prev.hidden === next.hidden) return prev;
      return next;
    });
  }, []);

  const toggleSheet = useCallback((panel: NavSidePanel) => {
    setActiveSheet((prev) => (prev === panel ? null : panel));
  }, []);

  const closeSheet = useCallback(() => setActiveSheet(null), []);

  const value = useMemo(
    () => ({ chatFade, setChatFade, activeSheet, toggleSheet, setBottomInset }),
    [chatFade, setChatFade, activeSheet, toggleSheet],
  );

  return (
    <NavBarHostContext.Provider value={value}>
      <View style={styles.host}>
        {children}
        <AccessibilitySheet
          open={activeSheet === 'accessibility'}
          onClose={closeSheet}
          bottom={bottomInset}
        />
        <SettingsSheet
          open={activeSheet === 'settings'}
          onClose={closeSheet}
          bottom={bottomInset}
        />
      </View>
    </NavBarHostContext.Provider>
  );
}

/** Lets ChatView fade the shared top bar out while the mobile keyboard lifts the pet circle. */
export function useChatNavFade(
  opacity: Animated.AnimatedInterpolation<number> | Animated.Value | null,
  hidden: boolean,
) {
  const ctx = useContext(NavBarHostContext);
  const setChatFade = ctx?.setChatFade;
  useEffect(() => {
    if (!setChatFade) return;
    if (!opacity) {
      setChatFade(null);
      return;
    }
    setChatFade({ opacity, hidden });
    return () => setChatFade(null);
  }, [setChatFade, opacity, hidden]);
}

export function AppTabBar({ state, navigateToTab, insets }: AppTabBarProps) {
  const { width } = useWindowDimensions();
  const ctx = useContext(NavBarHostContext);
  const setBottomInset = ctx?.setBottomInset;
  useEffect(() => {
    setBottomInset?.(insets.bottom);
  }, [insets.bottom, setBottomInset]);
  const currentName = state.routes[state.index]?.name ?? 'index';
  const active: NavTab = TAB_BY_ROUTE[currentName] ?? 'chat';
  const chatFade = active === 'chat' ? ctx?.chatFade ?? null : null;
  return (
    <Animated.View
      style={[StyleSheet.absoluteFill, chatFade ? { opacity: chatFade.opacity } : null]}
      pointerEvents={chatFade?.hidden ? 'none' : 'box-none'}
    >
      <CloudNavBar
        active={active}
        top={insets.top + GAP}
        screenWidth={width}
        activeSide={ctx?.activeSheet ?? null}
        onAccessibility={() => ctx?.toggleSheet('accessibility')}
        onSettings={() => ctx?.toggleSheet('settings')}
        onSelect={(tab) => {
          const target = state.routes.find((route) => route.name === ROUTE[tab]);
          if (target) navigateToTab(target.key);
        }}
      />
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  host: { flex: 1 },
});
