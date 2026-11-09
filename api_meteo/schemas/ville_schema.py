from pydantic import BaseModel, Field


class VilleSchema(BaseModel):
    """schema des données de Ville reçue de l'API Open-Meteo"""
    nom: str = Field(alias="name",max_length=50)
    latitude:float = Field(ge=-90,le=90)
    longitude:float = Field(ge=-180,le=180)


class VilleReponse(BaseModel):
    """Schema d'une ville de la réponse FastAPI au client"""
    id: int
    nom: str
    latitude: float
    longitude: float
