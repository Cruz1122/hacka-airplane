package expo.modules.deviceperformance

import android.app.ActivityManager
import android.content.Context
import android.os.Debug
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

      mapOf(
        "memoryBytes" to if (memory.totalPss > 0) memory.totalPss * 1024.0 else null,
        "availableBytes" to device?.availMem?.toDouble(),
        "totalBytes" to device?.totalMem?.toDouble(),
        "cpuMs" to Process.getElapsedCpuTime().toDouble(),
        "elapsedMs" to SystemClock.elapsedRealtime().toDouble(),
        "cores" to Runtime.getRuntime().availableProcessors(),
        "pid" to Process.myPid(),
        "threads" to threadCount(),
        "processes" to processes?.takeIf { it > 0 }
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
