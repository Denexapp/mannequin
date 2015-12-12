"""
by Denexapp

time should be in ms

"""

#Speech
mouth_pin = 23
mouth_closed = 2.5
mouth_half_open = 2.8
mouth_open = 3.1
mouth_sound_time = 220

#Speech repeat time
repeat_time_whisper = 15000
repeat_time_far = 15000
repeat_time_close = 15000
repeat_time_pay_more = 20000

#payment
payment_price = 100
payment_timeout = 5*60*1000
payment_afterpay_time = 60*1000

#Face detection
face_close_size = 42
face_min_size = 20
face_pattern = "haarcascade_frontalface_alt.xml"

#Hand
hand_pin = 10
#parameters below require to use hand.py instead of hand_2,py
hand_default = 1000
hand_min = 800
hand_max = 1200
hand_time = 3000
hand_direction = 1

#Breathing
breathing_pin = 15
breathing_min = 850
breathing_max = 1100
breathing_time = 3000

#Led payment
led_payment_pin = 18
led_payment_period = 3000

#Money acceptor
money_device = "/dev/ttyUSB0"

