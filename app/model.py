import requests, json
import random, string

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
