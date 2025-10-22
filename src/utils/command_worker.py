from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
from configparser import ConfigParser
import os
import sys
import threading
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
                CONFIG_PATH = f"{os.environ.get('HOME', '~')}/.config/peppy/peppy.conf"
                if not os.path.isfile(CONFIG_PATH):
                    # Create the directory if it doesn't exist
                    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
                    # Create the config file with default values
                    config = ConfigParser(interpolation=None)
                    config["MISC"] = {'PATHS': ''}
                    with open(CONFIG_PATH, 'w') as configfile:
                        config.write(configfile)

                config = ConfigParser(interpolation=None)
                config.read(CONFIG_PATH)
                paths = config["MISC"].get('PATHS', '')
            except (KeyError, Exception) as e:
                # Handle potential errors during config file reading
                paths = ''
                self.error_signal.emit(f"[CONFIG ERROR] {str(e)}")

            command = f'export PATH="$PATH:{paths}";{self.command_text}'
            self._process = subprocess.Popen(command,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True,
                                             text=True,
                                             bufsize=1,
                                             universal_newlines=True
                                             )

            # Use select to read from stdout and stderr in a non-blocking way
            while True:
                if self._is_killed:
                    self._process.terminate()
                    break

                # Check if there's data to read from stdout or stderr
                rlist, _, _ = select.select([self._process.stdout, self._process.stderr], [], [], 0.1) # 0.1 second timeout

                for fd in rlist:
                    if fd == self._process.stdout:
                        line = self._process.stdout.readline()
                        if line:
                            self.output_signal.emit(line.rstrip())
                    elif fd == self._process.stderr:
                        line = self._process.stderr.readline()
                        if line:
                            self.error_signal.emit(line.rstrip())

                # If the process has terminated and there's no more output, break the loop
                if self._process.poll() is not None and not rlist:
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