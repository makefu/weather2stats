#!/usr/bin/env python
""" usage: to-influx [options] [loop TIMEOUT]

Options:
    --lol=LOL           set log level [Default: info]
    --server=HOST:PORT  set influx host and port [Default: localhost:8086]
    --db=DB             influx Database [Default: weather]
    --config=FILE       path to config file
"""
from weather2stats.common import load_plugins, set_lol, load_config
import logging
import json
import time
from influxdb import InfluxDBClient

from docopt import docopt
from functools import partial
from threading import Timer

log = logging.getLogger("to-influx")

def d2influx(data):
    """ transforms internal data (list of kv ) to influx data
    [
        {
            "_id": "<unique identity>",
            "_name": "<name of data source based on id>",
            "_source": "<source name>",
            "_ts": "<timestamp of the input values in rfc3339>",

            "field1": <value1 (float)>,
            ... ,
            "fieldX": <valueX (float)>
        }
    ]
    [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
    ]
    """
    ret = []
    for d in data:
        _id = str(d.pop("_id"))
        _name = d.pop("_name")
        _source = d.pop("_source")
        _ts = d.pop("_ts")
        for measurement,val in d.items():
            e = {
                "measurement": measurement,
                "tags": {
                    "source": _source,
                    "id": _id,
                    "name": _name
                },
                "time": _ts,
                "fields": {
                    "value": float(val)
                }
            }
            ret.append(e)
    return ret

def run_plugs(cfg):
    all_data = []
    plugs = load_plugins() # TODO: not every time?
    for plug in plugs:
        name = plug.__name__
        log.info("Running "+name)
        try:
            all_data.extend(plug.get_data(plug.ids,cfg))
            # all_data.extend(plug.get_mock_data())
        except Exception as e:
            log.error("Unable to complete {}, reason: {}".format(name,e))
    return all_data

def send_data(client,cfg):
    log.info("Beginning to retrieve data" )
    payload = d2influx(run_plugs(cfg))
    log.debug(payload)
    log.info("Writing {} points to influx".format(len(payload)))
    client.write_points(payload)

def main():

    args = docopt(__doc__)
    set_lol(args['--lol'])
    db = args['--db']
    do_loop = args['loop']
    timeout = float(args['TIMEOUT'] or 60)
    host,port = args['--server'].split(":")
    if args['--config']:
        cfg = load_config(args['--config'])
    else:
        log.info("no configuration defined")
        cfg = {}

    client = InfluxDBClient(host, int(port), database=db)
    if not db in [ c['name'] for c in client.get_list_database() ]:
        log.warn("Creating database "+db)
        client.create_database(db)

    while True:
        begin = time.clock()
        send_data(client,cfg)
        end = (time.clock() - begin)
        delta = timeout - end
        log.info("Sending data took {} seconds".format(end,delta))

        if not do_loop:
            log.debug("Not looping")
            break
        if delta > 0:
            log.info("Sleeping for {} more secs".format(delta))
            time.sleep(delta)
        else:
            log.warning("We are already {} seconds late, execution took {} seconds!starting right now".format(-delta,end))


if __name__ == "__main__":
    main()

