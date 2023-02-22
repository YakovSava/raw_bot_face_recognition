from os import mkdir
from os.path import isdir, join, exists
from json import dumps, loads
from aiofiles import open as aiopen
from cxx.downoloader import Downoloader

class Binder:

	def __init__(self):
		self.config_file = 'parameters.json'
		self.cache_path = 'cache'
		self.html_file = 'html'
		self.downoload = Downoloader()
		if not isdir(self.cache_path):
			mkdir(self.cache_path)
			print('Cache path is create')
		if not isdir(self.html_file):
			mkdir(self.html_file)
			self.downoload.write(join(self.html_file, 'index.html'), '<!DOCTYPE html>')
		if not exists(join(self.cache_path, 'parameters.json')):
			self.downoload.write('parameters.json', '''{
	"admin": [],
	"count": 0
}''')

	async def _write_bytes(self, content:bytes, name:str) -> bool:
		try:
			async with aiopen(join(self.cache_path, name), 'wb') as new_photo:
				await new_photo.write(content)
		except:
			return False
		else:
			return True

	async def get_config(self) -> dict:
		lines = self.downoload.read(self.config_file)
		return eval(f'{lines}')

	async def save_photo(self, content:bytes, name:str) -> bool:
		if isinstance(content, bytes):
			return await self._write_bytes(content, name)
		else:
			return False

	async def get_photo(self, name:str) -> bytes:
		async with aiopen(join(self.cache_path, name), 'rb') as photo:
			photo = await photo.read()
		self.downoload.deleter(join(self.cache_path, name))
		return photo

	async def delete_photo(self, name:str) -> bool:
		try:
			self.downoload.deleter(join(self.cache_path, name))
		except:
			return False
		else:
			return True
	
	async def get_page(self, route_page:str) -> str:
		try:
			file_reads = self.downoload.read(join(self.html_file, route_page))
		except:
			file_reads = 'false'
		finally:
			return file_reads

	async def server_get_photo(self, name:str) -> bytes:
		async with aiopen(join(self.html_file, name), 'rb') as photo:
			return await photo.read()

	async def get_open_source(self) -> str:
		return self.downoload.read('server.py')

	async def get_photo_by_name(self, filename:str) -> bytes:
		async with aiopen(join(self.cache_path, filename), 'rb') as file: byte = await file.read()
		self.downoload.deleter(join(self.cache_path, filename))
		return byte
	
	async def get_parameters(self) -> dict:
		return loads(self.downoload.read('parameters.json'))

	async def edit_parameters(self, new_parameters:dict) -> None:
		self.downoload.write('parameters.json', f'{dumps(new_parameters)}')