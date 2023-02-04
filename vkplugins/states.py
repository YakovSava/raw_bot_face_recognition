from vkbottle_types import BaseStateGroup

class SendPhotoState(BaseStateGroup):
	photo = 0

class InputQiwiAmount(BaseStateGroup):
	amount = 0

class InputVkPayAmount(BaseStateGroup):
	amount = 0