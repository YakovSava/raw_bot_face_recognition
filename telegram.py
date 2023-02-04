import asyncio
import warnings

from sys import platform
from random import randint
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_plugins.binder import Binder
from bot_plugins.ai import recognition, recognize
from bot_plugins.states import PhotoReg, RegPhotoToRecognizeText
from serv_plugins.database import database
from config import tgtoken

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

warnings.filterwarnings('ignore')

binder = Binder()
bot = Bot(tgtoken, parse_mode='MarkdownV2')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start', 'run'])
async def start_handler(message:Message):
	is_registred = await database.exists(message.from_id)
	await message.answer(f'''Привет!
Этот бот может распознавать лица и текст на фото!\
По команде "/recognition" (следующим сообщением надо отправить фото после предупреждения бота) вы можеет воспользоваться функционалом бота)\
По сообщению "/text" бот будет распознаввать текст на фото

{'Однако что бы пользоваться ботом, необходимо зарегестрироваться командой "/reg"'
if is_registred else
f"Что бы пользоваться ботом, необходимо иметь на балансе"}''')

@dp.message_handler(commands=['rec', 'recognition'])
async def recognition_first_handler(message:Message):
	await message.answer('Следующем сообщением бот попытается распознать лицо! Он обрежет лицо от всей остальной фотографии и скажет что это.\
Если он это не увидит то вернёт вмеcте с фото значение "unknow face"')
	await PhotoReg.photo.set()

@dp.message_handler(state=PhotoReg.photo, content_types=['photo'])
async def recognition_second_handler(message:Message, state:FSMContext):
	await message.answer('Ожидайте ответа')
	await state.finish()
	photoname = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	file_info = await bot.get_file(message.photo[-1].file_id)
	downloaded_file = await bot.download_file(file_info.file_path)
	photo_name = await binder.save_photo(photoname, downloaded_file)
	face_response = await recognition(photo_name)
	photo = await binder.get_photo(photo_name)
	await bot.send_photo(
		chat_id=message['from']['id'],
		photo=photo,
		caption=face_response
	)

@dp.message_handler(commands=['text'])
async def text_recognition_handler(message:Message):
	await message.answer('Следующим сообщением отправьте фотграфию, бот её распознает и отправит вам текст!')
	await RegPhotoToRecognizeText.photo.set()

@dp.message_handler(state=RegPhotoToRecognizeText.photo, content_types=['photo'])
async def text_recognition_second_handler(message:Message, state:FSMContext):
	await message.answer('Ожидайте ответа')
	await state.finish()
	photoname = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	file_info = await bot.get_file(message.photo[-1].file_id)
	downloaded_file = await bot.download_file(file_info.file_path)
	photo_name = await binder.save_photo(photoname, downloaded_file)
	ai_response = await recognize(photo_name)
	await message.answer(f'Ответ ИИ: {ai_response}')

@dp.message_handler(commands=['dev', 'developer'])
async def developer_handler(message:Message):
	await message.answer('Разработчик: Савельев Яков\n\
Разработано для: [Чайковский индустриальный колледж](http://spo-chik)\n\
GitHub: https://github.com/yakovsava/\n\
Open source: https://github.com/yakovsava/raw_bot_face_recognition')

@dp.message_handler(commands=['/reg'])
async def reg_handler(message:Message):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*['/developer', '/recognition', '/start', '/api', '/balance'])
	if (await database.exists(message.from_id)):
		await message.answer('Вы уже зарегестрированы! Вам не необходимо регестрироваться снова!', reply_markup=keyboard)
	else:
		await database.reg({
			'vk': 0,
			'tg': message.from_id,
			'balance': 0
		})
		await message.answer('Вы успешно зарегестрированы! Теперь вам доступны некоторые функции бота!', reply_markup=keyboard)

@dp.message_handler(commands=['/api'])
async def api_handler(message:Message):
	pass

@dp.message_handler(commands=['/balance'])
async def balance_handler(message:Message):
	pass

def polling(loop=asyncio.get_event_loop()):
	executor.start_polling(dp, skip_updates=True, loop=loop)

if __name__ == '__main__':
	polling()