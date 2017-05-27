#!/usr/bin/env python3
import datetime as dt
import requests
import sys,json
import graphite

api_end= "https://api.opensensemap.org/"
box= "56a0de932cb6e1e41040a68b" #shackspace
mapping = { "UV-Intensität": "uv_intensity",
            "Temperatur": "temperature",
            "rel. Luftfeuchte": "humidity",
            "Luftdruck": "pressure",
            "Beleuchtungsstärke": "brightness" }

to = dt.datetime.now().isoformat()
sense_params = {
    # "from-date": "2016-05-12T21:11:12.621978",
    # "to-date": "2016-06-12T21:11:12.621978", 
    "to-date": to,
    "from-date": "",
    "format":"JSON"
}

data = []


def get_sensemap(boxid):
    info = requests.get(api_end+"/boxes/"+boxid).json()
    val = {
        "_id": boxid,
        "name": info['name'],
        # TODO: createdAt may be different for different sensors, we take the
        # latest val
        "ts": int(dt.datetime.strptime(info['updatedAt']+"+0000","%Y-%m-%dT%H:%M:%S.%fZ%z").timestamp())
    }
    # TODO: original code used /boxes/boxid/data/sensorid to fetch all previous points
    # ts = int(dt.datetime.strptime(kv['createdAt']+"+0000","%Y-%m-%dT%H:%M:%S.%fZ%z").timestamp())
    for sense in info['sensors']:
        name = sense['title']
        kv = sense['lastMeasurement']
        if name in mapping:
            val[mapping[name]] = float(kv['value'])
    return val

def boxmain(boxid):
    """ Returns a list of sensors
    boxid may be a single string or a list, return value ist always a list of
    dicts
    """
    if type(boxid) == str:
        return [get_sensemap(boxid)]
    elif type(boxid) == list:
        return [ get_sensemap(b) for b in boxid ]

def main():
    print(json.dumps(boxmain(box)))

if __name__ == "__main__":
    main()
    # graphite.send_all_data(data,host=host)