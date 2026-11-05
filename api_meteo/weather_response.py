import collections
from datetime import datetime
from decimal import Decimal
from typing import Literal
import pytz
import datetime as DT

from pydantic import BaseModel, Field, field_validator, model_validator



def sep(nombre=50):
    print("=" * nombre)

def afficher_erreurs(erreur,nombre=50):
    """Résume une ValidationError : une ligne par problème."""
    print(f"{erreur.error_count()} erreur(s) pour le modèle {erreur.title}")
    for err in erreur.errors():
        # loc est un tuple : on le transforme en chemin lisible
        champ = " → ".join(str(element) for element in err["loc"]) or "(modèle entier)"
        print(f"  ❌ {champ} : {err['msg']} [reçu : {err['input']!r}]")
    sep(nombre)

def get_tz():
    tzones = collections.defaultdict(set)
    abbrevs = collections.defaultdict(set)

    zones = []

    for name in pytz.all_timezones:
        # tzone = pytz.timezone(name)
        zones.append(name)
        # for utcoffset, dstoffset, tzabbrev in getattr(
        #         tzone, '_transition_info', [[None, None, DT.datetime.now(tzone).tzname()]]):
        #     # tzones[tzabbrev].add(name)
        #     abbrevs[name].add(tzabbrev)

    # print(zones)
    return zones

def get_abbr():
    tzones = collections.defaultdict(set)
    abbrevs = collections.defaultdict(set)

    zones = collections.defaultdict()

    for name in pytz.all_timezones:
        tzone = pytz.timezone(name)
        for utcoffset, dstoffset, tzabbrev in getattr(
                tzone, '_transition_info', [[None, None, DT.datetime.now(tzone).tzname()]]):
            # tzones[tzabbrev].add(name)
            abbrevs[name].add(tzabbrev)
        zones[name] = (name, abbrevs[name])

    # print(zones)
    return zones


TIMEZONE_SET = pytz.all_timezones_set



class CurrentWeather(BaseModel):
    time: datetime
    interval: int
    temperature: float
    windspeed: float = Field()
    winddirection: int
    is_day: bool
    weathercode: int


    @field_validator("time", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        if isinstance(valeur, str) and "-" in valeur and valeur[2] == "-":
            print(valeur)
            return datetime.strptime(valeur.strip(), "%d-%m-%Y").date()
        return valeur


class WeatherResponseModel(BaseModel):
    latitude:float=None
    longitude:float=None
    elevation:Decimal=None
    timezone:str
    timezone_abbreviation:str
    current_weather : CurrentWeather


    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls,valeur):
        """Vérifie que la timezone existe."""
        # if valeur not in pytz.all_timezones_set:
        if valeur not in get_tz():
            raise ValueError("Cette timezone n'existe pas")
        return valeur

    @model_validator(mode="after")
    def valid_abbr(self):
        zone = get_abbr()[self.timezone]
        print(zone)
        if self.timezone_abbreviation not in zone[1]:
            raise ValueError("Cette abbreviation est incorrecte")
        return self


# try:
#     w = WeatherResponseModel(timezone="UTC")
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# try:
#     w = WeatherResponseModel(timezone="gmt")
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# try:
#     w = WeatherResponseModel(timezone="GMT",timezone_abbreviation="GMT")
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# try:
#     w = WeatherResponseModel(timezone="GB",timezone_abbreviation="GMT")
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# try:
#     w = WeatherResponseModel(timezone="CST")
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# try:
#     w = CurrentWeather(
#         time="2022-07-01T00:00",
#         interval=200,
#         temperature=15.6,
#         windspeed=12,
#         winddirection=3,
#         is_day=1,
#         wheatercode=3
#     )
#     print(w)
#     sep()
# except ValueError as ve:
#     afficher_erreurs(ve) 

# # get_tz_and_abbr()