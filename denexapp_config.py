"""
by Denexapp

time should be in ms
sudo
"""

# Speech
#mouth_pin = 23
mouth_pin = 23
mouth_closed = 0.9
mouth_half_open = 1.5
mouth_open = 1.9
mouth_sound_time = 220
mouth_recognition_max = 60000

# Behaviour
user_gone_timeout = 1000 # plus 5 sec of hardware MD's delay

# Gsm
gsm_device = "/dev/ttyACM0"
gsm_phone1_default = 79615730488
gsm_phone2_default = 79826301445

# Music
music_file = ["music_1.mp3", "music_2.mp3", "music_3.mp3", "music_4.mp3", "music_5.mp3"]
music_repeat_time = [(19*60+54)*1000, (26*60+5)*1000, (31*60+55)*1000, (22*60+48)*1000, (34*60+23)*1000]
music_volume = 9

# Speech repeat time
repeat_time_far = 10000
repeat_time_close = 10000
repeat_time_pay_more = 45000

# Magic
magic_duration = 36000

# Super button
super_button_pin = 20
super_button_led_pin = 17
super_button_led_blink_period = 1000
super_button_phase_duration = 5000
super_button_blocking_time = 90*1000
super_button_presses_in_a_row_allowed = 3

# Payment
payment_price_default = 100
payment_timeout = 3*60*1000
payment_afterpay_time = 60*1000

# Face detection
face_close_size = 55
face_min_size = 20
face_pattern = "haarcascade_frontalface_alt.xml"

# Hand
hand_pin = 13
# parameters below require to use hand.py instead of hand_2,py
hand_default = 1000
hand_min = 800
hand_max = 1200
hand_time = 3000
hand_direction = 1

# Breathing
#breathing_pin = 24
breathing_pin = 24
#breathing_min = 0.8
breathing_min = 0.8
#breathing_max = 2.3
breathing_max = 2.3
breathing_time = 3000
breathing_delay = 2000

# Motion detector
# these pins should be in a row: power_pin, pin, ground
motion_detector_power_pin = 19
motion_detector_pin = 26

# Led
led_payment_pin = 18
led_payment_period = 0
led_lamp_pin = 12
led_card_pin = 16
led_waiting_pin = 5
led_magic_pin = 6

# Money acceptor
money_device = "/dev/ttyAMA0"
money_capacity_default = 100
money_aware = 25

# Card_dispenser
card_dispenser_pin = 27
card_dispenser_capacity_default = 30
card_dispenser_aware = 10

# Ups
check_interval = 1000
vendor_id = 0x0001
product_id = 0x0000
