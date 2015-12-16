import card_dispenser
import time

card_dispenser_object = card_dispenser.card_dispenser()
while True:
    card_dispenser_object.give_card()
    time.sleep(10)