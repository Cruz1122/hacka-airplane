// The phone owner's two Pets, one as a guide and one as a visitor: what each wears and in which
// colors. Kept on the device (expo-sqlite kv-store, like settings) and shared by every screen
// through one module store.
// Only this phone sees it for now: the radio does not carry it to the other phones yet.
import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

import {
  defaultTint,
  PET_ACCESSORIES,
  PET_TINTS,
  type PetAccessory,
  type PetTint,
} from '@/ui/pet/petCore';

/** 'role': the hat of the role you pick (guide hat or visitor cap); 'none': bare head. */
export type LookAccessory = PetAccessory | 'role' | 'none';

export interface PetLook {
  accessory: LookAccessory;
  /** null: the accessory's own colors. */
  tint: PetTint | null;
}

export const DEFAULT_LOOK: PetLook = { accessory: 'role', tint: null };

export type PetRole = 'guide' | 'visitor';
export type PetLooks = Record<PetRole, PetLook>;
export const DEFAULT_LOOKS: PetLooks = { guide: DEFAULT_LOOK, visitor: DEFAULT_LOOK };

const KEY = 'petLook.v2';

const isAccessory = (v: unknown): v is LookAccessory =>
  v === 'role' || v === 'none' || (PET_ACCESSORIES as readonly unknown[]).includes(v);
const isTint = (v: unknown): v is PetTint => (PET_TINTS as readonly unknown[]).includes(v);

function lookFrom(v: unknown): PetLook {
  const o = (typeof v === 'object' && v) || {};
  const accessory = 'accessory' in o && isAccessory(o.accessory) ? o.accessory : 'role';
  const tint = 'tint' in o && isTint(o.tint) ? o.tint : null;
  return { accessory, tint };
}

/** Reads the stored looks; anything unknown (damaged or missing) falls back field by field. */
export function parsePetLooks(raw: string | null): PetLooks {
  if (!raw) return DEFAULT_LOOKS;
  let v: unknown;
  try {
    v = JSON.parse(raw);
  } catch {
    return DEFAULT_LOOKS;
  }
  const o = (typeof v === 'object' && v) || {};
  return {
    guide: lookFrom('guide' in o ? o.guide : null),
    visitor: lookFrom('visitor' in o ? o.visitor : null),
  };
}

/** What the Pet wears for a role, after the look's choice. */
export function wornBy(look: PetLook, role: PetRole): { accessory?: PetAccessory; tint?: PetTint } {
  const accessory =
    look.accessory === 'role'
      ? role === 'guide'
        ? 'guideHat'
        : 'visitorCap'
      : look.accessory === 'none'
        ? undefined
        : look.accessory;
  if (!accessory) return {};
  return { accessory, tint: look.tint ?? defaultTint(accessory) };
}

let looks = DEFAULT_LOOKS;
let loaded = false;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

function load() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(KEY).then(
    (raw) => {
      looks = parsePetLooks(raw);
      emit();
    },
    (e: unknown) => console.warn('Could not read the saved Pet look; using the default.', e),
  );
}

export function setPetLook(role: PetRole, patch: Partial<PetLook>) {
  looks = { ...looks, [role]: { ...looks[role], ...patch } };
  emit();
  Storage.setItemAsync(KEY, JSON.stringify(looks)).catch((e: unknown) =>
    console.warn('Could not save the Pet look; it lasts until the app closes.', e),
  );
}

const subscribe = (l: () => void) => {
  load();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};
const read = () => looks;

/** Both looks; `looks[role]` is one role's Pet. */
export const usePetLooks = () => useSyncExternalStore(subscribe, read, read);
