from ctypes import *
from os import getcwd
from sys import platform

if platform in ['linux', 'linux2']:
	end = '.so'
elif platform in ['win32', 'cygwin', 'msys']:
	end = '.dll'

writer = CDLL(f'./writer{end}')

a = c_char_p(f'{getcwd()}\\file.txt'.encode())
b = c_char_p(b'Help me pls')

writer.write.argtypes = [c_char_p, c_char_p]
writer.write.restype = c_int

print(writer.write(a, b))