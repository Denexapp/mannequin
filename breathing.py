"""
by Denexapp

"""

import denexapp_config as dconfig
import threading
import time
import math
from RPIO import PWM

class breathing():
    servo = PWM.Servo()
    stop = False
    range = dconfig.breathing_max - dconfig.breathing_min
    counter = (dconfig.breathing_min - dconfig.breathing_max)/range*math.pi
    direction = math.copysign(1,dconfig.breathing_max-dconfig.breathing_min)
    position = dconfig.breathing_min
    delta = 2*math.pi/dconfig.breathing_time*30

    def __init__(self):
        #turn to default position
        self.servo.set_servo(dconfig.breathing_pin, round((dconfig.breathing_min)/10)*10)
        print "Init breath started"

    def start_move(self):
        thread = threading.Thread(target=self.__start_move_action)
        thread.daemon = True
        thread.start()

    def stop_move(self):
        thread = threading.Thread(target=self.__stop_move_action)
        thread.daemon = True
        thread.start()

    def __start_move_action(self):
        self.stop=False
        print "Start breathing action started"
        while True:
            self.counter += self.delta*self.direction
            if self.direction == -1:
                if self.counter + self.delta*self.direction < -math.pi:
                    self.direction = 1
            elif self.direction == 1:
                if self.counter + self.delta*self.direction > 0:
                    self.direction = -1
            self.position = (math.cos(self.counter)*0.5+0.5)*self.range+dconfig.breathing_min
            self.servo.set_servo(dconfig.breathing_pin, round((self.position)/10)*10)
            time.sleep(0.03)
        """direct = 1
        val = 1000
        while True:
            if val + direct*10 > 1300:
                direct = -1
            if val + direct*10 < 1000:
                direct = 1
            val = val + 10 * direct
            self.servo.set_servo(dconfig.breathing_pin,val)
            time.sleep(0.2)
            if self.stop:
                print "Start breathing action stopped"
                break"""

    def __stop_move_action(self):
        self.stop = True
        print "Stop breathing action started"
        self.direction = -1
        while (math.cos(self.counter+self.delta*self.direction)*0.5+0.5)*self.range+dconfig.breathing_min > dconfig.breathing_min:
            self.counter+=self.delta*self.direction
            self.position = (math.cos(self.counter)*0.5+0.5)*self.range+dconfig.breathing_min
            self.servo.set_servo(dconfig.breathing_pin, round((self.position)/10)*10)
            time.sleep(0.03)
            if self.stop == False:
                break
        print "Stop breathing action stoped"