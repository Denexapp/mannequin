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

    def say(self, sound_id, v=1):
        if v == 1:
            self.thread = threading.Thread(target=self.__say_action,
                                       args=(speech_markup.sound_files[sound_id],
                                             speech_markup.sound_markup[sound_id]))
        elif v == 2:
            self.thread = threading.Thread(target=self.__say_action,
                                       args=(speech_markup.sound_files_2[sound_id],
                                             speech_markup.sound_markup_2[sound_id]))
        self.thread.daemon = True
        self.thread.start()
        print "Speech.say ended"

    def __phrase(self,sound_time_milisecons, angle):
        sound_time = float(sound_time_milisecons) / 1000
        start_time = time.time()
        middle_time = start_time + (sound_time/2)
        end_time = start_time + sound_time
        delta_t = middle_time - start_time
        delta_p = angle - dconfig.mouth_closed
        now = time.time()
        while now < middle_time:
            k = (now - start_time)/delta_t
            self.servo.start(dconfig.mouth_closed + delta_p*k)
            time.sleep(0.03)
            now = time.time()
            if self.stop:
                break
        while now < end_time:
            k = 1 - (now - middle_time)/delta_t
            self.servo.start(dconfig.mouth_closed + delta_p*k)
            time.sleep(0.03)
            now = time.time()
            if self.stop:
                break
        self.servo.start(dconfig.mouth_closed)

    def __say_action(self, sound_path, markup):
        self.stop = True
        while self.stopped is False:
            time.sleep(0.05)
        time.sleep(0.05)
        self.stop = False
        self.stopped = False
        sounds = markup.split(" ")
        self.player_play(sound_path, 100)
        for sound in sounds:
            if self.stop:
                break
            if sound.find("~") == -1:
                if sound == "1":
                    self.__phrase(dconfig.mouth_sound_time, dconfig.mouth_half_open)
                elif sound == "2":
                    self.__phrase(dconfig.mouth_sound_time, dconfig.mouth_open)
                else:
                    self.servo.start(0)
                    time.sleep(float(sound)/1000)
            else:
                sound_parts = sound.split("~")
                mouth_state = int(sound_parts[0])
                sound_time = float(sound_parts[1])
                if mouth_state == 1:
                    self.__phrase(sound_time, dconfig.mouth_half_open)
                elif mouth_state == 2:
                    self.__phrase(sound_time, dconfig.mouth_open)
                else:
                    pass
        self.servo.start(0)
        time.sleep(1)
        self.stop = False
        self.stopped = True
        print "Speech() in speech.py came to the end"

    def now_saying(self):
        return not self.stopped

    def sound_length(self, sound_id):
        length = 0.0
        markup = speech_markup.sound_markup[sound_id]
        sounds = markup.split(" ")
        for sound in sounds:
            if sound.find("~") == -1:
                if (sound == "1") or (sound == "2"):
                    length += dconfig.mouth_sound_time
                else:
                    length += int(sound)
            else:
                sound_parts = sound.split("~")
                length += float(sound_parts[1])
        print "length is", length
        return length

    def player_play(self, sound_path, volume):
        if self.player:
            self.player.terminate()
        self.player = subprocess.Popen(["mpg321", "-g "+str(volume), "sounds/"+sound_path])
