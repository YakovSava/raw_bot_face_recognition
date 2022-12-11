import asyncio
import warnings

from sys import platform
from os.path import isdir, join
from os import mkdir, remove
from aiofiles import open as async_open

warnings.filterwarnings('ignore')

if platform in ['linux', 'linux2']:
	try:
		import uvloop
	except ImportError:
		warnings.warn('Please install uvloop ("pip install uvloop") before fast job')
	else:
		asyncio.set_event_loop(uvloop.EventLoopPolicy())
elif platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

class Binder:

	def __init__(self):
		self.cache_path = 'cache/'
		if not isdir(self.cache_path[:-1]):
			mkdir(self.cache_path[:-1])

	async def get_photo(self, name:str) -> bytes:
		async with async_open(join(self.cache_path, name), 'wb') as photo:
			img = await photo.read()
		remove(join(self.cache_path, name))
		return img

	async def get_parameters(self) -> dict:
		async with async_open('parameters.json', 'r', encoding = 'utf-8') as file:
			lines = await file.read()
		return eval(f'dict({lines})')