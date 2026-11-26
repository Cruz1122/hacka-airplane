export type VoiceError = 'unavailable' | 'permission' | 'no-speech' | 'busy' | 'failed';

export interface DictateCallbacks {
  onPartial?: (text: string) => void;
  onResult: (text: string) => void;
  onError: (reason: VoiceError) => void;
  onEnd?: () => void;
}
