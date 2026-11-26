import { requireOptionalNativeModule } from 'expo';

import type { PerformanceReading } from './performanceReading';

const device = requireOptionalNativeModule<{
  sample(): Promise<PerformanceReading>;
}>('DevicePerformance');

export async function readDevicePerformance(): Promise<PerformanceReading> {
  return device ? device.sample() : {};
}
