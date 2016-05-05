import motion_detector
import time

motion_detector_object = motion_detector.motion_detector(17)
motion_detector_object.detection_process()
while True:
    time.sleep(1)
