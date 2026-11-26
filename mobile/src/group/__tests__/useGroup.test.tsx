// The hook as the guide screen drives it: a fake radio records what it is told.
import { act } from 'react';
import { createRoot, type Root } from 'test-renderer';

import type { GroupState } from '@/core/group/groupState';
import { alertMetersOf } from '@/core/group/groupState';
import { memberId, type Member } from '@/core/group/types';

import type { GroupTransport } from '../transport';
import { useGroup } from '../useGroup';

const guide: Member = { id: memberId('g'), role: 'guide', name: 'Ana', slot: 'front' };
const visitor: Member = { id: memberId('v'), role: 'visitor', name: 'Tomás' };

function fakeRadio() {
  const calls: string[] = [];
  const transport: GroupTransport = {
    findSyncingGuides: async () => [],
    setSyncMode: () => {},
    setAlertMeters: (m) => calls.push(`alert ${m}`),
    start: (self) => {
      calls.push(`start ${self.id}`);
      return () => calls.push('stop');
    },
  };
  return { transport, calls };
}

let root: Root | null = null;
afterEach(() => {
  act(() => root?.unmount());
  root = null;
});

function mount(transport: GroupTransport, self: Member, alertMeters: number) {
  let state: GroupState | null = null;
  function Probe({ meters }: { meters: number }) {
    state = useGroup(transport, self, true, meters).state;
    return null;
  }
  root = createRoot();
  act(() => root!.render(<Probe meters={alertMeters} />));
  return {
    state: () => state!,
    slide: (meters: number) => act(() => root!.render(<Probe meters={meters} />)),
  };
}

describe('useGroup alert distance', () => {
  it("a guide's slider reaches the radio before it starts, then re-zones without a restart", () => {
    const { transport, calls } = fakeRadio();
    const hook = mount(transport, guide, 30);
    expect(calls).toEqual(['alert 30', 'start g']);
    expect(alertMetersOf(hook.state())).toBe(30);

    hook.slide(60);
    expect(calls).toEqual(['alert 30', 'start g', 'alert 60']);
    expect(alertMetersOf(hook.state())).toBe(60);
  });

  it('a visitor phone never sets a distance of its own', () => {
    const { transport, calls } = fakeRadio();
    const hook = mount(transport, visitor, 60);
    expect(calls).toEqual(['start v']);
    expect(alertMetersOf(hook.state())).toBe(30);
  });
});
