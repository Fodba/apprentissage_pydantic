# https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true



# from urllib import request
import sqlite3

import requests

import collections
import datetime as DT
import pytz

from db import Connection_bdd
from weather_response import WeatherResponseModel

# def connecter_bdd(bdd):
#     with open(bdd, 'r') as sql_file:
#         sql_script = sql_file.read()
#     connection = sqlite3.connect("ma_bdd.db")
#     cursor = connection.cursor()
#     return connection, cursor, sql_script

def sep(nombre=50):
    print("=" * nombre)

latitude = 48.85
longitude = 2.35

link = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

response = requests.get(link)
print(response.text)
new_response = WeatherResponseModel.model_validate_json(response.text)
sep()
print(new_response.model_dump_json())

ma_connection = Connection_bdd("ma_bdd.db")
# connecter_bdd("ma_bdd.db")

# conn = sqlite3.connect("ma_base.db")
# cursor = conn.cursor()
sep()

tables = ma_connection.execute_requete(
    # "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    "SELECT name FROM sqlite_master;"
)
# tables = ma_connection.cursor.fetchall()

print(tables)
# for table in tables:
#   print(table[0])
sep()
ma_connection.connection.close()


































# tzones = collections.defaultdict(set)
# abbrevs = collections.defaultdict(set)

# zones = collections.defaultdict(set)

# for name in pytz.all_timezones:
#     tzone = pytz.timezone(name)
#     for utcoffset, dstoffset, tzabbrev in getattr(
#             tzone, '_transition_info', [[None, None, DT.datetime.now(tzone).tzname()]]):
#         # tzones[tzabbrev].add(name)
#         abbrevs[name].add(tzabbrev)
#     zones[name] = (tzone, abbrevs[name])
    # print(f"{name} - {tzone} - {abbrevs[name]}")
    # sep()
# print(len(pytz.all_timezones))
# print(pytz.all_timezones_set)

# for zone in tzones:
#     print(zone)
# sep()
# # for abbr in abbrevs:
# #     print(abbr)
# print(len(abbrevs))
# print(len(tzones))
# if len(tzones) == len(abbrevs):
#     for i in range(len(tzones)):
#         print(f"abbr: {abbrevs[i]} - timezone: {tzones[i]}")