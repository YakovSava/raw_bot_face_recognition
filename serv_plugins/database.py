import asyncio
import aiosqlite

from string import ascii_letters
from typing import Any
from random import choice

class DataBase:

	def __init__(self):
		asyncio.run(self._construct())

	async def _construct(self):
		self.connection = await aiosqlite.connect('cache/users.db', check_same_thread=False)
		self.connection.row_factory = aiosqlite.Row
		self.cursor = await self.connection.cursor()
		self.cursor.execute('''CREATE DATABASE if not exists Users (
	vk BIGINT,
	tg BIGINT,
	quantity INTEGER,
	balance INTEGER,
	token TEXT
)''')

	async def get_all(self) -> tuple:
		await self.cursor.execute('SELECT * FROM Users')
		return await self.cursor.fetchall()

	async def exists(self, exist_id:int=None) -> bool:
		return (await self.get(exist_id)) is not None

	async def reg(self, new:dict=None) -> None:
		await self.cursor.execute('INSERT INTO Users VALUES (?,?,?,?)', (new['vk'], new['tg'], 0, new['balance'], 'not'))
		await self.connection.commit()

	async def delete(self, delete_id:int=None) -> None:
		try: await self.cursor.execute(f'DELETE FROM Users WHERE vk = {delete_id}')
		except: await self.cursor.execute(f'DELETE FROM Users WHERE tg = {delete_id}')
		finally: await self.connection.commit()

	async def get(self, get_id:int=None) -> aiosqlite.Row:
		rec = await self.cursor.execute(f'SELECT * FROM Users WHERE vk = {get_id}')
		if rec is None:
			rec = await self.cursor.execute(f'SELECT * FROM Users WHERE tg = {get_id}')
		return rec

	async def edit(self, edited_id:int=None, what:str=None, to:Any=None) -> None:
		try: await self.cursor.execute(f'UPDATE Users SET what = {to} WHERE vk = {edited_id}')
		except: await self.cursor.execute(f'UPDATE Users SET what = {to} WHERE tg = {edited_id}')
		finally: await self.connection.commit()

	async def edit_int(self, edited_id:int=None, what:str=None, to:int=None) -> None:
		old = (await self.get(edited_id))[what]
		try: await self.cursor.execute(f'UPDATE Users SET what = {old + to} WHERE vk = {edited_id}')
		except: await self.cursor.execute(f'UPDATE Users SET what = {old + to} WHERE tg = {edited_id}')
		finally: await self.connection.commit()

	async def get_token(self, getter_id:int=None) -> str:
		rec = await self.get(getter_id)
		if rec is not None:
			if rec['token'] == 'not':
				token = await self._gen_token()
				await self.edit(
					edited_id=getter_id,
					what='token',
					to=token
				)
			else:
				token = rec['token']
			return token
		else:
			return 'Зарегестрируйтесь!'

	async def _gen_token(self) -> str:
		return ''.join(choice(ascii_letters) for _ in range(10))

	async def _get_all_tokens(self) -> list:
		return list(map(
			lambda x: x['token'],
			(await self.get_all())
		))

	async def _get_all_users_with_tokens(self) -> list:
		return list(filter(
			lambda x: x['token'] != 'not',
			(await self.get_all())
		))

	async def exists_token(self, token:str) -> bool:
		return token in (await self._get_all_tokens())
	
	async def get_from_token(self, token:str) -> int:
		for rec in (await self._get_all_users_with_tokens()):
			if rec['token'] == token:
				return rec['vk'] if rec['vk'] is not None else rec['tg']

database = DataBase()