"""
by Denexapp

"""

import denexapp_config as dconfig
import threading
import time
import math
from RPIO import PWM

class hand():
    servo = PWM.Servo()
    stop = False
    range = dconfig.hand_max - dconfig.hand_min
    counter = (dconfig.hand_default - dconfig.hand_max)/range*math.pi
    direction = dconfig.hand_direction
    position = dconfig.hand_default
    delta = 2*math.pi/dconfig.hand_time*30

    def __init__(self):
        #turn to default position
        self.servo.set_servo(dconfig.hand_pin, round((dconfig.hand_default)/10)*10)
        print "Init hand started"

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
        print "Start move action started"
        while True:
            self.counter += self.delta*self.direction
            if self.direction == -1:
                if self.counter + self.delta*self.direction < -math.pi:
                    self.direction = 1
            elif self.direction == 1:
                if self.counter + self.delta*self.direction > 0:
                    self.direction = -1
            self.position = (math.cos(self.counter)*0.5+0.5)*self.range+dconfig.hand_min
            self.servo.set_servo(dconfig.hand_pin, round((self.position)/10)*10)
            time.sleep(0.03)
            if self.stop:
                print "Start move action stopped"
                break

    def __stop_move_action(self):
        self.stop = True
        print "Stop move action started"
        if self.position < dconfig.hand_default:
            self.direction = 1
            while (math.cos(self.counter+self.delta*self.direction)*0.5+0.5)*self.range+dconfig.hand_min < dconfig.hand_default:
                self.counter += self.delta*self.direction
                self.position = (math.cos(self.counter)*0.5+0.5)*self.range+dconfig.hand_min
                self.servo.set_servo(dconfig.hand_pin, round(self.position/10)*10)
                time.sleep(0.03)
                if self.stop == False:
                    break
            print "Stop move action stoped"
        elif self.position > dconfig.hand_default:
            self.direction = -1
            while (math.cos(self.counter+self.delta*self.direction)*0.5+0.5)*self.range+dconfig.hand_min > dconfig.hand_default:
                self.counter+=self.delta*self.direction
                self.position = (math.cos(self.counter)*0.5+0.5)*self.range+dconfig.hand_min
                self.servo.set_servo(dconfig.hand_pin, round((self.position)/10)*10)
                time.sleep(0.03)
                if self.stop == False:
                    break
            print "Stop move action stoped"



