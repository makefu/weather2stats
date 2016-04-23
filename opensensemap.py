#!/usr/bin/env python3
import datetime as dt
import requests
import sys,json
import graphite

api_end= "http://opensensemap.org:8000/"
host="heidi.retiolum"
box= "56a0de932cb6e1e41040a68b" #shackspace
mapping = { "UV-Intensität": "global_radiation",
            "Temperatur": "temperature",
            "rel. Luftfeuchte": "humidity",
            "Luftdruck": "pressure",
            "Beleuchtungsstärke": "brightness" }

to = dt.datetime.now().isoformat()
sense_params = { "from-date":"", "to-date": to, "format":"JSON" }

data = []
base_key = "weather.sensebox.shackspace."
for sense in requests.get(api_end+"/boxes/"+box).json()['sensors']:
    name = sense['title']
    if name in mapping:
        ret = requests.get("{}/boxes/{}/data/{}".format(api_end,box,sense['_id']),
                params=sense_params).json()
        for kv in ret:
            ts = int(dt.datetime.strptime(kv['createdAt']+"+0000","%Y-%m-%dT%H:%M:%S.%fZ%z").timestamp())
            data.append([base_key+mapping[name],float(kv['value']),ts])

graphite.send_all_data(data,host=host)
