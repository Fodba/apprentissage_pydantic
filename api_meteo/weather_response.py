from datetime import datetime

from pydantic import BaseModel, Field



def sep(nombre=50):
    print("=" * nombre)


class CurrentWeather(BaseModel):
    time: datetime
    interval: int
    temperature: float
    windspeed: float = Field(ge=0)
    winddirection: int = Field(ge=0,le=360)
    is_day: bool
    weathercode: int


class WeatherResponseModel(BaseModel):
    latitude:float = Field(ge=-90,le=90)
    longitude:float = Field(ge=-180,le=180)
    elevation:float
    timezone:str
    timezone_abbreviation:str
    current_weather : CurrentWeather


