import asyncio 

from time import sleep
from multiprocessing import Process
from server import runner
from telegram import polling as tgpolling
from vkontakte import polling as vkpolling

def main():
	for func in [runner, tgpolling]:
		pr = Process(target=func)
		pr.start()
	sleep(1)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(vkpolling())
		])
	)

if __name__ == '__main__':
	main()