import RPi.GPIO as GPIO
import threading
import time
import denexapp_config as dconfig

class card_dispenser():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.card_dispencer_pin, GPIO.OUT)
        GPIO.output(dconfig.card_dispencer_pin, 0)

    def give_card(self):
        thread = threading.Thread(target=self.__give_card_action)
        thread.daemon = True
        thread.start()

    def __give_card_action(self):
        GPIO.output(dconfig.card_dispencer_pin, 1)
        time.sleep(1)
        GPIO.output(dconfig.card_dispencer_pin, 0)