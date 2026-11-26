// The Chat/Grupo tabs as the user drives them: real tabs layout and cloud bar, stand-in screens.
import { ExpoRoot, Stack, router, useLocalSearchParams, usePathname } from 'expo-router';
import { getMockContext } from 'expo-router/build/testing-library/mock-config';
import { act, useState } from 'react';
import { Pressable, Text } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type Root, type TestInstance } from 'test-renderer';

import { t } from '@/i18n';
import { AppNavBar } from '@/ui/AppNavBar';

import TabsLayout from '../../../app/(tabs)/_layout';

let mockDone = false;
jest.mock('@/onboarding/launch', () => ({
  onboardingDone: () => mockDone,
  markOnboardingDone: () => {
    mockDone = true;
  },
}));

function Chat() {
  return (
    <>
      <Text>chat screen</Text>
      <AppNavBar active="chat" />
    </>
  );
}

/** Stands in for the group screen: local state (a session) and the route's params. */
function Group() {
  const [joined, setJoined] = useState(0);
  const { from } = useLocalSearchParams<{ from?: string }>();
  return (
    <>
      <Text>{`group screen from=${from ?? '-'}`}</Text>
      <Pressable accessibilityRole="button" onPress={() => setJoined((n) => n + 1)}>
        <Text>{`joined ${joined}`}</Text>
      </Pressable>
      <AppNavBar active="group" />
    </>
  );
}

function Onboarding() {
  return (
    <Pressable
      onPress={() => {
        mockDone = true;
        router.replace('/');
      }}
    >
      <Text>onboarding</Text>
    </Pressable>
  );
}

/** The path the router shows, next to the navigator. */
function Path() {
  return <Text>{`path ${usePathname()}`}</Text>;
}

const routes = {
  _layout: () => (
    <>
      <Stack screenOptions={{ headerShown: false }} />
      <Path />
    </>
  ),
  '(tabs)/_layout': TabsLayout,
  '(tabs)/index': Chat,
  '(tabs)/group': Group,
  onboarding: Onboarding,
};

const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

const mounted: Root[] = [];
afterEach(() => {
  for (const root of mounted.splice(0)) act(() => root.unmount());
});

async function open(url: string) {
  const root = createRoot();
  mounted.push(root);
  await act(async () => root.render(<ExpoRoot context={getMockContext(routes)} location={url} />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const texts = () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join(''));
  const press = async (node: TestInstance) => act(async () => node.props.onClick(PRESS));
  const byText = (text: string) => {
    const found = all((n) => n.type === 'Text' && [n.props.children].flat().join('') === text);
    expect(found.length).toBeGreaterThan(0);
    // The Text sits inside its Pressable's View.
    let node: TestInstance | null = found[0];
    while (node && !node.props.onClick) node = node.parent;
    return node!;
  };
  const tab = (label: string) =>
    all((n) => n.props.accessibilityRole === 'tab' && n.props.accessibilityLabel === label).filter(
      (n) => n.props.onClick,
    );
  return {
    path: () => texts().find((s) => s.startsWith('path '))?.slice(5),
    has: (text: string) => texts().includes(text),
    pressText: (text: string) => press(byText(text)),
    // Both tabs stay mounted with their own bar; the visible one is where `label` is not selected.
    pressTab: (label: string) => press(tab(label).find((n) => !n.props.accessibilityState.selected)!),
    back: () => act(async () => router.back()),
  };
}

beforeEach(() => {
  mockDone = false;
});

it('opens on the onboarding, which hands over to the chat with nothing to go back to', async () => {
  const app = await open('/');
  expect(app.path()).toBe('/onboarding');
  await app.pressText('onboarding');
  expect(app.path()).toBe('/');
  // Back from the chat leaves the app instead of reaching the onboarding.
  expect(router.canGoBack()).toBe(false);
});

it('goes back from Grupo to Chat, and back from Chat leaves the app', async () => {
  mockDone = true;
  const app = await open('/');
  await app.pressTab(t.nav.group);
  expect(app.path()).toBe('/group');
  expect(router.canGoBack()).toBe(true);
  await app.back();
  expect(app.path()).toBe('/');
  expect(router.canGoBack()).toBe(false);
});

it('keeps the group session and its params across a trip to the chat', async () => {
  mockDone = true;
  const app = await open('/group?from=link');
  await app.pressText('joined 0');
  await app.pressTab(t.nav.chat);
  expect(app.path()).toBe('/');
  await app.pressTab(t.nav.group);
  expect(app.path()).toBe('/group');
  expect(app.has('joined 1')).toBe(true);
  expect(app.has('group screen from=link')).toBe(true);
});

it('opens a link into Grupo directly, and its Chat tab never shows the onboarding', async () => {
  const app = await open('/group');
  expect(app.path()).toBe('/group');
  await app.pressTab(t.nav.chat);
  expect(app.path()).toBe('/');
  expect(app.has('onboarding')).toBe(false);
});
