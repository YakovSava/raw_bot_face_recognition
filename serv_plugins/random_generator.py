from string import printable
from random import randint, choice

class Generator:

	def __init__(self):
		self._storage = []

	async def get(self) -> str:
		key = ''
		for _ in range(randint(0, 30)):
			key += choice(printable)
		self._storage.append(key)
		return key

	async def check(self, key:str) -> bool:
		return key in self._storage

	async def delete(self, key:str) -> None:
		self._storage.remove(key)