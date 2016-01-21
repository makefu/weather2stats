#!/usr/bin/env python
import sys

def send_all_data(kvt,host='localhost',port=2003):
    import socket
    data=""
    for key,value,ts in kvt:
        data+="{} {} {}\n".format(key.replace(" ","_"),value,ts)
    print(data)
    #sys.exit()
    sock = socket.socket()
    sock.connect((host, port))
    sock.sendall(data.encode())
    sock.close()

def k2c(t):
    return t-273.15

with open ("historical_data.json") as f:
    import json
    kvt = []
    done = {}
    for line in f:
        d = json.loads(line)
        for l in d['list']:
            sensor = "weather.openweathermap.{}".format(l['name'])
            # middle of the hour
            ts = l['dt'] - 1800

            if not sensor in done:
                done[sensor] = []
            if ts in done[sensor]: continue

            for k,v in l['main'].items():
                if "temp" in k:
                    v = k2c(v)
                kvt.append([ sensor+"."+k,v,ts])
            done[sensor].append(ts)
        #import pdb;pdb.set_trace()
    send_all_data(kvt,"heidi.retiolum")
