
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Ville(Base):
    __tablename__ = "villes"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(50), unique=True,nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)