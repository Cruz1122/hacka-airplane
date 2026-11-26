const mockSpeech = {
  maxSpeechInputLength: 4000,
  speak: jest.fn(),
  stop: jest.fn(),
};

jest.mock('expo-speech', () => mockSpeech);

import { getSpeakingKey, toggleSpeak } from '../speak';

describe('speak', () => {
  beforeEach(() => {
    mockSpeech.speak.mockReset();
    mockSpeech.stop.mockReset();
  });

  it('speaks the reply in Colombian Spanish', () => {
    toggleSpeak('a1', 'Hay refugio', jest.fn());
    expect(mockSpeech.stop).toHaveBeenCalled();
    expect(mockSpeech.speak).toHaveBeenCalledWith('Hay refugio', {
      language: 'es-CO',
      pitch: 1,
      rate: 1,
      volume: 1,
      onDone: expect.any(Function),
      onStopped: expect.any(Function),
      onError: expect.any(Function),
    });
    expect(getSpeakingKey()).toBe('a1');
    mockSpeech.speak.mock.calls[0][1].onDone();
    expect(getSpeakingKey()).toBeNull();
  });

  it('stops when the same reply is toggled again', () => {
    toggleSpeak('a1', 'Hay refugio', jest.fn());
    mockSpeech.stop.mockClear();
    toggleSpeak('a1', 'Hay refugio', jest.fn());
    expect(mockSpeech.stop).toHaveBeenCalled();
    expect(mockSpeech.speak).toHaveBeenCalledTimes(1);
  });
});
