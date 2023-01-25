import asyncio

from aiohttp import ClientSession
from sys import argv

async def main():
	async with ClientSession(trust_env=True) as session:
		await asyncio.gather(*[session.get(argv[1]) for _ in range(5)])

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()