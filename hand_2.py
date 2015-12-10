"""
by Denexapp

"""

import denexapp_config as dconfig
import RPi.GPIO as GPIO

class hand():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.hand_pin, GPIO.OUT)

    def start_move(self):
        GPIO.output(dconfig.hand_pin, 1)

    def stop_move(self):
        GPIO.output(dconfig.hand_pin, 0)