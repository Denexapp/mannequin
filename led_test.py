import led
import time
pin = int(input('Enter pin'))
period = int(input('Enter period'))
led_object = led.led(pin, period)

while True:
    led_object.start_blink()
    time.sleep(5)
    led_object.stop_blink()
    time.sleep(5)
