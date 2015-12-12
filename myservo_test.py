import my_servo
pin = input('Enter pin')
a = my_servo.Servo(int(pin))
while True:
    val = input('Enter value')
    a.start(float(val))