from decimal import Decimal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


class Produit(BaseModel):
    """Un produit du catalogue Pixel & Co."""

    reference: str | None = Field(min_length=2, pattern=r"^PX-[a-zA-Z0-9]{1,4}$")
    nom: str = Field(min_length=2)
    # prix: float | None
    prix: Decimal | None = Field(gt=0,decimal_places=2)
    # remise: float = None # la valeur par défaut est obligatoire pour rendre le champ facultatif
    remise: float = Field(gt=0,default=0)
    stock: int = 0

    @field_validator("stock","prix","remise")
    @classmethod
    def positif(cls, valeur:int|Decimal):
        """Vérifie que la valeur entrée est strictement positive.

        Args:
            valeur (int|Decimal): valeur à évaluer

        Returns:
            la valeur vérifiée
        
        Raises:
            ValueError: Si la valeur est négative
        """
        if valeur is not None and valeur < 0:
            raise ValueError("La valeur doit être strictement positive")
        return valeur


    @model_validator(mode="after")
    def remise_cohérente(self):
        """Le remise ne doit pas être supérieure au prix."""
        if self.remise > self.prix:
            raise ValueError("La remise doit être inférieure au prix")
        return self
