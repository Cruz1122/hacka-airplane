// Every threshold of the group-sync core. These are UNCALIBRATED defaults from typical BLE
// outdoor figures (about -59 dBm at 1 m, path-loss exponent near 2 in open terrain); they must be
// measured on the target phones (in a pocket, in a hand, on the trail) before anyone trusts them.
// No other file in src/core/group may hold a threshold literal.

export const GROUP_POLICY = {
  /** A zone is left only once the smoothed value is this far past the cut-off, so noise at a
   *  boundary does not flip it back and forth. */
  hysteresisDb: 3,
  /** Readings in the median that drops single-reading spikes. */
  medianWindow: 5,
  /** Weight of the newest median in the moving average (0..1). */
  emaAlpha: 0.3,
  /** Pocket guard: a worse zone is committed only after it persists this long. A phone slipped
   *  into a pocket drops ~15 dB for seconds; the median and EMA stretch a 5 s dip to about 7 s. */
  degradeDwellMs: 10_000,
  /** A member not heard for this long is unseen; also how long a sighting keeps a guide
   *  reachable, and the gap after which an edge's history is discarded. */
  unseenAfterMs: 12_000,
  /** Log-distance model for the lane: d = 10^((refDbmAt1m - rssi) / (10 * n)). */
  pathLossExponent: 2,
  refDbmAt1m: -59,
  /** Minimum RSSI to pair by bringing phones close (<~1 m); measured -39..-59 dBm on A24/Edge. */
  pairMinDbm: -65,
  /** A visitor with NFC facing a guide whose card is up waits this long, from the first time it
   *  hears that guide within pairing range, for the tap; then it pairs over BLE so a failed or
   *  impossible tap (case, misaligned antennas) never leaves it stranded. */
  nfcGraceMs: 8_000,
  /** The guide's alert distance (slider), in whole meters: beyond it a visitor is far. Zones derive
   *  from it through the log-distance model above: near up to `nearFraction` of it, mid up to it.
   *  Fits one beacon byte. */
  alertMeters: { min: 5, max: 150, step: 5, default: 30, nearFraction: 0.5 },
} as const;
