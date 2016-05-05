import RPi.GPIO as GPIO
import time
import threading
import denexapp_config
import random
import led

# 57 - first sound, 31 - third


class SuperButton:
    def __init__(self, speech_object, led_lamp_object, led_magic_object, hand_object):
        self.list_of_phrases = ("effects/20.mp3",
                                "welcome/5.mp3",
                                "effects/31.mp3")
        self.hand_object = hand_object
        self.led_lamp_object = led_lamp_object
        self.led_magic_object = led_magic_object
        self.speech_object = speech_object
        self.pin = denexapp_config.super_button_pin
        self.led_pin = denexapp_config.super_button_led_pin
        self.phase_duration = denexapp_config.super_button_phase_duration
        self.led_button_object = led.led(self.led_pin, denexapp_config.super_button_led_blink_period, invert=True)
        self.current_phase = 0  # 1 - hand moving, 2 - hand moving + sphere lightning, 3 - hand+sphere+speech
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin of button, takes 1 and 0
        # GPIO.setup(self.led_pin, GPIO.OUT)
        self.presses_in_a_row = 0  # times button pressed in a row during one 'session'
        self.button_blocked = False  # deactivates button's affect on the robot
        self.button_unblock_time = None  # time when button's affect will be unblocked
        self.processes_are_executing = False
        self.led_button_object.start_blink()

    def activate_button(self):
        thread = threading.Thread(target=self._listen_to_button)
        thread.daemon = True
        thread.start()

    def _listen_to_button(self):
        print 'super_button listening started'
        phase_start_time = time.time()  # time when current phase was started
        first_press_in_a_row_time = time.time()
        current_button_state = 0  # 0 if unpressed, 1 if pressed
        while True:
            if self.button_blocked:
                if self.button_unblock_time and time.time() > self.button_unblock_time:
                    self.unblock_button()
                else:
                    time.sleep(0.2)
                    continue
            old_button_state = current_button_state
            try:
                if GPIO.input(self.pin) == 1:
                    current_button_state = 0
                else:
                    current_button_state = 1
            except BaseException:
                print 'problem with super_button state determination'
                time.sleep(5)
            if current_button_state != old_button_state and current_button_state == 1:
                # user pressed button
                print 'user pressed button'
                phase_start_time = time.time()  # start time of current phase
                if not self.presses_in_a_row:
                    first_press_in_a_row_time = time.time()
                self.current_phase += 1  # current phase number
                self.exec_phase()  # activate features of current phase
                self.presses_in_a_row += 1  # adds one more press in a row
                print 'presses in a row: ', self.presses_in_a_row
            if time.time() > (first_press_in_a_row_time + denexapp_config.super_button_blocking_time / 1000):
                self.presses_in_a_row = 0
            if self.presses_in_a_row >= denexapp_config.super_button_presses_in_a_row_allowed\
                    and not self.processes_are_executing \
                    or self.presses_in_a_row >= denexapp_config.super_button_presses_in_a_row_allowed:  # 3 presses max
                self.block_button()
                self.button_unblock_time = first_press_in_a_row_time + denexapp_config.super_button_blocking_time / 1000
                print 'blocking super button for ', self.button_unblock_time - time.time(), ' seconds'
                self.presses_in_a_row = 0
                self.current_phase = 0
            if phase_start_time + self.phase_duration / 1000 < time.time()\
                    and self.processes_are_executing:
                # if current phase ins't 0, but it's time has ended
                print 'stopping phases features'
                self.stop_processes()

    def block_button(self, time_var=None):
        self.button_blocked = True
        self.led_button_object.stop_blink()
        if time_var:
            self.button_unblock_time = time.time() + time_var
        else:
            self.button_unblock_time = None

    def unblock_button(self):
        self.led_button_object.start_blink()
        self.button_blocked = False
        self.button_unblock_time = None

    def try_to_say(self):  # say special phrase if not speaking this moment
        if not self.speech_object.now_saying():
            choice = random.choice(self.list_of_phrases)
            print choice
            self.speech_object.player_play(choice, 100)

    def blink_with_magic_led(self):  # execute one time blink while button is pressed
        GPIO.output(self.led_magic_object.pin, 1)
        time.sleep(1)
        GPIO.output(self.led_magic_object.pin, 0)

    def exec_phase(self):
        self.blink_with_magic_led()
        self.processes_are_executing = True
        if self.current_phase == 1:  # first phase
            print 'staring phase 1'
            self.hand_object.start_move()
        elif self.current_phase == 2:
            print 'staring phase 2'  # second phase
            self.hand_object.stop_move()
            self.led_lamp_object.start_blink()
        elif self.current_phase == 3:  # third phase
            print 'staring phase 3'
            self.hand_object.start_move()
            self.led_lamp_object.start_blink()
            self.blink_with_magic_led()
            self.try_to_say()

    def stop_processes(self):
        self.processes_are_executing = False
        self.hand_object.stop_move()
        self.led_lamp_object.stop_blink()
        print "Super button lamp stop blink"
        #   here could be your code for stopping speech
