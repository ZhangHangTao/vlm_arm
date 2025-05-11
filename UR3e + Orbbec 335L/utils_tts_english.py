import os
import requests
import pyaudio
import wave

def tts(TEXT='我是TAI麒麟臂', tts_wav_path='temp/tts.wav'):
    res = requests.post('http://192.168.1.101:8888/tts', data={
        "text": TEXT,
        "prompt": "[oral_2][laugh_0][break_6]",
        "voice": "3333",
        "temperature": 0.3,
        "top_p": 0.7,
        "top_k": 20,
        "skip_refine": 0,
        "custom_voice": 0
    })
    audio_url = res.json()['audio_files'][0]['url']
    audio_data = requests.get(audio_url).content
    with open(tts_wav_path, 'wb') as f:
        f.write(audio_data)


def play_wav(wav_file='asset/welcome.wav'):
    '''
    播放wav音频文件
    '''
    prompt = 'aplay -t wav {} -q'.format(wav_file)
    os.system(prompt)

