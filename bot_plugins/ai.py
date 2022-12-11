from serv_plugins.face_classification_tensorflow.tensorBinder import face_rec

async def recognition(*args):
	return face_rec(*args)