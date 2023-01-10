import asyncio
import warnings

from sys import platform
from os.path import join
from random import randint
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from bots_plugins.binder import Binder
from bots_plugins.ai import recognition
from bots_plugins.states import photo_reg
from config import tgtoken

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

warnings.filterwarnings('ignore')

binder = Binder()
bot = Bot(tgtoken)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'run', 'menu'])
async def start_handler(message:Message):
	await message.answer('''Привет!
Это бот по распознаванию лица. Этот бот может распознавать лица (удивительно). По команде "/recognition" (следующим сообщением надо отправить фото после предупреждения бота) вы можеет воспользоваться функционалом бота)''')

@dp.message_handler(commands=['rec', 'recognition'])
async def recognition_first_handler(message:Message):
	await message.answer('Следующем сообщением бот попытается распозанать лицо! Он обрежет лицо от всей остальной фотографии и скажет что это. Если он это не увидит то вернёт вмечте с фото значение "unknow face"')
	await photo_reg.photo.set()

@dp.message_handler(state=photo_reg.photo, content_type=['photo'])
async def recognition_second_handler(message:Message, state:FSMContext):
	await state.finish()
	photo_name = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	await message.photo[-1].downoload(join(binder.cache_path, f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'))
	await message.answer('Ожидайте ответа')
	face_response = await recognition(photo_name)
	photo = await binder.get_photo(photo_name)
	await bot.send_photo(
		chat_id = message['from']['id'],
		photo = photo,
		caption = face_response
	)

@dp.message_handler(commands=['dev', 'developer'])
async def developer_handler(message:Message):
	await message.answer('Разработчик: Савельев Яков\nРазработано для: Чайковский индустриальный колледж (http://spo-chik)\nGitHub: https://github.com/yakovsava/\nOpen source: https://github.com/yakovsava/raw_bot_face_recognition')

if __name__ == '__main__':
	executor(dp, skip_updates = True)