// Sources the visitor saved from the SourcesSheet. Persisted locally via expo-sqlite/kv-store
// and shared across the app through one external store.
import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

import type { ChatSource } from '@/ui/chat/citations';

const KEY = 'chat.favoriteSources.v1';

export interface FavoriteSource {
  key: string;
  title: string;
  url?: string;
  date?: string;
  excerpt?: string;
}

/** Stable identity for a saved source: its URL when present, otherwise its catalog id. */
export const sourceFavoriteKey = (source: Pick<ChatSource, 'id' | 'url'>): string =>
  source.url?.trim() || source.id;

export function parseFavoriteSources(raw: string | null): FavoriteSource[] {
  if (!raw) return [];
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    const seen = new Set<string>();
    const out: FavoriteSource[] = [];
    for (const item of parsed) {
      if (!item || typeof item !== 'object') continue;
      const row = item as Record<string, unknown>;
      if (typeof row.key !== 'string' || !row.key || typeof row.title !== 'string') continue;
      if (seen.has(row.key)) continue;
      seen.add(row.key);
      out.push({
        key: row.key,
        title: row.title,
        ...(typeof row.url === 'string' ? { url: row.url } : undefined),
        ...(typeof row.date === 'string' ? { date: row.date } : undefined),
        ...(typeof row.excerpt === 'string' ? { excerpt: row.excerpt } : undefined),
      });
    }
    return out;
  } catch {
    return [];
  }
}

let favorites: FavoriteSource[] = [];
let loaded = false;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

function load() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(KEY).then(
    (raw) => {
      if (favorites.length === 0) {
        favorites = parseFavoriteSources(raw);
        emit();
      }
    },
    (e: unknown) => console.warn('Could not read saved favorite sources.', e),
  );
}

function persist(next: FavoriteSource[]) {
  favorites = next;
  emit();
  Storage.setItemAsync(KEY, JSON.stringify(next)).catch((e: unknown) =>
    console.warn('Could not save favorite sources.', e),
  );
}

export function toggleFavoriteSource(source: ChatSource) {
  const key = sourceFavoriteKey(source);
  const exists = favorites.some((f) => f.key === key);
  if (exists) {
    persist(favorites.filter((f) => f.key !== key));
  } else {
    persist([
      {
        key,
        title: source.title,
        ...(source.url ? { url: source.url } : undefined),
        ...(source.date ? { date: source.date } : undefined),
        ...(source.excerpt ? { excerpt: source.excerpt } : undefined),
      },
      ...favorites,
    ]);
  }
}

/** Test helper to reset module state between suites. */
export function resetFavoriteSourcesForTest() {
  favorites = [];
  loaded = true;
  emit();
}

const subscribe = (l: () => void) => {
  load();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};
const read = (): readonly FavoriteSource[] => favorites;

export const useFavoriteSources = () => useSyncExternalStore(subscribe, read, read);
