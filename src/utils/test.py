import ctypes
import json

lib=ctypes.CDLL('./main.so')
lib.listApplications()
lib.testjson.restype=ctypes.c_char_p

# calling function
jsontest_bytes=lib.testjson()
jsontest_str=jsontest_bytes.decode('utf-8')

#converting json to python dict
data=json.loads(jsontest_str)
print(data)
