// Knowledge updates between phones over Bluetooth (Android 10+), with no QR code: the sharer
// advertises an offer, a receiver lists nearby offers, connects and reads one bundle. Web and
// older builds have no radio and keep the QR series.
import { Platform } from 'react-native';

import {
  decodeKnowledgeBundle,
  encodeKnowledgeBundle,
  type KnowledgePatch,
} from '@/core/knowledge/qrPatch';
import { ensureRadioPermissions } from '@/group/bleTransport';
import { GroupRadio, type ShareOffer } from '../../modules/group-radio';

export type { ShareOffer };

const permissionError = 'Permite el acceso a dispositivos cercanos para usar Bluetooth.';

export function bluetoothShareAvailable(): boolean {
  if (Platform.OS !== 'android' || !GroupRadio) return false;
  return GroupRadio.capabilities().knowledgeLink === true;
}

function radio() {
  if (!GroupRadio) throw new Error('Este teléfono no tiene Bluetooth disponible para la app.');
  return GroupRadio;
}

/** Serves the update to every nearby receiver; the returned function stops sharing. */
export async function startBluetoothShare(
  patches: readonly KnowledgePatch[],
  onSent: (receivers: number) => void,
): Promise<() => void> {
  const bundle = encodeKnowledgeBundle(patches);
  const r = radio();
  if ((await ensureRadioPermissions()) !== 'granted') throw new Error(permissionError);
  const sub = r.addListener('onShareSent', ({ receivers }) => onSent(receivers));
  try {
    await r.shareStart(bundle, patches.length);
  } catch (cause) {
    sub.remove();
    throw cause;
  }
  return () => {
    sub.remove();
    r.shareStop();
  };
}

/** Lists offers as they are heard; the returned function stops scanning. */
export async function findBluetoothShares(
  onOffer: (offer: ShareOffer) => void,
): Promise<() => void> {
  const r = radio();
  if ((await ensureRadioPermissions()) !== 'granted') throw new Error(permissionError);
  const sub = r.addListener('onShareOffer', onOffer);
  const error = r.findShares();
  if (error) {
    sub.remove();
    throw new Error(error);
  }
  return () => {
    sub.remove();
    r.stopFindShares();
  };
}

export async function receiveBluetoothShare(address: string): Promise<KnowledgePatch[]> {
  let payload: string;
  try {
    payload = await radio().receiveShare(address);
  } catch (cause) {
    const detail = cause instanceof Error ? cause.message : String(cause);
    throw new Error(
      'No se pudo recibir por Bluetooth. Acércate al otro teléfono e inténtalo de nuevo. (' +
        detail +
        ')',
    );
  }
  return decodeKnowledgeBundle(payload);
}
