import asyncio

from sys import platform
from time import sleep
from multiprocessing import Process
from server import runner
from telegram import polling as tgpolling
from vkontakte import polling as vkpolling

if platform in ['win32', 'cygwin', 'msys']:
	try: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except: pass

if __name__ == '__main__':
	loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
	pr = Process(target=tgpolling, kwargs={'loop': loop})
	pr.start()
	pr = Process(target=runner, kwargs={'loop': loop})
	pr.start()
	sleep(1)
	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(vkpolling())
		])
	)