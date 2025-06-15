import ctypes
lib=ctypes.CDLL('./main.so')
lib.listApplications()
