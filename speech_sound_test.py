import speech
import time
import denexapp_config as dconfig

if __name__ == '__main__':
    speech_object = speech.speech()
    val = 9
    ask_val = True
    if ask_val:
        while True:
                val = int(input('Enter value'))
                speech_object.say(val)
    else:
        speech_object.say(val)
        time.sleep(0.5)
        while speech_object.now_saying():
            time.sleep(0.2)