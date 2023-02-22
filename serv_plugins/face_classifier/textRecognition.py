# Что бы вы понимали. я случайно удалил файл...
import asyncio

from os.path import exists, isdir
from os import mkdir
from concurrent.futures import ThreadPoolExecutor
from easyocr import Reader

class TextRecognizer:

	class OCRError(Exception): pass

	def __init__(self, standart_path:str='cache', loop:asyncio.AbstractEventLoop=asyncio.get_event_loop()):
		if not isdir(standart_path):
			mkdir(standart_path)
		self.path = standart_path
		self.reader = Reader(['ru', 'en'])
		self._loop = loop

	async def recognition(self, filename:str=None) -> str:
		if filename is None:
			raise self.OCRError('Filename is None!')
		elif not exists(filename):
			raise self.OCRError('File name is not exists!')
		else:
			with ThreadPoolExecutor() as pool:
				return await self._loop.run_in_executor(pool, self.reader.readtext(filename, detail=0))
			