from vkbottle import Keyboard, KeyboardButtonColor, Text

class keyboards:
	start = (Keyboard(one_time=True, inline=False)
		.add(Text('Меню', payload={'menu': 1}), color=KeyboardButtonColor.POSITIVE)
	).get_json()
	menu = (Keyboard(one_time=True, inline=False)
		.add(Text('Распознавание', payload={'recognition': 0}), color=KeyboardButtonColor.POSITIVE)
		.add(Text('Текст', payload={'text': 0, 'recognition': 0}), color=KeyboardButtonColor.POSITIVE)
		.row()
		.add(Text('Разработчик', payload={'developer': 0}), color=KeyboardButtonColor.PRIMARY)
		.row()
		.add(Text('Сайт', payload={'site': 0}), color=KeyboardButtonColor.NEGATIVE)
	).get_json()
	back = (Keyboard(one_time=True, inline=False)
		.add(Text('Вернуться назад', payload={'menu': 1}), color=KeyboardButtonColor.POSITIVE)
	).get_json()