// JS face of the local `GroupRadio` native module (Android only): BLE beacon + scan held by a
// foreground service, plus NFC tap pairing (the guide's phone emulates a card, the visitor's reads
// it). Null on web and on builds made before the module existed.
import { requireOptionalNativeModule } from 'expo';

export interface RadioCapabilities {
  sdk: number;
  bluetoothOn: boolean;
  /** False when the chipset cannot advertise: the phone can listen but not be seen. */
  canAdvertise: boolean;
  running: boolean;
  lastError: string | null;
  /** No NFC controller, NFC switched off in settings, or ready. */
  nfc: 'none' | 'off' | 'on';
  /** LE Coded PHY + extended advertising: the service adds a long-range coded beacon and scans
   *  both PHYs. False while Bluetooth is off. */
  codedPhy: boolean;
}

export interface RadioSighting {
  /** The beacon's bytes after the company id, hex. */
  payload: string;
  rssi: number;
  /** Primary PHY the packet arrived on: the legacy 1M beacon or the long-range coded one. */
  phy: '1m' | 'coded';
  /** Receiving phone's clock, ms since epoch. */
  atMs: number;
}

export interface RadioTick {
  /** Receiving phone's clock, ms since epoch. */
  atMs: number;
}

export interface RadioNfcCard {
  /** The guide card's answer to SELECT AID without the status word, hex. */
  payload: string;
  /** Receiving phone's clock, ms since epoch. */
  atMs: number;
}

export interface GroupRadioModule {
  capabilities(): RadioCapabilities;
  /** `payloadHex`: up to 22 bytes broadcast after the magic prefix. */
  start(payloadHex: string, advertise: boolean, scan: boolean): void;
  /** Replaces the advertised payload without restarting the scan. */
  updatePayload(payloadHex: string): void;
  stop(): void;
  /** Plays the native alert tone and vibration (works with the screen off). */
  alert(count: number): void;
  /** Bytes the NFC card answers a SELECT with (hex); null makes it answer "not found". */
  setNfcCard(payloadHex: string | null): void;
  /** Polls for a guide's card while this app's activity is in the foreground; emits onNfcCard. */
  startNfcReader(): void;
  stopNfcReader(): void;
  /** Writes to logcat (tag GroupRadio): Metro is not reachable on an untethered phone. */
  log(message: string): void;
  addListener(event: 'onSighting', listener: (s: RadioSighting) => void): { remove(): void };
  addListener(event: 'onTick', listener: (t: RadioTick) => void): { remove(): void };
  addListener(event: 'onNfcCard', listener: (c: RadioNfcCard) => void): { remove(): void };
}

export const GroupRadio = requireOptionalNativeModule<GroupRadioModule>('GroupRadio');
