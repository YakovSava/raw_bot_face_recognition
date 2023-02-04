# Что бы вы понимали. я случайно удалил файл...
from os.path import exists, isdir, join
from os import mkdir
from easyocr import Reader

class TextRecognizer:

	class OCRError(Exception): pass

	def __init__(self, standart_path:str='cache'):
		if not isdir(standart_path):
			mkdir(standart_path)
		self.path = standart_path
		self.reader = Reader(['ru', 'en'])

	async def recognition(self, filename:str=None) -> str:
		if filename is None:
			raise self.OCRError('Filename is None!')
		elif not exists(filename):
			raise self.OCRError('File name is not exists!')
		else:
			return (self.reader.readtext(filename, detail=0))
			