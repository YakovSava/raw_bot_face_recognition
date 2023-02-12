import asyncio

from sys import argv
from aiohttp import ClientSession, ClientResponse
from aiofiles import open as aiopen

async def main():
	async with ClientSession(trust_env=True) as session:
		host = argv[1]
		async with session.get(host) as resp:
			if resp.status == 200:
				resps = await asyncio.gather(*[
					asyncio.create_task(session.get(f'{host}/api/{api}'))
					for api in ['all', 'open', 'links']
				])
				for resp in resps:
					resp:ClientResponse
					if resp.status == 200:
						print(await resp.json())
					else:
						print(resp.status)
					resp.close()

				async with aiopen('test1.png', 'rb') as file:
					f1 = await file.read()
				async with aiopen('test0.png', 'rb') as file:
					f0 = await file.read()
				post_resps = await asyncio.gather(*[
					asyncio.create_task(session.post(f'{host}/api/{method}', data=data))
					for method, data in [
						['recognition', {'token': 'dxlvzSMBPc', 'photo': f1}],
						['text', {'token': 'dxlvzSMBPc', 'photo': f0}],
						['balance', {'token': 'dxlvzSMBPc'}]
					]
				])
				print({'token': 'dxlvzSMBPc', 'photo': f1})
				for post_resp in post_resps:
					post_resp:ClientResponse
					print(await post_resp.read())
					if post_resp.status == 200:
						print(await post_resp.json())
					else:
						print(resp.status)
					post_resp.close()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())