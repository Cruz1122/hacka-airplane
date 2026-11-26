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
