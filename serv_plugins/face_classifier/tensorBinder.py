from serv_plugins.face_classifier.LiveClassifier import FaceClassifier
from serv_plugins.face_classifier.textRecognition import TextRecognizer

classifier = FaceClassifier("Male", "Female")

face_rec = classifier.liveDetectChange