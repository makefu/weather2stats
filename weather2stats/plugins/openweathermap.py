#!/usr/bin/env python
"""
    takes a list of openweathermap ids and a config dict with
    'openweathermap_apikey'
"""
from datetime import datetime as dt
from pytz import timezone
import sys
import json
import requests

ids = [2825297,6930414,2867993,2927043]

def k2c(t):
    """ kelvin to degree celsius """
    return float(t)-273.15


def get_data(ids,cfg):
    if not "openweathermap_apikey" in cfg:
        raise ValueError("No apikey defined for openweathermap")
    kvt = []
    d = requests.get('http://api.openweathermap.org/data/2.5/group?id={}&appid={}'.format(
        ",".join(map(str,ids)), cfg['openweathermap_apikey'])).json()
    for l in d['list']:
        val = {
            "_id": l['id'],
            "_name": l['name'],
            "_source": "openweathermap",
            # TODO: dt returned is always localtime
            #       need to translate coords to timezone
            "_ts": timezone("Europe/Berlin").localize(
                dt.fromtimestamp(l['dt'] - 1800)).isoformat()
        }

        for k,v in l['main'].items():
            if "temp" in k:
                k = k.replace("temp","temperature")
                v = k2c(v)
            val[k] = v
        # 'wind': {'speed': 2.6, 'deg': 340}
        for k,v in l['wind'].items():
            val["wind_"+k] = v
        kvt.append(val)
    return kvt



def main():
    kvt = get_data(ids, { "openweathermap_apikey": "lol" })
    print(json.dumps(kvt))

def get_mock_data():
    return [
            {
                "_id": 2825297,
                "_ts": "2017-05-28T19:00:15Z",
                "temperature_max": 29,
                "wind_speed": 2.1,
                "_name": "Stuttgart",
                "temperature_min": 28,
                "_source": "openweathermap",
                "temperature": 28.360000000000014,
                "pressure": 1017,
                "humidity": 35,
                "wind_deg": 50
                },
            {
                "_id": 6930414,
                "_ts": "2017-05-28T19:00:15Z",
                "temperature_max": 29,
                "wind_speed": 2.1,
                "_name": "Stuttgart-Ost",
                "temperature_min": 28,
                "_source": "openweathermap",
                "temperature": 28.360000000000014,
                "pressure": 1017,
                "humidity": 35,
                "wind_deg": 50
                },
            {
                "_id": 2867993,
                "_ts": "2017-05-28T19:00:15Z",
                "temperature_max": 29,
                "wind_speed": 2.1,
                "_name": "Stuttgart Muehlhausen",
                "temperature_min": 28,
                "_source": "openweathermap",
                "temperature": 28.379999999999995,
                "pressure": 1017,
                "humidity": 35,
                "wind_deg": 50
                },
            {
                "_id": 2927043,
                "_ts": "2017-05-28T19:00:15Z",
                "temperature_max": 29,
                "wind_speed": 2.1,
                "_name": "Stuttgart Feuerbach",
                "temperature_min": 28,
                "_source": "openweathermap",
                "temperature": 28.360000000000014,
                "pressure": 1017,
                "humidity": 35,
                "wind_deg": 50
                }
            ]

if __name__ == "__main__":
    main()
