package expo.modules.groupradio

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.le.AdvertiseCallback
import android.bluetooth.le.AdvertiseData
import android.bluetooth.le.AdvertiseSettings
import android.bluetooth.le.AdvertisingSet
import android.bluetooth.le.AdvertisingSetCallback
import android.bluetooth.le.AdvertisingSetParameters
import android.bluetooth.le.BluetoothLeAdvertiser
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import java.util.concurrent.CopyOnWriteArraySet
import java.util.concurrent.atomic.AtomicInteger

/** `phy`: "1m" or "coded", the primary PHY the beacon arrived on. */
typealias SightingListener = (payload: ByteArray, rssi: Int, phy: String, atMs: Long) -> Unit
typealias TickListener = (atMs: Long) -> Unit

fun ByteArray.toHex(): String = joinToString("") { "%02x".format(it) }

fun String.hexToBytes(): ByteArray {
  require(length % 2 == 0) { "odd hex length: $length" }
  return chunked(2).map { it.toInt(16).toByte() }.toByteArray()
}

/**
 * Holds the BLE beacon and the scan while the group is active, so both survive the screen turning
 * off. The beacon is manufacturer data under the Bluetooth SIG test company id, opened by a magic
 * prefix the scan filters on (a filter is what lets results through with the screen off).
 *
 * Two beacons carry the same bytes: a legacy 1M advertisement every BLE phone hears, and, on
 * chipsets with LE Coded PHY and extended advertising, a second set on the coded PHY for range.
 * Such phones scan both PHYs with one filter. The coded set is best effort: any failure drops it
 * and leaves the 1M beacon running.
 *
 * Also drives a 1 s native tick: React Native pauses JS timers (`JavaTimerManager.onHostPause`)
 * when the screen locks on some Android devices, while this service's Handler keeps firing.
 */
@SuppressLint("MissingPermission") // The JS side requests the runtime permissions before start().
class GroupRadioService : Service() {
  companion object {
    const val TAG = "GroupRadio"
    const val ACTION_START = "expo.modules.groupradio.START"
    const val EXTRA_PAYLOAD = "payload"
    const val EXTRA_ADVERTISE = "advertise"
    const val EXTRA_SCAN = "scan"

    /** 0xFFFF: reserved by the Bluetooth SIG for tests, never assigned to a company. */
    const val COMPANY_ID = 0xFFFF
    val MAGIC = byteArrayOf(0x4E, 0x56) // "NV"
    private const val CHANNEL_ID = "group-radio"
    private const val NOTIFICATION_ID = 4711
    private const val STAT_EVERY_MS = 5_000L
    private const val TICK_EVERY_MS = 1_000L
    /** Android degrades continuous BLE scans after ~30 min; refresh at 20 min. */
    private const val SCAN_REFRESH_MS = 20 * 60_000L
    private const val PULSE_MS = 400L
    private const val GAP_MS = 200L

    @Volatile var running = false
    @Volatile var lastError: String? = null
    @Volatile private var activeInstance: GroupRadioService? = null
    val listeners = CopyOnWriteArraySet<SightingListener>()
    val tickListeners = CopyOnWriteArraySet<TickListener>()

    private val alertHandler = Handler(Looper.getMainLooper())

    /** LE Coded PHY + extended advertising, both needed for the long-range beacon. */
    fun codedPhySupported(adapter: BluetoothAdapter?): Boolean =
      Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
        adapter != null &&
        adapter.isEnabled &&
        adapter.isLeCodedPhySupported &&
        adapter.isLeExtendedAdvertisingSupported

    /** Updates the advertised payload in-process (safe with screen off / Doze on Android 12+). */
    fun updatePayload(payloadHex: String) {
      val service = activeInstance ?: return
      service.handler.post { service.applyPayloadUpdate(payloadHex) }
    }

    /** Audible + tactile alert safe to call even when the screen is off / Activity paused. */
    fun triggerAlert(context: Context, rawCount: Int) {
      val count = rawCount.coerceIn(1, 4)
      try {
        val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
          (context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager)?.defaultVibrator
        } else {
          @Suppress("DEPRECATION")
          context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
        }
        if (vibrator?.hasVibrator() == true) {
          val pattern = LongArray(count * 2) { i ->
            when {
              i == 0 -> 0L
              i % 2 == 1 -> PULSE_MS
              else -> GAP_MS
            }
          }
          if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(VibrationEffect.createWaveform(pattern, -1))
          } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(pattern, -1)
          }
        }
      } catch (e: Exception) {
        Log.w(TAG, "alert vibrate: ${e.message}")
      }

      try {
        val tone = ToneGenerator(AudioManager.STREAM_ALARM, 90)
        val durationMs = (count * 350).coerceAtMost(1400)
        tone.startTone(ToneGenerator.TONE_PROP_BEEP2, durationMs)
        alertHandler.postDelayed({
          try {
            tone.release()
          } catch (_: Exception) {}
        }, durationMs + 150L)
      } catch (e: Exception) {
        Log.w(TAG, "alert tone: ${e.message}")
      }
    }
  }

  private val handler = Handler(Looper.getMainLooper())
  private val sightings = AtomicInteger(0)
  private val codedSightings = AtomicInteger(0)
  /** Legacy `startAdvertising` beacon is live (fallback when the advertising-set API fails). */
  private var legacyAdvertising = false
  /** Once the set API fails on this phone, stay on the legacy advertiser for the service's life. */
  private var setUnsupported = false
  /** Once the coded set fails on this phone, broadcast 1M only for the service's life. */
  private var codedUnsupported = false
  private var scanning = false
  /** The running scan asks for every PHY (extended results); false is the legacy 1M-only scan. */
  private var scanAllPhys = false
  /** The all-PHY scan failed once here: rescans (including the 20 min refresh) stay on 1M. */
  private var allPhyScanFailed = false
  private var currentPayloadHex: String? = null

  private val adapter get() = (getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter

  private val advertiseCallback = object : AdvertiseCallback() {
    override fun onStartSuccess(settingsInEffect: AdvertiseSettings) {
      Log.i(TAG, "ADV started (legacy) mode=${settingsInEffect.mode} tx=${settingsInEffect.txPowerLevel}")
    }

    override fun onStartFailure(errorCode: Int) {
      fail("advertise failed: code $errorCode")
    }
  }

  /**
   * One advertising set and its own callback: `stopAdvertisingSet` finds a set by its callback, so
   * the 1M and coded sets cannot share one. Callbacks arrive on [handler] (main looper), like every
   * other state change in this service.
   */
  private inner class BeaconSet(val label: String, val onFailure: (String) -> Unit) {
    /** Requested and not stopped; [set] is null until it starts. */
    var requested = false
      private set
    private var set: AdvertisingSet? = null
    /** Payload the set carries (or is starting with); differs from [currentPayloadHex] mid-update. */
    private var payloadHex: String? = null

    private val callback = object : AdvertisingSetCallback() {
      override fun onAdvertisingSetStarted(started: AdvertisingSet?, txPower: Int, status: Int) {
        if (!requested) return
        if (status != AdvertisingSetCallback.ADVERTISE_SUCCESS || started == null) {
          onFailure("ADV $label set start failed status=$status")
          return
        }
        set = started
        Log.i(TAG, "ADV $label set started tx=$txPower")
        // A payload update that landed while the set was starting.
        currentPayloadHex?.let { update(it) }
      }

      override fun onAdvertisingDataSet(changed: AdvertisingSet?, status: Int) {
        if (status == AdvertisingSetCallback.ADVERTISE_SUCCESS) Log.i(TAG, "ADV $label set data updated")
        else onFailure("ADV $label set data update failed status=$status")
      }

      override fun onAdvertisingSetStopped(stopped: AdvertisingSet?) {
        Log.i(TAG, "ADV $label set stopped")
      }
    }

    fun start(advertiser: BluetoothLeAdvertiser, parameters: AdvertisingSetParameters, payload: String) {
      requested = true
      payloadHex = payload
      advertiser.startAdvertisingSet(parameters, advertiseData(payload), null, null, null, callback, handler)
    }

    /** Swaps the data in place; before the set has started, [callback] applies the latest payload. */
    fun update(payload: String) {
      val live = set ?: return
      if (payload == payloadHex) return
      payloadHex = payload
      live.setAdvertisingData(advertiseData(payload))
    }

    fun stop() {
      try {
        if (requested) adapter?.bluetoothLeAdvertiser?.stopAdvertisingSet(callback)
      } catch (e: Exception) {
        Log.w(TAG, "stop $label set: ${e.message}")
      }
      requested = false
      set = null
      payloadHex = null
    }
  }

  private val legacySet = BeaconSet("1m") { reason -> fallBackToLegacy(reason) }
  private val codedSet = BeaconSet("coded") { reason -> dropCoded(reason) }

  private val scanCallback = object : ScanCallback() {
    override fun onScanResult(callbackType: Int, result: ScanResult) {
      val data = result.scanRecord?.getManufacturerSpecificData(COMPANY_ID) ?: return
      if (data.size < MAGIC.size || data[0] != MAGIC[0] || data[1] != MAGIC[1]) return
      val payload = data.copyOfRange(MAGIC.size, data.size)
      val coded = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
        result.primaryPhy == BluetoothDevice.PHY_LE_CODED
      sightings.incrementAndGet()
      if (coded) codedSightings.incrementAndGet()
      val now = System.currentTimeMillis()
      val phy = if (coded) "coded" else "1m"
      for (l in listeners) l(payload, result.rssi, phy, now)
    }

    override fun onScanFailed(errorCode: Int) {
      if (scanAllPhys && !allPhyScanFailed) {
        // A chipset that reports coded support but rejects the scan must not leave the phone deaf.
        allPhyScanFailed = true
        Log.w(TAG, "all-PHY scan failed: code $errorCode, retrying on 1M only")
        handler.post {
          try {
            adapter?.bluetoothLeScanner?.stopScan(this)
          } catch (e: Exception) {
            Log.w(TAG, "stopScan after failure: ${e.message}")
          }
          scanning = false
          if (running) startScan()
        }
        return
      }
      fail("scan failed: code $errorCode")
    }
  }

  private val stat = object : Runnable {
    override fun run() {
      Log.i(
        TAG,
        "STAT sightings=${sightings.getAndSet(0)} coded=${codedSightings.getAndSet(0)} " +
          "per ${STAT_EVERY_MS}ms listeners=${listeners.size}"
      )
      handler.postDelayed(this, STAT_EVERY_MS)
    }
  }

  private val tick = object : Runnable {
    override fun run() {
      val now = System.currentTimeMillis()
      for (l in tickListeners) l(now)
      handler.postDelayed(this, TICK_EVERY_MS)
    }
  }

  private val scanRefresh = object : Runnable {
    override fun run() {
      if (scanning) {
        try {
          adapter?.bluetoothLeScanner?.stopScan(scanCallback)
        } catch (e: Exception) {
          Log.w(TAG, "scan refresh stop: ${e.message}")
        }
        scanning = false
        startScan()
      }
      handler.postDelayed(this, SCAN_REFRESH_MS)
    }
  }

  override fun onBind(intent: Intent?): IBinder? = null

  override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
    lastError = null
    val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) ServiceInfo.FOREGROUND_SERVICE_TYPE_CONNECTED_DEVICE else 0
    ServiceCompat.startForeground(this, NOTIFICATION_ID, notification(), type)
    stopRadio()
    val payload = intent?.getStringExtra(EXTRA_PAYLOAD)
    if (payload == null) {
      // Restarted by the system without its intent: nothing to broadcast.
      stopSelf()
      return START_NOT_STICKY
    }
    try {
      val shouldAdvertise = intent.getBooleanExtra(EXTRA_ADVERTISE, true)
      val shouldScan = intent.getBooleanExtra(EXTRA_SCAN, true)
      if (shouldAdvertise) startAdvertising(payload)
      if (shouldScan) startScan()
      running = true
      activeInstance = this
      handler.postDelayed(stat, STAT_EVERY_MS)
      handler.postDelayed(tick, TICK_EVERY_MS)
      if (shouldScan) handler.postDelayed(scanRefresh, SCAN_REFRESH_MS)
    } catch (e: Exception) {
      fail("start failed: ${e.javaClass.simpleName}: ${e.message}")
    }
    return START_NOT_STICKY
  }

  /**
   * An advertising set swaps its data in place. The legacy advertiser can only stop and restart,
   * which on the Galaxy A24 left gaps in the beacon every time a visitor's echo changed (~2 s).
   */
  private fun applyPayloadUpdate(payloadHex: String) {
    if (!running || payloadHex == currentPayloadHex) return
    currentPayloadHex = payloadHex
    try {
      when {
        legacySet.requested -> legacySet.update(payloadHex)
        legacyAdvertising -> {
          stopLegacyAdvertiser()
          startLegacyAdvertising(payloadHex)
        }
      }
    } catch (e: Exception) {
      fail("updatePayload failed: ${e.javaClass.simpleName}: ${e.message}")
    }
    try {
      if (codedSet.requested) codedSet.update(payloadHex)
    } catch (e: Exception) {
      dropCoded("ADV coded set update threw ${e.javaClass.simpleName}: ${e.message}")
    }
  }

  override fun onDestroy() {
    if (activeInstance === this) activeInstance = null
    stopRadio()
    running = false
    Log.i(TAG, "service destroyed")
    super.onDestroy()
  }

  private fun advertiseData(payloadHex: String): AdvertiseData =
    AdvertiseData.Builder()
      .setIncludeDeviceName(false)
      .setIncludeTxPowerLevel(false)
      .addManufacturerData(COMPANY_ID, MAGIC + payloadHex.hexToBytes())
      .build()

  private fun startAdvertising(payloadHex: String) {
    currentPayloadHex = payloadHex
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O || setUnsupported || !startLegacySet(payloadHex)) {
      startLegacyAdvertising(payloadHex)
    }
    startCodedSet(payloadHex)
  }

  /** Same beacon as the legacy path: legacy (4.x) PDU so older scanners hear it, 100 ms, high power. */
  private fun startLegacySet(payloadHex: String): Boolean {
    val advertiser = adapter?.bluetoothLeAdvertiser ?: return false
    return try {
      val parameters = AdvertisingSetParameters.Builder()
        .setLegacyMode(true)
        .setConnectable(false)
        // What the legacy startAdvertising requests too.
        .setScannable(true)
        .setInterval(AdvertisingSetParameters.INTERVAL_MIN)
        .setTxPowerLevel(AdvertisingSetParameters.TX_POWER_HIGH)
        .build()
      legacySet.start(advertiser, parameters, payloadHex)
      true
    } catch (e: Exception) {
      legacySet.stop()
      setUnsupported = true
      Log.w(TAG, "ADV set unavailable, using legacy advertiser: ${e.javaClass.simpleName}: ${e.message}")
      false
    }
  }

  /** Extended (non-legacy) advertising on the coded PHY, primary and secondary, for range. */
  private fun startCodedSet(payloadHex: String) {
    val bt = adapter
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O || codedUnsupported || !codedPhySupported(bt)) {
      Log.i(TAG, "ADV coded off (supported=${codedPhySupported(bt)} failedBefore=$codedUnsupported)")
      return
    }
    val advertiser = bt?.bluetoothLeAdvertiser ?: return
    try {
      val parameters = AdvertisingSetParameters.Builder()
        .setLegacyMode(false)
        // Non-legacy sets may be connectable or scannable, never both; the beacon needs neither.
        .setConnectable(false)
        .setScannable(false)
        .setPrimaryPhy(BluetoothDevice.PHY_LE_CODED)
        .setSecondaryPhy(BluetoothDevice.PHY_LE_CODED)
        .setInterval(AdvertisingSetParameters.INTERVAL_MIN)
        .setTxPowerLevel(AdvertisingSetParameters.TX_POWER_HIGH)
        .build()
      Log.i(TAG, "ADV coded requesting maxData=${bt.leMaximumAdvertisingDataLength}")
      codedSet.start(advertiser, parameters, payloadHex)
    } catch (e: Exception) {
      dropCoded("ADV coded set unavailable: ${e.javaClass.simpleName}: ${e.message}")
    }
  }

  private fun dropCoded(reason: String) {
    Log.w(TAG, "$reason, keeping the 1M beacon only")
    codedSet.stop()
    codedUnsupported = true
  }

  private fun fallBackToLegacy(reason: String) {
    Log.w(TAG, "$reason, falling back to legacy advertiser")
    legacySet.stop()
    setUnsupported = true
    currentPayloadHex?.let {
      try {
        startLegacyAdvertising(it)
      } catch (e: Exception) {
        fail("legacy advertise failed: ${e.javaClass.simpleName}: ${e.message}")
      }
    }
  }

  private fun startLegacyAdvertising(payloadHex: String) {
    val advertiser = adapter?.bluetoothLeAdvertiser
      ?: return fail("no advertiser: Bluetooth off or advertising unsupported")
    val settings = AdvertiseSettings.Builder()
      .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
      .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
      .setConnectable(false)
      .build()
    advertiser.startAdvertising(settings, advertiseData(payloadHex), advertiseCallback)
    legacyAdvertising = true
  }

  private fun stopLegacyAdvertiser() {
    try {
      if (legacyAdvertising) adapter?.bluetoothLeAdvertiser?.stopAdvertising(advertiseCallback)
    } catch (e: Exception) {
      Log.w(TAG, "stopAdv: ${e.message}")
    }
    legacyAdvertising = false
  }

  private fun stopAdvertisingOnly() {
    legacySet.stop()
    codedSet.stop()
    stopLegacyAdvertiser()
  }

  private fun startScan() {
    val scanner = adapter?.bluetoothLeScanner ?: return fail("no scanner: Bluetooth off")
    val filter = ScanFilter.Builder()
      .setManufacturerData(COMPANY_ID, MAGIC, byteArrayOf(0xFF.toByte(), 0xFF.toByte()))
      .build()
    val allPhys = !allPhyScanFailed && codedPhySupported(adapter)
    val builder = ScanSettings.Builder()
      .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
      .setCallbackType(ScanSettings.CALLBACK_TYPE_ALL_MATCHES)
      .setReportDelay(0)
    // Extended results on every PHY: the same filter then matches the 1M and the coded beacon.
    if (allPhys && Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
      builder.setLegacy(false).setPhy(ScanSettings.PHY_LE_ALL_SUPPORTED)
    }
    scanAllPhys = allPhys
    scanner.startScan(listOf(filter), builder.build(), scanCallback)
    scanning = true
    Log.i(TAG, "SCAN started phy=${if (allPhys) "all" else "1m"}")
  }

  private fun stopRadio() {
    handler.removeCallbacks(stat)
    handler.removeCallbacks(tick)
    handler.removeCallbacks(scanRefresh)
    stopAdvertisingOnly()
    try {
      if (scanning) adapter?.bluetoothLeScanner?.stopScan(scanCallback)
    } catch (e: Exception) {
      Log.w(TAG, "stopScan: ${e.message}")
    }
    scanning = false
    currentPayloadHex = null
  }

  private fun fail(message: String) {
    lastError = message
    Log.e(TAG, message)
  }

  private fun notification(): Notification {
    val manager = getSystemService(NotificationManager::class.java)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
      manager.createNotificationChannel(
        NotificationChannel(CHANNEL_ID, "Grupo", NotificationManager.IMPORTANCE_LOW)
      )
    }
    return NotificationCompat.Builder(this, CHANNEL_ID)
      .setSmallIcon(android.R.drawable.stat_sys_data_bluetooth)
      .setContentTitle("Nevados")
      .setContentText("Grupo activo")
      .setOngoing(true)
      .build()
  }
}
