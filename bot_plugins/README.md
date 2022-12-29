## Bot plugins
Special self-written plugins written in *Python* were written for this bot. One of the plugins (*ai.py*) uses one of the server/site plugins.

## Plugin Requirements
All plugins are extremely small but require a large number of libraries:
- *asyncio* (**standart library**)
- *warnings* (**standart library**)
- *sys* (**standart library**)
- *os* (**standart library**)
- *aiofiles*
- *aiogram*

## Parts of the code
Some parts of the code look quite strange, you could call it a shit code, but believe me, this is done for the greatest beauty of the main file:

#### binder.py:
```py
class Binder:

	# Our code

	async def get_parameters(self) -> dict:
		async with async_open('parameters.json', 'r', encoding = 'utf-8') as file:
			lines = await file.read()
		return eval(f'dict({lines})')
```
- bot.py
```py
@dp.message_handler(state = photo_reg.photo, content_type = ['photo'])
async def recognition_second_handler(message:Message, state:FSMContext):
	# Code
	photo = await binder.get_photo(photo_name) # <-- Using binder.py (initialized)
	await bot.send_photo(
		chat_id = message['from']['id'],
		photo = photo,
		caption = face_response
	)
```
#### commands.py
```py
class command:
	start = ['start', 'run', 'menu']
	recognition = ['rec', 'recognition']
	developer = ['dev', 'developer']

class response:
	start = '''Привет!
Это бот по распознаванию лица. Этот бот может распознавать лица (удивительно). По команде "/recognition" (следующим сообщением надо отправить фото после предупреждения бота) вы можеет воспользоваться функционалом бота)'''
	recognition = 'Следующем сообщением бот попытается распозанать лицо! Он обрежет лицо от всей остальной фотографии и скажет что это. Если он это не увидит то вернёт вмечте с фото значение "unknow face"'
	developer = 'Разработчик: Савельев Яков\nРазработано для: Чайковский индустриальный колледж (http://spo-chik)\nGitHub: https://github.com/yakovsava/\nOpen source: https://github.com/yakovsava/raw_bot_face_recognition'
	await_user = 'Ожидайте ответа'
```
- bot.py
```py
@dp.message_handler(commands = command.start)
async def start_handler(message:Message):
	await message.answer(response.start)

@dp.message_handler(commands = command.recognition)
async def recognition_first_handler(message:Message):
	await message.answer(response.start)
	await photo_reg.photo.set()
```
<blockquote> The feeling when it gets into your portfolio, but the experience is not :( </blockquote>

#### Librarys in main file
- *asyncio* (**standart library**)
- *warnings* (**standart library**)
- *os* (**standart library**)
- *sys* (**standart library**)
- *random* (**standart library**)
- *aiogram*
<blockquote> And *uvloop* in Linux </blockquote>