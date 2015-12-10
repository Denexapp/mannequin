import speech
import time

if __name__ == '__main__':
    speech_object = speech.speech()
    speech_object.say("come_to_me.mp3", "2000 1 1 2 300 2 2 800 2 300 1~300 1~500 1~250 1~300 300 2~500")
    time.sleep(10)
    speech_object.say("come_to_me.mp3", "2000 1 1 2 300 2 2 800 2 300 1~300 1~500 1~250 1~300 300 2~500")
    time.sleep(10)
    speech_object.say("come_to_me.mp3", "2000 1 1 2 300 2 2 800 2 300 1~300 1~500 1~250 1~300 300 2~500")
    time.sleep(10)
    while True:
        time.sleep(1)