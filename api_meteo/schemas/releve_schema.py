from datetime import datetime

from pydantic import BaseModel, Field


class ReleveSchema(BaseModel):
    """schema des données de Releve reçue de l'API Open-Meteo"""

    temperature: float
    vitesse_vent: float = Field(alias="windspeed", ge=0)
    date_heure: datetime = Field(alias="time")


class ReleveReponse(BaseModel):
    """Schema d'un relevé de la réponse FastAPI au client"""

    id: int
    temperature: float
    vitesse_vent: float
    date_heure: datetime = Field(description="Heure GMT")
