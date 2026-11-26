import { Linking, PermissionsAndroid, Platform } from 'react-native';

const mockEnsure = jest.fn(async () => 'granted' as const);
jest.mock('@/group/bleTransport', () => ({
  ensureRadioPermissions: () => mockEnsure(),
}));

const mockMic = jest.fn(async () => ({ granted: true }));
jest.mock('expo-speech-recognition', () => ({
  ExpoSpeechRecognitionModule: { requestPermissionsAsync: () => mockMic() },
}));

const mockCaps = jest.fn((): { nfc: 'none' | 'off' | 'on' } => ({ nfc: 'on' }));
jest.mock('../../../modules/group-radio', () => ({
  GroupRadio: { capabilities: () => mockCaps() },
}));

import { requestDevicePermissions, resetDevicePermissionsForTest } from '../devicePermissions';

describe('requestDevicePermissions', () => {
  const os = Platform.OS;

  beforeEach(() => {
    mockEnsure.mockClear();
    mockMic.mockClear();
    mockCaps.mockReset();
    mockCaps.mockReturnValue({ nfc: 'on' });
    resetDevicePermissionsForTest();
    jest.spyOn(PermissionsAndroid, 'request').mockResolvedValue(PermissionsAndroid.RESULTS.GRANTED);
    jest.spyOn(Linking, 'sendIntent').mockClear().mockResolvedValue(undefined);
  });

  afterEach(() => {
    Platform.OS = os;
    jest.restoreAllMocks();
  });

  it('asks for the microphone and Bluetooth, and skips NFC settings when NFC is on', async () => {
    Platform.OS = 'android';
    await requestDevicePermissions();
    expect(mockMic).toHaveBeenCalledTimes(1);
    expect(mockEnsure).toHaveBeenCalledTimes(1);
    expect(PermissionsAndroid.request).toHaveBeenCalledWith('android.permission.NFC');
    expect(Linking.sendIntent).not.toHaveBeenCalled();
  });

  it('opens NFC settings when the chip is switched off', async () => {
    Platform.OS = 'android';
    mockCaps.mockReturnValue({ nfc: 'off' });
    await requestDevicePermissions();
    expect(Linking.sendIntent).toHaveBeenCalledWith('android.settings.NFC_SETTINGS');
  });

  it('asks only for the microphone on iOS', async () => {
    Platform.OS = 'ios';
    await requestDevicePermissions();
    expect(mockMic).toHaveBeenCalledTimes(1);
    expect(mockEnsure).not.toHaveBeenCalled();
    expect(Linking.sendIntent).not.toHaveBeenCalled();
  });
});
