"""
by Denexapp

Markup file example:
1 2 43 2~300
where
1 - half-open for default time
2 - open for default time
43 - closed for 43 ms
2~300 - open for 300 ms

"""

import subprocess
import time
import threading
from RPi.GPIO import PWM
import denexapp_config as dconfig
from my_servo import Servo

class speech():
    servo = Servo(dconfig.mouth_pin)
    stop = False
    stopped = True

    def __init__(self):
        #turn to default position
        self.servo.start(dconfig.mouth_closed)
        print "Speech.init ended"
        self.player = False


    def say(self,sound_path, markup):
        self.thread = threading.Thread(target=self.__say_action, args=(sound_path,markup))
        self.thread.daemon = True
        self.thread.start()
        print "Speech.say ended"

    def __phrase(self,sound_time_milisecons, angle):
        print("Phrase to angle ", angle, " with time ", sound_time_milisecons, " started.")
        sound_time = float(sound_time_milisecons) / 1000
        start_time = time.time()
        middle_time = start_time + (sound_time/2)
        end_time = start_time + sound_time
        delta_t = middle_time - start_time
        delta_p = angle - dconfig.mouth_closed
        now = time.time()
        while now < middle_time:
            k = (now - start_time)/delta_t
            print("Setting this to servo ", round((dconfig.mouth_closed + delta_p*k)/10)*10)
            self.servo.start(dconfig.mouth_closed)
            time.sleep(0.03)
            now = time.time()
            if self.stop:
                break
        while now < end_time:
            k = 1 - (now - middle_time)/delta_t
            print("Setting this to servo ", round((dconfig.mouth_closed + delta_p*k)/10)*10)
            self.servo.start(dconfig.mouth_closed)
            time.sleep(0.03)
            now = time.time()
            if self.stop:
                break
        print("Setting this to servo ", dconfig.mouth_closed)
        self.servo.start(dconfig.mouth_closed)

    def __say_action(self,sound_path, markup):
        if self.player:
            self.player.terminate()
        self.stop = True
        while self.stopped is False:
            time.sleep(0.05)
        time.sleep(0.05)
        self.stop = False
        self.stopped = False
        sounds = markup.split(" ")
        self.player = subprocess.Popen(["mpg321",sound_path])
        for sound in sounds:
            if self.stop:
                break
            if sound.find("~") == -1:
                if sound == "1":
                    self.__phrase(dconfig.mouth_sound_time,dconfig.mouth_half_open)
                elif sound == "2":
                    self.__phrase(dconfig.mouth_sound_time,dconfig.mouth_open)
                else:
                    time.sleep(int(sound)/1000)
            else:
                sound_parts = sound.split("~")
                mouth_state = int(sound_parts[0])
                sound_time = int(sound_parts[1])
                #print("Sound_time is ", sound_time)
                if mouth_state == 1:
                    self.__phrase(sound_time,dconfig.mouth_half_open)
                elif mouth_state == 2:
                    self.__phrase(sound_time,dconfig.mouth_open)
                else:
                    pass
        self.stop = False
        self.stopped = True
        print("Speech() in speech.py came to the end")