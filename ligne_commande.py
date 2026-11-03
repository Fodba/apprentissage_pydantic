from decimal import Decimal

from pydantic import BaseModel, Field


class LigneCommande(BaseModel):
    produit_id: int = Field(gt=0)
    quantite: int = Field(gt=0, le=100)  # entre 1 et 100 articles
    prix_unitaire: Decimal = Field(ge=0)  # gratuit à la rigueur, mais jamais négatif
