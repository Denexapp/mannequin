import my_servo

a = my_servo.Servo(24)
while True:
    a.start(20)