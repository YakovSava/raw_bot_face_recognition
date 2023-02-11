import asyncio
import warnings

from random import randint
from pyqiwip2p import AioQiwiP2P
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
	CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_plugins.binder import Binder
from bot_plugins.ai import recognition, recognize
from bot_plugins.states import PhotoReg, RegPhotoToRecognizeText, Qiwi
from serv_plugins.database import database
from config import tgtoken, qiwi_token

warnings.filterwarnings('ignore')

binder = Binder()
bot = Bot(tgtoken)
dp = Dispatcher(bot, storage=MemoryStorage())
qiwi = AioQiwiP2P(qiwi_token)
cb = CallbackData('Bill Storage', 'bill')

@dp.message_handler(commands=['start', 'run', 'menu'])
async def start_handler(message:Message):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	is_registred = await database.exists(message.from_id)
	keyboard.add(*['/recognition', '/text', '/developer', '/api', '/balance']) if is_registred else keyboard.add('/reg')
	await message.answer(f'''Привет!
Этот бот может распознавать лица и текст на фото!\
По команде "/recognition" (следующим сообщением надо отправить фото после предупреждения бота) вы можеет воспользоваться функционалом бота)\
По сообщению "/text" бот будет распознаввать текст на фото

{'Однако что бы пользоваться ботом, необходимо зарегестрироваться командой "/reg"'
if is_registred else
f"Что бы пользоваться ботом, необходимо иметь на балансе 0 рублей"}''')

@dp.message_handler(commands=['rec', 'recognition'])
async def recognition_first_handler(message:Message):
	if (await database.exists(message.from_id)):
		await message.answer('Следующем сообщением бот попытается распознать лицо! Он обрежет лицо от всей остальной фотографии и скажет что это.\
Если он это не увидит то вернёт вмеcте с фото значение "unknow face"')
		await PhotoReg.photo.set()
	else:
		await message.answer('Вы не зарегестрированы и не можете пользоваться ботом')

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
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(['/menu'])
	await bot.send_photo(
		chat_id=message['from']['id'],
		photo=photo,
		caption=face_response,
		reply_markup=keyboard
	)

@dp.message_handler(commands=['text'])
async def text_recognition_handler(message:Message):
	if (await database.exists(message.from_id)):
		await message.answer('Следующим сообщением отправьте фотграфию, бот её распознает и отправит вам текст!')
		await RegPhotoToRecognizeText.photo.set()
	else:
		await message.answer('Вы не зарегестрированы и не можете пользоваться ботом')

@dp.message_handler(state=RegPhotoToRecognizeText.photo, content_types=['photo'])
async def text_recognition_second_handler(message:Message, state:FSMContext):
	await message.answer('Ожидайте ответа')
	await state.finish()
	photoname = f'{message["from"]["id"]}_{randint(1000, 9999)}.jpg'
	file_info = await bot.get_file(message.photo[-1].file_id)
	downloaded_file = await bot.download_file(file_info.file_path)
	photo_name = await binder.save_photo(photoname, downloaded_file)
	ai_response = await recognize(photo_name)
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(['/menu'])
	await message.answer(f'Ответ ИИ: {" ".join(ai_response)}', reply_markup=keyboard)

@dp.message_handler(commands=['dev', 'developer'])
async def developer_handler(message:Message):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(['/menu'])
	await message.answer('Разработчик: Савельев Яков\n\
Разработано для: Чайковский индустриальный колледж (http://spo-chik)\n\
GitHub: https://github.com/yakovsava/\n\
Open source: https://github.com/yakovsava/raw_bot_face_recognition', reply_markup=keyboard)

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
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*['/back'])
	token = await database.get_token(message.from_id)
	await message.answer(f'Вот ваш токен: {token}\n\n{"Теперь вы можете отправлять запросы напрямую к API" if token.lower() != "зарегестрируйтесь!" else "Вы не зарегестрированы, потому вам не выдан токен!"}')

@dp.message_handler(commands=['/balance'])
async def balance_handler(message:Message):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	if (await database.exists(message.from_id)):
		keyboard.add(*['/back', '/api', '/qiwi'])
		await message.answer('Вы можете пополнить ваш баланс при помощи Qiwi. Иных способов пока что нету', reply_markup=keyboard)
	else:
		keyboard.add('/reg')
		await message.answer('Вы не можете даже пополнить кошелёк ввиду его отсутствия!\nЗарегестрируйтесь!', reply_markup=keyboard)

@dp.message_handler(commands=['/qiwi'])
async def qiwi_handler_step1(message:Message):
	if (await database.exists(message.from_id)):
		await message.answer('Напишите число на которое вы хотите пополнить ваш баланс')
		await Qiwi.qiwi.set()
	else:
		await message.answer('Ты настолько настойчивый что прописал команду что бы пополнить баланс?')

@dp.message_handler(state=Qiwi.qiwi)
async def qiwi_handler_step2(message:Message, state:FSMContext):
	if message.text.isdigit():
		await state.finish()
		if int(message.text) > 0:
			to_bill = int(message.text)
		else:
			to_bill = 100
		price = await qiwi.bill(
			amount=to_bill,
			comment='Оплата бота'
		)
		inline_keyboard = InlineKeyboardMarkup(row_width=1)
		inline_keyboard.add(
			InlineKeyboardButton('Проверить оплату', callback_data=cb.new(bill=price.bill_id))
		)
		await message.answer(f'Персональная ссылка для оплаты: {price.pay_url}\n\
Ссылка работает лишь 30 минут, потому советуем вам оплатить скорее!\n\
Что бы вернуться назад напишите "/menu"')
	else:
		await message.answer('Введите ЧИСЛО')

@dp.callback_query_handler(cb.filter())
async def check_pay(call:CallbackQuery, callback_data:dict):
	price = await qiwi.bill(bill_id=callback_data['bill'])
	if price.status == 'PAID':
		await call.message.answer(f'Вы успешно оплатили и ваш баланс теперь пополнен на {price.amount} рублей!')
		await database.edit_int(
			edited_id=call.message.from_id,
			what='balance',
			to=int(round(price.amount, 0))
		)
	else:
		await call.message.answer('Оплата пока ещё не поступала')

def polling(loop=asyncio.get_event_loop()):
	executor.start_polling(dp, skip_updates=True, loop=loop)

if __name__ == '__main__':
	polling()