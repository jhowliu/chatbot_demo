import requests
import json

url = "http://192.168.10.108:3123/dialogue_control"

def get_result_with_text(raw_text, session_id):
    payload = {
        'q' : raw_text,
        'session': session_id
    }

    response = requests.get(url, params=payload)

    return response.text