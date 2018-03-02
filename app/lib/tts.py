# -*- coding:utf8 -*-
from __future__ import unicode_literals

import os
import uuid

from gtts import gTTS

CURRENT_PATH = os.path.dirname(__file__)
AUDIO_PATH = os.path.join(CURRENT_PATH, '../static/audio')


def speech(text):
    audio_name = str(uuid.uuid4()) + '.mp3'
    tts = gTTS(text=text, lang='zh')

    tts.save(os.path.join(AUDIO_PATH, audio_name))

    return audio_name


if __name__ == '__main__':
    print(speech('您好，請問您需要什麼服務?'))
