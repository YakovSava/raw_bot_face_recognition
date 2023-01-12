import ctypes

from sys import platform

libs = {}
if platform in ['linux', 'linux2']:
	end = '.so'
elif platform in ['win32', 'cygwin', 'msys']:
	end = '.dll'

writer = ctypes.CDLL(f'./writer{end}')
reader = ctypes.CDLL(f'./reader{end}')
encryptor = ctypes.CDLL(f'./encrypt{end}')

writer.write.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
writer.write.restype = ctypes.c_int

print(
	writer.write(
		ctypes.c_char_p(b'file.txt'),
		ctypes.c_char_p(b'Hello!')
	)
)