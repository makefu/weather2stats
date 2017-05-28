
import logging

def set_lol(lol,logger=None):
  numeric_level = getattr(logging,lol.upper(),None)
  if not isinstance(numeric_level,int):
    raise AttributeError('No such log level {}'.format(lol))
  logging.basicConfig(level=numeric_level)

# https://copyninja.info/blog/dynamic-module-loading.html
import os
import sys
import re
import importlib

def load_plugins():
    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                           os.listdir(os.path.join(os.path.dirname(__file__),
                                                 'plugins')))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, pluginfiles)
    # import parent module / namespace
    importlib.import_module('weather2stats.plugins')
    modules = []
    for plugin in plugins:
             if not plugin.endswith("__init__"):
                 modules.append(importlib.import_module(plugin,
                     package="weather2stats.plugins"))

    return modules

import json
def load_config(f):
    with open(f) as fil:
        return json.load(fil)
