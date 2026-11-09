from datetime import datetime

from pydantic import BaseModel, Field

# from models.ville import Ville


class ReleveSchema(BaseModel):

    temperature: float 
    vitesse_vent: float = Field(alias="windspeed",ge=0)
    date_heure: datetime  = Field(alias="time")
    # ville: Ville
