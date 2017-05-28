#!/usr/bin/env python3

"""
    takes the list of parameters after index.php for stadtklima stuttgart
"""

import requests
from bs4 import BeautifulSoup
import datetime as dt
from pytz import timezone
import json
import logging as log

base_url = "http://www.stadtklima-stuttgart.de/index.php?"

ids = [ "luft_messdaten_station_smz",
        "luft_messdaten_station_gsg",
        "luft_messdaten_station_bd"
]

fields = {
    "Stickstoffmonoxid (NO):" : "NO",
    "Stickstoffdioxid (NO2):" : "NO2" ,
    "Ozon (O3):" : "O3",
    "Ozonpotential (O3 + NO2):" : "O3+NO2",
    "Feinstaub (PM10):":"PM10",
    "Feinstaub (PM2.5): (bisher ohne interaktiver Auswertung)" :"PM2_5",
    "Lufttemperatur:":"temperature",
    "Empfundene Temperatur in der Sonne:": "perceived_temp_sun",
    "Empfundene Temperatur im Schatten:": "perceived_temp_shadow",
    "Empfundene Temperatur mit Windchill-Effekt:*": "perceived_temp_chill",
    "Windgeschwindigkeit:":"wind_speed", # m/s
    "Windrichtung:":"wind_direction", # degree
    "Relative Luftfeuchte:":"humidity",
    "Absoluter Luftdruck: (in 250 m Messhöhe üNN)":"pressure_abs",
    "Absoluter Luftdruck: (in 220 m Messhöhe üNN)":"pressure_abs",
    "Relativer Luftdruck: (bisher ohne interaktiver Auswertung)":"pressure",
    "Niederschlag:" :"rain",
    "Globalstrahlung:":"uv_intensity",
    "Globalstrahlung: (bisher ohne interaktiver Auswertung)":"uv_intensity",
    "Strahlungsbilanz:":"radiation_balance",
    "UV-A Strahlung:":"UV-A",
    "UV-Index:":"uv_index",
    "UV-B Strahlung:":"UV-B"
    }

mapping = {
    "gsg" : "geschwister-scholl gymnasium",
    "smz" : "schwabenzentrum",
    "bd"  : "branddirektion"
    }


def get_data(ids,cfg=None):
    return [get_data_single(  ident) for ident in ids]

def get_data_single(ident):
    url = base_url + ident
    log.info("Fetching " + url)
    name = mapping[ident.split("_")[-1]]
    data = {
        "_name": name,
        "_source": "stadtklima-stuttgart",
        "_id": ident
    }
    ret = requests.get(url).text
    s = BeautifulSoup(ret,"html.parser")
    s.find(id="metstrPreview").decompose()
    for row in s.find_all("tr"):
        try:
            left = row.find(align="left").string
            right = row.find(align="right").string
            if left == "Windrichtung:":
                right = right.split(" ",1)[1]

            if left and left in fields:
                data[fields[left]] = float(right.strip().split(" ")[0])
            else:
                log.warn(left + " is not mapped")

        except Exception as e:
            pass

    for v in fields.values():
        if not v in data:
            log.debug(v + " is missing")

    def starts_with_stand(s):
        return s.string.startswith("(Stand")
    timestring = s.find("b",string=starts_with_stand).string\
            .replace("24:00 Uhr","00:00 Uhr") # fancy non-standard times
    if not timestring:
        raise LookupError("Unable to find timestamp in website")

    data["_ts"] = timezone("Europe/Berlin").localize(
            dt.datetime.strptime(timestring,
                "(Stand: %d.%m.%Y, %H:%M Uhr)")).isoformat()
    return data

def get_mock_data():
    """ Returns mocked data """
    return [
            {
                "humidity": 29,
                "temperature": 31,
                "NO2": 28.9,
                "pressure": 1016.6,
                "radiation_balance": 70.4,
                "O3+NO2": 70.5,
                "_ts": "2017-05-28T19:00:00+02:00",
                "_name": "schwabenzentrum",
                "perceived_temp_chill": 33.6,
                "NO": 1.1,
                "O3": 41.6,
                "perceived_temp_sun": 30.4,
                "pressure_abs": 985.3,
                "_source": "stadtklima-stuttgart",
                "UV-B": 0.34,
                "_id": "luft_messdaten_station_smz",
                "rain": 0,
                "UV-A": 15.42,
                "uv_intensity": 242.1,
                "perceived_temp_shadow": 26.3,
                "wind_speed": 1.4,
                "wind_direction": 21.7
                },
            {
                "_id": "luft_messdaten_station_gsg",
                "humidity": 23.4,
                "wind_speed": 1.3,
                "_name": "geschwister-scholl gymnasium",
                "_source": "stadtklima-stuttgart",
                "temperature": 32.7,
                "wind_direction": 30.9,
                "_ts": "2017-05-28T19:00:00+02:00"
                },
            {
                "_id": "luft_messdaten_station_bd",
                "pressure_abs": 989,
                "humidity": 29.7,
                "uv_intensity": 445.6,
                "wind_speed": 2.5,
                "_name": "branddirektion",
                "pressure": 1016.5,
                "_source": "stadtklima-stuttgart",
                "temperature": 31.1,
                "wind_direction": 15.1,
                "_ts": "2017-05-28T19:00:00+02:00"
                }
            ]


def main():
    print(json.dumps(get_data(ids)))

if __name__ == "__main__":
    main()
