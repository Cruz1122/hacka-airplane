// Wires a transport into the group reducer: joins `self`, feeds every link event, drives the
// 1 s clock (native when the transport provides it, JS interval otherwise), and fires alerts
// synchronously on the JS thread so sound and vibration still trigger with the screen off. Mount
// it per role (key it by self id): the group state belongs to one session.
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Vibration } from 'react-native';

import { alerts, groupOf, step, type GroupInput, type GroupState } from '@/core/group/groupState';
import type { Alert, Member } from '@/core/group/types';

import type { GroupTransport } from './transport';

const TICK_MS = 1000;
const PULSE_MS = 400;
const GAP_MS = 200;

/** `self` as it stands in the group: a guide carries its alert distance. */
const withAlert = (self: Member, alertMeters: number | undefined): Member =>
  self.role === 'guide' && alertMeters !== undefined ? { ...self, alertMeters } : self;

export const alertKey = (a: Alert) => `${a.kind}:${a.id}`;

/**
 * `alertMeters` is a guide's slider (ignored on a visitor phone, which follows its guide's): a
 * change re-joins `self` with it, so the next readings zone with it, and hands it to the radio.
 */
export function useGroup(
  transport: GroupTransport,
  self: Member,
  syncing: boolean,
  alertMeters?: number,
): { state: GroupState; alerts: Alert[] } {
  // The hook is mounted per session (keyed by self id), so the first state is built once here.
  const [state, setState] = useState<GroupState>(() =>
    groupOf(withAlert(self, alertMeters), Date.now()),
  );
  const stateRef = useRef<GroupState>(state);
  const knownRef = useRef<Set<string>>(new Set());

  const handleInput = useCallback(
    (input: GroupInput) => {
      const next = step(stateRef.current, input);
      if (next === stateRef.current) return;
      stateRef.current = next;

      const raisedNow = alerts(next, self.id);
      const keys = new Set(raisedNow.map(alertKey));
      const fresh = [...keys].filter((k) => !knownRef.current.has(k)).length;
      knownRef.current = keys;
      if (fresh > 0) {
        if (transport.alert) {
          transport.alert(fresh);
        } else {
          // One pulse per new alert, so two at once read as two.
          const pattern = [0];
          for (let i = 0; i < fresh; i++) pattern.push(PULSE_MS, GAP_MS);
          Vibration.vibrate(pattern.slice(0, -1));
        }
      }

      setState(next);
    },
    [transport, self.id],
  );

  // Set sync mode and the alert distance before `transport.start` encodes the first beacon.
  useEffect(() => transport.setSyncMode(syncing), [transport, syncing]);
  useEffect(() => {
    if (self.role !== 'guide' || alertMeters === undefined) return;
    transport.setAlertMeters?.(alertMeters);
    handleInput({ kind: 'joined', member: withAlert(self, alertMeters) });
  }, [transport, self, alertMeters, handleInput]);

  useEffect(() => {
    knownRef.current = new Set();
    const stop = transport.start(self, handleInput);
    const timer = transport.nativeTicks
      ? null
      : setInterval(() => handleInput({ kind: 'tick', nowMs: Date.now() }), TICK_MS);
    return () => {
      if (timer !== null) clearInterval(timer);
      stop();
    };
  }, [transport, self, handleInput]);

  const raised = useMemo(() => alerts(state, self.id), [state, self.id]);
  return { state, alerts: raised };
}
