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
		return eval(f'{lines}')
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
<blockquote> The feeling when it gets into your portfolio, but the experience is not :( </blockquote>

#### Librarys in main file
- *asyncio* (**standart library**)
- *warnings* (**standart library**)
- *os* (**standart library**)
- *sys* (**standart library**)
- *random* (**standart library**)
- *aiogram*