package expo.modules.deviceperformance

import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Debug
import android.os.PowerManager
import android.os.Process
import android.os.SystemClock
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition
import java.io.File
import java.io.IOException

class DevicePerformanceModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("DevicePerformance")

    AsyncFunction("sample") {
      val context = appContext.reactContext
      val manager = context?.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
      val device = manager?.let { ActivityManager.MemoryInfo().apply { it.getMemoryInfo(this) } }
      val memory = Debug.MemoryInfo().apply { Debug.getMemoryInfo(this) }
      val processes = manager?.runningAppProcesses?.count {
        it.uid == Process.myUid() && context?.packageName in it.pkgList.orEmpty()
      }
      val power = context?.getSystemService(Context.POWER_SERVICE) as? PowerManager
      val battery = context?.getSystemService(Context.BATTERY_SERVICE) as? BatteryManager
      val batteryInfo = context?.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        ?.takeIf { it.getBooleanExtra(BatteryManager.EXTRA_PRESENT, true) }
      val level = batteryInfo?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
      val scale = batteryInfo?.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
      val plugged = batteryInfo?.getIntExtra(BatteryManager.EXTRA_PLUGGED, -1)?.takeIf { it >= 0 }
      val current = battery?.getIntProperty(BatteryManager.BATTERY_PROPERTY_CURRENT_NOW)
        ?.takeUnless { it == Int.MIN_VALUE }
      val charge = battery?.getIntProperty(BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER)
        ?.takeIf { it > 0 }
      val voltage = batteryInfo?.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0)?.takeIf { it > 0 }
      val temperature = batteryInfo?.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, Int.MIN_VALUE)
        ?.takeUnless { it == Int.MIN_VALUE }

      mapOf(
        "memoryBytes" to if (memory.totalPss > 0) memory.totalPss * 1024.0 else null,
        "availableBytes" to device?.availMem?.toDouble(),
        "totalBytes" to device?.totalMem?.toDouble(),
        "cpuMs" to Process.getElapsedCpuTime().toDouble(),
        "elapsedMs" to SystemClock.elapsedRealtime().toDouble(),
        "cores" to Runtime.getRuntime().availableProcessors(),
        "pid" to Process.myPid(),
        "threads" to threadCount(),
        "processes" to processes?.takeIf { it > 0 },
        "batteryPercent" to if (level != null && scale != null && level in 0..scale && scale > 0)
          100.0 * level / scale else null,
        "batteryPlugged" to plugged?.let { it != 0 },
        "batteryCurrentMa" to current?.let { if (batteryInfo == null) null else it / 1000.0 },
        "batteryChargeMah" to charge?.let { if (batteryInfo == null) null else it / 1000.0 },
        "batteryVoltageMv" to voltage,
        "batteryTemperatureC" to temperature?.let { it / 10.0 },
        "powerSave" to power?.isPowerSaveMode
      )
    }
  }

  private fun threadCount(): Int? = try {
    File("/proc/self/status").useLines { lines ->
      lines.firstOrNull { it.startsWith("Threads:") }?.substringAfter(':')?.trim()?.toIntOrNull()
    }
  } catch (_: IOException) {
    null
  } catch (_: SecurityException) {
    null
  }
}
