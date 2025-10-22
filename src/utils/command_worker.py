from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
from configparser import ConfigParser
import os
import sys
import threading


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

            # Helper function to read from a stream in a separate thread.
            # This is crucial for real-time output streaming, as it prevents
            # blocking when one stream (stdout or stderr) is idle while the other is active.
            def stream_reader(stream, signal):
                for line in iter(stream.readline, ''):
                    if self._is_killed:
                        break
                    signal.emit(line.rstrip())

            # Create separate threads to read stdout and stderr.
            # This allows non-blocking, concurrent reading of both streams,
            # ensuring that output is displayed as it becomes available,
            # even if one stream is more active than the other.
            stdout_thread = threading.Thread(target=stream_reader, args=(self._process.stdout, self.output_signal))
            stderr_thread = threading.Thread(target=stream_reader, args=(self._process.stderr, self.error_signal))

            stdout_thread.start()
            stderr_thread.start()

            # The main thread waits here for the subprocess to finish.
            # It periodically checks if the process has terminated or if a stop signal was received.
            # This non-blocking wait allows the stream_reader threads to continue emitting output.
            while self._process.poll() is None:
                if self._is_killed:
                    self._process.terminate()
                    break
                self.msleep(100)  # sleep for 100ms to avoid busy waiting

            stdout_thread.join()
            stderr_thread.join()

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