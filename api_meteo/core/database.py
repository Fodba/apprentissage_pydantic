from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DATABASE_URL

# check_same_thread est nécessaire uniquement pour SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """envoie et maintient la session jusqu'à la fin du traitement de la requête FastAPI"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class Base(DeclarativeBase):
    pass
