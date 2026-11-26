// Asks for the radios and the microphone once per launch, from inside the app.
// Bluetooth and the microphone are runtime permissions. NFC is granted with the install;
// when the chip is switched off, Android has no permission dialog, so we open its settings.
import { Linking, PermissionsAndroid, Platform, type Permission } from 'react-native';

import { ensureRadioPermissions } from '@/group/bleTransport';

import { GroupRadio } from '../../modules/group-radio';

const NFC: Permission = 'android.permission.NFC' as Permission;

let pending: Promise<void> | null = null;

export function resetDevicePermissionsForTest(): void {
  pending = null;
}

export function requestDevicePermissions(): Promise<void> {
  if (Platform.OS === 'web') return Promise.resolve();
  if (!pending) pending = run();
  return pending;
}

async function run(): Promise<void> {
  await requestMicrophone();
  if (Platform.OS !== 'android') return;
  try {
    await ensureRadioPermissions();
  } catch (cause) {
    console.warn('Could not ask for Bluetooth.', cause);
  }
  await requestNfc();
}

async function requestMicrophone(): Promise<void> {
  try {
    const native = require('expo-speech-recognition').ExpoSpeechRecognitionModule as {
      requestPermissionsAsync: () => Promise<unknown>;
    };
    await native.requestPermissionsAsync();
  } catch (cause) {
    console.warn('Could not ask for the microphone.', cause);
  }
}

async function requestNfc(): Promise<void> {
  try {
    await PermissionsAndroid.request(NFC);
  } catch (cause) {
    console.warn('Could not ask for NFC.', cause);
  }
  if (GroupRadio?.capabilities().nfc !== 'off') return;
  try {
    await Linking.sendIntent('android.settings.NFC_SETTINGS');
  } catch (cause) {
    console.warn('Could not open NFC settings.', cause);
  }
}
