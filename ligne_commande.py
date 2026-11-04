from decimal import Decimal

from pydantic import BaseModel, Field, computed_field


class LigneCommande(BaseModel):
    produit_id: int = Field(gt=0)
    quantite: int = Field(gt=0, le=100)  # entre 1 et 100 articles
    prix_unitaire: Decimal = Field(ge=0,decimal_places=2)  # gratuit à la rigueur, mais jamais négatif

    @computed_field
    @property
    # def montant(self):# -> Decimal: Ne fonctionne pas si le type de retour n'est pas renseigné
    def montant(self) -> Decimal: # la déclaration du type de retour est obligatoire.
        """Montant de la ligne (toujours à jour, jamais stocké)."""
        return self.quantite * self.prix_unitaire