"""
by Denexapp

"""

import subprocess
import time
import threading
import denexapp_config as dconfig
import speech_markup
from my_servo import Servo

class speech():

    def __init__(self):
        # turn to default position
        self.servo = Servo(dconfig.mouth_pin)
        self.servo.start(0)
        self.stop = False
        self.stopped = True
        print "Speech.init ended"
        self.player = False

    def say(self, sound_id):
        self.thread = threading.Thread(target=self.__say_action,
                                       args=(speech_markup.sound_files[sound_id],))
        self.thread.daemon = True
        self.thread.start()
        print "Speech.say ended"

    def say_auto(self, scenario, situation, sound_id):
        self.thread = threading.Thread(target=self.__say_action,
                                       args=("Scenarios/" + str(scenario) + "/"
                                             + str(situation)
                                             + "/" + str((sound_id + 1)) + ".wav",))
        self.thread.daemon = True
        self.thread.start()
        print "Speech.say_auto ended"

    def __say_action(self, sound_path):
        self.stop = True
        while self.stopped is False:
            time.sleep(0.05)
        time.sleep(0.05)
        self.stop = False
        self.stopped = False
        f = open("sounds/" + sound_path + "_markup")
        sounds = []
        i = 0
        for element in f.readline().split(" "):
            sounds.insert(i, float(element))
            i += 1
        f.close()
        self.player_play(sound_path, 100)
        i = 0
        for sound in sounds:
            i += 1
            if self.stop:
                break
            if sound <= 50:
                self.servo.start(0)
            elif sound >= dconfig.mouth_recognition_max:
                self.servo.start(dconfig.mouth_open)
                print "maximum"
            else:
                delta = sound/dconfig.mouth_recognition_max/\
                        float(dconfig.mouth_open - dconfig.mouth_closed)
                self.servo.start(dconfig.mouth_closed + delta)
                print dconfig.mouth_closed + delta
            time.sleep(0.01)
        print i
        self.servo.start(0)
        time.sleep(1)
        self.stop = False
        self.stopped = True
        print "Speech() in speech.py came to the end"

    def now_saying(self):
        return not self.stopped

    def player_play(self, sound_path, volume):
        if self.player:
            self.player.terminate()
        self.player = subprocess.Popen(["mpg321", "-g "+str(volume), "sounds/"+sound_path])
