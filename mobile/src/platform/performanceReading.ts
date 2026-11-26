export interface PerformanceReading {
  memoryBytes?: number | null;
  availableBytes?: number | null;
  totalBytes?: number | null;
  cpuMs?: number;
  elapsedMs?: number;
  cores?: number;
  pid?: number;
  threads?: number | null;
  processes?: number | null;
  batteryPercent?: number | null;
  batteryPlugged?: boolean | null;
  batteryCurrentMa?: number | null;
  batteryChargeMah?: number | null;
  batteryVoltageMv?: number | null;
  batteryTemperatureC?: number | null;
  batteryRemainingSec?: number;
  powerSave?: boolean | null;
}

export function batteryPowerW(reading: PerformanceReading) {
  const { batteryPlugged, batteryCurrentMa, batteryVoltageMv } = reading;
  if (batteryPlugged !== false || batteryCurrentMa == null || batteryCurrentMa > 0 ||
      !batteryVoltageMv) return undefined;
  return Math.abs(batteryCurrentMa) * batteryVoltageMv / 1_000_000;
}

export function batteryUsedMah(current: PerformanceReading, previous?: PerformanceReading) {
  if (current.batteryPlugged !== false || previous?.batteryPlugged !== false ||
      current.batteryChargeMah == null || previous.batteryChargeMah == null) return undefined;
  return Math.max(0, previous.batteryChargeMah - current.batteryChargeMah);
}

export function cpuPercentage(current: PerformanceReading, previous?: PerformanceReading) {
  if (current.cpuMs === undefined || current.elapsedMs === undefined || !current.cores ||
      previous?.cpuMs === undefined || previous.elapsedMs === undefined) return undefined;
  const elapsed = current.elapsedMs - previous.elapsedMs;
  const cpu = current.cpuMs - previous.cpuMs;
  // Normalize to Android's available logical CPUs. The first reading only supplies a baseline.
  if (elapsed <= 0 || cpu < 0) return undefined;
  return Math.min(100, (100 * cpu) / (elapsed * current.cores));
}
