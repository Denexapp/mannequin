"""
by Denexapp
Uses some parts of Tony DiCola's pi-facerec-box project
"""

import time
import camera
#import hand # < old file designed to work with servos
import hand_2 as hand
#import breathing
#import speech
#import led_payment
import denexapp_config as dconfig
import money_acceptor
import RPi.GPIO as GPIO

if __name__ == '__main__':
    user_position = 0
    # 0 - no user, 1 - user is far, 2 - user is close
    payment_state = 0
    # 0 - no money, 1 - part of money, 2 - enough money
    cash_inside = 0
    cash_session = 0
    cash_got = 0
    last_magic_time = time.time() - 2*dconfig.payment_afterpay_time

    GPIO.cleanup()
    camera_object = camera.camera()
    hand_object = hand.hand()
    #breathing_object = breathing.breathing()
    #speech_object = speech.speech()
    #led_payment_object = led_payment.led_payment()
    #money_acceptor_object = money_acceptor.money_acceptor()
    #money_acceptor_object.start_working()


    print "Loop started"
    while True:
        if payment_state == 0:
            #money_acceptor_object.accept_money()
            while time.time().__sub__(last_magic_time) < dconfig.payment_afterpay_time:
                if payment_state != 0:
                    break
                time.sleep(0.2)
            if user_position == 0:
                #whispering
                last_whisper_time = time.time().__sub__(dconfig.repeat_time_whisper)
                while True:
                    if time.time().__sub__(last_whisper_time) >= dconfig.repeat_time_whisper:
                        last_whisper_time = time.time()
                        #speech_object.say()
                        #todo add whisper sound above
                    time.sleep(0.2)
                    if user_position != 0 or payment_state != 0:
                        break
            elif user_position == 1:
                last_far_time = time.time().__sub__(dconfig.repeat_time_far)
                while True:
                    if time.time().__sub__(last_far_time) >= dconfig.repeat_time_far:
                        speech_object.say("come_to_me.mp3", "2000 1 1 2 300 2 2 800 2 300 1~300 1~500 1~250 1~300 300 2~500")
                        last_far_time = time.time()
                        #todo add sound above
                    time.sleep(0.2)
                    if user_position != 1 or payment_state != 0:
                        break
            elif user_position == 2:
                last_close_time = time.time().__sub__(dconfig.repeat_time_close)
                while True:
                    if time.time().__sub__(last_close_time) >= dconfig.repeat_time_close:
                        last_close_time = time.time()
                        #speech_object.say()
                        #todo add sound above
                    time.sleep(0.2)
                    if user_position != 2 or payment_state != 0:
                        break
        elif payment_state == 1:
            #money_acceptor_object.accept_money()
            last_pay_time = time.time()
            last_paymore_speech_time = time.time().__sub__(dconfig.repeat_time_pay_more)
            while True:
                if cash_session >= dconfig.payment_price:
                    payment_state = 2
                if time.time().__sub__(last_paymore_speech_time) > dconfig.repeat_time_pay_more:
                    last_paymore_speech_time = time.time()
                    #speech_object.say()
                    #todo add sound above
                if cash_got > 0:
                    cash_session += cash_got
                    cash_inside += cash_got
                    cash_got = 0
                    last_pay_time = time.time()
                if cash_session >= dconfig.payment_price:
                    payment_state = 2
                if time.time().__sub__(last_pay_time) >= dconfig.payment_timeout:
                    #speech_object.say("","")
                    #todo add sound above
                    time.sleep(10)
                    payment_state = 0
                if payment_state != 1:
                    cash_session = 0
                    break
                time.sleep(0.2)
        elif payment_state == 2:
            #money_acceptor_object.reject_money()
            #speech_object.say("","")
            #todo add sound
            hand_object.start_move()
            time.sleep(10)
            hand_object.stop_move()
            payment_state = 0
            last_magic_time = time.time()
    print "End"