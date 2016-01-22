#!/usr/bin/env python
import sys
import requests,json
import graphite
openweathermap_apikey = ""
host = "heidi.retiolum"
def k2c(t):
    """ kelvin to degree celsius """
    return t-273.15

kvt = []
d = requests.get('http://api.openweathermap.org/data/2.5/group?id=2825297,6930414,2867993,2927043&appid={}'.format(openweathermap_apikey)).json()
for l in d['list']:
    sensor = "weather.openweathermap." + l['name']
    # middle of the hour
    ts = l['dt'] - 1800

    for k,v in l['main'].items():
        if "temp" in k:
            k = k.replace("temp","temperature")
            v = k2c(v)
        kvt.append([ sensor+"."+k,v,ts])

graphite.send_all_data(kvt,host=host)
