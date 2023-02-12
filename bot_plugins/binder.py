import asyncio
import warnings

from os import mkdir, remove
from os.path import isdir, join
from aiofiles import open as aiopen
from aiohttp import ClientSession

warnings.filterwarnings('ignore')

class Binder:

	def __init__(self):
		self.cache_path = 'cache/'
		if not isdir(self.cache_path[:-1]):
			mkdir(self.cache_path[:-1])
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self._async_setter())

	async def _async_setter(self):
		self.session = ClientSession(trust_env=True)

	async def get_photo(self, name:str) -> bytes:
		async with aiopen(name, 'rb') as photo:
			img = await photo.read()
		remove(name)
		return img

	async def get_parameters(self) -> dict:
		async with aiopen('parameters.json', 'r', encoding = 'utf-8') as file:
			lines = await file.read()
		return eval(f'{lines}')

	async def downoload_photo(self, url:str, filename:str) -> str:
		async with self.session.get(url) as resp:
			if resp.status == 200:
				async with aiopen(join(self.cache_path, filename), 'wb') as new_photo:
					await new_photo.write(await resp.read())
		return join(self.cache_path, filename)

	async def save_photo(self, name:str, content:bytes) -> str:
		if isinstance(content, bytes):
			async with aiopen(join(self.cache_path, name), 'wb') as photo:
				await photo.write(content)
			return join(self.cache_path, name)
		else:
			async with aiopen(join(self.cache_path, name), 'wb') as photo:
				await photo.write(content.read())
			return join(self.cache_path, name)

	async def remove(selff, name:str) -> None:
		remove(name)
	
	async def _destructor(self):
		await self.session.close()

	def __del__(self):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self._destructor())
		loop.close()