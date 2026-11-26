import type { PerformanceReading } from './performanceReading';

export async function readDevicePerformance(): Promise<PerformanceReading> {
  const browserPerformance = performance as Performance & { memory?: { usedJSHeapSize: number } };
  const browser = navigator as Navigator & {
    getBattery?: () => Promise<{ level: number; charging: boolean; dischargingTime: number }>;
  };
  const battery = await browser.getBattery?.().catch(() => undefined);
  return {
    memoryBytes: browserPerformance.memory?.usedJSHeapSize,
    batteryPercent: battery && battery.level * 100,
    batteryPlugged: battery?.charging,
    batteryRemainingSec: battery && !battery.charging && Number.isFinite(battery.dischargingTime)
      ? battery.dischargingTime : undefined,
  };
}
