// Group screen UX & accessibility: stop-searching / leave buttons, Android back staying inside
// Grupo's sub-sections instead of jumping to Chat, focus-scoped back handling, and vertical
// centering of the visitor view.
import { ExpoRoot, Stack, usePathname } from 'expo-router';
import { getMockContext } from 'expo-router/build/testing-library/mock-config';
import { act } from 'react';
import { BackHandler, Platform, StyleSheet, Text } from 'react-native';
import { createRoot, type Root, type TestInstance } from 'test-renderer';

import type { GroupInput } from '@/core/group/groupState';
import { memberId, type GuideMember } from '@/core/group/types';
import type { GroupTransport } from '@/group/transport';
import { fill, t } from '@/i18n';
import { PET_NAME } from '@/ui/pet/petCore';

import TabsLayout from '../../../../app/(tabs)/_layout';
import GroupRoute from '../../../../app/(tabs)/group';

jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: { getItemAsync: jest.fn(async () => null), setItemAsync: jest.fn(async () => {}) },
}));

jest.mock('react-native-reanimated', () => {
  const { View } = jest.requireActual('react-native');
  return {
    __esModule: true,
    default: { View },
    useSharedValue: (value: number) => ({
      value,
      set(v: number) {
        this.value = v;
      },
    }),
    useAnimatedStyle: (style: () => object) => style(),
    withTiming: (value: number) => value,
  };
});

jest.mock('react-native-gesture-handler', () => {
  const { View } = jest.requireActual('react-native');
  return {
    GestureHandlerRootView: View,
    GestureDetector: ({ children }: { children: unknown }) => children,
    usePanGesture: () => ({}),
  };
});

jest.mock('@/ui/pet/PetVaporCanvas', () => ({
  PetVaporCanvas: () => null,
}));

jest.mock('@/onboarding/launch', () => ({
  onboardingDone: () => true,
  markOnboardingDone: () => {},
}));

jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => true }));

let mockTransport: GroupTransport;
jest.mock('../../../../modules/group-radio', () => ({
  GroupRadio: { capabilities: () => ({ bluetoothOn: true }) },
}));
jest.mock('@/group/bleTransport', () => ({
  createBleTransport: () => mockTransport,
  ensureRadioPermissions: async () => 'granted',
}));

function makeTransport() {
  let emit: ((e: GroupInput) => void) | null = null;
  let stopped = 0;
  let findControl: {
    signal?: AbortSignal;
    resolve: (guides: GuideMember[]) => void;
  } | null = null;
  const transport: GroupTransport = {
    findSyncingGuides(signal?: AbortSignal) {
      return new Promise((resolve) => {
        findControl = { signal, resolve };
      });
    },
    setSyncMode() {},
    setAlertMeters() {},
    start(_self, onEvent) {
      emit = onEvent;
      return () => {
        emit = null;
        stopped += 1;
      };
    },
  };
  return {
    transport,
    emit: (e: GroupInput) => emit?.(e),
    get stops() {
      return stopped;
    },
    get findControl() {
      return findControl;
    },
  };
}

function ChatStub() {
  return <Text>chat stub</Text>;
}

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
  '(tabs)/index': ChatStub,
  '(tabs)/group': GroupRoute,
};

const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

const mounted: Root[] = [];
afterEach(() => {
  for (const root of mounted.splice(0)) act(() => root.unmount());
  jest.restoreAllMocks();
});

type BackListener = Parameters<typeof BackHandler.addEventListener>[1];

async function openGroup() {
  const listeners: BackListener[] = [];
  jest.spyOn(BackHandler, 'addEventListener').mockImplementation((_event, cb) => {
    listeners.push(cb);
    return {
      remove: () => {
        const i = listeners.indexOf(cb);
        if (i >= 0) listeners.splice(i, 1);
      },
    };
  });

  const root = createRoot();
  mounted.push(root);
  await act(async () =>
    root.render(<ExpoRoot context={getMockContext(routes)} location="/group" />),
  );
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const texts = () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join(''));
  const press = async (node: TestInstance) => act(async () => node.props.onClick(PRESS));
  const byLabel = (label: string) =>
    all((n) => n.props.accessibilityLabel === label && typeof n.props.onClick === 'function');
  const pressLabel = async (label: string) => {
    const matches = byLabel(label);
    expect(matches.length).toBeGreaterThan(0);
    await press(matches[0]);
  };
  const pressTab = async (label: string) => {
    const matches = all(
      (n) =>
        n.props.accessibilityRole === 'tab' &&
        n.props.accessibilityLabel === label &&
        typeof n.props.onClick === 'function',
    );
    const target = matches.find((n) => !n.props.accessibilityState?.selected);
    expect(target).toBeDefined();
    await press(target!);
  };
  /** Dispatches Android hardwareBackPress in LIFO order, returning whether any listener handled it. */
  const hardwareBack = async () => {
    let handled = false;
    await act(async () => {
      for (let i = listeners.length - 1; i >= 0; i--) {
        if (
          listeners[i]({
            type: 'hardwareBackPress',
            timeStamp: 0,
          } as Parameters<BackListener>[0]) === true
        ) {
          handled = true;
          break;
        }
      }
    });
    return handled;
  };
  return {
    all,
    texts,
    has: (text: string) => texts().includes(text),
    path: () => texts().find((s) => s.startsWith('path '))?.slice(5),
    byLabel,
    pressLabel,
    pressTab,
    hardwareBack,
    listenerCount: () => listeners.length,
  };
}

describe('Group screen navigation, stop searching, vertical centering and a11y', () => {
  const originalOs = Platform.OS;

  beforeEach(() => {
    Object.defineProperty(Platform, 'OS', { value: 'android', configurable: true });
  });

  afterEach(() => {
    Object.defineProperty(Platform, 'OS', { value: originalOs, configurable: true });
  });

  it('lets a searching visitor stop searching via button and centers the visitor content vertically', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    await app.pressLabel(t.group.imVisitor);
    expect(app.has(t.group.visitor.searchingTitle)).toBe(true);
    expect(app.byLabel(t.group.cancelSearch)).toHaveLength(1);

    // The visitor content wrapper must vertically center its children (not be defeated by flex: 1).
    const titleNode = app.all(
      (n) => n.type === 'Text' && n.props.children === t.group.visitor.searchingTitle,
    )[0];
    let ancestor: TestInstance | null = titleNode.parent;
    let foundCenteredContainer = false;
    while (ancestor) {
      const flat = StyleSheet.flatten(ancestor.props.style);
      if (flat?.justifyContent === 'center' && flat?.flexGrow === 1) {
        foundCenteredContainer = true;
        break;
      }
      ancestor = ancestor.parent;
    }
    expect(foundCenteredContainer).toBe(true);

    await app.pressLabel(t.group.cancelSearch);
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(harness.stops).toBe(1);
  });

  it('lets a paired visitor leave the group via button', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    await app.pressLabel(t.group.imVisitor);
    await act(async () => {
      harness.emit({
        kind: 'joined',
        member: { id: memberId('g1'), role: 'guide', name: 'Marta', slot: 'front' },
      });
    });
    expect(app.byLabel(t.group.leaveGroup)).toHaveLength(1);

    await app.pressLabel(t.group.leaveGroup);
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(harness.stops).toBe(1);
  });

  it('lets an active guide with visitors leave the group via button', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    await app.pressLabel(t.group.imGuide);
    await act(async () => {
      harness.findControl?.resolve([]);
    });
    await act(async () => {
      harness.emit({
        kind: 'joined',
        member: { id: memberId('v1'), role: 'visitor', name: 'Ana' },
      });
    });
    expect(app.byLabel(t.group.leaveGroup)).toHaveLength(1);

    await app.pressLabel(t.group.leaveGroup);
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(harness.stops).toBe(1);
  });

  it('lets a guide cancel guide discovery and ignores stale discovery results', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    await app.pressLabel(t.group.imGuide);
    expect(app.has(t.group.searchingGuides)).toBe(true);
    expect(app.byLabel(t.group.cancelSearch)).toHaveLength(1);

    await app.pressLabel(t.group.cancelSearch);
    expect(harness.findControl?.signal?.aborted).toBe(true);
    expect(app.has(t.group.searchingGuides)).toBe(false);

    // Resolving the aborted discovery must not transition into GuideView.
    await act(async () => {
      harness.findControl?.resolve([]);
    });
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(app.has(t.group.emptyTitle)).toBe(false);
  });

  it('handles Android back inside every Grupo subsection without jumping to Chat', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    // 1. Open PetCustomizer -> back closes customizer and stays on Grupo.
    await app.pressLabel(fill(t.group.pet.edit.guide, { pet: PET_NAME }));
    expect(app.has(t.group.pet.done)).toBe(true);
    expect(await app.hardwareBack()).toBe(true);
    expect(app.has(t.group.pet.done)).toBe(false);
    expect(app.path()).toBe('/group');

    // 2. Searching for another guide -> back cancels search and stays on ChooseRole.
    await app.pressLabel(t.group.imGuide);
    expect(app.has(t.group.searchingGuides)).toBe(true);
    expect(await app.hardwareBack()).toBe(true);
    expect(app.has(t.group.searchingGuides)).toBe(false);
    expect(app.path()).toBe('/group');

    // 3. GuideView (empty) -> back returns to ChooseRole.
    await app.pressLabel(t.group.imGuide);
    await act(async () => {
      harness.findControl?.resolve([]);
    });
    expect(app.has(t.group.emptyTitle)).toBe(true);
    expect(await app.hardwareBack()).toBe(true);
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(app.path()).toBe('/group');

    // 4. VisitorView -> back returns to ChooseRole.
    await app.pressLabel(t.group.imVisitor);
    expect(app.has(t.group.visitor.searchingTitle)).toBe(true);
    expect(await app.hardwareBack()).toBe(true);
    expect(app.has(t.group.chooseTitle)).toBe(true);
    expect(app.path()).toBe('/group');

    // 5. At top-level ChooseRole (nothing open) -> Grupo lets Tabs handle back and return to Chat.
    expect(await app.hardwareBack()).toBe(true);
    expect(app.path()).toBe('/');
  });

  it('does not intercept Android back while on the Chat tab during an active group session', async () => {
    const harness = makeTransport();
    mockTransport = harness.transport;
    const app = await openGroup();

    await app.pressLabel(t.group.imVisitor);
    expect(app.has(t.group.visitor.searchingTitle)).toBe(true);

    // Switch to Chat tab: Grupo stays mounted, but its BackHandler must detach while unfocused.
    await app.pressTab(t.nav.chat);
    expect(app.path()).toBe('/');
    expect(await app.hardwareBack()).toBe(false);

    // Returning to Grupo still shows the active visitor session.
    await app.pressTab(t.nav.group);
    expect(app.has(t.group.visitor.searchingTitle)).toBe(true);
  });
});
