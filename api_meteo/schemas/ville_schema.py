
from pydantic import BaseModel, Field


class VilleSchema(BaseModel):
    
    nom: str = Field(alias="name",max_length=50)
    latitude:float = Field(ge=-90,le=90)
    longitude:float = Field(ge=-180,le=180)