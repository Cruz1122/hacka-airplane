package expo.modules.groupradio

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothServerSocket
import android.bluetooth.BluetoothSocket
import android.bluetooth.le.AdvertiseCallback
import android.bluetooth.le.AdvertiseData
import android.bluetooth.le.AdvertiseSettings
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.Build
import android.util.Log
import java.io.DataInputStream
import java.io.DataOutputStream
import java.io.IOException
import java.util.concurrent.ConcurrentHashMap
import kotlin.random.Random

/**
 * Sends a knowledge update to nearby phones with no QR code. The sharer opens an insecure LE
 * L2CAP channel (no pairing) and advertises its PSM; a receiver scans for offers, connects to the
 * advertiser and reads one length-prefixed payload. Both screens stay on during a transfer, so no
 * foreground service holds it. L2CAP channels need Android 10 (API 29).
 */
@SuppressLint("MissingPermission")
class KnowledgeLink(
  private val context: Context,
  private val onOffer: (address: String, count: Int, session: String, rssi: Int) -> Unit,
  private val onSent: (receivers: Int) -> Unit,
) {
  companion object {
    private const val COMPANY_ID = 0xFFFF
    // Group beacons use "NV" under the same test company id; their scan filter ignores these.
    private val MAGIC = byteArrayOf('N'.code.toByte(), 'K'.code.toByte())
    private const val MAX_BYTES = 1 shl 20

    fun supported() = Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q
  }

  private val adapter
    get() = (context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter

  @Volatile private var server: BluetoothServerSocket? = null
  private var advertising: AdvertiseCallback? = null
  private var scanning: ScanCallback? = null
  /** Scan results keep the address type; a bare address string can miss a random LE address. */
  private val devices = ConcurrentHashMap<String, Pair<BluetoothDevice, Int>>()

  fun share(payload: ByteArray, count: Int, done: (error: String?) -> Unit) {
    stopShare()
    if (!supported()) return done("Necesitas Android 10 o superior para compartir por Bluetooth.")
    val a = adapter
    if (a == null || !a.isEnabled) return done("Enciende el Bluetooth para compartir.")
    val advertiser = a.bluetoothLeAdvertiser
      ?: return done("Este teléfono no puede anunciar por Bluetooth.")
    val socket = try {
      a.listenUsingInsecureL2capChannel()
    } catch (e: IOException) {
      return done("No se pudo abrir el canal Bluetooth: ${e.message}")
    }
    server = socket
    val psm = socket.psm
    Thread({ acceptLoop(socket, payload) }, "KnowledgeLinkServer").start()

    val session = Random.nextBytes(4)
    val data = MAGIC + byteArrayOf(
      (psm shr 8).toByte(), psm.toByte(), (count shr 8).toByte(), count.toByte()
    ) + session
    val settings = AdvertiseSettings.Builder()
      .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
      .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_MEDIUM)
      .setConnectable(true)
      .setTimeout(0)
      .build()
    val callback = object : AdvertiseCallback() {
      override fun onStartSuccess(settingsInEffect: AdvertiseSettings) {
        Log.i(GroupRadioService.TAG, "SHARE advertising psm=$psm count=$count")
        done(null)
      }

      override fun onStartFailure(errorCode: Int) {
        Log.w(GroupRadioService.TAG, "SHARE advertise failed $errorCode")
        stopShare()
        done("No se pudo anunciar por Bluetooth (código $errorCode).")
      }
    }
    advertising = callback
    advertiser.startAdvertising(
      settings,
      AdvertiseData.Builder().setIncludeDeviceName(false).addManufacturerData(COMPANY_ID, data).build(),
      callback,
    )
  }

  private fun acceptLoop(socket: BluetoothServerSocket, payload: ByteArray) {
    var receivers = 0
    while (server === socket) {
      val client = try {
        socket.accept()
      } catch (e: IOException) {
        break // closed by stopShare
      }
      Thread({
        try {
          client.use {
            val out = DataOutputStream(it.outputStream)
            out.writeInt(payload.size)
            out.write(payload)
            out.flush()
            // Closing before the receiver's ack can drop bytes still in flight.
            it.inputStream.read()
          }
          synchronized(this) { receivers += 1; onSent(receivers) }
          Log.i(GroupRadioService.TAG, "SHARE sent ${payload.size} bytes")
        } catch (e: IOException) {
          Log.w(GroupRadioService.TAG, "SHARE send failed: ${e.message}")
        }
      }, "KnowledgeLinkSend").start()
    }
  }

  fun stopShare() {
    val socket = server
    server = null
    try {
      socket?.close()
    } catch (_: IOException) {
    }
    advertising?.let { adapter?.bluetoothLeAdvertiser?.stopAdvertising(it) }
    advertising = null
  }

  fun find(): String? {
    stopFind()
    val scanner = adapter?.takeIf { it.isEnabled }?.bluetoothLeScanner
      ?: return "Enciende el Bluetooth para recibir."
    val callback = object : ScanCallback() {
      override fun onScanResult(callbackType: Int, result: ScanResult) {
        val bytes = result.scanRecord?.getManufacturerSpecificData(COMPANY_ID) ?: return
        if (bytes.size < 10 || bytes[0] != MAGIC[0] || bytes[1] != MAGIC[1]) return
        val psm = ((bytes[2].toInt() and 0xFF) shl 8) or (bytes[3].toInt() and 0xFF)
        val count = ((bytes[4].toInt() and 0xFF) shl 8) or (bytes[5].toInt() and 0xFF)
        val address = result.device.address
        devices[address] = result.device to psm
        onOffer(address, count, bytes.copyOfRange(6, 10).toHex(), result.rssi)
      }

      override fun onScanFailed(errorCode: Int) {
        Log.w(GroupRadioService.TAG, "SHARE scan failed $errorCode")
      }
    }
    scanning = callback
    scanner.startScan(
      listOf(ScanFilter.Builder().setManufacturerData(COMPANY_ID, MAGIC, byteArrayOf(-1, -1)).build()),
      ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY).build(),
      callback,
    )
    return null
  }

  fun stopFind() {
    scanning?.let { adapter?.bluetoothLeScanner?.stopScan(it) }
    scanning = null
  }

  /** Blocking: call off the main thread. */
  fun receive(address: String): String {
    if (!supported()) throw IOException("Necesitas Android 10 o superior para recibir por Bluetooth.")
    val (device, psm) = devices[address] ?: throw IOException("El teléfono que comparte ya no está cerca.")
    stopFind()
    val socket: BluetoothSocket = device.createInsecureL2capChannel(psm)
    socket.use {
      it.connect()
      val input = DataInputStream(it.inputStream)
      val size = input.readInt()
      if (size <= 0 || size > MAX_BYTES) throw IOException("Tamaño de actualización inválido: $size")
      val bytes = ByteArray(size)
      input.readFully(bytes)
      it.outputStream.write(1)
      it.outputStream.flush()
      Log.i(GroupRadioService.TAG, "SHARE received $size bytes")
      return String(bytes, Charsets.UTF_8)
    }
  }

  fun stop() {
    stopShare()
    stopFind()
  }
}
