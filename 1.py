import voicerss_tts
from mutagen.mp3 import MP3
import os

voice = voicerss_tts.speech({
    'key': '13abe1d0ea004089a03ba6455189f773',
    'hl': 'en-us',
    'v': 'John',
    'src': 'hello how are you today say, Are you doing well, fuck me fuck me please fuck me in the asshole',
    'r': '0',
    'c': 'mp3',
    'f': '44khz_16bit_stereo',
    'ssml': 'false',
    'b64': 'false'
})
f = open(os.getcwd() + "//mp3//file.mp3", "wb")
f.write(voice['response'])
f.flush()
f.close()
print(round(MP3("C://Users//Richard//Documents//VSCODE//Python//Fivver//vidGeneration//file.mp3").info.length, 2))
