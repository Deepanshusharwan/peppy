from PyQt6.QtCore import  QThread, pyqtSignal
import subprocess
from configparser import ConfigParser
import os
import shlex
import sys
import select

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
            try:
                CONFIG_PATH = f"{os.environ.get('HOME','~')}/.config/peppy/peppy.conf"
                os.path.isfile(CONFIG_PATH)            
                config = ConfigParser(interpolation=None)
                config.read(CONFIG_PATH)
                paths = config["MISC"].get('PATHS')
            except KeyError:
                config["MISC"] = {
                    'PATHS': ''
                }
                paths = ''
                with open(CONFIG_PATH,'w') as configfile:
                    config.write(configfile)

            command = f'export PATH="$PATH:{paths}";{self.command_text}'
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
                
                reads = [self._process.stdout.fileno(), self._process.stderr.fileno()]
                ret = select.select(reads, [], [])

                for fd in ret[0]:
                    if fd == self._process.stdout.fileno():
                        line = self._process.stdout.readline()
                        if line:
                            self.output_signal.emit(line.rstrip())
                    if fd == self._process.stderr.fileno():
                        line = self._process.stderr.readline()
                        if line:
                            self.error_signal.emit(line.rstrip())

                if self._process.poll() is not None:
                    break
                    
        except Exception as e:
            self.error_signal.emit(f"[ERROR] {str(e)}")
        finally:
            self.finished_signal.emit()
            if self._process:
                if self._process.stdout:
                    self._process.stdout.close()
                if self._process.stderr:
                    self._process.stderr.close()

    def stop(self):
        self._is_killed = True
        if self._process and self._process.poll() is None:
            self._process.terminate()

