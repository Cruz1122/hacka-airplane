const listeners: Record<string, ((ev?: unknown) => void)[]> = {};

jest.mock('expo-speech-recognition', () => {
  const ExpoSpeechRecognitionModule = {
    isRecognitionAvailable: jest.fn(() => true),
    requestPermissionsAsync: jest.fn(async () => ({ granted: true })),
    start: jest.fn(),
    stop: jest.fn(),
    abort: jest.fn(),
    addListener: jest.fn((event: string, listener: (ev?: unknown) => void) => {
      listeners[event] = listeners[event] ?? [];
      listeners[event].push(listener);
      return {
        remove: () => {
          listeners[event] = (listeners[event] ?? []).filter((l) => l !== listener);
        },
      };
    }),
  };
  return { ExpoSpeechRecognitionModule };
});

import { ExpoSpeechRecognitionModule } from 'expo-speech-recognition';

import { startDictate, stopDictate } from '../dictate';

function emit(event: string, payload?: unknown) {
  for (const l of listeners[event] ?? []) l(payload);
}

describe('dictate', () => {
  beforeEach(() => {
    for (const key of Object.keys(listeners)) delete listeners[key];
    (ExpoSpeechRecognitionModule.isRecognitionAvailable as jest.Mock).mockReturnValue(true);
    (ExpoSpeechRecognitionModule.requestPermissionsAsync as jest.Mock).mockResolvedValue({
      granted: true,
    });
    (ExpoSpeechRecognitionModule.start as jest.Mock).mockClear();
    (ExpoSpeechRecognitionModule.stop as jest.Mock).mockClear();
    (ExpoSpeechRecognitionModule.abort as jest.Mock).mockClear();
  });

  it('requests permission then starts native recognition in es-CO', async () => {
    await startDictate({ onResult: jest.fn(), onError: jest.fn() });
    expect(ExpoSpeechRecognitionModule.requestPermissionsAsync).toHaveBeenCalled();
    expect(ExpoSpeechRecognitionModule.start).toHaveBeenCalledWith({
      lang: 'es-CO',
      interimResults: true,
      continuous: true,
      maxAlternatives: 1,
    });
  });

  it('forwards a final transcript', async () => {
    const onResult = jest.fn();
    await startDictate({ onResult, onError: jest.fn() });
    emit('result', { isFinal: true, results: [{ transcript: 'hay refugio' }] });
    expect(onResult).toHaveBeenCalledWith('hay refugio');
  });

  it('maps permission denial without starting', async () => {
    (ExpoSpeechRecognitionModule.requestPermissionsAsync as jest.Mock).mockResolvedValue({
      granted: false,
    });
    const onError = jest.fn();
    await startDictate({ onResult: jest.fn(), onError });
    expect(onError).toHaveBeenCalledWith('permission');
    expect(ExpoSpeechRecognitionModule.start).not.toHaveBeenCalled();
  });

  it('maps recognizer errors', async () => {
    const onError = jest.fn();
    await startDictate({ onResult: jest.fn(), onError });
    const cases: [string, string][] = [
      ['not-allowed', 'permission'],
      ['no-speech', 'no-speech'],
      ['busy', 'busy'],
      ['network', 'failed'],
    ];
    for (const [error, reason] of cases) {
      onError.mockClear();
      emit('error', { error, message: error });
      expect(onError).toHaveBeenCalledWith(reason);
    }
  });

  it('stop asks the native module to finalize', async () => {
    await startDictate({ onResult: jest.fn(), onError: jest.fn() });
    stopDictate();
    expect(ExpoSpeechRecognitionModule.stop).toHaveBeenCalled();
  });
});
