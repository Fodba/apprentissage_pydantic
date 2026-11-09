import requests
from rich import print
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from schemas.ville_schema import VilleSchema
from models.ville import Ville


def coordonnees_ville(http_session,nom:str):
    """Permet de récupérer les coordonnées d'un ville

    Args:
        nom (str): nom de la ville
    """
    try:
        geo = http_session.get("https://geocoding-api.open-meteo.com/v1/search",
                params={"name": nom, "count": 1, "language": "fr"},
                timeout=(3, 10))
        geo.raise_for_status()
        geolocalisation = geo.json()
        if geolocalisation.get("results"):
            loc = geolocalisation["results"][0]
            return loc
        else:
            print(f"La ville '{nom}' n'est pas référencée")
            return None
    except requests.exceptions.Timeout as te:
        print(f"ville: {nom} - {te}")
        return None
    except requests.exceptions.ConnectionError as ce:
        print(f"ville: {nom} - {ce}")
        return None
    except requests.exceptions.HTTPError as he:
        print(f"ville: {nom} - {he}")
        return None
    except requests.exceptions.RequestException as re:
        print(f"ville: {nom} - {re}")
        return None



def chercher_ville(session: Session, ville):
    """Renvoie une ville si elle est présente en base de données"""
    requete = select(Ville).where(func.lower(Ville.nom) == ville.lower())
    ville_recu = session.scalar(requete)
    # print_ville(ville_recu)
    return ville_recu

def lister_villes(session: Session):
    """liste toutes les villes de la base de données"""
    requete = select(Ville)
    villes = session.scalars(requete).all()
    return villes


def inserer_ville(session: Session, ville):
    """insère une ville dans la base de données"""
    coordonnees = VilleSchema.model_validate(ville)
    
    result = chercher_ville(session,coordonnees.nom)

    if result is None:
        coor = coordonnees.model_dump()
        ville_actuelle = Ville(**coor)
        session.add(ville_actuelle)
        session.commit()
        return ville_actuelle
    else:
        return result
