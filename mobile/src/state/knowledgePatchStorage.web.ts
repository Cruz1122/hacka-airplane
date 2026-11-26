export const KNOWLEDGE_PATCH_KEY = 'knowledge-patches-v1';

export function knowledgePatchStorage(key: string) {
  return {
    read: async () => localStorage.getItem(key),
    write: async (value: string) => { localStorage.setItem(key, value); },
  };
}

