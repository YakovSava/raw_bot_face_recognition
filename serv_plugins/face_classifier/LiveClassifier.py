import threading
import cv2

from  serv_plugins.face_classifier.classifier import classify
from copy import deepcopy

class FaceClassifier:

    # Constructor: What classes are to classify?
    def __init__(self, *persons):
        self.__persons = persons

    def liveDetectChange(self, image:str):

        img = cv2.imread(image)

        # Inner function for thread to parallel process image classification according to trained model
        def classifyFace():
            #print("Classifying Face")
            prediction = classify(image, "./tf/training_output/retrained_graph.pb", "./tf/training_output/retrained_labels.txt", shape=224)
            nonlocal text
            text = prediction[0][0]
            #print("Finished classifying with text: " + text)

        # Initialize the cascade classifier for detecting faces
        face_cascade = cv2.CascadeClassifier("./face_cascade/haarcascade_frontalface_default.xml")

        # Initialize the camera (use bigger indices if you use multiple cameras)
        #cap = cv2.VideoCapture(0)
        # Set the video resolution to half of the possible max resolution for better performance
        #cap.set(3, 1920 / 2)
        #cap.set(4, 1080 / 2)

        # Standard text that is displayed above recognized face
        text = "unknown face"
        exceptional_frames = 100
        startpoint = (0, 0)
        endpoint = (0, 0)
        color = (0, 0, 255) # Red
        #while True:
        # Read frame from camera stream and convert it to greyscale
        #ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces using cascade face detection
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # Loop through detected faces and set new face rectangle positions
        for (x, y, w, h) in faces:
            color = (0, 0, 255)
            if not text == "unknown face":
                color = (0, 255, 0)
            oldstartpoint = deepcopy(startpoint)
            startpoint = (x, y)
            endpoint = (x + w, y + h)
            face = (img[y:y + h, x:x + w])
            # Only reclassify if face was lost for at least half a second (15 Frames at 30 FPS)
            if exceptional_frames > 15 or all(abs(i - j) > 15 for i, j in zip(startpoint, oldstartpoint)):
                # Save detected face and start thread to classify it using tensorflow model
                #print("Redetect face due to heavy movement")
                cv2.imwrite(image, face)
                threading._start_new_thread(classifyFace, ())
            exceptional_frames = 0
        # Face lost for too long, reset properties
        if exceptional_frames == 15:
            #print("Exceeded exceptional frames limit")
            text = "unknown face"
            startpoint = (0, 0)
            endpoint = (1, 1)
            # Draw face rectangle and text on image frame
        cv2.rectangle(img, startpoint, endpoint, color, 2)
        textpos = (startpoint[0], startpoint[1] - 7)
        cv2.putText(img, text, textpos, 1, 1.5, color, 2)
        return text