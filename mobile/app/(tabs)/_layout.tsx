import { Tabs } from 'expo-router';

import { t } from '@/i18n';
import { Icon } from '@/ui/icons/Icon';
import { brand, fonts } from '@/ui/theme/tokens';

function tabColor(color: unknown): string {
  return typeof color === 'string' ? color : brand.inkMuted;
}

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarHideOnKeyboard: true,
        tabBarActiveTintColor: brand.primary,
        tabBarInactiveTintColor: brand.inkMuted,
        tabBarStyle: {
          backgroundColor: brand.card,
          borderTopColor: brand.cardShade,
        },
        tabBarLabelStyle: { fontFamily: fonts.medium, fontSize: 13 },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: t.tabs.chat,
          tabBarIcon: ({ color }) => <Icon name="messagesSquare" size={22} color={tabColor(color)} />,
        }}
      />
      <Tabs.Screen
        name="recorrido"
        options={{
          title: t.tabs.trail,
          tabBarIcon: ({ color }) => <Icon name="map" size={22} color={tabColor(color)} />,
        }}
      />
    </Tabs>
  );
}
