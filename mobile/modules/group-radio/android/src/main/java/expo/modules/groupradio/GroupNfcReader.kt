package expo.modules.groupradio

import android.app.Activity
import android.content.Context
import android.nfc.NfcAdapter
import android.nfc.Tag
import android.nfc.tech.IsoDep
import android.util.Log
import java.io.IOException
import java.lang.ref.WeakReference

/**
 * The visitor's side of tap pairing: NFC reader mode on the app's activity, which reads the guide
 * phone's [GroupNfcCardService] card and hands the record to [onCard]. Reader mode only polls while
 * its activity is in the foreground, so [resume] re-applies it each time the activity comes back
 * (also covering an activity recreated while a reader session was wanted). [start] is idempotent,
 * so JS calls it again when NFC is switched on mid-session.
 */
class GroupNfcReader(private val onCard: (payload: ByteArray, atMs: Long) -> Unit) :
  NfcAdapter.ReaderCallback {
  companion object {
    /** HCE cards are ISO-DEP over NFC-A (most phones) or NFC-B; skip NDEF probing, it is not one. */
    private const val FLAGS =
      NfcAdapter.FLAG_READER_NFC_A or NfcAdapter.FLAG_READER_NFC_B or NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK
    private const val TRANSCEIVE_TIMEOUT_MS = 2_000

    fun state(context: Context): String {
      val adapter = NfcAdapter.getDefaultAdapter(context) ?: return "none"
      return if (adapter.isEnabled) "on" else "off"
    }
  }

  @Volatile private var wanted = false
  @Volatile private var enabledOn: WeakReference<Activity>? = null

  fun start(activity: Activity?) {
    wanted = true
    enable(activity)
  }

  fun stop() {
    wanted = false
    val activity = enabledOn?.get() ?: return
    activity.runOnUiThread {
      if (wanted) return@runOnUiThread
      try {
        NfcAdapter.getDefaultAdapter(activity)?.disableReaderMode(activity)
        Log.i(GroupRadioService.TAG, "NFC reader off")
      } catch (e: Exception) {
        Log.w(GroupRadioService.TAG, "NFC reader off failed: ${e.javaClass.simpleName}: ${e.message}")
      }
      enabledOn = null
    }
  }

  fun resume(activity: Activity?) {
    if (wanted) enable(activity)
  }

  private fun enable(activity: Activity?) {
    if (activity == null) {
      Log.w(GroupRadioService.TAG, "NFC reader: no activity yet, enabling on next resume")
      return
    }
    val adapter = NfcAdapter.getDefaultAdapter(activity)
    if (adapter == null) {
      Log.i(GroupRadioService.TAG, "NFC reader: this phone has no NFC")
      return
    }
    activity.runOnUiThread {
      if (!wanted) return@runOnUiThread
      try {
        adapter.enableReaderMode(activity, this, FLAGS, null)
        enabledOn = WeakReference(activity)
        Log.i(GroupRadioService.TAG, "NFC reader on (nfc enabled=${adapter.isEnabled})")
      } catch (e: Exception) {
        Log.w(GroupRadioService.TAG, "NFC reader on failed: ${e.javaClass.simpleName}: ${e.message}")
      }
    }
  }

  /** Runs on an NFC binder thread, once per tag presence. */
  override fun onTagDiscovered(tag: Tag) {
    val isoDep = IsoDep.get(tag)
    if (isoDep == null) {
      Log.i(GroupRadioService.TAG, "NFC read: tag is not ISO-DEP, ignored")
      return
    }
    try {
      isoDep.connect()
      isoDep.timeout = TRANSCEIVE_TIMEOUT_MS
      val response = isoDep.transceive(GroupNfcCardService.selectApdu())
      if (response.size < 2) {
        Log.w(GroupRadioService.TAG, "NFC read: short response ${response.toHex()}")
        return
      }
      val status = response.copyOfRange(response.size - 2, response.size)
      if (status[0] != 0x90.toByte() || status[1] != 0x00.toByte()) {
        Log.i(GroupRadioService.TAG, "NFC read: card answered ${status.toHex()}")
        return
      }
      val payload = response.copyOfRange(0, response.size - 2)
      Log.i(GroupRadioService.TAG, "NFC read: card ${payload.toHex()}")
      onCard(payload, System.currentTimeMillis())
    } catch (e: IOException) {
      // The phones moved apart mid-exchange; reader mode stays on for the next tap.
      Log.w(GroupRadioService.TAG, "NFC read failed: ${e.javaClass.simpleName}: ${e.message}")
    } catch (e: Exception) {
      Log.w(GroupRadioService.TAG, "NFC read error: ${e.javaClass.simpleName}: ${e.message}")
    } finally {
      try {
        isoDep.close()
      } catch (_: IOException) {}
    }
  }
}
