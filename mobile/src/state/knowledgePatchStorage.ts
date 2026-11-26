import Storage from 'expo-sqlite/kv-store';

export const KNOWLEDGE_PATCH_KEY = 'knowledge-patches-v1';

export function knowledgePatchStorage(key: string) {
  return {
    read: () => Storage.getItem(key),
    write: (value: string) => Storage.setItem(key, value),
  };
}

