"""
by Denexapp
Uses some parts of Tony DiCola's pi-facerec-box project under MIT license
"""

import time

cash_money = 0
# amount of money inside
cash_banknotes = 0
# amount of banknotes
cash_session = 0
# amount of money got during current session
cash_last_pay_time = time.time()
# last time when a banknote was accepted
#todo connect speech module, make voice markup
#todo set config values
#todo connect money acceptor through uart
#todo remove limits, use devices' api instead
#todo make gsm module

import camera
#import hand # < old file designed to work with servos
import hand_2 as hand
import breathing
import speech
import led_payment
import denexapp_config as dconfig
import money_acceptor
import card_dispenser
import speech_markup

if __name__ == "__main__":
    payment_state = 0
    # 0 - no money, 1 - part of money, 2 - enough money
    cash_session = 0
    # amount of money gotten in current session
    last_magic_time = time.time() - 2*dconfig.payment_afterpay_time
    # last time of prediction

    camera_object = camera.camera()
    hand_object = hand.hand()
    breathing_object = breathing.breathing()
    speech_object = speech.speech()
    led_payment_object = led_payment.led_payment()
    card_dispenser_object = card_dispenser.card_dispenser()
    money_acceptor_object = money_acceptor.money_acceptor()

    money_acceptor_object.start_working()
    camera_object.start_detection()
    # 0 - no user, 1 - user is far, 2 - user is close

    print "Loop started"
    while True:
        if money_acceptor_object.able_to_work() and card_dispenser_object.able_to_work():
            breathing_object.stop_move()
            led_payment_object.stop_blink()
            money_acceptor_object.reject_money()
            while True:
                time.sleep(3)
        if payment_state == 0:
            #todo ask should led_payment blink when human isn't close
            led_payment_object.start_blink()
            money_acceptor_object.accept_money()
            while (time.time() - last_magic_time) < (dconfig.payment_afterpay_time / 1000):
                if payment_state != 0:
                    break
                time.sleep(0.2)
            if camera_object.user_position == 0:
                #whispering
                breathing_object.stop_move()
                last_whisper_time = time.time() - dconfig.repeat_time_whisper / 1000
                while True:
                    if (time.time() - last_whisper_time) >= (dconfig.repeat_time_whisper / 1000):
                        last_whisper_time = time.time()
                        speech_object.say(speech_markup.sound_files[8], speech_markup.sound_markup[8])
                        #todo add music
                    time.sleep(0.2)
                    if camera_object.user_position != 0 or payment_state != 0:
                        break
            elif camera_object.user_position == 1:
                breathing_object.start_move()
                last_far_time = time.time() - (dconfig.repeat_time_far / 1000)
                while True:
                    if (time.time() - last_far_time) >= (dconfig.repeat_time_far / 1000):
                        speech_object.say(speech_markup.sound_files[2], speech_markup.sound_markup[2])
                        last_far_time = time.time()
                    time.sleep(0.2)
                    if camera_object.user_position != 1 or payment_state != 0:
                        break
            elif camera_object.user_position == 2:
                breathing_object.start_move()
                last_close_time = time.time() - (dconfig.repeat_time_close / 1000)
                while True:
                    if (time.time() - last_close_time) >= (dconfig.repeat_time_close / 1000):
                        last_close_time = time.time()
                        speech_object.say(speech_markup.sound_files[4], speech_markup.sound_markup[4])
                    time.sleep(0.2)
                    if camera_object.user_position != 2 or payment_state != 0:
                        break
        elif payment_state == 1:
            led_payment_object.start_blink()
            breathing_object.start_move()
            money_acceptor_object.accept_money()
            last_pay_time = cash_last_pay_time
            last_paymore_speech_time = time.time() - (dconfig.repeat_time_pay_more / 1000)
            while True:
                if cash_session >= dconfig.payment_price:
                    payment_state = 2
                if (time.time() - last_paymore_speech_time) > (dconfig.repeat_time_pay_more / 1000):
                    last_paymore_speech_time = time.time()
                    speech_object.say(speech_markup.sound_files[10], speech_markup.sound_markup[10])
                if cash_last_pay_time != time.time():
                    if cash_session < dconfig.payment_price:
                        speech_object.say(speech_markup.sound_files[10], speech_markup.sound_markup[10])
                    cash_last_pay_time = time.time()
                if cash_session >= dconfig.payment_price:
                    payment_state = 2
                if (time.time() - last_pay_time) >= (dconfig.payment_timeout / 1000):
                    speech_object.say(speech_markup.sound_files[14], speech_markup.sound_markup[14])
                    time.sleep(10)
                    payment_state = 0
                if payment_state != 1:
                    cash_session = 0
                    break
                time.sleep(0.2)
        elif payment_state == 2:
            led_payment_object.stop_blink()
            breathing_object.start_move()
            money_acceptor_object.reject_money()
            speech_object.say(speech_markup.sound_files[15], speech_markup.sound_markup[15])
            hand_object.start_move()
            time.sleep(dconfig.magic_duration / 1000)
            card_dispenser_object.give_card()
            hand_object.stop_move()
            speech_object.say(speech_markup.sound_files[1], speech_markup.sound_markup[1])
            breathing_object.stop_move()
            payment_state = 0
            last_magic_time = time.time()
