"""
by Denexapp

"""

import threading
import time
import RPi.GPIO as GPIO

class led():
    def __init__(self, pin, period):
        self.stop = True
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.period = period
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)

    def start_blink(self):
        if self.stop:
            thread = threading.Thread(target=self.__start_blink_action)
            thread.daemon = True
            thread.start()

    def stop_blink(self):
        GPIO.output(self.pin, 1)
        self.stop = True

    def __start_blink_action(self):
        self.stop = False
        if self.period != 0:
            while True:
                GPIO.output(self.pin, 0)
                time.sleep(self.period/1000)
                if self.stop:
                    break
                GPIO.output(self.pin, 1)
                time.sleep(self.period/1000)
                if self.stop:
                    break
        else:
            GPIO.output(self.pin, 0)
