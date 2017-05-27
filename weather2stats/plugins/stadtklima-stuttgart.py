#!/usr/bin/env python3

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


def get_data(ids):
    return [get_data_single(  ident) for ident in ids]

def get_data_single(ident):
    url = base_url + ident
    log.warn("Fetching " + url)
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
            log.warn(v + " is missing")

    def starts_with_stand(s):
        return s.string.startswith("(Stand")
    timestring = s.find("b",string=starts_with_stand).string\
            .replace("24:00 Uhr","00:00 Uhr") # fancy non-standard times
    if not timestring:
        raise LookupError("Unable to find timestamp in website")

    data["_ts"] = int(timezone("Europe/Berlin").localize(
            dt.datetime.strptime(timestring,
                "(Stand: %d.%m.%Y, %H:%M Uhr)")).timestamp())
    return data

def main():
    print(json.dumps(get_data(ids)))

if __name__ == "__main__":
    main()
