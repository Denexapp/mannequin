from serial import Serial
import RPi.GPIO as GPIO
from time import sleep

pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
sleep(5)
GPIO.output(pin, 1)
sleep(1)
GPIO.output(pin, 0)
sleep(1)
GPIO.output(pin, 1)
