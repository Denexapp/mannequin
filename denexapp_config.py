"""
by Denexapp

time should be in ms

"""

# Speech
mouth_pin = 23
mouth_closed = 0.9
mouth_half_open = 1.4
mouth_open = 1.7
mouth_sound_time = 220

# Behaviour
user_gone_timeout = 13000

# Gsm
gsm_device = "/dev/ttyACM0"
gsm_phone1_default = 79999999999
gsm_phone2_default = 79999999999

# Music
music_file = "music_1.mp3"
music_volume = 40

# Speech repeat time
repeat_time_far = 15000
repeat_time_close = 15000
repeat_time_pay_more = 20000
repeat_time_music = 110*1000

# Magic
magic_duration = 36000

# Payment
payment_price_default = 100
payment_timeout = 3*60*1000
payment_afterpay_time = 60*1000

# Face detection
face_close_size = 60
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
breathing_pin = 24
breathing_min = 0.8
breathing_max = 2
breathing_time = 3000

# Led
led_payment_pin = 18
led_payment_period = 3000
led_lamp_pin = 12

# Money acceptor
money_device = "/dev/ttyAMA0"
money_capacity_default = 100
money_aware = 25

# Card_dispenser
card_dispenser_pin = 27
card_dispenser_capacity_default = 30
card_dispenser_aware = 10
