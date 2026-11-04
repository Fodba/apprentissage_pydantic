from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Literal
from client import Client

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

from ligne_commande import LigneCommande


class StatutCommande(str, Enum):
    EN_COURS = "en cours"
    EXPEDIEE = "expédiée"
    LIVREE = "livrée"
    ANNULEE = "annulée"


class Commande(BaseModel):
    id: int
    client: Client = None
    date_commande: date = Field(default_factory=date.today)
    date_livraison: date = None
    # statut: Literal["en cours", "expédiée", "livrée", "annulée"] = "en cours"
    statut: StatutCommande = StatutCommande.EN_COURS
    lignes: list[LigneCommande] = Field(min_length=1, default_factory=None)     # une liste de modèles, avec au moins 1 élément
    
    @computed_field
    @property
    def total(self) -> Decimal:
        """Montant total de la commande."""
        return sum(ligne.montant for ligne in self.lignes)



    @field_validator("date_commande", "date_livraison", mode="before")
    @classmethod
    def accepter_date_francaise(cls, valeur):
        """Convertit 'JJ/MM/AAAA' en date. Tout le reste est transmis tel quel à Pydantic."""
        if isinstance(valeur, str) and "/" in valeur:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        if isinstance(valeur, str) and "-" in valeur and valeur[2] == "-":
            print(valeur)
            return datetime.strptime(valeur.strip(), "%d-%m-%Y").date()
        return valeur

    @model_validator(mode="after")
    def dates_coherentes(self):
        """La livraison ne peut pas précéder la commande, et une commande livrée a une date de livraison."""
        if self.date_livraison is not None and self.date_livraison < self.date_commande:
            raise ValueError("la date de livraison précède la date de commande")
        if self.statut == "livrée" and self.date_livraison is None:
            raise ValueError("une commande livrée doit avoir une date de livraison")
        return self