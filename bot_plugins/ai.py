from serv_plugins.face_classifier.tensorBinder import face_rec
from serv_plugins.face_classifier.tensorBinder import TextRecognizer

rec = TextRecognizer()

async def recognition(*args):
	return face_rec(*args)

async def recognize(*args):
	return await rec.recognition(*args)