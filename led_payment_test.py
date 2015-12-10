import led_payment
import time

led_payment_object = led_payment.led_payment()
led_payment_object.start_blink()
while True:
    time.sleep(10)