import pickle
import random
import time

import pyttsx3
speech_engine = pyttsx3.init('espeak')
# voice = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
# speech_engine.setProperty('voice',voice)
with open('words.pickle','rb') as pf:
    words = pickle.load(pf)

for _ in range(2):
    index = random.randrange(0, len(words))
    print('Trying to read {}'.format(words[index]))
    speech_engine.say('Click on the word: {}'.format(words[index]))
    speech_engine.runAndWait()

string = ''
for _ in range(5):
    string += '{} '.format(words[random.randrange(0, len(words))])

rate = speech_engine.getProperty('rate')
for _ in range(10):
    rate -= 20
    speech_engine.setProperty('rate', rate)
    print('Speaking at rate {}'.format(rate))
    speech_engine.say('The quick brown fox jumped over the lazy dog.')
    speech_engine.runAndWait()

voices = speech_engine.getProperty('voices')
for voice in voices:
    speech_engine.setProperty('voice',voice.id)
    speech_engine.say('Sally sold seashells by the seashore')
    print('Uttering {} with voice {}'.format(string,voice.id))
    speech_engine.runAndWait()

print(string)
speech_engine.say(string)
speech_engine.runAndWait()
