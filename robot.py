"""
by Denexapp
Uses some parts of Tony DiCola's pi-facerec-box project under MIT license
"""

import camera
# import hand # < old file designed to work with servos
import hand_2 as hand
import breathing
import speech
import led
import denexapp_config as dconfig
import money_acceptor
import card_dispenser
import speech_markup
import time
import gsm
import ups

if __name__ == "__main__":
    speech_scenario = 1
    payment_state = 0
    # 0 - no money, 1 - part of money, 2 - enough money
    last_magic_time = time.time() - 2*dconfig.payment_afterpay_time
    # last time of prediction
    last_far_time = time.time() - 2 * (dconfig.repeat_time_far / 1000)
    # last time of speech when user is far
    last_close_time = time.time() - 2 * (dconfig.repeat_time_close / 1000)
    # last time of speech when user is close
    last_close_state_time = time.time() - 2 * dconfig.user_gone_timeout / 1000
    last_far_state_time = time.time() - 2 * dconfig.user_gone_timeout / 1000

    camera_object = camera.camera()
    hand_object = hand.hand()
    breathing_object = breathing.breathing()
    speech_object = speech.speech()
    led_payment_object = led.led(dconfig.led_payment_pin, dconfig.led_payment_period)
    led_lamp_object = led.led(dconfig.led_lamp_pin, 0)
    card_dispenser_object = card_dispenser.card_dispenser()
    money_acceptor_object = money_acceptor.money_acceptor()
    gsm_object = gsm.gsm(money_acceptor_object, card_dispenser_object)
    ups_object = ups.ups(gsm_object)
    ups_object.start_monitoring()
    money_acceptor_object.start()
    gsm_object.start()
    camera_object.start_detection()
    # 0 - no user, 1 - user is far, 2 - user is close

    last_camera_detection_time = camera_object.last_update

    def set_user_position():
        global last_camera_detection_time
        global last_close_state_time
        global last_far_state_time
        if last_camera_detection_time != camera_object.last_update:
            last_camera_detection_time = camera_object.last_update
            if camera_object.user_position == 2:
                last_close_state_time = time.time()
            elif camera_object.user_position == 1:
                last_far_state_time = time.time()

    def get_user_position():
        if time.time() - last_close_state_time < (dconfig.user_gone_timeout / 1000):
            return 2
        elif time.time() - last_far_state_time < (dconfig.user_gone_timeout / 1000):
            return 1
        else:
            return 0

    print "Loop started"
    while True:
        if payment_state == 0:
            if not(money_acceptor_object.able_to_work() and
                    card_dispenser_object.able_to_work() and
                    ups_object.able_to_work()):
                breathing_object.stop_move()
                led_payment_object.stop_blink()
                money_acceptor_object.reject_money()
                if speech_object.player:
                    speech_object.player.terminate()

            if not money_acceptor_object.able_to_work():
                print "not able to work: money box full"
                gsm_object.send_status("money box full")

            if not card_dispenser_object.able_to_work():
                print "not able to work: out of cards"
                gsm_object.send_status("cards out")

            while not(money_acceptor_object.able_to_work() and
                      card_dispenser_object.able_to_work() and
                      ups_object.able_to_work()):
                time.sleep(3)

            if card_dispenser_object.cards_left() <= dconfig.card_dispenser_aware\
                    and not card_dispenser_object.card_send_warning:
                gsm_object.send_status("cards almost out")
                card_dispenser_object.card_send_warning = True

            if money_acceptor_object.capacity - money_acceptor_object.cash_banknotes\
                    <= dconfig.money_aware and not money_acceptor_object.money_send_warning:
                gsm_object.send_status("money box almost full")
                money_acceptor_object.money_send_warning = True

            led_payment_object.start_blink()
            money_acceptor_object.accept_money()
            while (time.time() - last_magic_time) < (dconfig.payment_afterpay_time / 1000):
                set_user_position()
                if money_acceptor_object.cash_session >= money_acceptor_object.price:
                    payment_state = 2
                elif money_acceptor_object.cash_session > 0:
                    payment_state = 1
                if payment_state != 0 or not ups_object.able_to_work():
                    break
                time.sleep(0.2)
            set_user_position()
            if get_user_position() == 2:
                breathing_object.start_move()
                while True:
                    set_user_position()
                    if money_acceptor_object.cash_session >= money_acceptor_object.price:
                        payment_state = 2
                    elif money_acceptor_object.cash_session > 0:
                        payment_state = 1
                    if ((time.time() - last_close_time) >= (dconfig.repeat_time_close / 1000)) \
                            and (not speech_object.now_saying()):
                        last_close_time = time.time()
                        speech_object.say(speech_markup.sound_scenarios[speech_scenario][1])
                    time.sleep(0.2)
                    if get_user_position() != 2 or payment_state != 0 or not ups_object.able_to_work():
                        break
            elif get_user_position() == 1:
                breathing_object.start_move()
                while True:
                    set_user_position()
                    if money_acceptor_object.cash_session >= money_acceptor_object.price:
                        payment_state = 2
                    elif money_acceptor_object.cash_session > 0:
                        payment_state = 1
                    if ((time.time() - last_far_time) >= (dconfig.repeat_time_far / 1000)) \
                            and (not speech_object.now_saying()):
                        speech_object.say(speech_markup.sound_scenarios[speech_scenario][0])
                        last_far_time = time.time()
                    time.sleep(0.2)
                    if get_user_position() != 1 or payment_state != 0 or not ups_object.able_to_work():
                        break
            elif get_user_position() == 0:
                breathing_object.stop_move()
                last_music_time = time.time() - 2 * dconfig.music_repeat_time[speech_scenario]
                while True:
                    set_user_position()
                    if money_acceptor_object.cash_session >= money_acceptor_object.price:
                        payment_state = 2
                    elif money_acceptor_object.cash_session > 0:
                        payment_state = 1
                    if (time.time() - last_music_time) >= (dconfig.music_repeat_time[speech_scenario] / 1000)\
                            and not speech_object.now_saying():
                        last_music_time = time.time()
                        speech_object.player_play(dconfig.music_file[speech_scenario], dconfig.music_volume)
                    time.sleep(0.2)
                    if get_user_position() != 0 or payment_state != 0 or not ups_object.able_to_work():
                        break
        elif payment_state == 1:
            led_payment_object.start_blink()
            breathing_object.start_move()
            money_acceptor_object.accept_money()
            last_pay_time = money_acceptor_object.cash_last_pay_time
            last_paymore_speech_time = time.time() - (dconfig.repeat_time_pay_more / 1000)
            two_minutes_left_said = False
            while True:
                if money_acceptor_object.cash_session >= money_acceptor_object.price:
                    payment_state = 2
                if (time.time() - last_paymore_speech_time) > (dconfig.repeat_time_pay_more / 1000):
                    last_paymore_speech_time = time.time()
                    speech_object.say(10)
                if last_pay_time != money_acceptor_object.cash_last_pay_time:
                    two_minutes_left_said = False
                    if money_acceptor_object.cash_session < money_acceptor_object.price:
                        speech_object.say(10)
                    last_pay_time = money_acceptor_object.cash_last_pay_time
                    last_paymore_speech_time = time.time()
                if ((dconfig.payment_timeout - (time.time() - last_pay_time)) <= 2 * 60) and (two_minutes_left_said is False) \
                        and (speech_object.now_saying() is False):
                    speech_object.say(7)
                    two_minutes_left_said = True
                if money_acceptor_object.cash_session >= money_acceptor_object.price:
                    payment_state = 2
                if (time.time() - last_pay_time) >= (dconfig.payment_timeout / 1000):
                    payment_state = 0
                    money_acceptor_object.cash_session = 0
                if payment_state != 1:
                    break
                time.sleep(0.2)
        elif payment_state == 2:
            money_acceptor_object.cash_session = 0
            led_payment_object.stop_blink()
            breathing_object.start_move()
            money_acceptor_object.reject_money()
            time.sleep(1)
            led_lamp_object.start_blink()
            time.sleep(1)
            speech_object.say(15)
            time.sleep(1)
            hand_object.start_move()
            time.sleep(dconfig.magic_duration / 1000)
            led_lamp_object.stop_blink()
            card_dispenser_object.give_card()
            hand_object.stop_move()
            speech_object.say(speech_markup.sound_scenarios[speech_scenario][2])
            breathing_object.stop_move()
            payment_state = 0
            last_magic_time = time.time()
            speech_scenario += 1
            if speech_scenario > 5:
                speech_scenario = 1
