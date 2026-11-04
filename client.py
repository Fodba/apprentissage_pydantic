from pydantic import BaseModel, EmailStr, Field, field_validator


class Client(BaseModel):
    prenom: str = Field(min_length=1, max_length=50)
    nom: str = Field(min_length=1, max_length=50)
    email: EmailStr
    telephone: str | None = None
    ville: str = Field(min_length=1, max_length=50)

    @field_validator("prenom", "nom", "ville")
    @classmethod
    def nom_propre(cls, valeur: str) -> str:
        """Refuse les chiffres, puis normalise : '  DUPONT ' devient 'Dupont'."""
        if any(caractere.isdigit() for caractere in valeur):
            raise ValueError("ne doit pas contenir de chiffre")
        return valeur.strip().title()

    @field_validator("email")
    @classmethod
    def email_en_minuscules(cls, valeur: str) -> str:
        return valeur.lower()

    @field_validator("telephone")
    @classmethod
    def telephone_normalise(cls, valeur: str | None) -> str | None:
        """Ramène un numéro français au format '06 12 34 56 78'."""
        if valeur is None:
            return None
        chiffres = "".join(caractere for caractere in valeur if caractere.isdigit())
        if len(chiffres) == 11 and chiffres.startswith("33"):   # +33 6 12... devient 06 12...
            chiffres = "0" + chiffres[2:]
        if len(chiffres) != 10 or not chiffres.startswith("0"):
            raise ValueError("numéro de téléphone français attendu (10 chiffres)")
        return " ".join(chiffres[i:i + 2] for i in range(0, 10, 2))