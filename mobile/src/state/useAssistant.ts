import { useFocusEffect } from 'expo-router';
import { useCallback, useEffect, useRef, useState } from 'react';

import type { LLMBackend } from '@/core/types';
import { DialogueRun, type StepResult } from '@/core/driver';
import { loadWorld } from '@/core/world';
import { HttpBackend } from '@/llm/http';
import { modelManager } from '@/llm/modelManager';

import type { ChatSource } from '@/ui/chat/citations';

import { recordEffect } from './history';
import { messageSources } from './messageSources';
import { loadSettings, type Settings } from './settings';

const SIDE_EFFECTS = new Set(['register_visit', 'report_emergency']);

type Msg = {
  id: string;
  role: 'user' | 'assistant';
  /** As the model or tool wrote it, citation markers included; the bubble hides them. */
  text: string;
  latencyMs?: number;
  sources?: ChatSource[];
};
type ModelState = { id: string; status: 'missing' | 'loading' | 'ready' | 'error'; error?: string };

let seq = 0;
const nextId = () => `m${++seq}`;

// Backend key -> promise, so a context stays alive across screen focus changes.
let cached: { key: string; backend: Promise<LLMBackend> } | null = null;
function getBackend(s: Settings): Promise<LLMBackend> {
  const key = s.backendKind === 'http' ? `http:${s.httpUrl}` : `device:${s.modelId}`;
  if (cached?.key !== key) {
    const backend =
      s.backendKind === 'http'
        ? Promise.resolve(new HttpBackend(s.httpUrl) as LLMBackend)
        : modelManager.load(s.modelId);
    // Drop failed loads so the next focus retries instead of caching the error.
    backend.catch(() => {
      if (cached?.backend === backend) cached = null;
    });
    cached = { key, backend };
  }
  return cached.backend;
}

const runKey = (s: Settings) =>
  [s.backendKind, s.modelId, s.httpUrl, s.deviceStation, s.answerMode, s.chat].join('|');

export function useAssistant() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState('');
  const [state, setState] = useState('ROUTER');
  const [lastSteps, setLastSteps] = useState<StepResult[]>([]);
  const [model, setModel] = useState<ModelState>({ id: '', status: 'loading' });
  const run = useRef<DialogueRun | null>(null);
  const key = useRef('');
  const seen = useRef(0);

  const init = useCallback(async () => {
    let s: Settings;
    try {
      s = await loadSettings();
    } catch (e) {
      // Corrupt kv-store must reach the UI, not become an unhandled rejection from `void init()`.
      setModel({ id: '', status: 'error', error: e instanceof Error ? e.message : String(e) });
      return;
    }
    if (key.current === runKey(s) && run.current) return;
    key.current = runKey(s);
    run.current = null;
    setMessages([]);
    setState('ROUTER');
    setLastSteps([]);
    setModel({ id: s.modelId, status: 'loading' });
    try {
      if (s.backendKind === 'device' && !(await modelManager.exists(s.modelId))) {
        setModel({ id: s.modelId, status: 'missing' });
        return;
      }
      const backend = await getBackend(s);
      const world = await loadWorld();
      if (key.current !== runKey(s)) return; // settings changed while loading
      run.current = new DialogueRun(world, backend, {
        guards: true,
        deviceStation: s.deviceStation,
        answerMode: s.answerMode,
        chat: s.chat,
        mode: 'uniform',
      });
      seen.current = 0;
      setModel({ id: s.modelId, status: 'ready' });
    } catch (e) {
      setModel({ id: s.modelId, status: 'error', error: e instanceof Error ? e.message : String(e) });
    }
  }, []);

  // Re-read settings whenever the chat regains focus (settings screen may have changed them).
  useFocusEffect(
    useCallback(() => {
      void init();
    }, [init]),
  );
  useEffect(() => () => void (run.current = null), []);

  const send = useCallback(async (text: string) => {
    const r = run.current;
    const t = text.trim();
    if (!r || !t || busy) return;
    setBusy(true);
    setMessages((m) => [...m, { id: nextId(), role: 'user', text: t }]);
    const t0 = Date.now();
    const replyId = nextId();
    const upsert = (msg: Msg) =>
      setMessages((m) => (m.some((x) => x.id === replyId) ? m.map((x) => (x.id === replyId ? msg : x)) : [...m, msg]));
    try {
      // Free-text calls stream into the reply bubble; the final text replaces the draft.
      setDraft('');
      const reply = await r.turn(
        t,
        (soFar) => upsert({ id: replyId, role: 'assistant', text: soFar }),
        setDraft,
      );
      const fresh = r.steps.slice(seen.current);
      seen.current = r.steps.length;
      const retrieved = fresh.flatMap((st) =>
        st.tool_result?.ok ? st.tool_result.passage_ids : [],
      );
      upsert({
        id: replyId,
        role: 'assistant',
        text: reply,
        latencyMs: Date.now() - t0,
        sources: messageSources(reply, r.world, retrieved),
      });
      setLastSteps(fresh);
      setState(r.state);
      for (const st of fresh) {
        const c = st.executed_call;
        if (c && SIDE_EFFECTS.has(c.name)) await recordEffect(c.name, c.arguments, st.tool_result);
      }
    } catch (e) {
      setMessages((m) => [
        ...m,
        { id: nextId(), role: 'assistant', text: `Error: ${e instanceof Error ? e.message : String(e)}` },
      ]);
    } finally {
      setDraft('');
      setBusy(false);
    }
  }, [busy]);

  const reset = useCallback(() => {
    key.current = ''; // forces a fresh DialogueRun; the backend context stays cached
    setMessages([]);
    setLastSteps([]);
    void init();
  }, [init]);

  return { messages, send, reset, busy, draft, state, lastSteps, model };
}
