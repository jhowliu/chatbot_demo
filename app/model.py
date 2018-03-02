# -*- coding=utf8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os.path
import time
import json
import requests
import random
import string

from lib.parser import parse_schedule_time
from lib.tts import speech

schedule_url = "http://122.146.85.107/abc/THRS/thsr.php"
url = "http://192.168.10.108:3124/new_dialogue_control"


def request_data(url, payload):
    reply = None

    while True:
        try:
            resp = requests.get(url, params=payload,
                                headers={'Connection': 'close'})
            reply = resp.text
            break
        except Exception as ex:
            print(ex)
            print("Connection Refused, wait for 5 seconds..")
            time.sleep(5)
            continue

    if resp.status_code == 500:
        print("ERROR OCCUR")
        print(resp.text)  # dictionary
        # 這裡應該Claude需要處理，而不是給我一個Internal Error
        reply = '{"dialogueReply":"對不起，我不明白您的意思。"}'
    else:
        reply = find_top_candidate(reply)

    audio_file_name = create_audio_file(reply)

    return reply, audio_file_name


def find_top_candidate(reply):
    reply = json.loads(reply)
    if 'type' in reply and reply['type'] == 'list':
        reply['dialogueReply'] = reply['dialogueReply'][0]

    return json.dumps(reply)


def create_audio_file(reply):
    audio_file_name = None
    reply = json.loads(reply)
    
    if 'dialogueReply' in reply:
        audio_file_name = speech(reply['dialogueReply'])

    return audio_file_name


def initial(session_id, app_id, id_no, user, service, date):
    payload = {
        'session': session_id,
        'appid': app_id,
        'IDNo': id_no,
        'PersonName': user,
        'ServiceType': service,
        'Date': date
    }

    resp_text, audio_file_name = request_data(url, payload=payload)

    return resp_text


# get dialogue result
def get_result_with_text(raw_text, session_id, app_id):
    payload = {
        'q': raw_text,
        'session': session_id,
        'appid': app_id,
    }

    resp_text, audio_file_name = request_data(url, payload=payload)

    return resp_text, audio_file_name


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def load_city_codes():
    city_code = None
    # relative path
    file_name = os.path.join(os.path.dirname(__file__),
                             'static/city_code.json')

    if os.path.isfile(file_name):
        with open(file_name) as f:
            city_code = json.load(f)

    return city_code


# loaded once
city_code = load_city_codes()


def get_schedule_with_data(data, session_id):
    json_data = json.loads(data)

    if city_code is None:
        return None

    departure_time = json_data['DepartureTime']
    departure_loc = json_data['DepartureLocation']
    arrival_loc = json_data['ArrivalLocation']

    if departure_loc not in city_code or arrival_loc not in city_code:
        return None

    departure_loc_code = city_code[departure_loc]
    arrival_loc_code = city_code[arrival_loc]

    payload = {
        'date': departure_time,
        'cityCode': departure_loc_code,
        'cityCode2': arrival_loc_code,
        'trainstation_name': departure_loc,
        'trainstation_name2': arrival_loc
    }

    print(payload)

    resp = requests.get(schedule_url, params=payload)

    obj = parse_schedule_time(resp.text)

    return json.loads(obj), resp.url
