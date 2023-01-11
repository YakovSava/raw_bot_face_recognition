import ctypes

from os import listdir
from sys import platform

libs = {}
if platform in ['linux', 'linux2']:
	end = '.so'
elif platform in ['win32', 'cygwin', 'msys']:
	end = '.dll'
for file in (listdir()):
	if file.endswith(end):
		libs[file.split('.')[0]] = ctypes.CDLL(f'./{file}')
print(ctypes.c_char_p(b'reader.cxx'))
print(ctypes.c_char_p(libs['reader'].get()).value)