import led
import time
pin = int(input('Enter pin'))
period = int(input('Enter period'))
led_object = led.led(pin, period)
led_object.start_blink()
while True:
    time.sleep(3)
