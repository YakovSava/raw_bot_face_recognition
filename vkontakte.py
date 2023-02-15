import asyncio
import warnings

from random import randint
from pyqiwip2p import AioQiwiP2P
from vkbottle.bot import Bot, Message
from vkbottle import PhotoMessageUploader, ABCRule
from vkplugins.keyboards import keyboards
from vkplugins.states import SendPhotoState, InputQiwiAmount, InputVkPayAmount
from bot_plugins.binder import Binder
from bot_plugins.ai import recognition, recognize
from serv_plugins.database import database
from config import vktoken, qiwi_token

# try:
# 	from loguru import logger
# except ImportError:
# 	pass
# else:
# 	logger.disable('vkbottle')

warnings.filterwarnings('ignore')

class VKPay(ABCRule[Message]):
	async def check(self, message:Message):
		payload = eval(f'{message.payload}')
		try: payload['vkpay'], payload['pay']
		except: return False
		else: return True

class CheckerQiwi(ABCRule[Message]):
	async def check(self, message:Message):
		payload = eval(f'{message.payload}')
		try: payload['check'], payload['bill_id']
		except: return False
		else: return True

vk = Bot(token=vktoken)
vk.on.vbml_ignore_case = True
uploader = PhotoMessageUploader(vk.api)
qiwi = AioQiwiP2P(qiwi_token)
binder = Binder()
null = None

@vk.on.private_message(text='Начать')
async def start_handler(message:Message):
	if (await vk.state_dispenser.get(message.from_id)) is not None:
		await vk.state_dispenser.delete(message.from_id)
	await message.answer('Здравствуйте!\nЭто бот для обнаружения лица на фотографии ли распознаванию текста на ней.\n\
Для того что бы начать необходимо авторизоваться', keyboard=keyboards.start)

@vk.on.private_message(payload={'menu': 0})
async def menu_handler(message:Message):
	if not (await database.exists(message.from_id)):
		await database.reg({
			'id': message.from_id,
			'balance': 0
		})
		await message.answer('Вы успешно зарегестрированы и теперь вам доступны некоторые возможности бота!')
	await message.answer('Выберите одно из действий ниже:\n\
Распознование - распознает лицо на фото\n\
Текст - распознает текст на фото (могут быть ложные срабатывания; не работает с капчей)\n\
Разработчик - отобразить информацию о разработчике', keyboard=keyboards.menu)

@vk.on.private_message(payload={'recognition': 0})
async def recognition_handler(message:Message):
	if (await database.get(message.from_id))['balance'] <= 0:
		await message.answer('Вы не можете пользоваться ботом, пока у вас на балансе 0')
	else:
		await message.answer('Следующим сообщением отправьте вашу фотографию на которой необходимо распознать человека\n\
	Бот обрежет лицо человека и попытается распознать его лицо. Если у него не получиться это сделать, он вернёт ответ "Unknow face"')
		await vk.state_dispenser.set(message.from_id, SendPhotoState.photo)

@vk.on.private_message(state=SendPhotoState.photo)
async def await_photo(message:Message):
	if message.attachments is not None:
		await vk.state_dispenser.delete(message.from_id)
		await message.answer('Ожидайте ответа')
		name = f'{message.from_id}_{randint(1000, 9999)}.png'
		absolute_path = await binder.downoload_photo(message.attachments[-1].photo.sizes[-1].url, name)
		ai_resp = await recognition(absolute_path)
		attach = await uploader.upload(absolute_path)
		await binder.remove(absolute_path)
		await message.answer(f'Ответ нейросети: {ai_resp}\n\nЛицо найденное на фото:', attachment=attach, keyboard=keyboards.back)
		await database.edit_int(edited_id=message.from_id, to='quantity', what=1)
	else:
		await message.answer('Вы не отправили фото!')

@vk.on.private_message(payload={'text': 0, 'recognition': 0})
async def text_recognition_handler(message:Message):
	if (await database.get(message.from_id))['balance'] <= 0:
		await message.answer('Вы не можете пользоваться ботом, пока у вас на балансе 0')
	else:
		await message.answer('Следующим сообщением отправьте фотографию на которой необходимо распознать текст\n\
	ЕСли отправите фото без текста, бот пришлёт пустой ответ')
		await vk.state_dispenser.set(message.from_id, SendPhotoState.text)

@vk.on.private_message(state=SendPhotoState.text)
async def await_text(message:Message):
	if message.attachments is not None:
		await vk.state_dispenser.delete(message.from_id)
		await message.answer('Ожидайте ответа')
		name = f'{message.from_id}_{randint(1000, 9999)}.png'
		absolute_path = await binder.downoload_photo(message.attachments[-1].photo.sizes[-1].url, name)
		ai_resp = await recognize(absolute_path)
		user_photo = await uploader.upload(absolute_path)
		await binder.remove(absolute_path)
		await message.answer(f'Ответ нейросети:\n{" ".join(ai_resp)}', attachment=user_photo, keyboard=keyboards.back)
		await database.edit_int(edited_id=message.from_id, to='quantity', what=1)
	else:
		await message.answer('Вы не прислали фото!')

@vk.on.private_message(payload={'developer': 0})
async def show_developer_handler(message:Message):
	await message.answer('Разработчик: Савельев Яков\n\
Разработано для: Чайковский индустриальный колледж (http://spo-chik)\n\
GitHub: https://github.com/yakovsava/\n\
Open source: https://github.com/yakovsava/raw_bot_face_recognition', keyboard=keyboards.back)

@vk.on.private_message(payload={'api': 0})
async def api_handler(message:Message):
	token = await database.get_token(message.from_id)
	await message.answer(f'Вот ваш токен: {token}\n\n\
{"Теперь вы можете отправлять запросы напрямую к API" if token.lower() != "зарегестрируйтесь!" else "Вы не зарегестрированы, потому вам не выдан токен!"}', keyboard=keyboards.back)

@vk.on.private_message(payload={'pay': 0})
async def pay_handler(message:Message):
	await message.answer('Выберите действие', keyboard=keyboards.pay)

@vk.on.private_message(payload={'qiwi': 0})
async def qiwi_pay_step1(message:Message):
	await vk.state_dispenser.set(message.from_id, InputQiwiAmount.amount)
	await message.answer('Введите сумму которую хотите внести нна баланс')

@vk.on.private_message(state=InputQiwiAmount.amount)
async def qiwi_pay_step2(message:Message):
	if message.text.isdigit():
		await vk.state_dispenser.delete(message.from_id)
		if int(message.text) > 0:
			to_bill = int(message.text)
		else:
			to_bill = 100
		price = await qiwi.bill(
			amount=to_bill,
			comment='Оплата бота'
		)
		await message.answer(f'Персональная ссылка для оплаты: {price.pay_url}', keyboard=keyboards.inline.check_pay(price.bill_id))
		await message.answer('Ссылка работает лишь 30 минут, потому советуем вам оплатить скорее!', keyboard=keyboards.back)
	else:
		await message.answer('Введите ЧИСЛО')

@vk.on.private_message(payload={'VKPay': 0})
async def vkpay_step1(message:Message):
	await vk.state_dispenser.set(message.from_id, InputVkPayAmount.amount)
	await message.answer('Введите сумму которую хотите внести нна баланс')

@vk.on.private_message(state=InputVkPayAmount.amount)
async def vkpay_step2(message:Message):
	if message.text.isdigit():
		await vk.state_dispenser.delete(message.from_id)
		if int(message.text) > 0:
			to_bill = int(message.text)
		else:
			to_bill = 100
		group_id = (await vk.api.groups.get_by_id())[0].id
		await message.answer(f'Персональная кнопка для оплаты:', keyboard=keyboards.vkpay(group_id, to_bill))
	else:
		await message.answer('Введите ЧИСЛО')

@vk.on.private_message(VKPay())
async def vkpay_pay(message:Message):
	amount = eval(f'{message.payload}')['amount']
	await message.answer(f'Вы успешно пополнили баланс на {amount} рублей')
	if amount == 42:
		await message.answer('Вы купили жизнь!')
	await database.edit_int(
		edited_id=message.from_id,
		what='balance',
		to=amount
	)

@vk.on.private_message(CheckerQiwi())
async def check_qiwi_pay(message:Message):
	payload = eval(f'{message.payload}')
	bill = await qiwi.bill(bill_id=payload['bill_id'])
	if bill.status == 'PAID':
		if bill.amount == 42:
			await message.answer('Вы купили жизнь!')
		await message.answer(f'Вы успешно пополнили баланс на {bill.amount} рублей', keyboard=keyboards.back)
		await database.edit_int(
			edited_id=message.from_id,
			what='balance',
			to=int(bill.amount)
		)
	else:
		await message.answer('Оплата ещё не поступала')

@vk.on.private_message()
async def this_command_not_exists(message:Message):
	await message.answer('Ваша команда не распознана', keyboard=keyboards.back)

async def polling():
	await vk.run_polling()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(polling())