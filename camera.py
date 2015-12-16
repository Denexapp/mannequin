"""
by Denexapp

"""

import cv2
import threading
import denexapp_config as dconfig
import picam
import time

class camera():

    def __init__(self):
        self.camera = picam.OpenCVCapture()
        self.stop = False
        self.user_position = 0

    def start_detection(self):
        thread = threading.Thread(target=self.__start_detection_action)
        thread.daemon = True
        thread.start()

    def stop_detection(self):
        self.stop = True

    def __start_detection_action(self):
        self.stop=False
        while True:
            image = self.camera.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = cv2.resize(image, (0, 0), fx=0.6, fy=0.6)
            cv2.imwrite('captureResized.pgm', image)
            result = self.detect_single(image)
            if result != None:
                face_size = (result[2]+result[3])/2
                print ("Face size is ", result[2], "x", result[3])
                if face_size >= dconfig.face_close_size:
                    self.user_position = 2
                    print "User is close", time.time()
                else:
                    self.user_position = 1
                    print "User is far", time.time()
            else:
                self.user_position = 0
                print "User isn't seen", time.time()
            if self.stop:
                break

    def detect_single(self,image):
        haar_faces = cv2.CascadeClassifier(dconfig.face_pattern)
        faces = haar_faces.detectMultiScale(image,
                    scaleFactor=1.3,
                    minNeighbors=4,
                    minSize=(dconfig.face_min_size, dconfig.face_min_size),
                    flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) > 1:
            max_value = faces[0].w + faces[0].h
            max_id = 0
            counter = 0
            while counter < len(faces):
                value = faces[counter].w + faces[counter].h
                if value > max_value:
                    max_id = counter
                counter += 1
            return faces[max_id]
        if len(faces) < 1:
            return None
        return faces[0]