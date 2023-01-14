from ctypes import *
from sys import platform

if platform in ['linux', 'linux2']:
	end = '.so'
elif platform in ['win32', 'cygwin', 'msys']:
	end = '.dll'

writer = windll.LoadLibrary(f'./writer.cxx{end}')
# reader = ctypes.CDLL(f'./reader{end}')
# encryptor = ctypes.CDLL(f'./encrypt{end}')

string = 'Hi!'
string = string.encode('utf-16')

print(string)

a = c_char_p(b'file.txt')
b = c_char_p(string)

# writer.write.argtypes = [c_char_p, c_char_p]
writer.write.restype = c_int

print(writer.write(a, a))