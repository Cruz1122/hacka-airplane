import { useEffect, useState } from 'react';
import { AppState, Platform, Pressable, ScrollView, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { fill, t } from '@/i18n';
import { readDevicePerformance } from '@/platform/devicePerformance';
import { batteryPowerW, batteryUsedMah, cpuPercentage, type PerformanceReading } from '@/platform/performanceReading';
import { useKnowledge } from '@/state/useKnowledge';
import { usePerformanceMonitor } from '@/state/performanceMonitor';

import { radius, type } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';

const copy = t.performance;
const SAMPLE_MS = 5_000;
const HISTORY_SIZE = 6;

type Sample = PerformanceReading & { at: number; cpu?: number };
type History = { samples: Sample[]; peak?: number; usedMah?: number };

function useSamples(): History {
  const [history, setHistory] = useState<History>({ samples: [] });

  useEffect(() => {
    let active = false;
    let generation = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let previous: PerformanceReading | undefined;

    async function sample(attempt: number) {
      const reading = await readDevicePerformance().catch((): PerformanceReading => ({}));
      if (!active || attempt !== generation) return;
      const next = { ...reading, at: Date.now(), cpu: cpuPercentage(reading, previous) };
      const discharge = batteryUsedMah(reading, previous);
      previous = reading;
      setHistory(({ samples, peak, usedMah }) => ({
        samples: [...samples.slice(1 - HISTORY_SIZE), next],
        peak: next.memoryBytes == null ? peak : Math.max(peak ?? 0, next.memoryBytes),
        usedMah: discharge === undefined ? usedMah : (usedMah ?? 0) + discharge,
      }));
      timer = setTimeout(() => { void sample(attempt); }, SAMPLE_MS);
    }

    function setActive(next: boolean) {
      if (active === next) return;
      active = next;
      generation += 1;
      clearTimeout(timer);
      previous = undefined;
      if (active) void sample(generation);
    }

    setActive(AppState.currentState === 'active' || AppState.currentState == null);
    const subscription = AppState.addEventListener('change', (state) => setActive(state === 'active'));
    return () => {
      setActive(false);
      subscription.remove();
    };
  }, []);

  return history;
}

const mib = (bytes: number) => Math.round(bytes / 1024 ** 2);

export function PerformanceMonitor() {
  const enabled = usePerformanceMonitor();
  return enabled ? <PerformanceBadge /> : null;
}

function PerformanceBadge() {
  const { top, left } = useSafeAreaInsets();
  const { palette } = useAccessibilityTheme();
  const { samples, peak, usedMah } = useSamples();
  const { height } = useWindowDimensions();
  const [expanded, setExpanded] = useState(false);
  const { rows } = useKnowledge();
  const last = rows.findLast((row) => row.role === 'assistant' && 'timing' in row && row.timing);
  const latency = last && 'timing' in last ? last.timing?.totalMs : undefined;
  const current = samples.at(-1);
  const web = Platform.OS === 'web';
  const memory = current?.memoryBytes == null ? undefined
    : fill(web ? copy.heap : copy.appMemory, { value: mib(current.memoryBytes) });
  const cpu = current?.cpu == null ? undefined : fill(copy.cpu, { value: current.cpu.toFixed(1) });
  const reply = latency === undefined ? undefined : fill(copy.reply, { value: Math.round(latency) });
  const battery = current?.batteryPercent == null ? undefined
    : fill(copy.battery, { value: Math.round(current.batteryPercent) });
  const watts = current && batteryPowerW(current);
  const compact = [memory, battery ?? cpu].filter(Boolean).join(' · ') || reply || copy.title;
  const detail = [
    memory,
    current?.availableBytes != null && current.totalBytes != null
      ? fill(copy.available, { available: mib(current.availableBytes), total: mib(current.totalBytes) }) : undefined,
    cpu,
    current?.processes == null ? undefined : fill(copy.processes, { value: current.processes }),
    current?.pid == null ? undefined : fill(copy.pid, { value: current.pid }),
    current?.threads == null ? undefined : fill(copy.threads, { value: current.threads }),
    peak == null ? undefined : fill(copy.peak, { value: mib(peak) }),
    reply,
  ].filter((value): value is string => !!value);
  const batteryDetail = [
    battery,
    current?.batteryPlugged == null ? undefined : current.batteryPlugged ? copy.plugged : copy.unplugged,
    watts == null ? undefined : fill(copy.batteryPower, { value: watts.toFixed(2) }),
    usedMah == null ? undefined : fill(copy.batteryUsed, { value: usedMah.toFixed(1) }),
    current?.batteryCurrentMa == null ? undefined
      : fill(copy.batteryCurrent, { value: Math.round(current.batteryCurrentMa) }),
    current?.batteryVoltageMv == null ? undefined
      : fill(copy.batteryVoltage, { value: (current.batteryVoltageMv / 1000).toFixed(2) }),
    current?.batteryTemperatureC == null ? undefined
      : fill(copy.batteryTemp, { value: current.batteryTemperatureC.toFixed(1) }),
    current?.batteryRemainingSec == null ? undefined
      : fill(copy.batteryRemaining, { value: Math.ceil(current.batteryRemainingSec / 60) }),
    current?.powerSave == null ? undefined : current.powerSave ? copy.powerSaveOn : copy.powerSaveOff,
  ].filter((value): value is string => !!value);
  const recent = samples
    .filter((sample) => sample.memoryBytes != null || sample.cpu != null || sample.batteryPercent != null)
    .reverse();
  const help = web ? copy.web : memory ? undefined : copy.nativeUnavailable;
  const textColor = { color: palette.ink };
  const color = { backgroundColor: palette.card, borderColor: palette.primarySoft };

  return (
    <View pointerEvents="box-none" style={[styles.overlay, { top: top + 54, left: left + 10 }]}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={copy.title}
        accessibilityState={{ expanded }}
        aria-expanded={expanded}
        onPress={() => setExpanded((value) => !value)}
        style={styles.touch}
      >
        <View style={[styles.badge, color]}>
          <Text style={[styles.metric, textColor]} numberOfLines={1}>{compact}</Text>
        </View>
      </Pressable>
      {expanded && (
        <ScrollView style={[styles.panel, color, { maxHeight: Math.max(120, height - top - 115) }]}
          contentContainerStyle={styles.panelContents} nestedScrollEnabled>
          <Text accessibilityRole="header" style={[type.label, textColor]}>{copy.title}</Text>
          {detail.map((value) => <Text style={[styles.metric, textColor]} key={value}>{value}</Text>)}
          {!!help && <Text style={[styles.metric, { color: palette.inkMuted }]}>{help}</Text>}
          <Text style={[type.caption, textColor]}>{copy.batteryTitle}</Text>
          {batteryDetail.length ? batteryDetail.map((value) => (
            <Text style={[styles.metric, textColor]} key={value}>{value}</Text>
          )) : <Text style={[styles.metric, textColor]}>{copy.batteryUnavailable}</Text>}
          {recent.length > 0 && (
            <>
              <Text style={[type.caption, textColor]}>{copy.recent}</Text>
              {recent.map((value) => {
                const time = new Date(value.at).toLocaleTimeString();
                const values = [time];
                if (value.memoryBytes != null) values.push(fill(copy.mib, { value: mib(value.memoryBytes) }));
                if (value.cpu != null) values.push(fill(copy.cpu, { value: value.cpu.toFixed(1) }));
                if (value.batteryPercent != null) values.push(fill(copy.battery, { value: Math.round(value.batteryPercent) }));
                const power = batteryPowerW(value);
                if (power != null) values.push(fill(copy.watts, { value: power.toFixed(2) }));
                return <Text style={[styles.metric, textColor]} key={value.at}>{values.join(' · ')}</Text>;
              })}
            </>
          )}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: { position: 'absolute', zIndex: 10, alignItems: 'flex-start', maxWidth: '90%' },
  touch: { minHeight: 44, justifyContent: 'center' },
  badge: { paddingHorizontal: 9, paddingVertical: 4, borderRadius: radius.pill, borderWidth: 1 },
  panel: { borderRadius: radius.md, borderWidth: 1, maxWidth: 300 },
  panelContents: { gap: 4, padding: 12 },
  metric: { ...type.caption, fontSize: 11, lineHeight: 16, fontVariant: ['tabular-nums'] },
});
