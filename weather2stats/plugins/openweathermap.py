#!/usr/bin/env python
import sys
import json
import requests
import graphite
openweathermap_apikey = "***REMOVED***"

def k2c(t):
    """ kelvin to degree celsius """
    return float(t)-273.15


def get_openweathermap(ids):
    kvt = []
    d = requests.get('http://api.openweathermap.org/data/2.5/group?id={}&appid={}'.format(
        ",".join(map(str,ids)), openweathermap_apikey)).json()
    for l in d['list']:
        val = {
            "name": l['name'],
            "ts": l['dt'] - 1800,
            "_id": l['id']
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
    kvt = get_openweathermap([2825297,6930414,2867993,2927043])
    print(json.dumps(kvt))
    # graphite.send_all_data(kvt,host="heidi.shack")

if __name__ == "__main__":
    main()
