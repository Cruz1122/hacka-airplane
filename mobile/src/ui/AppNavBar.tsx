// CloudNavBar wired to the Chat/Grupo tabs (app/(tabs)/_layout.tsx): under the status bar,
// switching tabs inside the tab navigator so each tab keeps its state and params.
import { useNavigation } from 'expo-router';
import { useWindowDimensions } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { CloudNavBar, type NavTab } from './CloudNavBar';

/** Route name of each tab in the tabs layout. */
const ROUTE = { chat: 'index', group: 'group' } as const;

/** Gap between the safe area and the bar. */
const GAP = 2;

interface TabNavigation {
  // `merge` keeps the tab's params (e.g. the chat's sceneTime); without it a
  // switch clears them and the group would rebuild its radio mid-session.
  navigate(options: { name: string; merge: true }): void;
}

export function AppNavBar({ active }: { active: NavTab }) {
  const insets = useSafeAreaInsets();
  const { width } = useWindowDimensions();
  const navigation = useNavigation<TabNavigation>();
  return (
    <CloudNavBar
      active={active}
      top={insets.top + GAP}
      screenWidth={width}
      onSelect={(tab) => {
        if (tab !== 'route') navigation.navigate({ name: ROUTE[tab], merge: true });
      }}
    />
  );
}
