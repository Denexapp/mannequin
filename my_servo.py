import RPi.GPIO as GPIO

class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        self.pin = pin
        self.freq = 20

        self.pwm = GPIO.PWM(pin, self.freq)

    def start(self, duty_cycle):
        self.pwm.start(duty_cycle)

    def update(self, duty):
        self.duty_cycle = duty

    def stop(self):
        self.pwm.stop()
