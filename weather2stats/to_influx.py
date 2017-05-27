#!/usr/bin/env python
""" usage: to-influx [options] [loop]

Options:
    --lol=LOL           set log level [Default: info]
    --server=HOST:PORT  set influx host and port
"""

from weather2stats.common import load_plugins,set_lol
import logging
import json
log = logging.getLogger("to-influx")

def main():
    from docopt import docopt
    args = docopt(__doc__)
    set_lol(args['--lol'])
    plugs = load_plugins()
    all_data = []
    for plug in plugs:
        log.info("Running "+plug.__name__)
        all_data.extend(plug.get_data(plug.ids))
    print(json.dumps(all_data))

if __name__ == "__main__":
    main()

