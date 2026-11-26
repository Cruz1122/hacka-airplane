import { cpuPercentage } from '../performanceReading';

test('reports a process share of CPU capacity using the elapsed sample interval', () => {
  const first = { cpuMs: 100, elapsedMs: 1_000, cores: 4 };
  const next = { cpuMs: 1_100, elapsedMs: 6_000, cores: 4 };
  expect(cpuPercentage(first)).toBeUndefined();
  expect(cpuPercentage(next, first)).toBe(5);
  expect(cpuPercentage(next, next)).toBeUndefined();
  expect(cpuPercentage(first, next)).toBeUndefined();
  expect(cpuPercentage({ ...next, cpuMs: first.cpuMs }, first)).toBe(0);
});
