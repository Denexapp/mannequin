import speech
import speech_markup

if __name__ == '__main__':
    speech_object = speech.speech()
    while True:
        val = int(input('Enter value'))
        speech_object.say(speech_markup.sound_files[val],speech_markup.sound_markup[val])