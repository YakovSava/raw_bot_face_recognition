import asyncio
import cppyy

from os import listdir
from typing import Any
from concurrent.futures import ThreadPoolExecutor

class Downoloader:

	def __init__(self, loop:asyncio.AbstractEventLoop=asyncio.get_event_loop()):
		self._loop = loop
		self._loop.run_until_complete(self._setter())

	async def _setter(self):
		with ThreadPoolExecutor() as pool:
			await asyncio.gather(*[
				self._loop.run_in_executor(pool, cppyy.include(file))
				for file in (listdir())
				if file.endswith('.cxx')
			])


	def __getattr__(self, name:str) -> Any:
		return getattr(cppyy.gbl, name)