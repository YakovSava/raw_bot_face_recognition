from os import mkdir, remove
from os.path import isdir, join
from aiofiles import open as aiopen

class Binder:

	def __init__(self):
		self.config_file = 'parameters.json'
		self.cache_path = 'cache'
		self.html_file = 'html'
		if not isdir(self.cache_path):
			mkdir(self.cache_path)
			print('Cache path is create')
		if not isdir(self.html_file):
			mkdir(self.html_file)
			with open(join(self.html_file, 'index.html'), 'w', encoding='utf-8') as file:
				file.write('<!DOCTYPE html>')

	async def _write_bytes(self, content:bytes, name:str) -> bool:
		try:
			async with aiopen(join(self.cache_path, name), 'wb') as new_photo:
				await new_photo.write(content)
		except:
			return False
		else:
			return True

	async def get_config(self) -> dict:
		async with aiopen(self.config_file, 'r', encoding='utf-8') as file:
			lines = await file.read()
		return eval(f'{lines}')

	async def save_photo(self, content:bytes, name:str) -> bool:
		if isinstance(content, bytes):
			return await self._write_bytes(content, name)
		else:
			return False

	async def get_photo(self, name:str) -> bytes:
		async with aiopen(join(self.cache_path, name), 'rb') as photo:
			photo = await photo.read()
		remove(join(self.cache_path, name))
		return photo

	async def delete_photo(self, name:str) -> bool:
		try:
			remove(join(self.cache_path, name))
		except:
			return False
		else:
			return True
	
	async def get_page(self, route_page:str) -> str:
		try:
			async with aiopen(join(self.html_file, route_page), 'r', encoding='utf-8') as html:
				file_reads = await html.read()
		except:
			file_reads = 'false'
		finally:
			return file_reads

	async def server_get_photo(self, name:str) -> bytes:
		async with aiopen(join(self.html_file, name), 'rb') as photo:
			return await photo.read()

	async def get_open_source(self) -> str:
		async with aiopen('server.py', 'r', encoding='utf-8') as py:
			return await py.read()