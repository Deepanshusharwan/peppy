from PyQt6.QtCore import  QThread, pyqtSignal
import subprocess
import shlex
import sys


class WorkerThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, command_text: str):
        super().__init__()
        self.command_text = command_text
        self._process = None
        self._is_killed = False


    def run(self):
        try:
            command = self.command_text
            self._process = subprocess.Popen(command,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell = True,
                                             text=True,
                                             bufsize=1,
                                             universal_newlines=True
                                             )

            while True:
                if self._is_killed:
                    self._process.terminate()
                    break

                stdout_line = self._process.stdout.readline()
                stderr_line = self._process.stderr.readline()

                if stdout_line:
                    self.output_signal.emit(stdout_line.rstrip())
                if stderr_line:
                    self.error_signal.emit(stderr_line.rstrip())

                if not stdout_line and not stderr_line and self._process.poll() is not None:
                    break

                    
            # Drain any remaining output (optional but safe)
            if self._process.stdout:
                for line in self._process.stdout:
                    self.output_signal.emit(line.rstrip())

            if self._process.stderr:
                for line in self._process.stderr:
                    self.error_signal.emit(line.rstrip())


        except Exception as e:
            self.error_signal.emit(f"[ERROR] {str(e)}")
        finally:
            self.finished_signal.emit()
            # Explicit close to avoid further I/O attempts
            if self._process:
                if self._process.stdout:
                    self._process.stdout.close()
                if self._process.stderr:
                    self._process.stderr.close()

    def stop(self):
        self._is_killed = True
        if self._process and self._process.poll() is None:
            self._process.terminate()

