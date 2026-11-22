export type Role = 'system' | 'user' | 'assistant';

export interface ChatMessage {
  role: Role;
  content: string;
}

// Same fields and semantics as Python schemas.PromptRequest; snake_case is the wire format.
export interface PromptRequest {
  messages: ChatMessage[];
  max_tokens: number;
  json_schema?: Record<string, unknown>;
  tool_choice?: string;
  temperature?: number;
  top_p?: number;
  top_k?: number;
  seed?: number;
  cache_prompt?: boolean;
  extra_body?: Record<string, unknown>;
}

// Subset of Python schemas.Completion, same names.
export interface Completion {
  content: string; // "" when empty, as in Python
  tool_calls?: { name: string; arguments: string }[];
  finish_reason?: string | null;
  prompt_n?: number | null;
  cache_n?: number | null;
  predicted_n?: number | null;
  ttft_ms?: number | null;
  total_ms?: number | null;
  prompt_ms?: number | null;
  predicted_ms?: number | null;
  timeout?: boolean;
  http_error?: string | null;
}

export interface LLMBackend {
  complete(
    req: PromptRequest,
    signal?: AbortSignal,
    /** Called with the full text generated so far; backends that cannot stream ignore it. */
    onText?: (textSoFar: string) => void,
  ): Promise<Completion>;
}

// Python schemas.ToolCall / Case / Gold / ParsedOutput; snake_case as in the fixtures.
export interface ToolCall {
  name: string;
  arguments: Record<string, unknown>;
}

export type CallType = 'route' | 'extract' | 'answer';
export type Decision = 'call' | 'clarify' | 'none';

export interface Gold {
  decision?: Decision | null;
  calls?: ToolCall[];
  acceptable_tools?: string[];
  missing_required?: string[];
  slot_name?: string | null;
  slot_value?: unknown;
  answerable?: boolean | null;
  gold_values?: string[];
  gold_passage_id?: string | null;
  lure_values?: string[];
  prior_values?: string[];
  next_state?: string | null;
}

export interface Case {
  case_id: string;
  suite: string;
  call_type: CallType;
  fsm_state: string;
  user_message: string;
  language?: 'es' | 'en' | 'mixed';
  strata?: string[];
  history: { role: string; content: string }[];
  state_summary: string | null;
  tool_names: string[];
  passage_ids: string[];
  context_level: string | null;
  bundle_id: string | null;
  slot_name: string | null;
  gold?: Gold;
  tags?: Record<string, unknown>;
  priority?: number;
}

export interface ParsedOutput {
  parse_ok: boolean;
  decision: Decision | null;
  calls: ToolCall[];
  slot_value: unknown;
  answer_text: string | null;
  parse_error: string | null;
}
