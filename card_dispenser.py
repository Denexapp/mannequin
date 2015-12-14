import RPi.GPIO as GPIO
import threading
import time
import denexapp_config as dconfig
import file_io

class card_dispenser():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.card_dispencer_pin, GPIO.OUT)
        GPIO.output(dconfig.card_dispencer_pin, 0)
        self.cards_given = file_io.read("card_dispenser_file")

    def able_to_work(self):
        return self.cards_given < dconfig.card_dispenser_capacity

    def give_card(self):
        thread = threading.Thread(target=self.__give_card_action)
        thread.daemon = True
        thread.start()

    def __give_card_action(self):
        GPIO.output(dconfig.card_dispencer_pin, 1)
        self.cards_given += 1
        file_io.write("card_dispenser_file", self.cards_given)
        time.sleep(1)
        GPIO.output(dconfig.card_dispencer_pin, 0)