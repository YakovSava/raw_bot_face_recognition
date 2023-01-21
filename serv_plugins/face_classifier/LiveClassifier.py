import threading
import cv2

from  serv_plugins.face_classifier.classifier import classify
from copy import deepcopy

class FaceClassifier:
	def __init__(self, *persons):
		self.__persons = persons

	def liveDetectChange(self, image:str):

		img = cv2.imread(image)

		def classifyFace():
			prediction = classify(image, "./tf/training_output/retrained_graph.pb", "./tf/training_output/retrained_labels.txt", shape=224)
			nonlocal text
			text = prediction[0][0]
		face_cascade = cv2.CascadeClassifier("./face_cascade/haarcascade_frontalface_default.xml")

		text = "unknown face"
		exceptional_frames = 100
		startpoint = (0, 0)
		endpoint = (0, 0)
		color = (0, 0, 255)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x, y, w, h) in faces:
			color = (0, 0, 255)
			if not text == "unknown face":
				color = (0, 255, 0)
			oldstartpoint = deepcopy(startpoint)
			startpoint = (x, y)
			endpoint = (x + w, y + h)
			face = (img[y:y + h, x:x + w])
			if exceptional_frames > 15 or all(abs(i - j) > 15 for i, j in zip(startpoint, oldstartpoint)):
				cv2.imwrite(image, face)
				threading._start_new_thread(classifyFace, ())
			exceptional_frames = 0
		if exceptional_frames == 15:
			text = "unknown face"
			startpoint = (0, 0)
			endpoint = (1, 1)
		cv2.rectangle(img, startpoint, endpoint, color, 2)
		return text