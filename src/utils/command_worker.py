from PyQt6.QtCore import  Qt, QThread, pyqtSignal
import subprocess
import shlex


class WorkerThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, command_text: str):
        super().__init__()
        self.command_text = command_text


    def run(self):
        try:
            command = shlex.split(self.command_text, posix=True)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()

            if stdout:
               self.output_signal.emit(stdout.decode()) 
            if stderr:
                self.error_signal.emit(stderr.decoe())

        except Exception as e:
            self.error_signal.emit(str(e))
            print(e)
