// Device text-to-speech for an assistant reply (`expo-speech`: Android/iOS/Web engines).
type SpeechApi = {
  maxSpeechInputLength: number;
  speak: (
    text: string,
    options: {
      language?: string;
      pitch?: number;
      rate?: number;
      volume?: number;
      onDone?: () => void;
      onStopped?: () => void;
      onError?: (error: Error) => void;
    },
  ) => void;
  stop: () => void | Promise<void>;
};

function speech(): SpeechApi {
  // Loaded on first tap so importing a bubble does not need the native module (Jest).
  return require('expo-speech') as SpeechApi;
}

let speakingKey: string | null = null;
const listeners = new Set<() => void>();

function emit() {
  for (const l of listeners) l();
}

function clearIf(key: string) {
  if (speakingKey === key) speakingKey = null;
  emit();
}

export function subscribeSpeak(onStoreChange: () => void) {
  listeners.add(onStoreChange);
  return () => {
    listeners.delete(onStoreChange);
  };
}

export function getSpeakingKey() {
  return speakingKey;
}

export function toggleSpeak(key: string, text: string, onError: (error: Error) => void) {
  const Speech = speech();
  if (speakingKey === key) {
    void Speech.stop();
    return;
  }
  void Speech.stop();
  speakingKey = key;
  emit();
  const clipped =
    text.length > Speech.maxSpeechInputLength ? text.slice(0, Speech.maxSpeechInputLength) : text;
  Speech.speak(clipped, {
    language: 'es-CO',
    pitch: 1,
    rate: 1,
    volume: 1,
    onDone: () => clearIf(key),
    onStopped: () => clearIf(key),
    onError: (error) => {
      clearIf(key);
      onError(error);
    },
  });
}
