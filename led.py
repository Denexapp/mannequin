"""
by Denexapp

"""

import threading
import time
import RPi.GPIO as GPIO

class led():
    def __init__(self, pin, period, invert=False):
        self.stop = True
        self.on = 0
        self.off = 1
        if invert:
            self.on = 1
            self.off = 0
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.period = period
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, self.off)

    def start_blink(self):
        if self.stop:
            thread = threading.Thread(target=self.__start_blink_action)
            thread.daemon = True
            thread.start()

    def stop_blink(self):
        GPIO.output(self.pin, self.off)
        self.stop = True

    def __start_blink_action(self):
        self.stop = False
        if self.period != 0:
            while True:
                GPIO.output(self.pin, self.on)
                time.sleep(self.period/1000)
                if self.stop:
                    break
                GPIO.output(self.pin, self.off)
                time.sleep(self.period/1000)
                if self.stop:
                    break
        else:
            GPIO.output(self.pin, self.on)
