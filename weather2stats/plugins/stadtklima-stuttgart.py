#!/usr/bin/env python3

urls = [ "http://www.stadtklima-stuttgart.de/index.php?luft_messdaten_station_smz",
         "http://www.stadtklima-stuttgart.de/index.php?luft_messdaten_station_gsg" ]
urls = [ "http://localhost:8000/messdate_gsg",
         "http://localhost:8000/messdaten_smz" ]
top_key = "weather.stadtklima-stuttgart."

import requests
from bs4 import BeautifulSoup
import datetime as dt
from pytz import timezone
import json
import logging as log

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
    "Windgeschwindigkeit:":"wind_speed",
    "Windrichtung:":"wind_direction",
    "Relative Luftfeuchte:":"humidity",
    "Absoluter Luftdruck: (in 250 m Messhöhe üNN)":"pressure_abs",
    "Relativer Luftdruck: (bisher ohne interaktiver Auswertung)":"pressure",
    "Niederschlag:" :"rain",
    "Globalstrahlung:":"uv_intensity",
    "Strahlungsbilanz:":"radiation_balance",
    "UV-A Strahlung:":"UV-A",
    "UV-Index:":"uv_index",
    "UV-B Strahlung:":"UV-B"
    }

mapping = {
    "gsg" : "geschwister-scholl gymnasium",
    "smz" : "schwabenzentrum" }


def get_data(url):
    log.warn("Fetching " + url)
    name = mapping[url.split("_")[-1]]
    data = {
        "name": name
    }
    base_key = top_key + name + "."
    ret = requests.get(url).text
    s = BeautifulSoup(ret,"html.parser")

    # TODO: will match for gsg the weather data from smz
    for row in s.find_all("tr"):
        try:
            left = row.find(align="left").string
            right = row.find(align="right").string
            if left and left in fields:
                data[fields[left]] = float(right.strip().split(" ")[0])
            else:
                log.warn(left + " is not mapped")

        except:pass

    for v in fields.values():
        if not v in data:
            log.warn(v + " is missing")
    def starts_with_stand(s):
        return s.string.startswith("(Stand")
    timestring = s.find("b",string=starts_with_stand).string

    ts = int(timezone("Europe/Berlin").localize(
            dt.datetime.strptime(timestring,
                "(Stand: %d.%m.%Y, %H:%M Uhr)")).timestamp())
    return data

def main():
    print(json.dumps([get_data(url) for url in urls]))
    #graphite.send_all_data(d,host=host)

if __name__ == "__main__":
    main()
