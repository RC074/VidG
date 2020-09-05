from moviepy.editor import *
import voicerss_tts
import os

import config # config file

pF = os.path.abspath(__file__)[0:len(os.path.abspath(__file__)) - len(os.path.basename(__file__))]

def textToMp3(text, num, speaker):

    voice = voicerss_tts.speech({
        'key': config.api,
        'hl': 'en-us',
        'v': config.speakers["speaker"],
        'src': text,
        'r': '0',
        'c': 'mp3',
        'f': '44khz_16bit_stereo',
        'ssml': 'false',
        'b64': 'false'
    })

    mp3Folder = pF + "mp3"
    mp3File = open(mp3Folder + f"\{num}.mp3", "wb")
    mp3File.write(voice['response'])
    mp3File.flush()
    mp3File.close()
    return round(AudioFileClip(mp3Folder + f"\{num}.mp3").duration, 2)

def mp4MatchToAudio(mp4Path, mp3Duration, text, num):
    cnt = 0
    formattedText = ""
    for char in text:
        if cnt < config.text['lineChars']:
            formattedText += char
            cnt += 1
        else:
            formattedText += "\n" + char
            cnt = 0
    mp4Clip = VideoFileClip(mp4Path)
    mp4Duration = round(mp4Clip.duration, 2)

    mp4Text = TextClip(
        formattedText, 
        color=config.text['color'], 
        align='West', 
        fontsize=config.text["size"], 
        font=config.text['font'], 
        method='label'
    ).set_position(config.text['pos'], relative=True)

    if mp4Duration < mp3Duration:
        cuts = [mp4Clip] * round(mp3Duration // mp4Duration)
        shortClipLength = round(mp3Duration % mp4Duration, 2)
        cuts.append(mp4Clip.subclip(0, shortClipLength))
        mergedClip = concatenate_videoclips(cuts)
        mergedClip = CompositeVideoClip([mergedClip, mp4Text]).set_duration(mp3Duration)
        return mergedClip
    else:
        return CompositeVideoClip([mp4Clip.subclip(0, mp3Duration), mp4Text]).set_duration(mp3Duration)

def main():
    videoToMerge = []
    audioToMerge = []
    pF = os.path.abspath(__file__)[0:len(os.path.abspath(__file__)) - len(os.path.basename(__file__))]
    inputScript = open(os.path.abspath(__file__)[0:len(os.path.abspath(__file__)) - len(os.path.basename(__file__))] + "script.txt", "r")
    for i, line in enumerate(inputScript.readlines()):
        actor = line[7:12]
        voice = line[20:23]
        text = line[26:]
        mp3Duration = textToMp3(text, i+1, voice)
        mp3ToMerge = AudioFileClip(pF + f"mp3\{i+1}.mp3")
        mp4ToProcess = ""
        for mp4File in os.listdir(pF + "mp4"):
            print(actor.upper(), mp4File.upper())
            if actor.upper() in mp4File.upper():
                mp4ToProcess = pF + f"mp4\{mp4File}"
                break
        print(mp4ToProcess)
        videoToMerge.append(mp4MatchToAudio(mp4ToProcess, mp3Duration, text, i+1))
        audioToMerge.append(mp3ToMerge)

    mergedMp4 = concatenate_videoclips(videoToMerge)
    mergedMp3 = concatenate_audioclips(audioToMerge)
    mergedMp3.write_audiofile(pF + "mp3\merge.mp3")
    mergedMp4.write_videofile(pF + "mp4Final\merge.mp4", audio=pF + "mp3\merge.mp3")

if __name__ == '__main__':
    main()
