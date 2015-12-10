"""
by Denexapp

"""

import threading
import denexapp_config as dconfig
import time
import RPi.GPIO as GPIO

class led_payment():
    stop = True

    def __init__(self):
        #turn to default position
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.led_payment_pin, GPIO.OUT)

    def start_blink(self):
        if self.stop:
            thread = threading.Thread(target=self.__start_blink_action)
            thread.daemon = True
            thread.start()

    def stop_blink(self):
        GPIO.output(dconfig.led_payment_pin, 0)
        self.stop = True

    def __start_blink_action(self):
        self.stop=False
        while True:
            GPIO.output(dconfig.led_payment_pin, 1)
            time.sleep(dconfig.led_payment_period/1000)
            if self.stop:
                break
            GPIO.output(dconfig.led_payment_pin, 0)
            time.sleep(dconfig.led_payment_period/1000)
            if self.stop:
                break