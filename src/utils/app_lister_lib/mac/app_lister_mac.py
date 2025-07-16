import ctypes
import json
import os

lib = ctypes.CDLL(os.path.abspath(os.path.join(os.path.dirname(__file__),'app_lister.so')))
# lib.listApplications()

# set return type for testjson()
# lib.listApplications.restype=ctypes.c_char_p

# calling function
# jsontest_bytes=lib.testjson()
# jsontest_str=jsontest_bytes.decode('utf-8')

# converting json to python dict
# data=json.loads(li)
# print(data)

# don't use c_char_p, memory must be manually freed and c_char_p doesnt support properly w/ go allocated memory
# set return type of func
# restype = ctypes.c_void_p, func returns a pointer (*void) and not a string or int
lib.listApplications.restype = ctypes.c_void_p

# define argument type for go func, expects void pointer (c_void_p)
lib.FreeCString.argtypes = [ctypes.c_void_p]

ptr = lib.listApplications()
# print("Pointer received from Go:", ptr)

# convert c string pointer to python string
json_str = ctypes.string_at(ptr).decode("utf-8")

# free memory that was allocated in go, using C.CString() for the string
lib.FreeCString(ptr)

mac_apps = json.loads(json_str)
