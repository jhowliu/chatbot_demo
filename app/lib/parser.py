import json
import requests

from bs4 import BeautifulSoup

def parse_schedule_time(html):
    obj = []
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.select('tr')[2:]

    for ix, row in enumerate(rows):
        if ix % 2 == 1:
            continue

        cols = row.select('td')[:4]

        obj.append(
                {
                    "start": cols[1].text,
                    "arrival": cols[3].text
                }
        )

    return json.dumps(obj)

