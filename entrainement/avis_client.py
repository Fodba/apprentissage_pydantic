import json
from typing import Literal

from pydantic import BaseModel, Field


class AvisClient(BaseModel):
    """Avis laissé par un client sur un produit."""

    produit_id: int = Field(gt=0, description="Identifiant du produit évalué")
    note: int = Field(ge=1, le=5, description="Note de 1 (mauvais) à 5 (excellent)")
    sentiment: Literal["positif", "neutre", "négatif"]
    commentaire: str | None = Field(default=None, max_length=500)


print(json.dumps(AvisClient.model_json_schema(), indent=2, ensure_ascii=False))