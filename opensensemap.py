#!/usr/bin/env python3
import datetime as dt
import requests
import sys,json
import graphite

api_end= "http://opensensemap.org:8000/"
host="heidi.retiolum"
box= "56a0de932cb6e1e41040a68b" #shackspace
timespan = 3600 * 1000 # time into past (millisecs)
mapping = { "UV-Intensität": "global_radiation",
            "Temperatur": "temperature",
            "rel. Luftfeuchte": "humidity",
            "Luftdruck": "pressure",
            "Beleuchtungsstärke": "brightness" }

# we will always grab a full hour starting from 30 minutes ago
# this assumes that the script will run every 30 minutes
end = int(dt.datetime.now().timestamp() - 3600 )*1000
sense_params = { "from-date":end,
               "format":"JSON" }
data = []
base_key = "weather.sensebox.shackspace."
for sense in requests.get(api_end+"/boxes/"+box).json()['sensors']:
    name = sense['title']
    if name in mapping:
        ret = requests.get("{}/boxes/{}/data/{}".format(api_end,box,sense['_id']),
                params=sense_params).json()
        for kv in ret:
            ts = int(dt.datetime.strptime(kv['createdAt'],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
            data.append([base_key+mapping[name],float(kv['value']),ts])

graphite.send_all_data(data,host=host)
