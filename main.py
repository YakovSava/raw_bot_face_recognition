import asyncio 

from time import sleep
from multiprocessing import Process
from server import runner
from telegram import polling as tgpolling
from vkontakte import polling as vkpolling

def main():
	loop = asyncio.get_event_loop()
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

if __name__ == '__main__':
	main()