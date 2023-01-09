import ctypes

from os import listdir
from sys import platform

class DynamicLibrarys:

	class NotSupported(Exception): pass

	def __init__(self):
		self.libs = {}
		if platform in ['linux', 'linux2']:
			end = '.so'
		elif platform in ['win32', 'cygwin', 'msys']:
			end = '.dll'
		else:
			raise self.NotSupported()
		for file in (listdir('cxx/')):
			if file.endswith(end):
				self.libs[file.split('.'[0])] = ctypes.CDLL(file)

	def __del__(self):
		del self.libs
		del self.libs