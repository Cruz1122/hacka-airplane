// Port of nevados_bench.fsm.states. Tables come from world.json (generated from Python).
import type { World } from './world';
import { loadWorld } from './world';

export const ROUTER = 'ROUTER';
export const STATION_INFO = 'STATION_INFO';
export const TRAILS = 'TRAILS';
export const ENTRY_REQUIREMENTS = 'ENTRY_REQUIREMENTS';
export const ALTITUDE_SAFETY = 'ALTITUDE_SAFETY';
export const WEATHER_GEAR = 'WEATHER_GEAR';
export const FLORA_FAUNA = 'FLORA_FAUNA';
export const REGULATIONS = 'REGULATIONS';
export const VISIT_REGISTRATION = 'VISIT_REGISTRATION';
export const EMERGENCY = 'EMERGENCY';
export const OUT_OF_SCOPE = 'OUT_OF_SCOPE';
export const CLARIFY = 'CLARIFY';
export const SLOT_FILLING = 'SLOT_FILLING';
export const CONFIRM = 'CONFIRM';
export const EXECUTE = 'EXECUTE';
export const ANSWER = 'ANSWER';

const T = loadWorld().json.states;

export const STATES: readonly string[] = T.all;
export const TOPIC_STATES: readonly string[] = T.topic;
export const TRANSITIONS: Readonly<Record<string, readonly string[]>> = T.transitions;
export const FLOW_STATE: Readonly<Record<string, string>> = T.flow_state;
export const REQUIRED_SLOTS: Readonly<Record<string, readonly string[]>> = T.required_slots;
export const SLOT_LABELS: Readonly<Record<string, string>> = T.slot_labels;
export const SLOT_QUESTIONS: Readonly<Record<string, string>> = T.slot_questions;
export const TOOL_LABELS: Readonly<Record<string, string>> = T.tool_labels;

export function canTransition(src: string, dst: string): boolean {
  return (TRANSITIONS[src] ?? []).includes(dst);
}

/** Throws if consecutive states in `path` are not legal transitions. */
export function checkPath(path: readonly string[]): void {
  for (let i = 1; i < path.length; i++) {
    if (!canTransition(path[i - 1], path[i]))
      throw new Error(`illegal FSM transition ${path[i - 1]} -> ${path[i]}`);
  }
}

/** Intent state a tool belongs to (its first non-ROUTER state). */
export function toolTopic(world: World, toolName: string): string {
  const spec = world.tools.get(toolName);
  const topic = spec?.fsm_states.find((s) => s !== ROUTER);
  if (!topic) throw new Error(`no topic state for tool ${toolName}`);
  return topic;
}

/** Tools visible in `state`, in catalogue order. ROUTER sees every base tool. */
export function visibleTools(world: World, state: string, includeClones = false): string[] {
  const names: string[] = [];
  for (const [name, spec] of world.tools) {
    if (spec.fsm_states.includes(state) && (includeClones || spec.near_duplicate_of === null))
      names.push(name);
  }
  return names;
}
