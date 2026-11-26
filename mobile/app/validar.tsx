import { useRouter } from 'expo-router';
import { useCallback, useRef, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import {
  HOUR_MS,
  isStationUnlocked,
  openUntilMs,
  parseStationCode,
} from '@/core/access/parkAccess';
import { fill, t } from '@/i18n';
import { STATION_IDS, type StationId } from '@/recorrido/stations';
import { getParkAccess, recordStationScan } from '@/state/parkAccess';
import { Icon } from '@/ui/icons/Icon';
import { InfoCard } from '@/ui/InfoCard';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { QrCamera } from '@/ui/QrCamera';
import { radius, spacing } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

const labels = t.parkAccess.validate;

type Step =
  | { kind: 'scanning' }
  | { kind: 'done'; until: number; unlocked: StationId | null }
  | { kind: 'invalid' }
  | { kind: 'noCamera' };

const untilText = (ms: number) =>
  new Date(ms).toLocaleString(undefined, {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });

export default function ValidateAccessScreen() {
  const router = useRouter();
  const { palette, scaled } = useAccessibilityTheme();
  // The camera reports the same QR many times per second; only the first one counts.
  const handled = useRef(false);
  const [step, setStep] = useState<Step>({ kind: 'scanning' });

  const scan = useCallback((text: string) => {
    if (handled.current) return;
    handled.current = true;
    const station = parseStationCode(text);
    if (!station) return setStep({ kind: 'invalid' });
    const before = getParkAccess().access;
    const access = recordStationScan(station);
    const unlocked =
      STATION_IDS.find((id) => !isStationUnlocked(before, id) && isStationUnlocked(access, id)) ??
      null;
    const until = openUntilMs(access, getParkAccess().hours * HOUR_MS) ?? Date.now();
    setStep({ kind: 'done', until, unlocked });
  }, []);
  const cameraError = useCallback(() => setStep({ kind: 'noCamera' }), []);
  const rescan = () => {
    handled.current = false;
    setStep({ kind: 'scanning' });
  };

  return (
    <ScrollView style={{ backgroundColor: palette.card }} contentContainerStyle={styles.content}>
      <View style={[styles.badge, { backgroundColor: palette.primary }]} aria-hidden>
        <Icon name="scanLine" size={28} color={palette.onPrimary} />
      </View>
      <Text accessibilityRole="header" style={[scaled.display, { color: palette.ink }]}>
        {labels.heading}
      </Text>
      <Text style={[scaled.body, { color: palette.inkMuted }]}>{labels.body}</Text>
      {step.kind === 'scanning' && <QrCamera onCode={scan} onError={cameraError} />}
      {step.kind === 'done' && (
        <InfoCard
          tone="done"
          icon="circleCheck"
          title={labels.okTitle}
          body={
            fill(labels.ok, { time: untilText(step.until) }) +
            (step.unlocked
              ? ' ' + fill(labels.unlocked, { name: t.trail.stations[step.unlocked].name })
              : '')
          }
        >
          <PrimaryButton label={labels.back} onPress={() => router.back()} />
        </InfoCard>
      )}
      {step.kind === 'invalid' && (
        <InfoCard icon="triangleAlert" title={labels.invalidTitle} body={labels.invalid}>
          <PrimaryButton label={labels.retry} onPress={rescan} />
        </InfoCard>
      )}
      {step.kind === 'noCamera' && (
        <InfoCard icon="camera" title={labels.noCameraTitle} body={labels.noCamera}>
          <PrimaryButton label={labels.retry} onPress={rescan} />
        </InfoCard>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.xl,
    gap: spacing.lg,
    width: '100%',
    maxWidth: 560,
    alignSelf: 'center',
  },
  badge: {
    width: 56,
    height: 56,
    borderRadius: radius.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
