from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class StatutCommande(str, Enum):
    EN_COURS = "en cours"
    EXPEDIEE = "expédiée"
    LIVREE = "livrée"
    ANNULEE = "annulée"


class Commande(BaseModel):
    id: int
    date_commande: date = Field(default_factory=date.today)
    enregistree_le: datetime = None
    # statut: Literal["en cours", "expédiée", "livrée", "annulée"] = "en cours"
    statut: StatutCommande = StatutCommande.EN_COURS
