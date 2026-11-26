import type { PerformanceReading } from './performanceReading';

export async function readDevicePerformance(): Promise<PerformanceReading> {
  const browserPerformance = performance as Performance & { memory?: { usedJSHeapSize: number } };
  return { memoryBytes: browserPerformance.memory?.usedJSHeapSize };
}
