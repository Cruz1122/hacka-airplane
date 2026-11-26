// Hold-to-talk dictation via expo-speech-recognition (Android SpeechRecognizer, iOS
// SFSpeechRecognizer, web SpeechRecognition).
import type { DictateCallbacks, VoiceError } from './dictateTypes';

export type { DictateCallbacks, VoiceError };

const LOCALE = 'es-CO';

type SpeechError =
  | 'aborted'
  | 'audio-capture'
  | 'interrupted'
  | 'bad-grammar'
  | 'language-not-supported'
  | 'network'
  | 'no-speech'
  | 'not-allowed'
  | 'service-not-allowed'
  | 'busy'
  | 'client'
  | 'speech-timeout'
  | 'too-many-requests'
  | 'unknown';

type Speech = {
  isRecognitionAvailable(): boolean;
  requestPermissionsAsync(): Promise<{ granted: boolean }>;
  start(options: {
    lang: string;
    interimResults: boolean;
    continuous: boolean;
    maxAlternatives: number;
  }): void;
  stop(): void;
  abort(): void;
  addListener(
    event: 'result',
    listener: (e: { isFinal: boolean; results: { transcript?: string }[] }) => void,
  ): { remove(): void };
  addListener(event: 'nomatch', listener: () => void): { remove(): void };
  addListener(event: 'error', listener: (e: { error: SpeechError }) => void): { remove(): void };
  addListener(event: 'end', listener: () => void): { remove(): void };
};

let cached: Speech | null = null;
let subs: { remove(): void }[] = [];

function speech(): Speech {
  // Loaded on first use so importing the composer does not need the native module (Jest).
  const native: Speech = require('expo-speech-recognition').ExpoSpeechRecognitionModule;
  cached = native;
  return native;
}

function detach() {
  for (const s of subs) s.remove();
  subs = [];
}

function reasonOf(error: SpeechError): VoiceError {
  switch (error) {
    case 'not-allowed':
    case 'service-not-allowed':
      return 'permission';
    case 'no-speech':
    case 'speech-timeout':
    case 'aborted':
      return 'no-speech';
    case 'busy':
      return 'busy';
    case 'language-not-supported':
      return 'unavailable';
    case 'audio-capture':
    case 'interrupted':
    case 'bad-grammar':
    case 'network':
    case 'client':
    case 'too-many-requests':
    case 'unknown':
      return 'failed';
    default: {
      const _never: never = error;
      return _never;
    }
  }
}

export async function startDictate(cb: DictateCallbacks): Promise<void> {
  cancelDictate();
  const native = speech();
  if (!native.isRecognitionAvailable()) {
    cb.onError('unavailable');
    cb.onEnd?.();
    return;
  }
  const permiso = await native.requestPermissionsAsync();
  if (!permiso.granted) {
    cb.onError('permission');
    cb.onEnd?.();
    return;
  }
  subs = [
    native.addListener('result', (event) => {
      const text = event.results[0]?.transcript ?? '';
      cb.onPartial?.(text);
      if (event.isFinal) cb.onResult(text);
    }),
    native.addListener('nomatch', () => {
      cb.onError('no-speech');
    }),
    native.addListener('error', (event) => {
      cb.onError(reasonOf(event.error));
    }),
    native.addListener('end', () => {
      detach();
      cb.onEnd?.();
    }),
  ];
  native.start({
    lang: LOCALE,
    interimResults: true,
    continuous: true,
    maxAlternatives: 1,
  });
}

export function stopDictate() {
  speech().stop();
}

export function cancelDictate() {
  detach();
  if (cached) cached.abort();
}
