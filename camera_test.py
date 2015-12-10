import camera
import time

if __name__ == '__main__':
    camera_object = camera.camera()
    camera_object.start_detection()
    while True:
        time.sleep(1)