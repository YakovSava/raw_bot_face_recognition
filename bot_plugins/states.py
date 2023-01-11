from aiogram.dispatcher.filters.state import State, StatesGroup

class PhotoReg(StatesGroup):
	photo = State()

class RegPhotoToRecognizeText(StatesGroup):
	photo = State()