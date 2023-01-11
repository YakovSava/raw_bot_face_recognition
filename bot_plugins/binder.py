import asyncio
import warnings

from aiofiles import open as async_open
from aiohttp import ClientSession
from sys import platform
from os.path import isdir, join
from os import mkdir, remove

warnings.filterwarnings('ignore')

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

class Binder:

	def __init__(self):
		self.cache_path = 'cache/'
		if not isdir(self.cache_path[:-1]):
			mkdir(self.cache_path[:-1])

	async def _async_setter(self):
		self.session = ClientSession(trust_env=True)

	async def get_photo(self, name:str) -> bytes:
		async with async_open(join(self.cache_path, name), 'wb') as photo:
			img = await photo.read()
		remove(join(self.cache_path, name))
		return img

	async def get_parameters(self) -> dict:
		async with async_open('parameters.json', 'r', encoding = 'utf-8') as file:
			lines = await file.read()
		return eval(f'{lines}')

	async def downoload_photo(self, url:str, filename:str) -> str:
		async with self.session.get(url) as resp:
			if resp == 200:
				async with async_open(join(self.cache_path, filename), 'wb') as new_photo:
					await new_photo.write(resp.content)
		return join(self.cache_path, filename)
	
	async def _destructor(self):
		await self.session.close()

	def __del__(self):
		asyncio.run(self._destructor())