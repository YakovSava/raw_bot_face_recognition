from serv_plugins.face_classifier.tensorBinder import face_rec

async def recognition(*args):
	return face_rec(*args)