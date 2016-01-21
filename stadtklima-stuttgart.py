#!/usr/bin/env python
url = "http://www.stadtklima-stuttgart.de/index.php?luft_messdaten_station_smz"

import requests
from bs4 import BeautifulSoup
import datetime as dt
from pytz import timezone
import json


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
    "Windgeschwindigkeit:":"wind",
    #"Windrichtung:",
    "Relative Luftfeuchte:":"humidity",
    "Absoluter Luftdruck: (in 250 m Messhöhe üNN)":"pressure_abs",
    "Relativer Luftdruck: (bisher ohne interaktiver Auswertung)":"pressure",
    "Niederschlag:" :"rain",
    "Globalstrahlung:":"global_radiation",
    "Strahlungsbilanz:":"radiation_balance",
    "UV-A Strahlung:":"UV-A",
    "UV-B Strahlung:":"UV-B" }



data = {}
ret = requests.get(url)
s = BeautifulSoup(ret.text,"html.parser")
for row in s.find_all("tr"):
    try:
        left = row.find(align="left").string
        right = row.find(align="right").string
        if left and left in fields:
            data[fields[left]] = float(right.strip().split(" ")[0])

    except:pass

for v in fields.values():
    if not v in data:
        print(v + " is missing")
def starts_with_stand(s):
    return s.string.startswith("(Stand")
timestring = s.find("b",string=starts_with_stand).string
data["ts"] = timezone("Europe/Berlin").localize(
        dt.datetime.strptime(timestring,"(Stand: %d.%m.%Y, %H:%M Uhr)")).timestamp()

print(json.dumps(data))
