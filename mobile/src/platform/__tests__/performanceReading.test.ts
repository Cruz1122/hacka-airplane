import { batteryPowerW, batteryUsedMah, cpuPercentage } from '../performanceReading';

test('reports a process share of CPU capacity using the elapsed sample interval', () => {
  const first = { cpuMs: 100, elapsedMs: 1_000, cores: 4 };
  const next = { cpuMs: 1_100, elapsedMs: 6_000, cores: 4 };
  expect(cpuPercentage(first)).toBeUndefined();
  expect(cpuPercentage(next, first)).toBe(5);
  expect(cpuPercentage(next, next)).toBeUndefined();
  expect(cpuPercentage(first, next)).toBeUndefined();
  expect(cpuPercentage({ ...next, cpuMs: first.cpuMs }, first)).toBe(0);
});

test('reports device discharge only when unplugged and backed by battery readings', () => {
  const reading = { batteryPlugged: false, batteryCurrentMa: -400, batteryVoltageMv: 3_950, batteryChargeMah: 900 };
  const prev = { ...reading, batteryChargeMah: 901.5 };
  expect(batteryPowerW(reading)).toBeCloseTo(1.58);
  expect(batteryPowerW({ ...reading, batteryPlugged: true })).toBeUndefined();
  expect(batteryPowerW({ ...reading, batteryCurrentMa: 20 })).toBeUndefined();
  expect(batteryPowerW({ batteryPlugged: false, batteryPercent: 70 })).toBeUndefined();
  expect(batteryUsedMah(reading, prev)).toBe(1.5);
  expect(batteryUsedMah(prev, reading)).toBe(0);
  expect(batteryUsedMah(reading, { ...prev, batteryPlugged: true })).toBeUndefined();
});
