import hand_2 as hand
import time

hand_object = hand.hand()
while True:
    hand_object.start_move()
    time.sleep(5)
    hand_object.stop_move()
    time.sleep(5)
