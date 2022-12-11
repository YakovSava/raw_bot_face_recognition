import asyncio
import warnings

from sys import platform
from os.path import join
from random import randint
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from bot_plugins.binder import Binder
from bot_plugins.ai import recognition
from bot_plugins.commands import command, response
from bot_plugins.states import photo_reg

warnings.filterwarnings('ignore')

if platform in ['linux', 'linux2']:
	try:
		import uvloop
	except ImportError:
		warnings.warn('Please install uvloop ("pip install uvloop") before fast job')
	else:
		asyncio.set_event_loop(uvloop.EventLoopPolicy())
elif platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

binder = Binder()
bot = Bot(asyncio.run(binder.get_parameters())['token'])
dp = Dispatcher(bot)

@dp.message_handler(commands = command.start)
async def start_handler(message:Message):
	await message.answer(response.start)

@dp.message_handler(commands = command.recognition)
async def recognition_first_handler(message:Message):
	await message.answer(response.start)
	await photo_reg.photo.set()

@dp.message_handler(state = photo_reg.photo, content_type = ['photo'])
async def recognition_second_handler(message:Message, state:FSMContext):
	await state.finish()
	photo_name = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	await message.photo[-1].downoload(join(binder.cache_path, f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'))
	await message.answer(response.await_user)
	face_response = await recognition(photo_name)
	photo = await binder.get_photo(photo_name)
	await bot.send_photo(
		chat_id = message['from']['id'],
		photo = photo,
		caption = face_response
	)

@dp.message_handler(commands = command.developer)
async def developer_handler(message:Message):
	await message.answer(response.developer)

if __name__ == '__main__':
	executor(dp, skip_updates = True)