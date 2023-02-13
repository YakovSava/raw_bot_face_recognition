from os import exists
from ctypes import *

class Downoload:

	def __init__(self):
		if exists('cxx/writer.dll'):
			writer = CDLL('./cxx/writer.dll')
			writer.write.argtypes = [c_char_p, c_char_p]; writer.write.restypes = c_int
			async def write(self, filename:str, lines:str) -> int:
				return writer.write(filename.encode(), lines.encode())
			self.writer = write

	def __getattr__(self, attr_name:str):
		return None