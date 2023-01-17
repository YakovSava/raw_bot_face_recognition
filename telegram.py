import asyncio
import warnings

from sys import platform
from os.path import join
from random import randint
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext 
from bots_plugins.binder import Binder
from bots_plugins.ai import recognition, recognize
from bots_plugins.states import PhotoReg, RegPhotoToRecognizeText
from config import tgtoken

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

warnings.filterwarnings('ignore')

binder = Binder()
bot = Bot(tgtoken)
dp = Dispatcher()

@dp.message(commands=['start', 'run', 'menu'])
async def start_handler(message:Message):
	await message.answer('''Привет!
Это бот по распознаванию лица. Этот бот может распознавать лица и текст на фото!\
По команде "/recognition" (следующим сообщением надо отправить фото после предупреждения бота) вы можеет воспользоваться функционалом бота)\
По сообщению "/text" бот будет распознаввать текст на фото''')

@dp.message(commands=['rec', 'recognition'])
async def recognition_first_handler(message:Message):
	await message.answer('Следующем сообщением бот попытается распозанать лицо! Он обрежет лицо от всей остальной фотографии и скажет что это.\
Если он это не увидит то вернёт вмечте с фото значение "unknow face"')
	await PhotoReg.photo.set()

@dp.message(state=PhotoReg.photo, content_type=['photo'])
async def recognition_second_handler(message:Message, state:FSMContext):
	await message.answer('Ожидайте ответа')
	await state.finish()
	photo_name = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	await message.photo[-1].downoload(join(binder.cache_path, photo_name))
	face_response = await recognition(photo_name)
	photo = await binder.get_photo(photo_name)
	await bot.send_photo(
		chat_id=message['from']['id'],
		photo=photo,
		caption=face_response
	)

@dp.message(commands=['text'])
async def text_recognition_handler(message:Message):
	await message.answer('Следующим сообщением отправьте фотграфию, бот её распознает и отправит вам текст!')
	await RegPhotoToRecognizeText.photo.set()

@dp.message(state=RegPhotoToRecognizeText.photo, content_type=['photo'])
async def text_recognition_second_handler(message:Message, state:FSMContext):
	await message.answer('Ожидайте ответа')
	await state.finish()
	photo_name = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	await message.photo[-1].downoload(join(binder.cache_path, photo_name))
	ai_response = await recognize(photo_name)
	await message.answer(f'Ответ ИИ: {ai_response}')

@dp.message(commands=['dev', 'developer'])
async def developer_handler(message:Message):
	await message.answer('Разработчик: Савельев Яков\n\
Разработано для: Чайковский индустриальный колледж (http://spo-chik)\n\
GitHub: https://github.com/yakovsava/\n\
Open source: https://github.com/yakovsava/raw_bot_face_recognition')

async def polling(): 
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(polling())