import asyncio 

from server import runner
from telegram import polling as tgpolling
from vkontakte import polling as vkpolling

loop = asyncio.get_event_loop()
loop.run_until_complete(
	asyncio.wait([
		loop.create_task(runner()),
		loop.create_task(tgpolling()),
		loop.create_task(vkpolling())
	])
)