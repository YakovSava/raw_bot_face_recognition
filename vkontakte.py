import warnings
import asyncio

from vkbottle.bot import Bot, Message
from vkbottle import PhotoMessageUploader
from sys import platform
from vkplugins.keyboards import keyboards
from bot_plugins.binder import Binder
from bot_plugins.ai import recognition, recognize
from serv_plugins.random_generator import Generator
from config import vktoken

try:
	from loguru import logger
except ImportError:
	pass
else:
	logger.disable('vkbottle')

warnings.filterwarnings('ignore')

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

vk = Bot(token=vktoken)
vk.on.vbml_ignore_case = True
gen = Generator()
binder = Binder()

@vk.on.private_message(text='Начать')
async def start_handler(message:Message):
	await message.answer('Здравствуйте!\nЭто бот для обнаружения лица на фотографии ли распознаванию текста на ней. Для того что бы начать нажмите на кнопку ниже', keyboard=keyboards.start)

@vk.on.private_message(payload={'menu': 0})
async def menu_handler(message:Message):
	await message.answer('Выберите одно из действий ниже:\n\
Распознование - распознает лицо на фото\n\
Текст - распознает текст на фото (могут быть ложные срабатывания; не работает с капчей)\n\
Разработчик - отобразить информацию о разработчике\n\
Сайт - перевдёт вас на сайт', keyboard=keyboards.menu)

@vk.on.private_message(payload={'recognition': 0})
async def recognition_handler(message:Message):
	await message.answer('Ожидайте ответа')
	key = await gen.get(); await gen.delete(key)
	absolute_path = await binder.downoload_photo(message.attachments[0][0].url, f'{key}.png')
	ai_resp = await recognition(absolute_path)
	attach = await PhotoMessageUploader(vk.api).upload(ai_resp)
	await message.answer('Ответ нейросети:', attachment=attach, keyboard=keyboards.back)

@vk.on.private_message(payload={'text': 0, 'recognition': 0})
async def text_recognition_handler(message:Message):
	await message.answer('Ожидайте ответа')
	key = await gen.get(); await gen.delete(key)
	absolute_path = await binder.downoload_photo(message.attachments[0][0].url, f'{key}.png')
	ai_resp = await recognize(f'{key}.png')
	user_photo = await PhotoMessageUploader(vk.api).upload(absolute_path)
	await message.answer(f'Ответ нейросети:\n{ai_resp}', attachment=user_photo, keyboard=keyboards.back)

@vk.on.private_message(payload={'developer': 0})
async def show_developer_handler(message:Message):
	await message.answer('Разработчик: Савельев Яков\n\
Разработано для: Чайковский индустриальный колледж (http://spo-chik)\n\
GitHub: https://github.com/yakovsava/\n\
Open source: https://github.com/yakovsava/raw_bot_face_recognition', keyboard=keyboards.back)

@vk.on.private_message(payload={'site': 0})
async def show_site_handler(message:Message):
	await message.answer('Наш сайт: САЙТА ПОКА ЧТО НЕТУ!!!', keyboard=keyboards.back)

@vk.on.private_message()
async def this_command_not_exists(message:Message):
	await message.answer('Ваша комана не распознана', keyboard=keyboards.back)

async def polling():
	await vk.run_polling()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(polling())