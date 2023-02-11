from vkbottle import BaseStateGroup

class SendPhotoState(BaseStateGroup):
	photo = 0
	text = 1

class InputQiwiAmount(BaseStateGroup):
	amount = 0

class InputVkPayAmount(BaseStateGroup):
	amount = 0