from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
from configparser import ConfigParser
import os
import signal
import select

class WorkerThread(QThread):
    # Signals for communicating with the GUI thread
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)  # will emit exit code

    def __init__(self, command_text: str):
        super().__init__()
        self.command_text = command_text
        self.process = None
        self.is_terminated = False

    def run(self):
        try:
            # --- Load configuration file ---
            config_path = f"{os.environ.get('HOME', '~')}/.config/peppy/peppy.conf"
            config = ConfigParser(interpolation=None)
            config.read(config_path)

            # Retrieve additional PATH entries from config, if any
            custom_paths = config.get("MISC", "PATHS", fallback="")

            # --- Prepare command ---
            # Use bash explicitly to support `export`
            full_command = (
                f'bash -c "export PATH=\\"$PATH:{custom_paths}\\"; {self.command_text}"'
            )

            # --- Start subprocess in a new process group ---
            self.process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                bufsize=1,
                universal_newlines=True,
                preexec_fn=os.setsid,  # ensures we can terminate child processes safely
            )

            # --- Read process output in real time ---
            while True:
                if self.is_terminated:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                    break

                read_descriptors = [self.process.stdout.fileno(), self.process.stderr.fileno()]
                ready_descriptors, _, _ = select.select(read_descriptors, [], [])

                for descriptor in ready_descriptors:
                    if descriptor == self.process.stdout.fileno():
                        line = self.process.stdout.readline()
                        if line:
                            self.output_signal.emit(line.rstrip())
                    elif descriptor == self.process.stderr.fileno():
                        line = self.process.stderr.readline()
                        if line:
                            self.error_signal.emit(line.rstrip())

                if self.process.poll() is not None:
                    break

            exit_code = self.process.returncode or 0

        except Exception as exception:
            self.error_signal.emit(f"[ERROR] {str(exception)}")
            exit_code = 1

        finally:
            # Clean up I/O streams
            if self.process:
                if self.process.stdout:
                    self.process.stdout.close()
                if self.process.stderr:
                    self.process.stderr.close()

            self.finished_signal.emit(exit_code)

    def stop(self):
        """Request the thread to terminate and kill the process if running."""
        self.is_terminated = True
        if self.process and self.process.poll() is None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
