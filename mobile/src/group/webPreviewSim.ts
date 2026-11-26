// TEMPORARY web-only preview simulator for /group. Lets a reviewer test having a guide,
// visitors, or another guide in the browser where the native Android BLE radio is absent.
// Remove this file and the matching WEB_PREVIEW_SIM block in app/(tabs)/group.tsx before shipping.
import type { GroupInput } from '@/core/group/groupState';
import { GROUP_POLICY } from '@/core/group/policy';
import { dbmAtMeters } from '@/core/group/signal';
import {
  memberId,
  type GuideMember,
  type Member,
  type MemberLook,
  type VisitorMember,
} from '@/core/group/types';

import type { GroupTransport } from './transport';

export type SimVisitorLink = 'none' | 'near' | 'away' | 'lost';

export interface WebPreviewSimSnapshot {
  guideNearby: boolean;
  visitorCount: number;
  hasOtherGuide: boolean;
  visitorLink: SimVisitorLink;
}

export interface WebPreviewSim {
  readonly transport: GroupTransport;
  snapshot(): WebPreviewSimSnapshot;
  subscribe(listener: () => void): () => void;
  toggleGuideNearby(): void;
  addVisitor(): void;
  toggleOtherGuide(): void;
  setVisitorLink(mode: Exclude<SimVisitorLink, 'none'>): void;
  clearPeers(): void;
}

interface SimVisitor {
  member: VisitorMember;
  frontMeters: number;
  rearMeters: number;
}

const VISITOR_PRESETS: readonly {
  name: string;
  frontMeters: number;
  rearMeters: number;
  look: MemberLook;
}[] = [
  { name: 'Sofía', frontMeters: 6, rearMeters: 28, look: { accessory: 'flower', tint: 'lupine' } },
  { name: 'Mateo', frontMeters: 21, rearMeters: 14, look: { accessory: 'beanie', tint: 'sky' } },
  {
    name: 'Valentina',
    frontMeters: 40,
    rearMeters: 6,
    look: { accessory: 'bandana', tint: 'sun' },
  },
  { name: 'Lucas', frontMeters: 11, rearMeters: 22, look: { accessory: 'visitorCap', tint: 'ink' } },
  { name: 'Camila', frontMeters: 26, rearMeters: 10, look: { accessory: 'flower', tint: 'sun' } },
];

const SIM_GUIDE_NAME = 'Carlos';
const SIM_GUIDE_LOOK: MemberLook = { accessory: 'guideHat', tint: 'sun' };
const HEARTBEAT_MS = 2000;
const NEAR_METERS = 5;
const AWAY_METERS = 42;
const GUIDE_GAP_METERS = 20;

export function createWebPreviewSim(): WebPreviewSim {
  const listeners = new Set<() => void>();
  let guideNearby = false;
  let self: Member | null = null;
  let emit: ((e: GroupInput) => void) | null = null;
  let alertMeters: number = GROUP_POLICY.alertMeters.default;
  let visitors: SimVisitor[] = [];
  let otherGuide: GuideMember | null = null;
  let visitorLink: SimVisitorLink = 'none';
  let nextVisitorIndex = 0;

  let cached: WebPreviewSimSnapshot = {
    guideNearby,
    visitorCount: 0,
    hasOtherGuide: false,
    visitorLink,
  };

  const notify = () => {
    cached = {
      guideNearby,
      visitorCount: visitors.length,
      hasOtherGuide: otherGuide !== null,
      visitorLink,
    };
    for (const fn of listeners) fn();
  };

  const simGuideMember = (slot: 'front' | 'rear'): GuideMember => ({
    id: memberId(`web-sim-guide-${slot}`),
    role: 'guide',
    name: SIM_GUIDE_NAME,
    slot,
    alertMeters,
    look: SIM_GUIDE_LOOK,
  });

  const emitSighting = (observer: Member['id'], subject: Member['id'], meters: number) => {
    emit?.({
      kind: 'sighting',
      sighting: { observer, subject, rssi: dbmAtMeters(meters), atMs: Date.now() },
    });
  };

  const emitGuideSightings = () => {
    if (!self || self.role !== 'guide' || !emit) return;
    const front = self.slot === 'front' ? self : otherGuide;
    const rear = self.slot === 'rear' ? self : otherGuide;
    if (otherGuide) {
      emitSighting(self.id, otherGuide.id, GUIDE_GAP_METERS);
    }
    for (const v of visitors) {
      if (front) emitSighting(front.id, v.member.id, v.frontMeters);
      if (rear) emitSighting(rear.id, v.member.id, v.rearMeters);
    }
  };

  const emitVisitorSighting = () => {
    if (!self || self.role !== 'visitor' || !emit) return;
    if (visitorLink !== 'near' && visitorLink !== 'away') return;
    const guide = simGuideMember('front');
    emitSighting(guide.id, self.id, visitorLink === 'near' ? NEAR_METERS : AWAY_METERS);
  };

  const addVisitorInternal = () => {
    if (!self || self.role !== 'guide' || !emit) return;
    const preset = VISITOR_PRESETS[nextVisitorIndex % VISITOR_PRESETS.length];
    const lap = Math.floor(nextVisitorIndex / VISITOR_PRESETS.length);
    const id = memberId(`web-sim-v-${nextVisitorIndex + 1}`);
    nextVisitorIndex += 1;
    const sim: SimVisitor = {
      member: {
        id,
        role: 'visitor',
        name: lap === 0 ? preset.name : `${preset.name} ${lap + 1}`,
        look: preset.look,
      },
      frontMeters: preset.frontMeters,
      rearMeters: preset.rearMeters,
    };
    visitors = [...visitors, sim];
    emit({ kind: 'joined', member: sim.member });
    emitGuideSightings();
  };

  const attachOtherGuideInternal = () => {
    if (!self || self.role !== 'guide' || !emit || otherGuide) return;
    const slot = self.slot === 'front' ? 'rear' : 'front';
    otherGuide = simGuideMember(slot);
    emit({ kind: 'joined', member: otherGuide });
    if (visitors.length === 0) addVisitorInternal();
    else emitGuideSightings();
  };

  const setVisitorLinkInternal = (mode: Exclude<SimVisitorLink, 'none'>) => {
    if (!self || self.role !== 'visitor' || !emit) return;
    const guide = simGuideMember('front');
    visitorLink = mode;
    // Resetting the guide edge lets the reviewer switch near/away/lost immediately without
    // waiting for the 10 s pocket-guard dwell or 12 s unseen timeout.
    emit({ kind: 'left', id: guide.id });
    if (mode === 'near' || mode === 'away') {
      emit({ kind: 'joined', member: guide });
      emitVisitorSighting();
    }
    notify();
  };

  const transport: GroupTransport = {
    async findSyncingGuides() {
      return guideNearby ? [simGuideMember('front')] : [];
    },
    setSyncMode() {},
    setAlertMeters(meters: number) {
      alertMeters = meters;
      emitGuideSightings();
    },
    start(member, onEvent) {
      self = member;
      emit = onEvent;
      visitors = [];
      otherGuide = null;
      visitorLink = 'none';
      nextVisitorIndex = 0;

      let initTimer: ReturnType<typeof setTimeout> | null = null;
      if (guideNearby) {
        initTimer = setTimeout(() => {
          initTimer = null;
          if (!self || !emit) return;
          if (self.role === 'guide') {
            attachOtherGuideInternal();
            notify();
          } else {
            setVisitorLinkInternal('near');
          }
        }, 0);
      }

      const heartbeat = setInterval(() => {
        if (self?.role === 'guide') emitGuideSightings();
        else if (self?.role === 'visitor') emitVisitorSighting();
      }, HEARTBEAT_MS);

      notify();
      return () => {
        if (initTimer !== null) clearTimeout(initTimer);
        clearInterval(heartbeat);
        self = null;
        emit = null;
        visitors = [];
        otherGuide = null;
        visitorLink = 'none';
        notify();
      };
    },
  };

  return {
    transport,
    snapshot: () => cached,
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    toggleGuideNearby() {
      guideNearby = !guideNearby;
      notify();
    },
    addVisitor() {
      addVisitorInternal();
      notify();
    },
    toggleOtherGuide() {
      if (!self || self.role !== 'guide' || !emit) return;
      if (otherGuide) {
        const id = otherGuide.id;
        otherGuide = null;
        emit({ kind: 'left', id });
        emitGuideSightings();
      } else {
        attachOtherGuideInternal();
      }
      notify();
    },
    setVisitorLink(mode) {
      setVisitorLinkInternal(mode);
    },
    clearPeers() {
      if (!emit) return;
      for (const v of visitors) emit({ kind: 'left', id: v.member.id });
      if (otherGuide) emit({ kind: 'left', id: otherGuide.id });
      visitors = [];
      otherGuide = null;
      nextVisitorIndex = 0;
      notify();
    },
  };
}
