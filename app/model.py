# -*- coding=utf8 -*-
import os.path
import requests, json
import random, string

schedule_url = "http://122.146.85.107/abc/THRS/thsr.php"
url = "http://192.168.10.108:3123/dialogue_control"

def get_result_with_text(raw_text, session_id):
    payload = {
        'q' : raw_text,
        'session': session_id
    }

    response = requests.get(url, params=payload)

    return response.text

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def load_city_codes():
    city_code = None
    # relative path
    file_name = os.path.join(os.path.dirname(__file__), 'static/city_code.json')

    if os.path.isfile(file_name):
        with open(file_name) as f: 
            city_code = json.load(f)

    return city_code

# loaded once
city_code = load_city_codes()

def get_schedule_with_data(data, session_id):
    json_data = json.loads(data)
    
    if city_code is None: return None

    print city_code

    departure_time = json_data['DepartureTime']
    departure_loc = json_data['DepartureLocation']
    arrival_loc= json_data['ArrivalLocation']
    departure_loc_code = city_code[departure_loc]
    arrival_loc_code = city_code[arrival_loc]

    payload = {
        'date': departure_time,
        'cityCode': departure_loc_code,
        'cityCode2': arrival_loc_code,
        'trainstation_name': departure_loc,
        'trainstation_name2':arrival_loc
    }

    print payload

    response = requests.get(schedule_url, params=payload)


    return response.url

