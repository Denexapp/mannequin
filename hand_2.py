"""
by Denexapp

"""

import denexapp_config as dconfig
import RPi.GPIO as GPIO
import time

class hand():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.hand_pin, GPIO.OUT)
        time.sleep(0.3)
        GPIO.output(dconfig.hand_pin, 1)

    def start_move(self):
        GPIO.output(dconfig.hand_pin, 0)

    def stop_move(self):
        GPIO.output(dconfig.hand_pin, 1)