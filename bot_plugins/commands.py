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