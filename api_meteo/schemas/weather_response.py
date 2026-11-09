from datetime import datetime

from pydantic import BaseModel, Field


class CurrentWeather(BaseModel):
    """format attendu d'une ligne de relevé météo"""
    time: datetime
    interval: int
    temperature: float
    windspeed: float = Field(ge=0)
    winddirection: int = Field(ge=0,le=360)
    is_day: bool
    weathercode: int


class WeatherResponseModel(BaseModel):
    """format attendu de la réponse de l'API météo pour une ville"""
    latitude:float = Field(ge=-90,le=90)
    longitude:float = Field(ge=-180,le=180)
    elevation:float
    timezone:str
    timezone_abbreviation:str
    current_weather : CurrentWeather
