import asyncio

from aiohttp import ClientSession

async def getter():
	async with ClientSession(trust_env=True) as session:
		async with session.get('http://192.168.100.6:9000/api/all') as resp:
			if resp.status == 200:
				response = await resp.json()
	print(response)

async def post_put_delete():
	pass

if __name__ == '__main__':
	asyncio.run(getter())