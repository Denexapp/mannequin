"""
by Alidus

"""

import threading
import time
import RPi.GPIO as GPIO


# pin which near the mode switcher (yellow one) is Ground, mid pin is Output
# and third is power 5V. Works fine in H mode (edge position of yellow switcher)


class motion_detector:
    def __init__(self, pin, power_pin):
        self.stop = False  # detection stops if True
        self.pin = pin  # number of pin used for m/d
        self.power_pin = power_pin  # power_pin gives power to detector
        self.is_user = 0  # does m.d. is noticing motion or not
        self.last_update = time.time()  # last time when m.d. checked for people
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)  # configuration pin to input mode
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.output(self.power_pin, 1)

    def start_detection(self):
        thread = threading.Thread(target=self._detection_process)
        thread.daemon = True
        thread.start()

    def stop_detection(self):
        self.stop = True

    def _detection_process(self):
        curr_state = 0
        self.stop = False
        print "detection started"
        while not self.stop:
            prev_state = curr_state
            curr_state = GPIO.input(self.pin)
            if curr_state != prev_state:
                if curr_state == 0:
                    print "nothing is moving"
                    self.is_user = 0
                else:
                    print "something is moving"
                    self.is_user = 1
            self.last_update = time.time()
            time.sleep(0.1)
