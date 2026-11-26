package expo.modules.groupradio

import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.core.os.bundleOf
import expo.modules.kotlin.Promise
import expo.modules.kotlin.exception.Exceptions
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition
import java.lang.ref.WeakReference

class GroupRadioModule : Module() {
  private var sightingListener: SightingListener? = null
  private var tickListener: TickListener? = null
  private val nfcReader = GroupNfcReader { payload, atMs ->
    sendEvent("onNfcCard", bundleOf("payload" to payload.toHex(), "atMs" to atMs.toDouble()))
  }

  private val context: Context
    get() = appContext.reactContext ?: throw Exceptions.ReactContextLost()

  private var linkInstance: KnowledgeLink? = null
  private val link: KnowledgeLink
    get() = linkInstance ?: KnowledgeLink(
      context,
      onOffer = { address, count, session, rssi ->
        sendEvent(
          "onShareOffer",
          bundleOf("address" to address, "count" to count, "session" to session, "rssi" to rssi)
        )
      },
      onSent = { receivers -> sendEvent("onShareSent", bundleOf("receivers" to receivers)) },
    ).also { linkInstance = it }

  override fun definition() = ModuleDefinition {
    Name("GroupRadio")

    Events("onSighting", "onTick", "onNfcCard", "onShareOffer", "onShareSent")

    Function("capabilities") {
      val adapter = (context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter
      val on = adapter?.isEnabled == true
      mapOf(
        "sdk" to Build.VERSION.SDK_INT,
        "bluetoothOn" to on,
        // The advertiser is null while Bluetooth is off, so this is only meaningful when on.
        "canAdvertise" to (on && adapter?.bluetoothLeAdvertiser != null),
        "running" to GroupRadioService.running,
        "lastError" to GroupRadioService.lastError,
        "nfc" to GroupNfcReader.state(context),
        "codedPhy" to GroupRadioService.codedPhySupported(adapter),
        "knowledgeLink" to KnowledgeLink.supported()
      )
    }

    Function("start") { payloadHex: String, advertise: Boolean, scan: Boolean ->
      val intent = Intent(context, GroupRadioService::class.java)
        .setAction(GroupRadioService.ACTION_START)
        .putExtra(GroupRadioService.EXTRA_PAYLOAD, payloadHex)
        .putExtra(GroupRadioService.EXTRA_ADVERTISE, advertise)
        .putExtra(GroupRadioService.EXTRA_SCAN, scan)
      ContextCompat.startForegroundService(context, intent)
    }

    Function("updatePayload") { payloadHex: String ->
      GroupRadioService.updatePayload(payloadHex)
    }

    Function("stop") {
      context.stopService(Intent(context, GroupRadioService::class.java))
    }

    Function("alert") { count: Int ->
      GroupRadioService.triggerAlert(context, count)
    }

    Function("setNfcCard") { payloadHex: String? ->
      GroupNfcCardService.record = payloadHex?.hexToBytes()
      Log.i(GroupRadioService.TAG, if (payloadHex == null) "NFC card cleared" else "NFC card set $payloadHex")
    }

    Function("startNfcReader") {
      nfcReader.start(appContext.currentActivity)
    }

    Function("stopNfcReader") {
      nfcReader.stop()
    }

    OnActivityEntersForeground {
      nfcReader.resume(appContext.currentActivity)
    }

    AsyncFunction("shareStart") { payload: String, count: Int, promise: Promise ->
      link.share(payload.toByteArray(Charsets.UTF_8), count) { error ->
        if (error == null) promise.resolve(null) else promise.reject("ERR_SHARE", error, null)
      }
    }

    Function("shareStop") {
      link.stopShare()
    }

    Function("findShares") {
      link.find()
    }

    Function("stopFindShares") {
      link.stopFind()
    }

    AsyncFunction("receiveShare") { address: String, promise: Promise ->
      // The L2CAP read blocks; keep it off the module queue other calls share.
      Thread({
        try {
          promise.resolve(link.receive(address))
        } catch (e: Exception) {
          Log.w(GroupRadioService.TAG, "SHARE receive failed: ${e.javaClass.simpleName}: ${e.message}")
          promise.reject("ERR_RECEIVE", e.message ?: "No se pudo recibir la actualización.", e)
        }
      }, "KnowledgeLinkReceive").start()
    }

    Function("log") { message: String ->
      Log.i(GroupRadioService.TAG, "JS $message")
    }

    OnStartObserving("onSighting") {
      val weak = WeakReference(this@GroupRadioModule)
      val l: SightingListener = { payload, rssi, phy, atMs ->
        weak.get()?.sendEvent(
          "onSighting",
          bundleOf("payload" to payload.toHex(), "rssi" to rssi, "phy" to phy, "atMs" to atMs.toDouble())
        )
      }
      sightingListener?.let { GroupRadioService.listeners.remove(it) }
      sightingListener = l
      GroupRadioService.listeners.add(l)
    }

    OnStopObserving("onSighting") {
      sightingListener?.let { GroupRadioService.listeners.remove(it) }
      sightingListener = null
    }

    OnStartObserving("onTick") {
      val weak = WeakReference(this@GroupRadioModule)
      val l: TickListener = { atMs ->
        weak.get()?.sendEvent("onTick", bundleOf("atMs" to atMs.toDouble()))
      }
      tickListener?.let { GroupRadioService.tickListeners.remove(it) }
      tickListener = l
      GroupRadioService.tickListeners.add(l)
    }

    OnStopObserving("onTick") {
      tickListener?.let { GroupRadioService.tickListeners.remove(it) }
      tickListener = null
    }

    OnDestroy {
      linkInstance?.stop()
      // A JS reload must not leave a stale card answering taps or the reader polling.
      GroupNfcCardService.record = null
      nfcReader.stop()
      sightingListener?.let { GroupRadioService.listeners.remove(it) }
      sightingListener = null
      tickListener?.let { GroupRadioService.tickListeners.remove(it) }
      tickListener = null
    }
  }
}
