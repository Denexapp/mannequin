"""
by Denexapp

"""

from RPIO import PWM

servo = PWM.Servo()

pin = input('Enter pin')
pin = int(pin)

while True:
    val = input('Enter value')
    val = int(val)
    servo.set_servo(pin, val)
