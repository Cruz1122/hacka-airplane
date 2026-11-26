package expo.modules.groupradio

import android.nfc.cardemulation.HostApduService
import android.os.Bundle
import android.util.Log

/**
 * The guide's side of tap pairing: answers a visitor's SELECT of [AID] with the pairing record JS
 * set through `setNfcCard`. The record format lives in `src/core/group/wire.ts`; this only moves
 * bytes. The system binds this service on its own, so the record is a process-wide static.
 */
class GroupNfcCardService : HostApduService() {
  companion object {
    /** Proprietary AID: 0xF0 then "NEVGR". Must match res/xml/group_radio_apdu_service.xml. */
    val AID = "F04E45564752".hexToBytes()
    private val SW_OK = byteArrayOf(0x90.toByte(), 0x00)
    private val SW_NOT_FOUND = byteArrayOf(0x6A, 0x82.toByte())
    private val SW_INS_NOT_SUPPORTED = byteArrayOf(0x6D, 0x00)

    /** Null while no guide session is syncing: a tap then answers "not found". */
    @Volatile var record: ByteArray? = null

    /** SELECT by DF name (00 A4 04 00 Lc AID [Le]). */
    fun selectApdu(): ByteArray =
      byteArrayOf(0x00, 0xA4.toByte(), 0x04, 0x00, AID.size.toByte()) + AID + byteArrayOf(0x00)

    private fun isSelectOfAid(apdu: ByteArray): Boolean {
      if (apdu.size < 5 + AID.size) return false
      if (apdu[0] != 0x00.toByte() || apdu[1] != 0xA4.toByte() || apdu[2] != 0x04.toByte()) return false
      if (apdu[4].toInt() != AID.size) return false
      return apdu.copyOfRange(5, 5 + AID.size).contentEquals(AID)
    }
  }

  override fun processCommandApdu(commandApdu: ByteArray, extras: Bundle?): ByteArray {
    if (!isSelectOfAid(commandApdu)) {
      Log.w(GroupRadioService.TAG, "NFC card: unexpected APDU ${commandApdu.toHex()}")
      return SW_INS_NOT_SUPPORTED
    }
    val current = record
    if (current == null) {
      Log.i(GroupRadioService.TAG, "NFC card: SELECT answered 6A82 (no guide session)")
      return SW_NOT_FOUND
    }
    Log.i(GroupRadioService.TAG, "NFC card: SELECT answered 9000 with ${current.size} bytes")
    return current + SW_OK
  }

  override fun onDeactivated(reason: Int) {
    Log.i(GroupRadioService.TAG, "NFC card: deactivated reason=$reason")
  }
}
