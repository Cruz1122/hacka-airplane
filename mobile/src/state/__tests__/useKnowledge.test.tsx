import type { KnowledgeChatState } from '../knowledgeChat';

// Fonts never finish under Jest, so the root layout renders nothing but still runs its effects.
jest.mock('expo-font', () => ({ useFonts: () => [false, null] }));
jest.mock('expo-router', () => ({ Stack: { Screen: () => null } }));

let mockSettle: { resolve: (rt: unknown) => void; reject: (e: unknown) => void } | undefined;
const mockLoad = jest.fn(
  () =>
    new Promise((resolve, reject) => {
      mockSettle = { resolve, reject };
    }),
);
jest.mock('@/llm/knowledgeRuntime', () => ({
  loadKnowledgeRuntime: () => mockLoad(),
  degradedKnowledgeEngine: () => ({
    ask: () => Promise.reject(new Error('degraded')),
  }),
}));

/** A fresh module graph per test (React and the renderer too): the store is one per process. */
function modules() {
  let out!: {
    act: typeof import('react').act;
    createRoot: typeof import('test-renderer').createRoot;
    RootLayout: () => React.ReactNode;
    useKnowledge: typeof import('../useKnowledge').useKnowledge;
  };
  jest.isolateModules(() => {
    /* eslint-disable @typescript-eslint/no-require-imports -- isolateModules loads with require */
    out = {
      act: require('react').act,
      createRoot: require('test-renderer').createRoot,
      RootLayout: require('../../../app/_layout').default,
      useKnowledge: require('../useKnowledge').useKnowledge,
    };
    /* eslint-enable @typescript-eslint/no-require-imports */
  });
  return out;
}

describe('knowledge preload', () => {
  beforeEach(() => {
    mockLoad.mockClear();
    mockSettle = undefined;
  });

  it('starts at app launch and the chat reuses that one load', async () => {
    const { act, createRoot, RootLayout, useKnowledge } = modules();
    const root = createRoot();
    act(() => root.render(<RootLayout />));
    expect(mockLoad).toHaveBeenCalledTimes(1);

    let seen: KnowledgeChatState['status'] | undefined;
    function Chat() {
      seen = useKnowledge().status;
      return null;
    }
    const chat = createRoot();
    act(() => chat.render(<Chat />));
    expect(seen).toBe('loading');
    expect(mockLoad).toHaveBeenCalledTimes(1);

    await act(async () => mockSettle!.resolve({ engine: { ask: jest.fn() } }));
    expect(seen).toBe('ready');
    expect(mockLoad).toHaveBeenCalledTimes(1);
    act(() => {
      chat.unmount();
      root.unmount();
    });
  });

  it('keeps answering safety rules on a failed load and logs the cause', async () => {
    const warn = jest.spyOn(console, 'warn').mockImplementation(() => {});
    const { act, createRoot, RootLayout, useKnowledge } = modules();
    const root = createRoot();
    let seen: KnowledgeChatState | undefined;
    function Chat() {
      seen = useKnowledge();
      return null;
    }
    act(() =>
      root.render(
        <>
          <RootLayout />
          <Chat />
        </>,
      ),
    );
    const cause = new Error('e5 GGUF missing');
    await act(async () => mockSettle!.reject(cause));
    expect(seen?.status).toBe('degraded');
    expect(seen?.error).toBe('e5 GGUF missing');
    expect(warn).toHaveBeenCalledWith(expect.stringContaining('Knowledge runtime'), cause);
    expect(mockLoad).toHaveBeenCalledTimes(1);
    act(() => root.unmount());
    warn.mockRestore();
  });
});
