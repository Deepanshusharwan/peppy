import ctypes
import json

lib=ctypes.CDLL('./main.so')
# lib.listApplications()

# set return type for testjson()
lib.listApplications.restype=ctypes.c_char_p

# calling function
jsontest_bytes=lib.listApplications()
jsontest_str=jsontest_bytes.decode('utf-8')

#converting json to python dict
data=json.loads(li)
print(data)
