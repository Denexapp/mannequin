import RPi.GPIO as GPIO
import threading
import time
import denexapp_config as dconfig
import file_io

class card_dispenser():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dconfig.card_dispenser_pin, GPIO.OUT)
        GPIO.output(dconfig.card_dispenser_pin, 1)
        self.cards_given = file_io.read("card_dispenser_file")
        self.capacity = file_io.read("card_capacity_file")
        if self.capacity == 0:
            self.set_capacity(dconfig.card_dispenser_capacity_default)
        self.card_send_warning = False

    def set_capacity(self, capacity):
        self.capacity = capacity
        file_io.write("card_capacity_file", capacity)

    def able_to_work(self):
        return self.cards_given < self.capacity

    def cards_left(self):
        return self.capacity - self.cards_given

    def reset(self):
        self.cards_given = 0
        file_io.write("card_dispenser_file", self.cards_given)
        self.card_send_warning = False

    def give_card(self):
        thread = threading.Thread(target=self.__give_card_action)
        thread.daemon = True
        thread.start()

    def __give_card_action(self):
        GPIO.output(dconfig.card_dispenser_pin, 0)
        self.cards_given += 1
        file_io.write("card_dispenser_file", self.cards_given)
        time.sleep(1)
        GPIO.output(dconfig.card_dispenser_pin, 1)