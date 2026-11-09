
from sqlalchemy import Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from core.database import Base
from .ville import Ville


class Releve(Base):
    __tablename__ = "releves"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    temperature: Mapped[float] = mapped_column(Float,nullable=False)
    vitesse_vent: Mapped[float] = mapped_column(Float,nullable=False)
    date_heure: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    ville_id: Mapped[int] = mapped_column(ForeignKey("villes.id"),nullable=False)