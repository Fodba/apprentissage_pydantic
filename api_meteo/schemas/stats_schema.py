from pydantic import BaseModel


class StatVille(BaseModel):
    """Schema des statistique de la réponse FastAPI au client"""

    nom: str
    releves : int
    minimum: float
    maximum: float
    moyenne: float
