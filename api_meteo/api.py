from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db

from services.releve_service import lister_releves
from services.stats_service import stats_temperature
from services.ville_service import chercher_ville, lister_villes

from schemas.releve_schema import ReleveReponse
from schemas.stats_schema import StatVille
from schemas.ville_schema import VilleReponse

app = FastAPI()


@app.get("/")
def hello_world():
    """route de test"""
    return {
        "message": "hello world !",
    }


# @app.get("/villes")
# def liste_villes(session: Session = Depends(get_db)) -> list[VilleReponse]:
# Les deux lignes précédentes sont équivalentes aux deux suivantes
@app.get("/villes", response_model=list[VilleReponse])
def liste_villes(session: Session = Depends(get_db)):
    """Liste toutes les villes de la base de données"""
    villes = lister_villes(session)
    return villes


@app.get("/meteo/{ville}")
def meteo_ville(ville: str, session: Session = Depends(get_db)) -> list[ReleveReponse]:
    """Donne la météo d'une ville"""
    ville_recherche = chercher_ville(session, ville)
    
    if ville_recherche is None:
        raise HTTPException(
            status_code=404,
            detail="La ville demandée n'est pas inscrite dans notre base de données",
        )
    meteo = lister_releves(session, ville_recherche)
    
    if not meteo:
        raise HTTPException(
            status_code=404,
            detail="La ville demandée n'a pas de relevés dans notre base de données",
        )
    return meteo


@app.get("/stats")
def stats_villes(session: Session = Depends(get_db)) -> list[StatVille]:
    """Donne les stats pour toutes les villes de la base de données"""
    stats = stats_temperature(session)
    return stats
