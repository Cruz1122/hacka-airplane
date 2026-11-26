// Dev-only radio spike: open nevados://radio-spike?id=a1 (any two hex digits per phone).
// Starts the BLE beacon + scan service and counts what this phone hears. Every 5 s it writes a
// "JS hb" line to logcat (tag GroupRadio) so a screen-off run shows whether JS still receives
// sightings: `adb logcat -s GroupRadio`.
import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { PermissionsAndroid, Platform, ScrollView, Text } from 'react-native';

import { GroupRadio } from '../modules/group-radio';

const HEARTBEAT_MS = 5000;

async function askPermissions(): Promise<Record<string, string>> {
  const P = PermissionsAndroid.PERMISSIONS;
  const wanted =
    Number(Platform.Version) >= 31
      ? [P.BLUETOOTH_SCAN, P.BLUETOOTH_ADVERTISE, P.BLUETOOTH_CONNECT, P.POST_NOTIFICATIONS]
      : [P.ACCESS_FINE_LOCATION];
  return PermissionsAndroid.requestMultiple(wanted.filter(Boolean));
}

export default function RadioSpike() {
  const { id = '00' } = useLocalSearchParams<{ id?: string }>();
  const [out, setOut] = useState<Record<string, unknown>>(() =>
    GroupRadio ? {} : { error: 'GroupRadio native module missing (web, or an APK built before it)' },
  );

  useEffect(() => {
    const radio = GroupRadio;
    if (!radio) return;
    let total = 0;
    let window = 0;
    const peers: Record<string, { n: number; rssi: number }> = {};
    const sub = radio.addListener('onSighting', (s) => {
      total += 1;
      window += 1;
      const p = (peers[s.payload] ??= { n: 0, rssi: s.rssi });
      p.n += 1;
      p.rssi = s.rssi;
    });
    const timer = setInterval(() => {
      radio.log(`hb id=${id} window=${window} total=${total} peers=${JSON.stringify(peers)}`);
      window = 0;
      setOut((o) => ({ ...o, total, peers: { ...peers }, radio: radio.capabilities() }));
    }, HEARTBEAT_MS);
    askPermissions()
      .then((permissions) => {
        setOut((o) => ({ ...o, id, permissions, before: radio.capabilities() }));
        radio.start(id, true, true);
      })
      .catch((e: unknown) => setOut((o) => ({ ...o, error: String(e) })));
    return () => {
      clearInterval(timer);
      sub.remove();
      radio.stop();
    };
  }, [id]);

  return (
    <ScrollView contentContainerStyle={{ padding: 24 }}>
      <Text selectable style={{ fontFamily: 'monospace' }}>
        {JSON.stringify(out, null, 2)}
      </Text>
    </ScrollView>
  );
}
