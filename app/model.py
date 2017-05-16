# -*- coding=utf8 -*-
import requests, json
import random, string

url = "http://192.168.10.108:3123/dialogue_control"

schedule_url = 'http://122.146.85.107/abc/THRS/thsr.php'

def get_result_with_text(raw_text, session_id):
    payload = {
        'q' : raw_text,
        'session': session_id
    }

    response = requests.get(url, params=payload)

    return response.text

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_schedule_with_result(result, session_id):

    departure_time = result['DepartureTime']
    departure_city = result['DepartureLocation']
    arrival_city = result['ArrivalLocation']
    departure_city_code = city_code[departure_city]
    arrival_city_code = city_code[arrival_city]

    payload = {
 	'date': departure_time
	'cityCode': departure_city_code
	'cityCode2': arrival_city_code
	'trainstation_name': departure_location
	'trainstation_name2':arrival_location

    }

    response = request.get(schedule_url, params=payload)

    return response.text

city_code = {'台北':'tp', '基隆':'kl', '新北':'nt', '桃園':'tu', '台中':'tc', '新竹':'hn' }
