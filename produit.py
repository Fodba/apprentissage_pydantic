from decimal import Decimal

from pydantic import BaseModel, Field, ValidationError


class Produit(BaseModel):
    """Un produit du catalogue Pixel & Co."""

    reference: str | None = Field(min_length=2, pattern=r"^PX-[a-zA-Z0-9]{1,4}$")
    nom: str = Field(min_length=2)
    # prix: float | None
    prix: Decimal | None
    remise: float = None # la valeur par défaut est obligatoire pour rendre le champ facultatif
    remise: float = Field(gt=0,default=None)
    stock: int = 0
