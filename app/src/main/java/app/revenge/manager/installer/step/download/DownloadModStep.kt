package app.revenge.manager.installer.step.download

import android.content.Context
import androidx.compose.runtime.Stable
import app.revenge.manager.R
import app.revenge.manager.installer.step.Step
import app.revenge.manager.installer.step.StepGroup
import app.revenge.manager.installer.step.StepRunner
import org.koin.core.component.inject
import java.io.File

@Stable
class DownloadModStep(workingDir: File) : Step() {
    private val context: Context by inject()
    override val nameRes = R.string.step_dl_mod
    override val group = StepGroup.PATCHING
    val workingCopy = workingDir.resolve("xposed.apk")

    override suspend fun run(runner: StepRunner) {
        runner.logger.i("Extracting embedded BotClient loader")
        workingCopy.parentFile?.mkdirs()
        context.assets.open("botclient-loader.apk").use { input ->
            workingCopy.outputStream().use { output -> input.copyTo(output) }
        }
        check(workingCopy.length() > 0) { "Embedded BotClient loader is empty" }
    }
}
