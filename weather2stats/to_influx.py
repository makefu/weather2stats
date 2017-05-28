#!/usr/bin/env python
""" usage: to-influx [options] [loop]

Options:
    --lol=LOL           set log level [Default: info]
    --server=HOST:PORT  set influx host and port
    --db=DB             influx Database
    --config=FILE       path to config file
"""
from weather2stats.common import load_plugins, set_lol, load_config
import logging
import json
from influxdb import InfluxDBClient

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
                    "value": val
                }
            }
            ret.append(e)
    return ret

def main():
    from docopt import docopt
    args = docopt(__doc__)
    set_lol(args['--lol'])
    if args['--config']:
        cfg = load_config(args['--config'])
    else:
        log.info("no configuration defined")
        cfg = {}
    plugs = load_plugins()
    all_data = []
    for plug in plugs:
        name = plug.__name__
        log.info("Running "+name)
        try:
            all_data.extend(plug.get_data(plug.ids,cfg))
            # all_data.extend(plug.get_mock_data())
        except Exception as e:
            log.error("Unable to complete {}, reason: {}".format(name,e))
    print(json.dumps(d2influx(all_data)))

if __name__ == "__main__":
    main()

