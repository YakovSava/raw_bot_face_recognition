import asyncio

from concurrent.futures import ThreadPoolExecutor
from serv_plugins.face_classifier.LiveClassifier import FaceClassifier
from serv_plugins.face_classifier.textRecognition import TextRecognizer

classifier = FaceClassifier("Male", "Female")

async def face_rec(path, loop:asyncio.AbstractEventLoop=asyncio.get_event_loop()):
	with ThreadPoolExecutor() as pool:
		return await loop.run_in_executor(pool, classifier.liveDetectChange)